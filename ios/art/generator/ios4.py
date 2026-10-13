"""Round 4: game play scenes + place scenes."""
import math, random
import ios
from ios import *
from f_scenes3 import room, window, bowl, FLOOR
import kiri

def counter(y, h=80):
    return (f'<rect x="10" y="{y}" width="370" height="9" rx="2" fill="{KRAFT}"/><rect x="16" y="{y+9}" width="358" height="{h}" fill="{TEAL_D}"/>'
            f'<rect x="16" y="{y+9}" width="358" height="{h}" fill="url(#dotsW)" opacity="0.4"/>')

def floor_scene(wall=230):
    return (f'<rect width="390" height="{wall}" fill="#F6DCCB"/><rect y="{wall-50}" width="390" height="50" fill="{TEAL}"/><rect y="{wall-50}" width="390" height="50" fill="url(#stripeV)" opacity="0.35"/>'
            f'<rect y="{wall-54}" width="390" height="5" fill="{CREAM}"/><rect y="{wall}" width="390" height="{844-wall}" fill="url(#planksF)"/>')

# ---------- G1 coin under wing ----------
XS = [52, 123, 195, 267, 338]
def g_coin():
    p = [room(520), window(130, 110, 130, 170)]
    p.append(counter(520))
    for i, x in enumerate(XS):
        p.append(pg(x - 4, 520, 1.8, *MEMBERS[i], flip=(i >= 3)))
        p.append(f'<path d="M{x-24} 440 l-4 -6 M{x+22} 440 l4 -6" stroke="{CHAR}" stroke-width="1.6" stroke-linecap="round" opacity="0.6"/>')
    return ''.join(p)

# ---------- G2 Kiri's choice ----------
BOWLS = [(62, 600), (112, 470), (195, 420), (278, 470), (328, 600)]
def g_kiri():
    p = [floor_scene(230)]
    p.append(f'<ellipse cx="195" cy="520" rx="170" ry="140" fill="{CREAM}" opacity="0.55"/>')
    for i, (x, y) in enumerate(BOWLS):
        p.append(bowl(x, y, SEGC[i], s=1.9))
    rnd = random.Random(2)
    path = [(195, 780), (190, 740), (200, 700), (214, 664), (232, 628), (246, 596)]
    p.append(''.join(f'<ellipse cx="{x}" cy="{y}" rx="4" ry="3" fill="{CAT}" opacity="0.45"/>' for x, y in path))
    p.append(kiri.jump(226, 580, 3.0))
    p.append(f'<path d="M290 420 q6 -8 12 0 M300 404 q4 -6 8 0" stroke="{CHAR}" stroke-width="1.8" fill="none" stroke-linecap="round"/>')
    return ''.join(p)

# ---------- G3 espresso ----------
def gauge(cx, cy, r, val):
    p = [f'<circle cx="{cx}" cy="{cy}" r="{r+10}" fill="{CHAR}"/><circle cx="{cx}" cy="{cy}" r="{r}" fill="{CREAM}"/>']
    def ang(v): return math.radians(135 + v / 12 * 270)
    a0, a1 = ang(8.5), ang(9.5)
    rr = r - 10
    p.append(f'<path d="M{cx+rr*math.cos(a0):.1f} {cy+rr*math.sin(a0):.1f} A{rr} {rr} 0 0 1 {cx+rr*math.cos(a1):.1f} {cy+rr*math.sin(a1):.1f}" stroke="#7FB58A" stroke-width="12" fill="none"/>')
    a2, a3 = ang(10.5), ang(12)
    p.append(f'<path d="M{cx+rr*math.cos(a2):.1f} {cy+rr*math.sin(a2):.1f} A{rr} {rr} 0 0 1 {cx+rr*math.cos(a3):.1f} {cy+rr*math.sin(a3):.1f}" stroke="{CORAL}" stroke-width="12" fill="none"/>')
    for v in range(0, 13):
        a = ang(v); l = 12 if v % 3 == 0 else 6
        p.append(f'<path d="M{cx+(r-2)*math.cos(a):.1f} {cy+(r-2)*math.sin(a):.1f} L{cx+(r-2-l)*math.cos(a):.1f} {cy+(r-2-l)*math.sin(a):.1f}" stroke="{CHAR}" stroke-width="2" stroke-linecap="round"/>')
    a = ang(val)
    p.append(f'<path d="M{cx} {cy} L{cx+(r-16)*math.cos(a):.1f} {cy+(r-16)*math.sin(a):.1f}" stroke="{RED}" stroke-width="4" stroke-linecap="round"/><circle cx="{cx}" cy="{cy}" r="8" fill="{CHAR}"/>')
    return ''.join(p)

