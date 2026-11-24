/* QGIS Agent chat page.
 *
 * How it works:
 *  - Each chat has an id. The server keeps one Agent per id (its memory, its place).
 *  - Sending a question POSTs to /api/chat. The answer STREAMS back as one JSON
 *    event per line: "step" (what the agent is doing), "code", "run" (what the
 *    code printed), "progress" (downloads), "place", "answer", "map", "files", "done".
 *  - Each event updates the bot message on screen as it arrives.
 *  - Chats are saved in the browser (localStorage), so they survive a reload.
 */

const $ = (id) => document.getElementById(id);
const ICON = {
  pin: '<svg viewBox="0 0 24 24"><path d="M12 2.5c-3.6 0-6.5 2.9-6.5 6.5 0 4.8 6.5 12.5 6.5 12.5s6.5-7.7 6.5-12.5c0-3.6-2.9-6.5-6.5-6.5zm0 9.2a2.7 2.7 0 110-5.4 2.7 2.7 0 010 5.4z"/></svg>',
  check: '<svg viewBox="0 0 24 24"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>',
  cross: '<svg viewBox="0 0 24 24"><path d="M6 6l12 12M18 6L6 18"/></svg>',
  chev: '<svg class="chev" viewBox="0 0 24 24"><path d="M7 10l5 5 5-5"/></svg>',
  copy: '<svg viewBox="0 0 24 24"><rect x="9" y="9" width="11" height="11" rx="2"/><path d="M5 15V5a1 1 0 011-1h10"/></svg>',
  file: '<svg viewBox="0 0 24 24"><path d="M14 3H7a1 1 0 00-1 1v16a1 1 0 001 1h10a1 1 0 001-1V7z"/><path d="M14 3v4h4"/></svg>',
  trash: '<svg viewBox="0 0 24 24"><path d="M5 7h14M10 7V5h4v2M7 7l1 12h8l1-12"/></svg>',
  sparkle: '<svg viewBox="0 0 24 24"><path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5L18 18M6 18l2.5-2.5M15.5 8.5L18 6"/></svg>',
};

const EXAMPLES = [
  { tag: "Count", text: "How many hospitals are there in Sharjah? Only hospitals, not clinics." },
  { tag: "Map", text: "Show me the schools in Cairo that are more than 2 km from any hospital." },
  { tag: "Heatmap", text: "Make a heatmap of the pharmacies in Berlin." },
  { tag: "Population", text: "How many people in Sharjah live within 1 km of a hospital or clinic?" },
  { tag: "Terrain", text: "Show me a map of how steep the ground is in Sharjah." },
  { tag: "Distance", text: "On average, how far is a school in Berlin from its nearest hospital?" },
];

/* ---------------- state ---------------- */
const store = {
  load() { try { return JSON.parse(localStorage.getItem("qgis-agent-chats") || "[]"); } catch { return []; } },
  save(chats) { try { localStorage.setItem("qgis-agent-chats", JSON.stringify(chats.slice(0, 40))); } catch {} },
};
let chats = store.load();          // [{id, title, place, messages:[{role, text, answer, map, files, code, work}]}]
let current = null;                // the open chat
let controller = null;             // to stop a running answer

function newId() { return (crypto.randomUUID ? crypto.randomUUID() : String(Date.now()) + Math.random()).replace(/-/g, ""); }
function openChat(chat) {
  current = chat;
  renderHistory();
  renderThread();
  setPlace(chat.place || null);
}
function startNewChat() {
  const chat = { id: newId(), title: "New chat", place: current ? current.place : null, messages: [] };
  chats.unshift(chat);
  openChat(chat);
  closeSidebar();
  $("input").focus();
}

