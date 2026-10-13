"""Round 3 scenes: A-street night, cafe w/ loaf Kiri, cleaner roulette, two-step result."""
import math, random, json
import ios
from ios import *
from ios2 import street, BASE, S, cloud
import kiri

def street_night():
    p = [street()]
    p.append(f'<rect width="1170" height="844" fill="{NIGHT}" opacity="0.64"/>')
    cx0 = 585 - 87 * S
    gy0, gy1 = BASE - 60 * S, BASE - 6 * S
    pane_w = (174 - 24) / 3
    for i in (0, 2):
        px = cx0 + (8 + i * (pane_w + 4)) * S
        p.append(f'<rect x="{px:.1f}" y="{gy0:.1f}" width="{pane_w*S:.1f}" height="{(gy1-gy0)*0.5:.1f}" fill="#FBD98A" opacity="0.9"/>')
    for i in range(4):
        wx = cx0 + (14 + i * (174 - 50) / 3) * S
        p.append(f'<path d="M{wx+3*S:.1f} {BASE-112*S:.1f} V{BASE-137*S:.1f} A{8*S} {8*S} 0 0 1 {wx+19*S:.1f} {BASE-137*S:.1f} V{BASE-112*S:.1f} Z" fill="#FBD98A" opacity="0.9"/>')
    for (gx, gy, r) in ((585, BASE - 50, 110), (585, BASE - 230, 80), (300, BASE - 66, 40), (895, BASE - 66, 40), (390, BASE - 200, 60), (810, BASE - 120, 50), (968, BASE - 50, 50), (1100, BASE - 50, 50), (150, BASE - 50, 50)):
        p.append(f'<ellipse cx="{gx}" cy="{gy}" rx="{r}" ry="{r*0.8:.0f}" fill="url(#glow)"/>')
    p.append(''.join(f'<rect x="{x}" y="{y}" width="10" height="12" fill="#FBD98A" opacity="0.85"/>' for x, y in ((352, 380), (382, 380), (352, 440), (382, 470), (770, 480), (812, 480), (854, 480), (930, 545), (980, 545), (1068, 545), (1116, 545))))
    p.append(f'<circle cx="980" cy="120" r="26" fill="{CREAM}"/><circle cx="992" cy="112" r="24" fill="{NIGHT}" opacity="0.9"/>')
    rnd = random.Random(7)
    p.append(''.join(f'<circle cx="{rnd.uniform(0,1170):.0f}" cy="{rnd.uniform(20,300):.0f}" r="{rnd.choice([1,1.2,1.6])}" fill="{CREAM}"/>' for _ in range(40)))
    return ''.join(p)

def cafe3():
    p = [room(430)]
    p.append(window(130, 98, 130, 176))
    p.append(f'<rect x="124" y="272" width="142" height="8" rx="3" fill="{CREAM}"/>')
    p.append(pg(172, 272, 0.75, *MEMBERS[0]) + pg(232, 272, 0.75, *MEMBERS[1], flip=True))
    for lx in (70, 320):
        p.append(f'<rect x="{lx-1}" y="0" width="2" height="54" fill="{CHAR}"/><path d="M{lx-15} 70 Q{lx} 44 {lx+15} 70 Z" fill="{TEAL_D}"/><ellipse cx="{lx}" cy="90" rx="50" ry="34" fill="url(#glow)" opacity="0.45"/>')
    p.append(f'<rect x="298" y="122" width="66" height="84" rx="4" fill="{CHAR}"/>' + ''.join(f'<rect x="306" y="{136+k*13}" width="{40 if k%2 else 50}" height="2.4" fill="{CREAM}" opacity="0.85"/>' for k in range(5)))
    p.append(f'<rect x="34" y="150" width="50" height="60" fill="{CREAM}"/><rect x="40" y="156" width="38" height="48" fill="{TEAL_XL}"/>' + a_tree(59, 200, 12, TEAL_D))
    p.append(f'<rect x="10" y="352" width="370" height="9" rx="2" fill="{KRAFT}"/><rect x="16" y="361" width="358" height="69" fill="{TEAL_D}"/><rect x="16" y="361" width="358" height="69" fill="url(#dotsW)" opacity="0.4"/>')
    p.append(esp_machine(40, 352, 72))
    p.append(f'<path d="M290 352 l4 -26 h28 l4 26 z" fill="{CREAM}"/>' + ''.join(f'<ellipse cx="{300+k*9}" cy="324" rx="5" ry="3" fill="{c}"/>' for k, c in enumerate((KRAFT, '#D9A35A', KRAFT))))
    p.append(kiri.loaf(205, 352, 2.3))
    return ''.join(p)

