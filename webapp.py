"""
webapp.py: the web server behind the chat page (web/index.html).

HOW TO RUN
----------
    conda activate gis-llm
    python app.py              # starts this server and prints the address
    (or: uvicorn webapp:app --port 7860)

WHAT IT DOES
------------
The page in web/ is plain HTML + CSS + JavaScript (no internet needed). It talks
to this server:

    GET  /                 the chat page
    GET  /api/status       model, whether the model is on the GPU
    POST /api/chat         ask a question; the answer STREAMS back as events,
                           one JSON object per line ("step", "code", "answer",
                           "map", ...), so the page can show each step as it happens
    POST /api/place        switch the conversation to another place
    POST /api/reset        forget a conversation
    POST /api/open_qgis    open the conversation's results in QGIS Desktop
    GET  /files/...        the maps and result files the agent saved (outputs/)

Each conversation (one per browser chat) has its own Agent: its own memory, its
own workspace and its own place. The language model and QGIS are shared, so
only one question is answered at a time (a lock), which is also what a single
GPU can do.
"""

import json
import os
import threading
import uuid

from fastapi import FastAPI
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from qgis_agent import config, llm_client, qgis_engine

ROOT = os.path.dirname(os.path.abspath(__file__))
WEB = os.path.join(ROOT, "web")

app = FastAPI(title="QGIS Agent", docs_url="/api/docs")
_conversations = {}            # conversation id -> Agent
_busy = threading.Lock()       # one question at a time (one model, one QGIS)


class ChatRequest(BaseModel):
    conversation_id: str = ""
    message: str
    mode: str = ""             # ignored since 2026-11-24 (lookup only)


class PlaceRequest(BaseModel):
    conversation_id: str
    place: str


class ConversationRequest(BaseModel):
    conversation_id: str


def _agent(conversation_id):
    from qgis_agent.agent import Agent
    if conversation_id not in _conversations:
        _conversations[conversation_id] = Agent()
    return _conversations[conversation_id]


def _public(event):
    """Turn file paths in an event into links the page can open."""
    event = dict(event)
    if event.get("type") == "map":
        event["url"] = _file_url(event.pop("path"))
    elif event.get("type") == "files":
        event["files"] = [{"name": os.path.basename(p), "url": _file_url(p)}
                          for p in event.pop("paths")]
    return event


def _file_url(path):
    relative = os.path.relpath(os.path.abspath(path), config.OUTPUTS_DIR)
    return "/files/" + relative.replace(os.sep, "/")


def _stream(conversation_id, events):
    """Run the agent's events through the lock and send them as JSON lines."""
    def generate():
        yield json.dumps({"type": "conversation", "id": conversation_id}) + "\n"
        with _busy:
            agent = _agent(conversation_id)
            if agent.place is not None:
                from qgis_agent.agent import use_data_folder
                use_data_folder(agent.place.folder)     # several chats, one QGIS
            try:
                for event in events(agent):
                    if event.get("type") in ("draft",):
                        continue        # the page shows code and answers, not raw drafts
                    yield json.dumps(_public(event), ensure_ascii=False, default=str) + "\n"
            except Exception as exc:    # never leave the page waiting
                yield json.dumps({"type": "error", "text": f"{type(exc).__name__}: {exc}"}) + "\n"
            if agent.place is not None:
                yield json.dumps({"type": "place_state", "name": agent.place.name,
                                  "display": agent.place.display_name}) + "\n"
    return StreamingResponse(generate(), media_type="application/x-ndjson")


@app.get("/", include_in_schema=False)
def page():
    return FileResponse(os.path.join(WEB, "index.html"))


@app.get("/api/status")
def status():
    share = llm_client.gpu_share()
    return {"model": config.MODEL, "mode": config.PROMPT_MODE,
            "ollama": llm_client.is_available(),
            "gpu_share": share, "qgis": qgis_engine.qgis_version()}


@app.post("/api/chat")
def chat(request: ChatRequest):
    conversation_id = request.conversation_id or uuid.uuid4().hex

    def events(agent):
        yield from agent.respond(request.message.strip())
    return _stream(conversation_id, events)


@app.post("/api/place")
def place(request: PlaceRequest):
    return _stream(request.conversation_id, lambda agent: agent.choose_place(request.place))


@app.post("/api/reset")
def reset(request: ConversationRequest):
    _conversations.pop(request.conversation_id, None)
    return {"ok": True}


@app.post("/api/open_qgis")
def open_qgis(request: ConversationRequest):
    agent = _conversations.get(request.conversation_id)
    if agent is None:
        return {"message": "There are no results to open yet. Ask a question first."}
    return {"message": agent.open_in_qgis()}


os.makedirs(config.OUTPUTS_DIR, exist_ok=True)
app.mount("/files", StaticFiles(directory=config.OUTPUTS_DIR), name="files")
app.mount("/static", StaticFiles(directory=WEB), name="static")
