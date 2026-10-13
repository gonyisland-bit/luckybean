"""Round 2: home A (horizontal street) vs home B (cafe-zoomed map). Kiri with small eyes + natural poses."""
import random
import ios
from ios import *

def kiri_walk2(x, y, s=1.0, flip=False):
    col = CAT; dk = '#C9722A'
    t = f'translate({x} {y}) scale({-s if flip else s} {s})'
    return f'''<g transform="{t}">
<path d="M-13 -14 C-22 -16 -24 -28 -18 -32 C-16 -33 -15 -31 -16 -30" stroke="{col}" stroke-width="3.2" stroke-linecap="round" fill="none"/>
<path d="M-8 -10 L-12 0 M9 -10 L6 0" stroke="{dk}" stroke-width="3.4" stroke-linecap="round"/>
<path d="M-6 -10 L-3 0 M11 -10 L14 0" stroke="{col}" stroke-width="3.6" stroke-linecap="round"/>
<ellipse cx="0" cy="-13" rx="14" ry="6.4" fill="{col}"/>
<path d="M-6 -18.6 q1.2 3 0 5.6 M-1 -19.2 q1.2 3 0 5.6 M4 -18.8 q1.2 3 0 5.4" stroke="{dk}" stroke-width="1.3" fill="none" stroke-linecap="round"/>
<path d="M11 -24 L12 -31.5 L16 -25.5 Z M16.5 -25 L19.5 -30.5 L20.5 -23 Z" fill="{col}"/>
<circle cx="15.5" cy="-19.5" r="6.2" fill="{col}"/>
<ellipse cx="19.6" cy="-17.6" rx="2.6" ry="1.9" fill="{CATC}"/>
<circle cx="17.4" cy="-20.6" r="0.7" fill="{CHAR}"/>
<path d="M21.6 -18.6 l0.9 0.6 -0.9 0.6 z" fill="{CHAR}"/>
</g>'''

ios.kiri_walk = lambda x, y, s=1.0: kiri_walk2(x, y + 1, s * 0.75, flip=True)

SKY = '#E9EEEA'

def cloud(x, y, s=1.0):
    return f'<g transform="translate({x} {y}) scale({s})"><ellipse cx="0" cy="0" rx="26" ry="9" fill="{WHITE}" opacity="0.9"/><ellipse cx="-8" cy="-6" rx="12" ry="9" fill="{WHITE}" opacity="0.9"/><ellipse cx="9" cy="-7" rx="10" ry="8" fill="{WHITE}" opacity="0.9"/></g>'

def sc(inner, s, tx, ty):
    return f'<g transform="translate({tx} {ty}) scale({s})">{inner}</g>'

BASE = 610  # street line
S = 1.8

