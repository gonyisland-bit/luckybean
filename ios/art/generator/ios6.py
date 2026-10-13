"""Round 6 scenes."""
import math, random, json
import f_kit
from f_kit import *
import ios
from ios import MEMBERS, SEGC, shade, a_tree
from ios4 import gauge
import kiri
from pg6 import pg2, straw, S as PS, M as PM, L as PL

OUT = '/home/claude/lb_art/ios'
BEANS = ['#6B3E22', '#7A4A2E', '#8A5A3C', '#5C3520']

# ---------------- shared ----------------
def pavement(y0=150):
    p = [f'<rect y="{y0}" width="390" height="{844-y0}" fill="#E8E0D2"/>']
    y = y0; row = 0
    while y < 844:
        h = 16 + (y - y0) * 0.045
        w = h * 2.2
        off = (row % 2) * w / 2
        p.append(f'<rect x="0" y="{y+h-1.2:.1f}" width="390" height="1.2" fill="#D6CCBA"/>')
        x = -off
        while x < 390:
            p.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="1.2" height="{h:.1f}" fill="#D6CCBA"/>')
            x += w
        y += h; row += 1
    return ''.join(p)

def facade_strip(h=150):
    p = [f'<rect width="390" height="{h}" fill="{TEAL_D}"/>']
    for i, x in enumerate((14, 140, 266)):
        if i == 1:
            p.append(f'<rect x="{x+20}" y="0" width="70" height="{h-14}" fill="{TEAL}"/><rect x="{x+30}" y="0" width="50" height="{h-40}" fill="#FBE3B0"/><circle cx="{x+78}" cy="{h-50}" r="3" fill="{MUST}"/>')
        else:
            p.append(f'<rect x="{x}" y="0" width="110" height="{h-30}" fill="#FBE3B0"/><rect x="{x}" y="{h-58}" width="110" height="4" fill="{BROWN}"/>' + ''.join(f'<rect x="{x+10+k*24}" y="{h-72}" width="14" height="14" rx="3" fill="{[WHITE, CORAL, TEAL, MUST][k]}"/>' for k in range(4)))
    p.append(f'<rect x="0" y="{h-14}" width="390" height="14" fill="{CHAR}"/>')
    return ''.join(p)

def shadow(x, y, rx=22):
    return f'<ellipse cx="{x}" cy="{y+2}" rx="{rx}" ry="{rx*0.28:.1f}" fill="#000" opacity="0.1"/>'

def feather(x, y, a=0, c='#C9CED2'):
    return f'<path d="M{x} {y} q6 -8 14 -6 q-4 8 -14 6 z" fill="{c}" transform="rotate({a} {x} {y})"/>'

def credit_card(x, y, a=-8, s=1.0):
    return (f'<g transform="translate({x} {y}) rotate({a}) scale({s})"><rect x="-38" y="-24" width="76" height="48" rx="7" fill="{TEAL_D}"/>'
            f'<rect x="-38" y="-12" width="76" height="9" fill="{CHAR}" opacity="0.5"/><rect x="-28" y="4" width="14" height="11" rx="2" fill="{MUST}"/>'
            f'<rect x="4" y="9" width="26" height="3" rx="1.5" fill="{CREAM}" opacity="0.8"/><circle cx="24" cy="-16" r="4" fill="{CORAL}"/><circle cx="29" cy="-16" r="4" fill="{MUST}" opacity="0.85"/></g>')

# ---------------- 1. card hug ----------------
CARD_SPOTS = [(92, 400), (262, 380), (160, 540), (300, 590), (96, 700)]
def card_scene(hit=False):
    p = [facade_strip(150), pavement(150)]
    p.append(f'<rect x="324" y="150" width="62" height="40" rx="4" fill="{BROWN}"/>' + ''.join(f'<circle cx="{332+k*12}" cy="152" r="7" fill="{[RED, MUST, CORAL, RED, MUST][k]}"/>' for k in range(5)))
    for i, (x, y) in enumerate(CARD_SPOTS):
        body, acc = MEMBERS[i]
        if not hit and i == 2:
            p.append(feather(x - 10, y - 4, 20) + feather(x + 8, y - 2, -40))
            continue
        if hit and i == 3:
            p.append(shadow(x + 2, y + 4, 40) + credit_card(x + 2, y - 2, -8, 1.0))
            continue
        if hit and i == 2:
            continue
        p.append(shadow(x, y, 30) + pg2(x, y, PM, body, acc, 'sit', flip=(i % 2 == 1)))
    if not hit:
        p.append(pg2(312, 300, PS, *MEMBERS[2], pose='fly') + feather(282, 330, 60))
    else:
        p.append(pg2(312, 566, PM, *MEMBERS[3], pose='flap', eyes='wide', flip=True))
        p.append(''.join(f'<path d="M{x} {y} l{dx} {dy}" stroke="{MUST}" stroke-width="3" stroke-linecap="round"/>' for x, y, dx, dy in ((246, 588, -14, -6), (250, 614, -14, 6), (356, 590, 14, -6), (352, 616, 14, 6))))
    return ''.join(p)

