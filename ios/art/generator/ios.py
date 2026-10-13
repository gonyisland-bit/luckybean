"""Lucky Bean iOS mockup backgrounds: pigeon guests + Kiri the cat (autumn)."""
import math, random, sys
import f_kit
from f_kit import *
import f_scenes2
from f_scenes2 import euro_cafe, a_frame, bistro, gazebo
from f_scenes3 import room, window, esp_machine, bowl, FLOOR

OUT = '/home/claude/lb_art/ios'
import os; os.makedirs(OUT, exist_ok=True)

NIGHT = '#2E3A4A'
# member feather colours + accessories
MEMBERS = [
    ('#A9B2BA', 'beret'),   # 민수 grey + coral beret
    ('#EEEAE2', 'ribbon'),  # 지은 white + ribbon
    ('#B89A80', 'scarf'),   # 서준 brown + mustard scarf
    ('#6F7882', 'glasses'), # 하린 charcoal + glasses
    ('#CFC6B6', 'cap'),     # 도윤 sand + teal cap
]
SEGC = [CORAL, LBLUE, MUST, TEAL_L, PEACH]

def shade(hexc, f):
    h = hexc.lstrip('#'); r, g, b = (int(h[i:i+2], 16) for i in (0, 2, 4))
    return '#%02X%02X%02X' % tuple(max(0, min(255, int(c * f))) for c in (r, g, b))

# ---------------- characters ----------------
def pg(x, y, s=1.0, body='#A9B2BA', acc=None, flip=False, wing_up=False, coin=False):
    """Pigeon guest, 3/4 view facing right, feet at (x, y)."""
    dk = shade(body, 0.82); lt = shade(body, 1.08)
    t = f'translate({x} {y}) scale({-s if flip else s} {s})'
    p = [f'<g transform="{t}">']
    p.append(f'<path d="M-12 -12 L-24 -8 L-13 -4 Z" fill="{dk}"/>')                      # tail
    p.append(f'<path d="M-1 -1 v4 M4 -1 v4" stroke="#E79A86" stroke-width="2.2" stroke-linecap="round"/>')
    p.append(f'<ellipse cx="0" cy="-14" rx="15" ry="13" fill="{body}"/>')                # body
    p.append(f'<ellipse cx="4" cy="-9" rx="9" ry="7" fill="{lt}"/>')                     # belly
    if wing_up:
        p.append(f'<path d="M-6 -20 C-20 -40 -2 -46 8 -30 C2 -24 -2 -20 -6 -20 Z" fill="{dk}"/>')
    else:
        p.append(f'<path d="M-13 -18 C-8 -26 6 -24 7 -15 C2 -7 -8 -6 -13 -11 Z" fill="{dk}"/>')
        p.append(f'<path d="M-9 -15 h10 M-8 -11 h8" stroke="{shade(body,0.7)}" stroke-width="1.2" stroke-linecap="round"/>')
    if coin:
        p.append(f'<circle cx="-6" cy="-36" r="6.5" fill="{MUST}"/><circle cx="-6" cy="-36" r="4" fill="none" stroke="{MUST_L}" stroke-width="1.4"/>')
    p.append(f'<ellipse cx="6" cy="-26" rx="8" ry="5.5" fill="#7FA79A" opacity="0.85"/>')  # neck sheen
    p.append(f'<ellipse cx="6" cy="-28" rx="6" ry="3" fill="#B58AA8" opacity="0.45"/>')
    p.append(f'<circle cx="7" cy="-34" r="8.4" fill="{body}"/>')                          # head
    p.append(f'<circle cx="10" cy="-35" r="2.6" fill="{WHITE}"/><circle cx="10.4" cy="-35" r="1.4" fill="{CHAR}"/>')
    p.append(f'<path d="M14.6 -34 l5.4 1.6 -5.4 1.4 z" fill="{CHAR}"/><ellipse cx="15.2" cy="-34.4" rx="1.6" ry="1" fill="{WHITE}"/>')
    p.append(f'<ellipse cx="5" cy="-31" rx="2" ry="1.3" fill="{CORAL}" opacity="0.55"/>')
    if acc == 'beret':
        p.append(f'<ellipse cx="5" cy="-41" rx="9.5" ry="4" fill="{CORAL}" transform="rotate(-12 5 -41)"/><rect x="4" y="-47.5" width="2.4" height="3" rx="1" fill="{CORAL}"/>')
    elif acc == 'ribbon':
        p.append(f'<path d="M2 -42 l-5 -4 v8 z M2 -42 l5 -4 v8 z" fill="{RED}"/><circle cx="2" cy="-42" r="1.8" fill="{RED}"/>')
    elif acc == 'scarf':
        p.append(f'<path d="M-1 -27 Q6 -22 13 -27 L13 -23 Q6 -18 -1 -23 Z" fill="{MUST}"/><path d="M0 -24 l-4 10 l4 -1 z" fill="{MUST}"/><path d="M1 -26 h10" stroke="{WHITE}" stroke-width="0.8" opacity="0.6"/>')
    elif acc == 'glasses':
        p.append(f'<circle cx="10.2" cy="-35" r="3.6" fill="none" stroke="{CHAR}" stroke-width="1.2"/><path d="M6.6 -35 h-3" stroke="{CHAR}" stroke-width="1.2"/>')
    elif acc == 'cap':
        p.append(f'<path d="M-1 -38 Q6 -48 14 -39 Z" fill="{TEAL_D}"/><path d="M12 -39.5 l7 1 l-7 1.4 z" fill="{TEAL_D}"/><circle cx="6" cy="-44.6" r="1.4" fill="{MUST}"/>')
    p.append('</g>')
    return ''.join(p)