WEIGHTS = [1, 1, 1, 1, 1, 0.2]
def wheel_plain(cx, cy, r, rot=0):
    tot = sum(WEIGHTS); p = [f'<circle cx="{cx}" cy="{cy}" r="{r+14}" fill="{KRAFT}"/><circle cx="{cx}" cy="{cy}" r="{r+6}" fill="{CREAM}"/>']
    a = -90 + rot; labels = []
    for i, wi in enumerate(WEIGHTS):
        sw = 360 * wi / tot; a0, a1 = math.radians(a), math.radians(a + sw)
        col = SEGC[i] if i < 5 else CHAR
        d = f'M{cx} {cy} L{cx+r*math.cos(a0):.1f} {cy+r*math.sin(a0):.1f} A{r} {r} 0 {1 if sw>180 else 0} 1 {cx+r*math.cos(a1):.1f} {cy+r*math.sin(a1):.1f} Z'
        p.append(f'<path d="{d}" fill="{col}"/>')
        if i % 2 == 0 and i < 5:
            p.append(f'<path d="{d}" fill="url(#dotsW)" opacity="0.5"/>')
        am = a + sw / 2
        rr = 0.62 if i < 5 else 0.8
        labels.append((round(cx + r * rr * math.cos(math.radians(am)), 1), round(cy + r * rr * math.sin(math.radians(am)), 1), round(am + 90, 1)))
        if i == 5:
            hx, hy = labels[-1][:2]
            p.append(f'<path d="M{hx} {hy-7} l2 5 5 2 -5 2 -2 5 -2 -5 -5 -2 5 -2 z" fill="{MUST}"/>')
        a += sw
    p.append(''.join(f'<circle cx="{cx+(r+10)*math.cos(math.radians(k)):.1f}" cy="{cy+(r+10)*math.sin(math.radians(k)):.1f}" r="2.4" fill="{MUST}"/>' for k in range(0, 360, 15)))
    p.append(f'<circle cx="{cx}" cy="{cy}" r="{r*0.16:.1f}" fill="{CHAR}"/><ellipse cx="{cx}" cy="{cy}" rx="{r*0.06:.1f}" ry="{r*0.09:.1f}" fill="{KRAFT}" transform="rotate(18 {cx} {cy})"/>')
    return ''.join(p), labels

def roulette3():
    p = [room(560)]
    p.append(window(24, 96, 92, 150) + window(274, 96, 92, 150))
    p.append(f'<rect x="188" y="470" width="14" height="96" fill="{CHAR}"/><rect x="150" y="560" width="90" height="12" rx="4" fill="{CHAR}"/>')
    w, labels = wheel_plain(195, 340, 140, rot=-14)
    p.append(w)
    p.append(f'<path d="M181 174 h28 l-14 26 z" fill="{RED}"/><circle cx="195" cy="178" r="5" fill="{CREAM}"/>')
    json.dump(labels, open(f'{OUT}/wheel_labels.json', 'w'))
    return ''.join(p)

def reveal():
    p = [f'<rect width="390" height="844" fill="#F3E2D2"/>']
    p.append(f'<path d="M195 120 L70 640 H320 Z" fill="#FFF3D6" opacity="0.85"/>')
    p.append(f'<ellipse cx="195" cy="640" rx="130" ry="24" fill="#EAD2B6"/>')
    rnd = random.Random(3)
    for _ in range(26):
        x = rnd.uniform(20, 370); y = rnd.uniform(140, 520); c = rnd.choice([MUST, CORAL, TEAL, LBLUE]); a = rnd.uniform(0, 180)
        p.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="7" height="4" fill="{c}" transform="rotate({a:.0f} {x:.0f} {y:.0f})"/>')
    p.append(pg(195, 640, 4.6, *MEMBERS[2]))
    # little wallet under the wing
    p.append(f'<g transform="translate(112 556) rotate(-18)"><rect x="0" y="0" width="44" height="30" rx="5" fill="{TEAL_D}"/><rect x="26" y="9" width="18" height="12" rx="3" fill="{TEAL}"/><circle cx="34" cy="15" r="2.4" fill="{MUST}"/></g>')
    return ''.join(p)

def receipt_bg():
    p = [f'<rect width="390" height="844" fill="#EFE6DA"/>']
    p.append(f'<rect x="40" y="70" width="310" height="44" rx="14" fill="{CHAR}"/><rect x="58" y="104" width="274" height="8" rx="4" fill="#1E1E20"/>')
    p.append(f'<circle cx="320" cy="92" r="5" fill="{TEAL_L}"/>')
    return ''.join(p)

if __name__ == '__main__':
    sn = street_night()
    open(f'{OUT}/home_a_night.html', 'w').write(page(wrap(f'<g transform="translate(-390 0)">{sn}</g>'), 390, 844))
    for n, s in (('cafe3', cafe3()), ('roulette3', roulette3()), ('reveal', reveal()), ('receipt_bg', receipt_bg())):
        open(f'{OUT}/{n}.html', 'w').write(page(wrap(s)))
    print(open(f'{OUT}/wheel_labels.json').read())
