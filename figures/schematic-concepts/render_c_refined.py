"""Render the focused C revision with Blender.

Run with Blender 4.x in WSL. The particles are explanatory symbols, not sampled
world lines in the auxiliary-field representation. The open two-dimensional net
is a schematic fluctuating auxiliary field, not numerical data or lattice bonds.
"""

from __future__ import annotations

import argparse
import math
from pathlib import Path
import sys

import bpy
from mathutils import Vector


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "pdf" / "schematic-concepts" / "C_refined_v2_assets"
OUT.mkdir(parents=True, exist_ok=True)


def arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--quality", choices=["draft", "final"], default="draft")
    parser.add_argument("--only", choices=["background", "field", "interaction", "loop", "hs", "both", "all"], default="all")
    return parser.parse_args(sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else [])


def linear_rgb(hex_color):
    values = [int(hex_color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    return tuple(v / 12.92 if v < .04045 else ((v + .055) / 1.055) ** 2.4
                 for v in values)


def material(name, color, roughness=.30, metallic=0.0):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*linear_rgb(color), 1)
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Coat Weight"].default_value = .18
    bsdf.inputs["Coat Roughness"].default_value = .24
    return mat


def diagram_ink(name, color, opacity=1.0):
    """Unlit, shadowless ink for interactions, distinct from material rods."""
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nodes, links = mat.node_tree.nodes, mat.node_tree.links
    nodes.clear()
    output = nodes.new("ShaderNodeOutputMaterial")
    emission = nodes.new("ShaderNodeEmission")
    emission.inputs["Color"].default_value = (*linear_rgb(color), 1)
    transparent = nodes.new("ShaderNodeBsdfTransparent")
    mix = nodes.new("ShaderNodeMixShader")
    mix.inputs[0].default_value = opacity
    links.new(transparent.outputs[0], mix.inputs[1])
    links.new(emission.outputs[0], mix.inputs[2])
    links.new(mix.outputs[0], output.inputs["Surface"])
    return mat


def smooth(obj, mat):
    obj.data.materials.append(mat)
    if obj.type == "MESH":
        for face in obj.data.polygons:
            face.use_smooth = True
    return obj


def sphere(name, xyz, radius, mat):
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=48, ring_count=32, radius=radius, location=xyz
    )
    obj = bpy.context.object
    obj.name = name
    return smooth(obj, mat)


def tube(name, points, radius, mat, closed=False):
    data = bpy.data.curves.new(name, "CURVE")
    data.dimensions = "3D"
    data.resolution_u = 2
    data.bevel_depth = radius
    data.bevel_resolution = 5
    spline = data.splines.new("POLY")
    spline.points.add(len(points) - 1)
    for p, xyz in zip(spline.points, points):
        p.co = (*xyz, 1)
    spline.use_cyclic_u = closed
    obj = bpy.data.objects.new(name, data)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(mat)
    return obj


def area_light(name, xyz, energy, size, color=(1, 1, 1)):
    data = bpy.data.lights.new(name, type="AREA")
    data.energy, data.shape, data.size = energy, "DISK", size
    data.color = color
    obj = bpy.data.objects.new(name, data)
    bpy.context.collection.objects.link(obj)
    obj.location = xyz
    obj.rotation_euler = (Vector((0, 0, 0)) - obj.location).to_track_quat("-Z", "Y").to_euler()