def pg_head(x, y, s, body, acc):
    """Front avatar crop: reuse full pigeon, centred on head."""
    return pg(x, y, s, body, acc)

def kiri_sit(x, y, s=1.0, eyes='open', bandana=True):
    col = CAT; dk = '#C9722A'
    e = (f'<circle cx="-3.2" cy="-19" r="1.2" fill="{CHAR}"/><circle cx="3.2" cy="-19" r="1.2" fill="{CHAR}"/>' if eyes == 'open'
         else f'<path d="M-4.6 -19 q1.4 1.3 2.8 0 M1.8 -19 q1.4 1.3 2.8 0" stroke="{CHAR}" stroke-width="0.9" fill="none" stroke-linecap="round"/>')
    return f'''<g transform="translate({x} {y}) scale({s})">
<path d="M7 -1 C17 0 18 -10 12 -14" stroke="{col}" stroke-width="3.2" stroke-linecap="round" fill="none"/>
<path d="M14.6 -10 l2 -1.6 M16.4 -6 l2.2 -0.6" stroke="{dk}" stroke-width="1.2" stroke-linecap="round"/>
<path d="M-8 0 C-9.5 -8 -6.5 -15 0 -15.5 C6.5 -15 9.5 -8 8 0 Z" fill="{col}"/>
<path d="M-7.6 -6 q2 -1 3 0 M5 -8 q2 -1 3 0 M-8 -2.4 q2 -1 3 0" stroke="{dk}" stroke-width="1.1" fill="none" stroke-linecap="round"/>
<ellipse cx="0" cy="-5.5" rx="3.6" ry="4.6" fill="{CATC}"/>
<path d="M-6.6 -20 L-5.6 -27.5 L-1.6 -23 Z M6.6 -20 L5.6 -27.5 L1.6 -23 Z" fill="{col}"/>
<path d="M-5.4 -22.4 L-5 -25.6 L-3.2 -23.4 Z M5.4 -22.4 L5 -25.6 L3.2 -23.4 Z" fill="{PEACH}"/>
<ellipse cx="0" cy="-19" rx="7.4" ry="6.3" fill="{col}"/>
<path d="M-1.6 -25 v2.4 M0 -25.3 v2.6 M1.6 -25 v2.4" stroke="{dk}" stroke-width="0.9" stroke-linecap="round"/>
<ellipse cx="0" cy="-16.4" rx="2.6" ry="1.8" fill="{CATC}"/>
{e}<path d="M-1 -17.4 h2 l-1 1.1 z" fill="{CHAR}"/>
<ellipse cx="-4.8" cy="-16.6" rx="1.4" ry="0.8" fill="{CORAL}" opacity="0.6"/><ellipse cx="4.8" cy="-16.6" rx="1.4" ry="0.8" fill="{CORAL}" opacity="0.6"/>
{f'<path d="M-6 -13 Q0 -10 6 -13 L4.6 -11 Q0 -7.6 -4.6 -11 Z" fill="{TEAL_D}"/><path d="M-1.4 -10 L0 -6.6 L1.4 -10 Z" fill="{TEAL_D}"/>' if bandana else ''}
</g>'''

def kiri_walk(x, y, s=1.0):
    col = CAT; dk = '#C9722A'
    return f'''<g transform="translate({x} {y}) scale({s})">
<path d="M12 -8 C20 -12 21 -22 17 -26" stroke="{col}" stroke-width="3" stroke-linecap="round" fill="none"/>
<rect x="-10" y="-5" width="3" height="8" rx="1.5" fill="{col}"/><rect x="-5" y="-5" width="3" height="8" rx="1.5" fill="{dk}"/><rect x="5" y="-5" width="3" height="8" rx="1.5" fill="{col}"/><rect x="9" y="-5" width="3" height="8" rx="1.5" fill="{dk}"/>
<ellipse cx="1" cy="-8" rx="13" ry="6.4" fill="{col}"/>
<path d="M-2 -13 q1 3 0 6 M3 -14 q1 3 0 6 M8 -13 q1 3 0 5" stroke="{dk}" stroke-width="1.2" fill="none" stroke-linecap="round"/>
<path d="M-17 -15 L-16 -22 L-12 -17 Z M-9 -16 L-9.6 -23 L-12.6 -17.4 Z" fill="{col}"/>
<circle cx="-13" cy="-12" r="6" fill="{col}"/><circle cx="-15" cy="-12.6" r="0.9" fill="{CHAR}"/><circle cx="-11" cy="-12.6" r="0.9" fill="{CHAR}"/>
<path d="M-17 -9 Q-13 -6.6 -9 -9 L-10 -7.4 Q-13 -5 -16 -7.4 Z" fill="{TEAL_D}"/>
</g>'''

