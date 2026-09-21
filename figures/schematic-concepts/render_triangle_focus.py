"""Standalone perspective study; never replaces the manuscript schematic.

Render in WSL with Blender, then run compose_triangle_focus.py. Identical amber
spheres denote bosons, opaque bonds the equilateral triangular lattice, and one
arrow an example hop in H_t = +t sum_<ij> (b_i^+ b_j + b_j^+ b_i).
The geometry is illustrative, not an occupation snapshot or a chiral current.
"""

import argparse
import json
import math
from pathlib import Path
import sys

import bpy
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Vector


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "pdf" / "triangle-focus-draft"
OUT.mkdir(parents=True, exist_ok=True)
parser = argparse.ArgumentParser()
parser.add_argument("--final", action="store_true")
parser.add_argument("--metadata-only", action="store_true")
args = parser.parse_args(sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else [])


def linear(hex_color):
    rgb = [int(hex_color[k:k+2], 16)/255 for k in (1, 3, 5)]
    return [v/12.92 if v < .04045 else ((v+.055)/1.055)**2.4 for v in rgb]


def material(name, color, roughness=.26, metal=.0):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    tree = mat.node_tree
    bsdf = tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*linear(color), 1)
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metal
    bsdf.inputs["IOR"].default_value = 1.33
    bsdf.inputs["Coat Weight"].default_value = .22
    bsdf.inputs["Coat Roughness"].default_value = .24
    return mat


def soft_boson():
    mat = material("All bosons - soft amber", "#CE984F", roughness=.42)
    tree = mat.node_tree
    bsdf = tree.nodes.get("Principled BSDF")
    bsdf.inputs["Transmission Weight"].default_value = .12
    bsdf.inputs["IOR"].default_value = 1.30
    bsdf.inputs["Coat Weight"].default_value = .025
    bsdf.inputs["Subsurface Weight"].default_value = .055
    bsdf.inputs["Subsurface Radius"].default_value = (.12, .075, .04)
    absorption = tree.nodes.new("ShaderNodeVolumeAbsorption")
    absorption.inputs["Color"].default_value = (*linear("#DFB475"), 1)
    absorption.inputs["Density"].default_value = 1.8
    tree.links.new(absorption.outputs[0], tree.nodes.get("Material Output").inputs["Volume"])
    return mat


def tube(name, a, b, radius, mat):
    curve = bpy.data.curves.new(name, "CURVE")
    curve.dimensions = "3D"
    curve.bevel_depth = radius
    curve.bevel_resolution = 4
    spline = curve.splines.new("POLY")
    spline.points.add(1)
    spline.points[0].co = (*a, 1)
    spline.points[1].co = (*b, 1)
    obj = bpy.data.objects.new(name, curve)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(mat)
    obj.visible_shadow = True


def sphere(name, p, mat):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=40,
                                       radius=.245, location=p)
    obj = bpy.context.object
    obj.name = name
    obj.data.materials.append(mat)
    for face in obj.data.polygons:
        face.use_smooth = True


def area(name, position, power, size, color, shadow=True):
    light = bpy.data.lights.new(name, "AREA")
    light.energy, light.shape, light.size = power, "DISK", size
    light.color = color
    light.use_shadow = shadow
    obj = bpy.data.objects.new(name, light)
    bpy.context.collection.objects.link(obj)
    obj.location = position
    obj.rotation_euler = (-obj.location).to_track_quat("-Z", "Y").to_euler()


bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
scene = bpy.context.scene
scene.render.engine = "CYCLES"
scene.cycles.device = "CPU"
scene.cycles.samples = 128 if args.final else 64
scene.cycles.use_denoising = True
scene.cycles.denoiser = "OPENIMAGEDENOISE"
scene.cycles.caustics_reflective = False
scene.cycles.caustics_refractive = False
scene.cycles.transparent_max_bounces = 32
scene.render.threads_mode = "FIXED"
scene.render.threads = 8
scene.render.resolution_x = 2000 if args.final else 1400
scene.render.resolution_y = 1545 if args.final else 1082
scene.render.resolution_percentage = 100
scene.render.film_transparent = True
scene.render.image_settings.file_format = "PNG"
scene.render.image_settings.color_mode = "RGBA"
scene.view_settings.view_transform = "Standard"
scene.view_settings.look = "Medium High Contrast"
scene.world.use_nodes = True
scene.world.node_tree.nodes["Background"].inputs["Color"].default_value = (.87, .93, 1, 1)
scene.world.node_tree.nodes["Background"].inputs["Strength"].default_value = .75

