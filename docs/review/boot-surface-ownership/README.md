# Boot surface ownership correction

Status: authored source study, not finished art or a replacement character sheet.

The user rejected laces on the wrong boot surface. The two generated recovery components remain rejected. This study adds distinct tongue/instep and front-shaft geometry to the existing editable recovery volume, with lace ribbons assigned only to those surfaces. Heel/back/sole faces receive no lace paint. No original costume pixels were copied across surfaces.

Research: Nicks Boots glossary (https://nicksboots.com/pages/glossary), retrieved 2026-10-15, describes the tongue as cushioning the top of the foot and distributing lace pressure. Its false-tongue explanation (https://nicksboots.com/blogs/blog/boot-building-specs-kiltie-reddit-wiki) places that protection over the tongue beneath lacing. These establish construction relationships, not SS dimensions, gait or camera choices.

Spec authority: d602775 controlled-character-source.md already requires explicitly authored hidden surfaces, boot perspective and reviewed source keys before in-betweening. This is a source correction under that existing requirement, not a new gameplay or presentation policy.

orientation.py exports named OBJ groups, a surface-ownership record and four depth-buffered diagnostic views. It inherits the prior authored pose without claiming anatomical correctness. The elevated front view hides the laces; the low diagnostic view reveals the forward shaft tongue. This is expected occlusion, not permission to paint laces onto visible rear surfaces. The shaft/foot transition, proportions and full-body recovery silhouette remain unresolved. The isolated model is visibly a proxy and cannot satisfy benchmark art acceptance.

Reproduction: Python 3 with NumPy and Pillow, run orientation.py in this folder. In this session the bundled desktop Python was used. Checks passed for the inherited closed volume and explicit forward-facing shaft placement. Lace/tongue overlays are intentionally open polygons; the exported assembly is not a manifold production mesh. Four views were inspected; no runtime, simulator or device claim follows. No active game code/resources/spec pins changed.

Next: refine the connected ankle/boot transition and apply the retained costume materials only to their owned surfaces; review assembled beneath the knee and coat before expanding the cycle.

## Full-character placement follow-up

fullpose-comparison.png uses the prior guide projection (origin 192,336, scale 6, elevation 30 degrees) without fitting the new mesh to the painting. Left: retained contact. Middle: source behind all retained pixels. Right: source over paint to expose overlap. The raised knee and projected boot do not form a convincing connected silhouette yet; this is diagnostic evidence, not an assembled art pass. The original image is included for reproduction. The next correction must address this joint/occlusion relationship before texture work.
