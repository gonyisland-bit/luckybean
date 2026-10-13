from f_kit import *
from f_scenes2 import euro_cafe

WALL = '#F6DCCB'; WAIN = TEAL; FLOOR = '#E9D7BC'
NAMES = ['bear', 'rabbit', 'fox', 'dog', 'pigeon']
SEG = [TEAL, MUST, CORAL, ORANGE, LBLUE]
BGS = [TEAL_XL, PEACH, MUST_L, LBLUE, GREY_L]

def room(wall_h=420):
    return (f'<rect width="390" height="{wall_h}" fill="{WALL}"/><rect y="{wall_h-70}" width="390" height="70" fill="{WAIN}"/>'
            f'<rect y="{wall_h-70}" width="390" height="70" fill="url(#stripeV)" opacity="0.35"/><rect y="{wall_h-74}" width="390" height="6" fill="{CREAM}"/>'
            f'<rect y="{wall_h}" width="390" height="{844-wall_h}" fill="{FLOOR}"/><rect y="{wall_h}" width="390" height="5" fill="#D6C1A0"/>')

def window(x, y, w, h, scene=0):
    p = [f'<path d="M{x} {y+h} V{y+w/2} A{w/2} {w/2} 0 0 1 {x+w} {y+w/2} V{y+h} Z" fill="{CREAM}"/>',
         f'<path d="M{x+6} {y+h-6} V{y+w/2} A{w/2-6} {w/2-6} 0 0 1 {x+w-6} {y+w/2} V{y+h-6} Z" fill="{LBLUE}"/>']
    gy = y + h - 6
    p.append(f'<rect x="{x+6}" y="{gy-26}" width="{w-12}" height="26" fill="{MAP}"/>')
    p.append(house(x + 14, gy - 26, 26, 40, MUST, CHAR, roof_h=12, cols=1, rows=2) + house(x + 46, gy - 26, 30, 30, CORAL, TEAL_D, roof_h=12, cols=2, rows=1) + tree(x + w - 22, gy - 26, 9) + (house(x + 84, gy - 26, 24, 48, TEAL, CHAR, roof_h=10, cols=1, rows=2) if w > 130 else ''))
    p.append(f'<rect x="{x+w/2-2}" y="{y+8}" width="4" height="{h-14}" fill="{CREAM}"/><path d="M{x+14} {y+w/2} l14 0 l-14 22 z" fill="#FFFFFF" opacity="0.5"/>')
    return ''.join(p)

def wheel(cx, cy, r, rot=0, rim=True):
    p = []
    if rim:
        p.append(f'<circle cx="{cx}" cy="{cy}" r="{r+9}" fill="{CREAM}"/>')
    for i in range(5):
        a0 = math.radians(-90 - 36 + i * 72 + rot); a1 = math.radians(-90 - 36 + (i + 1) * 72 + rot)
        d = f'M{cx} {cy} L{cx+r*math.cos(a0):.1f} {cy+r*math.sin(a0):.1f} A{r} {r} 0 0 1 {cx+r*math.cos(a1):.1f} {cy+r*math.sin(a1):.1f} Z'
        p.append(f'<path d="{d}" fill="{SEG[i]}"/>')
        if i % 2 == 0:
            p.append(f'<path d="{d}" fill="url(#dotsW)"/>')
    if rim:
        p.append(''.join(f'<circle cx="{cx+(r+4.5)*math.cos(math.radians(a)):.1f}" cy="{cy+(r+4.5)*math.sin(math.radians(a)):.1f}" r="{max(1.6, r/48):.1f}" fill="{MUST}"/>' for a in range(0, 360, 20)))
    p.append(f'<circle cx="{cx}" cy="{cy}" r="{r*0.18:.1f}" fill="{CHAR}"/><ellipse cx="{cx}" cy="{cy}" rx="{r*0.06:.1f}" ry="{r*0.09:.1f}" fill="{KRAFT}" transform="rotate(18 {cx} {cy})"/>')
    return ''.join(p)

