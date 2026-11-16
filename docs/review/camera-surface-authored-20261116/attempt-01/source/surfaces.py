"""Hand-authored surfaces, not a procedural material generator.

All contour/paint paths below are individually authored. No random/scumble shader,
source pixels, spatial color ramp, noise, or synthetic material sampling is used.
The reusable complete geometry is rendered back-to-front, then locally painted.
"""


def surface(name, color, path, width=0, opacity=255):
    return dict(name=name, color=color, path=path, width=width, opacity=opacity)


def part(name, contour, underpaint, surfaces):
    return dict(name=name, contour=contour, underpaint=underpaint, surfaces=surfaces)


CANVAS = [180,450]
ROOT = [46,427]
SCALE = 96/418
LANDMARKS = {'ground_root':[46,427], 'pole_axis_top':[46,44],
             'pole_axis_foot':[46,380], 'bracket_attachment':[59,92],
             'dome_center':[116,139], 'finial_tip':[45,12]}

PARTS = [
part('foot', 'M 12 390 C 17 381 69 379 80 390 L 84 414 C 80 426 64 432 46 432 C 28 432 13 425 10 416 Z', '#242726', [
 surface('left_cast_face','#373b38','M 12 394 L 23 402 L 25 424 L 17 420 L 12 413 Z'),
 surface('front_cast_face','#303331','M 24 401 C 37 407 57 407 67 402 L 68 425 C 54 432 38 431 26 426 Z'),
 surface('right_cast_face','#171d1e','M 67 401 L 80 393 L 82 412 L 77 420 L 68 425 Z'),
 surface('rim_wear','#7b7b6b','M 14 414 L 17 419 L 24 422 M 27 425 L 34 427 M 46 430 L 54 429 M 73 422 L 78 416',1.0),
 surface('cast_pits','#161d1e','M 29 410 L 30 419 M 47 411 L 46 426 M 66 409 L 65 419',1.4),
 surface('left_chip','#666a60','M 18 403 L 21 405 L 22 411 L 20 410 L 20 406 Z'),
 surface('front_chip','#5a6059','M 35 412 L 38 411 L 39 415 L 36 416 Z M 54 422 L 57 420 L 58 423 L 55 425 Z'),
]),
part('plinth', 'M 16 379 C 25 369 64 369 76 380 L 80 395 C 76 405 61 411 44 411 C 29 410 17 405 13 397 Z','#303433',[
 surface('sloping_crown','#666a62','M 17 380 C 27 369 64 370 75 381 L 72 389 C 61 401 31 400 19 390 Z'),
 surface('crown_left_light','#929084','M 20 380 L 25 375 L 29 376 L 25 383 L 26 389 L 32 393 L 29 394 L 22 390 Z'),
 surface('crown_right_turn','#444944','M 61 374 L 71 378 L 75 383 L 72 390 L 60 397 L 51 398 L 63 391 L 67 384 Z'),
 surface('front_vertical_lip','#292e2e','M 15 393 C 30 406 62 407 78 393 L 78 398 C 62 414 31 412 16 401 Z'),
 surface('thin_front_bevel','#a09c88','M 17 392 C 31 405 61 405 75 394',1.4),
 surface('bevel_gaps','#343a37','M 31 400 L 35 402 M 57 402 L 60 401',1.5),
 surface('cast_scar','#939083','M 23 387 L 26 385 L 27 389 L 25 391 Z M 61 390 L 63 388 L 63 392 L 60 394 Z'),
]),
part('socket', 'M 26 354 C 35 349 56 349 64 355 L 69 378 C 66 389 32 394 23 380 Z','#333735',[
 surface('left_curved_face','#595d55','M 27 358 L 34 361 L 34 382 L 30 385 L 26 381 Z'),
 surface('front_curved_face','#434842','M 35 362 C 43 366 52 365 58 360 L 60 385 C 52 389 41 389 34 385 Z'),
 surface('right_return','#1e2526','M 58 359 L 64 355 L 67 378 L 61 384 Z'),
 surface('left_worn_edge','#999482','M 27 359 L 28 366 M 28 370 L 29 376 L 31 379',1),
 surface('socket_front_marks','#666a5d','M 39 371 L 41 370 L 41 378 L 39 380 Z M 53 382 L 56 380 L 56 383 L 53 385 Z'),
]),
part('pole', 'M 29 43 C 37 41 53 41 61 45 L 62 97 L 61 160 L 62 224 L 61 289 L 62 355 C 60 366 35 369 27 359 L 28 285 L 27 219 L 28 146 Z','#282d2d',[
 surface('left_cylinder_turn','#474e49','M 29 46 L 34 48 L 34 104 L 33 159 L 34 218 L 32 282 L 34 352 L 32 360 L 29 356 L 30 284 L 29 220 L 30 148 Z'),
 surface('left_broken_light','#62695e','M 30 53 L 32 54 L 32 111 L 31 123 Z M 30 170 L 32 170 L 32 226 L 31 235 Z M 30 248 L 32 247 L 32 275 L 31 281 Z M 31 313 L 33 312 L 33 351 L 31 357 Z'),
 surface('front_broad_cast','#343a37','M 35 47 L 46 47 L 45 120 L 46 184 L 44 245 L 46 300 L 45 364 L 36 362 L 35 290 L 36 219 L 35 159 Z'),
 surface('front_plane_turn','#414740','M 37 53 L 40 52 L 40 98 L 38 104 Z M 38 125 L 41 126 L 40 177 L 38 180 Z M 37 202 L 40 198 L 41 235 L 39 249 L 37 246 Z M 37 263 L 40 266 L 40 287 L 38 286 Z M 39 319 L 42 314 L 42 356 L 39 359 Z'),
 surface('right_round_shadow','#161e20','M 49 46 L 60 46 L 59 160 L 60 224 L 59 289 L 60 354 L 53 362 L 51 296 L 52 231 L 50 161 Z'),
 surface('right_reflected_edge','#444b46','M 58 100 L 59 101 L 59 143 L 57 146 Z M 58 185 L 59 180 L 59 219 L 58 226 Z M 58 257 L 59 258 L 58 282 L 56 285 Z M 58 332 L 59 329 L 59 353 L 57 356 Z'),
 surface('cast_damage_dark','#1a2222','M 35 115 L 38 114 L 37 127 L 35 129 Z M 42 184 L 45 181 L 44 189 L 42 190 Z M 35 298 L 38 297 L 37 305 L 35 304 Z'),
 surface('sparse_wear','#777b6c','M 31 84 L 32 83 L 32 89 M 37 151 L 38 154 M 32 205 L 33 208 M 41 241 L 42 238 M 30 270 L 31 271 M 39 345 L 40 347',.7),
]),
part('ankle_ring','M 25 351 C 32 360 54 363 64 351 L 65 361 C 62 372 31 374 24 362 Z','#252b2b',[
 surface('top_worn_roll','#777a6d','M 26 351 C 34 361 55 362 64 351 L 63 355 C 52 366 33 364 26 356 Z'),
 surface('front_return','#454c45','M 27 358 C 35 366 53 366 62 358 L 62 362 C 51 371 35 370 27 363 Z'),
 surface('broken_left_rim','#aaa38d','M 27 352 L 30 356 L 35 359 M 37 360 L 43 362',.85),
 surface('right_dark','#192222','M 59 360 L 64 355 L 63 362 L 58 367 Z'),
]),
part('middle_ring','M 25 285 C 32 294 56 297 65 284 L 66 294 C 61 307 31 309 24 296 Z','#252d2d',[
 surface('rolled_upper_rim','#686e62','M 26 285 C 34 295 57 295 64 285 L 64 289 C 56 300 33 300 26 291 Z'),
 surface('face_left','#4d564c','M 25 291 L 33 297 L 35 304 L 28 301 L 25 296 Z'),
 surface('face_front','#394139','M 34 298 C 43 302 53 299 60 295 L 61 300 C 53 306 42 308 35 304 Z'),
 surface('rim_glints','#b1ab92','M 27 286 L 30 290 L 35 293 M 39 295 L 45 296 M 57 293 L 61 290',1),
 surface('notch','#252b28','M 35 292 L 38 295 L 38 298 L 35 296 Z'),
]),
part('upper_ring','M 25 140 C 32 149 55 150 65 138 L 66 149 C 61 163 31 163 24 152 Z','#242d2c',[
 surface('top_roll','#74796a','M 26 140 C 35 151 56 150 64 140 L 64 145 C 56 155 33 156 25 146 Z'),
 surface('front_metal','#444d42','M 26 147 C 34 156 53 157 63 148 L 63 153 C 55 161 35 162 27 154 Z'),
 surface('contact_shadow','#151e20','M 33 157 C 43 161 55 158 62 152 L 62 156 C 51 164 36 162 31 159 Z'),
 surface('left_rim','#b2ab93','M 26 142 L 29 146 L 34 149 M 38 151 L 44 152',.9),
]),
part('top_collar','M 27 59 C 34 67 54 67 63 59 L 64 72 C 57 82 32 81 26 72 Z','#293130',[
 surface('left_roll','#707669','M 28 60 L 34 65 L 36 73 L 31 72 L 28 68 Z'),
 surface('front_cast','#444d43','M 35 66 C 44 70 54 68 61 63 L 61 72 C 54 78 43 79 35 74 Z'),
 surface('right_return','#192323','M 57 68 L 63 62 L 62 73 L 57 77 Z'),
 surface('upper_edge','#9b9c88','M 28 61 L 32 65 L 37 68 M 40 69 L 45 70',.85),
]),
part('finial_seat','M 23 35 C 31 29 60 29 67 36 L 67 46 C 61 59 29 59 23 47 Z','#282e2e',[
 surface('turned_top','#63695f','M 24 36 C 33 29 59 30 66 37 L 63 42 C 50 50 32 46 25 41 Z'),
 surface('front_roll','#444d45','M 24 40 C 34 50 56 52 65 41 L 65 47 C 54 57 33 55 25 47 Z'),
 surface('rim_highlight','#9ca18b','M 25 40 C 29 46 37 49 44 49 M 47 49 L 55 47',1.1),
 surface('right_undercut','#172022','M 60 43 L 66 39 L 65 47 L 60 51 L 56 52 Z'),
]),
part('finial','M 29 26 C 28 19 34 12 43 12 C 52 11 59 16 62 24 C 66 35 58 42 46 43 C 34 42 27 37 29 26 Z','#303936',[
 surface('shadow_turn','#1d2829','M 52 14 C 61 19 65 28 61 35 C 55 44 39 44 32 36 C 40 40 50 36 55 31 C 59 25 56 19 52 14 Z'),
 surface('broad_lit_dome','#515e52','M 33 23 C 35 15 45 12 52 18 C 59 23 55 31 49 35 C 40 39 31 34 31 29 Z'),
 surface('middle_bounce','#677364','M 35 20 L 39 16 L 47 16 L 53 20 L 53 26 L 49 31 L 42 32 L 36 29 L 34 25 Z'),
 surface('upper_lit_patch','#8d9782','M 37 19 L 42 16 L 47 17 L 49 20 L 47 24 L 43 25 L 38 23 Z'),
 surface('small_specular','#c5c4a7','M 41 17 L 44 17 L 45 19 L 43 21 L 40 20 Z'),
 surface('scuffed_edge','#75806d','M 31 26 L 32 30 M 33 33 L 36 35 M 54 20 L 56 23',.7),
]),
part('service_box','M 55 165 L 68 158 L 76 163 L 76 193 L 65 202 L 55 197 Z','#aaa28c',[
 surface('top','#e2d6b9','M 56 165 L 68 160 L 74 163 L 63 168 Z'),
 surface('left','#c8bea3','M 56 166 L 62 169 L 62 198 L 57 195 Z'),
 surface('front','#b3ab92','M 64 170 L 74 165 L 74 191 L 65 199 Z'),
 surface('side_shadow','#777e6a','M 72 166 L 75 164 L 75 193 L 65 201 L 65 198 L 72 192 Z'),
 surface('edge_wear','#eee2c2','M 57 168 L 58 184 M 58 187 L 58 193 M 65 171 L 65 179',.9),
]),
part('bracket','M 52 64 L 64 57 L 73 62 L 73 77 L 102 68 C 107 61 122 58 130 64 C 134 67 133 78 132 84 C 130 94 116 97 104 91 L 84 97 C 76 101 74 109 74 127 L 63 134 L 52 129 Z','#b9b19a',[
 surface('left_thickness','#d4c9ac','M 53 65 L 61 69 L 61 130 L 54 127 Z'),
 surface('mount_top','#e5d9bc','M 53 64 L 64 59 L 71 62 L 61 68 Z'),
 surface('mount_front','#aaa48d','M 63 69 L 71 64 L 71 81 L 104 71 L 108 88 L 84 95 C 75 101 71 109 71 126 L 64 131 Z'),
 surface('curved_arm_front','#cec2a6','M 64 82 L 104 70 C 111 66 120 66 128 69 L 127 83 C 123 88 115 89 105 85 L 82 92 C 75 96 70 103 68 114 L 65 118 Z'),
 surface('arm_underside','#777b68','M 69 112 C 71 100 76 94 84 91 L 104 84 L 108 88 L 84 97 C 77 100 74 110 73 125 L 70 128 Z'),
 surface('long_upper_bevel','#f0e3c4','M 64 79 L 103 67 L 106 69 L 104 72 L 65 84 Z'),
 surface('left_edge_wear','#eee2c4','M 54 69 L 55 89 M 55 94 L 55 121 M 57 125 L 60 127',1),
 surface('front_age','#b2aa91','M 76 83 L 80 81 L 82 82 L 80 85 L 76 86 Z M 89 79 L 93 77 L 95 78 L 92 81 Z'),
]),
part('dome','M 85 118 C 94 108 137 108 148 120 C 148 142 134 159 117 160 C 101 160 88 147 85 130 Z','#0b1519',[
 surface('left_glass_curve','#293c3b','M 87 123 L 92 128 C 94 141 104 151 114 156 C 104 156 92 146 89 137 Z'),
 surface('upper_reflected_rim','#3d4c47','M 89 122 C 105 132 132 133 145 123 L 143 129 C 127 139 103 136 91 130 Z'),
 surface('left_soft_turn','#1c2c2f','M 95 132 C 100 141 107 147 118 152 L 120 158 C 108 156 99 148 95 142 Z'),
 surface('right_deep_glass','#050e13','M 132 132 L 144 126 C 141 143 132 151 123 155 L 123 147 Z'),
 surface('small_reflection','#516059','M 91 132 L 94 135 L 95 139 L 93 138 Z'),
]),
part('hood','M 109 89 C 117 86 129 89 136 96 C 143 102 148 114 148 121 C 147 129 136 135 121 136 C 103 137 87 131 82 124 C 80 119 84 107 90 100 C 95 94 101 91 109 89 Z','#bbb29a',[
 surface('back_shoulder','#d4c7aa','M 88 108 C 92 98 102 92 113 91 C 125 88 136 96 141 105 L 139 113 C 129 119 109 119 91 115 Z'),
 surface('upper_round_light','#e6d6b6','M 91 105 C 97 97 107 95 117 96 C 127 95 134 100 137 106 L 134 115 C 121 121 105 118 94 113 Z'),
 surface('front_cream_bowl','#c8bda2','M 85 112 C 98 124 124 127 142 116 L 145 121 C 137 133 108 136 91 127 L 85 122 Z'),
 surface('right_round_return','#8f927a','M 133 96 C 143 104 148 115 146 122 L 139 128 L 132 130 L 136 123 L 140 117 L 139 109 Z'),
 surface('left_round_return','#a6a68b','M 89 103 L 86 112 L 87 122 L 94 128 L 94 132 L 85 127 L 82 121 L 84 111 Z'),
 surface('rim_front','#e6dab8','M 86 125 C 100 137 131 140 145 125 L 143 130 C 127 142 100 137 87 130 Z'),
 surface('rim_under_shadow','#4b5149','M 89 128 C 103 135 128 137 143 127 L 141 131 C 128 138 104 135 90 130 Z'),
 surface('broad_soft_glint','#f1e2c0','M 98 106 L 102 102 L 108 102 L 112 104 L 119 102 L 123 105 L 122 110 L 116 113 L 108 112 L 103 115 L 99 113 Z'),
 surface('small_hot_glint','#fff0cf','M 103 105 L 107 104 L 110 106 L 109 109 L 104 111 L 101 109 Z'),
 surface('paint_weathering','#a2a088','M 92 115 L 95 113 L 97 115 L 96 118 L 93 119 Z M 124 120 L 128 118 L 129 121 L 126 124 L 124 123 Z M 137 111 L 139 112 L 139 115 L 137 116 Z'),
 surface('small_edge_chips','#f2e6c6','M 89 126 L 92 128 M 97 131 L 101 132 M 113 135 L 119 135 M 132 133 L 136 131',1),
]),
part('bracket_neck','M 104 67 C 111 61 124 60 130 65 L 132 69 L 131 84 C 127 93 113 95 104 88 Z','#b9af94',[
 surface('curved_front','#c6b99d','M 106 73 C 114 78 126 75 131 70 L 130 83 C 126 91 114 93 106 87 Z'),
 surface('right_cylinder_turn','#8f927a','M 125 75 L 130 71 L 130 83 L 126 88 L 123 90 Z'),
 surface('top_lid','#e4d8b8','M 105 68 C 111 61 124 61 130 66 C 132 70 125 75 117 76 C 111 76 105 73 105 68 Z'),
 surface('top_lid_light','#f1e5c6','M 108 67 L 113 64 L 122 64 L 128 67 L 127 70 L 121 73 L 115 73 L 109 71 Z'),
 surface('front_bevel','#f0e1c0','M 106 73 C 113 78 124 77 130 72',1),
 surface('front_scuff','#dbcfaf','M 110 80 L 112 81 L 112 86 M 117 88 L 121 88',.8),
]),
part('cyan_lens','M 116 142 L 120 146 L 116 150 L 112 146 Z','#30d4d0',[
 surface('inner_glint','#a2ffe4','M 116 143 L 117 146 L 116 148 L 115 146 Z'),
]),
]

HIDDEN = [dict(under='pole',over='middle_ring',point=[45,300]),
          dict(under='pole',over='bracket',point=[56,100]),
          dict(under='dome',over='hood',point=[115,122]),
          dict(under='foot',over='plinth',point=[45,399]),
          dict(under='hood',over='bracket_neck',point=[116,90])]