# ---------------- 2. roasting roulette ----------------
W6 = [1, 1, 1, 1, 1, 0.2]
SILVER, SILVER_D, SILVER_L, FLOOR6 = '#C8CED3', '#A9B1B8', '#EEF1F3', '#DCE1E5'
def _wedge(cx, cy, r, a0, a1):
    a0r, a1r = math.radians(a0), math.radians(a1)
    big = 1 if (a1 - a0) > 180 else 0
    return f'M{cx} {cy} L{cx+r*math.cos(a0r):.1f} {cy+r*math.sin(a0r):.1f} A{r} {r} 0 {big} 1 {cx+r*math.cos(a1r):.1f} {cy+r*math.sin(a1r):.1f} Z'
def roast_scene(result=False, rot=-14):
    """Silver roaster drum seen from above, filled to the brim with beans (paddles hidden).
    Names are painted on the drum floor; on stop, beans drain from the winning wedge under the arrow and reveal the name."""
    cx, cy, R = 195, 410, 150
    RI = R - 16
    p = [f'<rect width="390" height="844" fill="#D9C4A4"/>' + ''.join(f'<rect x="0" y="{y}" width="390" height="1.4" fill="#C9B391"/>' for y in range(20, 844, 28))]
    # drum body
    p.append(f'<circle cx="{cx+6}" cy="{cy+12}" r="{R+14}" fill="#000" opacity="0.13"/>')
    p.append(f'<circle cx="{cx}" cy="{cy}" r="{R+12}" fill="{SILVER_D}"/><circle cx="{cx}" cy="{cy}" r="{R+6}" fill="{SILVER}"/>')
    p.append(f'<path d="M{cx-R+4} {cy-40} A{R+2} {R+2} 0 0 1 {cx+40} {cy-R+4}" stroke="{SILVER_L}" stroke-width="6" fill="none" stroke-linecap="round"/>')
    p.append(''.join(f'<circle cx="{cx+(R+3)*math.cos(math.radians(k)):.1f}" cy="{cy+(R+3)*math.sin(math.radians(k)):.1f}" r="2.6" fill="{SILVER_D}"/>' for k in range(0, 360, 24)))
    p.append(f'<circle cx="{cx}" cy="{cy}" r="{RI+2}" fill="{SILVER_D}"/>')
    # floor (brushed silver) with segment lines
    p.append(f'<circle cx="{cx}" cy="{cy}" r="{RI}" fill="{FLOOR6}"/>')
    p.append(''.join(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#CDD3D8" stroke-width="1.2"/>' for r in range(20, RI, 14)))
    tot = sum(W6); a = -90 - (360 * W6[2] / tot) / 2; bounds = []   # winner (index 2) centred under the arrow
    order = [2, 3, 4, 5, 0, 1]
    for i in order:
        sw = 360 * W6[i] / tot
        bounds.append((i, a, a + sw)); a += sw
    for i, a0, a1 in bounds:
        p.append(f'<path d="M{cx} {cy} L{cx+RI*math.cos(math.radians(a0)):.1f} {cy+RI*math.sin(math.radians(a0)):.1f}" stroke="{SILVER_D}" stroke-width="2.4"/>')
    win = [bb for bb in bounds if bb[0] == 2][0]
    rnd = random.Random(7)
    # beans: dense fill (mask out the winning wedge on result)
    mask = ''
    if result:
        mask = f'<mask id="drain"><rect width="390" height="844" fill="white"/><path d="{_wedge(cx, cy, RI+4, win[1], win[2])}" fill="black"/></mask>'
    beans = [f'<circle cx="{cx}" cy="{cy}" r="{RI}" fill="#4A2A17"/>']
    step = 8.6
    yy = cy - RI
    row = 0
    while yy < cy + RI + step:
        xx = cx - RI + (row % 2) * step / 2
        while xx < cx + RI + step:
            jx, jy = rnd.uniform(-2.2, 2.2), rnd.uniform(-2.2, 2.2)
            bx, by = xx + jx, yy + jy
            if math.hypot(bx - cx, by - cy) < RI - 3:
                ang = math.degrees(math.atan2(by - cy, bx - cx)) + 90 + rnd.uniform(-35, 35)
                beans.append(f'<g transform="rotate({ang:.0f} {bx:.1f} {by:.1f})"><ellipse cx="{bx:.1f}" cy="{by:.1f}" rx="5.8" ry="4" fill="{rnd.choice(BEANS)}"/><path d="M{bx-4.2:.1f} {by:.1f} q4.2 1.4 8.4 0" stroke="#2E190C" stroke-width="1" fill="none"/></g>')
            xx += step
        yy += step * 0.88; row += 1
    p.append(mask + (f'<g mask="url(#drain)">' if result else '<g>') + ''.join(beans) + '</g>')
    if not result:
        # motion swirl on top of the beans + hub cap
        p.append(''.join(f'<path d="M{cx+math.cos(math.radians(k))*36:.1f} {cy+math.sin(math.radians(k))*36:.1f} A{70} {70} 0 0 1 {cx+math.cos(math.radians(k+70))*96:.1f} {cy+math.sin(math.radians(k+70))*96:.1f}" stroke="{CREAM}" stroke-width="3" fill="none" stroke-linecap="round" opacity="0.55"/>' for k in (10, 130, 250)))
    else:
        # a few stragglers in the emptied wedge + beans tumbling over the rim
        for _ in range(7):
            ang = math.radians(rnd.uniform(win[1] + 6, win[2] - 6)); rr = rnd.uniform(40, RI - 10)
            bx, by = cx + rr * math.cos(ang), cy + rr * math.sin(ang)
            p.append(f'<ellipse cx="{bx:.1f}" cy="{by:.1f}" rx="5.4" ry="3.8" fill="{rnd.choice(BEANS)}" transform="rotate({rnd.uniform(0,180):.0f} {bx:.1f} {by:.1f})"/>')
        for bx, by, rr in ((cx - 70, cy - R - 6, 30), (cx - 56, cy - R - 20, 70), (cx + 64, cy - R - 10, -20), (cx + 78, cy - R - 24, 50)):
            p.append(f'<ellipse cx="{bx}" cy="{by}" rx="5.4" ry="3.8" fill="{BEANS[1]}" transform="rotate({rr} {bx} {by})"/>')
        p.append(f'<path d="M{cx-86} {cy-R-14} l-6 -6 M{cx+92} {cy-R-18} l6 -6" stroke="{CHAR}" stroke-width="1.6" stroke-linecap="round" opacity="0.4"/>')
    p.append(f'<circle cx="{cx}" cy="{cy}" r="17" fill="{SILVER}"/><circle cx="{cx}" cy="{cy}" r="11" fill="{SILVER_L}"/><circle cx="{cx-3}" cy="{cy-3}" r="3.4" fill="{WHITE}"/>')
    # arrow
    p.append(f'<path d="M{cx-18} {cy-R-26} h36 l-18 30 z" fill="{RED}"/><rect x="{cx-22}" y="{cy-R-34}" width="44" height="10" rx="4" fill="{CHAR}"/>')
    wand = [(54, 214, 'peck', False, 0), (338, 230, 'stand', True, 1), (48, 650, 'stand', False, 3), (342, 664, 'peck', True, 4), (200, 712, 'stand', False, 2)]
    for x, y, pose, fl, mi in wand:
        if result and mi == 2:
            continue
        p.append(shadow(x, y, 20) + pg2(x, y, PS, *MEMBERS[mi], pose=pose, flip=fl))
    if result:
        p.append(pg2(cx - 2, cy - R - 34, PM, *MEMBERS[2], pose='flap'))
    am = math.radians((win[1] + win[2]) / 2)
    json.dump({'reveal': [round(cx + RI * 0.6 * math.cos(am), 1), round(cy + RI * 0.6 * math.sin(am), 1)]}, open(f'{OUT}/roast_labels.json', 'w'))
    return ''.join(p)

# ---------------- 3. Kiri lawn (top view) ----------------
def kiri_top(x, y, s=1.0, ang=0):
    C = CAT; D = '#C9722A'
    return f'''<g transform="translate({x} {y}) rotate({ang}) scale({s})">
<path d="M0 16 C2 30 -10 36 -6 46" stroke="{C}" stroke-width="5" fill="none" stroke-linecap="round"/>
<ellipse cx="-9" cy="10" rx="3.4" ry="4.6" fill="{C}"/><ellipse cx="9" cy="10" rx="3.4" ry="4.6" fill="{C}"/>
<ellipse cx="-8" cy="-10" rx="3" ry="4.4" fill="{C}"/><ellipse cx="8" cy="-6" rx="3" ry="4.4" fill="{C}"/>
<ellipse cx="0" cy="2" rx="10.5" ry="17" fill="{C}"/>
<path d="M-8 -4 q8 3 16 0 M-9 3 q9 3 18 0 M-8 10 q8 3 16 0" stroke="{D}" stroke-width="2" fill="none" stroke-linecap="round"/>
<path d="M0 -10 v20" stroke="{D}" stroke-width="2" stroke-linecap="round"/>
<path d="M-7 -21 L-6 -31 L-1 -24 Z M7 -21 L6 -31 L1 -24 Z" fill="{C}"/>
<ellipse cx="0" cy="-20" rx="8.4" ry="7.6" fill="{C}"/>
<path d="M-2.4 -25 v4 M0 -25.6 v4.4 M2.4 -25 v4" stroke="{D}" stroke-width="1.3" stroke-linecap="round"/>
</g>'''

def bowl_top(x, y, col, s=1.0):
    rnd = random.Random(int(x + y))
    kib = ''.join(f'<circle cx="{x+rnd.uniform(-12,12)*s:.1f}" cy="{y+rnd.uniform(-12,12)*s:.1f}" r="{2.6*s:.1f}" fill="{KRAFT}"/>' for _ in range(12))
    return (f'<ellipse cx="{x+3}" cy="{y+4}" rx="{30*s}" ry="{30*s}" fill="#000" opacity="0.08"/><circle cx="{x}" cy="{y}" r="{30*s}" fill="{col}"/>'
            f'<circle cx="{x}" cy="{y}" r="{21*s}" fill="#7A4A2E"/>{kib}')

BOWLS6 = [(72, 570), (118, 420), (195, 360), (272, 420), (318, 570)]
def kiri_lawn():
    p = [f'<rect width="390" height="844" fill="#BFD8A8"/>']
    p.append(''.join(f'<rect x="{x}" y="0" width="40" height="844" fill="#C9E0B4" opacity="0.6"/>' for x in range(0, 390, 80)))
    p.append(f'<path d="M-20 780 C80 720 140 820 260 760 S380 700 420 740" stroke="#E9E0CC" stroke-width="40" fill="none" stroke-linecap="round"/>')
    rnd = random.Random(9)
    p.append(''.join(f'<path d="M{(x:=rnd.uniform(0,390)):.0f} {(y:=rnd.uniform(0,844)):.0f} l2 -4 l2 4" stroke="#A5C48F" stroke-width="1.4" fill="none" stroke-linecap="round"/>' for _ in range(140)))
    p.append(''.join(f'<circle cx="{rnd.uniform(0,390):.0f}" cy="{rnd.uniform(160,840):.0f}" r="3" fill="{rnd.choice([WHITE, MUST, CORAL])}"/>' for _ in range(30)))
    for i, (x, y) in enumerate(BOWLS6):
        p.append(bowl_top(x, y, SEGC[i], 1.3))
    trail = [(195, 790), (205, 760), (196, 730), (210, 700), (222, 668), (232, 636), (244, 604)]
    p.append(''.join(f'<g transform="translate({x} {y})"><ellipse cx="0" cy="0" rx="3.4" ry="4" fill="#9DB989"/><circle cx="-3.4" cy="-5" r="1.4" fill="#9DB989"/><circle cx="0" cy="-6" r="1.4" fill="#9DB989"/><circle cx="3.4" cy="-5" r="1.4" fill="#9DB989"/></g>' for x, y in trail))
    p.append(kiri_top(250, 524, 2.4, ang=28))
    return ''.join(p)

# ---------------- 4. straw draw ----------------
STRAWS = [(110, 500, 300, -8), (160, 480, 330, -2), (205, 490, 310, 4), (250, 485, 340, 8), (292, 505, 290, 14)]  # base x,y, length, tilt
def straw_scene(hit=False):
    p = [f'<rect width="390" height="844" fill="{KRAFT}"/>' + ''.join(f'<rect x="0" y="{y}" width="390" height="3" fill="{KRAFT_D}" opacity="0.6"/>' for y in range(40, 844, 70))]
    p.append(f'<path d="M330 90 q20 -30 46 -10 q-20 24 -46 10 z" fill="{TEAL}"/>')
    # cup body (front wall below rim)
    p.append(f'<path d="M30 520 L58 844 H332 L360 520 Z" fill="#E7F1F4" opacity="0.75"/>')
    p.append(f'<path d="M30 520 L58 844 H332 L360 520 Z" fill="#C9A47A" opacity="0.35"/>')
    rnd = random.Random(4)
    p.append(''.join(f'<ellipse cx="{rnd.uniform(60,330):.0f}" cy="{rnd.uniform(560,830):.0f}" rx="2.4" ry="3.2" fill="{WHITE}" opacity="0.8"/>' for _ in range(40)))
    # rim + liquid surface
    p.append(f'<ellipse cx="195" cy="520" rx="168" ry="62" fill="#B98A5E"/><ellipse cx="195" cy="520" rx="168" ry="62" fill="none" stroke="#F4FAFB" stroke-width="8"/>')
    p.append(f'<ellipse cx="195" cy="524" rx="150" ry="50" fill="#C99B6C"/><path d="M80 520 q60 -24 120 0 q60 24 110 -6" stroke="#E7CBA8" stroke-width="6" fill="none" opacity="0.7"/>')
    for (x, y, a) in ((110, 520, 12), (190, 545, -8), (270, 515, 20), (230, 500, 0), (150, 500, -20)):
        p.append(f'<rect x="{x-20}" y="{y-14}" width="40" height="28" rx="8" fill="{WHITE}" opacity="0.55" transform="rotate({a} {x} {y})"/>')
    cols = [CORAL, LBLUE, MUST, TEAL_L, PEACH]
    for i, (bx, by, L, tilt) in enumerate(STRAWS):
        gone = (not hit and i in (1, 4)) or (hit and i in (0, 1, 2, 4))
        if gone:
            continue
        if hit and i == 3:
            continue
        tx = bx + L * math.sin(math.radians(tilt)); ty = by - L * math.cos(math.radians(tilt))
        p.append(straw(bx, by, round(tx, 1), round(ty, 1), cols[i], w=10))
    if not hit:
        p.append(straw(338, 110, 368, 300, cols[1], w=10) + pg2(310, 150, PM, *MEMBERS[1], pose='fly'))
        p.append(straw(46, 80, 20, 230, cols[4], w=8) + pg2(70, 112, PS, *MEMBERS[4], pose='fly', flip=True))
    else:
        p.append(f'<path d="M258 468 q14 -10 8 -40 q-8 -22 6 -40 q14 -18 2 -40 q-10 -18 4 -38 L272 260" stroke="{WHITE}" stroke-width="10" fill="none" stroke-linecap="round"/>'
                 f'<path d="M258 468 q14 -10 8 -40 q-8 -22 6 -40 q14 -18 2 -40 q-10 -18 4 -38 L272 260" stroke="{cols[3]}" stroke-width="10" stroke-dasharray="10 10" fill="none"/>')
        p.append(pg2(252, 262, PM, *MEMBERS[3], pose='flap', eyes='wide'))
        p.append(feather(200, 220, 30) + feather(320, 300, -50) + feather(210, 320, 80))
    return ''.join(p)

# ---------------- 5. pigeon jump (roof) ----------------
def roof_scene_jump():
    p = [f'<rect width="390" height="844" fill="#CFE3E6"/>']
    p.append(''.join(f'<g transform="translate({x} {y})"><ellipse cx="0" cy="0" rx="34" ry="11" fill="{WHITE}"/><ellipse cx="-12" cy="-8" rx="16" ry="11" fill="{WHITE}"/><ellipse cx="12" cy="-9" rx="13" ry="10" fill="{WHITE}"/></g>' for x, y in ((90, 170), (300, 120), (230, 300))))
    # far rooftops strip
    # Lucky Bean's roof among the far rooftops (same pink wall + dark scalloped roof + yellow sign)
    j_lb = (f'<rect x="222" y="676" width="64" height="168" fill="#E9C3B6"/><path d="M216 676 L230 652 H278 L292 676 Z" fill="{CHAR}"/><path d="M216 676 L230 652 H278 L292 676 Z" fill="url(#scallopW)" opacity="0.5"/>'
            f'<rect x="266" y="638" width="8" height="16" fill="{CHAR}"/><rect x="236" y="690" width="36" height="7" rx="2" fill="{MUST}"/>' + ''.join(f'<path d="M{x-5} 718 V710 a5 5 0 0 1 10 0 V718 Z" fill="#FBE3B0"/>' for x in (238, 254, 270)))
    for x, w, h, c in ((150, 70, 120, '#B7C9CC'), (280, 80, 140, '#B7C9CC'), (360, 60, 100, '#A9BDC0')):
        p.append(f'<rect x="{x}" y="{760-h}" width="{w}" height="{h+84}" fill="{c}"/><path d="M{x-4} {760-h} l{w/2+4} -18 l{w/2+4} 18 z" fill="{shade(c,0.85)}"/>')
    p.append(j_lb)
    p.append(f'<rect x="140" y="756" width="250" height="88" fill="#9FB3B6"/>')
    # our roof (left, big)
    p.append(f'<path d="M-40 844 L-40 560 L150 560 L180 844 Z" fill="{CHAR}"/><path d="M-40 844 L-40 560 L150 560 L180 844 Z" fill="url(#scallopW)" opacity="0.6"/>')
    p.append(f'<rect x="-40" y="552" width="196" height="12" rx="4" fill="{CREAM}"/><rect x="40" y="480" width="34" height="76" fill="{CHAR}"/><rect x="34" y="472" width="46" height="12" fill="{CREAM}"/>')
    p.append(f'<path d="M140 520 Q240 320 330 700" stroke="{TEAL_D}" stroke-width="3" stroke-dasharray="2 10" fill="none" stroke-linecap="round" opacity="0.7"/>')
    p.append(pg2(124, 552, PM, *MEMBERS[2], pose='sit'))
    for x, mi in ((322, 0), (262, 1)):
        y = 760 - (140 if x > 280 else 108)
        p.append(f'<rect x="{x-1.2}" y="{y-40}" width="2.4" height="40" fill="{CHAR}"/><path d="M{x+1} {y-40} h18 l-5 6 l5 6 h-18 z" fill="{SEGC[mi]}"/>' + pg2(x - 12, y, 0.8, *MEMBERS[mi], pose='stand'))
    return ''.join(p)

# ---------------- 6. espresso with current pigeon ----------------
def espresso6():
    import ios5
    return ios5.espresso5() + shadow(330, 530, 20) + pg2(336, 530, PM, *MEMBERS[2], pose='stand', flip=True)

# ---------------- 7. handoff: cafe roof ----------------
def roof_handoff(mi=3):
    p = [f'<rect width="390" height="844" fill="#D8E8EA"/>']
    p.append(''.join(f'<g transform="translate({x} {y})"><ellipse cx="0" cy="0" rx="40" ry="12" fill="{WHITE}"/><ellipse cx="-14" cy="-9" rx="18" ry="12" fill="{WHITE}"/><ellipse cx="14" cy="-10" rx="15" ry="11" fill="{WHITE}"/></g>' for x, y in ((80, 140), (300, 200))))
    p.append(f'<path d="M-20 844 L-20 520 L410 520 L410 844 Z" fill="{CHAR}"/><path d="M-20 844 L-20 520 L410 520 L410 844 Z" fill="url(#scallopW)" opacity="0.65"/>')
    p.append(f'<rect x="-20" y="510" width="430" height="16" rx="5" fill="{CREAM}"/>')
    p.append(f'<path d="M70 760 V640 L120 590 L170 640 V760 Z" fill="{CREAM}"/><rect x="90" y="650" width="60" height="80" fill="{LBLUE}"/><rect x="118" y="650" width="4" height="80" fill="{CREAM}"/><path d="M96 660 l14 0 l-14 22 z" fill="{WHITE}" opacity="0.6"/>')
    p.append(f'<rect x="290" y="420" width="50" height="100" fill="{TEAL_D}"/><rect x="282" y="410" width="66" height="14" fill="{CREAM}"/>')
    p.append(pg2(190, 512, PL, *MEMBERS[mi], pose='flap'))
    p.append(f'<path d="M262 400 v-22 l12 -4 v20" stroke="{CHAR}" stroke-width="3" fill="none" stroke-linecap="round"/><ellipse cx="258" cy="400" rx="5" ry="4" fill="{CHAR}"/><ellipse cx="270" cy="396" rx="5" ry="4" fill="{CHAR}"/>'
             f'<path d="M296 360 v-18" stroke="{CHAR}" stroke-width="3" stroke-linecap="round"/><ellipse cx="292" cy="360" rx="5" ry="4" fill="{CHAR}"/>')
    return ''.join(p)

# ---------------- 8. reveal: everyone flaps, the payer stands trembling ----------------
def reveal6():
    p = [facade_strip(120), pavement(120)]
    p.append(f'<ellipse cx="195" cy="640" rx="120" ry="24" fill="{MUST}" opacity="0.25"/>')
    for (x, y, mi, fl) in ((60, 600, 0, False), (110, 700, 1, False), (290, 700, 3, True), (338, 600, 4, True)):
        p.append(shadow(x, y, 20) + pg2(x, y, PS, *MEMBERS[mi], pose='flap', flip=fl))
    p.append(shadow(195, 640, 34) + pg2(195, 640, PL, *MEMBERS[2], pose='upright'))
    return ''.join(p)

# ---------------- 9. nearby: real-map style ----------------
def nearby_map():
    p = [f'<rect width="390" height="844" fill="#F2EFE9"/>']
    p.append(f'<path d="M-10 610 C80 570 160 640 260 600 S400 560 420 590 V650 C380 620 300 670 220 650 S60 640 -10 670 Z" fill="#B7D7EA"/>')
    p.append(f'<rect x="200" y="120" width="150" height="120" rx="6" fill="#CFE5C2"/>')
    for (x, y, w, h) in ((20, 20, 140, 80), (20, 130, 140, 100), (200, 20, 150, 80), (20, 270, 80, 110), (130, 270, 90, 110), (250, 270, 100, 110), (20, 420, 140, 130), (200, 420, 150, 130), (20, 700, 160, 120), (220, 700, 150, 120)):
        p.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="#E6E1D8"/>')
        rnd = random.Random(x * 7 + y)
        for _ in range(4):
            bw = rnd.uniform(18, 40); bh = rnd.uniform(14, 30)
            p.append(f'<rect x="{x+rnd.uniform(4,w-bw-4):.0f}" y="{y+rnd.uniform(4,h-bh-4):.0f}" width="{bw:.0f}" height="{bh:.0f}" rx="2" fill="#DAD4C9"/>')
    for d, wdt, c in (('M0 110 H390', 14, WHITE), ('M0 255 H390', 22, '#F7E2A6'), ('M180 0 V844', 22, '#F7E2A6'), ('M0 400 H390', 14, WHITE), ('M110 255 V560', 12, WHITE), ('M235 255 V560', 12, WHITE), ('M0 685 H390', 14, WHITE)):
        p.append(f'<path d="{d}" stroke="#E2DCCF" stroke-width="{wdt+3}" fill="none"/><path d="{d}" stroke="{c}" stroke-width="{wdt}" fill="none"/>')
    p.append(f'<path d="M180 330 V255 H300 V200" stroke="#2F6E71" stroke-width="5" stroke-dasharray="2 9" stroke-linecap="round" fill="none"/>')
    p.append(f'<circle cx="180" cy="330" r="34" fill="#3E7CB1" opacity="0.14"/><path d="M180 330 L164 296 A36 36 0 0 1 196 296 Z" fill="#3E7CB1" opacity="0.22"/><circle cx="180" cy="330" r="10" fill="{WHITE}"/><circle cx="180" cy="330" r="7" fill="#3E7CB1"/>')
    for (x, y, big) in ((300, 200, True), (80, 160, False), (300, 330, False), (60, 470, False), (270, 470, False), (120, 760, False)):
        r = 17 if big else 13
        p.append(f'<path d="M{x} {y+r+10} l-{r*0.6:.0f} -{r*0.9:.0f} a{r} {r} 0 1 1 {r*1.2:.0f} 0 z" fill="{"#2F6E71" if big else "#5E9C9E"}"/><circle cx="{x}" cy="{y}" r="{r-4}" fill="{CREAM}"/><path d="M{x-5} {y-4} h10 l-1.4 8 h-7.2 z" fill="{BROWN}"/>')
    return ''.join(p)

# ---------------- 10. night street ----------------
def street_night6():
    import ios2
    old_sky, old_walk, old_pg = ios2.SKY, ios2.kiri_walk2, ios2.pg
    ios2.SKY = '#5A82BD'
    ios2.kiri_walk2 = lambda x, y, s=1.0, flip=False: kiri.curl(x + 6, y - 2, s * 0.8)
    ios2.pg = lambda x, y, s, body, acc, flip=False, **k: pg2(x, y, s, body, acc, 'sit', flip=flip, eyes='closed')
    base = ios2.street()
    ios2.SKY, ios2.kiri_walk2, ios2.pg = old_sky, old_walk, old_pg
    p = [base]
    p.append(f'<rect width="1170" height="844" fill="#8EA6CF" style="mix-blend-mode:multiply"/>')
    p.append(f'<rect width="1170" height="844" fill="#2B4E8A" opacity="0.12"/>')
    rnd = random.Random(3)
    p.append(''.join(f'<path d="M{(x:=rnd.uniform(0,1170)):.0f} {(y:=rnd.uniform(20,330)):.0f} l1.2 3 3 1.2 -3 1.2 -1.2 3 -1.2 -3 -3 -1.2 3 -1.2 z" fill="#FFF6D8"/>' for _ in range(36)))
    p.append(''.join(f'<circle cx="{rnd.uniform(0,1170):.0f}" cy="{rnd.uniform(20,360):.0f}" r="1.2" fill="#FFF6D8"/>' for _ in range(60)))
    p.append(f'<circle cx="960" cy="110" r="28" fill="#FFF3C4"/><circle cx="972" cy="102" r="25" fill="#4E6FA0"/>')
    from ios2 import S, BASE
    cx0 = 585 - 87 * S; pane_w = (174 - 24) / 3
    for i in (0, 2):
        px = cx0 + (8 + i * (pane_w + 4)) * S
        p.append(f'<rect x="{px:.1f}" y="{BASE-60*S:.1f}" width="{pane_w*S:.1f}" height="{30*S:.1f}" fill="#FFD98A"/>')
    for i in range(4):
        wx = cx0 + (14 + i * (174 - 50) / 3) * S
        p.append(f'<path d="M{wx+3*S:.1f} {BASE-112*S:.1f} V{BASE-137*S:.1f} A{8*S} {8*S} 0 0 1 {wx+19*S:.1f} {BASE-137*S:.1f} V{BASE-112*S:.1f} Z" fill="#FFD98A"/>')
    p.append(f'<rect x="{cx0+(8+pane_w+4)*S+ (pane_w*S/2-12*S):.1f}" y="{BASE-52*S:.1f}" width="{16*S:.1f}" height="{22*S:.1f}" fill="#FFD98A"/>')
    p.append(''.join(f'<rect x="{x}" y="{y}" width="10" height="13" fill="#FFD98A"/>' for x, y in ((360, 380), (390, 380), (360, 440), (390, 470), (770, 470), (812, 470), (854, 470), (930, 545), (980, 545), (1068, 545), (1116, 545))))
    for lx in (300, 895):
        p.append(f'<path d="M{lx-34} {BASE+38} L{lx-8} {BASE-60} H{lx+8} L{lx+34} {BASE+38} Z" fill="#FFE9A8" opacity="0.28"/><ellipse cx="{lx}" cy="{BASE+30}" rx="40" ry="9" fill="#FFE9A8" opacity="0.45"/><rect x="{lx-5}" y="{BASE-62}" width="10" height="8" fill="#FFF3C4"/>')
    return ''.join(p)

# ---------------- icons ----------------
def ic_card():
    return credit_card(60, 82, -10, 0.9) + pg2(62, 70, 1.3, *MEMBERS[0], pose='sit')
def ic_roast():
    p = [f'<circle cx="60" cy="64" r="46" fill="{SILVER_D}"/><circle cx="60" cy="64" r="42" fill="{SILVER}"/><circle cx="60" cy="64" r="35" fill="#4A2A17"/>']
    rnd = random.Random(1)
    for k in range(70):
        r = 33 * math.sqrt(rnd.random()); a = rnd.uniform(0, 6.283)
        x, y = 60 + r * math.cos(a), 64 + r * math.sin(a)
        p.append(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="4" ry="2.8" fill="{rnd.choice(BEANS)}" transform="rotate({a*57+90:.0f} {x:.1f} {y:.1f})"/>')
    p.append(f'<circle cx="60" cy="64" r="7" fill="{SILVER_L}"/><path d="M50 6 h20 l-10 16 z" fill="{RED}"/>')
    return ''.join(p)
def ic_straw():
    p = [f'<path d="M24 64 L32 116 H88 L96 64 Z" fill="#E7F1F4"/><ellipse cx="60" cy="64" rx="36" ry="12" fill="#C99B6C"/><ellipse cx="60" cy="64" rx="36" ry="12" fill="none" stroke="#F4FAFB" stroke-width="3"/>']
    for x, tilt, c in ((46, -8, CORAL), (60, 2, MUST), (74, 10, TEAL_L)):
        p.append(straw(x, 64, round(x + 50 * math.sin(math.radians(tilt)), 1), round(64 - 50 * math.cos(math.radians(tilt)), 1), c))
    return ''.join(p)
def ic_jump():
    return (f'<path d="M0 120 L0 84 L50 84 L60 120 Z" fill="{CHAR}"/><rect x="0" y="80" width="54" height="6" rx="2" fill="{CREAM}"/>'
            f'<path d="M44 76 Q80 20 110 90" stroke="{TEAL_D}" stroke-width="2.4" stroke-dasharray="2 7" fill="none" stroke-linecap="round"/>' + pg2(82, 52, 1.0, *MEMBERS[4], pose='fly'))

if __name__ == '__main__':
    from ios import svg_raw
    scenes = {'card_a': card_scene(False), 'card_b': card_scene(True), 'roast_a': roast_scene(False), 'roast_b': roast_scene(True),
              'kiri_lawn': kiri_lawn(), 'straw_a': straw_scene(False), 'straw_b': straw_scene(True), 'jump6': roof_scene_jump(),
              'espresso6': espresso6(), 'handoff6': roof_handoff(), 'reveal6': reveal6(), 'nearby6': nearby_map()}
    for n, s in scenes.items():
        open(f'{OUT}/{n}.html', 'w').write(page(wrap(s)))
    sn = street_night6()
    open(f'{OUT}/night6.html', 'w').write(page(wrap(f'<g transform="translate(-390 0)">{sn}</g>'), 390, 844))
    for n, f in (('i6_card', ic_card), ('i6_roast', ic_roast), ('i6_straw', ic_straw), ('i6_jump', ic_jump)):
        open(f'{OUT}/{n}.html', 'w').write(f'<!doctype html><html><head><meta charset="utf-8"><style>html,body{{margin:0;background:transparent}}</style></head><body style="width:120px;height:120px">{svg_raw("<rect width=\"120\" height=\"120\" fill=\"none\"/>" + f(), 120, 120)}</body></html>')
    print(open(f'{OUT}/roast_labels.json').read())
    import ios2
    ios2.pg = lambda x, y, s, body, acc, flip=False, **k: pg2(x, y, s * 1.1, body, acc, 'stand', flip=flip)
    open(f'{OUT}/home6.html', 'w').write(page(wrap(f'<g transform="translate(-390 0)">{ios2.street()}</g>'), 390, 844))
