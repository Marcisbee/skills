# Bodies, garments, and fit checks

Use this guide after concept approval. Work in a new asset file or version. Preserve the original character files.

## Build a reusable character

1. Fit a base mesh to the approved body views. Use the supplied height or record an assumed scale. Compare the gray mesh in front and side views. Match shoulder width, chest and seat depth, limb length, and foot size before adding accessories.
2. Keep the complete body in the source file. Make the underlayers, clothing, hair, and equipment separately editable as appropriate. Use reversible body masks for skin fully covered by an outfit. Check cuffs, collars, and hems in motion and with the outfit removed.
3. Place the skeleton at the character's joint pivots. Bind the body and adjust the weights at the shoulders, elbows, hips, and knees. For a humanoid that must hold a prop or plant a foot, add an IK target for the contact and a control for the elbow or knee direction. Give the animator a way to release the contact for free motion. Attach rigid gear to the bone that carries it.
4. Match the approved finish at the intended camera distance. For the rider style, keep large folds in the silhouette, a few visible seams, and distinct responses for skin, cloth, rubber, and a hard shell. Recheck the face and hands in the closest requested shot.
5. Save the body and rig as a fitting reference. Include a body ID or name, revision, rest pose, scene units, and a front and side preview. These identify the target when another outfit is requested.

## Fit one garment to several bodies

Start with the actual target bodies in their rest poses. Check scale, transforms, rig, and garment layers. If characters have different rest poses, align fitting copies before transferring a garment and verify it on each original rig. A shared skeleton can help transfer weights. Check each body's shoulder slope, waist, hips, and limb length separately.

| Decision | Fitting method |
| --- | --- |
| A fitted shirt or gloves | Shape the garment close to the body. Transfer weights from the matching body as a starting point. Inspect fingers, armpits, and inner thighs for weights picked up from a nearby surface. |
| A loose coat, skirt, or layered outfit | Fit the outer garment over the intended underlayer. Preserve space for motion and the approved silhouette. Give hems thickness where visible. Use extra controls or cloth simulation if the brief needs secondary motion. |
| A helmet, buckle, or hard plate | Keep the part rigid. Test its clearance against nearby moving surfaces. For an opening visor, rotate it around the hinge and check the nose and shell. |
| Bodies with close proportions and matching garment topology | Keep one editable garment mesh with named fit shapes when practical. Test the active shape with each wearer's skin weights and rig. |
| Bodies with substantially different proportions or rigs | Keep a named fit variant per body. Share the material and design details where practical. Adjust panels, openings, and weights on the variant. Preserve the original wearer and garment design. |

For example, a rain jacket on a broad mechanic may need a wider back panel and more room around the upper arm than the courier's jacket. Keep the zipper, pockets, and hem treatment recognizable on both. Check overhead reach before accepting either fit.

## Inspect and record each fit

Equip the garment on the saved target body with its intended layers. Inspect the rest pose and a short action at the delivery camera distance. For a jacket, reach forward, lift an arm, and sit. For trousers, sit and take a long step. Choose poses that stress the actual item.

Inspect skin and underlayers for clipping, joints for collapse, and fasteners for distortion. Check the transition between poses as well as the endpoints. For a rider, move the torso while both hands hold the grips. Inspect palms relative to the handles, then release one hand. Correct defects and replay the same action on that body.

Record the garment and concept version, layer, target body and revision, fitted object or shape, poses tested, result, and any limits. Distinguish a passed fit, a fit with a known issue, and an untested target. A concept sheet or a successful test on one wearer establishes no fit result for another.

Reopen the editable `.blend` with its textures. Equip and remove each requested garment or fit variant. Confirm the complete body is available, the rig still poses, and the reported checks match the saved asset. Include a fitted preview for each tested wearer. If game export was requested, also check the export in the named target.