def kiri_curl(x, y, s=1.0):
    return f_kit.cat_curl(x, y, s) + f'<path d="M{x-12*s} {y+8*s} q{4*s} {2*s} {8*s} 0" stroke="{TEAL_D}" stroke-width="{3*s}" fill="none" stroke-linecap="round"/>'

# ---------------- autumn trees ----------------
AUT = [MUST, ORANGE, '#D9A35A', TEAL_D, CORAL, MUST]
def a_tree(x, base, r, col=None, trunk=CHAR):
    c = col if col and col not in (TEAL, TEAL_D) else AUT[int(x * 7 + base) % len(AUT)]
    pat = ['dotsW', 'stripeW', None][int(x + base) % 3]
    out = f'<rect x="{x-1.6}" y="{base-r*1.1}" width="3.2" height="{r*1.1}" fill="{trunk}"/><ellipse cx="{x}" cy="{base-r*1.5}" rx="{r*0.85}" ry="{r}" fill="{c}"/>'
    if pat:
        out += f'<ellipse cx="{x}" cy="{base-r*1.5}" rx="{r*0.85}" ry="{r}" fill="url(#{pat})" opacity="0.5"/>'
    return out
def a_pine(x, base, w, h, col=TEAL_D, trunk=CHAR):
    return pine(x, base, w, h, col, trunk)
tree = a_tree
f_scenes2.tree = a_tree

