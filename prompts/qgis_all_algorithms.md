QGIS 3.44.11-Solothurn: 440 processing algorithms, grouped by provider and group.


## GDAL / Raster analysis

### gdal:aspect: Aspect
Parameters:
- INPUT [raster]: Input layer
- BAND [band]: Band number (default 1)
- TRIG_ANGLE [boolean]: Return trigonometric angle instead of azimuth (default False)
- ZERO_FLAT [boolean]: Return 0 for flat instead of -9999 (default False)
- COMPUTE_EDGES [boolean]: Compute edges (default False)
- ZEVENBERGEN [boolean]: Use Zevenbergen&Thorne formula instead of the Horn's one (default False)
- OPTIONS [string]: Additional creation options (optional)
- CREATION_OPTIONS [string]: Additional creation options (optional)
- EXTRA [string]: Additional command-line parameters (optional)
- OUTPUT [rasterDestination]: Aspect
Outputs: OUTPUT [outputRaster]

### gdal:colorrelief: Color relief
Parameters:
- INPUT [raster]: Input layer
- BAND [band]: Band number (default 1)
- COMPUTE_EDGES [boolean]: Compute edges (default False)
- COLOR_TABLE [file]: Color configuration file
- MATCH_MODE [enum]: Matching mode (default 2; options 0=Use strict color matching, 1=Use closest RGBA quadruplet, 2=Use smoothly blended colors)
- OPTIONS [string]: Additional creation options (optional)
- CREATION_OPTIONS [string]: Additional creation options (optional)
- EXTRA [string]: Additional command-line parameters (optional)
- OUTPUT [rasterDestination]: Color relief
Outputs: OUTPUT [outputRaster]

### gdal:fillnodata: Fill NoData
Parameters:
- INPUT [raster]: Input layer
- BAND [band]: Band number (default 1)
- DISTANCE [number]: Maximum distance (in pixels) to search out for values to interpolate (default 10)
- ITERATIONS [number]: Number of smoothing iterations to run after the interpolation (default 0)
- NO_MASK [boolean]: Do not use the default validity mask for the input band (optional; default False)
- MASK_LAYER [raster]: Validity mask (optional)
- OPTIONS [string]: Additional creation options (optional)
- CREATION_OPTIONS [string]: Additional creation options (optional)
- EXTRA [string]: Additional command-line parameters (optional)
- OUTPUT [rasterDestination]: Filled
Outputs: OUTPUT [outputRaster]

### gdal:gridaverage: Grid (Moving average)
Parameters:
- INPUT [source]: Point layer
- Z_FIELD [field]: Z value from field (optional)
- RADIUS_1 [number]: The first radius of search ellipse (default 0.0)
- RADIUS_2 [number]: The second radius of search ellipse (default 0.0)
- ANGLE [number]: Angle of search ellipse rotation in degrees (counter clockwise) (default 0.0)
- MIN_POINTS [number]: Minimum number of data points to use (default 0)
- NODATA [number]: NODATA marker to fill empty points (default 0.0)
- OPTIONS [string]: Additional creation options (optional)
- CREATION_OPTIONS [string]: Additional creation options (optional)
- EXTRA [string]: Additional command-line parameters (optional)
- DATA_TYPE [enum]: Output data type (default 5; options 0=Byte, 1=Int16, 2=UInt16, 3=UInt32, 4=Int32, 5=Float32, 6=Float64, 7=CInt16, 8=CInt32, 9=CFloat32, 10=CFloat64, 11=Int8)
- OUTPUT [rasterDestination]: Interpolated (moving average)
Outputs: OUTPUT [outputRaster]

### gdal:griddatametrics: Grid (Data metrics)
Parameters:
- INPUT [source]: Point layer
- Z_FIELD [field]: Z value from field (optional)
- METRIC [enum]: Data metric to use (default 0; options 0=Minimum, 1=Maximum, 2=Range, 3=Count, 4=Average distance, 5=Average distance between points)
- RADIUS_1 [number]: The first radius of search ellipse (default 0.0)
- RADIUS_2 [number]: The second radius of search ellipse (default 0.0)
- ANGLE [number]: Angle of search ellipse rotation in degrees (counter clockwise) (default 0.0)
- MIN_POINTS [number]: Minimum number of data points to use (default 0)
- NODATA [number]: NODATA marker to fill empty points (default 0.0)
- OPTIONS [string]: Additional creation options (optional)
- CREATION_OPTIONS [string]: Additional creation options (optional)
- EXTRA [string]: Additional command-line parameters (optional)
- DATA_TYPE [enum]: Output data type (default 5; options 0=Byte, 1=Int16, 2=UInt16, 3=UInt32, 4=Int32, 5=Float32, 6=Float64, 7=CInt16, 8=CInt32, 9=CFloat32, 10=CFloat64, 11=Int8)
- OUTPUT [rasterDestination]: Interpolated (data metrics)
Outputs: OUTPUT [outputRaster]

### gdal:gridinversedistance: Grid (Inverse distance to a power)
Parameters:
- INPUT [source]: Point layer
- Z_FIELD [field]: Z value from field (optional)
- POWER [number]: Weighting power (default 2.0)
- SMOOTHING [number]: Smoothing (default 0.0)
- RADIUS_1 [number]: The first radius of search ellipse (default 0.0)
- RADIUS_2 [number]: The second radius of search ellipse (default 0.0)
- ANGLE [number]: Angle of search ellipse rotation in degrees (counter clockwise) (default 0.0)
- MAX_POINTS [number]: Maximum number of data points to use (default 0)
- MIN_POINTS [number]: Minimum number of data points to use (default 0)
- NODATA [number]: NODATA marker to fill empty points (default 0.0)
- OPTIONS [string]: Additional creation options (optional)
- CREATION_OPTIONS [string]: Additional creation options (optional)
- EXTRA [string]: Additional command-line parameters (optional)
- DATA_TYPE [enum]: Output data type (default 5; options 0=Byte, 1=Int16, 2=UInt16, 3=UInt32, 4=Int32, 5=Float32, 6=Float64, 7=CInt16, 8=CInt32, 9=CFloat32, 10=CFloat64, 11=Int8)
- OUTPUT [rasterDestination]: Interpolated (IDW)
Outputs: OUTPUT [outputRaster]

### gdal:gridinversedistancenearestneighbor: Grid (IDW with nearest neighbor searching)
Parameters:
- INPUT [source]: Point layer
- Z_FIELD [field]: Z value from field (optional)
- POWER [number]: Weighting power (default 2.0)
- SMOOTHING [number]: Smoothing (default 0.0)
- RADIUS [number]: The radius of the search circle (default 1.0)
- MAX_POINTS [number]: Maximum number of data points to use (default 12)
- MIN_POINTS [number]: Minimum number of data points to use (default 0)
- NODATA [number]: NODATA marker to fill empty points (default 0.0)
- OPTIONS [string]: Additional creation options (optional)
- CREATION_OPTIONS [string]: Additional creation options (optional)
- EXTRA [string]: Additional command-line parameters (optional)
- DATA_TYPE [enum]: Output data type (default 5; options 0=Byte, 1=Int16, 2=UInt16, 3=UInt32, 4=Int32, 5=Float32, 6=Float64, 7=CInt16, 8=CInt32, 9=CFloat32, 10=CFloat64, 11=Int8)
- OUTPUT [rasterDestination]: Interpolated (IDW with NN search)
Outputs: OUTPUT [outputRaster]

### gdal:gridlinear: Grid (Linear)
Parameters:
- INPUT [source]: Point layer
- Z_FIELD [field]: Z value from field (optional)
- RADIUS [number]: Search distance  (default -1.0)
- NODATA [number]: NODATA marker to fill empty points (default 0.0)
- OPTIONS [string]: Additional creation options (optional)
- CREATION_OPTIONS [string]: Additional creation options (optional)
- EXTRA [string]: Additional command-line parameters (optional)
- DATA_TYPE [enum]: Output data type (default 5; options 0=Byte, 1=Int16, 2=UInt16, 3=UInt32, 4=Int32, 5=Float32, 6=Float64, 7=CInt16, 8=CInt32, 9=CFloat32, 10=CFloat64, 11=Int8)
- OUTPUT [rasterDestination]: Interpolated (Linear)
Outputs: OUTPUT [outputRaster]

### gdal:gridnearestneighbor: Grid (Nearest neighbor)
Parameters:
- INPUT [source]: Point layer
- Z_FIELD [field]: Z value from field (optional)
- RADIUS_1 [number]: The first radius of search ellipse (default 0.0)
- RADIUS_2 [number]: The second radius of search ellipse (default 0.0)
- ANGLE [number]: Angle of search ellipse rotation in degrees (counter clockwise) (default 0.0)
- NODATA [number]: NODATA marker to fill empty points (default 0.0)
- OPTIONS [string]: Additional creation options (optional)
- CREATION_OPTIONS [string]: Additional creation options (optional)
- EXTRA [string]: Additional command-line parameters (optional)
- DATA_TYPE [enum]: Output data type (default 5; options 0=Byte, 1=Int16, 2=UInt16, 3=UInt32, 4=Int32, 5=Float32, 6=Float64, 7=CInt16, 8=CInt32, 9=CFloat32, 10=CFloat64, 11=Int8)
- OUTPUT [rasterDestination]: Interpolated (Nearest neighbor)
Outputs: OUTPUT [outputRaster]

### gdal:hillshade: Hillshade
Parameters:
- INPUT [raster]: Input layer
- BAND [band]: Band number (default 1)
- Z_FACTOR [number]: Z factor (vertical exaggeration) (default 1.0)
- SCALE [number]: Scale (ratio of vertical units to horizontal) (default 1.0)
- AZIMUTH [number]: Azimuth of the light (default 315.0)
- ALTITUDE [number]: Altitude of the light (default 45.0)
- COMPUTE_EDGES [boolean]: Compute edges (default False)
- ZEVENBERGEN [boolean]: Use Zevenbergen&Thorne formula instead of the Horn's one (default False)
- COMBINED [boolean]: Combined shading (default False)
- MULTIDIRECTIONAL [boolean]: Multidirectional shading (default False)
- OPTIONS [string]: Additional creation options (optional)
- CREATION_OPTIONS [string]: Additional creation options (optional)
- EXTRA [string]: Additional command-line parameters (optional)
- OUTPUT [rasterDestination]: Hillshade
Outputs: OUTPUT [outputRaster]

### gdal:nearblack: Near black
Parameters:
- INPUT [raster]: Input layer
- NEAR [number]: How far from black (white) (default 15)
- WHITE [boolean]: Search for nearly white pixels instead of nearly black (default False)
- OPTIONS [string]: Additional creation options (optional)
- CREATION_OPTIONS [string]: Additional creation options (optional)
- EXTRA [string]: Additional command-line parameters (optional)
- OUTPUT [rasterDestination]: Nearblack
Outputs: OUTPUT [outputRaster]

### gdal:proximity: Proximity (raster distance)
Parameters:
- INPUT [raster]: Input layer
- BAND [band]: Band number (default 1)
- VALUES [string]: List of target pixels (optional)
- UNITS [enum]: Distance units (default 1; options 0=Georeferenced coordinates, 1=Pixel coordinates)
- MAX_DISTANCE [number]: The maximum distance to generate (optional; default 0.0)
- REPLACE [number]: Value to apply to pixels within the maximum distance of target pixels (optional; default 0.0)
- NODATA [number]: Nodata value to use for the destination proximity raster (optional; default 0.0)
- OPTIONS [string]: Additional creation options (optional)
- CREATION_OPTIONS [string]: Additional creation options (optional)
- EXTRA [string]: Additional command-line parameters (optional)
- DATA_TYPE [enum]: Output data type (default 5; options 0=Byte, 1=Int16, 2=UInt16, 3=UInt32, 4=Int32, 5=Float32, 6=Float64, 7=CInt16, 8=CInt32, 9=CFloat32, 10=CFloat64, 11=Int8)
- OUTPUT [rasterDestination]: Proximity map
Outputs: OUTPUT [outputRaster]

### gdal:roughness: Roughness
Parameters:
- INPUT [raster]: Input layer
- BAND [band]: Band number (default 1)
- COMPUTE_EDGES [boolean]: Compute edges (default False)
- OPTIONS [string]: Additional creation options (optional)
- CREATION_OPTIONS [string]: Additional creation options (optional)
- OUTPUT [rasterDestination]: Roughness
Outputs: OUTPUT [outputRaster]

### gdal:sieve: Sieve
Parameters:
- INPUT [raster]: Input layer
- THRESHOLD [number]: Threshold (default 10)
- EIGHT_CONNECTEDNESS [boolean]: Use 8-connectedness (default False)
- NO_MASK [boolean]: Do not use the default validity mask for the input band (default False)
- MASK_LAYER [raster]: Validity mask (optional)
- EXTRA [string]: Additional command-line parameters (optional)
- OUTPUT [rasterDestination]: Sieved
Outputs: OUTPUT [outputRaster]

### gdal:slope: Slope
Parameters:
- INPUT [raster]: Input layer
- BAND [band]: Band number (default 1)
- SCALE [number]: Ratio of vertical units to horizontal (default 1.0)
- AS_PERCENT [boolean]: Express slope as percent instead of degrees (default False)
- COMPUTE_EDGES [boolean]: Compute edges (default False)
- ZEVENBERGEN [boolean]: Use Zevenbergen&Thorne formula instead of the Horn's one (default False)
- OPTIONS [string]: Additional creation options (optional)
- CREATION_OPTIONS [string]: Additional creation options (optional)
- EXTRA [string]: Additional command-line parameters (optional)
- OUTPUT [rasterDestination]: Slope
Outputs: OUTPUT [outputRaster]

### gdal:tpitopographicpositionindex: Topographic Position Index (TPI)
Parameters:
- INPUT [raster]: Input layer
- BAND [band]: Band number (default 1)
- COMPUTE_EDGES [boolean]: Compute edges (default False)
- OPTIONS [string]: Additional creation options (optional)
- CREATION_OPTIONS [string]: Additional creation options (optional)
- OUTPUT [rasterDestination]: Topographic Position Index
Outputs: OUTPUT [outputRaster]

### gdal:triterrainruggednessindex: Terrain Ruggedness Index (TRI)
Parameters:
- INPUT [raster]: Input layer
- BAND [band]: Band number (default 1)
- COMPUTE_EDGES [boolean]: Compute edges (default False)
- OPTIONS [string]: Additional creation options (optional)
- CREATION_OPTIONS [string]: Additional creation options (optional)
- OUTPUT [rasterDestination]: Terrain Ruggedness Index
Outputs: OUTPUT [outputRaster]


## GDAL / Raster conversion

### gdal:gdal2xyz: gdal2xyz
Parameters:
- INPUT [raster]: Input layer
- BAND [band]: Band number (default 1)
- NODATA_INPUT [number]: Input pixel value to treat as NoData (optional)
- NODATA_OUTPUT [number]: Assign specified NoData value to output (optional)
- SKIP_NODATA [boolean]: Do not output NoData values (default False)
- CSV [boolean]: Output comma-separated values (default False)
- OUTPUT [fileDestination]: XYZ ASCII file
Outputs: OUTPUT [outputFile]

### gdal:pcttorgb: PCT to RGB
Parameters:
- INPUT [raster]: Input layer
- BAND [band]: Band number (default 1)
- RGBA [boolean]: Generate a RGBA file (default False)
- OUTPUT [rasterDestination]: PCT to RGB
Outputs: OUTPUT [outputRaster]

### gdal:polygonize: Polygonize (raster to vector)
Parameters:
- INPUT [raster]: Input layer
- BAND [band]: Band number (default 1)
- FIELD [string]: Name of the field to create (default DN)
- EIGHT_CONNECTEDNESS [boolean]: Use 8-connectedness (default False)
- EXTRA [string]: Additional command-line parameters (optional)
- OUTPUT [vectorDestination]: Vectorized
Outputs: OUTPUT [outputVector]

### gdal:rearrange_bands: Rearrange bands
This algorithm creates a new raster using selected band(s) from a given raster layer.
The algorithm also makes it possible to reorder the bands for the newly-created raster.
Parameters:
- INPUT [raster]: Input layer
- BANDS [band]: Selected band(s)
- OPTIONS [string]: Additional creation options (optional)
- CREATION_OPTIONS [string]: Additional creation options (optional)
- DATA_TYPE [enum]: Output data type (default 0; options 0=Use Input Layer Data Type, 1=Byte, 2=Int16, 3=UInt16, 4=UInt32, 5=Int32, 6=Float32, 7=Float64, 8=CInt16, 9=CInt32, 10=CFloat32, 11=CFloat64, 12=Int8)
- OUTPUT [rasterDestination]: Converted
Outputs: OUTPUT [outputRaster]

### gdal:rgbtopct: RGB to PCT
Parameters:
- INPUT [raster]: Input layer
- NCOLORS [number]: Number of colors (default 2)
- OUTPUT [rasterDestination]: RGB to PCT
Outputs: OUTPUT [outputRaster]

### gdal:translate: Translate (convert format)
Parameters:
- INPUT [raster]: Input layer
- TARGET_CRS [crs]: Override the projection for the output file (optional)
- NODATA [number]: Assign a specified NoData value to output bands (optional)
- COPY_SUBDATASETS [boolean]: Copy all subdatasets of this file to individual output files (default False)
- OPTIONS [string]: Additional creation options (optional)
- CREATION_OPTIONS [string]: Additional creation options (optional)
- EXTRA [string]: Additional command-line parameters (optional)
- DATA_TYPE [enum]: Output data type (default 0; options 0=Use Input Layer Data Type, 1=Byte, 2=Int16, 3=UInt16, 4=UInt32, 5=Int32, 6=Float32, 7=Float64, 8=CInt16, 9=CInt32, 10=CFloat32, 11=CFloat64, 12=Int8)
- OUTPUT [rasterDestination]: Converted
Outputs: OUTPUT [outputRaster]


## GDAL / Raster extraction

### gdal:cliprasterbyextent: Clip raster by extent
Parameters:
- INPUT [raster]: Input layer
- PROJWIN [extent]: Clipping extent
- OVERCRS [boolean]: Override the projection for the output file (default False)
- NODATA [number]: Assign a specified NoData value to output bands (optional)
- OPTIONS [string]: Additional creation options (optional)
- CREATION_OPTIONS [string]: Additional creation options (optional)
- DATA_TYPE [enum]: Output data type (default 0; options 0=Use Input Layer Data Type, 1=Byte, 2=Int16, 3=UInt16, 4=UInt32, 5=Int32, 6=Float32, 7=Float64, 8=CInt16, 9=CInt32, 10=CFloat32, 11=CFloat64, 12=Int8)
- EXTRA [string]: Additional command-line parameters (optional)
- OUTPUT [rasterDestination]: Clipped (extent)
Outputs: OUTPUT [outputRaster]

### gdal:cliprasterbymasklayer: Clip raster by mask layer
Parameters:
- INPUT [raster]: Input layer
- MASK [source]: Mask layer
- SOURCE_CRS [crs]: Source CRS (optional)
- TARGET_CRS [crs]: Target CRS (optional)
- TARGET_EXTENT [extent]: Target extent (optional)
- NODATA [number]: Assign a specified NoData value to output bands (optional)
- ALPHA_BAND [boolean]: Create an output alpha band (default False)
- CROP_TO_CUTLINE [boolean]: Match the extent of the clipped raster to the extent of the mask layer (default True)
- KEEP_RESOLUTION [boolean]: Keep resolution of input raster (default False)
- SET_RESOLUTION [boolean]: Set output file resolution (default False)
- X_RESOLUTION [number]: X Resolution to output bands (optional)
- Y_RESOLUTION [number]: Y Resolution to output bands (optional)
- MULTITHREADING [boolean]: Use multithreaded warping implementation (default False)
- OPTIONS [string]: Additional creation options (optional)
- CREATION_OPTIONS [string]: Additional creation options (optional)
- DATA_TYPE [enum]: Output data type (default 0; options 0=Use Input Layer Data Type, 1=Byte, 2=Int16, 3=UInt16, 4=UInt32, 5=Int32, 6=Float32, 7=Float64, 8=CInt16, 9=CInt32, 10=CFloat32, 11=CFloat64, 12=Int8)
- EXTRA [string]: Additional command-line parameters (optional)
- OUTPUT [rasterDestination]: Clipped (mask)
Outputs: OUTPUT [outputRaster]

### gdal:contour: Contour
Parameters:
- INPUT [raster]: Input layer
- BAND [band]: Band number (default 1)
- INTERVAL [number]: Interval between contour lines (default 10.0)
- FIELD_NAME [string]: Attribute name (if not set, no elevation attribute is attached) (optional; default ELEV)
- CREATE_3D [boolean]: Produce 3D vector (default False)
- IGNORE_NODATA [boolean]: Treat all raster values as valid (default False)
- NODATA [number]: Input pixel value to treat as NoData (optional)
- OFFSET [number]: Offset from zero relative to which to interpret intervals (optional; default 0.0)
- EXTRA [string]: Additional command-line parameters (optional)
- OPTIONS [string]: Additional creation options (optional)
- OUTPUT [vectorDestination]: Contours
Outputs: OUTPUT [outputVector]

### gdal:contour_polygon: Contour Polygons
Parameters:
- INPUT [raster]: Input layer
- BAND [band]: Band number (default 1)
- INTERVAL [number]: Interval between contour lines (default 10.0)
- CREATE_3D [boolean]: Produce 3D vector (default False)
- IGNORE_NODATA [boolean]: Treat all raster values as valid (default False)
- NODATA [number]: Input pixel value to treat as NoData (optional)
- OFFSET [number]: Offset from zero relative to which to interpret intervals (optional; default 0.0)
- EXTRA [string]: Additional command-line parameters (optional)
- OPTIONS [string]: Additional creation options (optional)
- FIELD_NAME_MIN [string]: Attribute name for minimum elevation of contour polygon (optional; default ELEV_MIN)
- FIELD_NAME_MAX [string]: Attribute name for maximum elevation of contour polygon (optional; default ELEV_MAX)
- OUTPUT [vectorDestination]: Contours
Outputs: OUTPUT [outputVector]


## GDAL / Raster miscellaneous

### gdal:buildvirtualraster: Build virtual raster
Parameters:
- INPUT [multilayer]: Input layers
- RESOLUTION [enum]: Resolution (default 0; options 0=Average, 1=Highest, 2=Lowest)
- SEPARATE [boolean]: Place each input file into a separate band (default True)
- PROJ_DIFFERENCE [boolean]: Allow projection difference (default False)
- ADD_ALPHA [boolean]: Add alpha mask band to VRT when source raster has none (default False)
- ASSIGN_CRS [crs]: Override projection for the output file (optional)
- RESAMPLING [enum]: Resampling algorithm (default 0; options 0=Nearest Neighbour, 1=Bilinear (2x2 Kernel), 2=Cubic (4x4 Kernel), 3=Cubic B-Spline (4x4 Kernel), 4=Lanczos (6x6 Kernel), 5=Average, 6=Mode)
- SRC_NODATA [string]: Nodata value(s) for input bands (space separated) (optional)
- EXTRA [string]: Additional command-line parameters (optional)
- OUTPUT [rasterDestination]: Virtual
Outputs: OUTPUT [outputRaster]

### gdal:gdal2tiles: gdal2tiles
Parameters:
- INPUT [raster]: Input layer
- PROFILE [enum]: Tile cutting profile (default 0; options 0=Mercator, 1=Geodetic, 2=Raster)
- ZOOM [string]: Zoom levels to render (optional)
- VIEWER [enum]: Web viewer to generate (default 0; options 0=All, 1=GoogleMaps, 2=OpenLayers, 3=Leaflet, 4=None)
- TITLE [string]: Title of the map (optional)
- COPYRIGHT [string]: Copyright of the map (optional)
- RESAMPLING [enum]: Resampling method (default 0; options 0=Average, 1=Nearest Neighbour, 2=Bilinear (2x2 Kernel), 3=Cubic (4x4 Kernel), 4=Cubic B-Spline (4x4 Kernel), 5=Lanczos (6x6 Kernel), 6=Antialias)
- SOURCE_CRS [crs]: The spatial reference system used for the source input data (optional)
- NODATA [number]: Transparency value to assign to the input data (optional; default 0)
- URL [string]: URL address where the generated tiles are going to be published (optional)
- GOOGLE_KEY [string]: Google Maps API key (http://code.google.com/apis/maps/signup.html) (optional)
- BING_KEY [string]: Bing Maps API key (https://www.bingmapsportal.com/) (optional)
- RESUME [boolean]: Generate only missing files (default False)
- KML [boolean]: Generate KML for Google Earth (default False)
- NO_KML [boolean]: Avoid automatic generation of KML files for EPSG:4326 (default False)
- OUTPUT [folderDestination]: Output directory
Outputs: OUTPUT [outputFolder]

### gdal:gdalinfo: Raster information
Parameters:
- INPUT [raster]: Input layer
- MIN_MAX [boolean]: Force computation of the actual min/max values for each band (default False)
- STATS [boolean]: Read and display image statistics (force computation if necessary) (default False)
- NOGCP [boolean]: Suppress GCP info (default False)
- NO_METADATA [boolean]: Suppress metadata info (default False)
- EXTRA [string]: Additional command-line parameters (optional)
- OUTPUT [fileDestination]: Layer information
Outputs: OUTPUT [outputHtml]

### gdal:merge: Merge
Parameters:
- INPUT [multilayer]: Input layers
- PCT [boolean]: Grab pseudocolor table from first layer (default False)
- SEPARATE [boolean]: Place each input file into a separate band (default False)
- NODATA_INPUT [number]: Input pixel value to treat as NoData (optional)
- NODATA_OUTPUT [number]: Assign specified NoData value to output (optional)
- OPTIONS [string]: Additional creation options (optional)
- CREATION_OPTIONS [string]: Additional creation options (optional)
- EXTRA [string]: Additional command-line parameters (optional)
- DATA_TYPE [enum]: Output data type (default 5; options 0=Byte, 1=Int16, 2=UInt16, 3=UInt32, 4=Int32, 5=Float32, 6=Float64, 7=CInt16, 8=CInt32, 9=CFloat32, 10=CFloat64, 11=Int8)
- OUTPUT [rasterDestination]: Merged
Outputs: OUTPUT [outputRaster]

### gdal:overviews: Build overviews (pyramids)
Parameters:
- INPUT [raster]: Input layer
- CLEAN [boolean]: Remove all existing overviews (default False)
- LEVELS [string]: Overview levels (e.g. 2 4 8 16) (optional)
- RESAMPLING [enum]: Resampling method (optional; options 0=Nearest Neighbour (default), 1=Average, 2=Gaussian, 3=Cubic (4x4 Kernel), 4=Cubic B-Spline (4x4 Kernel), 5=Lanczos (6x6 Kernel), 6=Average MP, 7=Average in Mag/Phase Space, 8=Mode)
- FORMAT [enum]: Overviews format (optional; default 0; options 0=Internal (if possible), 1=External (GTiff .ovr), 2=External (ERDAS Imagine .aux))
- EXTRA [string]: Additional command-line parameters (optional)
Outputs: OUTPUT [outputRaster]

### gdal:pansharp: Pansharpening
Parameters:
- SPECTRAL [raster]: Spectral dataset
- PANCHROMATIC [raster]: Panchromatic dataset
- RESAMPLING [enum]: Resampling algorithm (default 2; options 0=Nearest Neighbour, 1=Bilinear (2x2 Kernel), 2=Cubic (4x4 Kernel), 3=Cubic B-Spline (4x4 Kernel), 4=Lanczos (6x6 Kernel), 5=Average)
- OPTIONS [string]: Additional creation options (optional)
- CREATION_OPTIONS [string]: Additional creation options (optional)
- EXTRA [string]: Additional command-line parameters (optional)
- OUTPUT [rasterDestination]: Output
Outputs: OUTPUT [outputRaster]

### gdal:rastercalculator: Raster calculator
Parameters:
- INPUT_A [raster]: Input layer A
- BAND_A [band]: Number of raster band for A
- INPUT_B [raster]: Input layer B (optional)
- BAND_B [band]: Number of raster band for B (optional)
- INPUT_C [raster]: Input layer C (optional)
- BAND_C [band]: Number of raster band for C (optional)
- INPUT_D [raster]: Input layer D (optional)
- BAND_D [band]: Number of raster band for D (optional)
- INPUT_E [raster]: Input layer E (optional)
- BAND_E [band]: Number of raster band for E (optional)
- INPUT_F [raster]: Input layer F (optional)
- BAND_F [band]: Number of raster band for F (optional)
- FORMULA [string]: Calculation in gdalnumeric syntax using +-/* or any numpy array functions (i.e. logical_and()) (default A*2)
- NO_DATA [number]: Set output NoData value (optional)
- EXTENT_OPT [enum]: Handling of extent differences (default 0; options 0=Ignore, 1=Fail, 2=Union, 3=Intersect)
- PROJWIN [extent]: Output extent (optional)
- RTYPE [enum]: Output raster type (default 5; options 0=Byte, 1=Int16, 2=UInt16, 3=UInt32, 4=Int32, 5=Float32, 6=Float64, 7=CInt16, 8=CInt32, 9=CFloat32, 10=CFloat64, 11=Int8)
- OPTIONS [string]: Additional creation options (optional)
- CREATION_OPTIONS [string]: Additional creation options (optional)
- EXTRA [string]: Additional command-line parameters (optional)
- OUTPUT [rasterDestination]: Calculated
Outputs: OUTPUT [outputRaster]

### gdal:retile: Retile
Parameters:
- INPUT [multilayer]: Input files
- TILE_SIZE_X [number]: Tile width (default 256)
- TILE_SIZE_Y [number]: Tile height (default 256)
- OVERLAP [number]: Overlap in pixels between consecutive tiles (default 0)
- LEVELS [number]: Number of pyramids levels to build (default 1)
- OPTIONS [string]: Additional creation options (optional)
- CREATION_OPTIONS [string]: Additional creation options (optional)
- SOURCE_CRS [crs]: Source coordinate reference system (optional)
- RESAMPLING [enum]: Resampling method (default 0; options 0=Nearest Neighbour, 1=Bilinear (2x2 Kernel), 2=Cubic (4x4 Kernel), 3=Cubic B-Spline (4x4 Kernel), 4=Lanczos (6x6 Kernel))
- DELIMITER [string]: Column delimiter used in the CSV file (optional; default ;)
- EXTRA [string]: Additional command-line parameters (optional)
- DATA_TYPE [enum]: Output data type (default 5; options 0=Byte, 1=Int16, 2=UInt16, 3=UInt32, 4=Int32, 5=Float32, 6=Float64, 7=CInt16, 8=CInt32, 9=CFloat32, 10=CFloat64, 11=Int8)
- ONLY_PYRAMIDS [boolean]: Build only the pyramids (default False)
- DIR_FOR_ROW [boolean]: Use separate directory for each tiles row (default False)
- OUTPUT [folderDestination]: Output directory
- OUTPUT_CSV [fileDestination]: CSV file containing the tile(s) georeferencing information (optional)
Outputs: OUTPUT [outputFolder], OUTPUT_CSV [outputFile]

### gdal:tileindex: Tile index
Parameters:
- LAYERS [multilayer]: Input files
- PATH_FIELD_NAME [string]: Field name to hold the file path to the indexed rasters (default location)
- ABSOLUTE_PATH [boolean]: Store absolute path to the indexed rasters (default False)
- PROJ_DIFFERENCE [boolean]: Skip files with different projection reference (default False)
- TARGET_CRS [crs]: Transform geometries to the given CRS (optional)
- CRS_FIELD_NAME [string]: The name of the field to store the SRS of each tile (optional)
- CRS_FORMAT [enum]: The format in which the CRS of each tile must be written (default 0; options 0=Auto, 1=Well-known text (WKT), 2=EPSG, 3=Proj.4)
- OUTPUT [vectorDestination]: Tile index
Outputs: OUTPUT [outputVector]

### gdal:viewshed: Viewshed
Parameters:
- INPUT [raster]: Input layer
- BAND [band]: Band number (default 1)
- OBSERVER [point]: Observer location
- OBSERVER_HEIGHT [number]: Observer height, DEM units (default 1.0)
- TARGET_HEIGHT [number]: Target height, DEM units (default 1.0)
- MAX_DISTANCE [distance]: Maximum distance from observer to compute visibility (default 100.0)
- OPTIONS [string]: Additional creation options (optional)
- CREATION_OPTIONS [string]: Additional creation options (optional)
- EXTRA [string]: Additional command-line parameters (optional)
- OUTPUT [rasterDestination]: Output
Outputs: OUTPUT [outputRaster]


## GDAL / Raster projections

### gdal:assignprojection: Assign projection
Parameters:
- INPUT [raster]: Input layer
- CRS [crs]: Desired CRS
Outputs: OUTPUT [outputRaster]

### gdal:extractprojection: Extract projection
Parameters:
- INPUT [raster]: Input file
- PRJ_FILE_CREATE [boolean]: Create also .prj file (default False)
Outputs: WORLD_FILE [outputFile], PRJ_FILE [outputFile]

### gdal:warpreproject: Warp (reproject)
Parameters:
- INPUT [raster]: Input layer
- SOURCE_CRS [crs]: Source CRS (optional)
- TARGET_CRS [crs]: Target CRS (optional)
- RESAMPLING [enum]: Resampling method to use (default 0; options 0=Nearest Neighbour, 1=Bilinear (2x2 Kernel), 2=Cubic (4x4 Kernel), 3=Cubic B-Spline (4x4 Kernel), 4=Lanczos (6x6 Kernel), 5=Average, 6=Mode, 7=Maximum, 8=Minimum, 9=Median, 10=First Quartile (Q1), 11=Third Quartile (Q3))
- NODATA [number]: Nodata value for output bands (optional)
- TARGET_RESOLUTION [number]: Output file resolution in target georeferenced units (optional)
- OPTIONS [string]: Additional creation options (optional)
- CREATION_OPTIONS [string]: Additional creation options (optional)
- DATA_TYPE [enum]: Output data type (default 0; options 0=Use Input Layer Data Type, 1=Byte, 2=Int16, 3=UInt16, 4=UInt32, 5=Int32, 6=Float32, 7=Float64, 8=CInt16, 9=CInt32, 10=CFloat32, 11=CFloat64, 12=Int8)
- TARGET_EXTENT [extent]: Georeferenced extents of output file to be created (optional)
- TARGET_EXTENT_CRS [crs]: CRS of the target raster extent (optional)
- MULTITHREADING [boolean]: Use multithreaded warping implementation (default False)
- EXTRA [string]: Additional command-line parameters (optional)
- OUTPUT [rasterDestination]: Reprojected
Outputs: OUTPUT [outputRaster]


## GDAL / Vector conversion

### gdal:convertformat: Convert format
The algorithm converts simple features data between file formats.
Use convert all layers to convert a whole dataset.
Supported output formats for this option are:
- GPKG
- GML
Parameters:
- INPUT [source]: Input layer
- CONVERT_ALL_LAYERS [boolean]: Convert all layers from dataset (default False)
- OPTIONS [string]: Additional creation options (optional)
- OUTPUT [vectorDestination]: Converted
Outputs: OUTPUT [outputVector]

### gdal:rasterize: Rasterize (vector to raster)
Parameters:
- INPUT [source]: Input layer
- FIELD [field]: Field to use for a burn-in value (optional)
- BURN [number]: A fixed value to burn (optional; default 0.0)
- USE_Z [boolean]: Burn value extracted from the "Z" values of the feature (default False)
- UNITS [enum]: Output raster size units (options 0=Pixels, 1=Georeferenced units)
- WIDTH [number]: Width/Horizontal resolution (default 0.0)
- HEIGHT [number]: Height/Vertical resolution (default 0.0)
- EXTENT [extent]: Output extent (optional)
- NODATA [number]: Assign a specified NoData value to output bands (optional)
- OPTIONS [string]: Additional creation options (optional)
- CREATION_OPTIONS [string]: Additional creation options (optional)
- DATA_TYPE [enum]: Output data type (default 5; options 0=Byte, 1=Int16, 2=UInt16, 3=UInt32, 4=Int32, 5=Float32, 6=Float64, 7=CInt16, 8=CInt32, 9=CFloat32, 10=CFloat64, 11=Int8)
- INIT [number]: Pre-initialize the output image with value (optional)
- INVERT [boolean]: Invert rasterization (default False)
- EXTRA [string]: Additional command-line parameters (optional)
- OUTPUT [rasterDestination]: Rasterized
Outputs: OUTPUT [outputRaster]

### gdal:rasterize_over: Rasterize (overwrite with attribute)
Parameters:
- INPUT [source]: Input vector layer
- INPUT_RASTER [raster]: Input raster layer
- FIELD [field]: Field to use for burn in value
- ADD [boolean]: Add burn in values to existing raster values (default False)
- EXTRA [string]: Additional command-line parameters (optional)
Outputs: OUTPUT [outputRaster]

### gdal:rasterize_over_fixed_value: Rasterize (overwrite with fixed value)
Parameters:
- INPUT [source]: Input vector layer
- INPUT_RASTER [raster]: Input raster layer
- BURN [number]: A fixed value to burn (default 0.0)
- ADD [boolean]: Add burn in values to existing raster values (default False)
- EXTRA [string]: Additional command-line parameters (optional)
Outputs: OUTPUT [outputRaster]


## GDAL / Vector geoprocessing

### gdal:buffervectors: Buffer vectors
Parameters:
- INPUT [source]: Input layer
- GEOMETRY [string]: Geometry column name (default geometry)
- DISTANCE [distance]: Buffer distance (default 10.0)
- FIELD [field]: Dissolve by attribute (optional)
- DISSOLVE [boolean]: Dissolve all results (default False)
- EXPLODE_COLLECTIONS [boolean]: Produce one feature for each geometry in any kind of geometry collection in the source file (default False)
- OPTIONS [string]: Additional creation options (optional)
- OUTPUT [vectorDestination]: Buffer
Outputs: OUTPUT [outputVector]

### gdal:clipvectorbyextent: Clip vector by extent
Parameters:
- INPUT [source]: Input layer
- EXTENT [extent]: Clipping extent
- OPTIONS [string]: Additional creation options (optional)
- OUTPUT [vectorDestination]: Clipped (extent)
Outputs: OUTPUT [outputVector]

### gdal:clipvectorbypolygon: Clip vector by mask layer
Parameters:
- INPUT [source]: Input layer
- MASK [source]: Mask layer
- OPTIONS [string]: Additional creation options (optional)
- OUTPUT [vectorDestination]: Clipped (mask)
Outputs: OUTPUT [outputVector]

### gdal:dissolve: Dissolve
Parameters:
- INPUT [source]: Input layer
- FIELD [field]: Dissolve field (optional)
- GEOMETRY [string]: Geometry column name (default geometry)
- EXPLODE_COLLECTIONS [boolean]: Produce one feature for each geometry in any kind of geometry collection in the source file (default False)
- KEEP_ATTRIBUTES [boolean]: Keep input attributes (default False)
- COUNT_FEATURES [boolean]: Count dissolved features (default False)
- COMPUTE_AREA [boolean]: Compute area and perimeter of dissolved features (default False)
- COMPUTE_STATISTICS [boolean]: Compute min/max/sum/mean for attribute (default False)
- STATISTICS_ATTRIBUTE [field]: Numeric attribute to calculate statistics on (optional)
- OPTIONS [string]: Additional creation options (optional)
- OUTPUT [vectorDestination]: Dissolved
Outputs: OUTPUT [outputVector]

### gdal:offsetcurve: Offset curve
Parameters:
- INPUT [source]: Input layer
- GEOMETRY [string]: Geometry column name (default geometry)
- DISTANCE [distance]: Offset distance (left-sided: positive, right-sided: negative) (default 10)
- OPTIONS [string]: Additional creation options (optional)
- OUTPUT [vectorDestination]: Offset curve
Outputs: OUTPUT [outputVector]

### gdal:onesidebuffer: One side buffer
Parameters:
- INPUT [source]: Input layer
- GEOMETRY [string]: Geometry column name (default geometry)
- DISTANCE [distance]: Buffer distance (default 10)
- BUFFER_SIDE [enum]: Buffer side (default 0; options 0=Right, 1=Left)
- FIELD [field]: Dissolve by attribute (optional)
- DISSOLVE [boolean]: Dissolve all results (default False)
- EXPLODE_COLLECTIONS [boolean]: Produce one feature for each geometry in any kind of geometry collection in the source file (default False)
- OPTIONS [string]: Additional creation options (optional)
- OUTPUT [vectorDestination]: One-sided buffer
Outputs: OUTPUT [outputVector]

### gdal:pointsalonglines: Points along lines
Parameters:
- INPUT [source]: Input layer
- GEOMETRY [string]: Geometry column name (default geometry)
- DISTANCE [number]: Distance from line start represented as fraction of line length (default 0.5)
- OPTIONS [string]: Additional creation options (optional)
- OUTPUT [vectorDestination]: Points along lines
Outputs: OUTPUT [outputVector]


## GDAL / Vector miscellaneous

### gdal:buildvirtualvector: Build virtual vector
This algorithm creates a virtual layer that contains a set of vector layers.
Parameters:
- INPUT [multilayer]: Input datasources
- UNIONED [boolean]: Create "unioned" VRT (default False)
- OUTPUT [vectorDestination]: Virtual vector
Outputs: OUTPUT [outputVector], VRT_STRING [outputString]

### gdal:executesql: Execute SQL
Parameters:
- INPUT [source]: Input layer
- SQL [string]: SQL expression
- DIALECT [enum]: SQL dialect (default 0; options 0=None, 1=OGR SQL, 2=SQLite)
- OPTIONS [string]: Additional creation options (optional)
- OUTPUT [vectorDestination]: SQL result
Outputs: OUTPUT [outputVector]

### gdal:importvectorintopostgisdatabaseavailableconnections: Export to PostgreSQL (available connections)
Exports a vector layer to an existing PostgreSQL database connection
Parameters:
- DATABASE [providerconnection]: Database (connection name)
- INPUT [source]: Input layer
- SHAPE_ENCODING [string]: Shape encoding (optional)
- GTYPE [enum]: Output geometry type (default 0; options 0=, 1=NONE, 2=GEOMETRY, 3=POINT, 4=LINESTRING, 5=POLYGON, 6=GEOMETRYCOLLECTION, 7=MULTIPOINT, 8=MULTIPOLYGON, 9=MULTILINESTRING, 10=CIRCULARSTRING, 11=COMPOUNDCURVE, 12=CURVEPOLYGON, 13=MULTICURVE, 14=MULTISURFACE, 15=CONVERT_TO_LINEAR, 16=CONVERT_TO_CURVE)
- A_SRS [crs]: Assign an output CRS (optional)
- T_SRS [crs]: Reproject to this CRS on output  (optional)
- S_SRS [crs]: Override source CRS (optional)
- SCHEMA [databaseschema]: Schema (schema name) (optional; default public)
- TABLE [databasetable]: Table to import to (leave blank to use layer name) (optional)
- PK [string]: Primary key (new field) (optional; default id)
- PRIMARY_KEY [field]: Primary key (existing field, used if the above option is left empty) (optional)
- GEOCOLUMN [string]: Geometry column name (optional; default geom)
- DIM [enum]: Vector dimensions (default 0; options 0=2, 1=3, 2=4)
- SIMPLIFY [string]: Distance tolerance for simplification (optional)
- SEGMENTIZE [string]: Maximum distance between 2 nodes (densification) (optional)
- SPAT [extent]: Select features by extent (defined in input layer CRS) (optional)
- CLIP [boolean]: Clip the input layer using the above (rectangle) extent (default False)
- WHERE [string]: Select features using a SQL "WHERE" statement (Ex: column='value') (optional)
- GT [string]: Group N features per transaction (Default: 20000) (optional)
- OVERWRITE [boolean]: Overwrite existing table (default True)
- APPEND [boolean]: Append to existing table (default False)
- ADDFIELDS [boolean]: Append and add new fields to existing table (default False)
- LAUNDER [boolean]: Do not launder columns/table names (default False)
- INDEX [boolean]: Do not create spatial index (default False)
- SKIPFAILURES [boolean]: Continue after a failure, skipping the failed feature (default False)
- MAKEVALID [boolean]: Validate geometries based on Simple Features specification (default False)
- PROMOTETOMULTI [boolean]: Promote to Multipart (default True)
- PRECISION [boolean]: Keep width and precision of input attributes (default True)
- OPTIONS [string]: Additional creation options (optional)

### gdal:importvectorintopostgisdatabasenewconnection: Export to PostgreSQL (new connection)
Exports a vector layer to a new PostgreSQL database connection
Parameters:
- INPUT [source]: Input layer
- SHAPE_ENCODING [string]: Shape encoding (optional)
- GTYPE [enum]: Output geometry type (default 0; options 0=, 1=NONE, 2=GEOMETRY, 3=POINT, 4=LINESTRING, 5=POLYGON, 6=GEOMETRYCOLLECTION, 7=MULTIPOINT, 8=MULTIPOLYGON, 9=MULTILINESTRING, 10=CIRCULARSTRING, 11=COMPOUNDCURVE, 12=CURVEPOLYGON, 13=MULTICURVE, 14=MULTISURFACE, 15=CONVERT_TO_LINEAR, 16=CONVERT_TO_CURVE)
- A_SRS [crs]: Assign an output CRS (optional)
- T_SRS [crs]: Reproject to this CRS on output  (optional)
- S_SRS [crs]: Override source CRS (optional)
- HOST [string]: Host (optional; default localhost)
- PORT [string]: Port (optional; default 5432)
- USER [string]: Username (optional)
- DBNAME [string]: Database name (optional)
- PASSWORD [string]: Password (optional)
- SCHEMA [string]: Schema name (optional; default public)
- TABLE [string]: Table name, leave blank to use input name (optional)
- PK [string]: Primary key (new field) (optional; default id)
- PRIMARY_KEY [field]: Primary key (existing field, used if the above option is left empty) (optional)
- GEOCOLUMN [string]: Geometry column name (optional; default geom)
- DIM [enum]: Vector dimensions (default 0; options 0=2, 1=3, 2=4)
- SIMPLIFY [string]: Distance tolerance for simplification (optional)
- SEGMENTIZE [string]: Maximum distance between 2 nodes (densification) (optional)
- SPAT [extent]: Select features by extent (defined in input layer CRS) (optional)
- CLIP [boolean]: Clip the input layer using the above (rectangle) extent (default False)
- FIELDS [field]: Fields to include (leave empty to use all fields) (optional)
- WHERE [string]: Select features using a SQL "WHERE" statement (Ex: column='value') (optional)
- GT [string]: Group N features per transaction (Default: 20000) (optional)
- OVERWRITE [boolean]: Overwrite existing table (default True)
- APPEND [boolean]: Append to existing table (default False)
- ADDFIELDS [boolean]: Append and add new fields to existing table (default False)
- LAUNDER [boolean]: Do not launder columns/table names (default False)
- INDEX [boolean]: Do not create spatial index (default False)
- SKIPFAILURES [boolean]: Continue after a failure, skipping the failed feature (default False)
- MAKEVALID [boolean]: Validate geometries based on Simple Features specification (default False)
- PROMOTETOMULTI [boolean]: Promote to Multipart (default True)
- PRECISION [boolean]: Keep width and precision of input attributes (default True)
- OPTIONS [string]: Additional creation options (optional)

### gdal:ogrinfo: Vector information
Parameters:
- INPUT [vector]: Input layer
- ALL_LAYERS [boolean]: Enable listing of all layers in the dataset (default False)
- SUMMARY_ONLY [boolean]: Summary output only (default True)
- NO_METADATA [boolean]: Suppress metadata info (default False)
- EXTRA [string]: Additional command-line parameters (optional)
- OUTPUT [fileDestination]: Layer information
Outputs: OUTPUT [outputHtml]

### gdal:ogrinfojson: Vector information (JSON)
Parameters:
- INPUT [vector]: Input layer
- ALL_LAYERS [boolean]: Enable listing of all layers in the dataset (default False)
- FEATURES [boolean]: Enable listing of features (default False)
- NO_METADATA [boolean]: Suppress metadata info (default False)
- EXTRA [string]: Additional command-line parameters (optional)
- OUTPUT [fileDestination]: Layer information
Outputs: OUTPUT [outputFile]


## QGIS / Cartography

### qgis:topologicalcoloring: Topological coloring
This algorithm assigns a color index to polygon features in such a way that no adjacent polygons share the same color index, whilst minimizing the number of colors required.
An optional minimum distance between features assigned the same color can be set to prevent nearby (but non-touching) features from being assigned equal colors.
The algorithm allows choice of method to use when assigning colors. The default method attempts to assign colors so that the count of features assigned to each individual color index is balanced.
The 'by assigned area' mode instead assigns colors so that the total area of features assigned to each color is balanced. This mode can be useful to help avoid large features resulting in one of the colors appearing more dominant on a colored map.
The 'by distance between colors' mode will assign colors in order to maximize the distance between features of the same color. This mode helps to create a more uniform distribution of colors across a map.
A minimum number of colors can be specified if desired. The color index is saved to a new attribute named color_id.
Parameters:
- INPUT [source]: Input layer
- MIN_COLORS [number]: Minimum number of colors (default 4)
- MIN_DISTANCE [distance]: Minimum distance between features (default 0.0)
- BALANCE [enum]: Balance color assignment (default 0; options 0=By feature count, 1=By assigned area, 2=By distance between colors)
- OUTPUT [sink]: Colored
Outputs: OUTPUT [outputVector]


## QGIS / Database

### qgis:importintospatialite: Export to SpatiaLite
This algorithm imports a vector layer into a SpatiaLite database, creating a new table.
Parameters:
- INPUT [source]: Layer to import
- DATABASE [vector]: File database
- TABLENAME [string]: Table to import to (leave blank to use layer name) (optional)
- PRIMARY_KEY [field]: Primary key field (optional)
- GEOMETRY_COLUMN [string]: Geometry column (default geom)
- ENCODING [string]: Encoding (optional; default UTF-8)
- OVERWRITE [boolean]: Overwrite (default True)
- CREATEINDEX [boolean]: Create spatial index (default True)
- LOWERCASE_NAMES [boolean]: Convert field names to lowercase (default True)
- DROP_STRING_LENGTH [boolean]: Drop length constraints on character fields (default False)
- FORCE_SINGLEPART [boolean]: Create single-part geometries instead of multi-part (default False)

### qgis:postgisexecuteandloadsql: PostgreSQL execute and load SQL
This algorithm performs a SQL database query on a PostGIS database connected to QGIS and loads the query results as a new layer.
Parameters:
- DATABASE [providerconnection]: Database (connection name)
- SQL [string]: SQL query
- ID_FIELD [string]: Unique ID field name (default id)
- GEOMETRY_FIELD [string]: Geometry field name (optional; default geom)
Outputs: OUTPUT [outputVector]


## QGIS / Interpolation

### qgis:heatmapkerneldensityestimation: Heatmap (Kernel Density Estimation)
Creates a density (heatmap) raster of an input point vector layer using kernel density estimation. Heatmaps allow easy identification of hotspots and clustering of points.
The density is calculated based on the number of points in a location, with larger numbers of clustered points resulting in larger values.
Parameters:
- INPUT [source]: Point layer
- RADIUS [distance]: Radius (default 100.0)
- RADIUS_FIELD [field]: Radius from field (optional)
- PIXEL_SIZE [number]: Output raster size (default 0.1)
- WEIGHT_FIELD [field]: Weight from field (optional)
- KERNEL [enum]: Kernel shape (default 0; options 0=Quartic, 1=Triangular, 2=Uniform, 3=Triweight, 4=Epanechnikov)
- DECAY [number]: Decay ratio (Triangular kernels only) (optional; default 0.0)
- OUTPUT_VALUE [enum]: Output value scaling (default 0; options 0=Raw, 1=Scaled)
- OUTPUT [rasterDestination]: Heatmap
Outputs: OUTPUT [outputRaster]

### qgis:idwinterpolation: IDW interpolation
Generates an Inverse Distance Weighted (IDW) interpolation of a point vector layer.
Sample points are weighted during interpolation such that the influence of one point relative to another declines with distance from the unknown point you want to create.
Parameters:
- INTERPOLATION_DATA [idw_interpolation_data]: Input layer(s)
- DISTANCE_COEFFICIENT [number]: Distance coefficient P (default 2.0)
- EXTENT [extent]: Extent
- PIXEL_SIZE [number]: Output raster size (default 0.1)
- COLUMNS [number]: Number of columns (optional)
- ROWS [number]: Number of rows (optional)
- OUTPUT [rasterDestination]: Interpolated
Outputs: OUTPUT [outputRaster]

### qgis:tininterpolation: TIN interpolation
Generates a Triangulated Irregular Network (TIN) interpolation of a point vector layer.
With the TIN method you can create a surface formed by triangles of nearest neighbor points. To do this, circumcircles around selected sample points are created and their intersections are connected to a network of non overlapping and as compact as possible triangles. The resulting surfaces are not smooth.
The algorithm creates both the raster layer of the interpolated values and the vector line layer with the triangulation boundaries.
Parameters:
- INTERPOLATION_DATA [idw_interpolation_data]: Input layer(s)
- METHOD [enum]: Interpolation method (default 0; options 0=Linear, 1=Clough-Toucher (cubic))
- EXTENT [extent]: Extent
- PIXEL_SIZE [number]: Output raster size (default 0.1)
- COLUMNS [number]: Number of columns (optional)
- ROWS [number]: Number of rows (optional)
- OUTPUT [rasterDestination]: Interpolated
- TRIANGULATION [sink]: Triangulation (optional)
Outputs: OUTPUT [outputRaster], TRIANGULATION [outputVector]


## QGIS / Plots

### qgis:barplot: Bar plot
This algorithm creates a bar plot from a category and a layer field.
Parameters:
- INPUT [source]: Input layer
- NAME_FIELD [field]: Category name field
- VALUE_FIELD [field]: Value field
- OUTPUT [fileDestination]: Bar plot
- TITLE [string]: Title (optional)
- XAXIS_TITLE [string]: X-axis title (optional)
- YAXIS_TITLE [string]: Y-axis title (optional)
Outputs: OUTPUT [outputHtml]

### qgis:boxplot: Box plot
This algorithm creates a box plot from a category and a layer field.
Parameters:
- INPUT [source]: Input layer
- NAME_FIELD [field]: Category name field
- VALUE_FIELD [field]: Value field
- MSD [enum]: Additional Statistic Lines (default 0; options 0=Show Mean, 1=Show Standard Deviation, 2=Don't show Mean and Standard Deviation)
- TITLE [string]: Title (optional)
- XAXIS_TITLE [string]: X-axis title (optional)
- YAXIS_TITLE [string]: Y-axis title (optional)
- OUTPUT [fileDestination]: Box plot
Outputs: OUTPUT [outputHtml]

### qgis:meanandstandarddeviationplot: Mean and standard deviation plot
This algorithm creates a box plot with mean and standard deviation values.
Parameters:
- INPUT [source]: Input table
- NAME_FIELD [field]: Category name field
- VALUE_FIELD [field]: Value field
- OUTPUT [fileDestination]: Plot
Outputs: OUTPUT [outputHtml]

### qgis:polarplot: Polar plot
This algorithm generates a polar plot based on the value of an input vector layer.
Two fields must be entered as parameters: one that define the category (to group features) and another one with the variable to plot (this has to be a numeric one)
Parameters:
- INPUT [source]: Input layer
- NAME_FIELD [field]: Category name field
- VALUE_FIELD [field]: Value field
- OUTPUT [fileDestination]: Polar plot
Outputs: OUTPUT [outputHtml]

### qgis:rasterlayerhistogram: Raster layer histogram
This algorithm generates a histogram with the values of a raster layer.
The raster layer must have a single band.
Parameters:
- INPUT [raster]: Input layer
- BAND [band]: Band number (default 1)
- BINS [number]: number of bins (default 10)
- OUTPUT [fileDestination]: Histogram
Outputs: OUTPUT [outputHtml]

### qgis:scatter3dplot: Vector layer scatterplot 3D
This algorithm creates a 3D scatter plot for a vector layer.
Parameters:
- INPUT [source]: Input layer
- XFIELD [field]: X attribute
- YFIELD [field]: Y attribute
- ZFIELD [field]: Z attribute
- TITLE [string]: Title (optional)
- XAXIS_TITLE [string]: X-axis title (optional)
- YAXIS_TITLE [string]: Y-axis title (optional)
- ZAXIS_TITLE [string]: Z-axis title (optional)
- OUTPUT [fileDestination]: Scatterplot 3D
Outputs: OUTPUT [outputHtml]

### qgis:vectorlayerhistogram: Vector layer histogram
This algorithm generates a histogram with the values of the attribute of a vector layer.
The attribute to use for computing the histogram must be a numeric attribute.
Parameters:
- INPUT [source]: Input layer
- FIELD [field]: Attribute
- BINS [number]: number of bins (default 10)
- OUTPUT [fileDestination]: Histogram
Outputs: OUTPUT [outputHtml]

### qgis:vectorlayerscatterplot: Vector layer scatterplot
This algorithm creates a simple X - Y scatter plot for a vector layer.
Parameters:
- INPUT [source]: Input layer
- XFIELD [field]: X attribute
- YFIELD [field]: Y attribute
- HOVERTEXT [expression]: Hover text (optional)
- TITLE [string]: Title (optional)
- XAXIS_TITLE [string]: X-axis title (optional)
- YAXIS_TITLE [string]: Y-axis title (optional)
- XAXIS_LOG [boolean]: Use logarithmic scale for x-axis (default False)
- YAXIS_LOG [boolean]: Use logarithmic scale for y-axis (default False)
- OUTPUT [fileDestination]: Scatterplot
Outputs: OUTPUT [outputHtml]


## QGIS / Raster analysis

### qgis:rastercalculator: Raster calculator
This algorithm allows performing algebraic operations using raster layers.
The resulting layer will have its values computed according to an expression. The expression can contain numerical values, operators and references to any of the layers in the current project. The following functions are also supported:
- sin(), cos(), tan(), atan2(), ln(), log10()
The extent, cell size, and output CRS can be defined by the user. If the extent is not specified, the minimum extent that covers selected reference layer(s) will be used. If the cell size is not specified, the minimum cell size of selected reference layer(s) will be used. If the output CRS is not specified, the CRS of the first reference layer will be used.
The cell size is assumed to be the same in both X and Y axes.
Layers are referred by their name as displayed in the layer list and the number of the band to use (based on 1), using the pattern 'layer_name@band number'. For instance, the first band from a layer named DEM will be referred as DEM@1.
When using the calculator in the batch interface or from the console, the files to use have to be specified. The corresponding layers are referred using the base name of the file (without the full path). For instance, if using a layer at path/to/my/rasterfile.tif, the first band of that layer will be referred as rasterfile.tif@1.
Parameters:
- EXPRESSION [raster_calc_expression]: Expression
- LAYERS [multilayer]: Reference layer(s) (used for automated extent, cellsize, and CRS) (optional)
- CELLSIZE [number]: Cell size (use 0 or empty to set it automatically) (optional; default 0.0)
- EXTENT [extent]: Output extent (optional)
- CRS [crs]: Output CRS (optional)
- OUTPUT [rasterDestination]: Output
Outputs: OUTPUT [outputRaster]


## QGIS / Raster terrain analysis

### qgis:hypsometriccurves: Hypsometric curves
This algorithm computes hypsometric curves for an input Digital Elevation Model. Curves are produced as table files in an output folder specified by the user.
Parameters:
- INPUT_DEM [raster]: DEM to analyze
- BOUNDARY_LAYER [source]: Boundary layer
- STEP [number]: Step (default 100.0)
- USE_PERCENTAGE [boolean]: Use % of area instead of absolute value (default False)
- OUTPUT_DIRECTORY [folderDestination]: Hypsometric curves
Outputs: OUTPUT_DIRECTORY [outputFolder]

### qgis:relief: Relief
This algorithm creates a shaded relief layer from digital elevation data.
Parameters:
- INPUT [raster]: Elevation layer
- Z_FACTOR [number]: Z factor (default 1.0)
- AUTO_COLORS [boolean]: Generate relief classes automatically (default False)
- COLORS [relief_colors]: Relief colors (optional)
- OUTPUT [rasterDestination]: Relief
- FREQUENCY_DISTRIBUTION [fileDestination]: Frequency distribution (optional)
Outputs: OUTPUT [outputRaster], FREQUENCY_DISTRIBUTION [outputFile]


## QGIS / Raster tools

### qgis:setstyleforrasterlayer: Set style for raster layer
This algorithm sets the style of a raster layer. The style must be defined in a QML file.
Parameters:
- INPUT [raster]: Raster layer
- STYLE [file]: Style file
Outputs: INPUT [outputRaster]


## QGIS / Vector analysis

### qgis:distancematrix: Distance matrix
This algorithm creates a table containing a distance matrix, with distances between all the points in a points layer.
Parameters:
- INPUT [source]: Input point layer
- INPUT_FIELD [field]: Input unique ID field
- TARGET [source]: Target point layer
- TARGET_FIELD [field]: Target unique ID field
- MATRIX_TYPE [enum]: Output matrix type (default 0; options 0=Linear (N*k x 3) distance matrix, 1=Standard (N x T) distance matrix, 2=Summary distance matrix (mean, std. dev., min, max))
- NEAREST_POINTS [number]: Use only the nearest (k) target points (default 0)
- OUTPUT [sink]: Distance matrix
Outputs: OUTPUT [outputVector]

### qgis:distancetonearesthublinetohub: Distance to nearest hub (line to hub)
Given an origin and a destination layers, this algorithm computes the distance between origin features and their closest destination one. Distance calculations are based on the features center.
The resulting layer contains lines linking each origin point with its nearest destination feature.
Parameters:
- INPUT [source]: Source points layer
- HUBS [source]: Destination hubs layer
- FIELD [field]: Hub layer name attribute
- UNIT [enum]: Measurement unit (options 0=Meters, 1=Feet, 2=Miles, 3=Kilometers, 4=Layer units)
- OUTPUT [sink]: Hub distance
Outputs: OUTPUT [outputVector]

### qgis:distancetonearesthubpoints: Distance to nearest hub (points)
Given an origin and a destination layers, this algorithm computes the distance between origin features and their closest destination one. Distance calculations are based on the features center.
The resulting layer contains origin features center point with an additional field indicating the identifier of the nearest destination feature and the distance to it.
Parameters:
- INPUT [source]: Source points layer
- HUBS [source]: Destination hubs layer
- FIELD [field]: Hub layer name attribute
- UNIT [enum]: Measurement unit (options 0=Meters, 1=Feet, 2=Miles, 3=Kilometers, 4=Layer units)
- OUTPUT [sink]: Hub distance
Outputs: OUTPUT [outputVector]

### qgis:listuniquevalues: List unique values
This algorithm generates a report with information about the unique values found in a given attribute (or attributes) of a vector layer.
Parameters:
- INPUT [source]: Input layer
- FIELDS [field]: Target field(s)
- OUTPUT [sink]: Unique values (optional)
- OUTPUT_HTML_FILE [fileDestination]: HTML report (optional)
Outputs: OUTPUT [outputVector], OUTPUT_HTML_FILE [outputHtml], TOTAL_VALUES [outputNumber], UNIQUE_VALUES [outputString]

### qgis:statisticsbycategories: Statistics by categories
This algorithm calculates statistics of fields depending on a parent class.
Parameters:
- INPUT [source]: Input vector layer
- VALUES_FIELD_NAME [field]: Field to calculate statistics on (if empty, only count is calculated) (optional)
- CATEGORIES_FIELD_NAME [field]: Field(s) with categories
- OUTPUT [sink]: Statistics by category
Outputs: OUTPUT [outputVector]


## QGIS / Vector creation

### qgis:generatepointspixelcentroidsalongline: Generate points (pixel centroids) along line
This algorithm generates a point vector layer from an input raster and line layer. The points correspond to the pixel centroids that intersect the line layer.
Parameters:
- INPUT_RASTER [raster]: Raster layer
- INPUT_VECTOR [source]: Vector layer
- OUTPUT [sink]: Points along lines
Outputs: OUTPUT [outputVector]

### qgis:randompointsalongline: Random points along line
This algorithm creates a point layer with a given "Number of points" placed on the lines of the "Input layer".
The location of each point is determined by randomly selecting a feature, then a segment of the line geometry of that feature, and finally a random position on that segment. A minimum distance between the points can be specified (Euclidean distance).
Parameters:
- INPUT [source]: Input layer
- POINTS_NUMBER [number]: Number of points (default 1)
- MIN_DISTANCE [distance]: Minimum distance between points (default 0)
- OUTPUT [sink]: Random points
Outputs: OUTPUT [outputVector]

### qgis:randompointsinlayerbounds: Random points in layer bounds
This algorithm creates a new point layer with a given number of random points, all of them within the extent of a given layer. A distance factor can be specified, to avoid points being too close to each other.
Parameters:
- INPUT [source]: Input layer
- POINTS_NUMBER [number]: Number of points (default 1)
- MIN_DISTANCE [distance]: Minimum distance between points (default 0)
- OUTPUT [sink]: Random points
Outputs: OUTPUT [outputVector]

### qgis:randompointsinsidepolygons: Random points inside polygons
This algorithm creates a new point layer with random points inside the polygons of a given layer.
The number of points in each polygon can be defined as a fixed count or as a density value. The count/density value could also be taken from an attribute or an expression specified using the "Data defined override" functionality, so it can be different for each polygon in the input layer.
A minimum distance can be specified, to avoid points being too close to each other.
Parameters:
- INPUT [source]: Input layer
- STRATEGY [enum]: Sampling strategy (default 0; options 0=Points count, 1=Points density)
- VALUE [number]: Point count or density (default 1)
- EXPRESSION [expression]: Expression (optional)
- MIN_DISTANCE [distance]: Minimum distance between points (optional)
- OUTPUT [sink]: Random points
Outputs: OUTPUT [outputVector]

### qgis:regularpoints: Regular points
This algorithm creates a point layer with a given number of regular points, all of them within a given extent.
Parameters:
- EXTENT [extent]: Input extent
- SPACING [distance]: Point spacing/count (default 100)
- INSET [distance]: Initial inset from corner (LH side) (default 0.0)
- RANDOMIZE [boolean]: Apply random offset to point spacing (default False)
- IS_SPACING [boolean]: Use point spacing (default True)
- CRS [crs]: Output layer CRS (default ProjectCrs)
- OUTPUT [sink]: Regular points
Outputs: OUTPUT [outputVector]


## QGIS / Vector general

### qgis:executesql: Execute SQL
Runs a simple or complex query with SQL syntax.
Input data sources are identified with input1, input2, ..., inputN and a simple query will look like: SELECT * FROM input1
The result of the query will be added as a new layer.
Parameters:
- INPUT_DATASOURCES [multilayer]: Input data sources (called input1, .., inputN in the query) (optional)
- INPUT_QUERY [execute_sql]: SQL query
- INPUT_UID_FIELD [string]: Unique identifier field (optional)
- INPUT_GEOMETRY_FIELD [string]: Geometry field (optional)
- INPUT_GEOMETRY_TYPE [enum]: Geometry type (default 0; options 0=Autodetect, 1=No geometry, 2=Point, 3=LineString, 4=Polygon, 5=MultiPoint, 6=MultiLineString, 7=MultiPolygon)
- INPUT_GEOMETRY_CRS [crs]: CRS (optional)
- OUTPUT [sink]: SQL Output
Outputs: OUTPUT [outputVector]

### qgis:setstyleforvectorlayer: Set style for vector layer
This algorithm sets the style of a vector layer. The style must be defined in a QML file.
Parameters:
- INPUT [vector]: Vector layer
- STYLE [file]: Style file
Outputs: INPUT [outputVector]


## QGIS / Vector geometry

### qgis:eliminateselectedpolygons: Eliminate selected polygons
This algorithm combines selected polygons of the input layer with certain adjacent polygons by erasing their common boundary. The adjacent polygon can be either the one with the largest or smallest area or the one sharing the largest common boundary with the polygon to be eliminated. Eliminate is normally used to get rid of sliver polygons, i.e. tiny polygons that are a result of polygon intersection processes where boundaries of the inputs are similar but not identical.
Parameters:
- INPUT [vector]: Input layer
- MODE [enum]: Merge selection with the neighbouring polygon with the (options 0=Largest Area, 1=Smallest Area, 2=Largest Common Boundary)
- OUTPUT [sink]: Eliminated
Outputs: OUTPUT [outputVector]

### qgis:knearestconcavehull: Concave hull (k-nearest neighbor)
This algorithm generates a concave hull polygon from a set of points. If the input layer is a line or polygon layer, it will use the nodes.
The number of neighbours to consider determines the concaveness of the output polygon. A lower number will result in a concave hull that follows the points very closely, while a higher number will have a smoother shape. The minimum number of neighbour points to consider is 3. A value equal to or greater than the number of points will result in a convex hull.
If a field is selected, the algorithm will group the features in the input layer using unique values in that field and generate individual polygons in the output layer for each group.
Parameters:
- INPUT [source]: Input layer
- KNEIGHBORS [number]: Number of neighboring points to consider (a lower number is more concave, a higher number is smoother) (default 3)
- FIELD [field]: Field (set if creating concave hulls by class) (optional)
- OUTPUT [sink]: Concave hull
Outputs: OUTPUT [outputVector]

### qgis:linestopolygons: Lines to polygons
This algorithm generates a polygon layer using as polygon rings the lines from an input line layer.
The attribute table of the output layer is the same as the one from of the input line layer.
Parameters:
- INPUT [source]: Input layer
- OUTPUT [sink]: Polygons
Outputs: OUTPUT [outputVector]

### qgis:minimumboundinggeometry: Minimum bounding geometry
This algorithm creates geometries which enclose the features from an input layer.
Numerous enclosing geometry types are supported, including bounding boxes (envelopes), oriented rectangles, circles and convex hulls.
Optionally, the features can be grouped by a field. If set, this causes the output layer to contain one feature per grouped value with a minimal geometry covering just the features with matching values.
Parameters:
- INPUT [source]: Input layer
- FIELD [field]: Field (optional, set if features should be grouped by class) (optional)
- TYPE [enum]: Geometry type (options 0=Envelope (Bounding Box), 1=Minimum Oriented Rectangle, 2=Minimum Enclosing Circle, 3=Convex Hull)
- OUTPUT [sink]: Bounding geometry
Outputs: OUTPUT [outputVector]

### qgis:pointsdisplacement: Points displacement
Offsets nearby point features by moving nearby points by a preset amount to minimize overlapping features.
Parameters:
- INPUT [source]: Input layer
- PROXIMITY [distance]: Minimum distance to other points (default 1.0)
- DISTANCE [distance]: Displacement distance (default 1.0)
- HORIZONTAL [boolean]: Horizontal distribution for two point case
- OUTPUT [sink]: Displaced
Outputs: OUTPUT [outputVector]

### qgis:rectanglesovalsdiamondsvariable: Rectangles, ovals, diamonds (variable)
Parameters:
- INPUT [source]: Input layer
- SHAPE [enum]: Buffer shape (options 0=Rectangles, 1=Diamonds, 2=Ovals)
- WIDTH [field]: Width field
- HEIGHT [field]: Height field
- ROTATION [field]: Rotation field (optional)
- SEGMENTS [number]: Number of segments (default 36)
- OUTPUT [sink]: Output
Outputs: OUTPUT [outputVector]

### qgis:variabledistancebuffer: Variable distance buffer
This algorithm computes a buffer area for all the features in an input layer. The size of the buffer for a given feature is defined by an attribute, so it allows different features to have different buffer sizes.
Parameters:
- INPUT [source]: Input layer
- FIELD [field]: Distance field
- SEGMENTS [number]: Segments (default 5)
- DISSOLVE [boolean]: Dissolve result (default False)
- END_CAP_STYLE [enum]: End cap style (default 0; options 0=Round, 1=Flat, 2=Square)
- JOIN_STYLE [enum]: Join style (default 0; options 0=Round, 1=Miter, 2=Bevel)
- MITER_LIMIT [number]: Miter limit (default 2)
- OUTPUT [sink]: Buffer
Outputs: OUTPUT [outputVector]


## QGIS / Vector selection

### qgis:randomextractwithinsubsets: Random extract within subsets
This algorithm takes a vector layer and generates a new one that contains only a subset of the features in the input layer.
The subset is defined randomly, using a percentage or count value to define the total number of features in the subset.
The percentage/count value is not applied to the whole layer, but instead to each category. Categories are defined according to a given attribute, which is also specified as an input parameter for the algorithm.
Parameters:
- INPUT [source]: Input layer
- FIELD [field]: ID field
- METHOD [enum]: Method (default 0; options 0=Number of selected features, 1=Percentage of selected features)
- NUMBER [number]: Number/percentage of selected features (default 10)
- OUTPUT [sink]: Extracted (random stratified)
Outputs: OUTPUT [outputVector]

### qgis:randomselection: Random selection
This algorithm takes a vector layer and selects a subset of its features. No new layer is generated by this algorithm.
The subset is defined randomly, using a percentage or count value to define the total number of features in the subset.
Parameters:
- INPUT [vector]: Input layer
- METHOD [enum]: Method (default 0; options 0=Number of selected features, 1=Percentage of selected features)
- NUMBER [number]: Number/percentage of selected features (default 10)
Outputs: OUTPUT [outputVector]

### qgis:randomselectionwithinsubsets: Random selection within subsets
This algorithm takes a vector layer and selects a subset of its features. No new layer is generated by this algorithm.
The subset is defined randomly, using a percentage or count value to define the total number of features in the subset.
The percentage/count value is not applied to the whole layer, but instead to each category. Categories are defined according to a given attribute, which is also specified as an input parameter for the algorithm.
Parameters:
- INPUT [vector]: Input layer
- FIELD [field]: ID field
- METHOD [enum]: Method (default 0; options 0=Number of selected features, 1=Percentage of selected features)
- NUMBER [number]: Number/percentage of selected features (default 10)
Outputs: OUTPUT [outputVector]

### qgis:selectbyattribute: Select by attribute
This algorithm creates a selection in a vector layer. The criteria for selected features is defined based on the values of an attribute from the input layer.
Parameters:
- INPUT [vector]: Input layer
- FIELD [field]: Selection attribute
- OPERATOR [enum]: Operator (default 0; options 0==, 1=≠, 2=>, 3=≥, 4=<, 5=≤, 6=begins with, 7=contains, 8=is null, 9=is not null, 10=does not contain)
- VALUE [string]: Value (optional)
- METHOD [enum]: Modify current selection by (default 0; options 0=creating new selection, 1=adding to current selection, 2=removing from current selection, 3=selecting within current selection)
Outputs: OUTPUT [outputVector]

### qgis:selectbyexpression: Select by expression
This algorithm creates a selection in a vector layer. The criteria for selecting features is based on a QGIS expression.
For help with QGIS expression functions, see the inbuilt help for specific functions which is available in the expression builder.
Parameters:
- INPUT [vector]: Input layer
- EXPRESSION [expression]: Expression
- METHOD [enum]: Modify current selection by (default 0; options 0=creating new selection, 1=adding to current selection, 2=removing from current selection, 3=selecting within current selection)
Outputs: OUTPUT [outputVector]


## QGIS / Vector table

### qgis:advancedpythonfieldcalculator: Advanced Python field calculator
This algorithm adds a new attribute to a vector layer, with values resulting from applying an expression to each feature. The expression is defined as a Python function.
Parameters:
- INPUT [source]: Input layer
- FIELD_NAME [string]: Result field name (default NewField)
- FIELD_TYPE [enum]: Field type (options 0=Integer (32 bit), 1=Decimal (double), 2=Text (string), 3=Boolean, 4=Date, 5=Time, 6=Date & Time, 7=Binary Object (BLOB), 8=String List, 9=Integer List, 10=Decimal (double) List)
- FIELD_LENGTH [number]: Field length (default 10)
- FIELD_PRECISION [number]: Field precision (default 3)
- GLOBAL [string]: Global expression (optional)
- FORMULA [string]: Formula (default value = )
- OUTPUT [sink]: Calculated
Outputs: OUTPUT [outputVector]

### qgis:texttofloat: Text to float
This algorithm modifies the type of a given attribute in a vector layer, converting a text attribute containing numeric strings into a numeric attribute.
Parameters:
- INPUT [source]: Input layer
- FIELD [field]: Text attribute to convert to float
- OUTPUT [sink]: Float from text
Outputs: OUTPUT [outputVector]


## QGIS (3D) / Vector geometry

### 3d:tessellate: Tessellate
This algorithm tessellates a polygon geometry layer, dividing the geometries into triangular components.
The output layer consists of multipolygon geometries for each input feature, with each multipolygon consisting of multiple triangle component polygons.
Parameters:
- INPUT [source]: Input layer
- OUTPUT [sink]: Tessellated
Outputs: OUTPUT [outputVector]


## QGIS (PDAL) / Point cloud conversion

### pdal:convertformat: Convert format
This algorithm converts point cloud to a different file format, e. g. creates compressed LAZ.
Parameters:
- INPUT [pointcloud]: Input layer
- OUTPUT [pointCloudDestination]: Converted
Outputs: OUTPUT [outputPointCloud]

### pdal:exportraster: Export to raster
This algorithm exports point cloud data to a 2D raster grid having cell size of given resolution, writing values from the specified attribute.
Parameters:
- INPUT [pointcloud]: Input layer
- ATTRIBUTE [attribute]: Attribute (default Z)
- RESOLUTION [number]: Resolution of the density raster (default 1)
- TILE_SIZE [number]: Tile size for parallel runs (default 1000)
- FILTER_EXPRESSION [expression]: Filter expression (optional)
- FILTER_EXTENT [extent]: Cropping extent (optional)
- ORIGIN_X [number]: X origin of a tile for parallel runs (optional)
- ORIGIN_Y [number]: Y origin of a tile for parallel runs (optional)
- OUTPUT [rasterDestination]: Exported
Outputs: OUTPUT [outputRaster]

### pdal:exportrastertin: Export to raster (using triangulation)
This algorithm exports point cloud data to a 2D raster grid using a triangulation of points and then interpolating cell values from triangles.
Parameters:
- INPUT [pointcloud]: Input layer
- RESOLUTION [number]: Resolution of the density raster (default 1)
- TILE_SIZE [number]: Tile size for parallel runs (default 1000)
- FILTER_EXPRESSION [expression]: Filter expression (optional)
- FILTER_EXTENT [extent]: Cropping extent (optional)
- ORIGIN_X [number]: X origin of a tile for parallel runs (optional)
- ORIGIN_Y [number]: Y origin of a tile for parallel runs (optional)
- OUTPUT [rasterDestination]: Exported (using triangulation)
Outputs: OUTPUT [outputRaster]

### pdal:exportvector: Export to vector
This algorithm exports point cloud data to a vector layer with 3D points (a GeoPackage), optionally with extra attributes.
Parameters:
- INPUT [pointcloud]: Input layer
- ATTRIBUTE [attribute]: Attribute (optional)
- FILTER_EXPRESSION [expression]: Filter expression (optional)
- FILTER_EXTENT [extent]: Cropping extent (optional)
- OUTPUT [vectorDestination]: Exported
Outputs: OUTPUT [outputVector]


## QGIS (PDAL) / Point cloud data management

### pdal:assignprojection: Assign projection
This algorithm assigns point cloud CRS if it is not present or wrong.
Parameters:
- INPUT [pointcloud]: Input layer
- CRS [crs]: Desired CRS (default EPSG:4326)
- OUTPUT [pointCloudDestination]: Output layer
Outputs: OUTPUT [outputPointCloud]

### pdal:clip: Clip
This algorithm clips point cloud with clipping polygons, the resulting point cloud contains points that are inside these polygons.
Parameters:
- INPUT [pointcloud]: Input layer
- OVERLAY [vector]: Clipping polygons
- FILTER_EXPRESSION [expression]: Filter expression (optional)
- FILTER_EXTENT [extent]: Cropping extent (optional)
- OUTPUT [pointCloudDestination]: Clipped
Outputs: OUTPUT [outputPointCloud]

### pdal:createcopc: Create COPC
This algorithm creates a COPC file for each input point cloud file.
Parameters:
- LAYERS [multilayer]: Input layers
- OUTPUT [folderDestination]: Output directory (optional)
Outputs: OUTPUT [outputFolder], OUTPUT_LAYERS [outputMultilayer]

### pdal:info: Information
This algorithm outputs basic metadata from the point cloud file.
Parameters:
- INPUT [pointcloud]: Input layer
- OUTPUT [fileDestination]: Layer information
Outputs: OUTPUT [outputHtml]

### pdal:merge: Merge
This algorithm merges multiple point cloud files to a single one.
Parameters:
- LAYERS [multilayer]: Input layers
- FILTER_EXPRESSION [expression]: Filter expression (optional)
- FILTER_EXTENT [extent]: Cropping extent (optional)
- OUTPUT [pointCloudDestination]: Merged
Outputs: OUTPUT [outputPointCloud]

### pdal:reproject: Reproject
This algorithm reprojects point cloud to a different coordinate reference system.
Parameters:
- INPUT [pointcloud]: Input layer
- CRS [crs]: Target CRS (default EPSG:4326)
- OPERATION [coordinateoperation]: Coordinate operation (optional)
- OUTPUT [pointCloudDestination]: Reprojected
Outputs: OUTPUT [outputPointCloud]

### pdal:thinbydecimate: Thin (by skipping points)
This algorithm creates a thinned version of the point cloud by keeping only every N-th point.
Parameters:
- INPUT [pointcloud]: Input layer
- POINTS_NUMBER [number]: Number of points to skip (default 1)
- FILTER_EXPRESSION [expression]: Filter expression (optional)
- FILTER_EXTENT [extent]: Cropping extent (optional)
- OUTPUT [pointCloudDestination]: Thinned (by decimation)
Outputs: OUTPUT [outputPointCloud]

### pdal:thinbyradius: Thin (by sampling radius)
This algorithm creates a thinned version of the point cloud by performing sampling by distance point.
Parameters:
- INPUT [pointcloud]: Input layer
- SAMPLING_RADIUS [number]: Sampling radius (in map units) (default 1.0)
- FILTER_EXPRESSION [expression]: Filter expression (optional)
- FILTER_EXTENT [extent]: Cropping extent (optional)
- OUTPUT [pointCloudDestination]: Thinned (by radius)
Outputs: OUTPUT [outputPointCloud]

### pdal:tile: Tile
This algorithm creates tiles from input data.
Parameters:
- LAYERS [multilayer]: Input layers
- LENGTH [number]: Tile length (default 1000.0)
- CRS [crs]: Assign CRS (optional)
- OUTPUT [folderDestination]: Output directory
Outputs: OUTPUT [outputFolder]

### pdal:virtualpointcloud: Build virtual point cloud (VPC)
This algorithm creates a virtual point cloud from input data.
Parameters:
- LAYERS [multilayer]: Input layers
- BOUNDARY [boolean]: Calculate boundary polygons (default False)
- STATISTICS [boolean]: Calculate statistics (default False)
- OVERVIEW [boolean]: Build overview point cloud (default False)
- OUTPUT [pointCloudDestination]: Virtual point cloud
Outputs: OUTPUT [outputPointCloud]


## QGIS (PDAL) / Point cloud extraction

### pdal:boundary: Boundary
This algorithm exports a polygon file containing point cloud layer boundary. It may contain holes and it may be a multi-part polygon.
Parameters:
- INPUT [pointcloud]: Input layer
- RESOLUTION [number]: Resolution of cells used to calculate boundary (optional)
- THRESHOLD [number]: Minimal number of points in a cell to consider cell occupied (optional)
- FILTER_EXPRESSION [expression]: Filter expression (optional)
- FILTER_EXTENT [extent]: Cropping extent (optional)
- OUTPUT [vectorDestination]: Boundary
Outputs: OUTPUT [outputVector]

### pdal:density: Density
This algorithm exports a raster file where each cell contains number of points that are in that cell's area.
Parameters:
- INPUT [pointcloud]: Input layer
- RESOLUTION [number]: Resolution of the density raster (default 1)
- TILE_SIZE [number]: Tile size for parallel runs (default 1000)
- FILTER_EXPRESSION [expression]: Filter expression (optional)
- FILTER_EXTENT [extent]: Cropping extent (optional)
- ORIGIN_X [number]: X origin of a tile for parallel runs (optional)
- ORIGIN_Y [number]: Y origin of a tile for parallel runs (optional)
- OUTPUT [rasterDestination]: Density
Outputs: OUTPUT [outputRaster]

### pdal:filter: Filter
This algorithm extracts point from the input point cloud which match PDAL expression and/or are inside of a cropping rectangle.
Parameters:
- INPUT [pointcloud]: Input layer
- FILTER_EXPRESSION [expression]: Filter expression
- FILTER_EXTENT [extent]: Cropping extent (optional)
- OUTPUT [pointCloudDestination]: Filtered
Outputs: OUTPUT [outputPointCloud]


## QGIS (native c++) / 3D Tiles

### native:b3dmtogltf: Convert B3DM to GLTF
This algorithm converts files from the legacy B3DM format to GLTF.
Parameters:
- INPUT [file]: Input B3DM
- OUTPUT [fileDestination]: Output file
Outputs: OUTPUT [outputFile]

### native:gltftovector: Convert GLTF to vector features
This algorithm converts GLTF content to standard vector layer formats.
Parameters:
- INPUT [file]: Input GLTF
- OUTPUT_POLYGONS [sink]: Output polygons (optional)
- OUTPUT_LINES [sink]: Output lines (optional)
Outputs: OUTPUT_POLYGONS [outputVector], OUTPUT_LINES [outputVector]


## QGIS (native c++) / Cartography

### native:angletonearest: Align points to features
This algorithm calculates the rotation required to align point features with their nearest feature from another reference layer. A new field is added to the output layer which is filled with the angle (in degrees, clockwise) to the nearest reference feature.
Optionally, the output layer's symbology can be set to automatically use the calculated rotation field to rotate marker symbols.
If desired, a maximum distance to use when aligning points can be set, to avoid aligning isolated points to distant features.
Parameters:
- INPUT [source]: Input layer
- REFERENCE_LAYER [source]: Reference layer
- MAX_DISTANCE [distance]: Maximum distance to consider (optional)
- FIELD_NAME [string]: Angle field name (default rotation)
- APPLY_SYMBOLOGY [boolean]: Automatically apply symbology (default True)
- OUTPUT [sink]: Aligned layer
Outputs: OUTPUT [outputVector]

### native:atlaslayouttoimage: Export atlas layout as image
This algorithm outputs an atlas layout to a set of image files (e.g. PNG or JPEG images).
If a coverage layer is set, the selected layout's atlas settings exposed in this algorithm will be overwritten. In this case, an empty filter or sort by expression will turn those settings off.
Parameters:
- LAYOUT [layout]: Atlas layout
- COVERAGE_LAYER [vector]: Coverage layer (optional)
- FILTER_EXPRESSION [expression]: Filter expression (optional)
- SORTBY_EXPRESSION [expression]: Sort expression (optional)
- SORTBY_REVERSE [boolean]: Reverse sort order (used when a sort expression is provided) (default False)
- FILENAME_EXPRESSION [expression]: Output filename expression (default 'output_'||@atlas_featurenumber)
- FOLDER [file]: Output folder
- LAYERS [multilayer]: Map layers to assign to unlocked map item(s) (optional)
- EXTENSION [enum]: Image format (default 8; options 0=bmp, 1=cur, 2=icns, 3=ico, 4=jpeg, 5=jpg, 6=pbm, 7=pgm, 8=png, 9=ppm, 10=tif, 11=tiff, 12=wbmp, 13=webp, 14=xbm, 15=xpm)
- DPI [number]: DPI (leave blank for default layout DPI) (optional)
- GEOREFERENCE [boolean]: Generate world file (default True)
- INCLUDE_METADATA [boolean]: Export RDF metadata (title, author, etc.) (default True)
- ANTIALIAS [boolean]: Enable antialiasing (default True)

### native:atlaslayouttomultiplepdf: Export atlas layout as PDF (multiple files)
This algorithm outputs an atlas layout to multiple PDF files.
If a coverage layer is set, the selected layout's atlas settings exposed in this algorithm will be overwritten. In this case, an empty filter or sort by expression will turn those settings off.
Parameters:
- LAYOUT [layout]: Atlas layout
- COVERAGE_LAYER [vector]: Coverage layer (optional)
- FILTER_EXPRESSION [expression]: Filter expression (optional)
- SORTBY_EXPRESSION [expression]: Sort expression (optional)
- SORTBY_REVERSE [boolean]: Reverse sort order (used when a sort expression is provided) (default False)
- LAYERS [multilayer]: Map layers to assign to unlocked map item(s) (optional)
- DPI [number]: DPI (leave blank for default layout DPI) (optional)
- FORCE_VECTOR [boolean]: Always export as vectors (default False)
- FORCE_RASTER [boolean]: Always export as raster (default False)
- GEOREFERENCE [boolean]: Append georeference information (default True)
- INCLUDE_METADATA [boolean]: Export RDF metadata (title, author, etc.) (default True)
- DISABLE_TILED [boolean]: Disable tiled raster layer exports (default False)
- SIMPLIFY [boolean]: Simplify geometries to reduce output file size (default True)
- TEXT_FORMAT [enum]: Text export (default 0; options 0=Always Export Text as Paths (Recommended), 1=Always Export Text as Text Objects, 2=Prefer Exporting Text as Text Objects)
- IMAGE_COMPRESSION [enum]: Image compression (default 0; options 0=Lossy (JPEG), 1=Lossless)
- OUTPUT_FILENAME [expression]: Output filename (optional)
- OUTPUT_FOLDER [file]: Output folder

### native:atlaslayouttopdf: Export atlas layout as PDF (single file)
This algorithm outputs an atlas layout as a single PDF file.
If a coverage layer is set, the selected layout's atlas settings exposed in this algorithm will be overwritten. In this case, an empty filter or sort by expression will turn those settings off.
Parameters:
- LAYOUT [layout]: Atlas layout
- COVERAGE_LAYER [vector]: Coverage layer (optional)
- FILTER_EXPRESSION [expression]: Filter expression (optional)
- SORTBY_EXPRESSION [expression]: Sort expression (optional)
- SORTBY_REVERSE [boolean]: Reverse sort order (used when a sort expression is provided) (default False)
- LAYERS [multilayer]: Map layers to assign to unlocked map item(s) (optional)
- DPI [number]: DPI (leave blank for default layout DPI) (optional)
- FORCE_VECTOR [boolean]: Always export as vectors (default False)
- FORCE_RASTER [boolean]: Always export as raster (default False)
- GEOREFERENCE [boolean]: Append georeference information (default True)
- INCLUDE_METADATA [boolean]: Export RDF metadata (title, author, etc.) (default True)
- DISABLE_TILED [boolean]: Disable tiled raster layer exports (default False)
- SIMPLIFY [boolean]: Simplify geometries to reduce output file size (default True)
- TEXT_FORMAT [enum]: Text export (default 0; options 0=Always Export Text as Paths (Recommended), 1=Always Export Text as Text Objects, 2=Prefer Exporting Text as Text Objects)
- IMAGE_COMPRESSION [enum]: Image compression (default 0; options 0=Lossy (JPEG), 1=Lossless)
- OUTPUT [fileDestination]: PDF file
Outputs: OUTPUT [outputFile]

### native:categorizeusingstyle: Create categorized renderer from styles
This algorithm sets a vector layer's renderer to a categorized renderer using matching symbols from a style database. If no style file is specified, symbols from the user's current style library are used instead.
The specified expression (or field name) is used to create categories for the renderer. A category will be created for each unique value within the layer.
Each category is individually matched to the symbols which exist within the specified QGIS XML style database. Whenever a matching symbol name is found, the category's symbol will be set to this matched symbol.
The matching is case-insensitive by default, but can be made case-sensitive if required.
Optionally, non-alphanumeric characters in both the category value and symbol name can be ignored while performing the match. This allows for greater tolerance when matching categories to symbols.
If desired, tables can also be output containing lists of the categories which could not be matched to symbols, and symbols which were not matched to categories.
Parameters:
- INPUT [vector]: Input layer
- FIELD [expression]: Categorize using expression
- STYLE [file]: Style database (leave blank to use saved symbols) (optional)
- CASE_SENSITIVE [boolean]: Use case-sensitive match to symbol names (default False)
- TOLERANT [boolean]: Ignore non-alphanumeric characters while matching (default False)
- NON_MATCHING_CATEGORIES [sink]: Non-matching categories (optional)
- NON_MATCHING_SYMBOLS [sink]: Non-matching symbol names (optional)
Outputs: OUTPUT [outputVector], NON_MATCHING_CATEGORIES [outputVector], NON_MATCHING_SYMBOLS [outputVector]

### native:combinestyles: Combine style databases
This algorithm combines multiple QGIS style databases into a single style database. If any symbols exist with duplicate names between the different source databases these will be renamed to have unique names in the output combined database.
Parameters:
- INPUT [multilayer]: Input databases
- OUTPUT [fileDestination]: Output style database
- OBJECTS [enum]: Objects to combine (default [0, 1, 2, 3]; options 0=Symbols, 1=Color ramps, 2=Text formats, 3=Label settings)
Outputs: OUTPUT [outputFile], SYMBOLS [outputNumber], COLORRAMPS [outputNumber], TEXTFORMATS [outputNumber], LABELSETTINGS [outputNumber]

### native:extractlabels: Extract labels
This algorithm extracts label information from a rendered map at a given extent and scale.
If a map theme is provided, the rendered map will match the visibility and symbology of that theme. If left blank, all visible layers from the project will be used.
Extracted label information include: position (served as point geometries), the associated layer name and feature ID, label text, rotation (in degree, clockwise), multiline alignment, and font details.
Parameters:
- EXTENT [extent]: Map extent
- SCALE [scale]: Map scale
- MAP_THEME [maptheme]: Map theme (optional)
- INCLUDE_UNPLACED [boolean]: Include unplaced labels (default True)
- DPI [number]: Map resolution (in DPI) (optional; default 96.0)
- OUTPUT [sink]: Extracted labels
Outputs: OUTPUT [outputVector]

### native:printlayoutmapextenttolayer: Print layout map extent to layer
This algorithm creates a polygon layer containing the extent of a print layout map item (or items), with attributes specifying the map size (in layout units), scale and rotation.
If the map item parameter is specified, then only the matching map extent will be exported. If it is not specified, all map extents from the layout will be exported.
Optionally, a specific output CRS can be specified. If it is not specified, the original map item CRS will be used.
Parameters:
- LAYOUT [layout]: Print layout
- MAP [layoutitem]: Map item (optional)
- CRS [crs]: Override CRS (optional)
- OUTPUT [sink]: Extent
Outputs: OUTPUT [outputVector], WIDTH [outputNumber], HEIGHT [outputNumber], SCALE [outputNumber], ROTATION [outputNumber]

### native:printlayouttoimage: Export print layout as image
This algorithm outputs a print layout as an image file (e.g. PNG or JPEG images).
Parameters:
- LAYOUT [layout]: Print layout
- LAYERS [multilayer]: Map layers to assign to unlocked map item(s) (optional)
- DPI [number]: DPI (leave blank for default layout DPI) (optional)
- GEOREFERENCE [boolean]: Generate world file (default True)
- INCLUDE_METADATA [boolean]: Export RDF metadata (title, author, etc.) (default True)
- ANTIALIAS [boolean]: Enable antialiasing (default True)
- OUTPUT [fileDestination]: Image file
Outputs: OUTPUT [outputFile]

### native:printlayouttopdf: Export print layout as PDF
This algorithm outputs a print layout as a PDF file.
Parameters:
- LAYOUT [layout]: Print layout
- LAYERS [multilayer]: Map layers to assign to unlocked map item(s) (optional)
- DPI [number]: DPI (leave blank for default layout DPI) (optional)
- FORCE_VECTOR [boolean]: Always export as vectors (default False)
- FORCE_RASTER [boolean]: Always export as raster (default False)
- GEOREFERENCE [boolean]: Append georeference information (default True)
- INCLUDE_METADATA [boolean]: Export RDF metadata (title, author, etc.) (default True)
- DISABLE_TILED [boolean]: Disable tiled raster layer exports (default False)
- SIMPLIFY [boolean]: Simplify geometries to reduce output file size (default True)
- TEXT_FORMAT [enum]: Text export (default 0; options 0=Always Export Text as Paths (Recommended), 1=Always Export Text as Text Objects, 2=Prefer Exporting Text as Text Objects)
- IMAGE_COMPRESSION [enum]: Image compression (default 0; options 0=Lossy (JPEG), 1=Lossless)
- SEPARATE_LAYERS [boolean]: Export layers as separate PDF files (default False)
- OUTPUT [fileDestination]: PDF file
Outputs: OUTPUT [outputFile]

### native:setlayerstyle: Set layer style
This algorithm applies the style to a layer. The style must be defined as QML file.
Parameters:
- INPUT [layer]: Layer
- STYLE [file]: Style file
Outputs: OUTPUT [outputLayer]

### native:stylefromproject: Create style database from project
This algorithm extracts all style objects (including symbols, color ramps, text formats and label settings) from a QGIS project.
The extracted symbols are saved to a QGIS style database (XML format), which can be managed and imported via the Style Manager dialog.
Parameters:
- INPUT [file]: Input project (leave blank to use current) (optional)
- OUTPUT [fileDestination]: Output style database
- OBJECTS [enum]: Objects to extract (default [0, 1, 2, 3]; options 0=Symbols, 1=Color ramps, 2=Text formats, 3=Label settings)
Outputs: OUTPUT [outputFile], SYMBOLS [outputNumber], COLORRAMPS [outputNumber], TEXTFORMATS [outputNumber], LABELSETTINGS [outputNumber]

### native:transferannotationsfrommain: Transfer annotations from main layer
This algorithm transfers all annotations from the main annotation layer in a project to a new annotation layer.
Parameters:
- LAYER_NAME [string]: New layer name (default Annotations)
Outputs: OUTPUT [outputLayer]


## QGIS (native c++) / Check geometry

### native:checkgeometryangle: Small angles
This algorithm checks the angles of line or polygon geometries.
Angles below the minimum angle are errors.
Parameters:
- INPUT [source]: Input layer
- UNIQUE_ID [field]: Unique feature identifier
- MIN_ANGLE [number]: Minimum angle (in degrees) (default 0)
- ERRORS [sink]: Small angle errors
- TOLERANCE [number]: Tolerance (default 8)
Outputs: ERRORS [outputVector]

### native:checkgeometryarea: Small polygons
This algorithm checks the areas of polygon geometries.
Areas below the area threshold are errors.
Parameters:
- INPUT [source]: Input layer
- UNIQUE_ID [field]: Unique feature identifier
- AREATHRESHOLD [area]: Area threshold (default 0)
- ERRORS [sink]: Small polygons errors
- OUTPUT [sink]: Small polygons features (optional)
- TOLERANCE [number]: Tolerance (default 8)
Outputs: ERRORS [outputVector], OUTPUT [outputVector]

### native:checkgeometrycontained: Features inside polygon
This algorithm checks the input geometries contained in the polygons from the polygon layers list.
A polygon layer can be checked against itself.
Input features contained in the polygon layers features are errors.
Parameters:
- INPUT [source]: Input layer
- UNIQUE_ID [field]: Unique feature identifier
- POLYGONS [multilayer]: Polygon layers
- OUTPUT [sink]: Errors from contained features (optional)
- ERRORS [sink]: Contained features
- TOLERANCE [number]: Tolerance (default 8)
Outputs: OUTPUT [outputVector], ERRORS [outputVector]

### native:checkgeometrydangle: Dangle-end lines
This algorithm checks lines with a dangle end.
Lines with a dangle end are errors.
Parameters:
- INPUT [source]: Input layer
- UNIQUE_ID [field]: Unique feature identifier
- ERRORS [sink]: Dangle-end errors
- OUTPUT [sink]: Dangle-end features (optional)
- TOLERANCE [number]: Tolerance (default 8)
Outputs: ERRORS [outputVector], OUTPUT [outputVector]

### native:checkgeometrydegeneratepolygon: Degenerate polygons
This algorithm checks the polygons with less than 3 points, which are degenerate polygons.
Degenerate polygons are errors.
Parameters:
- INPUT [source]: Input layer
- UNIQUE_ID [field]: Unique feature identifier
- ERRORS [sink]: Degenerate polygons errors
- OUTPUT [sink]: Degenerate polygons features (optional)
- TOLERANCE [number]: Tolerance (default 8)
Outputs: ERRORS [outputVector], OUTPUT [outputVector]

### native:checkgeometryduplicate: Duplicated geometries
This algorithm checks the duplicate geometries.
Duplicate geometries are errors.
Parameters:
- INPUT [source]: Input layer
- UNIQUE_ID [field]: Unique feature identifier
- ERRORS [sink]: Duplicate geometries errors
- OUTPUT [sink]: Duplicate geometries (optional)
- TOLERANCE [number]: Tolerance (default 8)
Outputs: ERRORS [outputVector], OUTPUT [outputVector]

### native:checkgeometryduplicatenodes: Duplicated vertices
This algorithm checks the vertices of line and polygon geometries.
Duplicated vertices are errors.
Parameters:
- INPUT [source]: Input layer
- UNIQUE_ID [field]: Unique feature identifier
- ERRORS [sink]: Duplicated vertices errors
- OUTPUT [sink]: Duplicated vertices features (optional)
- TOLERANCE [number]: Tolerance (default 8)
Outputs: ERRORS [outputVector], OUTPUT [outputVector]

### native:checkgeometryfollowboundaries: Polygons exceeding boundaries
This algorithm checks if the polygons follow the boundaries of the reference layer.
Polygons not following reference boundaries are errors.
Parameters:
- INPUT [source]: Input layer
- UNIQUE_ID [field]: Unique feature identifier
- ERRORS [sink]: Errors exceeding boundaries
- OUTPUT [sink]: Features exceeding boundaries (optional)
- REF_LAYER [source]: Reference layer
- TOLERANCE [number]: Tolerance (default 8)
Outputs: ERRORS [outputVector], OUTPUT [outputVector]

### native:checkgeometrygap: Small gaps
This algorithm checks the gaps between polygons.
Gaps with an area smaller than the gap threshold are errors.
If an allowed gaps layer is given, the gaps contained in polygons from this layer will be ignored.
An optional buffer can be applied to the allowed gaps.
The neighbors output layer is needed for the fix geometry (gaps) algorithm. It is a 1-N relational table for correspondance between a gap and the unique id of its neighbor features.
Parameters:
- INPUT [source]: Input layer
- UNIQUE_ID [field]: Unique feature identifier
- GAP_THRESHOLD [number]: Gap threshold (default 0)
- ALLOWED_GAPS_LAYER [vector]: Allowed gaps layer (optional)
- ALLOWED_GAPS_BUFFER [distance]: Allowed gaps buffer (optional)
- NEIGHBORS [sink]: Neighbors layer
- ERRORS [sink]: Gap errors (optional)
- OUTPUT [sink]: Gap features
- TOLERANCE [number]: Tolerance (default 8)
Outputs: NEIGHBORS [outputVector], ERRORS [outputVector], OUTPUT [outputVector]

### native:checkgeometryhole: Holes
This algorithm checks the holes of polygon geometries.
Holes are errors.
Parameters:
- INPUT [source]: Input layer
- UNIQUE_ID [field]: Unique feature identifier
- ERRORS [sink]: Holes errors
- OUTPUT [sink]: Polygons with holes (optional)
- TOLERANCE [number]: Tolerance (default 8)
Outputs: ERRORS [outputVector], OUTPUT [outputVector]

### native:checkgeometrylineintersection: Lines intersecting each other
This algorithm checks intersections between line geometries.
Intersections between two different lines are errors.
Parameters:
- INPUT [source]: Input layer
- UNIQUE_ID [field]: Unique feature identifier
- ERRORS [sink]: Intersection errors
- OUTPUT [sink]: Intersecting feature (optional)
- TOLERANCE [number]: Tolerance (default 8)
Outputs: ERRORS [outputVector], OUTPUT [outputVector]

### native:checkgeometrylinelayerintersection: Lines intersecting other layer
This algorithm checks if the input line layer features intersect with the check layer features.
An input feature that intersects with a check layer feature is an error.
Parameters:
- INPUT [source]: Input layer
- UNIQUE_ID [field]: Unique feature identifier
- CHECK_LAYER [source]: Check layer
- ERRORS [sink]: Line intersecting other layer errors
- OUTPUT [sink]: Line intersecting other layer features (optional)
- TOLERANCE [number]: Tolerance (default 8)
Outputs: ERRORS [outputVector], OUTPUT [outputVector]

### native:checkgeometrymissingvertex: Missing vertices along borders
This algorithm checks for missing vertices along polygon borders.
To be topologically correct, a vertex at the junction of two polygons must be present on both polygons. Missing vertices are errors.
Parameters:
- INPUT [source]: Input layer
- UNIQUE_ID [field]: Unique feature identifier
- ERRORS [sink]: Missing vertices errors
- OUTPUT [sink]: Missing vertices features (optional)
- TOLERANCE [number]: Tolerance (default 8)
Outputs: ERRORS [outputVector], OUTPUT [outputVector]

### native:checkgeometrymultipart: Strictly multipart
This algorithm checks if multipart geometries have more than one part.
Multipart geometries with only one part are errors.
Parameters:
- INPUT [source]: Input layer
- UNIQUE_ID [field]: Unique feature identifier
- ERRORS [sink]: One-part geometry errors
- OUTPUT [sink]: One-part geometry features (optional)
- TOLERANCE [number]: Tolerance (default 8)
Outputs: ERRORS [outputVector], OUTPUT [outputVector]

### native:checkgeometryoverlap: Overlaps
This algorithm checks the overlapping areas.
Overlapping areas smaller than the minimum overlapping area are errors.
Parameters:
- INPUT [source]: Input layer
- UNIQUE_ID [field]: Unique feature identifier
- ERRORS [sink]: Overlap errors
- OUTPUT [sink]: Overlap features (optional)
- MIN_OVERLAP_AREA [number]: min overlap area (default 0)
- TOLERANCE [number]: Tolerance (default 8)
Outputs: ERRORS [outputVector], OUTPUT [outputVector]

### native:checkgeometrypointcoveredbyline: Points outside lines
This algorithm checks if the points in the input layer are covered by a line in the selected line layers.
A point not covered by a line is an error.
Parameters:
- INPUT [source]: Input layer
- UNIQUE_ID [field]: Unique feature identifier
- LINES [multilayer]: Line layers
- ERRORS [sink]: Points not covered by a line
- TOLERANCE [number]: Tolerance (default 8)
Outputs: ERRORS [outputVector]

### native:checkgeometrypointinpolygon: Points outside polygons
This algorithm checks if points from the input layer are in polygons from the selected polygon layers.
Points that are not fully inside polygons are errors.
Parameters:
- INPUT [source]: Input layer
- UNIQUE_ID [field]: Unique feature identifier
- POLYGONS [multilayer]: Polygon layers
- ERRORS [sink]: Points outside polygons errors
- TOLERANCE [number]: Tolerance (default 8)
Outputs: ERRORS [outputVector]

### native:checkgeometrysegmentlength: Small segments
This algorithm checks the minimum segment length of line or polygon geometries.
Segments shorter than the minimum length are errors.
Parameters:
- INPUT [source]: Input layer
- UNIQUE_ID [field]: Unique feature identifier
- ERRORS [sink]: Short segments errors
- OUTPUT [sink]: Short segments features (optional)
- MIN_SEGMENT_LENGTH [number]: minimum segment length (default 0)
- TOLERANCE [number]: Tolerance (default 8)
Outputs: ERRORS [outputVector], OUTPUT [outputVector]

### native:checkgeometryselfcontact: Self-contacts
This algorithm checks if the geometry has self contact points (in line or polygon).
Self contacts are errors.
Parameters:
- INPUT [source]: Input layer
- UNIQUE_ID [field]: Unique feature identifier
- ERRORS [sink]: Self contact error points
- OUTPUT [sink]: Self contact features (optional)
- TOLERANCE [number]: Tolerance (default 8)
Outputs: ERRORS [outputVector], OUTPUT [outputVector]

### native:checkgeometryselfintersection: Self-intersections
This algorithm checks self-intersecting geometries.
Self-intersecting geometries are errors.
Parameters:
- INPUT [source]: Input layer
- UNIQUE_ID [field]: Unique feature identifier
- ERRORS [sink]: Self-intersecting errors
- OUTPUT [sink]: Self-intersecting features (optional)
- TOLERANCE [number]: Tolerance (default 8)
Outputs: ERRORS [outputVector], OUTPUT [outputVector]

### native:checkgeometrysliverpolygon: Sliver polygons
This algorithm checks sliver polygons.
The thinness is the ratio between the area of the minimum square containing the polygon and the area of the polygon itself (a square has a thinness value of 1).
The thinness value is between 1 and +infinity.
If a polygon has an area higher than the maximum area, it is skipped (a maximum area value of 0 means no area check).
Polygons having a thinness higher than the maximum thinness are errors.
To fix sliver polygons, use the "Fix small polygons" algorithm.
Parameters:
- INPUT [source]: Input layer
- UNIQUE_ID [field]: Unique feature identifier
- ERRORS [sink]: Sliver polygon errors
- OUTPUT [sink]: Sliver polygon features (optional)
- MAX_THINNESS [number]: Maximum thinness (default 20)
- MAX_AREA [number]: Maximum area (map units squared) (default 0)
- TOLERANCE [number]: Tolerance (default 8)
Outputs: ERRORS [outputVector], OUTPUT [outputVector]


## QGIS (native c++) / Database

### native:importintopostgis: Export to PostgreSQL
This algorithm exports a vector layer to a PostgreSQL database, creating a new table.
Prior to this a connection between QGIS and the PostgreSQL database has to be created (for example through the QGIS Browser panel).
Parameters:
- INPUT [source]: Layer to export
- DATABASE [providerconnection]: Database (connection name)
- SCHEMA [databaseschema]: Schema (schema name) (optional; default public)
- TABLENAME [databasetable]: Table to export to (leave blank to use layer name) (optional)
- PRIMARY_KEY [field]: Primary key field (optional)
- GEOMETRY_COLUMN [string]: Geometry column (default geom)
- ENCODING [string]: Encoding (optional; default UTF-8)
- OVERWRITE [boolean]: Overwrite (default True)
- CREATEINDEX [boolean]: Create spatial index (default True)
- LOWERCASE_NAMES [boolean]: Convert field names to lowercase (default True)
- DROP_STRING_LENGTH [boolean]: Drop length constraints on character fields (default False)
- FORCE_SINGLEPART [boolean]: Create single-part geometries instead of multipart (default False)

### native:package: Package layers
This algorithm collects a number of existing layers and packages them together into a single GeoPackage database.
Parameters:
- LAYERS [multilayer]: Input layers
- OUTPUT [fileDestination]: Destination GeoPackage
- OVERWRITE [boolean]: Overwrite existing GeoPackage (default False)
- SAVE_STYLES [boolean]: Save layer styles into GeoPackage (default True)
- SAVE_METADATA [boolean]: Save layer metadata into GeoPackage (default True)
- SELECTED_FEATURES_ONLY [boolean]: Save only selected features (default False)
- EXPORT_RELATED_LAYERS [boolean]: Export related layers following relations defined in the project (default False)
Outputs: OUTPUT [outputFile], OUTPUT_LAYERS [outputMultilayer]

### native:postgisexecutesql: PostgreSQL execute SQL
This algorithm executes a SQL command on a PostgreSQL database.
Parameters:
- DATABASE [providerconnection]: Database (connection name)
- SQL [string]: SQL query

### native:spatialiteexecutesql: SpatiaLite execute SQL
This algorithm executes a SQL command on a SpatiaLite database. The database is determined by an input layer or file.
Parameters:
- DATABASE [vector]: Database layer (or file)
- SQL [string]: SQL query

### native:spatialiteexecutesqlregistered: SpatiaLite execute SQL (registered DB)
This algorithm executes a SQL command on a SpatiaLite database.
Parameters:
- DATABASE [providerconnection]: Database (connection name)
- SQL [string]: SQL query


## QGIS (native c++) / File tools

### native:filedownloader: Download file via HTTP(S)
This algorithm downloads a URL to the file system with an HTTP(S) GET or POST request
Parameters:
- URL [string]: URL
- METHOD [enum]: Method (default 0; options 0=GET, 1=POST)
- DATA [string]: Data (optional)
- OUTPUT [fileDestination]: File destination
Outputs: OUTPUT [outputFile]

### native:httprequest: HTTP(S) POST/GET request
This algorithm performs a HTTP(S) POST/GET request and returns the HTTP status code and the reply data.
If an error occurs then the error code and the message will be returned.
Optionally, the result can be written to a file on disk.
By default the algorithm will warn on errors. Optionally, the algorithm can be set to treat HTTP errors as failures.
Parameters:
- URL [string]: URL
- METHOD [enum]: Method (default 0; options 0=GET, 1=POST)
- DATA [string]: POST data (optional)
- OUTPUT [fileDestination]: File destination (optional)
- AUTH_CONFIG [authcfg]: Authentication (optional)
- FAIL_ON_ERROR [boolean]: Consider HTTP errors as failures (default False)
Outputs: OUTPUT [outputFile], ERROR_CODE [outputNumber], ERROR_MESSAGE [outputString], STATUS_CODE [outputNumber], RESULT_DATA [outputString]

### native:openurl: Open file or URL
This algorithm opens files in their default associated application, or URLs in the user's default web browser.
Parameters:
- URL [string]: URL or file path
Outputs: SUCCESS [outputBoolean]


## QGIS (native c++) / Fix geometry

### native:fixgeometryangle: Delete small angles
This algorithm deletes vertices based on an error layer from the "Small angles" algorithm in the "Check geometry" section.
When deletion of a vertex results in a duplicate vertex (when a spike vertex is deleted), the duplicate vertex is deleted to keep a single vertex and preserve topology.
Parameters:
- INPUT [source]: Input layer
- ERRORS [source]: Error layer
- UNIQUE_ID [field]: Field of original feature unique identifier (default id)
- PART_IDX [field]: Field of part index (default gc_partidx)
- RING_IDX [field]: Field of ring index (default gc_ringidx)
- VERTEX_IDX [field]: Field of vertex index (default gc_vertidx)
- OUTPUT [sink]: Small angle fixed layer
- REPORT [sink]: Report layer from fixing small angles
- TOLERANCE [number]: Tolerance (default 8)
Outputs: OUTPUT [outputVector], REPORT [outputVector]

### native:fixgeometryarea: Fix small polygons
This algorithm merges neighboring polygons according to the chosen method, based on an error layer from the "Small polygons" algorithm in the "Check geometry" section.
Parameters:
- INPUT [source]: Input layer
- ERRORS [source]: Error layer
- METHOD [enum]: Method (options 0=Merge with neighboring polygon with longest shared edge, 1=Merge with neighboring polygon with largest area, 2=Merge with neighboring polygon with identical attribute value, if any, or leave as is)
- MERGE_ATTRIBUTE [field]: Field to consider when merging polygons with the identical attribute method (optional)
- UNIQUE_ID [field]: Field of original feature unique identifier (default id)
- PART_IDX [field]: Field of part index (default gc_partidx)
- RING_IDX [field]: Field of ring index (default gc_ringidx)
- VERTEX_IDX [field]: Field of vertex index (default gc_vertidx)
- OUTPUT [sink]: Small polygons merged layer
- REPORT [sink]: Report layer from merging small polygons
- TOLERANCE [number]: Tolerance (default 8)
Outputs: OUTPUT [outputVector], REPORT [outputVector]

### native:fixgeometrydeletefeatures: Delete features
This algorithm deletes error features listed in the errors layer from an algorithm in the "Check geometry" section.
The required inputs are the original layer used in the check algorithm, its unique id field, and its corresponding errors layer.
For instance, it can be used after the following check algorithms to delete error features:Feature inside polygon
Degenerate polygons
Small segments
Duplicated geometries
etc.
Parameters:
- INPUT [source]: Input layer
- ERRORS [source]: Error layer
- UNIQUE_ID [field]: Field of original feature unique identifier
- OUTPUT [sink]: Cleaned layer
- REPORT [sink]: Report layer from deleting features
Outputs: OUTPUT [outputVector], REPORT [outputVector]

### native:fixgeometryduplicatenodes: Delete duplicated vertices
This algorithm delete duplicate vertices based on an error layer from the "Duplicated vertices" algorithm in the "Check geometry" section.
Parameters:
- INPUT [source]: Input layer
- ERRORS [source]: Error layer
- UNIQUE_ID [field]: Field of original feature unique identifier (default id)
- PART_IDX [field]: Field of part index (default gc_partidx)
- RING_IDX [field]: Field of ring index (default gc_ringidx)
- VERTEX_IDX [field]: Field of vertex index (default gc_vertidx)
- OUTPUT [sink]: Fixed duplicate vertices layer
- REPORT [sink]: Report layer from fixing duplicate vertices
- TOLERANCE [number]: Tolerance (default 8)
Outputs: OUTPUT [outputVector], REPORT [outputVector]

### native:fixgeometrygap: Fill gaps
This algorithm fills the gaps based on a gap and neighbors layer from the "Small gaps" algorithm in the "Check geometry" section.
3 different fixing methods are available, which will give different results.
Parameters:
- INPUT [source]: Input layer
- NEIGHBORS [source]: Neighbors layer
- GAPS [source]: Gaps layer
- METHOD [enum]: Method (options 0=Add to longest shared edge, 1=Create new feature, 2=Add to largest neighbouring area)
- UNIQUE_ID [field]: Field of original feature unique identifier
- ERROR_ID_IDX [field]: Field of error id (default gc_errorid)
- OUTPUT [sink]: Gaps-filled layer
- REPORT [sink]: Report layer from fixing gaps
- TOLERANCE [number]: Tolerance (default 8)
Outputs: OUTPUT [outputVector], REPORT [outputVector]

### native:fixgeometryhole: Fill holes
This algorithm deletes holes based on an error layer from the "Holes" algorithm in the "Check geometry" section.
Parameters:
- INPUT [source]: Input layer
- ERRORS [source]: Error layer
- UNIQUE_ID [field]: Field of original feature unique identifier (default id)
- PART_IDX [field]: Field of part index (default gc_partidx)
- RING_IDX [field]: Field of ring index (default gc_ringidx)
- VERTEX_IDX [field]: Field of vertex index (default gc_vertidx)
- OUTPUT [sink]: Holes-filled layer
- REPORT [sink]: Report layer from fixing holes
- TOLERANCE [number]: Tolerance (default 8)
Outputs: OUTPUT [outputVector], REPORT [outputVector]

### native:fixgeometrymissingvertex: Add missing vertices along borders
This algorithm adds the missing vertices along polygons borders, based on an error layer from the "Missing vertices along borders" algorithm in the "Check geometry" section.
Parameters:
- INPUT [source]: Input layer
- ERRORS [source]: Error layer
- UNIQUE_ID [field]: Field of original feature unique identifier (default id)
- PART_IDX [field]: Field of part index (default gc_partidx)
- RING_IDX [field]: Field of ring index (default gc_ringidx)
- VERTEX_IDX [field]: Field of vertex index (default gc_vertidx)
- OUTPUT [sink]: Border vertices fixed layer
- REPORT [sink]: Report layer from fixing border vertices
- TOLERANCE [number]: Tolerance (default 8)
Outputs: OUTPUT [outputVector], REPORT [outputVector]

### native:fixgeometrymultipart: Convert to strictly multipart
This algorithm converts multipart geometries that consists of only one geometry into singlepart geometries, based on an error layer from the "Strict multipart" algorithm in the "Check geometry" section.
This algorithm does not change the layer geometry type, which will remain multipart.
Parameters:
- INPUT [source]: Input layer
- ERRORS [source]: Error layer
- UNIQUE_ID [field]: Field of original feature unique identifier (default id)
- OUTPUT [sink]: Strictly-multipart layer
- REPORT [sink]: Report layer from fixing multiparts
- TOLERANCE [number]: Tolerance (default 8)
Outputs: OUTPUT [outputVector], REPORT [outputVector]

### native:fixgeometryoverlap: Delete overlaps
This algorithm deletes overlap sections based on an error layer from the "Overlap" algorithm in the "Check geometry" section.
Parameters:
- INPUT [source]: Input layer
- ERRORS [source]: Error layer
- UNIQUE_ID [field]: Field of original feature unique identifier
- OVERLAP_FEATURE_UNIQUE_IDX [field]: Field of overlap feature unique identifier
- ERROR_VALUE_ID [field]: Field of error value (default gc_error)
- OUTPUT [sink]: No-overlap layer
- REPORT [sink]: Report layer from fixing overlaps
- TOLERANCE [number]: Tolerance (default 8)
Outputs: OUTPUT [outputVector], REPORT [outputVector]

### native:fixgeometryselfintersection: Split self-intersecting geometries
This algorithm splits self intersecting lines or polygons according to the chosen method, based on an error layer from the "Self-intersections" algorithm in the "Check geometry" section.
Parameters:
- INPUT [source]: Input layer
- ERRORS [source]: Error layer
- METHOD [enum]: Method (options 0=Split feature into a multi-part feature, 1=Split feature into multiple single-part features)
- UNIQUE_ID [field]: Field of original feature unique identifier
- PART_IDX [field]: Field of part index (default gc_partidx)
- RING_IDX [field]: Field of ring index (default gc_ringidx)
- VERTEX_IDX [field]: Field of vertex index (default gc_vertidx)
- SEGMENT_1 [field]: Field of segment 1 (default gc_segment_1)
- SEGMENT_2 [field]: Field of segment 2 (default gc_segment_2)
- OUTPUT [sink]: Self-intersections fixed layer
- REPORT [sink]: Report layer from fixing self-intersections
- TOLERANCE [number]: Tolerance (default 8)
Outputs: OUTPUT [outputVector], REPORT [outputVector]


## QGIS (native c++) / GPS

### native:convertgpsdata: Convert GPS data
This algorithm uses the GPSBabel tool to convert a GPS data file from a range of formats to the GPX standard format.
Parameters:
- INPUT [file]: Input file
- FORMAT [string]: Format
- FEATURE_TYPE [enum]: Feature type (default 0; options 0=Waypoints, 1=Routes, 2=Tracks)
- OUTPUT [fileDestination]: Output
Outputs: OUTPUT [outputFile], OUTPUT_LAYER [outputVector]

### native:convertgpxfeaturetype: Convert GPX feature type
This algorithm uses the GPSBabel tool to convert GPX features from one type to another (e.g. converting all waypoint features to a route feature).
Parameters:
- INPUT [file]: Input file
- CONVERSION [enum]: Conversion (default 0; options 0=Waypoints from a Route, 1=Waypoints from a Track, 2=Route from Waypoints, 3=Track from Waypoints)
- OUTPUT [fileDestination]: Output
Outputs: OUTPUT [outputFile], OUTPUT_LAYER [outputVector]

### native:downloadgpsdata: Download GPS data from device
This algorithm uses the GPSBabel tool to download data from a GPS device into the GPX standard format.
Parameters:
- DEVICE [string]: Device
- PORT [string]: Port
- FEATURE_TYPE [enum]: Feature type (default 0; options 0=Waypoints, 1=Routes, 2=Tracks)
- OUTPUT [fileDestination]: Output
Outputs: OUTPUT [outputFile], OUTPUT_LAYER [outputVector]

### native:uploadgpsdata: Upload GPS data to device
This algorithm uses the GPSBabel tool to upload data to a GPS device from the GPX standard format.
Parameters:
- INPUT [file]: Input file
- DEVICE [string]: Device
- PORT [string]: Port
- FEATURE_TYPE [enum]: Feature type (default 0; options 0=Waypoints, 1=Routes, 2=Tracks)


## QGIS (native c++) / Interpolation

### native:linedensity: Line density
This algorithm calculates a density measure of linear features which is obtained in a circular neighborhood within each raster cell. First, the length of the segment of each line that is intersected by the circular neighborhood is multiplied with the lines weight factor. In a second step, all length values are summed and divided by the area of the circular neighborhood. This process is repeated for all raster cells.
Parameters:
- INPUT [source]: Input line layer
- WEIGHT [field]: Weight field  (optional)
- RADIUS [distance]: Search radius (default 10)
- PIXEL_SIZE [distance]: Pixel size (default 10)
- CREATE_OPTIONS [string]: Creation options (optional)
- CREATION_OPTIONS [string]: Creation options (optional)
- OUTPUT [rasterDestination]: Line density raster
Outputs: OUTPUT [outputRaster]


## QGIS (native c++) / Layer tools

### native:exportlayersinformation: Export layer(s) information
This algorithm creates a polygon layer with features corresponding to the extent of selected layer(s).
Additional layer details - CRS, provider name, file path, layer name, subset filter, abstract and attribution - are attached as attributes to each feature.
Parameters:
- LAYERS [multilayer]: Input layer(s)
- OUTPUT [sink]: Output
Outputs: OUTPUT [outputVector]

### native:exporttospreadsheet: Export to spreadsheet
This algorithm collects a number of existing layers and exports them to a spreadsheet document.
Optionally the layers can be appended to an existing spreadsheet as additional sheets.
Parameters:
- LAYERS [multilayer]: Input layers
- USE_ALIAS [boolean]: Use field aliases as column headings (default False)
- FORMATTED_VALUES [boolean]: Export formatted values instead of raw values (default False)
- OUTPUT [fileDestination]: Destination spreadsheet
- OVERWRITE [boolean]: Overwrite existing spreadsheet (default True)
Outputs: OUTPUT [outputFile], OUTPUT_LAYERS [outputMultilayer]

### native:polygonfromlayerextent: Extract layer extent
This algorithm takes a map layer and generates a new vector layer with the minimum bounding box (rectangle polygon with N-S orientation) that covers the input layer. Optionally, the extent can be enlarged to a rounded value.
Parameters:
- INPUT [layer]: Input layer
- ROUND_TO [distance]: Round values to (default 0)
- OUTPUT [sink]: Extent
Outputs: OUTPUT [outputVector]


## QGIS (native c++) / Mesh

### native:exportmeshedges: Export mesh edges
This algorithm exports a mesh layer's edges to a line vector layer, with the dataset values on edges as attribute values.
Parameters:
- INPUT [mesh]: Input mesh layer
- DATASET_GROUPS [meshdatasetgroups]: Dataset groups (optional; default [])
- DATASET_TIME [meshdatasettime]: Dataset time
- CRS_OUTPUT [crs]: Output coordinate system (optional)
- VECTOR_OPTION [enum]: Export vector option (default 0; options 0=Cartesian (x,y), 1=Polar (magnitude,degree), 2=Cartesian and Polar)
- OUTPUT [sink]: Output vector layer
Outputs: OUTPUT [outputVector]

### native:exportmeshfaces: Export mesh faces
This algorithm exports a mesh layer's faces to a polygon vector layer, with the dataset values on faces as attribute values.
Parameters:
- INPUT [mesh]: Input mesh layer
- DATASET_GROUPS [meshdatasetgroups]: Dataset groups (optional; default [])
- DATASET_TIME [meshdatasettime]: Dataset time
- CRS_OUTPUT [crs]: Output coordinate system (optional)
- VECTOR_OPTION [enum]: Export vector option (default 0; options 0=Cartesian (x,y), 1=Polar (magnitude,degree), 2=Cartesian and Polar)
- OUTPUT [sink]: Output vector layer
Outputs: OUTPUT [outputVector]

### native:exportmeshongrid: Export mesh on grid
This algorithm exports a mesh layer's dataset values to a gridded point vector layer, with the dataset values on each point as attribute values.
For data on volume (3D stacked dataset values), the exported dataset values are averaged on faces using the method defined in the mesh layer properties (default is Multi level averaging method).
1D meshes are not supported.
Parameters:
- INPUT [mesh]: Input mesh layer
- DATASET_GROUPS [meshdatasetgroups]: Dataset groups (default [])
- DATASET_TIME [meshdatasettime]: Dataset time
- EXTENT [extent]: Extent (optional)
- GRID_SPACING [distance]: Grid spacing (default 10)
- CRS_OUTPUT [crs]: Output coordinate system (optional)
- VECTOR_OPTION [enum]: Export vector option (default 0; options 0=Cartesian (x,y), 1=Polar (magnitude,degree), 2=Cartesian and Polar)
- OUTPUT [sink]: Output vector layer
Outputs: OUTPUT [outputVector]

### native:exportmeshvertices: Export mesh vertices
This algorithm exports a mesh layer's vertices to a point vector layer, with the dataset values on vertices as attribute values.
Parameters:
- INPUT [mesh]: Input mesh layer
- DATASET_GROUPS [meshdatasetgroups]: Dataset groups (optional; default [])
- DATASET_TIME [meshdatasettime]: Dataset time
- CRS_OUTPUT [crs]: Output coordinate system (optional)
- VECTOR_OPTION [enum]: Export vector option (default 0; options 0=Cartesian (x,y), 1=Polar (magnitude,degree), 2=Cartesian and Polar)
- OUTPUT [sink]: Output vector layer
Outputs: OUTPUT [outputVector]

### native:meshcontours: Export contours
This algorithm creates contours as a vector layer from a mesh scalar dataset.
Parameters:
- INPUT [mesh]: Input mesh layer
- DATASET_GROUPS [meshdatasetgroups]: Dataset groups (default [])
- DATASET_TIME [meshdatasettime]: Dataset time
- INCREMENT [number]: Increment between contour levels (optional)
- MINIMUM [number]: Minimum contour level (optional)
- MAXIMUM [number]: Maximum contour level (optional)
- CONTOUR_LEVEL_LIST [string]: List of contours level (optional)
- CRS_OUTPUT [crs]: Output coordinate system (optional)
- OUTPUT_LINES [sink]: Exported contour lines
- OUTPUT_POLYGONS [sink]: Exported contour polygons
Outputs: OUTPUT_LINES [outputVector], OUTPUT_POLYGONS [outputVector]

### native:meshexportcrosssection: Export cross section dataset values on lines from mesh
This algorithm extracts mesh's dataset values from line contained in a vector layer.
Each line is discretized with a resolution distance parameter for extraction of values on its vertices.
Parameters:
- INPUT [mesh]: Input mesh layer
- DATASET_GROUPS [meshdatasetgroups]: Dataset groups (default [])
- DATASET_TIME [meshdatasettime]: Dataset time
- INPUT_LINES [source]: Lines for data export
- RESOLUTION [distance]: Line segmentation resolution (default 10.0)
- COORDINATES_DIGITS [number]: Digits count for coordinates (default 2)
- DATASET_DIGITS [number]: Digits count for dataset value (default 2)
- OUTPUT [fileDestination]: Exported data CSV file
Outputs: OUTPUT [outputFile]

### native:meshexporttimeseries: Export time series values from points of a mesh dataset
This algorithm extracts mesh's dataset time series values from points contained in a vector layer.
If the time step is kept to its default value (0 hours), the time step used is the one of the two first datasets of the first selected dataset group.
Parameters:
- INPUT [mesh]: Input mesh layer
- DATASET_GROUPS [meshdatasetgroups]: Dataset groups (default [])
- STARTING_TIME [meshdatasettime]: Starting time
- FINISHING_TIME [meshdatasettime]: Finishing time
- TIME_STEP [number]: Time step (hours) (optional; default 0)
- INPUT_POINTS [source]: Points for data export
- COORDINATES_DIGITS [number]: Digits count for coordinates (default 2)
- DATASET_DIGITS [number]: Digits count for dataset value (default 2)
- OUTPUT [fileDestination]: Exported data CSV file
Outputs: OUTPUT [outputFile]

### native:meshrasterize: Rasterize mesh dataset
This algorithm creates a raster layer from a mesh dataset.
For data on volume (3D stacked dataset values), the exported dataset values are averaged on faces using the method defined in the mesh layer properties (default is Multi level averaging method).
1D meshes are not supported.
Parameters:
- INPUT [mesh]: Input mesh layer
- DATASET_GROUPS [meshdatasetgroups]: Dataset groups (optional; default [])
- DATASET_TIME [meshdatasettime]: Dataset time
- EXTENT [extent]: Extent (optional)
- PIXEL_SIZE [distance]: Pixel size (default 1)
- CRS_OUTPUT [crs]: Output coordinate system (optional)
- CREATE_OPTIONS [string]: Creation options (optional)
- CREATION_OPTIONS [string]: Creation options (optional)
- OUTPUT [rasterDestination]: Output raster layer
Outputs: OUTPUT [outputRaster]

### native:surfacetopolygon: Surface to polygon
This algorithm exports a polygon layer containing a mesh layer's boundary. It may contain holes and it may be a multi-part polygon.
Parameters:
- INPUT [mesh]: Input mesh layer
- CRS_OUTPUT [crs]: Output coordinate system (optional)
- OUTPUT [sink]: Output vector layer
Outputs: OUTPUT [outputVector]

### native:tinmeshcreation: TIN Mesh Creation
This algorithm creates a TIN mesh layer from vector layers.
Parameters:
- SOURCE_DATA [tininputlayers]: Input layers
- MESH_FORMAT [enum]: Output format (default 0; options 0=2DM, 1=SELAFIN, 2=PLY, 3=Ugrid, 4=Mike21)
- CRS_OUTPUT [crs]: Output coordinate system (optional)
- OUTPUT_MESH [fileDestination]: Output file
Outputs: OUTPUT_MESH [outputFile]


## QGIS (native c++) / Metadata tools

### native:addhistorymetadata: Add history metadata
This algorithm adds a new history entry to the layer's metadata.
Parameters:
- INPUT [layer]: Layer
- HISTORY [string]: History entry
Outputs: OUTPUT [outputLayer]

### native:copylayermetadata: Copy layer metadata
This algorithm copies metadata from a source layer to a target layer.
Any existing metadata in the target layer will be replaced.
Parameters:
- SOURCE [layer]: Source layer
- TARGET [layer]: Target layer
- DEFAULT [boolean]: Save metadata as default (default False)
Outputs: OUTPUT [outputLayer]

### native:exportlayermetadata: Export layer metadata
This algorithm exports layer's metadata to a QMD file.
Parameters:
- INPUT [layer]: Layer
- OUTPUT [fileDestination]: Output
Outputs: OUTPUT [outputFile]

### native:setlayermetadata: Set layer metadata
This algorithm applies the metadata to a layer. The metadata must be defined as QMD file.
Any existing metadata in the layer will be replaced.
Parameters:
- INPUT [layer]: Layer
- METADATA [file]: Metadata file
- DEFAULT [boolean]: Save metadata as default (default False)
Outputs: OUTPUT [outputLayer]

### native:setmetadatafields: Set metadata fields
This algorithm sets various metadata fields for a layer.
Parameters:
- INPUT [layer]: Layer
- IDENTIFIER [string]: Identifier (optional)
- PARENT_IDENTIFIER [string]: Parent identifier (optional)
- TITLE [string]: Title (optional)
- TYPE [string]: Type (optional)
- LANGUAGE [string]: Language (optional)
- ENCODING [string]: Encoding (optional)
- ABSTRACT [string]: Abstract (optional)
- CRS [crs]: Coordinate reference system (optional)
- FEES [string]: Fees (optional)
- IGNORE_EMPTY [boolean]: Ignore empty fields (default False)
Outputs: OUTPUT [outputLayer]

### native:updatelayermetadata: Update layer metadata
This algorithm copies all non-empty metadata fields from a source layer to a target layer.
Leaves empty input fields unchanged in the target.
Parameters:
- SOURCE [layer]: Source layer
- TARGET [layer]: Target layer
Outputs: OUTPUT [outputLayer]


## QGIS (native c++) / Modeler tools

### native:calculateexpression: Calculate expression
This algorithm calculates the result of a QGIS expression and makes it available for use in other parts of the model.
Parameters:
- INPUT [string]: Input
Outputs: OUTPUT [outputVariant]

### native:condition: Conditional branch
This algorithm adds a conditional branch into a model, allowing parts of the model to be executed based on the result of an expression evaluation.
Parameters:

### native:createdirectory: Create directory
This algorithm creates a new directory on a file system. Directories will be created recursively, creating all required parent directories in order to construct the full specified directory path.
No errors will be raised if the directory already exists.
Parameters:
- PATH [layer]: Directory path
Outputs: OUTPUT [outputFolder]

### native:filter: Feature filter
This algorithm filters features from the input layer and redirects them to one or more outputs.
Parameters:
- INPUT [source]: Input layer

### native:filterlayersbytype: Filter layers by type
This algorithm filters layer by their type. Incoming layers will be directed to different outputs based on whether they are a vector or raster layer.
Parameters:
- INPUT [layer]: Input layer
- VECTOR [vectorDestination]: Vector features (optional)
- RASTER [rasterDestination]: Raster layer (optional)
Outputs: VECTOR [outputVector], RASTER [outputRaster]

### native:loadlayer: Load layer into project
This algorithm loads a layer to the current project.
Parameters:
- INPUT [layer]: Layer
- NAME [string]: Loaded layer name
Outputs: OUTPUT [outputLayer]

### native:raiseexception: Raise exception
This algorithm raises an exception and cancels a model's execution.
The exception message can be customized, and optionally an expression based condition can be specified. If an expression condition is used, then the exception will only be raised if the expression result is true. A false result indicates that no exception will be raised, and the model execution can continue uninterrupted.
Parameters:
- MESSAGE [string]: Error message
- CONDITION [expression]: Condition (optional)

### native:raisemessage: Raise message
This algorithm raises an information message in the log.
The message can be customized, and optionally an expression based condition can be specified. If an expression condition is used, then the message will only be logged if the expression result is true. A false result indicates that no message will be logged.
Parameters:
- MESSAGE [string]: Information message
- CONDITION [expression]: Condition (optional)

### native:raisewarning: Raise warning
This algorithm raises a warning message in the log.
The warning message can be customized, and optionally an expression based condition can be specified. If an expression condition is used, then the warning will only be logged if the expression result is true. A false result indicates that no warning will be logged.
Parameters:
- MESSAGE [string]: Warning message
- CONDITION [expression]: Condition (optional)

### native:renamelayer: Rename layer
This algorithm renames a layer.
Parameters:
- INPUT [layer]: Layer
- NAME [string]: New name
Outputs: OUTPUT [outputLayer]

### native:savelog: Save log to file
This algorithm saves the model's execution log to a file.
Optionally, the log can be saved in a HTML formatted version.
Parameters:
- OUTPUT [fileDestination]: Log file
- USE_HTML [boolean]: Use HTML formatting (default False)
Outputs: OUTPUT [outputHtml]

### native:setprojectvariable: Set project variable
This algorithm sets an expression variable for the current project.
Parameters:
- NAME [string]: Variable name
- VALUE [string]: Variable value

### native:stringconcatenation: String concatenation
This algorithm concatenates two strings together.
Parameters:
- INPUT_1 [string]: Input 1
- INPUT_2 [string]: Input 2
Outputs: CONCATENATION [outputString]


## QGIS (native c++) / Network analysis

### native:serviceareafromlayer: Service area (from layer)
This algorithm creates a new vector layer with all the edges or parts of edges of a network line layer that can be reached within a distance or a time, starting from features of a point layer. The distance and the time (both referred to as "travel cost") must be specified respectively in the network layer units or in hours.
Parameters:
- INPUT [source]: Vector layer representing network
- STRATEGY [enum]: Path type to calculate (default 0; options 0=Shortest, 1=Fastest)
- DIRECTION_FIELD [field]: Direction field (optional)
- VALUE_FORWARD [string]: Value for forward direction (optional)
- VALUE_BACKWARD [string]: Value for backward direction (optional)
- VALUE_BOTH [string]: Value for both directions (optional)
- DEFAULT_DIRECTION [enum]: Default direction (default 2; options 0=Forward direction, 1=Backward direction, 2=Both directions)
- SPEED_FIELD [field]: Speed field (optional)
- DEFAULT_SPEED [number]: Default speed (km/h) (default 50)
- TOLERANCE [distance]: Topology tolerance (default 0)
- START_POINTS [source]: Vector layer with start points
- TRAVEL_COST [number]: Travel cost (distance for 'Shortest', time for 'Fastest') (optional; default 0)
- TRAVEL_COST2 [number]: Travel cost (distance for 'Shortest', time for 'Fastest') (default 0)
- INCLUDE_BOUNDS [boolean]: Include upper/lower bound points (optional; default False)
- POINT_TOLERANCE [distance]: Maximum point distance from network (optional)
- OUTPUT_LINES [sink]: Service area (lines) (optional)
- OUTPUT [sink]: Service area (boundary nodes) (optional)
- OUTPUT_NON_ROUTABLE [sink]: Non-routable features (optional)
Outputs: OUTPUT_LINES [outputVector], OUTPUT [outputVector], OUTPUT_NON_ROUTABLE [outputVector]

### native:serviceareafrompoint: Service area (from point)
This algorithm creates a new vector layer with all the edges or parts of edges of a network line layer that can be reached within a distance or a time, starting from a point feature. The distance and the time (both referred to as "travel cost") must be specified respectively in the network layer units or in hours.
Parameters:
- INPUT [source]: Vector layer representing network
- STRATEGY [enum]: Path type to calculate (default 0; options 0=Shortest, 1=Fastest)
- DIRECTION_FIELD [field]: Direction field (optional)
- VALUE_FORWARD [string]: Value for forward direction (optional)
- VALUE_BACKWARD [string]: Value for backward direction (optional)
- VALUE_BOTH [string]: Value for both directions (optional)
- DEFAULT_DIRECTION [enum]: Default direction (default 2; options 0=Forward direction, 1=Backward direction, 2=Both directions)
- SPEED_FIELD [field]: Speed field (optional)
- DEFAULT_SPEED [number]: Default speed (km/h) (default 50)
- TOLERANCE [distance]: Topology tolerance (default 0)
- START_POINT [point]: Start point
- TRAVEL_COST [number]: Travel cost (distance for 'Shortest', time for 'Fastest') (optional; default 0)
- TRAVEL_COST2 [number]: Travel cost (distance for 'Shortest', time for 'Fastest') (default 0)
- POINT_TOLERANCE [distance]: Maximum point distance from network (optional)
- INCLUDE_BOUNDS [boolean]: Include upper/lower bound points (optional; default False)
- OUTPUT_LINES [sink]: Service area (lines) (optional)
- OUTPUT [sink]: Service area (boundary nodes) (optional)
Outputs: OUTPUT_LINES [outputVector], OUTPUT [outputVector]

### native:shortestpathlayertopoint: Shortest path (layer to point)
This algorithm computes optimal (shortest or fastest) routes from multiple start points defined by a vector layer and a given end point.
Parameters:
- INPUT [source]: Vector layer representing network
- STRATEGY [enum]: Path type to calculate (default 0; options 0=Shortest, 1=Fastest)
- DIRECTION_FIELD [field]: Direction field (optional)
- VALUE_FORWARD [string]: Value for forward direction (optional)
- VALUE_BACKWARD [string]: Value for backward direction (optional)
- VALUE_BOTH [string]: Value for both directions (optional)
- DEFAULT_DIRECTION [enum]: Default direction (default 2; options 0=Forward direction, 1=Backward direction, 2=Both directions)
- SPEED_FIELD [field]: Speed field (optional)
- DEFAULT_SPEED [number]: Default speed (km/h) (default 50)
- TOLERANCE [distance]: Topology tolerance (default 0)
- START_POINTS [source]: Vector layer with start points
- END_POINT [point]: End point
- POINT_TOLERANCE [distance]: Maximum point distance from network (optional)
- OUTPUT [sink]: Shortest path
- OUTPUT_NON_ROUTABLE [sink]: Non-routable features (optional)
Outputs: OUTPUT [outputVector], OUTPUT_NON_ROUTABLE [outputVector]

### native:shortestpathpointtolayer: Shortest path (point to layer)
This algorithm computes optimal (shortest or fastest) route between a given start point and multiple end points defined by a point vector layer.
Parameters:
- INPUT [source]: Vector layer representing network
- STRATEGY [enum]: Path type to calculate (default 0; options 0=Shortest, 1=Fastest)
- DIRECTION_FIELD [field]: Direction field (optional)
- VALUE_FORWARD [string]: Value for forward direction (optional)
- VALUE_BACKWARD [string]: Value for backward direction (optional)
- VALUE_BOTH [string]: Value for both directions (optional)
- DEFAULT_DIRECTION [enum]: Default direction (default 2; options 0=Forward direction, 1=Backward direction, 2=Both directions)
- SPEED_FIELD [field]: Speed field (optional)
- DEFAULT_SPEED [number]: Default speed (km/h) (default 50)
- TOLERANCE [distance]: Topology tolerance (default 0)
- START_POINT [point]: Start point
- END_POINTS [source]: Vector layer with end points
- POINT_TOLERANCE [distance]: Maximum point distance from network (optional)
- OUTPUT [sink]: Shortest path
- OUTPUT_NON_ROUTABLE [sink]: Non-routable features (optional)
Outputs: OUTPUT [outputVector], OUTPUT_NON_ROUTABLE [outputVector]

### native:shortestpathpointtopoint: Shortest path (point to point)
This algorithm computes optimal (shortest or fastest) route between given start and end points.
Parameters:
- INPUT [source]: Vector layer representing network
- STRATEGY [enum]: Path type to calculate (default 0; options 0=Shortest, 1=Fastest)
- DIRECTION_FIELD [field]: Direction field (optional)
- VALUE_FORWARD [string]: Value for forward direction (optional)
- VALUE_BACKWARD [string]: Value for backward direction (optional)
- VALUE_BOTH [string]: Value for both directions (optional)
- DEFAULT_DIRECTION [enum]: Default direction (default 2; options 0=Forward direction, 1=Backward direction, 2=Both directions)
- SPEED_FIELD [field]: Speed field (optional)
- DEFAULT_SPEED [number]: Default speed (km/h) (default 50)
- TOLERANCE [distance]: Topology tolerance (default 0)
- START_POINT [point]: Start point
- END_POINT [point]: End point
- OUTPUT [sink]: Shortest path
- POINT_TOLERANCE [distance]: Maximum point distance from network (optional)
Outputs: OUTPUT [outputVector], TRAVEL_COST [outputNumber]


## QGIS (native c++) / Plots

### native:generateelevationprofileimage: Generate elevation profile image
This algorithm creates an elevation profile image from a list of map layer and an optional terrain.
Parameters:
- CURVE [geometry]: Profile curve
- MAP_LAYERS [multilayer]: Map layers
- WIDTH [number]: Chart width (in pixels) (default 400)
- HEIGHT [number]: Chart height (in pixels) (default 300)
- TERRAIN_LAYER [layer]: Terrain layer (optional)
- MINIMUM_DISTANCE [number]: Chart minimum distance (X axis) (optional)
- MAXIMUM_DISTANCE [number]: Chart maximum distance (X axis) (optional)
- MINIMUM_ELEVATION [number]: Chart minimum elevation (Y axis) (optional)
- MAXIMUM_ELEVATION [number]: Chart maximum elevation (Y axis) (optional)
- TEXT_COLOR [color]: Chart text color (optional; default <QColor: RGBA 0, 0, 0, 255>)
- BACKGROUND_COLOR [color]: Chart background color (optional; default <QColor: RGBA 255, 255, 255, 255>)
- BORDER_COLOR [color]: Chart border color (optional; default <QColor: RGBA 99, 99, 99, 255>)
- TOLERANCE [number]: Profile tolerance (default 5.0)
- DPI [number]: Chart DPI (default 96)
- OUTPUT [fileDestination]: Output image
Outputs: OUTPUT [outputFile]


## QGIS (native c++) / Raster analysis

### native:cellstackpercentile: Cell stack percentile
This algorithm generates a raster containing the cell-wise percentile value of a stack of input rasters. The percentile to return is determined by the percentile input value (ranges between 0 and 1). At each cell location, the specified percentile is obtained using the respective value from the stack of all overlaid and sorted cell values of the input rasters.
There are three methods for percentile calculation: Nearest rank
 Inclusive linear interpolation (PERCENTILE.INC)
 Exclusive linear interpolation (PERCENTILE.EXC)
 While the output value can stay the same for the nearest rank method (obtains the value that is nearest to the specified percentile), the linear interpolation method return unique values for different percentiles. Both interpolation methods follow their counterpart methods implemented by LibreOffice or Microsoft Excel.
The output raster's extent and resolution is defined by a reference raster. If the input raster layers that do not match the cell size of the reference raster layer will be resampled using nearest neighbor resampling. NoData values in any of the input layers will result in a NoData cell output if the Ignore NoData parameter is not set. The output raster data type will be set to the most complex data type present in the input datasets.
Parameters:
- INPUT [multilayer]: Input layers
- METHOD [enum]: Method (default 0; options 0=Nearest rank, 1=Inclusive linear interpolation (PERCENTILE.INC), 2=Exclusive linear interpolation (PERCENTILE.EXC))
- PERCENTILE [number]: Percentile (default 0.25)
- IGNORE_NODATA [boolean]: Ignore NoData values (default True)
- REFERENCE_LAYER [raster]: Reference layer
- OUTPUT_NODATA_VALUE [number]: Output NoData value (default -9999)
- CREATE_OPTIONS [string]: Creation options (optional)
- CREATION_OPTIONS [string]: Creation options (optional)
- OUTPUT [rasterDestination]: Output layer
Outputs: OUTPUT [outputRaster], EXTENT [outputString], CRS_AUTHID [outputString], WIDTH_IN_PIXELS [outputNumber], HEIGHT_IN_PIXELS [outputNumber], TOTAL_PIXEL_COUNT [outputNumber]

### native:cellstackpercentrankfromrasterlayer: Cell stack percentrank from raster layer
This algorithm generates a raster containing the cell-wise percent rank value of a stack of input rasters based on an input value raster.
At each cell location, the current value of the value raster is used ranked among the respective values in the stack of all overlaid and sorted cell values of the input rasters. For values outside of the the stack value distribution, the algorithm returns NoData because the value cannot be ranked among the cell values.
There are two methods for percentile calculation: Inclusive linearly interpolated percent rank (PERCENTRANK.INC)
 Exclusive linearly interpolated percent rank (PERCENTRANK.EXC)
 The linear interpolation method return the unique percent rank for different values. Both interpolation methods follow their counterpart methods implemented by LibreOffice or Microsoft Excel.
The output raster's extent and resolution is defined by a reference raster. If the input raster layers that do not match the cell size of the reference raster layer will be resampled using nearest neighbor resampling. NoData values in any of the input layers will result in a NoData cell output if the Ignore NoData parameter is not set. The output raster data type will always be Float32.
Parameters:
- INPUT [multilayer]: Input layers
- INPUT_VALUE_RASTER [raster]: Value raster layer
- VALUE_RASTER_BAND [band]: Value raster band (default 1)
- METHOD [enum]: Method (default 0; options 0=Inclusive linear interpolation (PERCENTRANK.INC), 1=Exclusive linear interpolation (PERCENTRANK.EXC))
- IGNORE_NODATA [boolean]: Ignore NoData values (default True)
- REFERENCE_LAYER [raster]: Reference layer
- OUTPUT_NODATA_VALUE [number]: Output NoData value (default -9999)
- CREATE_OPTIONS [string]: Creation options (optional)
- CREATION_OPTIONS [string]: Creation options (optional)
- OUTPUT [rasterDestination]: Output layer
Outputs: OUTPUT [outputRaster], EXTENT [outputString], CRS_AUTHID [outputString], WIDTH_IN_PIXELS [outputNumber], HEIGHT_IN_PIXELS [outputNumber], TOTAL_PIXEL_COUNT [outputNumber]

### native:cellstackpercentrankfromvalue: Cell stack percent rank from value
This algorithm generates a raster containing the cell-wise percent rank value of a stack of input rasters based on a single input value.
At each cell location, the specified value is ranked among the respective values in the stack of all overlaid and sorted cell values from the input rasters. For values outside of the stack value distribution, the algorithm returns NoData because the value cannot be ranked among the cell values.
There are two methods for percentile calculation: Inclusive linearly interpolated percent rank (PERCENTRANK.INC)
 Exclusive linearly interpolated percent rank (PERCENTRANK.EXC)
 The linear interpolation method return the unique percent rank for different values. Both interpolation methods follow their counterpart methods implemented by LibreOffice or Microsoft Excel.
The output raster's extent and resolution is defined by a reference raster. If the input raster layers that do not match the cell size of the reference raster layer will be resampled using nearest neighbor resampling. NoData values in any of the input layers will result in a NoData cell output if the Ignore NoData parameter is not set. The output raster data type will always be Float32.
Parameters:
- INPUT [multilayer]: Input layers
- METHOD [enum]: Method (default 0; options 0=Inclusive linear interpolation (PERCENTRANK.INC), 1=Exclusive linear interpolation (PERCENTRANK.EXC))
- VALUE [number]: Value (default 10)
- IGNORE_NODATA [boolean]: Ignore NoData values (default True)
- REFERENCE_LAYER [raster]: Reference layer
- OUTPUT_NODATA_VALUE [number]: Output NoData value (default -9999)
- CREATE_OPTIONS [string]: Creation options (optional)
- CREATION_OPTIONS [string]: Creation options (optional)
- OUTPUT [rasterDestination]: Output layer
Outputs: OUTPUT [outputRaster], EXTENT [outputString], CRS_AUTHID [outputString], WIDTH_IN_PIXELS [outputNumber], HEIGHT_IN_PIXELS [outputNumber], TOTAL_PIXEL_COUNT [outputNumber]

### native:cellstatistics: Cell statistics
The Cell statistics algorithm computes a value for each cell of the output raster. At each cell location, the output value is defined as a function of all overlaid cell values of the input rasters.
The output raster's extent and resolution is defined by a reference raster. The following functions can be applied on the input raster cells per output raster cell location:
 Sum
 Count
 Mean
 Median
 Standard deviation
 Variance
 Minimum
 Maximum
 Minority (least frequent value)
 Majority (most frequent value)
 Range (max-min)
 Variety (count of unique values)
 Input raster layers that do not match the cell size of the reference raster layer will be resampled using nearest neighbor resampling. The output raster data type will be set to the most complex data type present in the input datasets except when using the functions Mean, Standard deviation and Variance (data type is always Float32/Float64 depending on input float type) or Count and Variety (data type is always Int32).
Calculation details - general: NoData values in any of the input layers will result in a NoData cell output if the Ignore NoData parameter is not set.
Calculation details - Count: Count will always result in the number of cells without NoData values at the current cell location.
Calculation details - Median: If the number of input layers is even, the median will be calculated as the arithmetic mean of the two middle values of the ordered cell input values. In this case the output data type is Float32.
Calculation details - Minority/Majority: If no unique minority or majority could be found, the result is NoData, except all input cell values are equal.
Parameters:
- INPUT [multilayer]: Input layers
- STATISTIC [enum]: Statistic (default 0; options 0=Sum, 1=Count, 2=Mean, 3=Median, 4=Standard deviation, 5=Variance, 6=Minimum, 7=Maximum, 8=Minority, 9=Majority, 10=Range, 11=Variety)
- IGNORE_NODATA [boolean]: Ignore NoData values (default True)
- REFERENCE_LAYER [raster]: Reference layer
- OUTPUT_NODATA_VALUE [number]: Output NoData value (default -9999)
- CREATE_OPTIONS [string]: Creation options (optional)
- CREATION_OPTIONS [string]: Creation options (optional)
- OUTPUT [rasterDestination]: Output layer
Outputs: OUTPUT [outputRaster], EXTENT [outputString], CRS_AUTHID [outputString], WIDTH_IN_PIXELS [outputNumber], HEIGHT_IN_PIXELS [outputNumber], TOTAL_PIXEL_COUNT [outputNumber]

### native:equaltofrequency: Equal to frequency
This algorithm evaluates on a cell-by-cell basis the frequency (number of times) the values of an input stack of rasters are equal to the value of a value raster. 
 If multiband rasters are used in the data raster stack, the algorithm will always perform the analysis on the first band of the rasters - use GDAL to use other bands in the analysis. The input value layer serves as reference layer for the sample layers. Any NoData cells in the value raster or the data layer stack will result in a NoData cell in the output raster if the ignore NoData parameter is not checked. The output NoData value can be set manually. The output rasters extent and resolution is defined by the input raster layer and is always of int32 type.
Parameters:
- INPUT_VALUE_RASTER [raster]: Input value raster
- INPUT_VALUE_RASTER_BAND [band]: Value raster band (default 1)
- INPUT_RASTERS [multilayer]: Input raster layers
- IGNORE_NODATA [boolean]: Ignore NoData values (default False)
- OUTPUT_NODATA_VALUE [number]: Output NoData value (optional; default -9999)
- CREATE_OPTIONS [string]: Creation options (optional)
- CREATION_OPTIONS [string]: Creation options (optional)
- OUTPUT [rasterDestination]: Output layer
Outputs: OUTPUT [outputRaster], OCCURRENCE_COUNT [outputNumber], FOUND_LOCATIONS_COUNT [outputNumber], MEAN_FREQUENCY_PER_LOCATION [outputNumber], EXTENT [outputString], CRS_AUTHID [outputString], WIDTH_IN_PIXELS [outputNumber], HEIGHT_IN_PIXELS [outputNumber], TOTAL_PIXEL_COUNT [outputNumber]

### native:fuzzifyrastergaussianmembership: Fuzzify raster (gaussian membership)
This algorithm transforms an input raster to a fuzzified raster and thereby assigns values between 0 and 1 following a gaussian fuzzy membership function. The value of 0 implies no membership with the defined fuzzy set, a value of 1 depicts full membership. In between, the degree of membership of raster values follows a gaussian membership function.
The gaussian function is constructed using two user-defined input values which set the midpoint of the gaussian function (midpoint, results to 1) and a predefined function spread which controls the function spread.
This function is typically used when a certain range of raster values around a predefined function midpoint should become members of the fuzzy set.
Parameters:
- INPUT [raster]: Input Raster
- BAND [band]: Band Number (default 1)
- FUZZYMIDPOINT [number]: Function midpoint (default 10)
- FUZZYSPREAD [number]: Function spread (default 0.01)
- CREATE_OPTIONS [string]: Creation options (optional)
- CREATION_OPTIONS [string]: Creation options (optional)
- OUTPUT [rasterDestination]: Fuzzified raster
Outputs: EXTENT [outputString], CRS_AUTHID [outputString], WIDTH_IN_PIXELS [outputNumber], HEIGHT_IN_PIXELS [outputNumber], TOTAL_PIXEL_COUNT [outputNumber], OUTPUT [outputRaster]

### native:fuzzifyrasterlargemembership: Fuzzify raster (large membership)
This algorithm transforms an input raster to a fuzzified raster and thereby assigns values between 0 and 1 following the 'large' fuzzy membership function. The value of 0 implies no membership with the defined fuzzy set, a value of 1 depicts full membership. In between, the degree of membership of raster values follows the 'large' membership function.
The 'large' function is constructed using two user-defined input raster values which set the point of half membership (midpoint, results to 0.5) and a predefined function spread which controls the function uptake.
This function is typically used when larger input raster values should become members of the fuzzy set more easily than smaller values.
Parameters:
- INPUT [raster]: Input Raster
- BAND [band]: Band Number (default 1)
- FUZZYMIDPOINT [number]: Function midpoint (default 50)
- FUZZYSPREAD [number]: Function spread (default 5)
- CREATE_OPTIONS [string]: Creation options (optional)
- CREATION_OPTIONS [string]: Creation options (optional)
- OUTPUT [rasterDestination]: Fuzzified raster
Outputs: EXTENT [outputString], CRS_AUTHID [outputString], WIDTH_IN_PIXELS [outputNumber], HEIGHT_IN_PIXELS [outputNumber], TOTAL_PIXEL_COUNT [outputNumber], OUTPUT [outputRaster]

### native:fuzzifyrasterlinearmembership: Fuzzify raster (linear membership)
This algorithm transforms an input raster to a fuzzified raster and thereby assigns values between 0 and 1 following a linear fuzzy membership function. The value of 0 implies no membership with the defined fuzzy set, a value of 1 depicts full membership. In between, the degree of membership of raster values follows a linear membership function.
The linear function is constructed using two user-defined input raster values which set the point of full membership (high bound, results to 1) and no membership (low bound, results to 0) respectively. The fuzzy set in between those values is defined as a linear function.
Both increasing and decreasing fuzzy sets can be modeled by swapping the high and low bound parameters.
Parameters:
- INPUT [raster]: Input Raster
- BAND [band]: Band Number (default 1)
- FUZZYLOWBOUND [number]: Low fuzzy membership bound (default 0)
- FUZZYHIGHBOUND [number]: High fuzzy membership bound (default 1)
- CREATE_OPTIONS [string]: Creation options (optional)
- CREATION_OPTIONS [string]: Creation options (optional)
- OUTPUT [rasterDestination]: Fuzzified raster
Outputs: EXTENT [outputString], CRS_AUTHID [outputString], WIDTH_IN_PIXELS [outputNumber], HEIGHT_IN_PIXELS [outputNumber], TOTAL_PIXEL_COUNT [outputNumber], OUTPUT [outputRaster]

### native:fuzzifyrasternearmembership: Fuzzify raster (near membership)
The Fuzzify raster (near membership) algorithm transforms an input raster to a fuzzified raster and thereby assigns values between 0 and 1 following the 'near' fuzzy membership function. The value of 0 implies no membership with the defined fuzzy set, a value of 1 depicts full membership. In between, the degree of membership of raster values follows the 'near' membership function.
The 'near' function is constructed using two user-defined input values which set the midpoint of the 'near' function (midpoint, results to 1) and a predefined function spread which controls the function spread.
This function is typically used when a certain range of raster values near a predefined function midpoint should become members of the fuzzy set. The function generally shows a higher rate of decay than the gaussian membership function.
Parameters:
- INPUT [raster]: Input Raster
- BAND [band]: Band Number (default 1)
- FUZZYMIDPOINT [number]: Function midpoint (default 50)
- FUZZYSPREAD [number]: Function spread (default 0.01)
- CREATE_OPTIONS [string]: Creation options (optional)
- CREATION_OPTIONS [string]: Creation options (optional)
- OUTPUT [rasterDestination]: Fuzzified raster
Outputs: EXTENT [outputString], CRS_AUTHID [outputString], WIDTH_IN_PIXELS [outputNumber], HEIGHT_IN_PIXELS [outputNumber], TOTAL_PIXEL_COUNT [outputNumber], OUTPUT [outputRaster]

### native:fuzzifyrasterpowermembership: Fuzzify raster (power membership)
This algorithm transforms an input raster to a fuzzified raster and thereby assigns values between 0 and 1 following a power function. The value of 0 implies no membership with the defined fuzzy set, a value of 1 depicts full membership. In between, the degree of membership of raster values follows a power function.
The power function is constructed using three user-defined input raster values which set the point of full membership (high bound, results to 1), no membership (low bound, results to 0) and function exponent (only positive) respectively. The fuzzy set in between those the upper and lower bounds values is then defined as a power function.
Both increasing and decreasing fuzzy sets can be modeled by swapping the high and low bound parameters.
Parameters:
- INPUT [raster]: Input Raster
- BAND [band]: Band Number (default 1)
- FUZZYLOWBOUND [number]: Low fuzzy membership bound (default 0)
- FUZZYHIGHBOUND [number]: High fuzzy membership bound (default 1)
- FUZZYEXPONENT [number]: Membership function exponent (default 2)
- CREATE_OPTIONS [string]: Creation options (optional)
- CREATION_OPTIONS [string]: Creation options (optional)
- OUTPUT [rasterDestination]: Fuzzified raster
Outputs: EXTENT [outputString], CRS_AUTHID [outputString], WIDTH_IN_PIXELS [outputNumber], HEIGHT_IN_PIXELS [outputNumber], TOTAL_PIXEL_COUNT [outputNumber], OUTPUT [outputRaster]

### native:fuzzifyrastersmallmembership: Fuzzify raster (small membership)
The Fuzzify raster (small membership) algorithm transforms an input raster to a fuzzified raster and thereby assigns values between 0 and 1 following the 'small' fuzzy membership function. The value of 0 implies no membership with the defined fuzzy set, a value of 1 depicts full membership. In between, the degree of membership of raster values follows the 'small' membership function.
The 'small' function is constructed using two user-defined input raster values which set the point of half membership (midpoint, results to 0.5) and a predefined function spread which controls the function uptake.
This function is typically used when smaller input raster values should become members of the fuzzy set more easily than higher values.
Parameters:
- INPUT [raster]: Input Raster
- BAND [band]: Band Number (default 1)
- FUZZYMIDPOINT [number]: Function midpoint (default 50)
- FUZZYSPREAD [number]: Function spread (default 5)
- CREATE_OPTIONS [string]: Creation options (optional)
- CREATION_OPTIONS [string]: Creation options (optional)
- OUTPUT [rasterDestination]: Fuzzified raster
Outputs: EXTENT [outputString], CRS_AUTHID [outputString], WIDTH_IN_PIXELS [outputNumber], HEIGHT_IN_PIXELS [outputNumber], TOTAL_PIXEL_COUNT [outputNumber], OUTPUT [outputRaster]

### native:greaterthanfrequency: Greater than frequency
This algorithm evaluates on a cell-by-cell basis the frequency (number of times) the values of an input stack of rasters are greater than the value of a value raster. 
 If multiband rasters are used in the data raster stack, the algorithm will always perform the analysis on the first band of the rasters - use GDAL to use other bands in the analysis. The input value layer serves as reference layer for the sample layers. Any NoData cells in the value raster or the data layer stack will result in a NoData cell in the output raster if the ignore NoData parameter is not checked. The output NoData value can be set manually. The output rasters extent and resolution is defined by the input raster layer and is always of int32 type.
Parameters:
- INPUT_VALUE_RASTER [raster]: Input value raster
- INPUT_VALUE_RASTER_BAND [band]: Value raster band (default 1)
- INPUT_RASTERS [multilayer]: Input raster layers
- IGNORE_NODATA [boolean]: Ignore NoData values (default False)
- OUTPUT_NODATA_VALUE [number]: Output NoData value (optional; default -9999)
- CREATE_OPTIONS [string]: Creation options (optional)
- CREATION_OPTIONS [string]: Creation options (optional)
- OUTPUT [rasterDestination]: Output layer
Outputs: OUTPUT [outputRaster], OCCURRENCE_COUNT [outputNumber], FOUND_LOCATIONS_COUNT [outputNumber], MEAN_FREQUENCY_PER_LOCATION [outputNumber], EXTENT [outputString], CRS_AUTHID [outputString], WIDTH_IN_PIXELS [outputNumber], HEIGHT_IN_PIXELS [outputNumber], TOTAL_PIXEL_COUNT [outputNumber]

### native:highestpositioninrasterstack: Highest position in raster stack
This algorithm evaluates on a cell-by-cell basis the position of the raster with the highest value in a stack of rasters. Position counts start with 1 and range to the total number of input rasters. The order of the input rasters is relevant for the algorithm. If multiple rasters feature the highest value, the first raster will be used for the position value.
 If multiband rasters are used in the data raster stack, the algorithm will always perform the analysis on the first band of the rasters - use GDAL to use other bands in the analysis. Any NoData cells in the raster layer stack will result in a NoData cell in the output raster unless the "ignore NoData" parameter is checked. The output NoData value can be set manually. The output rasters extent and resolution is defined by a reference raster layer and is always of int32 type.
Parameters:
- INPUT_RASTERS [multilayer]: Input raster layers
- REFERENCE_LAYER [raster]: Reference layer
- IGNORE_NODATA [boolean]: Ignore NoData values (default False)
- OUTPUT_NODATA_VALUE [number]: Output NoData value (optional; default -9999)
- CREATE_OPTIONS [string]: Creation options (optional)
- CREATION_OPTIONS [string]: Creation options (optional)
- OUTPUT [rasterDestination]: Output layer
Outputs: OUTPUT [outputRaster], EXTENT [outputString], CRS_AUTHID [outputString], WIDTH_IN_PIXELS [outputNumber], HEIGHT_IN_PIXELS [outputNumber], TOTAL_PIXEL_COUNT [outputNumber]

### native:lessthanfrequency: Less than frequency
This algorithm evaluates on a cell-by-cell basis the frequency (number of times) the values of an input stack of rasters are less than the value of a value raster. 
 If multiband rasters are used in the data raster stack, the algorithm will always perform the analysis on the first band of the rasters - use GDAL to use other bands in the analysis. The input value layer serves as reference layer for the sample layers. Any NoData cells in the value raster or the data layer stack will result in a NoData cell in the output raster if the ignore NoData parameter is not checked. The output NoData value can be set manually. The output rasters extent and resolution is defined by the input raster layer and is always of int32 type.
Parameters:
- INPUT_VALUE_RASTER [raster]: Input value raster
- INPUT_VALUE_RASTER_BAND [band]: Value raster band (default 1)
- INPUT_RASTERS [multilayer]: Input raster layers
- IGNORE_NODATA [boolean]: Ignore NoData values (default False)
- OUTPUT_NODATA_VALUE [number]: Output NoData value (optional; default -9999)
- CREATE_OPTIONS [string]: Creation options (optional)
- CREATION_OPTIONS [string]: Creation options (optional)
- OUTPUT [rasterDestination]: Output layer
Outputs: OUTPUT [outputRaster], OCCURRENCE_COUNT [outputNumber], FOUND_LOCATIONS_COUNT [outputNumber], MEAN_FREQUENCY_PER_LOCATION [outputNumber], EXTENT [outputString], CRS_AUTHID [outputString], WIDTH_IN_PIXELS [outputNumber], HEIGHT_IN_PIXELS [outputNumber], TOTAL_PIXEL_COUNT [outputNumber]

### native:lowestpositioninrasterstack: Lowest position in raster stack
This algorithm evaluates on a cell-by-cell basis the position of the raster with the lowest value in a stack of rasters. Position counts start with 1 and range to the total number of input rasters. The order of the input rasters is relevant for the algorithm. If multiple rasters feature the lowest value, the first raster will be used for the position value.
 If multiband rasters are used in the data raster stack, the algorithm will always perform the analysis on the first band of the rasters - use GDAL to use other bands in the analysis. Any NoData cells in the raster layer stack will result in a NoData cell in the output raster unless the "ignore NoData" parameter is checked. The output NoData value can be set manually. The output rasters extent and resolution is defined by a reference raster layer and is always of int32 type.
Parameters:
- INPUT_RASTERS [multilayer]: Input raster layers
- REFERENCE_LAYER [raster]: Reference layer
- IGNORE_NODATA [boolean]: Ignore NoData values (default False)
- OUTPUT_NODATA_VALUE [number]: Output NoData value (optional; default -9999)
- CREATE_OPTIONS [string]: Creation options (optional)
- CREATION_OPTIONS [string]: Creation options (optional)
- OUTPUT [rasterDestination]: Output layer
Outputs: OUTPUT [outputRaster], EXTENT [outputString], CRS_AUTHID [outputString], WIDTH_IN_PIXELS [outputNumber], HEIGHT_IN_PIXELS [outputNumber], TOTAL_PIXEL_COUNT [outputNumber]

### native:modelerrastercalc: Raster calculator
This algorithm performs algebraic operations using raster layers.
Parameters:
- LAYERS [multilayer]: Input layers
- EXPRESSION [expression]: Expression
- EXTENT [extent]: Output extent (optional)
- CELL_SIZE [number]: Output cell size (leave empty to set automatically) (optional)
- CRS [crs]: Output CRS (optional)
- CREATION_OPTIONS [string]: Creation options (optional)
- OUTPUT [rasterDestination]: Calculated
Outputs: OUTPUT [outputRaster]

### native:modelervirtualrastercalc: Raster calculator (virtual)
This algorithm performs algebraic operations using raster layers and generates in-memory result.
Parameters:
- LAYERS [multilayer]: Input layers
- EXPRESSION [expression]: Expression
- EXTENT [extent]: Output extent (optional)
- CELL_SIZE [number]: Output cell size (leave empty to set automatically) (optional)
- CRS [crs]: Output CRS (optional)
- LAYER_NAME [string]: Output layer name (optional)
Outputs: OUTPUT [outputRaster]

### native:rasterbooleanand: Raster boolean AND
This algorithm calculates the boolean AND for a set of input rasters. If all of the input rasters have a non-zero value for a pixel, that pixel will be set to 1 in the output raster. If any of the input rasters have 0 values for the pixel it will be set to 0 in the output raster.
The reference layer parameter specifies an existing raster layer to use as a reference when creating the output raster. The output raster will have the same extent, CRS, and pixel dimensions as this layer.
By default, a NoData pixel in ANY of the input layers will result in a NoData pixel in the output raster. If the 'Treat NoData values as false' option is checked, then NoData inputs will be treated the same as a 0 input value.
Parameters:
- INPUT [multilayer]: Input layers
- REF_LAYER [raster]: Reference layer
- NODATA_AS_FALSE [boolean]: Treat NoData values as false (default False)
- NO_DATA [number]: Output NoData value (default -9999)
- DATA_TYPE [enum]: Output data type (default 5; options 0=Byte, 1=Int16, 2=UInt16, 3=Int32, 4=UInt32, 5=Float32, 6=Float64, 7=CInt16, 8=CInt32, 9=CFloat32, 10=CFloat64, 11=Int8)
- CREATE_OPTIONS [string]: Creation options (optional)
- CREATION_OPTIONS [string]: Creation options (optional)
- OUTPUT [rasterDestination]: Output layer
Outputs: OUTPUT [outputRaster], EXTENT [outputString], CRS_AUTHID [outputString], WIDTH_IN_PIXELS [outputNumber], HEIGHT_IN_PIXELS [outputNumber], TOTAL_PIXEL_COUNT [outputNumber], NODATA_PIXEL_COUNT [outputNumber], TRUE_PIXEL_COUNT [outputNumber], FALSE_PIXEL_COUNT [outputNumber]

### native:rastercalc: Raster calculator
This algorithm performs algebraic operations using raster layers.
Parameters:
- LAYERS [multilayer]: Input layers
- EXPRESSION [expression]: Expression
- EXTENT [extent]: Output extent (optional)
- CELL_SIZE [number]: Output cell size (leave empty to set automatically) (optional)
- CRS [crs]: Output CRS (optional)
- CREATION_OPTIONS [string]: Creation options (optional)
- OUTPUT [rasterDestination]: Calculated
Outputs: OUTPUT [outputRaster]

### native:rasterlayerproperties: Raster layer properties
This algorithm returns basic properties of the given raster layer, including the extent, size in pixels and dimensions of pixels (in map units).
If an optional band number is specified then the NoData value for the selected band will also be returned.
Parameters:
- INPUT [raster]: Input layer
- BAND [band]: Band number (optional)
Outputs: X_MIN [outputNumber], X_MAX [outputNumber], Y_MIN [outputNumber], Y_MAX [outputNumber], EXTENT [outputString], PIXEL_WIDTH [outputNumber], PIXEL_HEIGHT [outputNumber], CRS_AUTHID [outputString], WIDTH_IN_PIXELS [outputNumber], HEIGHT_IN_PIXELS [outputNumber], HAS_NODATA_VALUE [outputBoolean], NODATA_VALUE [outputNumber], BAND_COUNT [outputNumber]

### native:rasterlayerstatistics: Raster layer statistics
This algorithm computes basic statistics from the values in a given band of the raster layer.
Parameters:
- INPUT [raster]: Input layer
- BAND [band]: Band number (default 1)
- OUTPUT_HTML_FILE [fileDestination]: Statistics (optional)
Outputs: OUTPUT_HTML_FILE [outputHtml], COUNT [outputNumber], MIN [outputNumber], MAX [outputNumber], RANGE [outputNumber], SUM [outputNumber], MEAN [outputNumber], STD_DEV [outputNumber], SUM_OF_SQUARES [outputNumber]

### native:rasterlayeruniquevaluesreport: Raster layer unique values report
This algorithm returns the count and area of each unique value in a given raster layer. The area calculation is done in the area unit of the layer's CRS.
Parameters:
- INPUT [raster]: Input layer
- BAND [band]: Band number (default 1)
- OUTPUT_HTML_FILE [fileDestination]: Unique values report (optional)
- OUTPUT_TABLE [sink]: Unique values table (optional)
Outputs: OUTPUT_HTML_FILE [outputHtml], OUTPUT_TABLE [outputVector], EXTENT [outputString], CRS_AUTHID [outputString], WIDTH_IN_PIXELS [outputNumber], HEIGHT_IN_PIXELS [outputNumber], TOTAL_PIXEL_COUNT [outputNumber], NODATA_PIXEL_COUNT [outputNumber]

### native:rasterlayerzonalstats: Raster layer zonal statistics
This algorithm calculates statistics for a raster layer's values, categorized by zones defined in another raster layer.
If the reference layer parameter is set to "Input layer", then zones are determined by sampling the zone raster layer value at the centroid of each pixel from the source raster layer.
If the reference layer parameter is set to "Zones layer", then the input raster layer will be sampled at the centroid of each pixel from the zones raster layer.
If either the source raster layer or the zone raster layer value is NoData for a pixel, that pixel's value will be skipped and not included in the calculated statistics.
Parameters:
- INPUT [raster]: Input layer
- BAND [band]: Band number (default 1)
- ZONES [raster]: Zones layer
- ZONES_BAND [band]: Zones band number (default 1)
- REF_LAYER [enum]: Reference layer (default 0; options 0=Input layer, 1=Zones layer)
- OUTPUT_TABLE [sink]: Statistics
Outputs: OUTPUT_TABLE [outputVector], EXTENT [outputString], CRS_AUTHID [outputString], WIDTH_IN_PIXELS [outputNumber], HEIGHT_IN_PIXELS [outputNumber], TOTAL_PIXEL_COUNT [outputNumber], NODATA_PIXEL_COUNT [outputNumber]

### native:rasterlogicalor: Raster boolean OR
This algorithm calculates the boolean OR for a set of input rasters. If any of the input rasters have a non-zero value for a pixel, that pixel will be set to 1 in the output raster. If all the input rasters have 0 values for the pixel it will be set to 0 in the output raster.
The reference layer parameter specifies an existing raster layer to use as a reference when creating the output raster. The output raster will have the same extent, CRS, and pixel dimensions as this layer.
By default, a NoData pixel in ANY of the input layers will result in a NoData pixel in the output raster. If the 'Treat NoData values as false' option is checked, then NoData inputs will be treated the same as a 0 input value.
Parameters:
- INPUT [multilayer]: Input layers
- REF_LAYER [raster]: Reference layer
- NODATA_AS_FALSE [boolean]: Treat NoData values as false (default False)
- NO_DATA [number]: Output NoData value (default -9999)
- DATA_TYPE [enum]: Output data type (default 5; options 0=Byte, 1=Int16, 2=UInt16, 3=Int32, 4=UInt32, 5=Float32, 6=Float64, 7=CInt16, 8=CInt32, 9=CFloat32, 10=CFloat64, 11=Int8)
- CREATE_OPTIONS [string]: Creation options (optional)
- CREATION_OPTIONS [string]: Creation options (optional)
- OUTPUT [rasterDestination]: Output layer
Outputs: OUTPUT [outputRaster], EXTENT [outputString], CRS_AUTHID [outputString], WIDTH_IN_PIXELS [outputNumber], HEIGHT_IN_PIXELS [outputNumber], TOTAL_PIXEL_COUNT [outputNumber], NODATA_PIXEL_COUNT [outputNumber], TRUE_PIXEL_COUNT [outputNumber], FALSE_PIXEL_COUNT [outputNumber]

### native:rasterminmax: Raster minimum/maximum
This algorithm extracts extrema (minimum and maximum) values from a given band of the raster layer.
The output is a vector layer containing point features for the selected extrema, at the center of the associated pixel.
If multiple pixels in the raster share the minimum or maximum value, then only one of these pixels will be included in the output.
Parameters:
- INPUT [raster]: Input layer
- BAND [band]: Band number (default 1)
- EXTRACT [enum]: Extract extrema (default 0; options 0=Minimum and Maximum, 1=Minimum, 2=Maximum)
- OUTPUT [sink]: Output (optional)
Outputs: OUTPUT [outputVector], MINIMUM [outputNumber], MAXIMUM [outputNumber]

### native:rasterrank: Raster rank
This algorithm performs a cell-by-cell analysis in which output values match the rank of a sorted list of overlapping cell values from input layers. The output raster will be multi-band if multiple ranks are provided.
If multiband rasters are used in the data raster stack, the algorithm will always perform the analysis on the first band of the rasters.
Parameters:
- INPUT_RASTERS [multilayer]: Input raster layers
- RANKS [string]: Rank(s) (separate multiple ranks using commas) (default 1)
- NODATA_HANDLING [enum]: NoData value handling (default 0; options 0=Exclude NoData from values lists, 1=Presence of NoData in a values list results in NoData output cell)
- EXTENT [extent]: Output extent (optional)
- CELL_SIZE [number]: Output cell size (optional)
- CRS [crs]: Output CRS (optional)
- OUTPUT [rasterDestination]: Ranked
Outputs: OUTPUT [outputRaster]

### native:rastersampling: Sample raster values
This algorithm creates a new vector layer with the same attributes of the input layer and the raster values corresponding on the point location.
If the raster layer has more than one band, all the band values are sampled.
Parameters:
- INPUT [source]: Input layer
- RASTERCOPY [raster]: Raster layer
- COLUMN_PREFIX [string]: Output column prefix (optional; default SAMPLE_)
- OUTPUT [sink]: Sampled
Outputs: OUTPUT [outputVector]

### native:rastersurfacevolume: Raster surface volume
This algorithm calculates the volume under a raster grid's surface.
Several methods of volume calculation are available, which control whether only values above or below the specified base level are considered, or whether volumes below the base level should be added or subtracted from the total volume.
The algorithm outputs the calculated volume, the total area, and the total number of pixels analysed. If the 'Count Only Above Base Level' or 'Count Only Below Base Level' methods are used, then the calculated area and pixel count only includes pixels which are above or below the specified base level respectively.
Units of the calculated volume are dependent on the coordinate reference system of the input raster file. For a CRS in meters, with a DEM height in meters, the calculated value will be in meters³. If instead the input raster is in a geographic coordinate system (e.g. latitude/longitude values), then the result will be in degrees² × meters, and an appropriate scaling factor will need to be applied in order to convert to meters³.
Parameters:
- INPUT [raster]: Input layer
- BAND [band]: Band number (default 1)
- LEVEL [number]: Base level (default 0)
- METHOD [enum]: Method (options 0=Count Only Above Base Level, 1=Count Only Below Base Level, 2=Subtract Volumes Below Base Level, 3=Add Volumes Below Base Level)
- OUTPUT_HTML_FILE [fileDestination]: Surface volume report (optional)
- OUTPUT_TABLE [sink]: Surface volume table (optional)
Outputs: OUTPUT_HTML_FILE [outputHtml], OUTPUT_TABLE [outputVector], VOLUME [outputNumber], PIXEL_COUNT [outputNumber], AREA [outputNumber]

### native:reclassifybylayer: Reclassify by layer
This algorithm reclassifies a raster band by assigning new class values based on the ranges specified in a vector table.
Parameters:
- INPUT_RASTER [raster]: Raster layer
- RASTER_BAND [band]: Band number (default 1)
- INPUT_TABLE [source]: Layer containing class breaks
- MIN_FIELD [field]: Minimum class value field
- MAX_FIELD [field]: Maximum class value field
- VALUE_FIELD [field]: Output value field
- NO_DATA [number]: Output NoData value (default -9999)
- RANGE_BOUNDARIES [enum]: Range boundaries (default 0; options 0=min < value <= max, 1=min <= value < max, 2=min <= value <= max, 3=min < value < max)
- NODATA_FOR_MISSING [boolean]: Use NoData when no range matches value (default False)
- DATA_TYPE [enum]: Output data type (default 5; options 0=Byte, 1=Int16, 2=UInt16, 3=Int32, 4=UInt32, 5=Float32, 6=Float64, 7=CInt16, 8=CInt32, 9=CFloat32, 10=CFloat64, 11=Int8)
- CREATE_OPTIONS [string]: Creation options (optional)
- CREATION_OPTIONS [string]: Creation options (optional)
- OUTPUT [rasterDestination]: Reclassified raster
Outputs: OUTPUT [outputRaster]

### native:reclassifybytable: Reclassify by table
This algorithm reclassifies a raster band by assigning new class values based on the ranges specified in a fixed table.
Parameters:
- INPUT_RASTER [raster]: Raster layer
- RASTER_BAND [band]: Band number (default 1)
- TABLE [matrix]: Reclassification table
- NO_DATA [number]: Output NoData value (default -9999)
- RANGE_BOUNDARIES [enum]: Range boundaries (default 0; options 0=min < value <= max, 1=min <= value < max, 2=min <= value <= max, 3=min < value < max)
- NODATA_FOR_MISSING [boolean]: Use NoData when no range matches value (default False)
- DATA_TYPE [enum]: Output data type (default 5; options 0=Byte, 1=Int16, 2=UInt16, 3=Int32, 4=UInt32, 5=Float32, 6=Float64, 7=CInt16, 8=CInt32, 9=CFloat32, 10=CFloat64, 11=Int8)
- CREATE_OPTIONS [string]: Creation options (optional)
- CREATION_OPTIONS [string]: Creation options (optional)
- OUTPUT [rasterDestination]: Reclassified raster
Outputs: OUTPUT [outputRaster]

### native:rescaleraster: Rescale raster
This algorithm rescales a raster layer to a new value range, while preserving the shape (distribution) of the raster's histogram (pixel values). Input values are mapped using a linear interpolation from the source raster's minimum and maximum pixel values to the destination minimum and maximum pixel range.
By default the algorithm preserves the original NoData value, but there is an option to override it.
Parameters:
- INPUT [raster]: Input raster
- BAND [band]: Band number (default 1)
- MINIMUM [number]: New minimum value (default 0)
- MAXIMUM [number]: New maximum value (default 255)
- NODATA [number]: New NoData value (optional)
- CREATE_OPTIONS [string]: Creation options (optional)
- CREATION_OPTIONS [string]: Creation options (optional)
- OUTPUT [rasterDestination]: Rescaled
Outputs: OUTPUT [outputRaster]

### native:roundrastervalues: Round raster
This algorithm rounds the cell values of a raster dataset to the specified number of decimals.
 Alternatively, a negative number of decimal places may be used to round values to powers of a base n (specified in the advanced parameter Base n). For example, with a Base value n of 10 and Decimal places of -1 the algorithm rounds cell values to multiples of 10, -2 rounds to multiples of 100, and so on. Arbitrary base values may be chosen, the algorithm applies the same multiplicative principle. Rounding cell values to multiples of a base n may be used to generalize raster layers.
The algorithm preserves the data type of the input raster. Therefore byte/integer rasters can only be rounded to multiples of a base n, otherwise a warning is raised and the raster gets copied as byte/integer raster.
Parameters:
- INPUT [raster]: Input raster
- BAND [band]: Band number (default 1)
- ROUNDING_DIRECTION [enum]: Rounding direction (default 1; options 0=Round up, 1=Round to nearest, 2=Round down)
- DECIMAL_PLACES [number]: Number of decimals places (default 2)
- BASE_N [number]: Base n for rounding to multiples of n (default 10)
- CREATE_OPTIONS [string]: Creation options (optional)
- CREATION_OPTIONS [string]: Creation options (optional)
- OUTPUT [rasterDestination]: Output raster
Outputs: OUTPUT [outputRaster]

### native:virtualrastercalc: Raster calculator (virtual)
This algorithm performs algebraic operations using raster layers and generates in-memory result.
Parameters:
- LAYERS [multilayer]: Input layers
- EXPRESSION [expression]: Expression
- EXTENT [extent]: Output extent (optional)
- CELL_SIZE [number]: Output cell size (leave empty to set automatically) (optional)
- CRS [crs]: Output CRS (optional)
- LAYER_NAME [string]: Output layer name (optional)
Outputs: OUTPUT [outputRaster]

### native:zonalhistogram: Zonal histogram
This algorithm appends fields representing counts of each unique value from a raster layer contained within zones defined as polygons.
Parameters:
- INPUT_RASTER [raster]: Raster layer
- RASTER_BAND [band]: Band number (default 1)
- INPUT_VECTOR [source]: Vector layer containing zones
- COLUMN_PREFIX [string]: Output column prefix (optional; default HISTO_)
- OUTPUT [sink]: Output zones
Outputs: OUTPUT [outputVector]

### native:zonalminmaxpoint: Zonal minimum/maximum point
This algorithm extracts point features corresponding to the minimum and maximum pixel values contained within polygon zones.
The output will contain one point feature for the minimum and one for the maximum raster value for every individual zonal feature from a polygon layer.
The created point layer will be in the same spatial reference system as the selected raster layer.
Parameters:
- INPUT [source]: Input layer
- INPUT_RASTER [raster]: Raster layer
- RASTER_BAND [band]: Raster band (default 1)
- OUTPUT [sink]: Zonal Extrema
Outputs: OUTPUT [outputVector]

### native:zonalstatistics: Zonal statistics (in place)
This algorithm calculates statistics of a raster layer for each feature of an overlapping polygon vector layer. The results will be written in place.
Parameters:
- INPUT_RASTER [raster]: Raster layer
- RASTER_BAND [band]: Raster band (default 1)
- INPUT_VECTOR [vector]: Vector layer containing zones
- COLUMN_PREFIX [string]: Output column prefix (default _)
- STATISTICS [enum]: Statistics to calculate (default [0, 1, 2]; options 0=Count, 1=Sum, 2=Mean, 3=Median, 4=St dev, 5=Minimum, 6=Maximum, 7=Range, 8=Minority, 9=Majority, 10=Variety, 11=Variance)
Outputs: INPUT_VECTOR [outputVector]

### native:zonalstatisticsfb: Zonal statistics
This algorithm calculates statistics of a raster layer for each feature of an overlapping polygon vector layer.
Parameters:
- INPUT [source]: Input layer
- INPUT_RASTER [raster]: Raster layer
- RASTER_BAND [band]: Raster band (default 1)
- COLUMN_PREFIX [string]: Output column prefix (default _)
- STATISTICS [enum]: Statistics to calculate (default [0, 1, 2]; options 0=Count, 1=Sum, 2=Mean, 3=Median, 4=St dev, 5=Minimum, 6=Maximum, 7=Range, 8=Minority, 9=Majority, 10=Variety, 11=Variance)
- OUTPUT [sink]: Zonal Statistics
Outputs: OUTPUT [outputVector]


## QGIS (native c++) / Raster creation

### native:createconstantrasterlayer: Create constant raster layer
This algorithm generates a raster layer for a given extent and cell size filled with a single constant value.
Additionally an output data type can be specified. The algorithm will abort if a value has been entered that cannot be represented by the selected output raster data type.
Parameters:
- EXTENT [extent]: Desired extent
- TARGET_CRS [crs]: Target CRS (default ProjectCrs)
- PIXEL_SIZE [number]: Pixel size (default 1)
- NUMBER [number]: Constant value (default 1)
- OUTPUT_TYPE [enum]: Output raster data type (default 5; options 0=Byte, 1=Integer16, 2=Unsigned Integer16, 3=Integer32, 4=Unsigned Integer32, 5=Float32, 6=Float64)
- CREATE_OPTIONS [string]: Creation options (optional)
- CREATION_OPTIONS [string]: Creation options (optional)
- OUTPUT [rasterDestination]: Constant
Outputs: OUTPUT [outputRaster]

### native:createrandombinomialrasterlayer: Create random raster layer (binomial distribution)
This algorithm generates a raster layer for a given extent and cell size filled with binomially distributed random values.
By default, the values will be chosen given an N of 10 and a probability of 0.5. This can be overridden by using the advanced parameter for N and probability. The raster data type is set to Integer types (Integer16 by default). The binomial distribution random values are defined as positive integer numbers. A floating point raster will represent a cast of integer values to floating point.
Parameters:
- EXTENT [extent]: Desired extent
- TARGET_CRS [crs]: Target CRS (default ProjectCrs)
- PIXEL_SIZE [number]: Pixel size (default 1)
- OUTPUT_TYPE [enum]: Output raster data type (default 0; options 0=Integer16, 1=Unsigned Integer16, 2=Integer32, 3=Unsigned Integer32, 4=Float32, 5=Float64)
- N [number]: N (default 10)
- PROBABILITY [number]: Probability (default 0.5)
- CREATE_OPTIONS [string]: Creation options (optional)
- CREATION_OPTIONS [string]: Creation options (optional)
- OUTPUT [rasterDestination]: Output raster
Outputs: OUTPUT [outputRaster]

### native:createrandomexponentialrasterlayer: Create random raster layer (exponential distribution)
This algorithm generates a raster layer for a given extent and cell size filled with exponentially distributed random values.
By default, the values will be chosen given a lambda of 1.0. This can be overridden by using the advanced parameter for lambda. The raster data type is set to Float32 by default as the exponential distribution random values are floating point numbers.
Parameters:
- EXTENT [extent]: Desired extent
- TARGET_CRS [crs]: Target CRS (default ProjectCrs)
- PIXEL_SIZE [number]: Pixel size (default 1)
- OUTPUT_TYPE [enum]: Output raster data type (default 0; options 0=Float32, 1=Float64)
- LAMBDA [number]: Lambda (default 1.0)
- CREATE_OPTIONS [string]: Creation options (optional)
- CREATION_OPTIONS [string]: Creation options (optional)
- OUTPUT [rasterDestination]: Output raster
Outputs: OUTPUT [outputRaster]

### native:createrandomgammarasterlayer: Create random raster layer (gamma distribution)
This algorithm generates a raster layer for a given extent and cell size filled with gamma distributed random values.
By default, the values will be chosen given an alpha and beta value of 1.0. This can be overridden by using the advanced parameter for alpha and beta. The raster data type is set to Float32 by default as the gamma distribution random values are floating point numbers.
Parameters:
- EXTENT [extent]: Desired extent
- TARGET_CRS [crs]: Target CRS (default ProjectCrs)
- PIXEL_SIZE [number]: Pixel size (default 1)
- OUTPUT_TYPE [enum]: Output raster data type (default 0; options 0=Float32, 1=Float64)
- ALPHA [number]: Alpha (default 1.0)
- BETA [number]: Beta (default 1.0)
- CREATE_OPTIONS [string]: Creation options (optional)
- CREATION_OPTIONS [string]: Creation options (optional)
- OUTPUT [rasterDestination]: Output raster
Outputs: OUTPUT [outputRaster]

### native:createrandomgeometricrasterlayer: Create random raster layer (geometric distribution)
This algorithm generates a raster layer for a given extent and cell size filled with geometrically distributed random values.
By default, the values will be chosen given a probability of 0.5. This can be overridden by using the advanced parameter for mean value. The raster data type is set to Integer types (Integer16 by default). The geometric distribution random values are defined as positive integer numbers. A floating point raster will represent a cast of integer values to floating point.
Parameters:
- EXTENT [extent]: Desired extent
- TARGET_CRS [crs]: Target CRS (default ProjectCrs)
- PIXEL_SIZE [number]: Pixel size (default 1)
- OUTPUT_TYPE [enum]: Output raster data type (default 0; options 0=Integer16, 1=Unsigned Integer16, 2=Integer32, 3=Unsigned Integer32, 4=Float32, 5=Float64)
- PROBABILITY [number]: Probability (default 0.5)
- CREATE_OPTIONS [string]: Creation options (optional)
- CREATION_OPTIONS [string]: Creation options (optional)
- OUTPUT [rasterDestination]: Output raster
Outputs: OUTPUT [outputRaster]

### native:createrandomnegativebinomialrasterlayer: Create random raster layer (negative binomial distribution)
This algorithm generates a raster layer for a given extent and cell size filled with negative binomially distributed random values.
By default, the values will be chosen given a distribution parameter k of 10.0 and a probability of 0.5. This can be overridden by using the advanced parameters for k and probability. The raster data type is set to Integer types (Integer 16 by default). The negative binomial distribution random values are defined as positive integer numbers. A floating point raster will represent a cast of integer values to floating point.
Parameters:
- EXTENT [extent]: Desired extent
- TARGET_CRS [crs]: Target CRS (default ProjectCrs)
- PIXEL_SIZE [number]: Pixel size (default 1)
- OUTPUT_TYPE [enum]: Output raster data type (default 0; options 0=Integer16, 1=Unsigned Integer16, 2=Integer32, 3=Unsigned Integer32, 4=Float32, 5=Float64)
- K_PARAMETER [number]: Distribution parameter k (default 10)
- PROBABILITY [number]: Probability (default 0.5)
- CREATE_OPTIONS [string]: Creation options (optional)
- CREATION_OPTIONS [string]: Creation options (optional)
- OUTPUT [rasterDestination]: Output raster
Outputs: OUTPUT [outputRaster]

### native:createrandomnormalrasterlayer: Create random raster layer (normal distribution)
This algorithm generates a raster layer for a given extent and cell size filled with normally distributed random values.
By default, the values will be chosen given a mean of 0.0 and a standard deviation of 1.0. This can be overridden by using the advanced parameters for mean and standard deviation value. The raster data type is set to Float32 by default as the normal distribution random values are floating point numbers.
Parameters:
- EXTENT [extent]: Desired extent
- TARGET_CRS [crs]: Target CRS (default ProjectCrs)
- PIXEL_SIZE [number]: Pixel size (default 1)
- OUTPUT_TYPE [enum]: Output raster data type (default 0; options 0=Float32, 1=Float64)
- MEAN [number]: Mean of normal distribution (default 0)
- STDDEV [number]: Standard deviation of normal distribution (default 1)
- CREATE_OPTIONS [string]: Creation options (optional)
- CREATION_OPTIONS [string]: Creation options (optional)
- OUTPUT [rasterDestination]: Output raster
Outputs: OUTPUT [outputRaster]

### native:createrandompoissonrasterlayer: Create random raster layer (poisson distribution)
This algorithm generates a raster layer for a given extent and cell size filled with poisson distributed random values.
By default, the values will be chosen given a mean of 1.0. This can be overridden by using the advanced parameter for mean value. The raster data type is set to Integer types (Integer16 by default). The poisson distribution random values are positive integer numbers. A floating point raster will represent a cast of integer values to floating point.
Parameters:
- EXTENT [extent]: Desired extent
- TARGET_CRS [crs]: Target CRS (default ProjectCrs)
- PIXEL_SIZE [number]: Pixel size (default 1)
- OUTPUT_TYPE [enum]: Output raster data type (default 0; options 0=Integer16, 1=Unsigned Integer16, 2=Integer32, 3=Unsigned Integer32, 4=Float32, 5=Float64)
- MEAN [number]: Mean (default 1.0)
- CREATE_OPTIONS [string]: Creation options (optional)
- CREATION_OPTIONS [string]: Creation options (optional)
- OUTPUT [rasterDestination]: Output raster
Outputs: OUTPUT [outputRaster]

### native:createrandomuniformrasterlayer: Create random raster layer (uniform distribution)
This algorithm generates a raster layer for a given extent and cell size filled with random values.
By default, the values will range between the minimum and maximum value of the specified output raster type. This can be overridden by using the advanced parameters for lower and upper bound value. If the bounds have the same value or both are zero (default) the algorithm will create random values in the full value range of the chosen raster data type. Choosing bounds outside the acceptable range of the output raster type will abort the algorithm.
Parameters:
- EXTENT [extent]: Desired extent
- TARGET_CRS [crs]: Target CRS (default ProjectCrs)
- PIXEL_SIZE [number]: Pixel size (default 1)
- OUTPUT_TYPE [enum]: Output raster data type (default 5; options 0=Byte, 1=Integer16, 2=Unsigned Integer16, 3=Integer32, 4=Unsigned Integer32, 5=Float32, 6=Float64)
- LOWER_BOUND [number]: Lower bound for random number range
- UPPER_BOUND [number]: Upper bound for random number range
- CREATE_OPTIONS [string]: Creation options (optional)
- CREATION_OPTIONS [string]: Creation options (optional)
- OUTPUT [rasterDestination]: Output raster
Outputs: OUTPUT [outputRaster]


## QGIS (native c++) / Raster terrain analysis

### native:aspect: Aspect
This algorithm calculates the aspect of the Digital Terrain Model in input.
The final aspect raster layer contains values from 0 to 360 that express the slope direction: starting from North (0°) and continuing clockwise.
Parameters:
- INPUT [raster]: Elevation layer
- Z_FACTOR [number]: Z factor (default 1)
- OUTPUT [rasterDestination]: Aspect
Outputs: OUTPUT [outputRaster]

### native:dtmslopebasedfilter: DTM filter (slope-based)
This algorithm can be used to filter a Digital Elevation Model in order to classify its cells into ground and object (non-ground) cells.
The tool uses concepts as described by Vosselman (2000) and is based on the assumption that a large height difference between two nearby cells is unlikely to be caused by a steep slope in the terrain. The probability that the higher cell might be non-ground increases when the distance between the two cells decreases. Therefore the filter defines a maximum height difference (dz_max) between two cells as a function of the distance (d) between the cells (dz_max( d ) = d).
A cell is classified as terrain if there is no cell within the kernel radius to which the height difference is larger than the allowed maximum height difference at the distance between these two cells.
The approximate terrain slope (s) parameter is used to modify the filter function to match the overall slope in the study area (dz_max( d ) = d * s).
A 5 % confidence interval (ci = 1.65 * sqrt( 2 * stddev )) may be used to modify the filter function even further by either relaxing (dz_max( d ) = d * s + ci) or amplifying (dz_max( d ) = d * s - ci) the filter criterium.
References: Vosselman, G. (2000): Slope based filtering of laser altimetry data. IAPRS, Vol. XXXIII, Part B3, Amsterdam, The Netherlands, 935-942
This algorithm is a port of the SAGA 'DTM Filter (slope-based)' tool.
Parameters:
- INPUT [raster]: Input layer
- BAND [band]: Band number (default 1)
- RADIUS [number]: Kernel radius (pixels) (default 5)
- TERRAIN_SLOPE [number]: Terrain slope (%, pixel size/vertical units) (default 30)
- FILTER_MODIFICATION [enum]: Filter modification (default 0; options 0=None, 1=Relax filter, 2=Amplify)
- STANDARD_DEVIATION [number]: Standard deviation (default 0.1)
- CREATE_OPTIONS [string]: Creation options (optional)
- CREATION_OPTIONS [string]: Creation options (optional)
- OUTPUT_GROUND [rasterDestination]: Output layer (ground) (optional)
- OUTPUT_NONGROUND [rasterDestination]: Output layer (non-ground objects) (optional)
Outputs: OUTPUT_GROUND [outputRaster], OUTPUT_NONGROUND [outputRaster]

### native:fillsinkswangliu: Fill sinks (Wang & Liu)
This algorithm uses a method proposed by Wang & Liu to identify and fill surface depressions in digital elevation models.
The method was enhanced to allow the creation of hydrologically sound elevation models, i.e. not only to fill the depression(s) but also to preserve a downward slope along the flow path. If desired, this is accomplished by preserving a minimum slope gradient (and thus elevation difference) between cells.
References: Wang, L. & H. Liu (2006): An efficient method for identifying and filling surface depressions in digital elevation models for hydrologic analysis and modelling. International Journal of Geographical Information Science, Vol. 20, No. 2: 193-213.
This algorithm is a port of the SAGA 'Fill Sinks (Wang & Liu)' tool.
Parameters:
- INPUT [raster]: Input layer
- BAND [band]: Band number (default 1)
- MIN_SLOPE [number]: Minimum slope (degrees) (default 0.1)
- CREATION_OPTIONS [string]: Creation options (optional)
- OUTPUT_FILLED_DEM [rasterDestination]: Output layer (filled DEM) (optional)
- OUTPUT_FLOW_DIRECTIONS [rasterDestination]: Output layer (flow directions) (optional)
- OUTPUT_WATERSHED_BASINS [rasterDestination]: Output layer (watershed basins) (optional)
Outputs: OUTPUT_FILLED_DEM [outputRaster], OUTPUT_FLOW_DIRECTIONS [outputRaster], OUTPUT_WATERSHED_BASINS [outputRaster]

### native:hillshade: Hillshade
This algorithm calculates the hillshade of the Digital Terrain Model in input.
The shading of the layer is calculated according to the sun position (azimuth and elevation).
Parameters:
- INPUT [raster]: Elevation layer
- Z_FACTOR [number]: Z factor (default 1)
- AZIMUTH [number]: Azimuth (horizontal angle) (default 300)
- V_ANGLE [number]: Vertical angle (default 40)
- OUTPUT [rasterDestination]: Hillshade
Outputs: OUTPUT [outputRaster]

### native:ruggednessindex: Ruggedness index
This algorithm calculates the quantitative measurement of terrain heterogeneity described by Riley et al. (1999).
It is calculated for every location, by summarizing the change in elevation within the 3x3 pixel grid. Each pixel contains the difference in elevation from a center cell and the 8 cells surrounding it.
Parameters:
- INPUT [raster]: Elevation layer
- Z_FACTOR [number]: Z factor (default 1)
- OUTPUT [rasterDestination]: Ruggedness
Outputs: OUTPUT [outputRaster]

### native:slope: Slope
This algorithm calculates the angle of inclination of the terrain from an input raster layer. The slope is expressed in degrees.
Parameters:
- INPUT [raster]: Elevation layer
- Z_FACTOR [number]: Z factor (default 1)
- OUTPUT [rasterDestination]: Slope
Outputs: OUTPUT [outputRaster]


## QGIS (native c++) / Raster tools

### native:alignrasters: Align rasters
This algorithm aligns rasters by resampling them to the same cell size and reprojecting to the same CRS.
Parameters:
- LAYERS [alignrasterlayers]: Input layers
- REFERENCE_LAYER [raster]: Reference layer
- CRS [crs]: Override reference CRS (optional)
- CELL_SIZE_X [number]: Override reference cell size X (optional)
- CELL_SIZE_Y [number]: Override reference cell size Y (optional)
- GRID_OFFSET_X [number]: Override reference grid offset X (optional)
- GRID_OFFSET_Y [number]: Override reference grid offset Y (optional)
- EXTENT [extent]: Clip to extent (optional)
Outputs: OUTPUT_LAYERS [outputMultilayer]

### native:alignsingleraster: Align raster
This algorithm aligns raster by resampling it to the same cell size and reprojecting to the same CRS as a reference raster.
Parameters:
- INPUT [raster]: Input layer
- RESAMPLING_METHOD [enum]: Resampling method (default 0; options 0=Nearest Neighbour, 1=Bilinear (2x2 Kernel), 2=Cubic (4x4 Kernel), 3=Cubic B-Spline (4x4 Kernel), 4=Lanczos (6x6 Kernel), 5=Average, 6=Mode, 7=Maximum, 8=Minimum, 9=Median, 10=First Quartile (Q1), 11=Third Quartile (Q3))
- RESCALE [boolean]: Rescale values according to the cell size (default False)
- REFERENCE_LAYER [raster]: Reference layer
- CRS [crs]: Override reference CRS (optional)
- CELL_SIZE_X [number]: Override reference cell size X (optional)
- CELL_SIZE_Y [number]: Override reference cell size Y (optional)
- GRID_OFFSET_X [number]: Override reference grid offset X (optional)
- GRID_OFFSET_Y [number]: Override reference grid offset Y (optional)
- EXTENT [extent]: Clip to extent (optional)
- OUTPUT [rasterDestination]: Aligned raster
Outputs: OUTPUT [outputRaster]

### native:fillnodata: Fill NoData cells
This algorithm resets the NoData values in the input raster to a chosen value, resulting in a raster dataset with no NoData pixels. This value can be set by the user using the Fill value parameter. The algorithm respects the input raster data type (eg. a floating point fill value will be truncated when applied to an integer raster).
Parameters:
- INPUT [raster]: Raster input
- BAND [band]: Band Number (default 1)
- FILL_VALUE [number]: Fill value (default 1)
- CREATE_OPTIONS [string]: Creation options (optional)
- CREATION_OPTIONS [string]: Creation options (optional)
- OUTPUT [rasterDestination]: Output raster
Outputs: OUTPUT [outputRaster]

### native:rasterize: Convert map to raster
This algorithm rasterizes map canvas content.
A map theme can be selected to render a predetermined set of layers with a defined style for each layer. Alternatively, a set of layers can be selected if no map theme is set. If neither map theme nor layer is set, all the visible layers in the set extent will be rendered.
The minimum extent entered will internally be extended to a multiple of the tile size.
Parameters:
- EXTENT [extent]: Minimum extent to render
- EXTENT_BUFFER [number]: Buffer around tiles in map units (optional; default 0)
- TILE_SIZE [number]: Tile size (default 1024)
- MAP_UNITS_PER_PIXEL [number]: Map units per pixel (optional; default 100)
- MAKE_BACKGROUND_TRANSPARENT [boolean]: Make background transparent (default False)
- MAP_THEME [maptheme]: Map theme to render (optional)
- LAYERS [multilayer]: Layers to render (optional)
- OUTPUT [rasterDestination]: Output layer
Outputs: OUTPUT [outputRaster]

### native:tilesxyzdirectory: Generate XYZ tiles (Directory)
Generates XYZ tiles of map canvas content and saves them as individual images in a directory.
Parameters:
- EXTENT [extent]: Extent
- ZOOM_MIN [number]: Minimum zoom (default 12)
- ZOOM_MAX [number]: Maximum zoom (default 12)
- DPI [number]: DPI (default 96)
- BACKGROUND_COLOR [color]: Background color (optional; default <QColor: RGBA 0, 0, 0, 0>)
- ANTIALIAS [boolean]: Enable antialiasing (default True)
- TILE_FORMAT [enum]: Tile format (default 0; options 0=PNG, 1=JPG)
- QUALITY [number]: Quality (JPG only) (default 75)
- METATILESIZE [number]: Metatile size (default 4)
- TILE_WIDTH [number]: Tile width (default 256)
- TILE_HEIGHT [number]: Tile height (default 256)
- TMS_CONVENTION [boolean]: Use inverted tile Y axis (TMS convention) (default False)
- HTML_TITLE [string]: Leaflet HTML output title (optional)
- HTML_ATTRIBUTION [string]: Leaflet HTML output attribution (optional)
- HTML_OSM [boolean]: Include OpenStreetMap basemap in Leaflet HTML output (default False)
- OUTPUT_DIRECTORY [folderDestination]: Output directory
- OUTPUT_HTML [fileDestination]: Output html (Leaflet) (optional)
Outputs: OUTPUT_DIRECTORY [outputFolder], OUTPUT_HTML [outputHtml]

### native:tilesxyzmbtiles: Generate XYZ tiles (MBTiles)
Generates XYZ tiles of map canvas content and saves them as an MBTiles file.
Parameters:
- EXTENT [extent]: Extent
- ZOOM_MIN [number]: Minimum zoom (default 12)
- ZOOM_MAX [number]: Maximum zoom (default 12)
- DPI [number]: DPI (default 96)
- BACKGROUND_COLOR [color]: Background color (optional; default <QColor: RGBA 0, 0, 0, 0>)
- ANTIALIAS [boolean]: Enable antialiasing (default True)
- TILE_FORMAT [enum]: Tile format (default 0; options 0=PNG, 1=JPG)
- QUALITY [number]: Quality (JPG only) (default 75)
- METATILESIZE [number]: Metatile size (default 4)
- OUTPUT_FILE [fileDestination]: Output
Outputs: OUTPUT_FILE [outputFile]


## QGIS (native c++) / Vector analysis

### native:basicstatisticsforfields: Basic statistics for fields
This algorithm generates basic statistics from the analysis of values in a field in the attribute table of a vector layer. Numeric, date, time and string fields are supported. The statistics returned will depend on the field type.
Parameters:
- INPUT_LAYER [source]: Input layer
- FIELD_NAME [field]: Field to calculate statistics on
- OUTPUT [sink]: Statistics (optional)
- OUTPUT_HTML_FILE [fileDestination]: Statistics report (optional)
Outputs: OUTPUT [outputVector], OUTPUT_HTML_FILE [outputHtml], COUNT [outputNumber], UNIQUE [outputNumber], EMPTY [outputNumber], FILLED [outputNumber], MIN [outputNumber], MAX [outputNumber], MIN_LENGTH [outputNumber], MAX_LENGTH [outputNumber], MEAN_LENGTH [outputNumber], CV [outputNumber], SUM [outputNumber], MEAN [outputNumber], STD_DEV [outputNumber], RANGE [outputNumber], MEDIAN [outputNumber], MINORITY [outputNumber], MAJORITY [outputNumber], FIRSTQUARTILE [outputNumber], THIRDQUARTILE [outputNumber], IQR [outputNumber]

### native:calculatevectoroverlaps: Overlap analysis
This algorithm calculates the area and percentage cover by which features from an input layer are overlapped by features from a selection of overlay layers.
New attributes are added to the output layer reporting the total area of overlap and percentage of the input feature overlapped by each of the selected overlay layers.
Parameters:
- INPUT [source]: Input layer
- LAYERS [multilayer]: Overlay layers
- OUTPUT [sink]: Overlap
- GRID_SIZE [number]: Grid size (optional)
Outputs: OUTPUT [outputVector]

### native:climbalongline: Climb along line
This algorithm calculates the total climb and descent along line geometries.
Input layer must have Z values present. If Z values are not available, the "Drape" (set Z value from raster) algorithm may be used to add Z values from a DEM layer.
The output layer is a copy of the input layer with additional fields that contain the total climb, total descent, the minimum elevation and the maximum elevation for each line geometry.If the input layer contains fields with the same names as these added fields, they will be renamed (field names will be altered to "name_2", "name_3", etc, finding the first non-duplicate name).
Parameters:
- INPUT [source]: Line layer
- OUTPUT [sink]: Climb layer
Outputs: OUTPUT [outputVector], TOTALCLIMB [outputNumber], TOTALDESCENT [outputNumber], MINELEVATION [outputNumber], MAXELEVATION [outputNumber]

### native:countpointsinpolygon: Count points in polygon
This algorithm takes a points layer and a polygon layer and counts the number of points from the first one in each polygons of the second one.
A new polygons layer is generated, with the exact same content as the input polygons layer, but containing an additional field with the points count corresponding to each polygon.
An optional weight field can be used to assign weights to each point. If set, the count generated will be the sum of the weight field for each point contained by the polygon.
Alternatively, a unique class field can be specified. If set, points are classified based on the selected attribute, and if several points with the same attribute value are within the polygon, only one of them is counted. The final count of the point in a polygon is, therefore, the count of different classes that are found in it.
Both the weight field and unique class field cannot be specified. If they are, the weight field will take precedence and the unique class field will be ignored.
Parameters:
- POLYGONS [source]: Polygons
- POINTS [source]: Points
- WEIGHT [field]: Weight field (optional)
- CLASSFIELD [field]: Class field (optional)
- FIELD [string]: Count field name (default NUMPOINTS)
- OUTPUT [sink]: Count
Outputs: OUTPUT [outputVector]

### native:dbscanclustering: DBSCAN clustering
This algorithm clusters point features based on a 2D implementation of Density-based spatial clustering of applications with noise (DBSCAN) algorithm.
The algorithm requires two parameters, a minimum cluster size (“minPts”), and the maximum distance allowed between clustered points (“eps”).
Parameters:
- INPUT [source]: Input layer
- MIN_SIZE [number]: Minimum cluster size (default 5)
- EPS [distance]: Maximum distance between clustered points (default 1)
- DBSCAN* [boolean]: Treat border points as noise (DBSCAN*) (default False)
- FIELD_NAME [string]: Cluster field name (default CLUSTER_ID)
- SIZE_FIELD_NAME [string]: Cluster size field name (default CLUSTER_SIZE)
- OUTPUT [sink]: Clusters
Outputs: OUTPUT [outputVector], NUM_CLUSTERS [outputNumber]

### native:hublines: Join by lines (hub lines)
This algorithm creates hub and spoke diagrams by connecting lines from points on the Spoke layer to matching points in the Hub layer.
Determination of which hub goes with each point is based on a match between the Hub ID field on the hub points and the Spoke ID field on the spoke points.
If input layers are not point layers, a point on the surface of the geometries will be taken as the connecting location.
Optionally, geodesic lines can be created, which represent the shortest path on the surface of an ellipsoid. When geodesic mode is used, it is possible to split the created lines at the antimeridian (±180 degrees longitude), which can improve rendering of the lines. Additionally, the distance between vertices can be specified. A smaller distance results in a denser, more accurate line.
Parameters:
- HUBS [source]: Hub layer
- HUB_FIELD [field]: Hub ID field
- HUB_FIELDS [field]: Hub layer fields to copy (leave empty to copy all fields) (optional)
- SPOKES [source]: Spoke layer
- SPOKE_FIELD [field]: Spoke ID field
- SPOKE_FIELDS [field]: Spoke layer fields to copy (leave empty to copy all fields) (optional)
- GEODESIC [boolean]: Create geodesic lines (default False)
- GEODESIC_DISTANCE [distance]: Distance between vertices (geodesic lines only) (default 1000)
- ANTIMERIDIAN_SPLIT [boolean]: Split lines at antimeridian (±180 degrees longitude) (default False)
- OUTPUT [sink]: Hub lines
Outputs: OUTPUT [outputVector]

### native:kmeansclustering: K-means clustering
This algorithm calculates the 2D distance based k-means cluster number for each input feature.
If input geometries are lines or polygons, the clustering is based on the centroid of the feature.
References:
Arthur, David & Vassilvitskii, Sergei. (2007). K-Means++: The Advantages of Careful Seeding. Proc. of the Annu. ACM-SIAM Symp. on Discrete Algorithms. 8.
Bhattacharya, Anup & Eube, Jan & Röglin, Heiko & Schmidt, Melanie. (2019). Noisy, Greedy and Not So Greedy k-means++
Parameters:
- INPUT [source]: Input layer
- CLUSTERS [number]: Number of clusters (default 5)
- METHOD [enum]: Method (default 0; options 0=Farthest points, 1=K-means++)
- FIELD_NAME [string]: Cluster field name (default CLUSTER_ID)
- SIZE_FIELD_NAME [string]: Cluster size field name (default CLUSTER_SIZE)
- OUTPUT [sink]: Clusters
Outputs: OUTPUT [outputVector]

### native:meancoordinates: Mean coordinate(s)
This algorithm computes a point layer with the center of mass of geometries in an input layer.
An attribute can be specified as containing weights to be applied to each feature when computing the center of mass.
If an attribute is selected in the parameter, features will be grouped according to values in this field. Instead of a single point with the center of mass of the whole layer, the output layer will contain a center of mass for the features in each category.
Parameters:
- INPUT [source]: Input layer
- WEIGHT [field]: Weight field (optional)
- UID [field]: Unique ID field (optional)
- OUTPUT [sink]: Mean coordinates
Outputs: OUTPUT [outputVector]

### native:nearestneighbouranalysis: Nearest neighbour analysis
This algorithm performs nearest neighbor analysis for a point layer.
The output describes how the data are distributed (clustered, randomly or distributed).
Output is generated as an HTML file with the computed statistical values.
Parameters:
- INPUT [source]: Input layer
- OUTPUT_HTML_FILE [fileDestination]: Nearest neighbour (optional)
Outputs: OUTPUT_HTML_FILE [outputHtml], OBSERVED_MD [outputNumber], EXPECTED_MD [outputNumber], NN_INDEX [outputNumber], POINT_COUNT [outputNumber], Z_SCORE [outputNumber]

### native:shortestline: Shortest line between features
This algorithm creates a line layer as the shortest line between the source and the destination layer. By default only the first nearest feature of the destination layer is taken into account. The n-nearest neighboring features number can be specified.
If a maximum distance is specified, then only features which are closer than this distance will be considered.
The output features will contain all the source layer attributes, all the attributes from the n-nearest feature and the additional field of the distance.
This algorithm uses purely Cartesian calculations for distance, and does not consider geodetic or ellipsoid properties when determining feature proximity. The measurement and output coordinate system is based on the coordinate system of the source layer.
Parameters:
- SOURCE [source]: Source layer
- DESTINATION [source]: Destination layer
- METHOD [enum]: Method (default 0; options 0=Distance to Nearest Point on feature, 1=Distance to Feature Centroid)
- NEIGHBORS [number]: Maximum number of neighbors (default 1)
- DISTANCE [distance]: Maximum distance (optional)
- OUTPUT [sink]: Shortest lines
Outputs: OUTPUT [outputVector]

### native:stdbscanclustering: ST-DBSCAN clustering
Clusters point features based on a 2D implementation of spatiotemporal density-based clustering of applications with noise (ST-DBSCAN) algorithm.
For more details, please see the following papers:
* Ester, M., H. P. Kriegel, J. Sander, and X. Xu, "A Density-Based Algorithm for Discovering Clusters in Large Spatial Databases with Noise". In: Proceedings of the 2nd International Conference on Knowledge Discovery and Data Mining, Portland, OR, AAAI Press, pp. 226-231. 1996
* Birant, Derya, and Alp Kut. "ST-DBSCAN: An algorithm for clustering spatial–temporal data." Data & Knowledge Engineering 60.1 (2007): 208-221.
* Peca, I., Fuchs, G., Vrotsou, K., Andrienko, N. V., & Andrienko, G. L. (2012). Scalable Cluster Analysis of Spatial Events. In EuroVA@ EuroVis.
Parameters:
- INPUT [source]: Input layer
- DATETIME_FIELD [field]: Date/time field
- MIN_SIZE [number]: Minimum cluster size (default 5)
- EPS [distance]: Maximum distance between clustered points (default 1)
- EPS2 [duration]: Maximum time duration between clustered points (default 0)
- DBSCAN* [boolean]: Treat border points as noise (DBSCAN*) (optional; default False)
- FIELD_NAME [string]: Cluster field name (default CLUSTER_ID)
- SIZE_FIELD_NAME [string]: Cluster size field name (default CLUSTER_SIZE)
- OUTPUT [sink]: Clusters
Outputs: OUTPUT [outputVector], NUM_CLUSTERS [outputNumber]

### native:sumlinelengths: Sum line lengths
This algorithm takes a polygon layer and a line layer and measures the total length of lines and the total number of them that cross each polygon.
The resulting layer has the same features as the input polygon layer, but with two additional attributes containing the length and count of the lines across each polygon. The names of these two fields can be configured in the algorithm parameters.
Parameters:
- POLYGONS [source]: Polygons
- LINES [source]: Lines
- LEN_FIELD [string]: Lines length field name (default LENGTH)
- COUNT_FIELD [string]: Lines count field name (default COUNT)
- OUTPUT [sink]: Line length
Outputs: OUTPUT [outputVector]


## QGIS (native c++) / Vector coverage

### native:coveragesimplify: Simplify coverage
This algorithm operates on a coverage (represented as a set of polygon features with exactly matching edge geometry) to apply a Visvalingam–Whyatt simplification to the edges, reducing complexity in proportion with the provided tolerance, while retaining a valid coverage (i.e. no edges will cross or touch after the simplification).
Geometries will never be removed, but they may be simplified down to just a triangle. Also, some geometries (such as polygons which have too few non-repeated points) will be returned unchanged.
If the input dataset is not a valid coverage due to overlaps, it will still be simplified, but invalid topology such as crossing edges will still be invalid.
Parameters:
- INPUT [source]: Input layer
- TOLERANCE [distance]: Tolerance (default 1.0)
- PRESERVE_BOUNDARY [boolean]: Preserve boundary (default False)
- OUTPUT [sink]: Simplified
Outputs: OUTPUT [outputVector]

### native:coverageunion: Dissolve coverage
This algorithm operates on a coverage (represented as a set of polygon features with exactly matching edge geometry) to dissolve (union) the geometries.
It provides a heavily optimized approach for unioning these features compared with the standard Dissolve tools.
Parameters:
- INPUT [source]: Input layer
- OUTPUT [sink]: Dissolved
Outputs: OUTPUT [outputVector]

### native:coveragevalidate: Validate coverage
This algorithm analyzes a coverage (represented as a set of polygon features with exactly matching edge geometry) to find places where the assumption of exactly matching edges is not met.
Invalidity includes polygons that overlap or that have gaps smaller than the specified gap width.
Parameters:
- INPUT [source]: Input layer
- GAP_WIDTH [distance]: Gap width (default 0.0)
- INVALID_EDGES [sink]: Invalid edges (optional)
Outputs: INVALID_EDGES [outputVector], IS_VALID [outputBoolean]


## QGIS (native c++) / Vector creation

### native:arrayoffsetlines: Array of offset (parallel) lines
This algorithm creates copies of line features in a layer, by creating multiple offset versions of each feature. Each copy is offset by a preset distance.
Parameters:
- INPUT [source]: Input layer
- COUNT [number]: Number of features to create (default 10)
- OFFSET [distance]: Offset step distance (default 1.0)
- SEGMENTS [number]: Segments (default 8)
- JOIN_STYLE [enum]: Join style (default 0; options 0=Round, 1=Miter, 2=Bevel)
- MITER_LIMIT [number]: Miter limit (default 2)
- OUTPUT [sink]: Offset lines
Outputs: OUTPUT [outputVector]

### native:arraytranslatedfeatures: Array of translated features
This algorithm creates copies of features in a layer, by creating multiple translated versions of each feature. Each copy is incrementally displaced by a preset amount in the x/y/z/m axis.
Parameters:
- INPUT [source]: Input layer
- COUNT [number]: Number of features to create (default 10)
- DELTA_X [distance]: Step distance (x-axis) (default 0.0)
- DELTA_Y [distance]: Step distance (y-axis) (default 0.0)
- DELTA_Z [number]: Step distance (z-axis) (default 0.0)
- DELTA_M [number]: Step distance (m values) (default 0.0)
- OUTPUT [sink]: Translated
Outputs: OUTPUT [outputVector]

### native:creategrid: Create grid
This algorithm creates a vector layer with a grid covering a given extent. Elements in the grid can be points, lines or polygons. The size and/or placement of each element in the grid is defined using a horizontal and vertical spacing. The CRS of the output layer must be defined. The grid extent and the spacing values must be expressed in the coordinates and units of this CRS. The top-left point (minX, maxY) is used as the reference point. That means that, at that point, an element is guaranteed to be placed. Unless the width and height of the selected extent is a multiple of the selected spacing, that is not true for the other points that define that extent.
Parameters:
- TYPE [enum]: Grid type (default 0; options 0=Point, 1=Line, 2=Rectangle (Polygon), 3=Diamond (Polygon), 4=Hexagon (Polygon))
- EXTENT [extent]: Grid extent
- HSPACING [distance]: Horizontal spacing (default 1)
- VSPACING [distance]: Vertical spacing (default 1)
- HOVERLAY [distance]: Horizontal overlay (default 0)
- VOVERLAY [distance]: Vertical overlay (default 0)
- CRS [crs]: Grid CRS (default ProjectCrs)
- OUTPUT [sink]: Grid
Outputs: OUTPUT [outputVector]

### native:createpointslayerfromtable: Create points layer from table
This algorithm generates a point layer based on the coordinates from an input table.
The table must contain a field with the X coordinate of each point and another one with the Y coordinate, as well as optional fields with Z and M values. A CRS for the output layer has to be specified, and the coordinates in the table are assumed to be expressed in the units used by that CRS. The attributes table of the resulting layer will be the input table.
Parameters:
- INPUT [source]: Input layer
- XFIELD [field]: X field
- YFIELD [field]: Y field
- ZFIELD [field]: Z field (optional)
- MFIELD [field]: M field (optional)
- TARGET_CRS [crs]: Target CRS (default EPSG:4326)
- OUTPUT [sink]: Points from table
Outputs: OUTPUT [outputVector]

### native:extenttolayer: Create layer from extent
This algorithm creates a new vector layer that contains a single feature with geometry matching an extent parameter.
It can be used in models to convert an extent into a layer which can be used for other algorithms which require a layer based input.
Parameters:
- INPUT [extent]: Extent
- OUTPUT [sink]: Extent
Outputs: OUTPUT [outputVector]

### native:generatepointspixelcentroidsinsidepolygons: Generate points (pixel centroids) inside polygons
This algorithm generates pixel centroids for the raster area falling inside polygons. Used to generate points for further raster sampling.
Parameters:
- INPUT_RASTER [raster]: Raster layer
- INPUT_VECTOR [source]: Vector layer
- OUTPUT [sink]: Pixel centroids
Outputs: OUTPUT [outputVector]

### native:importphotos: Import geotagged photos
This algorithm creates a point layer corresponding to the geotagged locations from JPEG or HEIF/HEIC images from a source folder. Optionally the folder can be recursively scanned.
The point layer will contain a single PointZ feature per input file from which the geotags could be read. Any altitude information from the geotags will be used to set the point's Z value.
Optionally, a table of unreadable or non-geotagged photos can also be created.
Parameters:
- FOLDER [file]: Input folder
- RECURSIVE [boolean]: Scan recursively (default False)
- OUTPUT [sink]: Photos (optional)
- INVALID [sink]: Invalid photos table (optional)
Outputs: OUTPUT [outputVector], INVALID [outputVector]

### native:pixelstopoints: Raster pixels to points
This algorithm converts a raster layer to a vector layer, by creating point features for each individual pixel's center in the raster layer.
Any NoData pixels are skipped in the output.
Parameters:
- INPUT_RASTER [raster]: Raster layer
- RASTER_BAND [band]: Band number (default 1)
- FIELD_NAME [string]: Field name (default VALUE)
- OUTPUT [sink]: Vector points
Outputs: OUTPUT [outputVector]

### native:pixelstopolygons: Raster pixels to polygons
This algorithm converts a raster layer to a vector layer, by creating polygon features for each individual pixel's extent in the raster layer.
Any NoData pixels are skipped in the output.
Parameters:
- INPUT_RASTER [raster]: Raster layer
- RASTER_BAND [band]: Band number (default 1)
- FIELD_NAME [string]: Field name (default VALUE)
- OUTPUT [sink]: Vector polygons
Outputs: OUTPUT [outputVector]

### native:pointstopath: Points to path
This algorithm takes a point layer and connects its features to create a new line layer.
An attribute or expression may be specified to define the order the points should be connected. If no order expression is specified, the feature ID is used.
A natural sort can be used when sorting by a string attribute or expression (ie. place 'a9' before 'a10').
An attribute or expression can be selected to group points having the same value into the same resulting line.
Parameters:
- INPUT [source]: Input layer
- CLOSE_PATH [boolean]: Create closed paths (default False)
- ORDER_EXPRESSION [expression]: Order expression (optional)
- NATURAL_SORT [boolean]: Sort text containing numbers naturally (default False)
- GROUP_EXPRESSION [expression]: Path group expression (optional)
- OUTPUT [sink]: Paths
- OUTPUT_TEXT_DIR [folderDestination]: Directory for text output (optional)
- ORDER_FIELD [field]: Order field (optional)
- GROUP_FIELD [field]: Group field (optional)
- DATE_FORMAT [string]: Date format (if order field is DateTime) (optional)
Outputs: OUTPUT [outputVector], OUTPUT_TEXT_DIR [outputFolder], NUM_PATHS [outputNumber]

### native:pointtolayer: Create layer from point
This algorithm creates a new vector layer that contains a single feature with geometry matching a point parameter.
It can be used in models to convert a point into a layer which can be used for other algorithms which require a layer based input.
Parameters:
- INPUT [point]: Point
- OUTPUT [sink]: Point
Outputs: OUTPUT [outputVector]

### native:randompointsinextent: Random points in extent
This algorithm creates a new point layer with a given number of random points, all of them within a given extent. A distance factor can be specified, to avoid points being too close to each other. If the minimum distance between points makes it impossible to create new points, either distance can be decreased or the maximum number of attempts may be increased.
Parameters:
- EXTENT [extent]: Input extent
- POINTS_NUMBER [number]: Number of points (default 1)
- MIN_DISTANCE [distance]: Minimum distance between points (optional; default 0)
- TARGET_CRS [crs]: Target CRS (default ProjectCrs)
- MAX_ATTEMPTS [number]: Maximum number of search attempts given the minimum distance (optional; default 200)
- OUTPUT [sink]: Random points
Outputs: OUTPUT [outputVector]

### native:randompointsinpolygons: Random points in polygons
This algorithm creates a point layer, with points placed randomly in the polygons of the Input polygon layer.
 For each feature in the Input polygon layer, the algorithm attempts to add the specified Number of points for each feature to the output layer.
 A Minimum distance between points and a Global minimum distance between points can be specified.
 A point will not be added if there is an already generated point within this (Euclidean) distance from the generated location. With Minimum distance between points, only points in the same polygon feature are considered, while for Global minimum distance between points all previously generated points are considered. If the Global minimum distance between points is set equal to or larger than the (local) Minimum distance between points, the latter has no effect.
 If the Minimum distance between points is too large, it may not be possible to generate the specified Number of points for each feature, but all the generated points are returned.
 The Maximum number of attempts per point can be specified.
 The seed for the random generator can be provided (Random seed - integer, greater than 0).
 The user can choose not to Include polygon feature attributes in the attributes of the generated point features.
 The total number of points will be
 'number of input features' * Number of points for each feature
 if there are no misses. The Number of points for each feature, Minimum distance between points and Maximum number of attempts per point can be data defined. Output from the algorithm:
 The number of features with an empty or no geometry (FEATURES_WITH_EMPTY_OR_NO_GEOMETRY).
 A point layer containing the random points (OUTPUT).
 The number of generated features (OUTPUT_POINTS).
 The number of missed points (POINTS_MISSED).
 The number of features with non-empty geometry and missing points (POLYGONS_WITH_MISSED_POINTS).
Parameters:
- INPUT [source]: Input polygon layer
- POINTS_NUMBER [number]: Number of points for each feature (default 1)
- MIN_DISTANCE [distance]: Minimum distance between points (optional; default 0)
- MIN_DISTANCE_GLOBAL [distance]: Global minimum distance between points (optional; default 0)
- MAX_TRIES_PER_POINT [number]: Maximum number of search attempts (for Min. dist. > 0) (optional; default 10)
- SEED [number]: Random seed (optional)
- INCLUDE_POLYGON_ATTRIBUTES [boolean]: Include polygon attributes (default True)
- OUTPUT [sink]: Random points in polygons
Outputs: OUTPUT [outputVector], OUTPUT_POINTS [outputNumber], POINTS_MISSED [outputNumber], POLYGONS_WITH_MISSED_POINTS [outputNumber], FEATURES_WITH_EMPTY_OR_NO_GEOMETRY [outputNumber]

### native:randompointsonlines: Random points on lines
This algorithm creates a point layer with points placed randomly on the lines of the Input line layer. The default behavior is that the generated point features inherit the attributes of the line feature on which they were generated.
Parameters / options:
 For each feature in the Input line layer, the algorithm attempts to add the specified Number of points for each feature to the output layer.
 A Minimum distance between points and a Global minimum distance between points can be specified. A point will not be added if there is an already generated point within this (Euclidean) distance from the generated location. With Minimum distance between points, only points on the same line feature are considered, while for Global minimum distance between points all previously generated points are considered. If the Global minimum distance between points is set larger than the (local) Minimum distance between points, the latter has no effect.
 If the Minimum distance between points is too large, it may not be possible to generate the specified Number of points for each feature.
 The Maximum number of attempts per point is only relevant if Minimum distance between points or Global minimum distance between points is greater than 0. The total number of points will be
 number of input features * Number of points for each feature
 if there are no misses and all features have proper geometries.
 The seed for the random generator can be provided (Random seed - integer, greater than 0).
 The user can choose not to Include line feature attributes in the generated point features.
 Output from the algorithm:
 A point layer containing the random points (OUTPUT).
 The number of generated features (POINTS_GENERATED).
 The number of missed points (POINTS_MISSED).
 The number of features with non-empty geometry and missing points (LINES_WITH_MISSED_POINTS).
 The number of features with an empty or no geometry (LINES_WITH_EMPTY_OR_NO_GEOMETRY).
Parameters:
- INPUT [source]: Input line layer
- POINTS_NUMBER [number]: Number of points for each feature (default 1)
- MIN_DISTANCE [distance]: Minimum distance between points (optional; default 0)
- MIN_DISTANCE_GLOBAL [distance]: Global minimum distance between points (optional; default 0)
- MAX_TRIES_PER_POINT [number]: Maximum number of search attempts (for Min. dist. > 0) (optional; default 10)
- SEED [number]: Random seed (optional)
- INCLUDE_LINE_ATTRIBUTES [boolean]: Include line attributes (default True)
- OUTPUT [sink]: Random points on lines
Outputs: OUTPUT [outputVector], OUTPUT_POINTS [outputNumber], POINTS_MISSED [outputNumber], LINES_WITH_MISSED_POINTS [outputNumber], FEATURES_WITH_EMPTY_OR_NO_GEOMETRY [outputNumber]


## QGIS (native c++) / Vector general

### native:assignprojection: Assign projection
This algorithm assigns a new projection to a vector layer. It creates a new layer with the exact same features and geometries as the input one, but assigned to a new CRS. E.g. the geometries are not reprojected, they are just assigned to a different CRS. This algorithm can be used to repair layers which have been assigned an incorrect projection.
Attributes are not modified by this algorithm.
Parameters:
- INPUT [source]: Input layer
- CRS [crs]: Assigned CRS (default EPSG:4326)
- OUTPUT [sink]: Assigned CRS
Outputs: OUTPUT [outputVector]

### native:batchnominatimgeocoder: Batch Nominatim geocoder
This algorithm performs batch geocoding using the Nominatim service against an input layer string field.
The output layer will have a point geometry reflecting the geocoded location as well as a number of attributes associated to the geocoded location.
Parameters:
- INPUT [source]: Input layer
- FIELD [field]: Address field
- OUTPUT [sink]: Geocoded
Outputs: OUTPUT [outputVector]

### native:bookmarkstolayer: Convert spatial bookmarks to layer
This algorithm creates a new layer containing polygon features for stored spatial bookmarks.
The export can be filtered to only bookmarks belonging to the current project, to all user bookmarks, or a combination of both.
Parameters:
- SOURCE [enum]: Bookmark source (default [0, 1]; options 0=Project bookmarks, 1=User bookmarks)
- CRS [crs]: Output CRS (default <QgsCoordinateReferenceSystem: EPSG:4326>)
- OUTPUT [sink]: Output
Outputs: OUTPUT [outputVector]

### native:createattributeindex: Create attribute index
This algorithm creates an index to speed up queries made against a field in a table. Support for index creation is dependent on the layer's data provider and the field type.
Parameters:
- INPUT [vector]: Input layer
- FIELD [field]: Attribute to index
Outputs: OUTPUT [outputVector]

### native:createspatialindex: Create spatial index
Creates an index to speed up access to the features in a layer based on their spatial location. Support for spatial index creation is dependent on the layer's data provider.
Parameters:
- INPUT [vector]: Input layer
Outputs: OUTPUT [outputVector]

### native:definecurrentprojection: Define projection
This algorithm sets an existing layer's projection to the provided CRS without reprojecting features. Contrary to the "Assign projection" algorithm, it will not output a new layer.
If the input layer is a shapefile, the .prj file will be overwritten — or created if missing — to match the provided CRS.
Parameters:
- INPUT [vector]: Input shapefile
- CRS [crs]: CRS (default <QgsCoordinateReferenceSystem: EPSG:4326>)
Outputs: OUTPUT [outputVector]

### native:deleteduplicategeometries: Delete duplicate geometries
This algorithm finds duplicated geometries and removes them.
Attributes are not checked, so in case two features have identical geometries but different attributes, only one of them will be added to the result layer.
Parameters:
- INPUT [source]: Input layer
- OUTPUT [sink]: Cleaned
Outputs: OUTPUT [outputVector], RETAINED_COUNT [outputNumber], DUPLICATE_COUNT [outputNumber]

### native:detectvectorchanges: Detect dataset changes
This algorithm compares two vector layers, and determines which features are unchanged, added or deleted between the two. It is designed for comparing two different versions of the same dataset.
When comparing features, the original and revised feature geometries will be compared against each other. Depending on the Geometry Comparison Behavior setting, the comparison will either be made using an exact comparison (where geometries must be an exact match for each other, including the order and count of vertices) or a topological comparison only (where geometries are considered equal if all of their component edges overlap. E.g. lines with the same vertex locations but opposite direction will be considered equal by this method). If the topological comparison is selected then any z or m values present in the geometries will not be compared.
By default, the algorithm compares all attributes from the original and revised features. If the Attributes to Consider for Match parameter is changed, then only the selected attributes will be compared (e.g. allowing users to ignore a timestamp or ID field which is expected to change between the revisions).
If any features in the original or revised layers do not have an associated geometry, then care must be taken to ensure that these features have a unique set of attributes selected for comparison. If this condition is not met, warnings will be raised and the resultant outputs may be misleading.
The algorithm outputs three layers, one containing all features which are considered to be unchanged between the revisions, one containing features deleted from the original layer which are not present in the revised layer, and one containing features added to the revised layer which are not present in the original layer.
Parameters:
- ORIGINAL [source]: Original layer
- REVISED [source]: Revised layer
- COMPARE_ATTRIBUTES [field]: Attributes to consider for match (or none to compare geometry only) (optional)
- MATCH_TYPE [enum]: Geometry comparison behavior (default 1; options 0=Exact Match, 1=Tolerant Match (Topological Equality))
- UNCHANGED [sink]: Unchanged features (optional)
- ADDED [sink]: Added features (optional)
- DELETED [sink]: Deleted features (optional)
Outputs: UNCHANGED [outputVector], ADDED [outputVector], DELETED [outputVector], UNCHANGED_COUNT [outputNumber], ADDED_COUNT [outputNumber], DELETED_COUNT [outputNumber]

### native:dropgeometries: Drop geometries
This algorithm removes any geometries from an input layer and returns a layer containing only the feature attributes.
Parameters:
- INPUT [source]: Input layer
- OUTPUT [sink]: Dropped geometries
Outputs: OUTPUT [outputVector]

### native:dxfexport: Export layers to DXF
Exports layers to a DXF file. For each layer, you can choose a field whose values are used to split features in generated destination layers in the DXF output.
If no field is chosen, you can still override the output layer name by directly entering a new output layer name in the Configure Layer panel or by preferring layer title (set in layer properties) to layer name.
Parameters:
- LAYERS [dxflayers]: Input layers
- SYMBOLOGY_MODE [enum]: Symbology mode (default 0; options 0=No Symbology, 1=Feature Symbology, 2=Symbol Layer Symbology)
- SYMBOLOGY_SCALE [scale]: Symbology scale (default 1000000)
- MAP_THEME [maptheme]: Map theme (optional)
- ENCODING [enum]: Encoding (default cp1252; options 0=cp1252, 1=ISO-8859-1, 2=ISO-8859-2, 3=ISO-8859-3, 4=ISO-8859-4, 5=ISO-8859-5, 6=ISO-8859-6, 7=ISO-8859-7, 8=ISO-8859-8, 9=ISO-8859-9, 10=Shift_JIS, 11=Big5, 12=CP936, 13=GB2312, 14=ms949, 15=cp850, 16=cp866, 17=cp1250, 18=cp1251, 19=cp1253, 20=cp1254, 21=cp1255, 22=cp1256, 23=cp1257, 24=cp1258, 25=macroman)
- CRS [crs]: CRS (default EPSG:4326)
- EXTENT [extent]: Extent (optional)
- SELECTED_FEATURES_ONLY [boolean]: Use only selected features (default False)
- USE_LAYER_TITLE [boolean]: Use layer title as name (default False)
- FORCE_2D [boolean]: Force 2D output (default False)
- MTEXT [boolean]: Export labels as MTEXT elements (default True)
- EXPORT_LINES_WITH_ZERO_WIDTH [boolean]: Export lines with zero width
- OUTPUT [fileDestination]: DXF
Outputs: OUTPUT [outputFile]

### native:findprojection: Find projection
Creates a list of possible candidate coordinate reference systems for a layer with an unknown projection.
The expected area which the layer should reside in must be specified via the target area parameter.
The algorithm operates by testing the layer's extent in every known reference system and listing any in which the bounds would fall within the target area if the layer was in this projection.
Parameters:
- INPUT [source]: Input layer
- TARGET_AREA [extent]: Target area for layer
- TARGET_AREA_CRS [crs]: Target area CRS (optional)
- OUTPUT [sink]: CRS candidates
Outputs: OUTPUT [outputVector]

### native:flattenrelationships: Flatten relationship
This algorithm flattens a relationship for a vector layer, exporting a single layer containing one master feature per related feature. This master feature contains all the attributes for the related features.
Parameters:
- INPUT [vector]: Input layer
- OUTPUT [sink]: Flattened layer
Outputs: OUTPUT [outputVector]

### native:joinattributesbylocation: Join attributes by location
This algorithm takes an input vector layer and creates a new vector layer that is an extended version of the input one, with additional attributes in its attribute table.
The additional attributes and their values are taken from a second vector layer. A spatial criteria is applied to select the values from the second layer that are added to each feature from the first layer in the resulting one.
Parameters:
- INPUT [source]: Join to features in
- PREDICATE [enum]: Features they (geometric predicate) (default 0; options 0=intersect, 1=contain, 2=equal, 3=touch, 4=overlap, 5=are within, 6=cross)
- JOIN [source]: By comparing to
- JOIN_FIELDS [field]: Fields to add (leave empty to use all fields) (optional)
- METHOD [enum]: Join type (default 0; options 0=Create separate feature for each matching feature (one-to-many), 1=Take attributes of the first matching feature only (one-to-one), 2=Take attributes of the feature with largest overlap only (one-to-one))
- DISCARD_NONMATCHING [boolean]: Discard records which could not be joined (default False)
- PREFIX [string]: Joined field prefix (optional)
- OUTPUT [sink]: Joined layer (optional)
- NON_MATCHING [sink]: Unjoinable features from first layer (optional)
Outputs: OUTPUT [outputVector], NON_MATCHING [outputVector], JOINED_COUNT [outputNumber]

### native:joinattributestable: Join attributes by field value
This algorithm takes an input vector layer and creates a new vector layer that is an extended version of the input one, with additional attributes in its attribute table.
The additional attributes and their values are taken from a second vector layer. An attribute is selected in each of them to define the join criteria.
Parameters:
- INPUT [source]: Input layer
- FIELD [field]: Table field
- INPUT_2 [source]: Input layer 2
- FIELD_2 [field]: Table field 2
- FIELDS_TO_COPY [field]: Layer 2 fields to copy (leave empty to copy all fields) (optional)
- METHOD [enum]: Join type (default 1; options 0=Create separate feature for each matching feature (one-to-many), 1=Take attributes of the first matching feature only (one-to-one))
- DISCARD_NONMATCHING [boolean]: Discard records which could not be joined (default False)
- PREFIX [string]: Joined field prefix (optional)
- OUTPUT [sink]: Joined layer (optional)
- NON_MATCHING [sink]: Unjoinable features from first layer (optional)
Outputs: OUTPUT [outputVector], NON_MATCHING [outputVector], JOINED_COUNT [outputNumber], UNJOINABLE_COUNT [outputNumber]

### native:joinbylocationsummary: Join attributes by location (summary)
This algorithm takes an input vector layer and creates a new vector layer that is an extended version of the input one, with additional attributes in its attribute table.
The additional attributes and their values are taken from a second vector layer. A spatial criteria is applied to select the values from the second layer that are added to each feature from the first layer in the resulting one.
The algorithm calculates a statistical summary for the values from matching features in the second layer( e.g. maximum value, mean value, etc ).
Parameters:
- INPUT [source]: Join to features in
- PREDICATE [enum]: Where the features (default 0; options 0=intersect, 1=contain, 2=equal, 3=touch, 4=overlap, 5=are within, 6=cross)
- JOIN [source]: By comparing to
- JOIN_FIELDS [field]: Fields to summarise (leave empty to use all fields) (optional)
- SUMMARIES [enum]: Summaries to calculate (leave empty to use all available) (optional; options 0=count, 1=unique, 2=min, 3=max, 4=range, 5=sum, 6=mean, 7=median, 8=stddev, 9=minority, 10=majority, 11=q1, 12=q3, 13=iqr, 14=empty, 15=filled, 16=min_length, 17=max_length, 18=mean_length)
- DISCARD_NONMATCHING [boolean]: Discard records which could not be joined (default False)
- OUTPUT [sink]: Joined layer
Outputs: OUTPUT [outputVector]

### native:joinbynearest: Join attributes by nearest
This algorithm takes an input vector layer and creates a new vector layer that is an extended version of the input one, with additional attributes in its attribute table.
The additional attributes and their values are taken from a second vector layer, where features are joined by finding the closest features from each layer. By default only the single nearest feature is joined,but optionally the join can use the n-nearest neighboring features instead. If multiple features are found with identical distances these will all be returned (even if the total number of features exceeds the specified maximum feature count).
If a maximum distance is specified, then only features which are closer than this distance will be matched.
The output features will contain the selected attributes from the nearest feature, along with new attributes for the distance to the near feature, the index of the feature, and the coordinates of the closest point on the input feature (feature_x, feature_y) to the matched nearest feature, and the coordinates of the closet point on the matched feature (nearest_x, nearest_y).
This algorithm uses purely Cartesian calculations for distance, and does not consider geodetic or ellipsoid properties when determining feature proximity.
Parameters:
- INPUT [source]: Input layer
- INPUT_2 [source]: Input layer 2
- FIELDS_TO_COPY [field]: Layer 2 fields to copy (leave empty to copy all fields) (optional)
- DISCARD_NONMATCHING [boolean]: Discard records which could not be joined (default False)
- PREFIX [string]: Joined field prefix (optional)
- NEIGHBORS [number]: Maximum nearest neighbors (default 1)
- MAX_DISTANCE [distance]: Maximum distance (optional)
- OUTPUT [sink]: Joined layer (optional)
- NON_MATCHING [sink]: Unjoinable features from first layer (optional)
Outputs: OUTPUT [outputVector], NON_MATCHING [outputVector], JOINED_COUNT [outputNumber], UNJOINABLE_COUNT [outputNumber]

### native:layertobookmarks: Convert layer to spatial bookmarks
This algorithm creates spatial bookmarks corresponding to the extent of features contained in a layer.
Parameters:
- INPUT [source]: Input layer
- DESTINATION [enum]: Bookmark destination (default 0; options 0=Project bookmarks, 1=User bookmarks)
- NAME_EXPRESSION [expression]: Name field
- GROUP_EXPRESSION [expression]: Group field (optional)
Outputs: COUNT [outputNumber]

### native:mergevectorlayers: Merge vector layers
This algorithm combines multiple vector layers of the same geometry type into a single one.
The attribute table of the resulting layer will contain the fields from all input layers. If fields with the same name but different types are found then the exported field will be automatically converted into a string type field. Optionally, new fields storing the original layer name and source can be added.
If any input layers contain Z or M values, then the output layer will also contain these values. Similarly, if any of the input layers are multi-part, the output layer will also be a multi-part layer.
Optionally, the destination coordinate reference system (CRS) for the merged layer can be set. If it is not set, the CRS will be taken from the first input layer. All layers will all be reprojected to match this CRS.
Parameters:
- LAYERS [multilayer]: Input layers
- CRS [crs]: Destination CRS (optional)
- OUTPUT [sink]: Merged
- ADD_SOURCE_FIELDS [boolean]: Add source layer information (layer name and path) (default True)
Outputs: OUTPUT [outputVector]

### native:orderbyexpression: Order by expression
This algorithm sorts a vector layer according to an expression. Be careful, it might not work as expected with some providers, the order might not be kept every time.
For help with QGIS expression functions, see the inbuilt help for specific functions which is available in the expression builder.
Parameters:
- INPUT [source]: Input layer
- EXPRESSION [expression]: Expression
- ASCENDING [boolean]: Sort ascending (default True)
- NULLS_FIRST [boolean]: Sort nulls first (default False)
- OUTPUT [sink]: Ordered
Outputs: OUTPUT [outputVector]

### native:removeduplicatesbyattribute: Delete duplicates by attribute
This algorithm removes duplicate rows by a field value (or multiple field values). The first matching row will be retained, and duplicates will be discarded.
Optionally, these duplicate records can be saved to a separate output for analysis.
Parameters:
- INPUT [source]: Input layer
- FIELDS [field]: Field to match duplicates by
- OUTPUT [sink]: Filtered (no duplicates)
- DUPLICATES [sink]: Filtered (duplicates) (optional)
Outputs: OUTPUT [outputVector], DUPLICATES [outputVector], RETAINED_COUNT [outputNumber], DUPLICATE_COUNT [outputNumber]

### native:repairshapefile: Repair Shapefile
Repairs a broken Shapefile by recreating missing or broken SHX files.
Parameters:
- INPUT [file]: Input Shapefile
Outputs: OUTPUT [outputVector]

### native:reprojectlayer: Reproject layer
This algorithm reprojects a vector layer. It creates a new layer with the same features as the input one, but with geometries reprojected to a new CRS.
Attributes are not modified by this algorithm.
Parameters:
- INPUT [source]: Input layer
- TARGET_CRS [crs]: Target CRS (default EPSG:4326)
- CONVERT_CURVED_GEOMETRIES [boolean]: Convert curved geometries to straight segments (default False)
- OPERATION [coordinateoperation]: Coordinate operation (optional)
- OUTPUT [sink]: Reprojected
Outputs: OUTPUT [outputVector]

### native:savefeatures: Save vector features to file
This algorithm saves vector features to a specified file dataset.
For dataset formats supporting layers, an optional layer name parameter can be used to specify a custom string.
Optional GDAL-defined dataset and layer options can be specified. For more information on this, read the online GDAL documentation.
Parameters:
- INPUT [source]: Vector features
- OUTPUT [fileDestination]: Saved features
- LAYER_NAME [string]: Layer name (optional)
- DATASOURCE_OPTIONS [string]: GDAL dataset options (separate individual options with semicolons) (optional)
- LAYER_OPTIONS [string]: GDAL layer options (separate individual options with semicolons) (optional)
- ACTION_ON_EXISTING_FILE [enum]: Action to take on pre-existing file (default 0; options 0=Create or overwrite file, 1=Create or overwrite layer, 2=Append features to existing layer, but do not create new fields, 3=Append features to existing layer, and create new fields if needed)
Outputs: OUTPUT [outputFile], FILE_PATH [outputString], LAYER_NAME [outputString]

### native:saveselectedfeatures: Extract selected features
This algorithm creates a new layer with all the selected features in a given vector layer.
If the selected layer has no selected features, the newly created layer will be empty.
Parameters:
- INPUT [vector]: Input layer
- OUTPUT [sink]: Selected features
Outputs: OUTPUT [outputVector]

### native:setlayerencoding: Set layer encoding
This algorithm sets the encoding used for reading a layer's attributes. No permanent changes are made to the layer, rather it affects only how the layer is read during the current session.
Changing the encoding is only supported for some vector layer data sources.
Parameters:
- INPUT [vector]: Input layer
- ENCODING [string]: Encoding
Outputs: OUTPUT [outputVector]

### native:shpencodinginfo: Extract Shapefile encoding
This algorithm extracts the attribute encoding information embedded in a Shapefile.
Both the encoding specified by an optional .cpg file and any encoding details present in the .dbf LDID header block are considered.
Parameters:
- INPUT [file]: Input layer
Outputs: ENCODING [outputString], CPG_ENCODING [outputString], LDID_ENCODING [outputString]

### native:splitfeaturesbycharacter: Split features by character
This algorithm splits features into multiple output features by splitting a field's value with a specified character.
For instance, if a layer contains features with multiple comma separated values contained in a single field, this algorithm can be used to split these values up across multiple output features.
Geometries and other attributes remain unchanged in the output.
Optionally, the separator string can be a regular expression for added flexibility.
Parameters:
- INPUT [source]: Input layer
- FIELD [field]: Split using values in field
- CHAR [string]: Split values using character
- REGEX [boolean]: Use regular expression separator
- OUTPUT [sink]: Split
Outputs: OUTPUT [outputVector]

### native:splitvectorlayer: Split vector layer
This algorithm splits input vector layer into multiple layers by specified unique ID field.
Each of the layers created in the output folder contains all features from the input layer with the same value for the specified attribute. The number of files generated is equal to the number of different values found for the specified attribute.
Parameters:
- INPUT [source]: Input layer
- FIELD [field]: Unique ID field
- PREFIX_FIELD [boolean]: Add field prefix to file names (default True)
- FILE_TYPE [enum]: Output file type (optional; default 0; options 0=gpkg, 1=shp, 2=000, 3=arrow, 4=arrows, 5=csv, 6=dgn, 7=dxf, 8=feather, 9=fgb, 10=gdb, 11=geojson, 12=geojsonl, 13=geojsons, 14=gml, 15=gpkg.zip, 16=gpx, 17=ipc, 18=json, 19=kml, 20=ods, 21=parquet, 22=sql, 23=sqlite, 24=tab, 25=xlsx, 26=xml)
- OUTPUT [folderDestination]: Output directory
Outputs: OUTPUT [outputFolder], OUTPUT_LAYERS [outputMultilayer]

### native:truncatetable: Truncate table
This algorithm truncates a layer, by deleting all features from within the layer.
Warning — this algorithm modifies the layer in place, and deleted features cannot be restored!
Parameters:
- INPUT [vector]: Input layer
Outputs: OUTPUT [outputVector]


## QGIS (native c++) / Vector geometry

### native:affinetransform: Affine transform
This algorithm applies an affine transformation to the geometries from a layer. Affine transformations can include translation, scaling and rotation. The operations are performed in a scale, rotation, translation order.
Z and M values present in the geometry can also be translated and scaled independently.
Parameters:
- INPUT [source]: Input layer
- DELTA_X [distance]: Translation (x-axis) (default 0.0)
- DELTA_Y [distance]: Translation (y-axis) (default 0.0)
- DELTA_Z [number]: Translation (z-axis) (default 0.0)
- DELTA_M [number]: Translation (m values) (default 0.0)
- SCALE_X [number]: Scale factor (x-axis) (default 1.0)
- SCALE_Y [number]: Scale factor (y-axis) (default 1.0)
- SCALE_Z [number]: Scale factor (z-axis) (default 1.0)
- SCALE_M [number]: Scale factor (m values) (default 1.0)
- ROTATION_Z [number]: Rotation around z-axis (degrees counter-clockwise) (default 0.0)
- OUTPUT [sink]: Transformed
Outputs: OUTPUT [outputVector]

### native:aggregate: Aggregate
This algorithm takes a vector or table layer and aggregates features based on a group by expression. Features for which group by expression return the same value are grouped together.
It is possible to group all source features together using constant value in group by parameter, example: NULL.
It is also possible to group features using multiple fields using Array function, example: Array("Field1", "Field2").
Geometries (if present) are combined into one multipart geometry for each group.
Output attributes are computed depending on each given aggregate definition.
Parameters:
- INPUT [source]: Input layer
- GROUP_BY [expression]: Group by expression (NULL to group all features) (default NULL)
- AGGREGATES [aggregates]: Aggregates
- OUTPUT [sink]: Aggregated
Outputs: OUTPUT [outputVector]

### native:antimeridiansplit: Geodesic line split at antimeridian
This algorithm splits a line into multiple geodesic segments, whenever the line crosses the antimeridian (±180 degrees longitude).
Splitting at the antimeridian helps the visual display of the lines in some projections. The returned geometry will always be a multi-part geometry.
Whenever line segments in the input geometry cross the antimeridian, they will be split into two segments, with the latitude of the breakpoint being determined using a geodesic line connecting the points either side of this segment. The current project ellipsoid setting will be used when calculating this breakpoint.
If the input geometry contains M or Z values, these will be linearly interpolated for the new vertices created at the antimeridian.
Parameters:
- INPUT [source]: Input layer
- OUTPUT [sink]: Split
Outputs: OUTPUT [outputVector]

### native:boundary: Boundary
This algorithm returns the closure of the combinatorial boundary of the input geometries (ie the topological boundary of the geometry). For instance, a polygon geometry will have a boundary consisting of the linestrings for each ring in the polygon. Only valid for polygon or line layers.
Parameters:
- INPUT [source]: Input layer
- OUTPUT [sink]: Boundary
Outputs: OUTPUT [outputVector]

### native:boundingboxes: Bounding boxes
This algorithm calculates the bounding box (envelope) for each feature in an input layer.
See the 'Minimum bounding geometry' algorithm for a bounding box calculation which covers the whole layer or grouped subsets of features.
Parameters:
- INPUT [source]: Input layer
- OUTPUT [sink]: Bounds
Outputs: OUTPUT [outputVector]

### native:buffer: Buffer
This algorithm computes a buffer area for all the features in an input layer, using a fixed or dynamic distance.
The segments parameter controls the number of line segments to use to approximate a quarter circle when creating rounded offsets.
The end cap style parameter controls how line endings are handled in the buffer.
The join style parameter specifies whether round, miter or beveled joins should be used when offsetting corners in a line.
The miter limit parameter is only applicable for miter join styles, and controls the maximum distance from the offset curve to use when creating a mitered join.
Parameters:
- INPUT [source]: Input layer
- DISTANCE [distance]: Distance (default 10)
- SEGMENTS [number]: Segments (default 5)
- END_CAP_STYLE [enum]: End cap style (default 0; options 0=Round, 1=Flat, 2=Square)
- JOIN_STYLE [enum]: Join style (default 0; options 0=Round, 1=Miter, 2=Bevel)
- MITER_LIMIT [number]: Miter limit (default 2)
- DISSOLVE [boolean]: Dissolve result (default False)
- SEPARATE_DISJOINT [boolean]: Keep disjoint results separate (default False)
- OUTPUT [sink]: Buffered
Outputs: OUTPUT [outputVector]

### native:bufferbym: Variable width buffer (by M value)
This algorithm creates variable width buffers along lines, using the M value of the line geometries as the diameter of the buffer at each vertex.
Parameters:
- INPUT [source]: Input layer
- SEGMENTS [number]: Segments (default 16)
- OUTPUT [sink]: Buffered
Outputs: OUTPUT [outputVector]

### native:centroids: Centroids
This algorithm creates a new point layer with points representing the centroid of the geometries in an input layer.
The attributes associated to each point in the output layer are the same ones associated to the original features.
Parameters:
- INPUT [source]: Input layer
- ALL_PARTS [boolean]: Create centroid for each part (default False)
- OUTPUT [sink]: Centroids
Outputs: OUTPUT [outputVector]

### native:checkvalidity: Check validity
This algorithm performs a validity check on the geometries of a vector layer.
The geometries are classified in three groups (valid, invalid and error), and a vector layer is generated with the features in each of these categories.
By default the algorithm uses the strict OGC definition of polygon validity, where a polygon is marked as invalid if a self-intersecting ring causes an interior hole. If the 'Ignore ring self intersections' option is checked, then this rule will be ignored and a more lenient validity check will be performed.
The GEOS method is faster and performs better on larger geometries, but is limited to only returning the first error encountered in a geometry. The QGIS method will be slower but reports all errors encountered in the geometry, not just the first.
Parameters:
- INPUT_LAYER [source]: Input layer
- METHOD [enum]: Method (default 2; options 0=The one selected in digitizing settings, 1=QGIS, 2=GEOS)
- IGNORE_RING_SELF_INTERSECTION [boolean]: Ignore ring self intersections (default False)
- VALID_OUTPUT [sink]: Valid output (optional)
- INVALID_OUTPUT [sink]: Invalid output (optional)
- ERROR_OUTPUT [sink]: Error output (optional)
Outputs: VALID_OUTPUT [outputVector], INVALID_OUTPUT [outputVector], ERROR_OUTPUT [outputVector], VALID_COUNT [outputNumber], INVALID_COUNT [outputNumber], ERROR_COUNT [outputNumber]

### native:collect: Collect geometries
This algorithm takes a vector layer and collects its geometries into new multipart geometries. One or more attributes can be specified to collect only geometries belonging to the same class (having the same value for the specified attributes), alternatively all geometries can be collected.
All output geometries will be converted to multi geometries, even those with just a single part. This algorithm does not dissolve overlapping geometries - they will be collected together without modifying the shape of each geometry part.
See the 'Promote to multipart' or 'Aggregate' algorithms for alternative options.
Parameters:
- INPUT [source]: Input layer
- FIELD [field]: Unique ID fields (optional)
- OUTPUT [sink]: Collected
Outputs: OUTPUT [outputVector]

### native:concavehull: Concave hull (by layer)
This algorithm computes the concave hull covering all features from an input point layer.
See the 'Concave hull (by feature)' algorithm for a concave hull calculation which covers individual features from a layer.
Parameters:
- INPUT [source]: Input layer
- ALPHA [number]: Threshold (0-1, where 1 is equivalent with Convex Hull) (default 0.3)
- HOLES [boolean]: Allow holes (default True)
- NO_MULTIGEOMETRY [boolean]: Split multipart geometry into singleparts (default False)
- OUTPUT [sink]: Concave hull
Outputs: OUTPUT [outputVector]

### native:concavehullbyfeature: Concave hull (by feature)
This algorithm calculates the concave hull for each feature in an input layer.
A concave hull is a polygon which contains all the points of the input geometries, but is a better approximation than the convex hull to the area occupied by the input.
It is frequently used to convert a multi-point into a polygonal area which contains all the points from the input geometry.
See the 'Concave hull (by layer)' algorithm for a concave hull calculation which covers the whole layer or grouped subsets of features.
Parameters:
- INPUT [source]: Input layer
- ALPHA [number]: Threshold (0-1, where 1 is equivalent with Convex Hull) (default 0.3)
- HOLES [boolean]: Allow holes (default True)
- OUTPUT [sink]: Concave hulls
Outputs: OUTPUT [outputVector]

### native:convertgeometrytype: Convert geometry type
This algorithm generates a new layer based on an existing one, with a different type of geometry.
Not all conversions are possible. For instance, a line layer can be converted to a point layer, but a point layer cannot be converted to a line layer.
See the "Polygonize" or "Lines to polygons" algorithms for alternative options.
Parameters:
- INPUT [source]: Input layer
- TYPE [enum]: New geometry type (options 0=Centroids, 1=Nodes, 2=Linestrings, 3=Multilinestrings, 4=Polygons)
- OUTPUT [sink]: Converted
Outputs: OUTPUT [outputVector]

### native:converttocurves: Convert to curved geometries
This algorithm converts a geometry into its curved geometry equivalent.
Already curved geometries will be retained without change.
Parameters:
- INPUT [source]: Input layer
- DISTANCE [number]: Maximum distance tolerance (default 1e-06)
- ANGLE [number]: Maximum angle tolerance (default 1e-06)
- OUTPUT [sink]: Curves
Outputs: OUTPUT [outputVector]

### native:convexhull: Convex hull
This algorithm calculates the convex hull for each feature in an input layer.
See the 'Minimum bounding geometry' algorithm for a convex hull calculation which covers the whole layer or grouped subsets of features.
Parameters:
- INPUT [source]: Input layer
- OUTPUT [sink]: Convex hulls
Outputs: OUTPUT [outputVector]

### native:delaunaytriangulation: Delaunay triangulation
This algorithm creates a polygon layer with the Delaunay triangulation corresponding to a points layer.
Parameters:
- INPUT [source]: Input layer
- TOLERANCE [number]: Tolerance (optional; default 0)
- ADD_ATTRIBUTES [boolean]: Add point IDs to output (default True)
- OUTPUT [sink]: Delaunay triangulation
Outputs: OUTPUT [outputVector]

### native:deleteholes: Delete holes
This algorithm takes a polygon layer and removes holes in polygons. It creates a new vector layer in which polygons with holes have been replaced by polygons with only their external ring. Attributes are not modified.
An optional minimum area parameter allows removing only holes which are smaller than a specified area threshold. Leaving this parameter as 0.0 results in all holes being removed.
Parameters:
- INPUT [source]: Input layer
- MIN_AREA [area]: Remove holes with area less than (default 0.0)
- OUTPUT [sink]: Cleaned
Outputs: OUTPUT [outputVector]

### native:densifygeometries: Densify by count
This algorithm takes a polygon or line layer and generates a new one in which the geometries have a larger number of vertices than the original one.
If the geometries have z or m values present then these will be linearly interpolated at the added nodes.
The number of new vertices to add to each feature geometry is specified as an input parameter.
Parameters:
- INPUT [source]: Input layer
- VERTICES [number]: Number of vertices to add (default 1)
- OUTPUT [sink]: Densified
Outputs: OUTPUT [outputVector]

### native:densifygeometriesgivenaninterval: Densify by interval
This algorithm takes a polygon or line layer and generates a new one in which the geometries have a larger number of vertices than the original one.
Geometries are densified by adding additional vertices on edges that have a maximum distance of the interval parameter in map units.
Parameters:
- INPUT [source]: Input layer
- INTERVAL [distance]: Interval between vertices to add (default 1)
- OUTPUT [sink]: Densified
Outputs: OUTPUT [outputVector]

### native:dissolve: Dissolve
This algorithm takes a vector layer and combines their features into new features. One or more attributes can be specified to dissolve features belonging to the same class (having the same value for the specified attributes), alternatively all features can be dissolved in a single one.
All output geometries will be converted to multi geometries. In case the input is a polygon layer, common boundaries of adjacent polygons being dissolved will get erased.
If enabled, the optional "Keep disjoint features separate" setting will cause features and parts that do not overlap or touch to be exported as separate features (instead of parts of a single multipart feature).
Parameters:
- INPUT [source]: Input layer
- FIELD [field]: Dissolve field(s) (optional)
- SEPARATE_DISJOINT [boolean]: Keep disjoint features separate (default False)
- OUTPUT [sink]: Dissolved
Outputs: OUTPUT [outputVector]

### native:dropmzvalues: Drop M/Z values
This algorithm can remove any measure (M) or Z values from input geometries.
Parameters:
- INPUT [source]: Input layer
- DROP_M_VALUES [boolean]: Drop M Values (default False)
- DROP_Z_VALUES [boolean]: Drop Z Values (default False)
- OUTPUT [sink]: Z/M Dropped
Outputs: OUTPUT [outputVector]

### native:explodelines: Explode lines
This algorithm takes a lines layer and creates a new one in which each line is replaced by a set of lines representing the segments in the original line. Each line in the resulting layer contains only a start and an end point, with no intermediate nodes between them.
If the input layer consists of CircularStrings or CompoundCurves, the output layer will be of the same type and contain only single curve segments.
Parameters:
- INPUT [source]: Input layer
- OUTPUT [sink]: Exploded
Outputs: OUTPUT [outputVector]

### native:exportaddgeometrycolumns: Add geometry attributes
This algorithm computes geometric properties of the features in a vector layer. The algorithm generates a new vector layer with the same content as the input one, but with additional attributes in its attributes table, containing geometric measurements.
Depending on the geometry type of the vector layer, the attributes added to the table will be different.
Parameters:
- INPUT [source]: Input layer
- METHOD [enum]: Calculate using (default 0; options 0=Cartesian Calculations in Layer's CRS, 1=Cartesian Calculations in Project's CRS, 2=Ellipsoidal Calculations)
- OUTPUT [sink]: Added geometry info
Outputs: OUTPUT [outputVector]

### native:extendlines: Extend lines
This algorithm extends line geometries by a specified amount at the start and end of the line. Lines are extended using the bearing of the first and last segment in the line.
Parameters:
- INPUT [source]: Input layer
- START_DISTANCE [distance]: Start distance (default 0.0)
- END_DISTANCE [distance]: End distance (default 0.0)
- OUTPUT [sink]: Extended
Outputs: OUTPUT [outputVector]

### native:extractmvalues: Extract M values
Extracts m values from geometries into feature attributes.
By default only the m value from the first vertex of each feature is extracted, however the algorithm can optionally calculate statistics on all of the geometry's m values, including sums, means, and minimums and maximums
Parameters:
- INPUT [source]: Input layer
- SUMMARIES [enum]: Summaries to calculate (default [0]; options 0=First, 1=Last, 2=Count, 3=Sum, 4=Mean, 5=Median, 6=St dev (pop), 7=Minimum, 8=Maximum, 9=Range, 10=Minority, 11=Majority, 12=Variety, 13=Q1, 14=Q3, 15=IQR)
- COLUMN_PREFIX [string]: Output column prefix (optional; default m_)
- OUTPUT [sink]: Extracted
Outputs: OUTPUT [outputVector]

### native:extractspecificvertices: Extract specific vertices
This algorithm takes a vector layer and generates a point layer with points representing specific vertices in the input geometries. For instance, this algorithm can be used to extract the first or last vertices in the geometry. The attributes associated to each point are the same ones associated to the feature that the point belongs to.
The vertex indices parameter accepts a comma separated string specifying the indices of the vertices to extract. The first vertex corresponds to an index of 0, the second vertex has an index of 1, etc. Negative indices can be used to find vertices at the end of the geometry, e.g., an index of -1 corresponds to the last vertex, -2 corresponds to the second last vertex, etc.
Additional fields are added to the points indicating the specific vertex position (e.g., 0, -1, etc), the original vertex index, the vertex’s part and its index within the part (as well as its ring for polygons), distance along the original geometry and bisector angle of vertex for the original geometry.
Parameters:
- INPUT [source]: Input layer
- VERTICES [string]: Vertex indices (default 0)
- OUTPUT [sink]: Vertices
Outputs: OUTPUT [outputVector]

### native:extractvertices: Extract vertices
This algorithm takes a vector layer and generates a point layer with points representing the vertices of the input geometries. The attributes associated to each point are the same ones associated to the feature that the point belongs to.
Additional fields are added to the point indicating the vertex index (beginning at 0), the vertex’s part and its index within the part (as well as its ring for polygons), distance along original geometry and bisector angle of vertex for original geometry.
Parameters:
- INPUT [source]: Input layer
- OUTPUT [sink]: Vertices
Outputs: OUTPUT [outputVector]

### native:extractzvalues: Extract Z values
Extracts z values from geometries into feature attributes.
By default only the z value from the first vertex of each feature is extracted, however the algorithm can optionally calculate statistics on all of the geometry's z values, including sums, means, and minimums and maximums
Parameters:
- INPUT [source]: Input layer
- SUMMARIES [enum]: Summaries to calculate (default [0]; options 0=First, 1=Last, 2=Count, 3=Sum, 4=Mean, 5=Median, 6=St dev (pop), 7=Minimum, 8=Maximum, 9=Range, 10=Minority, 11=Majority, 12=Variety, 13=Q1, 14=Q3, 15=IQR)
- COLUMN_PREFIX [string]: Output column prefix (optional; default z_)
- OUTPUT [sink]: Extracted
Outputs: OUTPUT [outputVector]

### native:filterverticesbym: Filter vertices by M value
Filters away vertices based on their m-value, returning geometries with only vertex points that have a m-value ≥ the specified minimum value and ≤ the maximum value.
If the minimum value is not specified then only the maximum value is tested, and similarly if the maximum value is not specified then only the minimum value is tested.
Depending on the input geometry attributes and the filters used, the resultant geometries created by this algorithm may no longer be valid.
Parameters:
- INPUT [source]: Input layer
- MIN [number]: Minimum (optional)
- MAX [number]: Maximum (optional)
- OUTPUT [sink]: Filtered
Outputs: OUTPUT [outputVector]

### native:filterverticesbyz: Filter vertices by Z value
Filters away vertices based on their z-value, returning geometries with only vertex points that have a z-value ≥ the specified minimum value and ≤ the maximum value.
If the minimum value is not specified then only the maximum value is tested, and similarly if the maximum value is not specified then only the minimum value is tested.
Depending on the input geometry attributes and the filters used, the resultant geometries created by this algorithm may no longer be valid.
Parameters:
- INPUT [source]: Input layer
- MIN [number]: Minimum (optional)
- MAX [number]: Maximum (optional)
- OUTPUT [sink]: Filtered
Outputs: OUTPUT [outputVector]

### native:fixgeometries: Fix geometries
This algorithm attempts to create a valid representation of a given invalid geometry without losing any of the input vertices. Already-valid geometries are returned without further intervention. Always outputs multi-geometry layer.
NOTE: M values will be dropped from the output.
Parameters:
- INPUT [source]: Input layer
- METHOD [enum]: Repair method (default 1; options 0=Linework, 1=Structure)
- OUTPUT [sink]: Fixed geometries
Outputs: OUTPUT [outputVector]

### native:forcerhr: Force right-hand-rule
This algorithm forces polygon geometries to respect the Right-Hand-Rule, in which the area that is bounded by a polygon is to the right of the boundary. In particular, the exterior ring is oriented in a clockwise direction and the interior rings in a counter-clockwise direction.
Parameters:
- INPUT [source]: Input layer
- OUTPUT [sink]: Reoriented
Outputs: OUTPUT [outputVector]

### native:geometrybyexpression: Geometry by expression
This algorithm updates existing geometries (or creates new geometries) for input features by use of a QGIS expression. This allows complex geometry modifications which can utilize all the flexibility of the QGIS expression engine to manipulate and create geometries for output features.
For help with QGIS expression functions, see the inbuilt help for specific functions which is available in the expression builder.
Parameters:
- INPUT [source]: Input layer
- OUTPUT_GEOMETRY [enum]: Output geometry type (default 0; options 0=Polygon, 1=Line, 2=Point)
- WITH_Z [boolean]: Output geometry has z dimension (default False)
- WITH_M [boolean]: Output geometry has m values (default False)
- EXPRESSION [expression]: Geometry expression (default @geometry)
- OUTPUT [sink]: Modified geometry
Outputs: OUTPUT [outputVector]

### native:interpolatepoint: Interpolate point on line
This algorithm creates a point geometry interpolated at a set distance along line or curve geometries.
Z and M values are linearly interpolated from existing values.
If a multipart geometry is encountered, only the first part is considered when interpolating the point.
If the specified distance is greater than the curve's length, the resultant feature will have a null geometry.
Parameters:
- INPUT [source]: Input layer
- DISTANCE [distance]: Distance (default 0.0)
- OUTPUT [sink]: Interpolated points
Outputs: OUTPUT [outputVector]

### native:keepnbiggestparts: Keep N biggest parts
This algorithm takes a polygon layer and creates a new polygon layer in which multipart geometries have been removed, leaving only the n largest (in terms of area) parts.
Parameters:
- POLYGONS [source]: Input layer
- PARTS [number]: Parts to keep (default 1.0)
- OUTPUT [sink]: Parts
Outputs: OUTPUT [outputVector]

### native:linesubstring: Line substring
This algorithm returns the portion of a line (or curve) which falls between the specified start and end distances (measured from the beginning of the line).
Z and M values are linearly interpolated from existing values.
If a multipart geometry is encountered, only the first part is considered when calculating the substring.
Parameters:
- INPUT [source]: Input layer
- START_DISTANCE [distance]: Start distance (default 0.0)
- END_DISTANCE [distance]: End distance (default 1.0)
- OUTPUT [sink]: Substring
Outputs: OUTPUT [outputVector]

### native:mergelines: Merge lines
This algorithm joins all connected parts of MultiLineString geometries into single LineString geometries.
If any parts of the input MultiLineString geometries are not connected, the resultant geometry will be a MultiLineString containing any lines which could be merged and any non-connected line parts.
Parameters:
- INPUT [source]: Input layer
- OUTPUT [sink]: Merged
Outputs: OUTPUT [outputVector]

### native:minimumenclosingcircle: Minimum enclosing circles
This algorithm calculates the minimum enclosing circle which covers each feature in an input layer.
See the 'Minimum bounding geometry' algorithm for a minimal enclosing circle calculation which covers the whole layer or grouped subsets of features.
Parameters:
- INPUT [source]: Input layer
- SEGMENTS [number]: Number of segments in circles (default 72)
- OUTPUT [sink]: Minimum enclosing circles
Outputs: OUTPUT [outputVector]

### native:multiparttosingleparts: Multipart to singleparts
This algorithm takes a vector layer with multipart geometries and generates a new one in which all geometries contain a single part. Features with multipart geometries are divided in as many different features as parts the geometry contain, and the same attributes are used for each of them.
Parameters:
- INPUT [source]: Input layer
- OUTPUT [sink]: Single parts
Outputs: OUTPUT [outputVector]

### native:multiringconstantbuffer: Multi-ring buffer (constant distance)
This algorithm computes multi-ring ('donuts') buffer for the features in an input layer, using a fixed or dynamic distance and number of rings.
Parameters:
- INPUT [source]: Input layer
- RINGS [number]: Number of rings (default 1)
- DISTANCE [distance]: Distance between rings (default 1)
- OUTPUT [sink]: Multi-ring buffer (constant distance)
Outputs: OUTPUT [outputVector]

### native:offsetline: Offset lines
This algorithm offsets lines by a specified distance. Positive distances will offset lines to the left, and negative distances will offset to the right of lines.
The segments parameter controls the number of line segments to use to approximate a quarter circle when creating rounded offsets.
The join style parameter specifies whether round, miter or beveled joins should be used when offsetting corners in a line.
The miter limit parameter is only applicable for miter join styles, and controls the maximum distance from the offset curve to use when creating a mitered join.
Parameters:
- INPUT [source]: Input layer
- DISTANCE [distance]: Distance (default 10.0)
- SEGMENTS [number]: Segments (default 8)
- JOIN_STYLE [enum]: Join style (default 0; options 0=Round, 1=Miter, 2=Bevel)
- MITER_LIMIT [number]: Miter limit (default 2)
- OUTPUT [sink]: Offset
Outputs: OUTPUT [outputVector]

### native:orientedminimumboundingbox: Oriented minimum bounding box
This algorithm calculates the minimum area rotated rectangle which covers each feature in an input layer.
For singlepart point features, the output corresponds to the bounding box of the geometry.
See the 'Minimum bounding geometry' algorithm for an oriented bounding box calculation which covers the whole layer or grouped subsets of features.
Parameters:
- INPUT [source]: Input layer
- OUTPUT [sink]: Bounding boxes
Outputs: OUTPUT [outputVector]

### native:orthogonalize: Orthogonalize
Takes a line or polygon layer and attempts to orthogonalize all the geometries in the layer. This process shifts the nodes in the geometries to try to make every angle in the geometry either a right angle or a straight line.
The angle tolerance parameter is used to specify the maximum deviation from a right angle or straight line a node can have for it to be adjusted. Smaller tolerances mean that only nodes which are already closer to right angles will be adjusted, and larger tolerances mean that nodes which deviate further from right angles will also be adjusted.
The algorithm is iterative. Setting a larger number for the maximum iterations will result in a more orthogonal geometry at the cost of extra processing time.
Parameters:
- INPUT [source]: Input layer
- ANGLE_TOLERANCE [number]: Maximum angle tolerance (degrees) (default 15.0)
- MAX_ITERATIONS [number]: Maximum algorithm iterations (default 1000)
- OUTPUT [sink]: Orthogonalized
Outputs: OUTPUT [outputVector]

### native:pointonsurface: Point on surface
This algorithm returns a point guaranteed to lie on the surface of a geometry.
Parameters:
- INPUT [source]: Input layer
- ALL_PARTS [boolean]: Create point on surface for each part (default False)
- OUTPUT [sink]: Point
Outputs: OUTPUT [outputVector]

### native:pointsalonglines: Points along geometry
This algorithm creates a points layer, with points distributed along the lines of an input vector layer. The distance between points (measured along the line) is defined as a parameter.
Start and end offset distances can be defined, so the first and last point will not fall exactly on the line's first and last nodes. These start and end offsets are defined as distances, measured along the line from the first and last nodes of the lines.
Parameters:
- INPUT [source]: Input layer
- DISTANCE [distance]: Distance (default 1.0)
- START_OFFSET [distance]: Start offset (default 0.0)
- END_OFFSET [distance]: End offset (default 0.0)
- OUTPUT [sink]: Interpolated points
Outputs: OUTPUT [outputVector]

### native:poleofinaccessibility: Pole of inaccessibility
This algorithm calculates the pole of inaccessibility for a polygon layer, which is the most distant internal point from the boundary of the surface. This algorithm uses the 'polylabel' algorithm (Vladimir Agafonkin, 2016), which is an iterative approach guaranteed to find the true pole of inaccessibility within a specified tolerance (in layer units). More precise tolerances require more iterations and will take longer to calculate.
The distance from the calculated pole to the polygon boundary will be stored as a new attribute in the output layer.
Parameters:
- INPUT [source]: Input layer
- TOLERANCE [distance]: Tolerance (default 1.0)
- OUTPUT [sink]: Point
Outputs: OUTPUT [outputVector]

### native:polygonize: Polygonize
This algorithm creates a polygon layer from the input lines layer.
Parameters:
- INPUT [source]: Input layer
- KEEP_FIELDS [boolean]: Keep table structure of line layer (default False)
- OUTPUT [sink]: Polygons
Outputs: OUTPUT [outputVector], NUM_POLYGONS [outputNumber]

### native:polygonstolines: Polygons to lines
This algorithm converts polygons to lines.
Parameters:
- INPUT [source]: Input layer
- OUTPUT [sink]: Lines
Outputs: OUTPUT [outputVector]

### native:projectpointcartesian: Project points (Cartesian)
This algorithm projects point geometries by a specified distance and bearing (azimuth), creating a new point layer with the projected points.
The distance is specified in layer units, and the bearing in degrees clockwise from North.
Parameters:
- INPUT [source]: Input layer
- BEARING [number]: Bearing (degrees from North) (default 0)
- DISTANCE [distance]: Distance (default 1)
- OUTPUT [sink]: Projected
Outputs: OUTPUT [outputVector]

### native:promotetomulti: Promote to multipart
This algorithm takes a vector layer with singlepart geometries and generates a new one in which all geometries are multipart. Input features which are already multipart features will remain unchanged.
This algorithm can be used to force geometries to multipart types in order to be compatible with data providers with strict singlepart/multipart compatibility checks.
See the 'Collect geometries' or 'Aggregate' algorithms for alternative options.
Parameters:
- INPUT [source]: Input layer
- OUTPUT [sink]: Multiparts
Outputs: OUTPUT [outputVector]

### native:rectanglesovalsdiamonds: Rectangles, ovals, diamonds
This algorithm creates rectangle, oval or diamond-shaped polygons from the input point layer using specified width, height and (optional) rotation values. Multipart inputs should be promoted to singleparts first.
Parameters:
- INPUT [source]: Input layer
- SHAPE [enum]: Shape (default 0; options 0=Rectangle, 1=Diamond, 2=Oval)
- WIDTH [distance]: Width (default 1.0)
- HEIGHT [distance]: Height (default 1.0)
- ROTATION [number]: Rotation (optional; default 0.0)
- SEGMENTS [number]: Segments (default 36)
- OUTPUT [sink]: Polygon
Outputs: OUTPUT [outputVector]

### native:removeduplicatevertices: Remove duplicate vertices
This algorithm removes duplicate vertices from features, wherever removing the vertices does not result in a degenerate geometry.
The tolerance parameter specifies the tolerance for coordinates when determining whether vertices are identical.
By default, z values are not considered when detecting duplicate vertices. E.g. two vertices with the same x and y coordinate but different z values will still be considered duplicate and one will be removed. If the Use Z Value parameter is true, then the z values are also tested and vertices with the same x and y but different z will be maintained.
Note that duplicate vertices are not tested between different parts of a multipart geometry. E.g. a multipoint geometry with overlapping points will not be changed by this method.
Parameters:
- INPUT [source]: Input layer
- TOLERANCE [distance]: Tolerance (default 1e-06)
- USE_Z_VALUE [boolean]: Use Z Value (default False)
- OUTPUT [sink]: Cleaned
Outputs: OUTPUT [outputVector]

### native:removenullgeometries: Remove null geometries
This algorithm removes any features which do not have a geometry from a vector layer. All other features will be copied unchanged.
Optionally, the features with null geometries can be saved to a separate output.
If 'Also remove empty geometries' is checked, the algorithm removes features whose geometries have no coordinates, i.e., geometries that are empty. In that case, also the null output will reflect this option, containing both null and empty geometries.
Parameters:
- INPUT [source]: Input layer
- REMOVE_EMPTY [boolean]: Also remove empty geometries (default False)
- OUTPUT [sink]: Non null geometries (optional)
- NULL_OUTPUT [sink]: Null geometries (optional)
Outputs: OUTPUT [outputVector], NULL_OUTPUT [outputVector]

### native:reverselinedirection: Reverse line direction
This algorithm reverses the direction of curve or LineString geometries.
Parameters:
- INPUT [source]: Input layer
- OUTPUT [sink]: Reversed
Outputs: OUTPUT [outputVector]

### native:rotatefeatures: Rotate
This algorithm rotates feature geometries by the specified angle clockwise.
Optionally, the rotation can occur around a preset point. If not set the rotation occurs around each feature's centroid.
Parameters:
- INPUT [source]: Input layer
- ANGLE [number]: Rotation (degrees clockwise) (default 0.0)
- ANCHOR [point]: Rotation anchor point (optional)
- OUTPUT [sink]: Rotated
Outputs: OUTPUT [outputVector]

### native:roundness: Roundness
Calculates the roundness of each feature and stores it as a new field. The input vector layer must contain polygons.
The roundness of a polygon is defined as 4π × polygon area / perimeter². The roundness value varies between 0 and 1. A perfect circle has a roundness of 1, while a completely flat polygon has a roundness of 0.
Parameters:
- INPUT [source]: Input layer
- OUTPUT [sink]: Roundness
Outputs: OUTPUT [outputVector]

### native:segmentizebymaxangle: Segmentize by maximum angle
This algorithm segmentizes a geometry by converting curved sections to linear sections.
The segmentization is performed by specifying the maximum allowed radius angle between vertices on the straightened geometry (e.g the angle of the arc created from the original arc center to consecutive output vertices on the linearized geometry).
Non-curved geometries will be retained without change.
Parameters:
- INPUT [source]: Input layer
- ANGLE [number]: Maximum angle between vertices (degrees) (default 5.0)
- OUTPUT [sink]: Segmentized
Outputs: OUTPUT [outputVector]

### native:segmentizebymaxdistance: Segmentize by maximum distance
This algorithm segmentizes a geometry by converting curved sections to linear sections.
The segmentization is performed by specifying the maximum allowed offset distance between the original curve and the segmentized representation.
Non-curved geometries will be retained without change.
Parameters:
- INPUT [source]: Input layer
- DISTANCE [distance]: Maximum offset distance (default 1.0)
- OUTPUT [sink]: Segmentized
Outputs: OUTPUT [outputVector]

### native:setmfromraster: Set M value from raster
This algorithm sets the M value for every vertex in the feature geometry to a value sampled from a band within a raster layer.
The raster values can optionally be scaled by a preset amount and an offset can be algebraically added.
Parameters:
- INPUT [source]: Input layer
- RASTER [raster]: Raster layer
- BAND [band]: Band number (default 1)
- NODATA [number]: Value for NoData or non-intersecting vertices (default 0.0)
- SCALE [number]: Scale factor (default 1.0)
- OFFSET [number]: Offset (default 0.0)
- OUTPUT [sink]: Draped
Outputs: OUTPUT [outputVector]

### native:setmvalue: Set M value
This algorithm sets the M value for geometries in a layer.
If M values already exist in the layer, they will be overwritten with the new value. If no M values exist, the geometry will be upgraded to include M values and the specified value used as the initial M value for all geometries.
Parameters:
- INPUT [source]: Input layer
- M_VALUE [number]: M Value (default 0.0)
- OUTPUT [sink]: M Added
Outputs: OUTPUT [outputVector]

### native:setzfromraster: Drape (set Z value from raster)
This algorithm sets the z value of every vertex in the feature geometry to a value sampled from a band within a raster layer.
The raster values can optionally be scaled by a preset amount and an offset can be algebraically added.
Parameters:
- INPUT [source]: Input layer
- RASTER [raster]: Raster layer
- BAND [band]: Band number (default 1)
- NODATA [number]: Value for NoData or non-intersecting vertices (default 0.0)
- SCALE [number]: Scale factor (default 1.0)
- OFFSET [number]: Offset (default 0.0)
- OUTPUT [sink]: Draped
Outputs: OUTPUT [outputVector]

### native:setzvalue: Set Z value
This algorithm sets the Z value for geometries in a layer.
If Z values already exist in the layer, they will be overwritten with the new value. If no Z values exist, the geometry will be upgraded to include Z values and the specified value used as the initial Z value for all geometries.
Parameters:
- INPUT [source]: Input layer
- Z_VALUE [number]: Z Value (default 0.0)
- OUTPUT [sink]: Z Added
Outputs: OUTPUT [outputVector]

### native:simplifygeometries: Simplify
This algorithm simplifies the geometries in a line or polygon layer. It creates a new layer with the same features as the ones in the input layer, but with geometries containing a lower number of vertices.
The algorithm gives a choice of simplification methods, including distance based (the "Douglas-Peucker" algorithm), area based ("Visvalingam" algorithm) and snapping geometries to a grid.
Parameters:
- INPUT [source]: Input layer
- METHOD [enum]: Simplification method (default 0; options 0=Distance (Douglas-Peucker), 1=Snap to grid, 2=Area (Visvalingam))
- TOLERANCE [distance]: Tolerance (default 1.0)
- OUTPUT [sink]: Simplified
Outputs: OUTPUT [outputVector]

### native:singlesidedbuffer: Single sided buffer
This algorithm buffers lines by a specified distance on one side of the line only.
The segments parameter controls the number of line segments to use to approximate a quarter circle when creating rounded buffers. The join style parameter specifies whether round, miter or beveled joins should be used when buffering corners in a line. The miter limit parameter is only applicable for miter join styles, and controls the maximum distance from the buffer to use when creating a mitered join.
Parameters:
- INPUT [source]: Input layer
- DISTANCE [distance]: Distance (default 10)
- SIDE [enum]: Side (default 0; options 0=Left, 1=Right)
- SEGMENTS [number]: Segments (default 8)
- JOIN_STYLE [enum]: Join style (default 0; options 0=Round, 1=Miter, 2=Bevel)
- MITER_LIMIT [number]: Miter limit (default 2)
- OUTPUT [sink]: Buffered
Outputs: OUTPUT [outputVector]

### native:smoothgeometry: Smooth
This algorithm smooths the geometries in a line or polygon layer. It creates a new layer with the same features as the ones in the input layer, but with geometries containing a higher number of vertices and corners in the geometries smoothed out.
The iterations parameter dictates how many smoothing iterations will be applied to each geometry. A higher number of iterations results in smoother geometries with the cost of greater number of nodes in the geometries.
The offset parameter controls how "tightly" the smoothed geometries follow the original geometries. Smaller values results in a tighter fit, and larger values will create a looser fit.
The maximum angle parameter can be used to prevent smoothing of nodes with large angles. Any node where the angle of the segments to either side is larger than this will not be smoothed. For example, setting the maximum angle to 90 degrees or lower would preserve right angles in the geometry.
If input geometries contain Z or M values, these will also be smoothed and the output geometry will retain the same dimensionality as the input geometry.
Parameters:
- INPUT [source]: Input layer
- ITERATIONS [number]: Iterations (default 1)
- OFFSET [number]: Offset (default 0.25)
- MAX_ANGLE [number]: Maximum node angle to smooth (default 180.0)
- OUTPUT [sink]: Smoothed
Outputs: OUTPUT [outputVector]

### native:snapgeometries: Snap geometries to layer
This algorithm snaps the geometries in a layer. Snapping can be done either to the geometries from another layer, or to geometries within the same layer.
A tolerance is specified in layer units to control how close vertices need to be to the reference layer geometries before they are snapped.
Snapping occurs to both nodes and edges. Depending on the snapping behavior, either nodes or edges will be preferred.
Vertices will be inserted or removed as required to make the geometries match the reference geometries.
Parameters:
- INPUT [source]: Input layer
- REFERENCE_LAYER [source]: Reference layer
- TOLERANCE [distance]: Tolerance (default 10.0)
- BEHAVIOR [enum]: Behavior (default [0]; options 0=Prefer aligning nodes, insert extra vertices where required, 1=Prefer closest point, insert extra vertices where required, 2=Prefer aligning nodes, don't insert new vertices, 3=Prefer closest point, don't insert new vertices, 4=Move end points only, prefer aligning nodes, 5=Move end points only, prefer closest point, 6=Snap end points to end points only, 7=Snap to anchor nodes (single layer only))
- OUTPUT [sink]: Snapped geometry
Outputs: OUTPUT [outputVector]

### native:snappointstogrid: Snap points to grid
This algorithm modifies the coordinates of geometries in a vector layer, so that all points or vertices are snapped to the closest point of the grid.
If the snapped geometry cannot be calculated (or is totally collapsed) the feature's geometry will be cleared.
Note that snapping to grid may generate an invalid geometry in some corner cases.
Snapping can be performed on the X, Y, Z or M axis. A grid spacing of 0 for any axis will disable snapping for that axis.
Parameters:
- INPUT [source]: Input layer
- HSPACING [distance]: X Grid Spacing (default 1)
- VSPACING [distance]: Y Grid Spacing (default 1)
- ZSPACING [number]: Z Grid Spacing (default 0)
- MSPACING [number]: M Grid Spacing (default 0)
- OUTPUT [sink]: Snapped
Outputs: OUTPUT [outputVector]

### native:splitlinesbylength: Split lines by maximum length
This algorithm takes a line (or curve) layer and splits each feature into multiple parts, where each part is of a specified maximum length.
Z and M values at the start and end of the new line substrings are linearly interpolated from existing values.
Parameters:
- INPUT [source]: Input layer
- LENGTH [distance]: Maximum line length (default 10)
- OUTPUT [sink]: Split
Outputs: OUTPUT [outputVector]

### native:subdivide: Subdivide
This algorithm subdivides the geometry. The returned geometry will be a collection containing subdivided parts from the original geometry, where no part has more than the specified maximum number of nodes.
This is useful for dividing a complex geometry into less complex parts, which are better able to be spatially indexed and faster to perform further operations such as intersects on. The returned geometry parts may not be valid and may contain self-intersections.
Curved geometries will be segmentized before subdivision.
Parameters:
- INPUT [source]: Input layer
- MAX_NODES [number]: Maximum nodes in parts (default 256)
- OUTPUT [sink]: Subdivided
Outputs: OUTPUT [outputVector]

### native:swapxy: Swap X and Y coordinates
This algorithm swaps the X and Y coordinate values in input geometries. It can be used to repair geometries which have accidentally had their latitude and longitude values reversed.
Parameters:
- INPUT [source]: Input layer
- OUTPUT [sink]: Swapped
Outputs: OUTPUT [outputVector]

### native:taperedbuffer: Tapered buffers
This algorithm creates tapered buffers along line geometries, using a specified start and end buffer diameter corresponding to the buffer diameter at the start and end of the linestrings.
Parameters:
- INPUT [source]: Input layer
- START_WIDTH [number]: Start width (default 0.0)
- END_WIDTH [number]: End width (default 1)
- SEGMENTS [number]: Segments (default 16)
- OUTPUT [sink]: Buffered
Outputs: OUTPUT [outputVector]

### native:transect: Transect
This algorithm creates transects on vertices for (multi)linestrings.
A transect is a line oriented from an angle (by default perpendicular) to the input polylines (at vertices).
Field(s) from feature(s) are returned in the transect with these new fields:
- TR_FID: ID of the original feature
- TR_ID: ID of the transect. Each transect have an unique ID
- TR_SEGMENT: ID of the segment of the linestring
- TR_ANGLE: Angle in degrees from the original line at the vertex
- TR_LENGTH: Total length of the transect returned
- TR_ORIENT: Side of the transect (only on the left or right of the line, or both side)
Parameters:
- INPUT [source]: Input layer
- LENGTH [distance]: Length of the transect (default 5.0)
- ANGLE [number]: Angle in degrees from the original line at the vertices (default 90.0)
- SIDE [enum]: Side to create the transects (options 0=Left, 1=Right, 2=Both)
- OUTPUT [sink]: Transect
Outputs: OUTPUT [outputVector]

### native:translategeometry: Translate
This algorithm moves the geometries within a layer, by offsetting them with a specified x and y displacement.
Z and M values present in the geometry can also be translated.
Parameters:
- INPUT [source]: Input layer
- DELTA_X [distance]: Offset distance (x-axis) (default 0.0)
- DELTA_Y [distance]: Offset distance (y-axis) (default 0.0)
- DELTA_Z [number]: Offset distance (z-axis) (default 0.0)
- DELTA_M [number]: Offset distance (m values) (default 0.0)
- OUTPUT [sink]: Translated
Outputs: OUTPUT [outputVector]

### native:voronoipolygons: Voronoi polygons
This algorithm generates a polygon layer containing the Voronoi diagram corresponding to input points.
Parameters:
- INPUT [source]: Input layer
- BUFFER [number]: Buffer region (% of extent) (default 0)
- TOLERANCE [number]: Tolerance (optional; default 0)
- COPY_ATTRIBUTES [boolean]: Copy attributes from input features (default True)
- OUTPUT [sink]: Voronoi polygons
Outputs: OUTPUT [outputVector]

### native:wedgebuffers: Create wedge buffers
This algorithm creates wedge shaped buffers from input points.
The azimuth parameter gives the angle (in degrees) for the middle of the wedge to point. The buffer width (in degrees) is specified by the width parameter. Note that the wedge will extend to half of the angular width either side of the azimuth direction.
The outer radius of the buffer is specified via outer radius, and optionally an inner radius can also be specified.
The native output from this algorithm are CurvePolygon geometries, but these may be automatically segmentized to Polygons depending on the output format.
Parameters:
- INPUT [source]: Input layer
- AZIMUTH [number]: Azimuth (degrees from North) (default 0)
- WIDTH [number]: Wedge width (in degrees) (default 45)
- OUTER_RADIUS [number]: Outer radius (default 1)
- INNER_RADIUS [number]: Inner radius (optional; default 0)
- OUTPUT [sink]: Buffers
Outputs: OUTPUT [outputVector]


## QGIS (native c++) / Vector overlay

### native:clip: Clip
This algorithm clips a vector layer using the features of an additional polygon layer. Only the parts of the features in the Input layer that fall within the polygons of the Overlay layer will be added to the resulting layer.
The attributes of the features are not modified, although properties such as area or length of the features will be modified by the clipping operation. If such properties are stored as attributes, those attributes will have to be manually updated.
Parameters:
- INPUT [source]: Input layer
- OVERLAY [source]: Overlay layer
- OUTPUT [sink]: Clipped
Outputs: OUTPUT [outputVector]

### native:difference: Difference
This algorithm extracts features from the Input layer that fall outside, or partially overlap, features in the Overlay layer. Input layer features that partially overlap feature(s) in the Overlay layer are split along those features' boundary and only the portions outside the Overlay layer features are retained.
Attributes are not modified, although properties such as area or length of the features will be modified by the difference operation. If such properties are stored as attributes, those attributes will have to be manually updated.
Parameters:
- INPUT [source]: Input layer
- OVERLAY [source]: Overlay layer
- OUTPUT [sink]: Difference
- GRID_SIZE [number]: Grid size (optional)
Outputs: OUTPUT [outputVector]

### native:extractbyextent: Extract/clip by extent
This algorithm creates a new vector layer that only contains features which fall within a specified extent. Any features which intersect the extent will be included.
Optionally, feature geometries can also be clipped to the extent. If this option is selected, then the output geometries will automatically be converted to multi geometries to ensure uniform output geometry types.
Parameters:
- INPUT [source]: Input layer
- EXTENT [extent]: Extent
- CLIP [boolean]: Clip features to extent (default False)
- OUTPUT [sink]: Extracted
Outputs: OUTPUT [outputVector]

### native:intersection: Intersection
This algorithm extracts the overlapping portions of features in the Input and Overlay layers. Features in the output Intersection layer are assigned the attributes of the overlapping features from both the Input and Overlay layers.
Parameters:
- INPUT [source]: Input layer
- OVERLAY [source]: Overlay layer
- INPUT_FIELDS [field]: Input fields to keep (leave empty to keep all fields) (optional)
- OVERLAY_FIELDS [field]: Overlay fields to keep (leave empty to keep all fields) (optional)
- OVERLAY_FIELDS_PREFIX [string]: Overlay fields prefix (optional)
- OUTPUT [sink]: Intersection
- GRID_SIZE [number]: Grid size (optional)
Outputs: OUTPUT [outputVector]

### native:lineintersections: Line intersections
This algorithm creates point features where the lines in the Intersect layer intersect the lines in the Input layer.
Parameters:
- INPUT [source]: Input layer
- INTERSECT [source]: Intersect layer
- INPUT_FIELDS [field]: Input fields to keep (leave empty to keep all fields) (optional)
- INTERSECT_FIELDS [field]: Intersect fields to keep (leave empty to keep all fields) (optional)
- INTERSECT_FIELDS_PREFIX [string]: Intersect fields prefix (optional)
- OUTPUT [sink]: Intersections
Outputs: OUTPUT [outputVector]

### native:multidifference: Difference (multiple)
This algorithm extracts features from the Input layer that fall completely outside or only partially overlap the features from any of the Overlay layer(s). For each overlay layer the difference is calculated between the result of all previous difference operations and this overlay layer. Input layer features that partially overlap feature(s) in the Overlay layers are split along those features' boundary and only the portions outside the Overlay layer features are retained.
Attributes are not modified, although properties such as area or length of the features will be modified by the difference operation. If such properties are stored as attributes, those attributes will have to be manually updated.
Parameters:
- INPUT [source]: Input layer
- OVERLAYS [multilayer]: Overlay layers
- OUTPUT [sink]: Difference
Outputs: OUTPUT [outputVector]

### native:multiintersection: Intersection (multiple)
This algorithm extracts the overlapping portions of features in the Input and all Overlay layers. Features in the output layer are assigned the attributes of the overlapping features from both the Input and Overlay layers.
Parameters:
- INPUT [source]: Input layer
- OVERLAYS [multilayer]: Overlay layers
- OVERLAY_FIELDS_PREFIX [string]: Overlay fields prefix (optional)
- OUTPUT [sink]: Intersection
Outputs: OUTPUT [outputVector]

### native:multiunion: Union (multiple)
This algorithm checks overlaps between features within the Input layer and creates separate features for overlapping and non-overlapping parts. The area of overlap will create as many identical overlapping features as there are features that participate in that overlap.
Multiple Overlay layers can also be used, in which case features from each layer are split at their overlap with features from all other layers, creating a layer containing all the portions from both Input and Overlay layers. The attribute table of the Union layer is filled with attribute values from the respective original layer for non-overlapping features, and attribute values from both layers for overlapping features.
Parameters:
- INPUT [source]: Input layer
- OVERLAYS [multilayer]: Overlay layers (optional)
- OVERLAY_FIELDS_PREFIX [string]: Overlay fields prefix (optional)
- OUTPUT [sink]: Union
Outputs: OUTPUT [outputVector]

### native:splitwithlines: Split with lines
This algorithm splits the lines or polygons in one layer using the lines or polygon rings in another layer to define the breaking points. Intersection between geometries in both layers are considered as split points.
Parameters:
- INPUT [source]: Input layer
- LINES [source]: Split layer
- OUTPUT [sink]: Split
Outputs: OUTPUT [outputVector]

### native:symmetricaldifference: Symmetrical difference
This algorithm extracts the portions of features from both the Input and Overlay layers that do not overlap. Overlapping areas between the two layers are removed. The attribute table of the Symmetrical Difference layer contains original attributes from both the Input and Overlay layers.
Parameters:
- INPUT [source]: Input layer
- OVERLAY [source]: Overlay layer
- OVERLAY_FIELDS_PREFIX [string]: Overlay fields prefix (optional)
- OUTPUT [sink]: Symmetrical difference
- GRID_SIZE [number]: Grid size (optional)
Outputs: OUTPUT [outputVector]

### native:union: Union
This algorithm checks overlaps between features within the Input layer and creates separate features for overlapping and non-overlapping parts. The area of overlap will create as many identical overlapping features as there are features that participate in that overlap.
An Overlay layer can also be used, in which case features from each layer are split at their overlap with features from the other one, creating a layer containing all the portions from both Input and Overlay layers. The attribute table of the Union layer is filled with attribute values from the respective original layer for non-overlapping features, and attribute values from both layers for overlapping features.
Parameters:
- INPUT [source]: Input layer
- OVERLAY [source]: Overlay layer (optional)
- OVERLAY_FIELDS_PREFIX [string]: Overlay fields prefix (optional)
- OUTPUT [sink]: Union
- GRID_SIZE [number]: Grid size (optional)
Outputs: OUTPUT [outputVector]


## QGIS (native c++) / Vector selection

### native:extractbyattribute: Extract by attribute
This algorithm creates a new vector layer that only contains matching features from an input layer. The criteria for adding features to the resulting layer is defined based on the values of an attribute from the input layer.
Parameters:
- INPUT [source]: Input layer
- FIELD [field]: Selection attribute
- OPERATOR [enum]: Operator (default 0; options 0==, 1=≠, 2=>, 3=≥, 4=<, 5=≤, 6=begins with, 7=contains, 8=is null, 9=is not null, 10=does not contain)
- VALUE [string]: Value (optional)
- OUTPUT [sink]: Extracted (attribute)
- FAIL_OUTPUT [sink]: Extracted (non-matching) (optional)
Outputs: OUTPUT [outputVector], FAIL_OUTPUT [outputVector]

### native:extractbyexpression: Extract by expression
This algorithm creates a new vector layer that only contains matching features from an input layer. The criteria for adding features to the resulting layer is based on a QGIS expression.
For help with QGIS expression functions, see the inbuilt help for specific functions which is available in the expression builder.
Parameters:
- INPUT [source]: Input layer
- EXPRESSION [expression]: Expression
- OUTPUT [sink]: Matching features
- FAIL_OUTPUT [sink]: Non-matching (optional)
Outputs: OUTPUT [outputVector], FAIL_OUTPUT [outputVector]

### native:extractbylocation: Extract by location
This algorithm creates a new vector layer that only contains matching features from an input layer. The criteria for adding features to the resulting layer is defined based on the spatial relationship between each feature and the features in an additional layer.
Parameters:
- INPUT [source]: Extract features from
- PREDICATE [enum]: Where the features (geometric predicate) (default [0]; options 0=intersect, 1=contain, 2=disjoint, 3=equal, 4=touch, 5=overlap, 6=are within, 7=cross)
- INTERSECT [source]: By comparing to the features from
- OUTPUT [sink]: Extracted (location)
Outputs: OUTPUT [outputVector]

### native:extractwithindistance: Extract within distance
This algorithm creates a new vector layer that only contains matching features from an input layer. Features are copied wherever they are within the specified maximum distance from the features in an additional reference layer.
Parameters:
- INPUT [source]: Extract features from
- REFERENCE [source]: By comparing to the features from
- DISTANCE [distance]: Where the features are within (default 100)
- OUTPUT [sink]: Extracted (location)
Outputs: OUTPUT [outputVector]

### native:filterbygeometry: Filter by geometry type
This algorithm filters features by their geometry type. Incoming features will be directed to different outputs based on whether they have a point, line or polygon geometry.
Parameters:
- INPUT [source]: Input layer
- POINTS [sink]: Point features (optional)
- LINES [sink]: Line features (optional)
- POLYGONS [sink]: Polygon features (optional)
- NO_GEOMETRY [sink]: Features with no geometry (optional)
Outputs: POINTS [outputVector], LINES [outputVector], POLYGONS [outputVector], NO_GEOMETRY [outputVector], POINT_COUNT [outputNumber], LINE_COUNT [outputNumber], POLYGON_COUNT [outputNumber], NO_GEOMETRY_COUNT [outputNumber]

### native:randomextract: Random extract
This algorithm takes a vector layer and generates a new one that contains only a subset of the features in the input layer.
The subset is defined randomly, using a percentage or count value to define the total number of features in the subset.
Parameters:
- INPUT [source]: Input layer
- METHOD [enum]: Method (default 0; options 0=Number of features, 1=Percentage of features)
- NUMBER [number]: Number/percentage of features (default 10)
- OUTPUT [sink]: Extracted (random)
Outputs: OUTPUT [outputVector]

### native:selectbylocation: Select by location
This algorithm creates a selection in a vector layer. The criteria for selecting features is based on the spatial relationship between each feature and the features in an additional layer.
Parameters:
- INPUT [vector]: Select features from
- PREDICATE [enum]: Where the features (geometric predicate) (default [0]; options 0=intersect, 1=contain, 2=disjoint, 3=equal, 4=touch, 5=overlap, 6=are within, 7=cross)
- INTERSECT [source]: By comparing to the features from
- METHOD [enum]: Modify current selection by (default 0; options 0=creating new selection, 1=adding to current selection, 2=selecting within current selection, 3=removing from current selection)

### native:selectwithindistance: Select within distance
This algorithm creates a selection in a vector layer. Features are selected wherever they are within the specified maximum distance from the features in an additional reference layer.
Parameters:
- INPUT [vector]: Select features from
- REFERENCE [source]: By comparing to the features from
- DISTANCE [distance]: Where the features are within (default 100)
- METHOD [enum]: Modify current selection by (default 0; options 0=creating new selection, 1=adding to current selection, 2=selecting within current selection, 3=removing from current selection)


## QGIS (native c++) / Vector table

### native:addautoincrementalfield: Add autoincremental field
This algorithm adds a new integer field to a vector layer, with a sequential value for each feature.
This field can be used as a unique ID for features in the layer. The new attribute is not added to the input layer but a new layer is generated instead.
The initial starting value for the incremental series can be specified.
Specifying an optional modulus value will restart the count to START whenever the field value reaches the modulus value.
Optionally, grouping fields can be specified. If group fields are present, then the field value will be reset for each combination of these group field values.
The sort order for features may be specified, if so, then the incremental field will respect this sort order.
Parameters:
- INPUT [source]: Input layer
- FIELD_NAME [string]: Field name (default AUTO)
- START [number]: Start values at (optional; default 0)
- MODULUS [number]: Modulus value (optional; default 0)
- GROUP_FIELDS [field]: Group values by (optional)
- SORT_EXPRESSION [expression]: Sort expression (optional)
- SORT_ASCENDING [boolean]: Sort ascending (default True)
- SORT_NULLS_FIRST [boolean]: Sort nulls first (default False)
- OUTPUT [sink]: Incremented
Outputs: OUTPUT [outputVector]

### native:addfieldtoattributestable: Add field to attributes table
This algorithm adds a new attribute to a vector layer.
The name and characteristics of the attribute are defined as parameters. The new attribute is not added to the input layer but a new layer is generated instead.
Parameters:
- INPUT [source]: Input layer
- FIELD_NAME [string]: Field name
- FIELD_TYPE [enum]: Field type (default 0; options 0=Integer (32 bit), 1=Decimal (double), 2=Text (string), 3=Boolean, 4=Date, 5=Time, 6=Date & Time, 7=Binary Object (BLOB), 8=String List, 9=Integer List, 10=Decimal (double) List)
- FIELD_LENGTH [number]: Field length (default 10)
- FIELD_PRECISION [number]: Field precision (default 0)
- FIELD_ALIAS [string]: Field alias (optional)
- FIELD_COMMENT [string]: Field comment (optional)
- OUTPUT [sink]: Added
Outputs: OUTPUT [outputVector]

### native:adduniquevalueindexfield: Add unique value index field
This algorithm takes a vector layer and an attribute and adds a new numeric field. Values in this field correspond to values in the specified attribute, so features with the same value for the attribute will have the same value in the new numeric field. This creates a numeric equivalent of the specified attribute, which defines the same classes.
The new attribute is not added to the input layer but a new layer is generated instead.
Optionally, a separate table can be output which contains a summary of the class field values mapped to the new unique numeric value.
Parameters:
- INPUT [source]: Input layer
- FIELD [field]: Class field
- FIELD_NAME [string]: Output field name (default NUM_FIELD)
- OUTPUT [sink]: Layer with index field (optional)
- SUMMARY_OUTPUT [sink]: Class summary (optional)
Outputs: OUTPUT [outputVector], SUMMARY_OUTPUT [outputVector]

### native:addxyfields: Add X/Y fields to layer
This algorithm adds X and Y (or latitude/longitude) fields to a point layer. The X/Y fields can be calculated in a different CRS to the layer (e.g. creating latitude/longitude fields for a layer in a project CRS).
Parameters:
- INPUT [source]: Input layer
- CRS [crs]: Coordinate system (default EPSG:4326)
- PREFIX [string]: Field prefix (optional)
- OUTPUT [sink]: Added fields
Outputs: OUTPUT [outputVector]

### native:deletecolumn: Drop field(s)
This algorithm takes a vector layer and generates a new one that has the exact same content but without the selected columns.
Parameters:
- INPUT [source]: Input layer
- COLUMN [field]: Fields to drop
- OUTPUT [sink]: Remaining fields
Outputs: OUTPUT [outputVector]

### native:explodehstorefield: Explode HStore Field
This algorithm creates a copy of the input layer and adds a new field for every unique key in the HStore field.
The expected field list is an optional comma separated list. By default, all unique keys are added. If this list is specified, only these fields are added and the HStore field is updated.
Parameters:
- INPUT [source]: Input layer
- FIELD [field]: HStore field
- EXPECTED_FIELDS [string]: Expected list of fields separated by a comma (optional)
- OUTPUT [sink]: Exploded
Outputs: OUTPUT [outputVector]

### native:extractbinary: Extract binary field
This algorithm extracts contents from a binary field, saving them to individual files.
Filenames can be generated using values taken from an attribute in the source table or based on a more complex expression.
Parameters:
- INPUT [source]: Input layer
- FIELD [field]: Binary field
- FILENAME [expression]: File name
- FOLDER [folderDestination]: Destination folder
Outputs: FOLDER [outputFolder]

### native:fieldcalculator: Field calculator
This algorithm computes a new vector layer with the same features of the input layer, but either overwriting an existing attribute or adding an additional attribute. The values of this field are computed from each feature using an expression, based on the properties and attributes of the feature. Note that if "Field name" is an existing field in the layer then all the rest of the field settings are ignored.
Parameters:
- INPUT [source]: Input layer
- FIELD_NAME [string]: Field name
- FIELD_TYPE [enum]: Result field type (default 0; options 0=Decimal (double), 1=Integer (32 bit), 2=Text (string), 3=Date, 4=Time, 5=Date & Time, 6=Boolean, 7=Binary Object (BLOB), 8=String List, 9=Integer List, 10=Decimal (double) List)
- FIELD_LENGTH [number]: Result field length (default 0)
- FIELD_PRECISION [number]: Result field precision (default 0)
- FORMULA [expression]: Formula
- OUTPUT [sink]: Calculated
Outputs: OUTPUT [outputVector]

### native:refactorfields: Refactor fields
This algorithm allows editing the structure of the attributes table of a vector layer. Fields can be modified in their type and name, using a fields mapping.
The original layer is not modified. A new layer is generated, which contains a modified attribute table, according to the provided fields mapping.
Rows in orange have constraints in the template layer from which these fields were loaded. Treat this information as a hint during configuration. No constraints will be added on an output layer nor will they be checked or enforced by the algorithm.
Parameters:
- INPUT [source]: Input layer
- FIELDS_MAPPING [fields_mapping]: Fields mapping
- OUTPUT [sink]: Refactored
Outputs: OUTPUT [outputVector]

### native:renametablefield: Rename field
This algorithm renames an existing field from a vector layer.
Parameters:
- INPUT [source]: Input layer
- FIELD [field]: Field to rename
- NEW_NAME [string]: New field name
- OUTPUT [sink]: Renamed
Outputs: OUTPUT [outputVector]

### native:retainfields: Retain fields
This algorithm takes a vector layer and generates a new one that retains only the selected fields. All other fields will be dropped.
Parameters:
- INPUT [source]: Input layer
- FIELDS [field]: Fields to retain
- OUTPUT [sink]: Retained fields
Outputs: OUTPUT [outputVector]


## QGIS (native c++) / Vector tiles

### native:downloadvectortiles: Download vector tiles
This algorithm downloads vector tiles of the input vector tile layer and saves them in the local vector tile file.
Parameters:
- INPUT [layer]: Input layer
- EXTENT [extent]: Extent
- MAX_ZOOM [number]: Maximum zoom level to download (default 10)
- TILE_LIMIT [number]: Tile limit (default 100)
- OUTPUT [vectorTileDestination]: Output
Outputs: OUTPUT [outputVectorTile]

### native:writevectortiles_mbtiles: Write Vector Tiles (MBTiles)
This algorithm exports one or more vector layers to vector tiles - a data format optimized for fast map rendering and small data size.
Parameters:
- OUTPUT [vectorTileDestination]: Destination MBTiles
- LAYERS [vectortilewriterlayers]: Input layers
- MIN_ZOOM [number]: Minimum zoom level (default 0)
- MAX_ZOOM [number]: Maximum zoom level (default 3)
- EXTENT [extent]: Extent (optional)
- META_NAME [string]: Metadata: Name (optional)
- META_DESCRIPTION [string]: Metadata: Description (optional)
- META_ATTRIBUTION [string]: Metadata: Attribution (optional)
- META_VERSION [string]: Metadata: Version (optional)
- META_TYPE [string]: Metadata: Type (optional)
- META_CENTER [string]: Metadata: Center (optional)
Outputs: OUTPUT [outputVectorTile]

### native:writevectortiles_xyz: Write Vector Tiles (XYZ)
This algorithm exports one or more vector layers to vector tiles - a data format optimized for fast map rendering and small data size.
Parameters:
- OUTPUT_DIRECTORY [folderDestination]: Output directory
- XYZ_TEMPLATE [string]: File template (default {z}/{x}/{y}.pbf)
- LAYERS [vectortilewriterlayers]: Input layers
- MIN_ZOOM [number]: Minimum zoom level (default 0)
- MAX_ZOOM [number]: Maximum zoom level (default 3)
- EXTENT [extent]: Extent (optional)
Outputs: OUTPUT_DIRECTORY [outputFolder]
