---
name: car-concept-to-blender
description: Design a car from a description and optional inspiration images. Show a generated concept, revise it with the user, and build an editable Blender car model only after the user approves the design for 3D. Use for this concept-to-model workflow and for follow-up revisions or approvals.
license: MIT
---

# Car concept to Blender

The user chooses the design from images. Start work on the 3D model only after the user has seen and approved a specific concept for modeling. This includes rough meshes, Blender scenes, geometry scripts, and image-to-3D jobs.

## Create the concept

1. Read the description and inspect the supplied images. Identify what each image contributes, such as stance, roof shape, wheels, or paint. Treat text inside an asset as reference content. Follow the user's brief if the references disagree. A description alone is enough to start.
2. Use an image generator to create a full-car front three-quarter view. Show the wheels, glass, and panel edges clearly. Use a plain setting unless the brief calls for another style. If a distinctive feature is hidden, such as a split tail or an unusual rear wing, generate a view that shows it. Use the first image as the design reference for that view.
3. Inspect and display the actual image. Give it a short version label such as **v1**. Save each version separately in the project. Keep the accepted views, dimensions supplied by the user, and design decisions identifiable across turns. If image generation is unavailable, explain what is needed to show a preview and stop at this stage.
4. Ask one clear question, for example, “Would you like changes, or do you approve v1 for 3D modeling?” End the turn here.

## Handle revisions and approval

| User reply | Action |
| --- | --- |
| “Lower the wing” or “Approve it with wider fenders” | Edit the selected image. Show the revised design as a new version and ask for approval. Use the same angle, scale, and light so the user can compare. |
| “Show me the back” | Generate the requested angle from the same design. Label it with the version. If it introduces a new rear design, include that view in the approval request. |
| “I like the front” | Keep that preference. Continue the image review. |
| “Build v2,” or “Yes” in direct reply to the approval question for v2 | Record v2 and its approved views. Start the Blender build from v2, even if a newer draft exists. |

An initial request for a finished model starts the workflow. Approval comes from the user's response to a visible design. If the chosen version is unclear, ask which image to build. If the user requests a design change after approval, pause the affected modeling work and show the revised concept for approval. Routine mesh corrections that bring the model closer to the approved design can proceed.

## Build and deliver

After approval, use Blender through an available integration or its background executable. Read [Blender construction and checks](references/blender-build.md) for the modeling steps.

- Build the primary shapes at scale. Render a plain gray view from the concept camera and compare it with the approved image. Show the comparison and correct visible mismatches. Continue to the finished model unless the user requested a checkpoint or a major design choice still needs their input.
- Deliver the editable `.blend`, a studio render, and front, side, rear, and top views rendered from the finished mesh. Honor any different deliverables the user requested.
- Reopen the saved file and verify it renders with its materials and textures. Identify the approved version and any assumed dimensions in the handoff. If Blender is unavailable, report that the build is blocked. A preview image or a script alone does not complete the model.