/* ---------------- rendering helpers ---------------- */
function esc(text) {
  return String(text ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
}
// Light formatting for answers: paragraphs, bullet lists, **bold**, `code`.
function formatAnswer(text) {
  const blocks = String(text || "").trim().split(/\n{2,}/);
  return blocks.map((block) => {
    const lines = block.split("\n");
    if (lines.every((l) => /^\s*([-*•]|\d+[.)])\s+/.test(l))) {
      return "<ul>" + lines.map((l) => "<li>" + inline(l.replace(/^\s*([-*•]|\d+[.)])\s+/, "")) + "</li>").join("") + "</ul>";
    }
    return "<p>" + lines.map(inline).join("<br>") + "</p>";
  }).join("");
}
function inline(text) {
  return esc(text).replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>").replace(/`([^`]+)`/g, "<code>$1</code>");
}
// A small Python highlighter (keywords, strings, numbers, comments, function calls).
function highlight(code) {
  const pattern = /(#[^\n]*)|("""[\s\S]*?"""|'''[\s\S]*?'''|"(?:\\.|[^"\\\n])*"|'(?:\\.|[^'\\\n])*')|\b(\d+(?:\.\d+)?)\b|\b(def|return|for|in|if|elif|else|import|from|as|with|while|not|and|or|None|True|False|lambda|try|except|print)\b|\b([A-Za-z_]\w*)(?=\()/g;
  let out = "", last = 0, m;
  while ((m = pattern.exec(code))) {
    out += esc(code.slice(last, m.index));
    const [all, com, str, num, kw, fn] = m;
    const cls = com ? "com" : str ? "str" : num ? "num" : kw ? "kw" : "fn";
    out += `<span class="tok-${cls}">${esc(all)}</span>`;
    last = m.index + all.length;
  }
  return out + esc(code.slice(last));
}
function codeBlock(code, label) {
  const wrap = document.createElement("div");
  wrap.className = "code";
  wrap.innerHTML = `<div class="code-head"><span>${esc(label)}</span><button type="button">${ICON.copy}Copy</button></div><pre>${highlight(code)}</pre>`;
  wrap.querySelector("button").onclick = (e) => copy(code, e.currentTarget);
  return wrap;
}
function copy(text, button) {
  navigator.clipboard?.writeText(text).then(() => {
    const old = button.innerHTML; button.innerHTML = ICON.check + "Copied";
    setTimeout(() => (button.innerHTML = old), 1200);
  });
}
function scrollDown(force) {
  const t = $("thread");
  if (force || t.scrollHeight - t.scrollTop - t.clientHeight < 160) t.scrollTop = t.scrollHeight;
}

/* ---------------- one bot message ---------------- */
class BotMessage {
  constructor(saved) {
    this.el = document.createElement("div");
    this.el.className = "msg bot";
    this.el.innerHTML = `<div class="avatar">${ICON.pin}</div><div class="bot-body"></div>`;
    this.body = this.el.querySelector(".bot-body");
    this.data = saved || { role: "bot", answer: "", map: null, files: [], code: "", work: [], seconds: null, note: "" };
    this.started = Date.now();
    if (saved) this.restore(); else this.thinking();
  }
  thinking() {
    this.work = document.createElement("details");
    this.work.className = "work";
    this.work.innerHTML = `<summary><span class="spinner"></span><span class="work-title">Working…</span>${ICON.chev}</summary><div class="work-list"></div>`;
    this.list = this.work.querySelector(".work-list");
    this.answerEl = document.createElement("div");
    this.answerEl.className = "answer";
    this.answerEl.innerHTML = '<span class="typing"><i></i><i></i><i></i></span>';
    this.body.append(this.work, this.answerEl);
  }
  setTitle(text) { const t = this.work?.querySelector(".work-title"); if (t) t.textContent = text; }
  finishPending(ok = true) {
    this.list?.querySelectorAll(".step.pending").forEach((s) => {
      s.classList.remove("pending"); s.classList.add(ok ? "done" : "fail");
      s.querySelector(".icon").innerHTML = ok ? ICON.check : ICON.cross;
    });
  }
  addStep(title) {
    this.finishPending(true);
    const step = document.createElement("div");
    step.className = "step pending";
    step.innerHTML = `<span class="icon"><span class="spinner"></span></span><span>${esc(title)}</span>`;
    this.list.append(step);
    this.setTitle(title + "…");
    this.data.work.push({ kind: "step", text: title });
  }
  addCode(code, attempt) {
    this.list.append(codeBlock(code, attempt > 1 ? `Python · attempt ${attempt}` : "Python"));
    this.data.code = code;
    this.data.work.push({ kind: "code", text: code, attempt });
  }
  addRun(ok, text) {
    if (!text) return;
    const out = document.createElement("div");
    out.className = "output" + (ok ? "" : " err");
    out.textContent = text.length > 4000 ? text.slice(0, 4000) + "\n…" : text;
    this.list.append(out);
    this.data.work.push({ kind: ok ? "out" : "err", text: out.textContent });
  }
  addProgress(text) {
    if (!this.progress) {
      this.progress = document.createElement("div");
      this.progress.className = "progress-lines";
      this.list.append(this.progress);
    }
    this.progress.textContent += text + "\n";
    this.progress.scrollTop = this.progress.scrollHeight;
    this.setTitle(text.slice(0, 80));
  }
  setAnswer(text) {
    this.data.answer = text;
    this.answerEl.innerHTML = formatAnswer(text);
  }
  setNote(text) {
    this.data.note = text;
    const n = document.createElement("div");
    n.className = "note"; n.textContent = text;
    this.answerEl.after(n);
  }
  addMap(url) {
    this.data.map = url;
    const m = document.createElement("div");
    m.className = "map";
    m.innerHTML = `<img src="${esc(url)}" alt="Map of the result">`;
    m.onclick = () => openLightbox(url);
    this.body.append(m);
  }
  addFiles(files) {
    this.data.files = files;
    const f = document.createElement("div");
    f.className = "files";
    f.innerHTML = files.map((x) => `<a class="file" href="${esc(x.url)}" download>${ICON.file}${esc(x.name)}</a>`).join("");
    this.body.append(f);
  }
  error(text) {
    this.finishPending(false);
    this.answerEl.innerHTML = `<p class="error-text">${esc(text)}</p>`;
    this.data.answer = text;
  }
  done(seconds) {
    this.finishPending(true);
    if (this.answerEl.querySelector(".typing")) this.answerEl.innerHTML = "";
    const steps = this.data.work.filter((w) => w.kind === "step").length;
    this.data.seconds = seconds ?? (Date.now() - this.started) / 1000;
    const summary = this.work.querySelector("summary");
    summary.innerHTML = `${ICON.sparkle}<span>Worked for ${Math.round(this.data.seconds)} s · ${steps} step${steps === 1 ? "" : "s"}</span>${ICON.chev}`;
    if (!steps && !this.data.code) this.work.remove();
    this.meta();
  }
  meta() {
    const meta = document.createElement("div");
    meta.className = "meta";
    meta.innerHTML = `<button type="button" title="Copy answer">${ICON.copy}</button>`;
    meta.querySelector("button").onclick = (e) => copy(this.data.answer, e.currentTarget);
    this.body.append(meta);
  }
  restore() {
    // Rebuild a saved message (after a reload): work panel, answer, map, files.
    this.thinking();
    for (const w of this.data.work || []) {
      if (w.kind === "step") {
        const step = document.createElement("div");
        step.className = "step done";
        step.innerHTML = `<span class="icon">${ICON.check}</span><span>${esc(w.text)}</span>`;
        this.list.append(step);
      } else if (w.kind === "code") this.list.append(codeBlock(w.text, w.attempt > 1 ? `Python · attempt ${w.attempt}` : "Python"));
      else { const o = document.createElement("div"); o.className = "output" + (w.kind === "err" ? " err" : ""); o.textContent = w.text; this.list.append(o); }
    }
    this.answerEl.innerHTML = formatAnswer(this.data.answer);
    if (this.data.note) { const n = document.createElement("div"); n.className = "note"; n.textContent = this.data.note; this.answerEl.after(n); }
    if (this.data.map) this.addMap(this.data.map);
    if (this.data.files?.length) this.addFiles(this.data.files);
    const steps = (this.data.work || []).filter((w) => w.kind === "step").length;
    this.work.querySelector("summary").innerHTML = `${ICON.sparkle}<span>Worked for ${Math.round(this.data.seconds || 0)} s · ${steps} step${steps === 1 ? "" : "s"}</span>${ICON.chev}`;
    if (!steps && !this.data.code) this.work.remove();
    this.meta();
  }
}

/* ---------------- thread & history ---------------- */
function renderThread() {
  const thread = $("thread");
  thread.innerHTML = "";
  if (!current.messages.length) {
    const w = document.createElement("div");
    w.className = "welcome";
    w.innerHTML = `<h1>Ask anything about a place.</h1>
      <p>Type a question in plain words. The agent writes QGIS code, runs it on real map data,
      checks the result and answers with a map. Name any city to start.</p><div class="examples"></div>`;
    const ex = w.querySelector(".examples");
    for (const e of EXAMPLES) {
      const b = document.createElement("button");
      b.className = "example"; b.type = "button";
      b.innerHTML = `<small>${esc(e.tag)}</small>${esc(e.text)}`;
      b.onclick = () => ask(e.text);
      ex.append(b);
    }
    thread.append(w);
    return;
  }
  for (const m of current.messages) {
    if (m.role === "user") thread.append(userBubble(m.text));
    else thread.append(new BotMessage(m).el);
  }
  scrollDown(true);
}
function userBubble(text) {
  const d = document.createElement("div");
  d.className = "msg user";
  d.innerHTML = `<div class="bubble">${esc(text)}</div>`;
  return d;
}
function renderHistory() {
  const h = $("history");
  h.innerHTML = "";
  for (const chat of chats) {
    if (!chat.messages.length && chat !== current) continue;
    const item = document.createElement("div");
    item.className = "history-item" + (chat === current ? " active" : "");
    item.innerHTML = `<span>${esc(chat.title)}</span><button class="del" title="Delete">${ICON.trash}</button>`;
    item.onclick = () => { openChat(chat); closeSidebar(); };
    item.querySelector(".del").onclick = (e) => {
      e.stopPropagation();
      chats = chats.filter((c) => c !== chat);
      fetch("/api/reset", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ conversation_id: chat.id }) });
      store.save(chats);
      if (chat === current) (chats[0] ? openChat(chats[0]) : startNewChat()); else renderHistory();
    };
    h.append(item);
  }
}
function setPlace(name) {
  $("placeName").textContent = name || "No place yet";
}

