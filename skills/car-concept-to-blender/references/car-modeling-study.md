# Car modeling study

Use these observations from 40 mesh views and finished renders to turn a car brief into visible, testable features. The image numbers refer to the original study. Each example below describes what to look for and can be used without the images. The user's brief determines the style.

## Choose the features that define the car

| Study example | What gives the car its character | Where to check it |
| --- | --- | --- |
| White supercar, 1–2 | The nose dips between high front fenders. The thin headlamp outlines and dark sill emphasize the low body. A tall dark roof intake and a thin rear lamp line identify the tail. | In a low front view, both fender crowns should stand above the middle of the nose. In a rear view, check the intake against the roof outline. |
| Yellow muscle coupe, 3–11 | The cabin sits well behind the front axle. Deep tire sidewalls, a raised hood center, and a long door crease give the car its proportions. Four rear lamps flank the plate recess. | Check the cabin position and tire profile from the side. Compare the hood ridge in plain shading (7) with the highlight on the painted car (10). |
| Gray square coupe, 12–17 | Upright pillars, narrow rear side glass, and a gently crowned roof sit over straight sides. Two hood ridges lead to a rectangular grille. The rear lamp band wraps around the corners. | Check the glass and trunk outline from the rear three-quarter view. Check that the hood ridges catch light and that the roof still has curvature. |
| Revised blue supercar, 18–22 | The redesign replaces round lamp pockets and a broad intake with tapered lamps and framed intake blades. Slim outer tail lamps and four central exhaust tips sit above deep diffuser channels. | Compare the front and rear in the same clay material for both revisions. Check the spacing and depth of the blades, lamps, exhausts, and fins. |
| Orange fastback and white widebody, 23–40 | A narrow cabin tapers into broad rear shoulders. The revised base has recessed rectangular lamps, a hood recess, three rear lamp elements per side, and a low wing. The kit adds bolted flares, a splitter, deeper side skirts, and a second wing blade. | Look across the roof and rear arches from above. Compare the base and kit from the same front angle (35 and 40). The shared openings should still line up. |

For a new design, write down the few features that must survive a change of camera. Include the axle and cabin positions, roof and side-glass outline, arch shape, lamp count, and wheel design as relevant. Assign each inspiration image a job. For example, use a mesh view for the fender section and a painted view for its finish. Combine features from different cars when the brief calls for it.

## Generate consistent references

Before approval, use images for the design review. Give each new image one job. A front three-quarter view shows the face and stance. A full side elevation shows axle position and roof profile. A rear view can settle the lamp layout and wing design. Keep the wheels straight in measurement views. Use even light, a plain background, and enough margin to see the complete car.

An example of a fixed design description is “late-1980s GT, one door per side, narrow center pillar, triangular rear side glass, rectangular headlamps, five-spoke wheels, and a short rear lip.” Carry these features into each prompt. Check the resulting image against the approved or current concept, including the far-side lamp and wheel. If the generator changes a fixed feature, correct the view before using it.

After the user approves a design and a measured Blender blockout exists, use two inputs for additional reference images. For example, “Image A defines the car design. Image B is the rear view from the measured blockout. Match B's camera, wheel centers, and framing. Keep A's roof, lamp count, and body width. Show the entire car in even light.” Request one angle at a time. For a lamp or arch detail, crop the design reference and identify the edges and parts that must remain visible.

### Measure a side reference

Use a side elevation with minimal perspective. Divide the known wheelbase in millimeters by the distance in pixels between hub centers. Use that scale to measure each overhang. In the study GT, 2,520 mm divided by 1,246 px gives about 2.02 mm/px. The image measures about 4,260 mm long against a 4,400 mm target. The measured front and rear overhangs are about 930 and 820 mm. The targets are 860 and 1,020 mm. With both axles fixed, shorten the nose and extend the tail. A uniform scale change would also move the hubs.

Use track width to scale an end view. Check the ground line and roof height across views. If generated views disagree, use the specified dimensions and render side, front, rear, and top views from one corrected shell. Use the same orthographic scale and image settings for each view. The example GT dimensions apply only to that example.

## Model quality checks

