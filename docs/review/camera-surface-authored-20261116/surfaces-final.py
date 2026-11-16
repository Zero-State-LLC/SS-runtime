"""Final bounded surface-only repaint. Every brush path is individually authored.

The complete component contours/root/landmarks are frozen in geometry.json.
No texture generator, noise, random placement, global tint or raster overlay.
Feather is the small soft edge of that named brush mark, in source pixels.
"""
import json
from pathlib import Path
G=json.loads((Path(__file__).parent/'geometry.json').read_text())
CANVAS,ROOT,SCALE,LANDMARKS,HIDDEN=(G[k] for k in ('canvas','root','scale','landmarks','hidden'))


def s(name,color,path,width=0,opacity=255,feather=0):
    return dict(name=name,color=color,path=path,width=width,opacity=opacity,feather=feather)


PAINT={
'foot':[
 s('left_cast_volume','#424442','M 12 394 L 18 399 L 22 401 L 23 420 L 20 422 L 14 417 Z',opacity=210,feather=.45),
 s('front_cast_volume','#333635','M 24 402 C 34 408 52 408 65 403 L 67 423 C 53 430 39 431 26 426 Z',feather=.4),
 s('right_cast_return','#181d1e','M 67 402 L 80 395 L 82 414 L 75 422 L 68 426 Z',feather=.55),
 s('vertical_joint_shadows','#1b2021','M 25 405 L 26 420 M 46 412 L 46 425 M 66 406 L 65 420',1.1,190,.3),
 s('rubbed_foot_edge','#797a6d','M 14 412 L 16 417 L 20 420 M 27 426 L 31 427 M 40 430 L 44 430 M 54 429 L 57 428 M 74 420 L 77 417',.7,200,.15),
 s('cast_small_dabs','#565b54','M 18 403 L 20 404 L 21 407 L 19 408 Z M 33 415 L 35 414 L 36 417 L 34 418 Z M 53 423 L 55 421 L 57 421 L 56 424 L 54 425 Z',opacity=170,feather=.35),
 s('dark_cast_pores','#151b1d','M 21 413 L 22 414 M 39 421 L 41 420 M 58 411 L 59 413 M 72 412 L 73 411',.7,170,.2),
],
'plinth':[
 s('sloping_crown','#575b55','M 17 380 C 27 371 64 371 75 381 L 72 389 C 61 401 31 400 19 390 Z',feather=.5),
 s('crown_left_turn','#73776c','M 20 380 L 25 376 L 28 377 L 25 381 L 24 386 L 27 390 L 31 393 L 29 394 L 23 391 L 20 386 Z',opacity=200,feather=.65),
 s('crown_back_shadow','#2b3230','M 35 373 L 56 373 L 64 376 L 65 381 L 61 386 L 56 389 L 54 386 L 59 381 L 57 378 L 36 377 Z',opacity=210,feather=.6),
 s('right_falloff','#303735','M 68 379 L 74 382 L 73 388 L 64 396 L 58 398 L 62 392 L 68 386 Z',feather=.5),
 s('front_lip','#22292a','M 15 393 C 30 406 62 407 78 393 L 78 398 C 62 414 31 412 16 401 Z',feather=.3),
 s('fine_rolled_rim','#aaa897','M 17 392 C 21 397 29 401 35 402 M 38 403 L 46 404 M 50 404 L 57 402 M 61 401 L 66 398 M 70 396 L 74 393',.8,220,.2),
 s('wear_clouds','#8a8b7a','M 22 383 L 24 382 L 25 384 L 24 387 L 22 388 Z M 30 392 L 33 393 L 34 395 L 31 396 Z M 61 390 L 63 389 L 63 392 L 60 393 Z',opacity=145,feather=.4),
],
'socket':[
 s('left_turn','#4a4f49','M 26 357 L 31 361 L 33 366 L 32 383 L 28 382 L 25 377 Z',feather=.55),
 s('front_cast','#393f3b','M 34 362 C 42 367 51 365 57 361 L 61 383 C 52 389 40 390 34 385 Z',feather=.5),
 s('right_return','#1b2223','M 58 359 L 64 357 L 67 377 L 63 383 L 58 386 Z',feather=.6),
 s('broken_turn_highlight','#74796b','M 28 360 L 29 365 M 29 369 L 29 376 L 31 380 M 34 384 L 38 386',.8,180,.25),
 s('cast_chips','#63695f','M 36 371 L 38 370 L 38 373 L 36 375 Z M 44 381 L 47 380 L 47 383 L 44 384 Z M 55 377 L 56 375 L 57 378 L 56 380 Z',opacity=150,feather=.3),
],
'pole':[
 s('left_curved_mass','#414744','M 29 46 L 34 48 L 34 104 L 33 159 L 34 218 L 32 282 L 34 352 L 32 360 L 29 356 L 30 284 L 29 220 L 30 148 Z',feather=.55),
 s('near_front_plane','#333936','M 35 47 L 44 47 L 45 121 L 44 185 L 43 246 L 45 300 L 44 363 L 36 361 L 35 290 L 36 219 L 35 159 Z',feather=.8),
 s('deep_round_return','#192123','M 49 46 L 60 46 L 59 160 L 60 224 L 59 289 L 60 354 L 53 362 L 51 296 L 52 231 L 50 161 Z',feather=.8),
 s('short_brushed_left_light','#646c61','M 31 53 L 32 61 L 31 75 M 31 85 L 32 93 L 31 107 M 31 118 L 31 130 M 30 171 L 31 184 L 30 197 M 31 204 L 32 213 L 31 225 M 31 244 L 30 251 L 31 264 M 31 273 L 31 280 M 31 314 L 32 324 L 31 337 M 32 346 L 32 353',1.45,145,.65),
 s('front_low_brush','#4b534b','M 38 57 L 39 68 L 38 78 M 39 94 L 38 102 M 38 127 L 39 136 M 38 165 L 39 179 M 38 200 L 39 211 L 38 222 M 39 237 L 39 245 M 38 265 L 39 277 M 39 317 L 40 327 M 39 344 L 40 353',2.4,150,.75),
 s('right_bounce_segments','#3e4944','M 58 103 L 58 119 M 58 130 L 57 141 M 58 180 L 58 193 M 58 204 L 58 216 M 57 260 L 57 274 M 58 335 L 57 351',.85,180,.35),
 s('material_breaks','#20292a','M 34 116 L 37 114 L 37 118 L 35 121 L 35 128 L 33 129 Z M 42 183 L 45 181 L 44 188 L 42 191 Z M 35 297 L 38 296 L 37 302 L 35 304 Z M 40 252 L 42 250 L 43 254 L 41 257 Z',opacity=180,feather=.45),
 s('hand_placed_cast_grain','#5a6358','M 33 68 L 34 70 M 37 83 L 38 84 M 31 99 L 32 101 M 40 110 L 41 109 M 36 136 L 37 137 M 31 179 L 32 180 M 41 194 L 42 193 M 35 209 L 36 212 M 38 228 L 39 229 M 31 248 L 32 250 M 36 271 L 37 269 M 41 283 L 42 284 M 34 324 L 35 325 M 40 338 L 41 336 M 32 351 L 33 353',.65,160,.25),
 s('quiet_scuffs','#858777','M 31 86 L 32 88 M 32 204 L 32 207 M 31 270 L 31 272 M 39 345 L 40 346',.5,145,.2),
],
'ankle_ring':[
 s('worn_top_roll','#626a60','M 26 351 C 34 361 55 362 64 351 L 63 355 C 52 366 33 364 26 356 Z',opacity=220,feather=.45),
 s('front_roll_mass','#363f3a','M 27 358 C 35 366 53 366 62 358 L 62 362 C 51 371 35 370 27 363 Z',feather=.45),
 s('left_polished_arc','#a0a08c','M 27 353 L 30 357 L 35 360 M 38 362 L 44 363',.7,225,.2),
 s('right_dark_cut','#172123','M 59 360 L 64 355 L 63 362 L 58 367 Z',feather=.3),
 s('tiny_nicks','#929783','M 31 361 L 32 363 M 48 365 L 50 364',.6,140,.15),
],
'middle_ring':[
 s('curved_roll','#59645a','M 26 285 C 34 295 57 295 64 285 L 64 289 C 56 300 33 300 26 291 Z',feather=.45),
 s('left_face','#454f47','M 25 291 L 33 297 L 35 304 L 28 301 L 25 296 Z',feather=.45),
 s('front_cast','#333a36','M 34 298 C 43 302 53 299 60 295 L 61 300 C 53 306 42 308 35 304 Z',feather=.5),
 s('fine_rim_light','#a6aa95','M 27 287 L 30 290 L 34 293 M 39 296 L 45 297 M 57 293 L 60 291',.8,210,.2),
 s('broken_notch','#252f2c','M 35 292 L 37 294 L 38 297 L 35 296 Z',opacity=200,feather=.25),
 s('cast_edge_specks','#7e8976','M 29 297 L 30 298 M 49 300 L 51 299 M 58 297 L 59 296',.55,150,.15),
],
'upper_ring':[
 s('rolled_top','#606b60','M 26 140 C 35 151 56 150 64 140 L 64 145 C 56 155 33 156 25 146 Z',feather=.45),
 s('front_metal','#3c423d','M 26 147 C 34 156 53 157 63 148 L 63 153 C 55 161 35 162 27 154 Z',feather=.6),
 s('under_contact','#131f22','M 33 157 C 43 161 55 158 62 152 L 62 156 C 51 164 36 162 31 159 Z',feather=.35),
 s('rim_brush','#aaa993','M 27 143 L 29 146 L 34 150 M 38 152 L 44 153',.85,210,.2),
 s('small_chips','#778572','M 29 151 L 30 153 M 50 156 L 52 155',.6,170,.15),
],
 'top_collar':[
 s('left_roll','#626d60','M 28 60 L 33 65 L 35 72 L 31 71 L 28 67 Z',opacity=190,feather=.6),
 s('front_mass','#3e433f','M 35 66 C 44 70 54 68 61 63 L 61 72 C 54 78 43 79 35 74 Z',feather=.6),
 s('right_recess','#172326','M 57 68 L 63 62 L 62 73 L 57 77 Z',feather=.5),
 s('rolled_edge','#959f8c','M 29 62 L 32 65 L 37 68 M 40 70 L 44 70',.7,190,.25),
],
'finial_seat':[
 s('turned_top','#555b56','M 24 36 C 33 29 59 30 66 37 L 63 42 C 50 50 32 46 25 41 Z',feather=.6),
 s('front_roll','#3b413e','M 24 40 C 34 50 56 52 65 41 L 65 47 C 54 57 33 55 25 47 Z',feather=.6),
 s('polished_left_rim','#8f9b86','M 25 41 C 29 46 37 49 44 49 M 48 49 L 54 47',.9,190,.25),
 s('right_undercut','#152225','M 60 43 L 66 39 L 65 47 L 60 51 L 56 52 Z',feather=.4),
 s('rolled_lip_dabs','#b3b6a2','M 28 44 L 29 45 M 37 48 L 39 49',.65,160,.15),
],
'finial':[
 s('sphere_shadow','#1e282b','M 52 14 C 61 19 65 28 61 35 C 55 44 39 44 32 36 C 40 40 50 36 55 31 C 59 25 56 19 52 14 Z',feather=.7),
 s('sphere_lit_turn','#4b504e','M 33 23 C 35 15 45 12 52 18 C 59 23 55 31 49 35 C 40 39 31 34 31 29 Z',opacity=225,feather=.8),
 s('soft_lit_patch','#696c65','M 35 21 L 39 17 L 45 16 L 50 19 L 52 23 L 50 28 L 45 31 L 39 30 L 35 27 Z',opacity=200,feather=.9),
 s('top_brush','#8c8e83','M 38 20 L 41 17 L 46 18 L 48 21 L 46 25 L 42 26 L 38 24 Z',opacity=200,feather=.65),
 s('small_glint','#b8beaa','M 41 18 L 44 18 L 45 20 L 43 22 L 40 21 Z',opacity=210,feather=.6),
 s('fine_surface_grain','#829282','M 34 24 L 35 25 M 39 29 L 41 30 M 48 26 L 49 24 M 52 20 L 53 22 M 44 34 L 46 33',.6,130,.35),
 s('lower_reflection','#47564b','M 33 34 L 36 36 L 40 37 M 49 37 L 53 35',.75,160,.4),
],
'service_box':[
 s('top_plane','#d5cfbb','M 56 165 L 68 160 L 74 163 L 63 168 Z'),
 s('left_round_edge','#c4beaa','M 56 166 L 62 169 L 62 198 L 57 195 Z',feather=.35),
 s('front_plane','#aaa893','M 64 170 L 74 165 L 74 191 L 65 199 Z',feather=.4),
 s('return_shadow','#777d6e','M 72 166 L 75 164 L 75 193 L 65 201 L 65 198 L 72 192 Z',feather=.4),
 s('cream_edge_wear','#e4dfca','M 57 169 L 58 181 M 58 187 L 58 193 M 65 171 L 65 177',.7,210,.3),
 s('enamel_dings','#929c89','M 67 182 L 68 184 M 70 175 L 71 176 M 59 190 L 60 189',.55,170,.2),
],
'bracket':[
 s('left_thickness','#c1bca9','M 53 65 L 61 69 L 61 130 L 54 127 Z',feather=.35),
 s('mount_top','#d9d2bd','M 53 64 L 64 59 L 71 62 L 61 68 Z'),
 s('front_mount_mass','#a8aa96','M 63 69 L 71 64 L 71 81 L 104 71 L 108 88 L 84 95 C 75 101 71 109 71 126 L 64 131 Z',feather=.5),
 s('curved_arm_front','#c5c0aa','M 64 82 L 104 70 C 111 66 120 66 128 69 L 127 83 C 123 88 115 89 105 85 L 82 92 C 75 96 70 103 68 114 L 65 118 Z',feather=.6),
 s('inside_filleted_shadow','#787f70','M 69 112 C 71 100 76 94 84 91 L 104 84 L 108 88 L 84 97 C 77 100 74 110 73 125 L 70 128 Z',feather=.7),
 s('upper_bevel','#e2deca','M 64 79 L 103 67 L 106 69 L 104 72 L 65 84 Z',opacity=220,feather=.45),
 s('broken_left_brush','#e0dcc8','M 54 70 L 55 81 M 55 87 L 55 98 M 55 105 L 55 119 M 57 125 L 60 127',.75,200,.35),
 s('arm_fine_mottles','#a3a68f','M 75 84 L 77 82 L 79 83 L 78 85 Z M 86 80 L 88 79 L 89 80 L 88 82 Z M 95 77 L 96 75 L 98 76 L 97 78 Z M 67 97 L 68 98 L 67 101 Z',opacity=140,feather=.45),
 s('arm_scuffs','#e4e0ca','M 80 79 L 82 78 M 92 75 L 94 74 M 65 88 L 66 90',.55,155,.25),
],
'dome':[
 s('left_glass_curve','#293b3a','M 87 123 L 92 128 C 94 141 104 151 114 156 C 104 156 92 146 89 137 Z',opacity=190,feather=.8),
 s('rim_reflection','#354640','M 89 122 C 105 132 132 133 145 123 L 143 129 C 127 139 103 136 91 130 Z',opacity=185,feather=.6),
 s('left_soft_turn','#1c2b2e','M 95 132 C 100 141 107 147 118 152 L 120 158 C 108 156 99 148 95 142 Z',opacity=160,feather=.85),
 s('right_deep_glass','#071015','M 132 132 L 144 126 C 141 143 132 151 123 155 L 123 147 Z',feather=.9),
 s('small_broken_glint','#506157','M 91 132 L 93 134 L 94 137',.85,170,.45),
],
'hood':[
 s('back_shoulder','#c7c0aa','M 88 108 C 92 98 102 92 113 91 C 125 88 136 96 141 105 L 139 113 C 129 119 109 119 91 115 Z',feather=.6),
 s('upper_round_light','#d8cfb8','M 91 105 C 97 97 107 95 117 96 C 127 95 134 100 137 106 L 134 115 C 121 121 105 118 94 113 Z',opacity=220,feather=.8),
 s('front_cream_bowl','#beb9a3','M 85 112 C 98 124 124 127 142 116 L 145 121 C 137 133 108 136 91 127 L 85 122 Z',opacity=225,feather=.65),
 s('right_round_return','#929c87','M 133 96 C 143 104 148 115 146 122 L 139 128 L 132 130 L 136 123 L 140 117 L 139 109 Z',opacity=210,feather=.8),
 s('left_round_return','#a1a992','M 89 103 L 86 112 L 87 122 L 94 128 L 94 132 L 85 127 L 82 121 L 84 111 Z',opacity=200,feather=.6),
 s('fine_rim_cream','#ded8be','M 86 125 C 100 137 131 140 145 125 L 143 130 C 127 142 100 137 87 130 Z',opacity=220,feather=.35),
 s('lip_under_shadow','#4b554c','M 89 128 C 103 135 128 137 143 127 L 141 131 C 128 138 104 135 90 130 Z',opacity=215,feather=.35),
 s('soft_glint_body','#e8dfc5','M 98 106 L 102 102 L 108 102 L 112 104 L 119 102 L 123 105 L 122 110 L 116 113 L 108 112 L 103 115 L 99 113 Z',opacity=205,feather=.65),
 s('small_hot_glint','#f6eed4','M 103 105 L 107 104 L 110 106 L 109 109 L 104 111 L 101 109 Z',opacity=220,feather=.5),
 s('small_glint_breaks','#fff9df','M 104 106 L 106 105 L 108 106 L 107 108 L 104 109 Z M 113 105 L 115 104 L 117 105 L 116 107 L 114 107 Z',opacity=150,feather=.25),
 s('enamel_fine_dabs','#a4ac95','M 91 114 L 93 113 L 94 115 L 92 117 Z M 97 121 L 99 120 L 101 121 L 100 123 L 98 123 Z M 120 120 L 122 119 L 123 121 L 122 123 L 120 122 Z M 129 113 L 131 112 L 132 114 L 130 116 Z M 137 117 L 138 116 L 139 118 L 138 120 Z',opacity=145,feather=.35),
 s('small_edge_chips','#e9e5cd','M 89 126 L 91 127 M 96 130 L 98 131 M 102 133 L 104 133 M 113 135 L 117 135 M 132 133 L 135 131',.7,205,.2),
 s('quiet_age_strokes','#8d9884','M 87 117 L 88 119 M 126 125 L 127 126 M 139 123 L 140 122',.5,130,.25),
],
'bracket_neck':[
 s('curved_front','#b8b49c','M 106 73 C 114 78 126 75 131 70 L 130 83 C 126 91 114 93 106 87 Z',feather=.5),
 s('right_cylinder_turn','#8e9782','M 125 75 L 130 71 L 130 83 L 126 88 L 123 90 Z',opacity=205,feather=.6),
 s('top_lid','#d5d0b7','M 105 68 C 111 61 124 61 130 66 C 132 70 125 75 117 76 C 111 76 105 73 105 68 Z',feather=.3),
 s('top_lid_light','#e4dfc5','M 108 67 L 113 64 L 122 64 L 128 67 L 127 70 L 121 73 L 115 73 L 109 71 Z',opacity=220,feather=.5),
 s('front_bevel','#e7e2c7','M 106 73 C 113 78 124 77 130 72',.8,225,.2),
 s('enamel_fine_scuffs','#d4d0b4','M 109 80 L 110 82 M 112 85 L 112 87 M 117 89 L 120 88 M 126 80 L 127 78',.6,160,.3),
],
'cyan_lens':[s('inner_glint','#a2ffe4','M 116 143 L 117 146 L 116 148 L 115 146 Z')],
}

UNDERPAINT={'foot':'#242827','plinth':'#303735','socket':'#303936','pole':'#292f2e',
'ankle_ring':'#252e2c','middle_ring':'#252f2e','upper_ring':'#242e2c','top_collar':'#29302f',
'finial_seat':'#292d2c','finial':'#303433','service_box':'#aaa995','bracket':'#b8b49e',
'dome':'#0b1519','hood':'#b9b39d','bracket_neck':'#b3b09a','cyan_lens':'#30d4d0'}
PARTS=[dict(name=p['name'],contour=p['contour'],underpaint=UNDERPAINT[p['name']],surfaces=PAINT[p['name']]) for p in G['parts']]