cam = bpy.data.objects.new("Wide perspective", bpy.data.cameras.new("Wide perspective"))
bpy.context.collection.objects.link(cam)
cam.location = (.60, -2.85, 2.50)
cam.rotation_euler = (Vector((0, -.16, .02))-cam.location).to_track_quat("-Z", "Y").to_euler()
cam.data.type = "PERSP"
cam.data.lens = 19
cam.data.sensor_width = 36
scene.camera = cam
area("Only shadow-casting key", (-3, -4, 8), 320, 4.5, (1, .98, .95))
area("Soft rim - no shadows", (3, 2, 5), 170, 3.5, (.90, .95, 1), shadow=False)
area("Front fill - no shadows", (1, -5, 2), 35, 3, (.95, .97, 1), shadow=False)

# A neutral shadow catcher conveys depth without introducing a visible platform.
# The spheres sit just above it; bonds cast slightly offset, soft shadows.
bpy.ops.mesh.primitive_plane_add(size=200, location=(0, 0, -.265))
ground = bpy.context.object
ground.name = "Invisible floor - soft contact shadows"
ground.is_shadow_catcher = True
ground.data.materials.append(material("Matte white floor", "#ffffff", roughness=1))

# Exact equilateral lattice: a1=(2,0), a2=(1,sqrt(3)); central triangle points
# toward the viewer. Every bond is a true nearest neighbour of length 2.
offset = Vector((0, -2*math.sqrt(3)/3, .0))
sites = {(i, j): Vector((2*i+j, math.sqrt(3)*j, 0))+offset
         for j in range(-1, 4) for i in range(-3, 3)}
core = [(0, 0), (-1, 1), (0, 1)]
edges = set()
for key in sites:
    for di, dj in ((1, 0), (0, 1), (-1, 1)):
        other = (key[0]+di, key[1]+dj)
        if other in sites:
            edges.add(tuple(sorted((key, other))))
adjacent = [(-1, 0), (1, 0), (-1, 2)]
bond_mat = material("All bonds - opaque matte graphite", "#505259", roughness=.78)
bond_shader = bond_mat.node_tree.nodes.get("Principled BSDF")
bond_shader.inputs["Coat Weight"].default_value = 0
bond_shader.inputs["Specular IOR Level"].default_value = .25
ball_mat = soft_boson()
for left, right in sorted(edges):
    a, b = sites[left], sites[right]
    assert abs((b-a).length-2) < 1e-6
    tube(f"Lattice bond {left}-{right}", a, b, .032, bond_mat)
for key, p in sites.items():
    sphere(f"Boson {key}", p, ball_mat)

bpy.context.view_layer.update()

def project(p):
    v = world_to_camera_view(scene, cam, p)
    return [float(v.x), float(1-v.y)]

# Project one example nearest-neighbour hop with the same camera. A single
# arrow illustrates hopping and does not assert a circulating current.
arcs = []
for left, right in [(core[0], core[2])]:
    a, b = sites[left], sites[right]
    points = []
    for n in range(101):
        t = .16 + .68*n/100
        p = a.lerp(b, t)
        p.z += .07 + .78*math.sin(math.pi*(t-.16)/.68)
        points.append(project(p))
    arcs.append(points)
label = list(min(arcs[0], key=lambda point: point[1]))
label[0] += .060
label[1] -= .039
camera_right = cam.matrix_world.to_quaternion() @ Vector((1, 0, 0))
halo_sites = []
for p in sites.values():
    center = project(p)
    radius_x = abs(project(p + .245*camera_right)[0] - center[0])
    halo_sites.append({"center": center, "radius_x": radius_x})
metadata = {"sites": [project(sites[k]) for k in core], "arcs": arcs,
            "halo_sites": halo_sites,
            "adjacent_sites": [project(sites[k]) for k in adjacent],
            "core_world": [[float(sites[k].x), float(sites[k].y)] for k in core],
            "plane_reference": [{"world": [x, y], "image": project(Vector((x, y, 0)))}
                                for x, y in [(0, 0), (1, 0), (1, 1), (0, 1)]],
            "hopping_label": label,
            "equal_boson_radius": .245, "bond_length": 2,
            "bond_radius": .032, "uniform_bond_material": True,
            "lattice_site_count": len(sites), "boson_count": len(sites),
            "camera_lens_mm": cam.data.lens,
            "convention": "H_t = +t sum_<ij> (b_i^+ b_j + b_j^+ b_i)",
            "example_hopping_arrows": 1}
(OUT / "projection.json").write_text(json.dumps(metadata, indent=2)+"\n")
scene.render.filepath = str(OUT / "lattice-render.png")
bpy.ops.wm.save_as_mainfile(filepath=str(OUT / "triangle-focus.blend"))
if not args.metadata_only:
    bpy.ops.render.render(write_still=True)
    print("Standalone motif rendered", flush=True)
