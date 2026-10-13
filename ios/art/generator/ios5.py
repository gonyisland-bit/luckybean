"""Round 5: front-view pigeon poses + distinct game spaces with foreground."""
import math, random
import ios
from ios import *
from f_scenes3 import window, bowl
import kiri
from ios4 import paper_cup, gauge

def pf(x, y, s=1.0, body='#A9B2BA', acc=None, pose='stand'):
    """Pigeon guest, FRONT view. feet at (x,y). pose: stand | surprised | wings | wallet | rest"""
    dk = shade(body, 0.82); lt = shade(body, 1.08)
    p = [f'<g transform="translate({x} {y}) scale({s})">']
    rx = 16 if pose == 'surprised' else 14
    if pose != 'rest':
        p.append(f'<path d="M-4 -4 v4 M4 -4 v4 M-6 0 h4 M2 0 h4" stroke="#E79A86" stroke-width="2" stroke-linecap="round"/>')
        cy = -17
    else:
        cy = -11
    if pose == 'wings':
        p.append(f'<path d="M-12 -22 C-30 -36 -32 -20 -26 -12 C-22 -10 -16 -12 -12 -14 Z" fill="{dk}"/><path d="M12 -22 C30 -36 32 -20 26 -12 C22 -10 16 -12 12 -14 Z" fill="{dk}"/>')
        p.append(f'<path d="M-26 -26 l-6 -2 M-28 -20 l-6 0 M26 -26 l6 -2 M28 -20 l6 0" stroke="{dk}" stroke-width="2" stroke-linecap="round"/>')
    if pose == 'rest':
        p.append(f'<ellipse cx="0" cy="{cy}" rx="18" ry="11" fill="{body}"/><ellipse cx="0" cy="{cy+3}" rx="11" ry="7" fill="{lt}"/>')
    else:
        p.append(f'<ellipse cx="0" cy="{cy}" rx="{rx}" ry="14" fill="{body}"/><ellipse cx="0" cy="{cy+4}" rx="{rx-5}" ry="9.5" fill="{lt}"/>')
    if pose in ('stand', 'surprised', 'rest'):
        p.append(f'<ellipse cx="{-rx+2}" cy="{cy}" rx="5" ry="{8 if pose=="rest" else 10}" fill="{dk}" transform="rotate(10 {-rx+2} {cy})"/><ellipse cx="{rx-2}" cy="{cy}" rx="5" ry="{8 if pose=="rest" else 10}" fill="{dk}" transform="rotate(-10 {rx-2} {cy})"/>')
    if pose == 'surprised':
        p.append(f'<path d="M-18 -26 l-4 -3 M18 -26 l4 -3 M-16 -8 l-4 1 M16 -8 l4 1" stroke="{dk}" stroke-width="1.6" stroke-linecap="round"/>')
    hy = cy - 18 if pose != 'rest' else cy - 14
    p.append(f'<ellipse cx="0" cy="{hy+8}" rx="9.5" ry="4.2" fill="#7FA79A" opacity="0.85"/><ellipse cx="0" cy="{hy+6.5}" rx="7" ry="2.6" fill="#B58AA8" opacity="0.45"/>')
    p.append(f'<circle cx="0" cy="{hy}" r="9" fill="{body}"/>')
    if pose == 'wings':
        p.append(f'<path d="M-6 {hy-1} q2 -2.4 4 0 M2 {hy-1} q2 -2.4 4 0" stroke="{CHAR}" stroke-width="1.3" fill="none" stroke-linecap="round"/>')
    elif pose == 'rest':
        p.append(f'<path d="M-6 {hy} q2 1.6 4 0 M2 {hy} q2 1.6 4 0" stroke="{CHAR}" stroke-width="1.2" fill="none" stroke-linecap="round"/>')
    else:
        er = 3.2 if pose == 'surprised' else 2.5; pr = 1.0 if pose == 'surprised' else 1.3
        p.append(f'<circle cx="-4" cy="{hy-1}" r="{er}" fill="{WHITE}"/><circle cx="4" cy="{hy-1}" r="{er}" fill="{WHITE}"/><circle cx="-4" cy="{hy-1}" r="{pr}" fill="{CHAR}"/><circle cx="4" cy="{hy-1}" r="{pr}" fill="{CHAR}"/>')
    p.append(f'<ellipse cx="0" cy="{hy+1.4}" rx="1.8" ry="1" fill="{WHITE}"/><path d="M-1.8 {hy+2.4} L1.8 {hy+2.4} L0 {hy+6} Z" fill="{CHAR}"/>')
    p.append(f'<ellipse cx="-6.4" cy="{hy+3}" rx="1.8" ry="1.1" fill="{CORAL}" opacity="0.5"/><ellipse cx="6.4" cy="{hy+3}" rx="1.8" ry="1.1" fill="{CORAL}" opacity="0.5"/>')
    if pose == 'wallet':
        p.append(f'<path d="M-13 -22 C-16 -12 -10 -6 -4 -8 M13 -22 C16 -12 10 -6 4 -8" stroke="{dk}" stroke-width="6" fill="none" stroke-linecap="round"/>')
        p.append(f'<rect x="-9" y="-16" width="18" height="12" rx="2.4" fill="{TEAL_D}"/><rect x="1" y="-12.6" width="8" height="5.2" rx="1.6" fill="{TEAL}"/><circle cx="5" cy="-10" r="1.2" fill="{MUST}"/>')
        p.append(f'<path d="M10 {hy-8} q2.4 3.6 0 5 q-2.4 -1.4 0 -5 z" fill="{LBLUE}"/>')
    if pose == 'surprised':
        p.append(f'<path d="M16 {hy-14} v7 M16 {hy-4} v0.5" stroke="{RED}" stroke-width="2.6" stroke-linecap="round"/>')
    # accessories
    if acc == 'beret':
        p.append(f'<ellipse cx="-1" cy="{hy-7.5}" rx="10" ry="4" fill="{CORAL}" transform="rotate(-10 -1 {hy-7.5})"/><rect x="-2" y="{hy-13.5}" width="2.4" height="3" rx="1" fill="{CORAL}"/>')
    elif acc == 'ribbon':
        p.append(f'<path d="M5 {hy-8} l-5 -4 v8 z M5 {hy-8} l5 -4 v8 z" fill="{RED}"/><circle cx="5" cy="{hy-8}" r="1.8" fill="{RED}"/>')
    elif acc == 'scarf':
        p.append(f'<path d="M-9 {hy+6} Q0 {hy+11} 9 {hy+6} L9 {hy+10} Q0 {hy+15} -9 {hy+10} Z" fill="{MUST}"/><path d="M4 {hy+11} l3 10 l-4 -1 z" fill="{MUST}"/>')
    elif acc == 'glasses' and pose not in ('wings', 'rest'):
        p.append(f'<circle cx="-4" cy="{hy-1}" r="3.8" fill="none" stroke="{CHAR}" stroke-width="1.2"/><circle cx="4" cy="{hy-1}" r="3.8" fill="none" stroke="{CHAR}" stroke-width="1.2"/><path d="M-0.2 {hy-1} h0.4" stroke="{CHAR}" stroke-width="1.2"/>')
    elif acc == 'cap':
        p.append(f'<path d="M-8.4 {hy-4} Q0 {hy-16} 8.4 {hy-4} Z" fill="{TEAL_D}"/><ellipse cx="0" cy="{hy-4}" rx="10" ry="2.2" fill="{TEAL_D}"/><circle cx="0" cy="{hy-11.6}" r="1.4" fill="{MUST}"/>')
    p.append('</g>')
    return ''.join(p)