def setup(name, quality):
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    scene = bpy.context.scene
    scene.name = name
    scene.render.engine = "CYCLES"
    scene.cycles.device = "CPU"
    scene.cycles.samples = 64 if quality == "draft" else 256
    # Use the official Linux build, which includes OpenImageDenoise. Blender's
    # build_options does not expose a reliable OIDN capability flag.
    scene.cycles.use_denoising = True
    scene.cycles.denoiser = "OPENIMAGEDENOISE"
    scene.cycles.use_adaptive_sampling = True
    scene.cycles.adaptive_threshold = .05 if quality == "draft" else .02
    scene.cycles.transparent_max_bounces = 8
    scene.render.threads_mode = "FIXED"
    scene.render.threads = 8
    scene.render.resolution_x = 1000 if quality == "draft" else 1600
    scene.render.resolution_y = 820 if quality == "draft" else 1312
    scene.render.resolution_percentage = 100
    scene.render.film_transparent = True
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGBA"
    scene.render.image_settings.color_depth = "8"
    scene.render.image_settings.compression = 35
    scene.view_settings.view_transform = "Standard"
    scene.view_settings.look = "Medium High Contrast"
    scene.view_settings.exposure = 0
    scene.view_settings.gamma = 1
    scene.world.use_nodes = True
    scene.world.node_tree.nodes["Background"].inputs["Color"].default_value = (.82, .88, .96, 1)
    scene.world.node_tree.nodes["Background"].inputs["Strength"].default_value = .40

    cam_data = bpy.data.cameras.new("Orthographic camera")
    camera = bpy.data.objects.new("Orthographic camera", cam_data)
    bpy.context.collection.objects.link(camera)
    camera.location = (5.8, -8.5, 10.5)
    camera.rotation_euler = (
        Vector((0, 0, .10)) - camera.location
    ).to_track_quat("-Z", "Y").to_euler()
    cam_data.type = "ORTHO"
    cam_data.ortho_scale = 4.8
    scene.camera = camera

    area_light("Large softbox", (-3.5, -4.5, 7.5), 530, 5.0, (1.0, .95, .91))
    area_light("Cool fill", (4, 1.5, 5), 190, 4.0, (.84, .92, 1.0))
    area_light("Rim", (-1, 4, 4), 150, 3.0, (1, 1, 1))
    bpy.ops.mesh.primitive_plane_add(size=200, location=(0, 0, -.32))
    ground = bpy.context.object
    ground.name = "Transparent shadow receiver"
    ground.is_shadow_catcher = True
    ground.data.materials.append(material("Receiver", "#ffffff", 1))
    return scene


def field_height(x, y):
    return (.15*math.sin(2.55*x+.45)*math.cos(2.4*y-.25)
            + .09*math.cos(3.4*y+.85*x) + .05*math.sin(4.2*x-1.5*y))


def field_net():
    """An open, gently fluctuating two-dimensional net, with no filled faces."""
    ink = diagram_ink("Auxiliary-field net", "#418ca4", .64)
    for i in range(9):
        x = -1.42 + 2.84*i/8
        points = [(x, -1.04 + 2.08*j/96,
                   field_height(x, -1.04 + 2.08*j/96)) for j in range(97)]
        line = tube(f"Field net x{i}", points, .0065, ink)
        line.visible_shadow = False
    for j in range(7):
        y = -1.04 + 2.08*j/6
        points = [(-1.42 + 2.84*i/112, y,
                   field_height(-1.42 + 2.84*i/112, y)) for i in range(113)]
        line = tube(f"Field net y{j}", points, .0065, ink)
        line.visible_shadow = False


def field_scene(quality):
    scene = setup("Bosons in an auxiliary-field background", quality)
    scene.camera.data.type = "PERSP"
    scene.camera.data.lens = 65
    scene.camera.location = (4.6,-6.8,8.2)
    scene.camera.rotation_euler = (Vector((0,0,.2))-scene.camera.location).to_track_quat("-Z","Y").to_euler()
    bpy.data.objects["Transparent shadow receiver"].hide_render = True
    copper = material("Boson - warm ceramic", "#c4634c", .25, .03)
    coupling = diagram_ink("Particle-field interaction", "#79698f", 1)
    field_net()
    sites = [(-.76, -.49), (.74, -.49), (-.02, .65)]
    for i, (x, y) in enumerate(sites):
        # Only particle-field couplings remain after HS decoupling. No edge
        # connects the particles to one another in this scene.
        # Land on a visible net line rather than in an empty mesh cell.
        anchor_x = -1.42 + round((x+1.42)/(2.84/8))*(2.84/8)
        bottom = field_height(anchor_x,y)
        sphere(f"Boson {i+1}", (x, y, bottom+.73), .18, copper)
        points = []
        for k in range(91):
            t = k/90
            wiggle = .045*math.sin(2*math.pi*3*t)*math.sin(math.pi*t)**.3
            points.append((anchor_x+(x-anchor_x)*t+.825*wiggle,
                           y+.563*wiggle, bottom+.55*t))
        wave = tube(f"Particle {i+1} coupled to field", points, .012, coupling)
        wave.visible_shadow = False
    return scene


