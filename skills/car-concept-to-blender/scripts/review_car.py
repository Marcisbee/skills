"""Measure a car exterior and render fixed review views in Blender background mode."""

import argparse
import json
import math
import sys
from pathlib import Path

import bpy
import numpy as np
from mathutils import Vector


VIEWS = {
    "front": (1, 0, 0),
    "rear": (-1, 0, 0),
    "left": (0, 1, 0),
    "top": (0, 0, 1),
    "front_three_quarter": (1, 1.45, 0.55),
    "rear_three_quarter": (-1, 1.45, 0.55),
}
ORTHOGRAPHIC = {"front", "rear", "left", "top"}
WHEELS = ("front_left", "front_right", "rear_left", "rear_right")


def number(value, label, *, minimum=None):
    if type(value) not in (int, float) or not math.isfinite(value):
        raise ValueError(f"{label} must be a finite number")
    if minimum is not None and value < minimum:
        raise ValueError(f"{label} is out of range")
    return value


def camera_frame(config, base=None):
    frame = {**(base or {}), **config}
    center = frame["center_mm"]
    size = frame.get("size_px", [640, 640])
    if len(center) != 3 or len(size) != 2:
        raise ValueError("Frame requires three center coordinates and two pixel dimensions")
    if any(type(n) is not int or not 64 <= n <= 4096 for n in size):
        raise ValueError("Frame pixel dimensions must be integers from 64 to 4096")
    return {
        "center_mm": [number(v, "center_mm") for v in center],
        "ortho_scale_mm": number(frame["ortho_scale_mm"], "ortho_scale_mm", minimum=1e-6),
        "size_px": size,
    }


def snapshot_car(source, collection_name, tire_names):
    collection = bpy.data.collections.get(collection_name)
    if collection is None:
        raise ValueError(f"Missing car collection {collection_name!r}")
    if set(tire_names) != set(WHEELS) or len(set(tire_names.values())) != 4:
        raise ValueError("Provide four distinct tire objects keyed by wheel position")
    source_names = {obj.name for obj in collection.all_objects}
    depsgraph = bpy.context.evaluated_depsgraph_get()
    scene = bpy.data.scenes.new("Car review")
    bounds = {}
    for name in sorted(source_names):
        obj = source.objects.get(name)
        if obj is None or obj.type not in {"MESH", "CURVE", "SURFACE"} or obj.hide_render:
            continue
        evaluated = obj.evaluated_get(depsgraph)
        mesh = bpy.data.meshes.new_from_object(evaluated, depsgraph=depsgraph)
        if not mesh.polygons:
            continue
        review_obj = bpy.data.objects.new(f"Review {name}", mesh)
        scene.collection.objects.link(review_obj)
        review_obj.matrix_world = evaluated.matrix_world.copy()

        coords = np.empty(len(mesh.vertices) * 3, dtype=np.float32)
        mesh.vertices.foreach_get("co", coords)
        matrix = np.asarray(review_obj.matrix_world, dtype=np.float64)
        world = coords.reshape(-1, 3) @ matrix[:3, :3].T + matrix[:3, 3]
        bounds[name] = np.stack((world.min(axis=0), world.max(axis=0)))
    missing = set(tire_names.values()) - bounds.keys()
    if missing:
        raise ValueError(f"Missing evaluated tire geometry in {collection_name!r}: {sorted(missing)}")
    if bounds.keys() == set(tire_names.values()):
        raise ValueError("The review collection needs body geometry as well as tires")
    return scene, bounds


def measure(bounds, tire_names, mm_per_unit):
    tire = {wheel: bounds[name] * mm_per_unit for wheel, name in tire_names.items()}
    axle = {wheel: box.mean(axis=0) for wheel, box in tire.items()}
    fl, fr, rl, rr = (axle[wheel] for wheel in WHEELS)
    sides = [fl[0] - rl[0], fr[0] - rr[0]]
    tracks = [fl[1] - fr[1], rl[1] - rr[1]]
    if min(*sides, *tracks) <= 0:
        raise ValueError("Wheel positions disagree with the +X front, +Y left axis convention")

    boxes = np.array(list(bounds.values())) * mm_per_unit
    lower, upper = boxes[:, 0, :].min(axis=0), boxes[:, 1, :].max(axis=0)
    length, width, height = upper - lower
    diameters = {wheel: box[1, 2] - box[0, 2] for wheel, box in tire.items()}
    measurements = {
        "length": [length],
        "width": [width],
        "height": [height],
        "wheelbase": sides,
        "front_track": [tracks[0]],
        "rear_track": [tracks[1]],
        "front_tire_diameter": [diameters["front_left"], diameters["front_right"]],
        "rear_tire_diameter": [diameters["rear_left"], diameters["rear_right"]],
        "front_overhang": [upper[0] - (fl[0] + fr[0]) / 2],
        "rear_overhang": [(rl[0] + rr[0]) / 2 - lower[0]],
    }
    return measurements, {wheel: center.tolist() for wheel, center in axle.items()}