PATS = '''<pattern id="tiles" width="24" height="14" patternUnits="userSpaceOnUse"><rect width="24" height="14" fill="#F4EFE6"/><path d="M0 13.5 H24 M12 0 V7 M0 7 H24 M0 7 V14 M24 7 V14" stroke="#DCD3C4" stroke-width="1"/></pattern>
<pattern id="rugstripe" width="20" height="20" patternUnits="userSpaceOnUse"><rect width="20" height="20" fill="#F2A48C"/><rect width="20" height="6" fill="#F6CBB8"/></pattern>
<pattern id="wall2" width="30" height="30" patternUnits="userSpaceOnUse"><rect width="30" height="30" fill="#DDEBE6"/><circle cx="15" cy="15" r="2" fill="#C5DDD6"/></pattern>'''
f_kit_defs_orig = ios.DEFS if hasattr(ios, 'DEFS') else None
import f_kit
f_kit.DEFS = f_kit.DEFS + PATS

def planks(y0, col='#E3D3BA'):
    return f'<rect y="{y0}" width="390" height="{844-y0}" fill="{col}"/>' + ''.join(f'<rect x="0" y="{y}" width="390" height="1.4" fill="{shade(col,0.92)}"/>' for y in range(y0 + 22, 844, 22))

# ---------- coin: window bar table ----------
def coin5():
    p = [f'<rect width="390" height="844" fill="url(#wall2)"/>']
    p.append(f'<rect x="20" y="110" width="350" height="290" rx="6" fill="{CREAM}"/><rect x="30" y="120" width="330" height="270" fill="{LBLUE}"/>')
    p.append(f'<rect x="30" y="330" width="330" height="60" fill="{MAP}"/>' + house(40, 330, 44, 70, MUST, CHAR, roof_h=16, cols=2, rows=2) + house(96, 330, 50, 46, CORAL, TEAL_D, roof_h=16, cols=2, rows=1) + house(160, 330, 40, 90, TEAL, CHAR, roof_h=14, cols=2, rows=3) + a_tree(222, 330, 14) + house(250, 330, 52, 56, PEACH, ORANGE, roof_h=18, cols=2, rows=1) + house(312, 330, 40, 76, GREY_L, CHAR, roof_h=16, cols=2, rows=2))
    p.append(f'<rect x="192" y="120" width="6" height="270" fill="{CREAM}"/><rect x="30" y="240" width="330" height="5" fill="{CREAM}"/>')
    p.append(planks(540))
    p.append(f'<rect x="0" y="512" width="390" height="16" fill="{KRAFT}"/><rect x="0" y="528" width="390" height="8" fill="{KRAFT_D}"/>')
    xs = [52, 123, 195, 267, 338]
    for i, x in enumerate(xs):
        p.append(pf(x, 512, 2.0, *MEMBERS[i]))
    p.append(f'<ellipse cx="70" cy="760" rx="62" ry="18" fill="{TEAL_D}"/><rect x="66" y="770" width="8" height="80" fill="{CHAR}"/><ellipse cx="320" cy="780" rx="62" ry="18" fill="{CORAL}"/><rect x="316" y="790" width="8" height="60" fill="{CHAR}"/>')
    p.append(f'<path d="M190 844 l8 -64 h40 l8 64 z" fill="{ORANGE}"/><path d="M218 782 C200 740 204 700 218 690 C232 700 236 740 218 782 Z" fill="{TEAL_D}"/><path d="M218 782 C186 760 182 730 194 722 C206 736 212 756 218 782 Z M218 782 C250 760 254 730 242 722 C230 736 224 756 218 782 Z" fill="{TEAL}"/>')
    return ''.join(p)