def interaction_edge(name, a, b, coupling):
    """The same continuous, unlit wavy notation for every direct interaction."""
    delta = Vector((b[0]-a[0], b[1]-a[1], 0))
    normal = Vector((-delta.y, delta.x, 0)).normalized()
    points = []
    for k in range(181):
        t = k/180
        lateral = .075*math.sin(8*math.pi*t)*math.sin(math.pi*t)**.3
        points.append(Vector((a[0],a[1],.18))+t*delta+lateral*normal)
    wave = tube(name, points, .012, coupling)
    wave.visible_shadow = False
    return wave


def interaction_scene(quality):
    scene = setup("Interacting bosons before HS decoupling", quality)
    scene.camera.data.ortho_scale = 3.4
    bpy.data.objects["Transparent shadow receiver"].hide_render = True
    copper = material("Boson - warm ceramic", "#c4634c", .25, .03)
    coupling = diagram_ink("Direct interaction - continuous wavy ink", "#79698f", 1)
    sites = [(-.76,-.49), (.74,-.49), (-.02,.65)]
    for i, a in enumerate(sites):
        b = sites[(i+1) % 3]
        interaction_edge(f"Interaction {i+1}", a, b, coupling)
    for i, (x,y) in enumerate(sites):
        sphere(f"Boson {i+1}", (x,y,.18), .18, copper)
    return scene


def pane(name, box, z, depth, mat, bevel=.046):
    x, y, width, height = box
    bpy.ops.mesh.primitive_cube_add(size=1, location=((x+width/2-500)/200, (500-y-height/2)/200, z))
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = (width/200, height/200, depth)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.data.materials.append(mat)
    edge = obj.modifiers.new("Rounded refractive edge", "BEVEL")
    edge.width, edge.segments = bevel, 10
    obj.modifiers.new("Weighted surface normals", "WEIGHTED_NORMAL")
    return obj


def glass(name, color):
    mat = material(name, color, .17, 0)
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Transmission Weight"].default_value = .62
    bsdf.inputs["IOR"].default_value = 1.52
    bsdf.inputs["Coat Weight"].default_value = .30
    bsdf.inputs["Coat Roughness"].default_value = .065
    return mat


def illuminated_blue():
    """A soft pool of light singles out the newly accessible quadrant."""
    mat = glass("Illuminated blue glass", "#75b8d1")
    nodes, links = mat.node_tree.nodes, mat.node_tree.links
    coordinates = nodes.new("ShaderNodeTexCoord")
    center = nodes.new("ShaderNodeVectorMath")
    center.operation = "SUBTRACT"
    center.inputs[1].default_value = (.25,.51,.5)
    links.new(coordinates.outputs["Generated"], center.inputs[0])
    flatten = nodes.new("ShaderNodeVectorMath")
    flatten.operation = "MULTIPLY"
    flatten.inputs[1].default_value = (1,1,0)
    links.new(center.outputs["Vector"], flatten.inputs[0])
    length = nodes.new("ShaderNodeVectorMath")
    length.operation = "LENGTH"
    links.new(flatten.outputs["Vector"], length.inputs[0])
    ramp = nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.interpolation = "EASE"
    ramp.color_ramp.elements[0].position = .11
    ramp.color_ramp.elements[0].color = (*linear_rgb("#bcecff"), 1)
    ramp.color_ramp.elements[1].position = .8
    ramp.color_ramp.elements[1].color = (*linear_rgb("#6aaec9"), 1)
    middle = ramp.color_ramp.elements.new(.56)
    middle.color = (*linear_rgb("#8dc8df"), 1)
    links.new(length.outputs["Value"], ramp.inputs["Fac"])
    links.new(ramp.outputs["Color"], nodes.get("Principled BSDF").inputs["Base Color"])
    return mat


