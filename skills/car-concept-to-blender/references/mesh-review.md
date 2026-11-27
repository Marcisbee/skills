# Measure the Blender mesh

Use the bundled [review_car.py](../scripts/review_car.py) after concept approval when a build needs repeatable measurements. It reads a saved Blender scene, builds a temporary review scene in memory, and writes a JSON report and images to a separate folder. For a simple brief, measuring directly in Blender is also sufficient.

## Prepare the scene

Use an exterior collection containing the body and four separate tire objects. Include the parts that count toward the specified dimensions. Keep floors, backup shells, and mesh helpers outside the collection. If the asset uses instances or different axes, prepare a review copy with the visible exterior realized and the nose along +X, vehicle left along +Y, and up along +Z. Use the same units, axes, and width convention for each revision.

The script uses world-space bounds of evaluated geometry. It takes each axle position from the center of the tire's bounding box and tire diameter from its vertical extent. For heavily deformed tires or wheels at an angle, measure from the actual hub centers in Blender.

## Configure the check

Save a project JSON file like this one. These example dimensions describe a fictional brief. Replace them with project values and record their sources alongside the file.

```json
{
  "collection": "Car Exterior",
  "mm_per_unit": 1000,
  "tires": {
    "front_left": "Tire.FL",
    "front_right": "Tire.FR",
    "rear_left": "Tire.RL",
    "rear_right": "Tire.RR"
  },
  "frame": {
    "center_mm": [0, 0, 650],
    "ortho_scale_mm": 5200,
    "size_px": [768, 768]
  },
  "targets": {
    "length": {"target_mm": 4400},
    "wheelbase": {"target_mm": 2520, "tolerance_mm": 5},
    "front_overhang": {"target_mm": 860},
    "rear_overhang": {"target_mm": 1020}
  }
}
```

Use 1000 millimeters per scene unit for geometry modeled in meters. Other supported targets are `width`, `height`, `front_track`, `rear_track`, `front_tire_diameter`, and `rear_tire_diameter`. Omit unknown targets. The report gives actual minus target in millimeters. A supplied tolerance yields a pass or fail. Without a tolerance, the report gives the difference and leaves acceptance to the brief.

For a silhouette overlay, add a top-level `references` map with an entry such as `"left": {"image": "refs/left.png"}`. Paths are relative to the JSON file. Supported views are `left`, `front`, `rear`, and `top`. Align the reference to known landmarks such as the wheel centers. Its image size, world center, and orthographic span must match the render. A view can override `size_px`, `center_mm`, and `ortho_scale_mm` from the default frame. The span covers the longer image dimension. The nose points left in the left view and up in the top view. Use the approved concept camera separately for perspective comparisons.

## Run and read the review

From the project folder, substitute the path to the bundled script and use a fresh output folder for each run.

```text
blender --background blockout.blend --python-exit-code 1 --python path/to/scripts/review_car.py -- --stage proportions --config car-review.json --out review/blockout
blender --background finished.blend --python-exit-code 1 --python path/to/scripts/review_car.py -- --stage proportions --config car-review.json --out review/finished
```

Read `review.json` and open the renders. A tolerance failure is recorded in the report even when the command succeeds. Wheelbase is measured on both sides, and tire diameters are measured per wheel. Inspect any overlays for local silhouette differences that overall dimensions miss. Use `--stage surface` on either run to add three glossy strip-light views for judging surface flow.