/* ---------------- talking to the server ---------------- */
async function stream(url, payload, bot) {
  controller = new AbortController();
  setBusy(true);
  try {
    const res = await fetch(url, { method: "POST", headers: { "Content-Type": "application/json" },
                                   body: JSON.stringify(payload), signal: controller.signal });
    if (!res.ok) throw new Error(`The server answered ${res.status}`);
    const reader = res.body.getReader();
    const decoder = new TextDecoder();
    let buffer = "";
    for (;;) {
      const { value, done } = await reader.read();
      if (done) break;
      buffer += decoder.decode(value, { stream: true });
      let nl;
      while ((nl = buffer.indexOf("\n")) >= 0) {
        const line = buffer.slice(0, nl).trim();
        buffer = buffer.slice(nl + 1);
        if (line) handle(JSON.parse(line), bot);
      }
    }
    if (!bot.data.seconds) bot.done();
  } catch (err) {
    if (err.name === "AbortError") { bot.error("Stopped."); bot.done(); }
    else { bot.error("Could not reach the agent: " + err.message); bot.done(); }
  } finally {
    setBusy(false);
    controller = null;
    store.save(chats);
    renderHistory();
  }
}
function handle(ev, bot) {
  switch (ev.type) {
    case "step": if (ev.status === "pending") bot.addStep(ev.title); break;
    case "code": bot.addCode(ev.code, ev.attempt); break;
    case "run": bot.addRun(ev.ok, ev.ok ? ev.output : ev.error); break;
    case "progress": bot.addProgress(ev.text); break;
    case "place": current.place = ev.name; setPlace(ev.name); if (ev.note) bot.setNote(ev.note); break;
    case "place_state": current.place = ev.name; setPlace(ev.name); break;
    case "answer": bot.setAnswer(ev.text); break;
    case "map": bot.addMap(ev.url); break;
    case "files": bot.addFiles(ev.files); break;
    case "error": bot.error(ev.text); break;
    case "done": bot.done(ev.seconds); break;
  }
  scrollDown();
}
function ask(text) {
  text = (text || "").trim();
  if (!text || controller) return;
  if (!current.messages.length) { current.title = text.length > 48 ? text.slice(0, 46) + "…" : text; $("thread").innerHTML = ""; }
  current.messages.push({ role: "user", text });
  $("thread").append(userBubble(text));
  const bot = new BotMessage();
  current.messages.push(bot.data);
  $("thread").append(bot.el);
  scrollDown(true);
  renderHistory();
  stream("/api/chat", { conversation_id: current.id, message: text }, bot);
}
function choosePlace(name) {
  if (!name || controller) return;
  if (!current.messages.length) $("thread").innerHTML = "";
  const text = `Use ${name}`;
  current.messages.push({ role: "user", text });
  $("thread").append(userBubble(text));
  const bot = new BotMessage();
  current.messages.push(bot.data);
  $("thread").append(bot.el);
  if (current.title === "New chat") current.title = text;
  stream("/api/place", { conversation_id: current.id, place: name }, bot);
}
function setBusy(busy) {
  $("send").classList.toggle("busy", busy);
  $("send").title = busy ? "Stop" : "Send";
}