def background_scene(quality):
    scene = setup("Layered liquid-glass classification", quality)
    bpy.data.objects["Transparent shadow receiver"].hide_render = True
    scene.render.resolution_x = scene.render.resolution_y = 1100 if quality == "draft" else 1800
    scene.cycles.max_bounces = 16
    scene.cycles.transmission_bounces = 12
    scene.cycles.samples = 96 if quality == "draft" else 128
    scene.camera.location = (0,-2,12)
    scene.camera.rotation_euler = (Vector((0,0,.12))-scene.camera.location).to_track_quat("-Z","Y").to_euler()
    scene.camera.data.ortho_scale = 5
    key = bpy.data.objects["Large softbox"]
    key.location = (-3.5,4.5,7.5)
    key.rotation_euler = (-key.location).to_track_quat("-Z","Y").to_euler()
    key.data.size = 3.2
    bpy.ops.mesh.primitive_plane_add(size=200, location=(0,0,-.14))
    bpy.context.object.name = "White studio backdrop"
    bpy.context.object.data.materials.append(material("Matte white", "#ffffff", 1))

    spotlight = bpy.data.lights.new("Soft spotlight on new territory", type="SPOT")
    spotlight.energy = 110
    spotlight.shadow_soft_size = 1.0
    spotlight.color = (.76,.91,1.0)
    spotlight.spot_size = math.radians(58)
    spotlight.spot_blend = .85
    light = bpy.data.objects.new("Soft spotlight on new territory", spotlight)
    bpy.context.collection.objects.link(light)
    light.location = (-.9, .82, 3.2)
    light.rotation_euler = (0,0,0)

    # A single neutral support. All categorical color belongs to the panes.
    base = material("Uniform gray support", "#b9c0c5", .9)
    base.node_tree.nodes.get("Principled BSDF").inputs["Coat Weight"].default_value = 0
    pane("Uniform gray support", (148,161,780,783), -.035, .10, base, .035)
    amber = glass("Amber glass", "#f1dbaa")
    amber.node_tree.nodes.get("Principled BSDF").inputs["Transmission Weight"].default_value = .45
    pane("Unfrustrated amber glass", (548,157,374,778), .29, .10, amber, .038)
    pane("Upper symmetry blue glass", (116,116,850,425), .78, .11,
         illuminated_blue(), .041)
    return scene


def loop_scene(quality):
    scene = setup("Four equal interacting bosons on an unfrustrated square", quality)
    scene.camera.data.ortho_scale = 3.8
    bpy.data.objects["Transparent shadow receiver"].hide_render = True
    copper = material("Boson - warm ceramic", "#c4634c", .25, .03)
    coupling = diagram_ink("Direct interaction - continuous wavy ink", "#79698f", 1)
    sites = [(-.85,-.78), (.85,-.78), (.85,.78), (-.85,.78)]
    for i, (x,y) in enumerate(sites):
        sphere(f"Boson {i+1}", (x,y,.18), .18, copper)
        interaction_edge(f"Square interaction {i+1}", (x,y), sites[(i+1)%4], coupling)
    return scene


def save_render(scene, name):
    scene.render.filepath = str(OUT / f"{name}.png")
    bpy.ops.wm.save_as_mainfile(filepath=str(OUT / f"{name}.blend"))
    result = bpy.ops.render.render(write_still=True)
    if "CANCELLED" in result:
        raise RuntimeError(f"Render cancelled: {name}")
    print(f"FINISHED {name}", flush=True)


if __name__ == "__main__":
    args = arguments()
    if args.only in ("all", "background"):
        save_render(background_scene(args.quality), "background")
    if args.only in ("all", "hs", "interaction"):
        save_render(interaction_scene(args.quality), "interaction")
    if args.only in ("both", "all", "hs", "field"):
        save_render(field_scene(args.quality), "field")
    if args.only in ("both", "all", "loop"):
        save_render(loop_scene(args.quality), "loop")