# ---------- espresso: behind the counter ----------
def espresso5():
    p = [f'<rect width="390" height="600" fill="url(#tiles)"/>']
    for sy in (110,):
        p.append(f'<rect x="0" y="{sy+46}" width="390" height="8" fill="{BROWN}"/>')
        p.append(''.join(f'<rect x="{x}" y="{sy+12}" width="22" height="34" rx="5" fill="{c}"/><rect x="{x+2}" y="{sy+6}" width="18" height="8" rx="2" fill="{CHAR}"/>' for x, c in ((20, '#D9A35A'), (50, '#8A5A3C'), (330, '#D9A35A'), (358, CREAM))))
    p.append(f'<rect x="70" y="200" width="250" height="330" rx="18" fill="{MUST}"/><rect x="60" y="186" width="270" height="24" rx="10" fill="{CHAR}"/>')
    p.append(''.join(f'<rect x="{84+k*40}" y="160" width="30" height="26" rx="5" fill="{WHITE}"/>' for k in range(6)))
    p.append(gauge(195, 310, 76, 8.6))
    p.append(f'<rect x="140" y="420" width="110" height="20" rx="6" fill="{CHAR}"/><rect x="236" y="424" width="70" height="10" rx="5" fill="{CHAR}"/>')
    p.append(f'<path d="M188 440 v40 M202 440 v40" stroke="#6B3E22" stroke-width="5" stroke-linecap="round"/>')
    p.append(f'<path d="M166 480 h58 l-6 46 q-1 6 -8 6 h-30 q-7 0 -8 -6 z" fill="{WHITE}"/><path d="M222 492 q14 0 12 12 q-2 10 -14 10" stroke="{WHITE}" stroke-width="5" fill="none"/><ellipse cx="195" cy="482" rx="27" ry="5" fill="#B7814F"/>')
    p.append(f'<rect x="0" y="530" width="390" height="14" fill="{KRAFT}"/><rect x="0" y="544" width="390" height="300" fill="{TEAL_D}"/>')
    for x in (12, 140, 268):
        p.append(f'<rect x="{x}" y="566" width="110" height="260" rx="8" fill="{TEAL}"/><rect x="{x+48}" y="580" width="14" height="4" rx="2" fill="{CREAM}"/>')
    p.append(f'<path d="M24 844 q-6 -60 30 -70 q40 -8 52 24 q8 30 -4 46 z" fill="#C9A06A"/><path d="M40 780 q14 -6 30 0" stroke="{KRAFT_D}" stroke-width="2" fill="none"/>' + ''.join(f'<ellipse cx="{x}" cy="{y}" rx="4" ry="2.6" fill="#6B3E22" transform="rotate(30 {x} {y})"/>' for x, y in ((120, 830), (132, 822), (110, 838))))
    return ''.join(p)