def g_espresso():
    p = [room(600)]
    p.append(f'<rect x="70" y="190" width="250" height="330" rx="18" fill="{MUST}"/><rect x="60" y="176" width="270" height="24" rx="10" fill="{CHAR}"/>')
    p.append(''.join(f'<rect x="{84+k*40}" y="150" width="30" height="26" rx="5" fill="{WHITE}"/>' for k in range(6)))
    p.append(gauge(195, 300, 76, 8.6))
    p.append(f'<rect x="140" y="410" width="110" height="20" rx="6" fill="{CHAR}"/><rect x="236" y="414" width="70" height="10" rx="5" fill="{CHAR}"/>')
    p.append(f'<path d="M188 430 v40 M202 430 v40" stroke="#6B3E22" stroke-width="5" stroke-linecap="round"/>')
    p.append(f'<path d="M166 470 h58 l-6 46 q-1 6 -8 6 h-30 q-7 0 -8 -6 z" fill="{WHITE}"/><path d="M222 482 q14 0 12 12 q-2 10 -14 10" stroke="{WHITE}" stroke-width="5" fill="none"/><ellipse cx="195" cy="472" rx="27" ry="5" fill="#B7814F"/>')
    p.append(f'<rect x="10" y="520" width="370" height="10" rx="3" fill="{KRAFT}"/>')
    p.append(''.join(f'<path d="M{x} {y} q-6 -10 0 -20" stroke="{CREAM}" stroke-width="3" fill="none" stroke-linecap="round" opacity="0.8"/>' for x, y in ((90, 160), (300, 170))))
    return ''.join(p)

# ---------- G4 cup knock ----------
CUPS = [40, 100, 160, 220, 280]
def paper_cup(x, base, sleeve, tilt=0, tapped=False):
    out = (f'<g transform="rotate({tilt} {x} {base})"><path d="M{x-17} {base-58} h34 l-5 58 h-24 z" fill="{WHITE}"/><rect x="{x-19}" y="{base-64}" width="38" height="8" rx="3" fill="{CREAM}"/>'
           f'<path d="M{x-15.5} {base-40} h31 l-1.4 16 h-28.2 z" fill="{sleeve}"/></g>')
    if tapped:
        out += f'<path d="M{x-24} {base-70} l-5 -6 M{x+24} {base-70} l5 -6 M{x} {base-76} v-7" stroke="{CHAR}" stroke-width="1.8" stroke-linecap="round" opacity="0.7"/>'
    return out

def g_knock():
    p = [room(520), window(24, 100, 92, 150), window(274, 100, 92, 150)]
    p.append(counter(520))
    for i, x in enumerate(CUPS):
        p.append(f'<g transform="translate({x} 520) scale(1.25) translate({-x} -520)">' + paper_cup(x, 520, [TEAL, CORAL, MUST, TEAL_L, PEACH][i], tilt=(-6 if i == 2 else 0), tapped=(i == 2)) + '</g>')
        if i in (0, 3):
            p.append(f'<circle cx="{x}" cy="418" r="9" fill="{CREAM}"/><path d="M{x-4} 418 l3 3 l5 -6" stroke="{TEAL_D}" stroke-width="2" fill="none" stroke-linecap="round"/>')
    p.append(kiri.loaf(348, 520, 2.0, flip=True))
    return ''.join(p)

# ---------- G5 boxes ----------
def closed_box(x, base, s=1.0, wobble=False, opened=False):
    t = f'rotate({-6 if wobble else 0} {x} {base})'
    body = f'<rect x="{x-24*s}" y="{base-34*s}" width="{48*s}" height="{34*s}" fill="{KRAFT}"/><rect x="{x-4*s}" y="{base-34*s}" width="{8*s}" height="{34*s}" fill="{CREAM}" opacity="0.45"/>'
    if opened:
        lid = (f'<path d="M{x-24*s} {base-34*s} l-10 {-9*s} h{14*s} l{8*s} {9*s} z M{x+24*s} {base-34*s} l10 {-9*s} h{-14*s} l{-8*s} {9*s} z" fill="{KRAFT_D}"/>'
               f'<path d="M{x-22*s} {base-34*s} h{44*s} l-3 6 h{-38*s} z" fill="#7A5A3A"/>')
    else:
        lid = f'<rect x="{x-26*s}" y="{base-40*s}" width="{52*s}" height="{8*s}" rx="2" fill="{KRAFT_D}"/>'
    out = f'<g transform="{t}"><ellipse cx="{x}" cy="{base+2}" rx="{28*s}" ry="{5*s}" fill="#000" opacity="0.08"/>{body}{lid}</g>'
    if wobble:
        out += f'<path d="M{x-36*s} {base-30*s} q-6 8 0 16 M{x+36*s} {base-30*s} q6 8 0 16" stroke="{CHAR}" stroke-width="2" fill="none" stroke-linecap="round" opacity="0.6"/>'
    return out

