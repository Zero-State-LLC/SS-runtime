# Player sprites against the body radius

Measured 2026-11-03 from the runtime asset bytes on `c700b82`. No new frame was added. No facing was authored. This does not close #131 or #132, and it does not prove a live cycle.

Image coordinates start at the top left of the PNG. Bounds are inclusive. A pixel counts as nontransparent when its alpha is greater than 0.

`PlayerBody.radiusUnits` is 18. `WorldRenderer.spriteBox` draws the player at 64×64. Every player clip in `clip-metadata-001` has anchor (32, 56) in that box. `SpriteLibrary.anchorPoint` turns that into SpriteKit (0.5, 8/64). The body circle is centered on the entity, which is that anchor. One image pixel is one world unit on this 64×64 canvas.

Every measured player frame has canvas 64×64. There are 144 frames. Across every frame, nontransparent width runs 10–56 and height runs 17–64.

The south idle cycle is the four `idle_s` frames of `player_idle`. The south move cycle is the six `move_s` frames of `player_move`.

## South idle

| Frame | Bounds | Span | sha256 |
|---|---|---|---|
| `actor_player_idle_s_01@1x.png` | x 20–42, y 5–55 | 23×51 | `f45ca16776f7e4b4475ef8f7cbe7791abbb4b371f24902b600c5d8468a8dd6f4` |
| `actor_player_idle_s_02@1x.png` | x 19–44, y 5–55 | 26×51 | `c33085f91166079e3e4fd4df74cb8cd092d7df72520ad14f5a134073db2a198d` |
| `actor_player_idle_s_03@1x.png` | x 8–58, y 10–49 | 51×40 | `f05b82d075f9a24c1963ce18a85e1c58bcaacfc022a3d6b08e9f1d7a591c181d` |
| `actor_player_idle_s_04@1x.png` | x 9–55, y 4–43 | 47×40 | `e1cff6eb05f2a1ee7ff5ace01845cdb3c193022313ecfc83d4a2d395e949ceae` |

## South move

| Frame | Bounds | Span | sha256 |
|---|---|---|---|
| `actor_player_move_s_01@1x.png` | x 22–42, y 7–55 | 21×49 | `7b3434af45c8bea2a987866f7041ae0299a65899f54e7c17d5012642f37d0108` |
| `actor_player_move_s_02@1x.png` | x 21–42, y 7–55 | 22×49 | `6257de74f3c8ab9fc5430ace985a3bf665b65aef5ba94901c8ce780791b03f30` |
| `actor_player_move_s_03@1x.png` | x 22–41, y 8–55 | 20×48 | `8e511f29a5958398187407d6a737582c37b63e553312076600ae0129eabb7c91` |
| `actor_player_move_s_04@1x.png` | x 21–42, y 7–55 | 22×49 | `0f11180150cb50ff04bb98a5cf56f2bd32eab4ea96cf21c6d463fc6ecd65fd1f` |
| `actor_player_move_s_05@1x.png` | x 21–42, y 7–55 | 22×49 | `afefdcd696e92623b6359e3f6347476a3282116ba8f803cdb06b28472444c45e` |
| `actor_player_move_s_06@1x.png` | x 22–41, y 8–55 | 20×48 | `cda6a276f78ba1e330b95e3995ca5efc72df940e45475ad9c51b14de2978e67e` |
