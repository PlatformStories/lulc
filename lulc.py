import json
import os
import protogen

input_ports_location = '/mnt/work/input/'
output_ports_location = '/mnt/work/output/'

# Get image directory
image_dir = os.path.join(input_ports_location, 'image')

# Point to image file. If there are multiple tif's in multiple subdirectories, pick one.
image = [os.path.join(dp, f) for dp, dn, fn in os.walk(image_dir) for f in fn if ('tif' in f) or ('TIF' in f)][0]

# Read from ports.json
input_ports_path = os.path.join(input_ports_location, 'ports.json')
if os.path.exists(input_ports_path):
    string_ports = json.load(open(input_ports_path))
else:
    string_ports = None

if string_ports:

    vegetation = string_ports.get('vegetation', 'false')
    water = string_ports.get('water', 'false')
    soil = string_ports.get('soil', 'false')
    clouds = string_ports.get('clouds', 'false')
    shadows = string_ports.get('shadows', 'false')
    unclassified = string_ports.get('unclassified', 'false')
    tiles = string_ports.get('tiles', '1')
    verbose = string_ports.get('verbose', 'false')
    bbox = string_ports.get('bbox', '')

    tiles = int(tiles)

    if bbox:
        bbox = map(float, bbox.split(','))

    if vegetation in ['true', 'True']:
        vegetation = True
    else:
        vegetation = False
    if water in ['true', 'True']:
        water = True
    else:
        water = False
    if soil in ['true', 'True']:
        soil = True
    else:
        soil = False
    if clouds in ['true', 'True']:
        clouds = True
    else:
        clouds = False
    if shadows in ['true', 'True']:
        shadows = True
    else:
        shadows = False
    if unclassified in ['true', 'True']:
        unclassified = True
    else:
        unclassified = False

    if vegetation or water or soil or clouds or shadows or unclassified:
        rgb = False
    else:
        rgb = True

    if verbose in ['true', 'True']:
        verbose = True
    else:
        verbose = False

else:

    vegetation = False
    water = False
    soil = False
    clouds = False
    shadows = False
    unclassified = False
    rgb = True
    tiles = 1
    verbose = False

# Create output directory
output_dir = os.path.join(output_ports_location, 'image')
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
os.chdir(output_dir)

# Run lulc
if rgb:
    p = protogen.Interface('lulc', 'layers')
    p.lulc.layers.name = 'lulc'
    p.lulc.layers.visualization = 'rgb'
else:
    p = protogen.Interface('lulc', 'masks')
    p.lulc.masks.type = 'single'
    p.lulc.masks.switch_vegetation = vegetation
    p.lulc.masks.switch_water = water
    p.lulc.masks.switch_bare_soil = soil
    p.lulc.masks.switch_clouds = clouds
    p.lulc.masks.switch_shadows = shadows
    p.lulc.masks.switch_unclassified = unclassified
    # no data can never be the foreground
    p.lulc.masks.switch_no_data = False

# Specify input image and range of bands
p.image = image
p.image_config.bands = range(1, 9)

# Tile if asked for
if tiles > 1:
    p.image_config.number_of_tiles = tiles
    p.image_config.mosaic_method = 'max'

# bbox if provided
if bbox:
    W, S, E, N = bbox
    p.image_config.input_latlong_rectangle = [W, N, E, S]

# Execute
p.verbose = verbose
p.execute()