def esp_machine(x, base, w=70, scale=1.0):
    s = scale
    return (f'<g transform="translate({x} {base}) scale({s})">'
            f'<rect x="0" y="-60" width="{w}" height="60" rx="6" fill="{MUST}"/><rect x="-4" y="-68" width="{w+8}" height="10" rx="4" fill="{CHAR}"/>'
            f'<circle cx="{w/2}" cy="-40" r="11" fill="{CREAM}"/><path d="M{w/2} -40 l6 -5" stroke="{CHAR}" stroke-width="2" stroke-linecap="round"/>'
            f'<rect x="{w*0.2}" y="-22" width="{w*0.22}" height="8" fill="{CHAR}"/><rect x="{w*0.58}" y="-22" width="{w*0.22}" height="8" fill="{CHAR}"/>'
            + ''.join(f'<rect x="{6+k*14}" y="-78" width="10" height="9" rx="2" fill="{WHITE}"/>' for k in range(int(w // 14))) + '</g>')

def bowl(x, y, col, kibble=True, s=1.0):
    return (f'<g transform="translate({x} {y}) scale({s})"><ellipse cx="0" cy="4" rx="22" ry="5" fill="#000000" opacity="0.08"/>'
            f'<path d="M-20 -6 Q-18 6 0 6 Q18 6 20 -6 Z" fill="{col}"/><ellipse cx="0" cy="-6" rx="20" ry="5" fill="{col}"/><ellipse cx="0" cy="-6" rx="16" ry="3.6" fill="#7A4A2E"/>'
            + (''.join(f'<circle cx="{dx}" cy="{-7+dy}" r="1.8" fill="{KRAFT}"/>' for dx, dy in ((-6, 0), (-1, -1), (5, 0), (9, -1), (-10, 0))) if kibble else '') + '</g>')

def draw_cup(x, base, s=1.0, shaking=False):
    p = [f'<g transform="translate({x} {base}) scale({s})">']
    sticks = [(-8, -50, CORAL), (-3, -56, TEAL), (2, -52, MUST), (7, -58, ORANGE), (11, -50, LBLUE)]
    for dx, top, c in sticks:
        p.append(f'<rect x="{dx-1.5}" y="{top}" width="3" height="{-top-10}" fill="{KRAFT}"/><circle cx="{dx}" cy="{top}" r="3" fill="{c}"/>')
    p.append(f'<path d="M-18 -30 L-14 0 L14 0 L18 -30 Z" fill="{TEAL_D}"/><rect x="-19" y="-33" width="38" height="5" rx="2" fill="{CREAM}"/><ellipse cx="0" cy="-15" rx="6" ry="8" fill="{MUST}" transform="rotate(18 0 -15)"/>')
    p.append('</g>')
    return ''.join(p)

def friends_row(y, s=1.6, xs=(48, 121, 195, 269, 342), bodies=True):
    p = []
    for i, x in enumerate(xs):
        if bodies:
            p.append(f'<path d="M{x-17*s/1.6} {y+40} Q{x-17*s/1.6} {y+8} {x} {y+8} Q{x+17*s/1.6} {y+8} {x+17*s/1.6} {y+40} Z" fill="{BGS[i]}"/>')
        p.append(animal_head(NAMES[i], x, y, s))
    return ''.join(p)

# ---------- café interior (concise) ----------
def cafe2():
    p = [room(430)]
    p.append(window(130, 108, 130, 176))
    p.append(f'<rect x="124" y="282" width="142" height="8" rx="3" fill="{CREAM}"/>')
    p.append(pigeon(232, 282, 1.4))
    for lx in (70, 320):
        p.append(f'<rect x="{lx-1}" y="0" width="2" height="54" fill="{CHAR}"/><path d="M{lx-15} 70 Q{lx} 44 {lx+15} 70 Z" fill="{TEAL_D}"/><ellipse cx="{lx}" cy="90" rx="50" ry="34" fill="url(#glow)" opacity="0.45"/>')
    p.append(f'<rect x="56" y="216" width="4" height="40" fill="{CHAR}"/>' + wheel(58, 176, 40) + f'<path d="M52 128 h12 l-6 10 z" fill="{RED}"/>')
    p.append(f'<rect x="298" y="132" width="66" height="84" rx="4" fill="{CHAR}"/>' + ''.join(f'<rect x="306" y="{146+k*13}" width="{40 if k%2 else 50}" height="2.4" fill="{CREAM}" opacity="0.85"/>' for k in range(5)))
    # counter
    p.append(f'<rect x="10" y="352" width="370" height="9" rx="2" fill="{KRAFT}"/><rect x="16" y="361" width="358" height="69" fill="{TEAL_D}"/><rect x="16" y="361" width="358" height="69" fill="url(#dotsW)" opacity="0.4"/>')
    p.append(esp_machine(52, 352, 72))
    p.append(person(195, 352, 1.15))
    p.append(draw_cup(316, 352, 1.15))
    # floor: cat + bowls
    xs = [70, 132, 195, 258, 320]
    for i, x in enumerate(xs):
        p.append(bowl(x, 512, SEG[i], s=0.95))
    p.append(cat_sit(195, 478, 2.0))
    return ''.join(p)

# ---------- game 1: roulette ----------
def g_roulette():
    p = [room(470)]
    p.append(f'<rect x="191" y="380" width="8" height="90" fill="{CHAR}"/><rect x="160" y="466" width="70" height="8" rx="3" fill="{CHAR}"/>')
    cx, cy, r = 195, 270, 124
    p.append(wheel(cx, cy, r, rot=18))
    for (a0, a1, rr) in ((200, 250, r + 24), (20, 70, r + 24), (110, 140, r + 30), (300, 330, r + 30)):
        x0, y0 = cx + rr * math.cos(math.radians(a0)), cy + rr * math.sin(math.radians(a0)); x1, y1 = cx + rr * math.cos(math.radians(a1)), cy + rr * math.sin(math.radians(a1))
        p.append(f'<path d="M{x0:.1f} {y0:.1f} A{rr} {rr} 0 0 1 {x1:.1f} {y1:.1f}" stroke="{WHITE}" stroke-width="3" stroke-linecap="round" fill="none"/>')
    p.append(f'<path d="M{cx-11} {cy-r-22} L{cx+11} {cy-r-22} L{cx} {cy-r+4} Z" fill="{RED}"/><circle cx="{cx}" cy="{cy-r-24}" r="6" fill="{MUST}"/>')
    p.append(friends_row(498, 1.5))
    p.append(cat_sit(352, 404, 1.6))
    return ''.join(p)

# ---------- game 2: espresso ----------
def g_espresso():
    p = [room(470)]
    p.append(f'<rect x="10" y="400" width="370" height="9" rx="2" fill="{KRAFT}"/>')
    # big machine
    x, base, w = 70, 400, 250
    p.append(f'<rect x="{x}" y="{base-230}" width="{w}" height="230" rx="16" fill="{MUST}"/><rect x="{x-8}" y="{base-246}" width="{w+16}" height="22" rx="8" fill="{CHAR}"/>')
    p.append(''.join(f'<rect x="{x+16+k*30}" y="{base-270}" width="24" height="22" rx="4" fill="{WHITE}"/>' for k in range(8)))
    # gauge
    gx, gy, gr = 195, base - 160, 52
    p.append(f'<circle cx="{gx}" cy="{gy}" r="{gr+8}" fill="{CHAR}"/><circle cx="{gx}" cy="{gy}" r="{gr}" fill="{CREAM}"/>')
    def arc(a0, a1, col, rr=gr - 10, wdt=10):
        x0, y0 = gx + rr * math.cos(math.radians(a0)), gy + rr * math.sin(math.radians(a0)); x1, y1 = gx + rr * math.cos(math.radians(a1)), gy + rr * math.sin(math.radians(a1))
        return f'<path d="M{x0:.1f} {y0:.1f} A{rr} {rr} 0 0 1 {x1:.1f} {y1:.1f}" stroke="{col}" stroke-width="{wdt}" fill="none"/>'
    p.append(arc(150, 230, LBLUE) + arc(230, 285, '#7FBF8A') + arc(285, 300, MUST) + arc(300, 390, CORAL))
    for a in range(150, 391, 15):
        x0, y0 = gx + (gr - 2) * math.cos(math.radians(a)), gy + (gr - 2) * math.sin(math.radians(a)); x1, y1 = gx + (gr - 8) * math.cos(math.radians(a)), gy + (gr - 8) * math.sin(math.radians(a))
        p.append(f'<path d="M{x0:.1f} {y0:.1f} L{x1:.1f} {y1:.1f}" stroke="{CHAR}" stroke-width="1.4"/>')
    na = math.radians(268)
    p.append(f'<path d="M{gx} {gy} L{gx+(gr-14)*math.cos(na):.1f} {gy+(gr-14)*math.sin(na):.1f}" stroke="{RED}" stroke-width="4" stroke-linecap="round"/><circle cx="{gx}" cy="{gy}" r="6" fill="{CHAR}"/>')
    # group head + portafilter + stream + cup
    p.append(f'<rect x="{gx-30}" y="{base-92}" width="60" height="16" rx="4" fill="{CHAR}"/><rect x="{gx-44}" y="{base-80}" width="88" height="12" rx="5" fill="{CHAR}"/><rect x="{gx+44}" y="{base-78}" width="50" height="8" rx="4" fill="{CHAR}"/>')
    p.append(f'<rect x="{gx-6}" y="{base-68}" width="3" height="30" fill="#7A4A2E"/><rect x="{gx+3}" y="{base-68}" width="3" height="30" fill="#7A4A2E"/>')
    p.append(f'<path d="M{gx-22} {base-38} h44 v16 a22 18 0 0 1 -44 0 z" fill="{WHITE}"/><path d="M{gx+22} {base-34} q12 0 10 10 q-2 8 -12 6" stroke="{WHITE}" stroke-width="4" fill="none"/><ellipse cx="{gx}" cy="{base-38}" rx="22" ry="4" fill="#C98A55"/>')
    p.append(f'<rect x="{x+10}" y="{base-10}" width="{w-20}" height="10" fill="{CHAR}" opacity="0.6"/>')
    p.append(f'<path d="M{x+30} {base-120} q-8 -14 0 -28 q8 -14 0 -26" stroke="{WHITE}" stroke-width="5" fill="none" stroke-linecap="round" opacity="0.8"/>')
    p.append(friends_row(498, 1.5))
    p.append(f'<path d="M{48} 470 l-4 -10 M{121} 470 l0 -12" stroke="{CHAR}" stroke-width="2" stroke-linecap="round" opacity="0"/>')
    return ''.join(p)

# ---------- game 3: Gugu's pick ----------
def g_gugu():
    p = [room(470)]
    p.append(window(40, 90, 150, 200) + window(210, 90, 150, 200))
    p.append(friends_row(420, 1.9, xs=(46, 120, 195, 270, 344)))
    p.append(f'<path d="M40 150 C120 60 300 80 280 190 C268 250 200 260 190 330" stroke="{CHAR}" stroke-width="2" stroke-dasharray="4 7" fill="none" stroke-linecap="round"/>')
    gx, gy = 200, 344
    p.append(f'<g transform="translate({gx} {gy}) scale(2.2)"><path d="M-6 -6 C-22 -22 -30 -14 -26 -4 C-20 -10 -12 -8 -6 -4 Z" fill="#8C96A0"/><path d="M6 -6 C22 -24 32 -16 28 -6 C22 -12 12 -8 6 -4 Z" fill="#A9B2BA"/>'
             f'<ellipse cx="0" cy="0" rx="9" ry="7" fill="#A9B2BA"/><circle cx="6" cy="-6" r="4.4" fill="#A9B2BA"/><path d="M10 -6 l4 1 -4 1 z" fill="{ORANGE}"/><circle cx="7" cy="-7" r="0.8" fill="{CHAR}"/><path d="M-2 6 v3 M2 6 v3" stroke="{ORANGE}" stroke-width="1.2"/></g>')
    p.append(f'<ellipse cx="195" cy="392" rx="20" ry="4" fill="#000000" opacity="0.1"/>')
    p.append(''.join(f'<path d="M{x} {y} q4 -6 8 0" stroke="#A9B2BA" stroke-width="2.4" fill="none" stroke-linecap="round"/>' for x, y in ((120, 250), (150, 214), (260, 150))))
    return ''.join(p)

# ---------- game 4: Kongi's pick ----------
def g_kongi():
    p = [f'<rect width="390" height="600" fill="{FLOOR}"/><rect width="390" height="120" fill="{WALL}"/><rect y="70" width="390" height="50" fill="{WAIN}"/><rect y="66" width="390" height="6" fill="{CREAM}"/><rect y="120" width="390" height="5" fill="#D6C1A0"/>']
    p.append(''.join(f'<rect x="0" y="{y}" width="390" height="1.2" fill="#D6C1A0"/>' for y in range(160, 600, 40)))
    p.append(f'<ellipse cx="195" cy="300" rx="170" ry="120" fill="{CREAM}" opacity="0.6"/>')
    pts = [(62, 400), (110, 250), (195, 200), (280, 250), (328, 400)]
    for i, (x, y) in enumerate(pts):
        p.append(bowl(x, y, SEG[i], s=1.5))
    p.append(f'<path d="M195 520 C180 470 260 420 262 300" stroke="{CAT}" stroke-width="2" stroke-dasharray="2 8" fill="none" stroke-linecap="round" opacity="0.8"/>')
    p.append(''.join(f'<ellipse cx="{x}" cy="{y}" rx="3.4" ry="2.4" fill="{CAT}" opacity="0.55"/>' for x, y in ((190, 500), (200, 480), (214, 452), (228, 430), (246, 400), (254, 372))))
    p.append(cat_walk(250, 344, 2.4))
    p.append(f'<path d="M290 296 q6 -8 12 0 M296 288 q4 -6 8 0" stroke="{CHAR}" stroke-width="1.6" fill="none" stroke-linecap="round"/>')
    return ''.join(p)

# ---------- game 5: hand shake (draw sticks) ----------
def g_shake():
    p = [room(470)]
    p.append(window(120, 80, 150, 170))
    p.append(f'<rect x="10" y="400" width="370" height="9" rx="2" fill="{KRAFT}"/>')
    cx, base = 195, 380
    p.append(f'<g transform="rotate(-10 {cx} {base})">' + draw_cup(cx, base, 3.0) + '</g>')
    p.append(f'<path d="M{cx+70} {base-20} C{cx+110} {base-10} {cx+150} {base+10} {cx+200} {base+10}" stroke="{CAT}" stroke-width="30" stroke-linecap="round" fill="none"/>'
             f'<ellipse cx="{cx+52}" cy="{base-24}" rx="24" ry="20" fill="{CAT}"/><circle cx="{cx+40}" cy="{base-30}" r="5" fill="{PEACH}"/><circle cx="{cx+44}" cy="{base-18}" r="5" fill="{PEACH}"/>')
    for dx, dy, rt in ((-90, -80, -20), (-100, -40, -10), (90, -130, 20), (100, -170, 30)):
        p.append(f'<path d="M{cx+dx} {base+dy} q8 -10 16 0" stroke="{CHAR}" stroke-width="3" fill="none" stroke-linecap="round" transform="rotate({rt} {cx+dx} {base+dy})"/>')
    p.append(f'<g transform="rotate(-24 {cx-30} {base-190})"><rect x="{cx-34}" y="{base-250}" width="8" height="120" fill="{KRAFT}"/><circle cx="{cx-30}" cy="{base-252}" r="10" fill="{CORAL}"/></g>')
    p.append(''.join(f'<path d="M{x} {y} l3 7 7 3 -7 3 -3 7 -3 -7 -7 -3 7 -3 z" fill="{MUST}"/>' for x, y in ((100, 120), (300, 160), (140, 200))))
    p.append(friends_row(498, 1.5))
    return ''.join(p)

if __name__ == '__main__':
    for n, f in (('G_cafe', cafe2), ('G1_roulette', g_roulette), ('G2_espresso', g_espresso), ('G3_gugu', g_gugu), ('G4_kongi', g_kongi), ('G5_shake', g_shake)):
        open(f'{OUT}/{n}.html', 'w').write(page(wrap(f())))
    print('ok')