def leaves(n, x0, y0, x1, y1, seed=3):
    rnd = random.Random(seed); out = []
    for _ in range(n):
        x = rnd.uniform(x0, x1); y = rnd.uniform(y0, y1); a = rnd.uniform(0, 180); c = rnd.choice([MUST, ORANGE, CORAL, '#D9A35A'])
        out.append(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="3" ry="1.6" fill="{c}" transform="rotate({a:.0f} {x:.1f} {y:.1f})"/>')
    return ''.join(out)

def lamp(x, base, night=False):
    g = f'<ellipse cx="{x}" cy="{base-44}" rx="26" ry="26" fill="url(#glow)"/>' if night else ''
    return g + f'<rect x="{x-1.2}" y="{base-40}" width="2.4" height="40" fill="{CHAR}"/><path d="M{x-5} {base-40} h10 l-2 -7 h-6 z" fill="{CHAR}"/><rect x="{x-3}" y="{base-46}" width="6" height="5" fill="{MUST_L if night else CREAM}"/>'

# ---------------- HOME ----------------
def home(night=False):
    p = [f'<rect width="390" height="844" fill="{MAP}"/>']
    p.append(f'<path d="M0 540 H276 V844 H0 Z" fill="#CFDCC3"/>')
    p.append(f'<path d="M286 540 H390 V844 H286 Z" fill="#E3DCCF"/>')
    p.append(f'<path d="M40 844 C60 760 120 650 150 640 C190 640 230 670 276 660" stroke="{CREAM}" stroke-width="10" fill="none" stroke-linecap="round"/>')
    p.append(f'<ellipse cx="70" cy="600" rx="34" ry="14" fill="{LBLUE}"/><ellipse cx="70" cy="600" rx="26" ry="9" fill="#BCD9DC"/>')
    for d in ('M0 520 H400', 'M100 -10 V520', 'M100 262 H400', 'M286 520 V860', 'M100 120 H-10'):
        p.append(f'<path d="{d}" stroke="{WHITE}" stroke-width="20" fill="none" stroke-linecap="round"/>')
    p.append(''.join(f'<rect x="{x}" y="518" width="10" height="3" fill="{GREY_L}"/>' for x in range(10, 390, 24)))
    p.append(''.join(f'<rect x="98" y="{y}" width="3" height="10" fill="{GREY_L}"/>' for y in range(0, 510, 24)))
    p.append(f'<rect x="110" y="496" width="270" height="14" fill="{CREAM}"/>')
    for (hx, hy) in ((50, 470), (200, 170), (350, 190), (330, 470), (200, 600), (120, 690), (40, 680), (330, 610), (200, 90), (40, 200)):
        p.append(hatch(hx, hy, '#B9C9A8' if hy > 540 else TEAL_L))
    # top band: small houses + trees (behind header)
    p.append(house(130, 100, 30, 34, MUST, CHAR, roof_h=14, cols=1, rows=1) + house(168, 100, 36, 28, CORAL, TEAL_D, roof_h=14, cols=2, rows=1) + house(212, 100, 26, 42, TEAL_L, CHAR, roof_h=12, cols=1, rows=2))
    p.append(tree(256, 100, 10) + tree(282, 96, 8) + a_pine(312, 104, 14, 34) + tree(346, 100, 11) + tree(24, 96, 9) + a_pine(56, 100, 12, 30))
    # TL: lounge (tall teal house)
    p.append(house(24, 330, 56, 150, TEAL, CHAR, roof_h=26, cols=2, rows=4, door=MUST, chimney=True))
    p.append(tree(30, 420, 10) + a_pine(70, 440, 16, 38) + tree(36, 500, 9) + tree(70, 236, 8))
    # post office
    p.append(house(130, 244, 70, 58, CREAM, RED, roof_h=24, cols=2, rows=1, door=TEAL_D, tex='stripe'))
    p.append(f'<rect x="210" y="226" width="12" height="18" rx="3" fill="{RED}"/><rect x="212" y="230" width="8" height="2" fill="{CHAR}"/><rect x="215" y="244" width="2" height="0"/>')
    p.append(f'<rect x="134" y="168" width="2" height="22" fill="{CHAR}"/><path d="M136 168 h14 l-4 5 l4 5 h-14 z" fill="{MUST}"/>')
    p.append(tree(244, 248, 11) + tree(262, 244, 8))
    # TR: records hall
    p.append(house(276, 244, 78, 90, GREY_L, CHAR, roof_h=28, cols=3, rows=2, door=ORANGE, arch=True))
    p.append(f'<circle cx="315" cy="146" r="9" fill="{WHITE}"/><path d="M315 146 v-5 M315 146 l3.4 2" stroke="{CHAR}" stroke-width="1.4" stroke-linecap="round"/>')
    p.append(tree(370, 244, 9))
    p.append(car(150, 268, MUST, kind='taxi') + car(316, 268, TEAL_D, w=30, flip=True))
    # CAFE
    p.append(euro_cafe(124, 498, 180))
    p.append(a_frame(318, 508, 1.0))
    p.append(bistro(350, 506, CORAL))
    p.append(tree(118, 498, 8) + a_pine(370, 470, 10, 26))
    p.append(kiri_walk(84, 510, 0.9))
    p.append(pg(258, 512, 0.5, *MEMBERS[2]) + pg(232, 512, 0.5, *MEMBERS[0], flip=True) + pg(352, 520, 0.45, *MEMBERS[1], flip=True))
    p.append(car(30, 528, ORANGE, w=46, kind='bus') + car(200, 530, CORAL, w=32))
    p.append(lamp(112, 508, night) + lamp(300, 508, night))
    # park
    p.append(gazebo(170, 650, 70))
    p.append(tree(30, 574, 11) + tree(240, 590, 12) + a_pine(120, 590, 16, 40) + tree(254, 700, 10) + a_pine(26, 700, 14, 34) + tree(214, 712, 9) + tree(80, 760, 12) + tree(180, 790, 10) + a_pine(250, 800, 14, 34))
    p.append(f'<rect x="96" y="690" width="34" height="5" rx="2" fill="{BROWN}"/><path d="M100 695 v8 M126 695 v8" stroke="{CHAR}" stroke-width="2"/>')
    p.append(pg(112, 688, 0.42, *MEMBERS[3]) + pg(196, 668, 0.42, *MEMBERS[4], flip=True))
    p.append(leaves(40, 10, 540, 280, 840, 5) + leaves(14, 110, 120, 380, 250, 9))
    # map shop
    p.append(house(302, 640, 70, 58, PEACH, ORANGE, roof_h=24, cols=2, rows=1, door=TEAL_D, tex='scallop'))
    p.append(f'<rect x="300" y="548" width="3" height="40" fill="{CHAR}"/><rect x="290" y="540" width="40" height="26" rx="3" fill="{WHITE}"/><path d="M296 560 l8 -10 l8 6 l8 -8 l6 4" stroke="{TEAL}" stroke-width="2" fill="none" stroke-linecap="round"/><circle cx="318" cy="552" r="2.4" fill="{RED}"/>')
    p.append(tree(372, 600, 9) + tree(330, 740, 12) + tree(370, 790, 9))
    if night:
        p.append(f'<rect width="390" height="844" fill="{NIGHT}" opacity="0.62"/>')
        for (gx, gy, r) in ((214, 455, 90), (214, 380, 70), (52, 260, 30), (165, 225, 26), (315, 205, 32), (337, 625, 28), (60, 80, 20), (190, 80, 22)):
            p.append(f'<ellipse cx="{gx}" cy="{gy}" rx="{r}" ry="{r*0.8}" fill="url(#glow)"/>')
        # lit windows on top of overlay
        g0 = 498 - 78
        p.append(''.join(f'<rect x="{124+8+i*((180-24)/3+4):.1f}" y="{g0+18}" width="{(180-24)/3:.1f}" height="54" fill="#FBD98A" opacity="0.85"/>' for i in (0, 2)))
        p.append(''.join(f'<path d="M{wx} {336+52} V{336+24} A11 11 0 0 1 {wx+22} {336+24} V{336+52} Z" fill="#FBD98A" opacity="0.9"/>' for wx in [124 + 14 + i * (180 - 28 - 22) / 3 for i in range(4)]))
        p.append(lamp(112, 508, True) + lamp(300, 508, True))
        p.append(''.join(f'<rect x="{x}" y="{y}" width="7" height="8" fill="#FBD98A" opacity="0.8"/>' for x, y in ((33, 186), (61, 214), (33, 250), (150, 210), (178, 210), (288, 180), (316, 180), (316, 214), (318, 612), (346, 612))))
        p.append(''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{CREAM}"/>' for x, y, r in ((40, 30, 1.2), (120, 18, 1), (250, 40, 1.4), (300, 14, 1), (360, 60, 1.2))))
    return ''.join(p)

# ---------------- CAFE interior (game select) ----------------
def cafe_select():
    p = [room(430)]
    p.append(window(130, 98, 130, 176))
    p.append(f'<rect x="124" y="272" width="142" height="8" rx="3" fill="{CREAM}"/>')
    p.append(pg(172, 272, 0.75, *MEMBERS[0]) + pg(232, 272, 0.75, *MEMBERS[1], flip=True))
    for lx in (70, 320):
        p.append(f'<rect x="{lx-1}" y="0" width="2" height="54" fill="{CHAR}"/><path d="M{lx-15} 70 Q{lx} 44 {lx+15} 70 Z" fill="{TEAL_D}"/><ellipse cx="{lx}" cy="90" rx="50" ry="34" fill="url(#glow)" opacity="0.45"/>')
    p.append(f'<rect x="298" y="122" width="66" height="84" rx="4" fill="{CHAR}"/>' + ''.join(f'<rect x="306" y="{136+k*13}" width="{40 if k%2 else 50}" height="2.4" fill="{CREAM}" opacity="0.85"/>' for k in range(5)))
    p.append(f'<path d="M30 150 h56 v62 h-56 z" fill="{CREAM}"/><path d="M36 156 h44 v50 h-44 z" fill="{MUST_L}"/>' + kiri_sit(58, 202, 1.3, bandana=False))
    p.append(f'<rect x="10" y="352" width="370" height="9" rx="2" fill="{KRAFT}"/><rect x="16" y="361" width="358" height="69" fill="{TEAL_D}"/><rect x="16" y="361" width="358" height="69" fill="url(#dotsW)" opacity="0.4"/>')
    p.append(esp_machine(40, 352, 72))
    p.append(f'<path d="M290 352 l4 -26 h28 l4 26 z" fill="{CREAM}"/><path d="M296 330 q12 -8 24 0" stroke="{GREY}" stroke-width="1.4" fill="none"/>' + ''.join(f'<ellipse cx="{300+k*9}" cy="324" rx="5" ry="3" fill="{c}"/>' for k, c in enumerate((KRAFT, '#D9A35A', KRAFT))))
    p.append(kiri_sit(195, 352, 2.6))
    p.append(f'<path d="M150 300 q-6 -10 0 -20 M240 300 q6 -10 0 -20" stroke="{MUST}" stroke-width="2" fill="none" stroke-linecap="round"/>')
    return ''.join(p)

# ---------------- roulette ----------------
def roulette_wheel(cx, cy, r, rot=0):
    w = [1, 1, 1, 1, 1, 0.2]; tot = sum(w); p = [f'<circle cx="{cx}" cy="{cy}" r="{r+14}" fill="{KRAFT}"/><circle cx="{cx}" cy="{cy}" r="{r+6}" fill="{CREAM}"/>']
    a = -90 + rot
    for i, wi in enumerate(w):
        sw = 360 * wi / tot; a0, a1 = math.radians(a), math.radians(a + sw)
        col = SEGC[i] if i < 5 else CHAR
        d = f'M{cx} {cy} L{cx+r*math.cos(a0):.1f} {cy+r*math.sin(a0):.1f} A{r} {r} 0 {1 if sw>180 else 0} 1 {cx+r*math.cos(a1):.1f} {cy+r*math.sin(a1):.1f} Z'
        p.append(f'<path d="{d}" fill="{col}"/>')
        if i % 2 == 0 and i < 5:
            p.append(f'<path d="{d}" fill="url(#dotsW)" opacity="0.7"/>')
        am = math.radians(a + sw / 2)
        if i < 5:
            hx, hy = cx + r * 0.64 * math.cos(am), cy + r * 0.64 * math.sin(am)
            p.append(f'<circle cx="{hx:.1f}" cy="{hy:.1f}" r="{r*0.2:.1f}" fill="{CREAM}"/>' + pg(hx - 2, hy + r * 0.2, r * 0.0105, *MEMBERS[i]))
        else:
            hx, hy = cx + r * 0.8 * math.cos(am), cy + r * 0.8 * math.sin(am)
            p.append(f'<path d="M{hx:.1f} {hy-7:.1f} l2 5 5 2 -5 2 -2 5 -2 -5 -5 -2 5 -2 z" fill="{MUST}"/>')
        a += sw
    p.append(''.join(f'<circle cx="{cx+(r+10)*math.cos(math.radians(k)):.1f}" cy="{cy+(r+10)*math.sin(math.radians(k)):.1f}" r="2.4" fill="{MUST}"/>' for k in range(0, 360, 15)))
    p.append(f'<circle cx="{cx}" cy="{cy}" r="{r*0.16:.1f}" fill="{CHAR}"/><ellipse cx="{cx}" cy="{cy}" rx="{r*0.06:.1f}" ry="{r*0.09:.1f}" fill="{KRAFT}" transform="rotate(18 {cx} {cy})"/>')
    return ''.join(p)

def roulette():
    p = [room(520)]
    p.append(window(24, 90, 92, 150) + window(274, 90, 92, 150))
    p.append(f'<rect x="188" y="470" width="14" height="80" fill="{CHAR}"/><rect x="150" y="544" width="90" height="12" rx="4" fill="{CHAR}"/>')
    p.append(roulette_wheel(195, 330, 132, rot=-20))
    p.append(f'<path d="M181 172 h28 l-14 26 z" fill="{RED}"/><circle cx="195" cy="176" r="5" fill="{CREAM}"/>')
    p.append(''.join(f'<path d="M{x} {y} q8 -10 16 0" stroke="{CHAR}" stroke-width="2.4" fill="none" stroke-linecap="round" transform="rotate({r} {x} {y})"/>' for x, y, r in ((40, 330, -30), (46, 300, -10), (336, 300, 20), (340, 270, 30))))
    p.append(kiri_sit(330, 548, 2.0))
    p.append(pg(60, 552, 1.0, *MEMBERS[4]))
    return ''.join(p)

# ---------------- result ----------------
def result():
    p = [f'<rect width="390" height="844" fill="#F3E2D2"/>']
    p.append(f'<path d="M195 0 L80 470 H310 Z" fill="#FFF3D6" opacity="0.8"/>')
    p.append(f'<ellipse cx="195" cy="420" rx="120" ry="26" fill="#EAD2B6"/>')
    rnd = random.Random(11)
    for _ in range(46):
        x = rnd.uniform(10, 380); y = rnd.uniform(60, 470); c = rnd.choice([MUST, CORAL, TEAL, ORANGE, LBLUE, RED]); a = rnd.uniform(0, 180)
        p.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{rnd.choice([5,7,9])}" height="4" fill="{c}" transform="rotate({a:.0f} {x:.0f} {y:.0f})"/>')
    p.append(pg(195, 420, 3.2, *MEMBERS[2], wing_up=True))
    p.append(kiri_sit(72, 432, 2.0, bandana=True) + f'<rect x="88" y="356" width="44" height="30" rx="3" fill="{CREAM}"/><rect x="104" y="384" width="3" height="30" fill="{BROWN}"/><path d="M96 366 h28 M96 374 h20" stroke="{CHAR}" stroke-width="2" stroke-linecap="round"/>')
    p.append(pg(320, 432, 1.3, *MEMBERS[0], flip=True) + pg(352, 440, 1.1, *MEMBERS[3], flip=True))
    return ''.join(p)

# ---------------- fortune lounge ----------------
def lounge():
    p = [f'<rect width="390" height="844" fill="#E8EFEC"/><rect y="0" width="390" height="844" fill="url(#wallpaper)" opacity="0.6"/>']
    p.append(f'<rect y="700" width="390" height="144" fill="{FLOOR}"/><rect y="696" width="390" height="6" fill="{CREAM}"/>')
    p.append(f'<rect x="24" y="560" width="96" height="140" fill="{BROWN}"/>' + ''.join(f'<rect x="{30+k*9}" y="{572+ (k%3)*2}" width="7" height="34" fill="{[CORAL,MUST,TEAL,CREAM,ORANGE,LBLUE,RED,MUST,TEAL][k]}"/>' for k in range(9)) + ''.join(f'<rect x="{30+k*12}" y="{622}" width="10" height="30" fill="{[TEAL_D,PEACH,MUST_L,CORAL,CREAM,TEAL][k]}"/>' for k in range(6)) + f'<rect x="24" y="612" width="96" height="5" fill="{shade(BROWN,0.8)}"/><rect x="24" y="656" width="96" height="5" fill="{shade(BROWN,0.8)}"/>')
    p.append(f'<path d="M250 700 v-70 q0 -24 30 -24 h50 q30 0 30 24 v70 z" fill="{TEAL}"/><rect x="242" y="650" width="136" height="40" rx="14" fill="{TEAL_D}"/><rect x="250" y="690" width="6" height="12" fill="{CHAR}"/><rect x="364" y="690" width="6" height="12" fill="{CHAR}"/>')
    p.append(kiri_curl(310, 644, 1.2))
    p.append(f'<rect x="168" y="664" width="40" height="36" rx="6" fill="{CORAL}"/><path d="M188 664 C170 640 176 610 188 600 C200 610 206 640 188 664 Z" fill="{TEAL_D}"/><path d="M188 664 C160 650 156 628 166 618 C178 630 184 646 188 664 Z M188 664 C216 650 220 628 210 618 C198 630 192 646 188 664 Z" fill="{TEAL}"/>')
    p.append(f'<rect x="166" y="0" width="2" height="44" fill="{CHAR}"/><path d="M152 60 Q167 34 182 60 Z" fill="{MUST}"/><ellipse cx="167" cy="80" rx="60" ry="40" fill="url(#glow)" opacity="0.6"/>')
    return ''.join(p)

def cup_icon():
    return (f'<ellipse cx="60" cy="96" rx="40" ry="8" fill="{shade(CREAM,0.9)}"/><path d="M26 50 h68 l-6 40 q-2 8 -10 8 h-36 q-8 0 -10 -8 z" fill="{WHITE}"/><path d="M92 58 q16 0 14 14 q-2 12 -16 12" stroke="{WHITE}" stroke-width="6" fill="none"/>'
            f'<ellipse cx="60" cy="50" rx="34" ry="8" fill="#B7814F"/><path d="M60 46 q-8 3 0 7 q8 -3 0 -7 M52 49 q8 4 16 0" stroke="{CREAM}" stroke-width="1.6" fill="none"/>'
            f'<path d="M50 34 q-6 -8 0 -16 M62 32 q-6 -8 0 -16 M74 34 q-6 -8 0 -16" stroke="{GREY}" stroke-width="2" fill="none" stroke-linecap="round"/>'
            f'<path d="M40 70 h40" stroke="{MUST}" stroke-width="5"/><path d="M40 70 h40" stroke="url(#dotsW)" stroke-width="5"/>')

# ---------------- vibe (rainy window seat, evening) ----------------
def vibe():
    p = [f'<rect width="390" height="844" fill="#3A4656"/>']
    # big window
    p.append(f'<rect x="30" y="80" width="330" height="430" rx="10" fill="{CREAM}"/><rect x="42" y="92" width="306" height="406" fill="#566A7C"/>')
    p.append(f'<g>' + house(60, 498, 60, 120, '#7A8C9C', '#46586A', roof_h=24, cols=2, rows=3, win='#F2C76E') + house(136, 498, 70, 80, '#8A97A3', '#46586A', roof_h=28, cols=2, rows=2, win='#F2C76E') + house(222, 498, 54, 150, '#6E8294', '#3E4E60', roof_h=20, cols=2, rows=4, win='#F2C76E') + house(290, 498, 50, 96, '#7E8E9C', '#46586A', roof_h=22, cols=1, rows=3, win='#F2C76E') + '</g>')
    rnd = random.Random(4)
    p.append(''.join(f'<path d="M{(x:=rnd.uniform(44,346)):.0f} {(y:=rnd.uniform(96,490)):.0f} l-4 14" stroke="#C9D8E6" stroke-width="1.3" stroke-linecap="round" opacity="0.7"/>' for _ in range(90)))
    p.append(''.join(f'<ellipse cx="{rnd.uniform(50,340):.0f}" cy="{rnd.uniform(110,480):.0f}" rx="2.2" ry="3" fill="#DCE7F0" opacity="0.6"/>' for _ in range(30)))
    p.append(f'<rect x="191" y="92" width="8" height="406" fill="{CREAM}"/><rect x="42" y="290" width="306" height="7" fill="{CREAM}"/>')
    p.append(f'<rect x="20" y="506" width="350" height="16" rx="4" fill="{KRAFT}"/>')
    # sill: cushion + kiri + cup
    p.append(f'<ellipse cx="120" cy="506" rx="70" ry="16" fill="{CORAL}"/><ellipse cx="120" cy="500" rx="62" ry="12" fill="{PEACH}"/>' + kiri_curl(120, 488, 1.6))
    p.append(f'<path d="M262 506 h36 l-4 -32 h-28 z" fill="{CREAM}"/><path d="M296 482 q12 0 10 10 q-2 8 -12 8" stroke="{CREAM}" stroke-width="4" fill="none"/><path d="M272 462 q-6 -10 0 -20 M284 460 q-6 -10 0 -20" stroke="{CREAM}" stroke-width="2" fill="none" stroke-linecap="round" opacity="0.7"/>')
    p.append(f'<ellipse cx="195" cy="470" rx="190" ry="70" fill="url(#glow)" opacity="0.35"/>')
    return ''.join(p)

# ---------------- game icons (120x120) ----------------
def icon_hand():
    return pg(58, 104, 2.0, *MEMBERS[0], wing_up=True, coin=True)
def icon_roulette():
    return roulette_wheel(60, 60, 42) + f'<path d="M52 4 h16 l-8 14 z" fill="{RED}"/>'
def icon_kiri():
    return bowl(30, 98, CORAL, s=0.9) + bowl(90, 98, TEAL, s=0.9) + kiri_sit(60, 90, 2.4)
def icon_espresso():
    return esp_machine(24, 108, 72, 1.0) + f'<path d="M50 88 h20 l-2 14 h-16 z" fill="{WHITE}"/>'
def icon_knock():
    p = []
    for i, x in enumerate((24, 60, 96)):
        rot = -18 if i == 1 else 0
        p.append(f'<g transform="rotate({rot} {x} 100)"><path d="M{x-14} 70 h28 l-4 30 h-20 z" fill="{[CREAM, WHITE, CREAM][i]}"/><rect x="{x-14}" y="80" width="28" height="7" fill="{[TEAL, CORAL, MUST][i]}"/></g>')
    p.append(f'<ellipse cx="58" cy="62" rx="10" ry="4" fill="#8A5A3C"/><circle cx="48" cy="52" r="3.4" fill="#8A5A3C"/><circle cx="66" cy="48" r="2.6" fill="#8A5A3C"/><circle cx="58" cy="42" r="2" fill="#8A5A3C"/><circle cx="74" cy="58" r="2.2" fill="#8A5A3C"/>')
    p.append(''.join(f'<path d="M{x} {y} q6 -8 12 0" stroke="{CHAR}" stroke-width="2.4" fill="none" stroke-linecap="round" transform="rotate({r} {x} {y})"/>' for x, y, r in ((34, 40, -20), (82, 30, 20))))
    return ''.join(p)
def icon_box():
    p = []
    for i, x in enumerate((26, 94)):
        p.append(f'<path d="M{x-20} 104 v-34 h40 v34 z" fill="{KRAFT}"/><path d="M{x-22} 70 h44 l-4 -8 h-36 z" fill="{KRAFT_D}"/><rect x="{x-4}" y="70" width="8" height="34" fill="{CREAM}" opacity="0.5"/>')
    p.append(f'<path d="M40 104 v-30 h40 v30 z" fill="{KRAFT}"/><path d="M38 74 l8 -18 h28 l6 18 z" fill="{KRAFT_D}" transform="rotate(-14 60 74)"/>')
    p.append(f'<path d="M80 92 C96 88 100 72 92 64" stroke="{CAT}" stroke-width="5" fill="none" stroke-linecap="round"/><circle cx="50" cy="70" r="1.6" fill="{CHAR}"/><circle cx="58" cy="70" r="1.6" fill="{CHAR}"/><path d="M46 66 l2 -8 l4 6 M58 64 l4 -6 l2 8" fill="{CAT}"/>')
    return ''.join(p)

def avatar(i):
    body, acc = MEMBERS[i]
    return pg(52, 112, 2.3, body, acc)
def avatar_guest():
    return pg(52, 112, 2.3, '#BFC4C8', None)

def svg_raw(inner, w, h):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><defs>{DEFS}</defs><g filter="url(#hand)">{inner}</g></svg>'

if __name__ == '__main__':
    scenes = {'home_day': home(), 'home_night': home(True), 'cafe': cafe_select(), 'roulette': roulette(), 'result': result(), 'lounge': lounge(), 'vibe': vibe()}
    for n, s in scenes.items():
        open(f'{OUT}/{n}.html', 'w').write(page(wrap(s)))
    small = {'ic_hand': icon_hand(), 'ic_roulette': icon_roulette(), 'ic_kiri': icon_kiri(), 'ic_espresso': icon_espresso(), 'ic_knock': icon_knock(), 'ic_box': icon_box(), 'ic_cup': cup_icon()}
    for i in range(5):
        small[f'av{i}'] = avatar(i)
    small['av_guest'] = avatar_guest()
    for n, s in small.items():
        open(f'{OUT}/{n}.html', 'w').write(f'<!doctype html><html><head><meta charset="utf-8"><style>html,body{{margin:0;background:transparent}}</style></head><body style="width:120px;height:120px">{svg_raw(s,120,120)}</body></html>')
    print('ok')