# ---------- knock: terrace ----------
def knock5():
    p = [f'<rect width="390" height="844" fill="#CFE3E6"/>']
    p.append(''.join(f'<rect x="{x}" y="{420-h}" width="{w}" height="{h}" fill="#E4ECEA"/>' for x, w, h in ((0, 60, 150), (66, 50, 110), (124, 70, 180), (200, 46, 120), (252, 64, 160), (322, 68, 130))))
    p.append(cloud_s(80, 200) + cloud_s(300, 160))
    p.append(f'<rect x="0" y="0" width="390" height="86" fill="url(#tentStripe)"/>' + ''.join(f'<circle cx="{10+k*20}" cy="86" r="10" fill="{CORAL if k%2==0 else CREAM}"/>' for k in range(20)))
    p.append(f'<rect y="420" width="390" height="424" fill="#E6DED0"/>' + ''.join(f'<path d="M{x} 420 L{x*1.6-117} 844" stroke="#D6CCBA" stroke-width="1.2"/>' for x in range(0, 400, 40)))
    p.append(f'<ellipse cx="195" cy="530" rx="190" ry="44" fill="{KRAFT_D}"/><ellipse cx="195" cy="522" rx="190" ry="44" fill="{KRAFT}"/>')
    for i, x in enumerate([60, 122, 184, 246, 308][:4] + []):
        pass
    cups = [70, 140, 210, 280]
    for i, x in enumerate(cups):
        g = f'<g transform="translate({x} 530) scale(1.3) translate({-x} -530)">' + paper_cup(x, 530, [TEAL, CORAL, MUST, TEAL_L][i], tilt=(-7 if i == 1 else 0), tapped=(i == 1)) + '</g>'
        p.append(g)
        if i in (0, 3):
            p.append(f'<circle cx="{x}" cy="430" r="9" fill="{CREAM}"/><path d="M{x-4} 430 l3 3 l5 -6" stroke="{TEAL_D}" stroke-width="2" fill="none" stroke-linecap="round"/>')
    p.append(kiri.loaf(345, 526, 1.9, flip=True))
    # foreground chairs + plant
    for cx in (60, 330):
        p.append(f'<path d="M{cx-50} 844 V700 Q{cx} 650 {cx+50} 700 V844" stroke="{CHAR}" stroke-width="7" fill="none"/><path d="M{cx-30} 844 V716 M{cx} 844 V700 M{cx+30} 844 V716" stroke="{CHAR}" stroke-width="5"/>')
    return ''.join(p)

def cloud_s(x, y):
    return f'<g transform="translate({x} {y})"><ellipse cx="0" cy="0" rx="30" ry="10" fill="{WHITE}"/><ellipse cx="-10" cy="-7" rx="14" ry="10" fill="{WHITE}"/><ellipse cx="10" cy="-8" rx="12" ry="9" fill="{WHITE}"/></g>'