/* ---------------- misc UI ---------------- */
function openLightbox(url) { $("lightboxImg").src = url; $("lightbox").hidden = false; }
function closeSidebar() { $("sidebar").classList.remove("open"); $("scrim").classList.remove("open"); }
function autosize() { const t = $("input"); t.style.height = "auto"; t.style.height = Math.min(t.scrollHeight, 200) + "px"; }
function applyTheme(theme) {
  if (theme) document.documentElement.dataset.theme = theme; else delete document.documentElement.dataset.theme;
}
async function refreshStatus() {
  try {
    const s = await (await fetch("/api/status")).json();
    const share = s.gpu_share;
    $("statusDot").className = "dot " + (share === null || share === undefined ? "warn" : share > 0.9 ? "ok" : "warn");
    $("statusText").textContent = `${s.model} · ${share === null || share === undefined ? "model not loaded yet" : Math.round(share * 100) + "% on GPU"}`;
  } catch {
    $("statusDot").className = "dot err";
    $("statusText").textContent = "Server not reachable";
  }
}

$("composer").addEventListener("submit", (e) => {
  e.preventDefault();
  if (controller) { controller.abort(); return; }
  const text = $("input").value;
  $("input").value = ""; autosize();
  ask(text);
});
$("input").addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey && !e.isComposing) { e.preventDefault(); $("composer").requestSubmit(); }
});
$("input").addEventListener("input", autosize);
$("newChat").onclick = startNewChat;
$("placeChip").onclick = () => { $("placeInput").value = ""; $("placeDialog").showModal(); $("placeInput").focus(); };
$("placeForm").addEventListener("submit", () => {
  if ($("placeDialog").returnValue !== "cancel") choosePlace($("placeInput").value.trim());
});
$("placeOk").onclick = () => { $("placeDialog").close("ok"); choosePlace($("placeInput").value.trim()); };
$("openQgis").onclick = async () => {
  const r = await (await fetch("/api/open_qgis", { method: "POST", headers: { "Content-Type": "application/json" },
                                                   body: JSON.stringify({ conversation_id: current.id }) })).json();
  alertNote(r.message);
};
function alertNote(text) {
  const bot = new BotMessage();
  bot.setAnswer(text); bot.done(0);
  $("thread").append(bot.el); scrollDown(true);
}
$("lightbox").onclick = () => ($("lightbox").hidden = true);
$("openSidebar").onclick = () => { $("sidebar").classList.add("open"); $("scrim").classList.add("open"); };
$("closeSidebar").onclick = closeSidebar;
$("scrim").onclick = closeSidebar;
$("themeToggle").onclick = () => {
  const dark = document.documentElement.dataset.theme === "dark" ||
    (!document.documentElement.dataset.theme && matchMedia("(prefers-color-scheme: dark)").matches);
  const next = dark ? "light" : "dark";
  applyTheme(next);
  try { localStorage.setItem("qgis-agent-theme", next); } catch {}
};

try { applyTheme(localStorage.getItem("qgis-agent-theme")); } catch {}
// Demo/screenshot helper: /#load=/files/demo_chat.json opens saved conversations
// (a JSON list in the same format the page stores). Used for the slides.
// Options after the file: &chat=<id> opens that conversation, &theme=light|dark.
async function start() {
  const params = new URLSearchParams(location.hash.slice(1));
  if (window.DEMO_CHATS) chats = window.DEMO_CHATS;          // embedded (screenshots)
  else if (params.get("load")) {
    try { chats = await (await fetch(params.get("load"))).json(); } catch {}
  }
  if (params.get("theme")) applyTheme(params.get("theme"));
  const wanted = chats.find((c) => c.id === params.get("chat"));
  if (wanted) openChat(wanted); else if (chats.length) openChat(chats[0]); else startNewChat();
}
start();
refreshStatus();
setInterval(refreshStatus, 30000);