Use these checks after design approval. Judge each part at the closest camera distance the user needs.

| Inspect | Method and acceptance check |
| --- | --- |
| Proportions | Place the tires at the chosen wheelbase and track. Render the plain gray shell from the concept angle. Compare the wheel gaps, overhangs, roof height, cabin position, and nose height. Then inspect the top and both ends for width errors that the concept camera hides. |
| Fender and shoulder | Follow the arch opening in side view, the body width in top view, and the section from glass to tire in end view. Place the highest point of the crown and the widest point of the fender independently. Turn the arch lip inward. Let the tire sit behind it with visible clearance. |
| Surface flow | For a symmetric smooth shell, start with a simple half mesh. Enable Merge and Clipping in Mirror. Put Subdivision Surface after Mirror and start at level 1. Use widely spaced rows on gentle curves. Add support near a crease or opening. Keep vertices where many edges meet away from broad highlights. Sweep a long white reflection over the glossy gray hood, fender, and door. Correct unintended pinches or steps in the mesh. |
| Panel fit | Preserve the continuous shell before separating a door. Turn both cut edges inward and check that the reflection continues when the door is closed. A 3 mm gap is a starting example for a full-size car. For an opening door, model the painted return, seal, sill, and visible inner trim. Rotate the door at the hinge and inspect clearance. |
| Wheels and brakes | Give the tire a sidewall profile, the rim a lip, and the hub a recess. Repeat one spoke sector when the pattern allows. Place the disc behind the spokes and check the caliper against the inner rim. Look through the wheel from the final camera. Check tire contact with the floor. |
| Lamps, ducts, and cabin | Give lamp housings an inner wall, optics, and a clear outer lens. Check them with emission off. Give visible intake blades and diffuser fins thickness and space behind them. Recess the gauge faces behind their rims. Use textures for printed marks. Use material roughness to distinguish the steering grip, dash, and gauge glass. |
| Base car and body kit | When both variants are requested, finish the common shell first. Keep the flare, splitter, skirt, and extra wing blade editable as separate parts. Compare both cars at the same angle. Check arch clearance and how the ends of add-on parts meet the existing panels. |
| Materials and presentation | For solid yellow or orange paint, try a Principled BSDF with Metallic 0, Roughness 0.30, Coat Weight 1, and Coat Roughness 0.12. Tune it under a long rectangular Area light above and to the side. Add weaker fill until the tire, intake walls, and trim are distinct. Use thickness and transmission for glass. Put visible seats and a dash behind it. Place scuffs and dirt at exposed fasteners, flares, and sills when the finish calls for wear. |
| Final render | A low 70 mm camera on a 36 mm sensor is a starting point for a studio view. Move it back to frame the whole car. A higher view reveals the roof taper and deck. For comparisons, keep the camera and exposure fixed. Check the finished car with the wire overlay off, at delivery size, on a matte floor with visible tire contact shadows. |

## Find a detail in the original study

| Images | Details to inspect |
| --- | --- |
| 1–2 | Nose height between the front crowns, roof intake, and rear lamp outline. |
| 3–6 | Mesh rows around four front openings, inset tail panel, paired rear lamps, and the inner door with crank, armrest, and painted edge. |
| 7–11 | Hood ridge in clay and paint, bumper wrapping a rear corner, door sill and pedals, and the reflection above the rear wheel. |
| 12–17 | Side rows meeting the arch, wraparound rear lamp, seat base and steering column, spoke pattern and hub depth, hood ridges, and squared trunk. |
| 18–22 | Central exhaust recess, before-and-after front and rear designs, projector depth, and the dark deck and diffuser against blue paint. |
| 23–26 | Front lamp recess below the crown, rear arch rows spreading into the shoulder, narrow glass between wide fenders, and roof taper from above. |
| 27–32 | Splitter, flare, brake disc, side panels, and two wing elements. The front and rear comparisons distinguish the headlamp and deck redesign from the later kit. |
| 33–36 | Front and rear fender reflections, fog lamp depth, and the sill, seat, and dash visible through the open door. |
| 37–40 | Flare fasteners and local wear, decal placement, gauge rims and pedals, and the change in front width compared with image 35. |