def compare(measurements, targets):
    unexpected = set(targets) - measurements.keys()
    if unexpected:
        raise ValueError(f"Unknown dimension keys: {sorted(unexpected)}")
    checks = {}
    for key, values in measurements.items():
        target = targets.get(key)
        check = {"actual_mm": [round(float(v), 3) for v in values], "status": "unverified"}
        if target is not None:
            expected = number(target["target_mm"], f"{key}.target_mm", minimum=1e-6)
            errors = [v - expected for v in values]
            check.update(
                target_mm=expected,
                error_mm=[round(float(v), 3) for v in errors],
                status="measured",
            )
            if target.get("tolerance_mm") is not None:
                tolerance = number(target["tolerance_mm"], f"{key}.tolerance_mm", minimum=0)
                check["tolerance_mm"] = tolerance
                check["status"] = "pass" if all(abs(v) <= tolerance + 1e-6 for v in errors) else "fail"
        checks[key] = check
    # Summarize the targets in the brief. Other dimensions are still reported as actuals.
    statuses = {checks[key]["status"] for key, target in targets.items() if target is not None}
    for status in ("fail", "measured", "pass"):
        if status in statuses:
            return status, checks
    return "unverified", checks


def material(name, color, roughness, metallic):
    mat = bpy.data.materials.new(name)
    if mat.node_tree is None:
        mat.use_nodes = True
    shader = mat.node_tree.nodes.get("Principled BSDF")
    shader.inputs["Base Color"].default_value = (*color, 1)
    shader.inputs["Roughness"].default_value = roughness
    shader.inputs["Metallic"].default_value = metallic
    return mat


def area_light(scene, name, center, span, offset, length, width, energy):
    data = bpy.data.lights.new(name, "AREA")
    data.shape = "RECTANGLE"
    data.size = length * span
    data.size_y = width * span
    data.energy = energy * span**2
    light = bpy.data.objects.new(name, data)
    scene.collection.objects.link(light)
    light.location = center + Vector(offset) * span
    light.rotation_euler = (center - light.location).to_track_quat("-Z", "X").to_euler()
    return light


def setup_scene(scene, frame, mm_per_unit, samples):
    scene.render.engine = "CYCLES"
    scene.cycles.device = "CPU"
    scene.cycles.samples = samples
    scene.cycles.use_denoising = True
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGBA"
    scene.render.film_transparent = True
    scene.world = bpy.data.worlds.new("Review world")
    if scene.world.node_tree is None:
        scene.world.use_nodes = True
    scene.world.node_tree.nodes.get("Background").inputs["Strength"].default_value = 0.35

    scene.camera = bpy.data.objects.new("Review camera", bpy.data.cameras.new("Review camera"))
    scene.collection.objects.link(scene.camera)
    center = Vector(frame["center_mm"]) / mm_per_unit
    span = frame["ortho_scale_mm"] / mm_per_unit
    clay_lights = [
        area_light(scene, "Clay key", center, span, (0.6, 0.7, 0.85), 0.65, 0.6, 14),
        area_light(scene, "Clay fill", center, span, (-0.45, -0.5, 0.65), 0.5, 0.45, 9),
    ]
    strips = [
        area_light(scene, "Roof strip", center, span, (0.1, -0.34, 0.8), 1.1, 0.06, 12),
        area_light(scene, "Shoulder strip", center, span, (-0.14, 0.65, 0.38), 1, 0.045, 7),
        area_light(scene, "Side strip", center, span, (0.2, 0.58, 0.05), 0.84, 0.035, 4.5),
    ]
    return clay_lights, strips


def render(scene, name, frame, mm_per_unit, path):
    center = Vector(frame["center_mm"]) / mm_per_unit
    span = frame["ortho_scale_mm"] / mm_per_unit
    direction = Vector(VIEWS[name]).normalized()
    camera = scene.camera
    camera.location = center + direction * (1.9 * span)
    camera.rotation_euler = (center - camera.location).to_track_quat("-Z", "Y").to_euler()
    if name == "top":
        camera.rotation_euler = (0, 0, -math.pi / 2)
    camera.data.type = "ORTHO" if name in ORTHOGRAPHIC else "PERSP"
    camera.data.ortho_scale = span
    camera.data.lens = 60
    camera.data.clip_start = span * 0.001
    camera.data.clip_end = span * 20
    scene.render.resolution_x, scene.render.resolution_y = frame["size_px"]
    scene.render.resolution_percentage = 100
    scene.render.filepath = str(path)
    bpy.ops.render.render(write_still=True, scene=scene.name)