def street(W=1170):
    p = [f'<rect width="{W}" height="844" fill="{SKY}"/>']
    # distant hills + pale town
    p.append(f'<path d="M0 470 C160 400 300 430 460 410 C640 386 760 440 920 400 C1020 380 1100 410 {W} 400 V{BASE} H0 Z" fill="#DCE6E1"/>')
    rnd = random.Random(2)
    for x in range(0, W, 46):
        h = rnd.choice([40, 56, 70, 48]); w = rnd.choice([30, 36, 26])
        p.append(f'<rect x="{x}" y="{BASE-60-h}" width="{w}" height="{h+60}" fill="#E4E9E5"/><path d="M{x-3} {BASE-60-h} l{w/2+3} -12 l{w/2+3} 12 z" fill="#DADFDB"/>')
    p.append(cloud(120, 150, 1.2) + cloud(520, 110) + cloud(840, 170, 1.3) + cloud(1060, 120, 0.9) + cloud(330, 240, 0.8))
    # sidewalk, road, foreground
    p.append(f'<rect y="{BASE}" width="{W}" height="40" fill="#E6DED0"/><rect y="{BASE}" width="{W}" height="4" fill="#D6CCBA"/>')
    p.append(''.join(f'<rect x="{x}" y="{BASE+4}" width="1.4" height="36" fill="#D6CCBA"/>' for x in range(30, W, 60)))
    p.append(f'<rect y="{BASE+40}" width="{W}" height="86" fill="#D9DDDB"/>' + ''.join(f'<rect x="{x}" y="{BASE+82}" width="26" height="4" rx="2" fill="{WHITE}"/>' for x in range(10, W, 64)))
    p.append(f'<rect y="{BASE+126}" width="{W}" height="{844-BASE-126}" fill="#CFDCC3"/>')
    for hx in range(40, W, 90):
        p.append(hatch(hx, BASE + 170, '#B5C8A4'))
    # ---- park (0..300)
    park = []
    park.append(gazebo(120, 0, 80))
    park.append(f'<ellipse cx="60" cy="-4" rx="40" ry="7" fill="{LBLUE}"/>')
    park.append(f'<rect x="190" y="-16" width="40" height="5" rx="2" fill="{BROWN}"/><path d="M194 -11 v11 M226 -11 v11" stroke="{CHAR}" stroke-width="2"/>')
    park.append(a_tree(26, 0, 20) + a_pine(70, 0, 24, 66) + a_tree(170, 0, 14))
    park.append(pg(206, -16, 0.55, *MEMBERS[3]))
    p.append(sc(''.join(park), 1.3, 0, BASE))
    # ---- lounge (tall teal house) at 330
    p.append(sc(house(0, 0, 56, 150, TEAL, CHAR, roof_h=26, cols=2, rows=4, door=MUST, chimney=True), S, 340, BASE))
        # ---- cafe centre (585)
    p.append(sc(euro_cafe(0, 0, 174), S, 585 - 87 * S, BASE))
    p.append(sc(a_frame(0, 0, 1.0), S, 585 + 87 * S + 18, BASE + 6))
    p.append(kiri_walk2(470, BASE + 30, 1.3))
    p.append(pg(690, BASE + 26, 0.62, *MEMBERS[0], flip=True) + pg(662, BASE + 32, 0.62, *MEMBERS[2]))
    # ---- records hall at 728
    p.append(sc(house(0, 0, 78, 90, GREY_L, CHAR, roof_h=28, cols=3, rows=2, door=ORANGE, arch=True) + f'<circle cx="39" cy="-104" r="9" fill="{WHITE}"/><path d="M39 -104 v-5 M39 -104 l3.4 2" stroke="{CHAR}" stroke-width="1.4" stroke-linecap="round"/>', S, 740, BASE))
        # ---- post office at 900
    p.append(sc(house(0, 0, 70, 58, CREAM, RED, roof_h=24, cols=2, rows=1, door=TEAL_D) + f'<rect x="78" y="-18" width="12" height="18" rx="3" fill="{RED}"/><rect x="80" y="-14" width="8" height="2" fill="{CHAR}"/>', S, 905, BASE))
    # ---- map shop at 1050
    p.append(sc(house(0, 0, 70, 58, PEACH, ORANGE, roof_h=24, cols=2, rows=1, door=TEAL_D, tex='scallop') + f'<rect x="80" y="-46" width="3" height="46" fill="{CHAR}"/><rect x="72" y="-62" width="34" height="22" rx="3" fill="{WHITE}"/><path d="M76 -46 l7 -8 l7 5 l7 -7 l5 3" stroke="{TEAL}" stroke-width="2" fill="none" stroke-linecap="round"/>', S, 1040, BASE))
    p.append(sc(lamp(0,0),1.5,300,BASE+8) + sc(lamp(0,0),1.5,895,BASE+8))
    p.append(car(560, BASE + 108, MUST, w=60, kind='taxi') + car(160, BASE + 110, ORANGE, w=70, kind='bus') + car(930, BASE + 108, TEAL_D, w=54, flip=True))
    p.append(ios.leaves(30, 0, BASE + 130, W, 830, 8))
    p.append(a_tree(60, 844, 22) + a_tree(1110, 844, 20))
    return ''.join(p)

def home_b():
    inner = ios.home()
    # strip the noisy layers: leaves are fine at zoom, but crop tight on the cafe
    return f'<rect width="390" height="844" fill="{MAP}"/><g transform="scale(1.75) translate(-100 -150)">{inner}</g>'

if __name__ == '__main__':
    pano = street()
    open(f'{OUT}/street_pano.html', 'w').write(page(wrap(pano, 1170, 844), 1170, 844))
    open(f'{OUT}/home_a.html', 'w').write(page(wrap(f'<g transform="translate(-390 0)">{pano}</g>'), 390, 844))
    open(f'{OUT}/home_b.html', 'w').write(page(wrap(home_b())))
    print('ok')
