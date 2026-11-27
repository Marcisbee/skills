---
name: character-concept-to-blender
description: Design a character or interchangeable clothing for one or more characters. Show a rider-style game-art concept, revise it with the user, and build the approved design in Blender. Use for reusable rigged bodies, outfits, and garments fitted to named existing characters.
license: MIT
---

# Character and wardrobe concepts for Blender

Start with an image. Build in Blender only after the user sees and explicitly approves a specific concept for 3D. This applies to both characters and clothes, including rough meshes, rig generation, fitting scripts, and image-to-3D jobs.

## Show the concept

Use the [rider-style example](assets/rider-style-example.png) as a style input to the image generator. It shows the level of detail and a useful review layout. Take identity, proportions, clothing, equipment, and colors from the brief. Use smooth skin shading, simple hair masses, broad fabric folds, and a few distinct material highlights. Frame the full figure in soft light against a neutral studio background. Inspect the silhouette at full-body size. If the user chooses another art style, follow it.

Choose the review views to suit the request.

- **New character.** Generate a dressed three-quarter view and front and side views of the same base body in plain, opaque, close-fitting underlayers. Keep the body views barefoot when foot shape matters. Align the floor and use the same body scale. Account for helmet and sole thickness in the dressed view. Check face, build, and limb proportions across views. For a character and wardrobe requested together, identify the character and each garment included in the review.
- **Clothing for existing characters.** Identify the intended wearers and layer, such as a coat worn over a uniform. Use each character's saved design image or existing model preview to preserve its identity and proportions. Show the same garment on each target, in comparable poses and framing. Label each wearer. Preserve the garment's cut, color, fasteners, and pocket layout across fits. Use another sheet if the figures become too small to compare. If a wearer lacks a reference, identify the missing input. A sample body can illustrate the garment concept, but its proportions cannot establish fit for that wearer.

Display the actual generated image or sheets and label the version, such as **Rain jacket v2 — courier and mechanic**. Save the views so the approved design can be found again. Ask a direct question such as “Do you approve this jacket for both characters, or would you like changes?” Stop for the answer. If an image generator is unavailable, report the missing capability and stop before the build.

## Handle revisions and approval

| User response | Action |
| --- | --- |
| “Widen the collar” or “Approved, but shorten the sleeves” | Edit the current concept, show the new version on the affected wearers, and ask again. |
| “Looks good on the courier” | Record the preference. Clarify build approval and scope if they remain unclear. |
| “Build v2 for the courier only” | Record the approved version and wearer. Build only that fit. |
| “Yes” to the approval question above | Record that version and both wearers. Proceed with the approved work. |

An initial request to make a model starts concept review. A bundled example is never a user's approval. If the user later requests a visible design change, show it for approval before changing the affected asset. Routine mesh and weight corrections that match the approved design can proceed.

## Build and deliver

Use Blender through an available integration or background executable. Read the [body, garment, and fit guide](references/blender-fit.md). For character work, keep a complete reusable body and a rig. For wardrobe work, keep one garment design and deliver a tested fit for each approved body. A new wearer can be fitted later using its own body and rig.

Deliver the editable Blender assets, a preview of the approved design, and the fit results for the requested wearers. Reopen the saved files and verify them. If Blender or a target body is unavailable, report exactly which work is blocked or untested. Keep concept images and tested fit results clearly identified.