def read_rgba(path, size):
    image = bpy.data.images.load(str(path), check_existing=False)
    try:
        if tuple(image.size) != tuple(size):
            raise ValueError(f"{path} is {tuple(image.size)} pixels. Expected {tuple(size)}")
        pixels = np.empty(size[0] * size[1] * 4, dtype=np.float32)
        image.pixels.foreach_get(pixels)
        return pixels.reshape(size[1], size[0], 4)
    finally:
        bpy.data.images.remove(image)


def make_overlay(reference, model, path, size):
    pixels = read_rgba(reference, size)
    mask = read_rgba(model, size)[:, :, 3] >= 0.5
    padded = np.pad(mask, 1)
    height, width = mask.shape
    interior = mask.copy()
    for row, col in ((0, 1), (2, 1), (1, 0), (1, 2)):
        interior &= padded[row:row + height, col:col + width]
    color = [0.0, 0.87, 1.0]
    pixels[:, :, :3][mask] = 0.82 * pixels[:, :, :3][mask] + 0.18 * np.array(color)
    pixels[:, :, :3][mask & ~interior] = color
    pixels[:, :, 3] = 1
    image = bpy.data.images.new("Reference overlay", width, height, alpha=True)
    try:
        image.pixels.foreach_set(pixels.ravel())
        image.filepath_raw = str(path)
        image.file_format = "PNG"
        image.save()
    finally:
        bpy.data.images.remove(image)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--stage", required=True, choices=["proportions", "surface"])
    parser.add_argument("--samples", type=int, default=24)
    args = parser.parse_args(sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else [])
    if args.samples < 1 or not bpy.data.filepath:
        parser.error("Open a .blend and use at least one render sample")

    config_path = args.config.resolve()
    config = json.loads(config_path.read_text(encoding="utf-8-sig"))
    mm_per_unit = number(config["mm_per_unit"], "mm_per_unit", minimum=1e-6)
    frame = camera_frame(config["frame"])
    references = config.get("references", {})
    if set(references) - ORTHOGRAPHIC:
        raise ValueError("Overlays support front, rear, left, and top references")
    view_frames = {name: camera_frame(ref, frame) for name, ref in references.items()}
    ref_paths = {name: config_path.parent / ref["image"] for name, ref in references.items()}
    for name, path in ref_paths.items():
        read_rgba(path, view_frames[name]["size_px"])

    scene, bounds = snapshot_car(bpy.context.scene, config["collection"], config["tires"])
    measurements, centers = measure(bounds, config["tires"], mm_per_unit)
    status, checks = compare(measurements, config.get("targets", {}))
    lights, strips = setup_scene(scene, frame, mm_per_unit, args.samples)
    layer = scene.view_layers[0]
    layer.material_override = material("Review clay", (0.47, 0.47, 0.47), 0.73, 0)
    for strip in strips:
        strip.hide_render = True

    output = args.out.resolve()
    output.mkdir(parents=True, exist_ok=True)
    report_path = output / "review.json"
    if report_path.exists():
        raise ValueError("Use a new output directory for each review")
    images = []
    for name in VIEWS:
        path = output / f"clay_{name}.png"
        current_frame = view_frames.get(name, frame)
        render(scene, name, current_frame, mm_per_unit, path)
        images.append(path.name)
        if name in ref_paths:
            overlay_path = output / f"overlay_{name}.png"
            make_overlay(ref_paths[name], path, overlay_path, current_frame["size_px"])
            images.append(overlay_path.name)

    if args.stage == "surface":
        layer.material_override = material("Review gloss", (0.30, 0.30, 0.30), 0.16, 0.72)
        scene.world.node_tree.nodes.get("Background").inputs["Strength"].default_value = 0.08
        for light in lights:
            light.hide_render = True
        for strip in strips:
            strip.hide_render = False
        for name in ("front_three_quarter", "rear_three_quarter", "left"):
            path = output / f"gloss_{name}.png"
            render(scene, name, view_frames.get(name, frame), mm_per_unit, path)
            images.append(path.name)

    report = {
        "blend": bpy.data.filepath,
        "config": str(config_path),
        "stage": args.stage,
        "dimension_status": status,
        "dimensions": checks,
        "wheel_centers_xyz_mm": centers,
        "default_frame": frame,
        "reference_frames": view_frames,
        "reference_paths": {name: str(path) for name, path in ref_paths.items()},
        "proportion_visual_review": "pending",
        "surface_visual_review": "pending" if args.stage == "surface" else "not_requested",
        "images": images,
    }
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"Dimension check: {status}. Review images and report: {output}")


if __name__ == "__main__":
    main()