BOXES = [(90, 470), (195, 470), (300, 470), (90, 640), (195, 640), (300, 640)]
def g_box():
    p = [floor_scene(230)]
    for i, (x, y) in enumerate(BOXES):
        p.append(closed_box(x, y, 2.0, wobble=(i == 5), opened=(i in (1, 3))))
    return ''.join(p)

# ---------- P records hall ----------
def records():
    p = [f'<rect width="390" height="844" fill="#E3E6E2"/><rect width="390" height="844" fill="url(#wallpaper)" opacity="0.35"/>']
    for sx in (24, 270):
        p.append(f'<rect x="{sx}" y="100" width="96" height="200" fill="{BROWN}"/>')
        for r in range(3):
            y = 110 + r * 64
            p.append(f'<rect x="{sx}" y="{y+52}" width="96" height="5" fill="{shade(BROWN,0.8)}"/>')
            p.append(''.join(f'<rect x="{sx+6+k*22}" y="{y+16}" width="18" height="36" rx="2" fill="{[TEAL,CREAM,MUST,CORAL][(k+r)%4]}"/>' for k in range(4)))
    p.append(f'<circle cx="195" cy="150" r="46" fill="{CREAM}"/><circle cx="195" cy="150" r="38" fill="{WHITE}"/><path d="M195 150 v-24 M195 150 l16 10" stroke="{CHAR}" stroke-width="4" stroke-linecap="round"/>')
    p.append(f'<rect x="150" y="214" width="90" height="70" fill="{CREAM}"/><rect x="158" y="222" width="74" height="54" fill="{LBLUE}"/>')
    return ''.join(p)

# ---------- P nearby map ----------
def nearby():
    p = [f'<rect width="390" height="844" fill="{MAP}"/>']
    p.append(f'<path d="M0 300 H390 M150 0 V520 M0 140 H390 M290 140 V520" stroke="{WHITE}" stroke-width="18"/>')
    p.append(f'<rect x="168" y="160" width="110" height="128" rx="8" fill="#CFDCC3"/>' + ios.a_tree(200, 230, 12) + ios.a_tree(244, 260, 10) + a_pine(222, 214, 14, 34))
    p.append(f'<ellipse cx="60" cy="430" rx="44" ry="24" fill="{LBLUE}"/>')
    for (hx, hy, c) in ((30, 120, MUST), (80, 120, CORAL), (310, 120, TEAL_L), (30, 280, PEACH), (310, 280, MUST), (190, 470, CORAL), (320, 470, TEAL_L), (100, 260, TEAL_L)):
        p.append(house(hx, hy, 32, 30, c, CHAR, roof_h=12, cols=1, rows=1))
    for (x, y) in ((96, 210), (230, 112), (330, 210), (210, 360), (60, 360), (340, 400)):
        p.append(f'<path d="M{x} {y+16} l-9 -12 a12 12 0 1 1 18 0 z" fill="{TEAL_D}"/><circle cx="{x}" cy="{y}" r="8" fill="{CREAM}"/><path d="M{x-4} {y-3} h8 l-1 6 h-6 z" fill="{BROWN}"/>')
    p.append(f'<circle cx="150" cy="300" r="26" fill="{TEAL}" opacity="0.2"/><circle cx="150" cy="300" r="9" fill="{WHITE}"/><circle cx="150" cy="300" r="6" fill="#3E7CB1"/>')
    return ''.join(p)

# ---------- P post office ----------
def post():
    p = [f'<rect width="390" height="844" fill="{CREAM}"/>']
    for r in range(3):
        for c in range(6):
            x = 30 + c * 56; y = 100 + r * 52
            p.append(f'<rect x="{x}" y="{y}" width="48" height="44" rx="4" fill="{TEAL_D}"/><rect x="{x+6}" y="{y+8}" width="36" height="30" rx="2" fill="{TEAL}"/>')
            if (r * 6 + c) % 3 == 0:
                p.append(f'<rect x="{x+10}" y="{y+14}" width="28" height="18" rx="2" fill="{WHITE}"/><path d="M{x+10} {y+14} l14 10 l14 -10" stroke="{GREY}" stroke-width="1.2" fill="none"/>')
    p.append(f'<rect x="0" y="262" width="390" height="10" fill="{RED}"/>')
    p.append(pg(320, 262, 1.1, *MEMBERS[4], flip=True))
    return ''.join(p)

if __name__ == '__main__':
    for n, f in (('g_coin', g_coin), ('g_kiri', g_kiri), ('g_espresso', g_espresso), ('g_knock', g_knock), ('g_box', g_box), ('p_records', records), ('p_nearby', nearby), ('p_post', post)):
        open(f'{OUT}/{n}.html', 'w').write(page(wrap(f())))
    print('ok')