# ---------- roulette: attic ----------
from ios3 import wheel_plain
def roulette5():
    p = [f'<rect width="390" height="844" fill="#F3E6D8"/><rect width="390" height="844" fill="url(#wallpaper)" opacity="0.25"/>']
    p.append(f'<path d="M0 0 L120 0 L0 170 Z M390 0 L270 0 L390 170 Z" fill="{BROWN}"/><path d="M0 170 L120 0 M390 170 L270 0" stroke="{shade(BROWN,0.8)}" stroke-width="10"/>')
    p.append(f'<circle cx="195" cy="120" r="0" fill="none"/>')
    p.append(planks(600, '#D9C4A4'))
    p.append(f'<ellipse cx="195" cy="660" rx="170" ry="40" fill="url(#rugstripe)"/>')
    p.append(f'<rect x="188" y="470" width="14" height="170" fill="{CHAR}"/><rect x="146" y="632" width="98" height="14" rx="5" fill="{CHAR}"/>')
    w, _ = wheel_plain(195, 340, 140, rot=-14)
    p.append(w)
    p.append(f'<path d="M181 174 h28 l-14 26 z" fill="{RED}"/><circle cx="195" cy="178" r="5" fill="{CREAM}"/>')
    p.append(''.join(f'<rect x="{18+d}" y="{820-k*22}" width="{80-d*2}" height="20" rx="3" fill="{c}"/>' for k, (d, c) in enumerate(((0, TEAL_D), (6, MUST), (2, CORAL), (10, CREAM)))))
    p.append(f'<rect x="338" y="560" width="4" height="284" fill="{CHAR}"/><path d="M314 566 Q340 520 366 566 Z" fill="{MUST}"/><ellipse cx="340" cy="600" rx="44" ry="40" fill="url(#glow)" opacity="0.6"/>')
    return ''.join(p)

# ---------- reveal with front pigeon ----------
def reveal5():
    p = [f'<rect width="390" height="844" fill="#F3E2D2"/>']
    p.append(f'<path d="M195 140 L60 660 H330 Z" fill="#FFF3D6" opacity="0.85"/><ellipse cx="195" cy="660" rx="140" ry="26" fill="#EAD2B6"/>')
    rnd = random.Random(3)
    for _ in range(24):
        x = rnd.uniform(20, 370); y = rnd.uniform(160, 520); c = rnd.choice([MUST, CORAL, TEAL, LBLUE]); a = rnd.uniform(0, 180)
        p.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="7" height="4" fill="{c}" transform="rotate({a:.0f} {x:.0f} {y:.0f})"/>')
    p.append(pf(195, 660, 5.2, *MEMBERS[2], pose='wallet'))
    return ''.join(p)

POSES = [('stand', 'stand'), ('surprised', 'surprised'), ('wings', 'wings'), ('wallet', 'wallet'), ('rest', 'rest')]

if __name__ == '__main__':
    from ios import svg_raw
    import f_kit as fk
    for n, f in (('coin5', coin5), ('espresso5', espresso5), ('knock5', knock5), ('roulette5', roulette5), ('reveal5', reveal5)):
        open(f'{OUT}/{n}.html', 'w').write(page(wrap(f())))
    for i, (n, pose) in enumerate(POSES):
        body, acc = MEMBERS[i]
        open(f'{OUT}/pp_{n}.html', 'w').write(f'<!doctype html><html><head><meta charset="utf-8"><style>html,body{{margin:0;background:transparent}}</style></head><body style="width:200px;height:170px">{svg_raw("<rect width=\"200\" height=\"170\" fill=\"none\"/>" + pf(100, 158, 2.6, body, acc, pose), 200, 170)}</body></html>')
    for i in range(5):
        body, acc = MEMBERS[i]
        open(f'{OUT}/pa_{i}.html', 'w').write(f'<!doctype html><html><head><meta charset="utf-8"><style>html,body{{margin:0;background:transparent}}</style></head><body style="width:120px;height:120px">{svg_raw("<rect width=\"120\" height=\"120\" fill=\"none\"/>" + pf(60, 150, 2.9, body, acc), 120, 120)}</body></html>')
    print('ok')
