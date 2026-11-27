# Blender construction and checks

## Set the dimensions

Use the user's dimensions first. For a fictional car with no measurements, choose plausible values for its class and record them as assumptions. Place the wheels at the chosen wheelbase, track width, and tire diameter. Set the ground plane, roof height, and front and rear overhangs. Check that the two overhangs plus the wheelbase equal the overall length.

Use a side image to judge the profile. Use the top and end views to judge body width, cabin taper, and fender width. An image generator can move an axle or change a lens between views. Use the approved image for design intent and the chosen dimensions for measurement. If an explicit measurement and a major approved styling feature conflict, show the conflict before changing the design.

Use the [measured GT example](car-modeling-study.md#measure-a-side-reference) to check a generated side view. Render matched projections from the corrected shell if you need more references.

When the brief specifies dimensions, measure them on the blockout before detailing. Record each target, actual value, signed difference, and any supplied tolerance in millimeters. Check the front and rear overhangs individually when specified. A correct overall length can hide a nose that is too long and a tail that is too short. Use Blender's measurement tools or the [optional mesh review script](mesh-review.md). If you have aligned orthographic references, keep the framing and reference alignment fixed across revisions.

## Build the surfaces

1. Block out the tires, body, and cabin. Match the silhouette and wheel gaps with a camera close to the approved view. Look at the car from above and from both ends. Shape the fender crowns and cabin width in those views.
2. For a symmetric body, model half the shell and use a Mirror modifier. Use a simple control mesh for the large panels. Use subdivision or bevels where the surface needs a controlled curve. Retain asymmetry called for in the design.
3. Establish the fender lip, its outer crown, and the transition into the door. Sweep a long reflected strip of light across the glossy shell. Correct unintended kinks before cutting panel gaps. Keep an editable copy of the continuous surface when splitting it into panels.
4. Give lamp housings, ducts, and wheel wells visible depth. Build the rims, spokes, and brakes as separate parts where visible. Add glass, seals, and enough cabin geometry for the approved views. Match the amount of detail to the requested use and closest camera.
5. Apply paint, glass, rubber, and trim materials. Light the car so the reflections show the major curves. Name and organize the body, wheels, glass, trim, and lights so the user can edit them. For a game asset, also respect any requested geometry budget, texture limits, and export format.

## Verify the saved model

- Repeat the specified measurements on the finished exterior with the same conventions as the blockout (for example, width with mirrors folded or excluded). Include parts added during detailing that affect the targets, such as bumpers or a splitter. Correct discrepancies or report any remaining difference in the handoff.
- Use the [car modeling study](car-modeling-study.md#model-quality-checks) to inspect the surface reflections, component depth, and finish.
- Compare a gray render with the approved image at a similar angle and framing. Check the roofline, axle locations, arch gaps, lamp shapes, and wheel design.
- Inspect the whole car for open seams, shading defects, or wheels that intersect the fenders. Check moving parts in their working positions if the brief calls for them.
- Render front, rear, side, and top views with orthographic cameras. Use the same orthographic scale, resolution, and pixel aspect so distances can be compared across the views. Use a separate perspective camera for the studio render.
- Pack textures into the file or include them with working relative paths. Reopen the delivered file in Blender and render a check frame. Confirm that visible geometry, materials, and camera framing survive the round trip.
