"""Kiri's choice v3: picture-book park (gingham lawn, patterned trees), Kiri seen from behind wiggling, catch = Kiri hugging the pigeon."""
import math, random, json
from f_kit import *
from ios import MEMBERS, shade
from pg6 import pg2, S as PS, M as PM
from ios6 import feather, OUT

C = CAT; D = '#C9722A'; W = CATC
G_BASE, G_LINE = '#6DBA86', '#86C899'
TR_DK, TR_MID, TR_LT, TR_PINE = '#2F8A5F', '#3FA06B', '#58B07A', '#2E9A62'
TRUNK, TRUNK_D = '#E9A43C', '#C98428'

DEFS2 = f'''<defs>
<pattern id="ging" width="26" height="26" patternUnits="userSpaceOnUse"><rect width="26" height="26" fill="{G_BASE}"/><rect width="26" height="11" fill="{G_LINE}" opacity="0.55"/><rect width="11" height="26" fill="{G_LINE}" opacity="0.55"/></pattern>
<pattern id="plaid" width="18" height="18" patternUnits="userSpaceOnUse"><path d="M0 4 H18 M0 12 H18 M5 0 V18 M13 0 V18" stroke="#1F6E49" stroke-width="2.4" opacity="0.45"/></pattern>
<pattern id="hatch" width="7" height="12" patternUnits="userSpaceOnUse"><path d="M3 2 V10" stroke="#1F6E49" stroke-width="1.6" stroke-linecap="round" opacity="0.45"/></pattern>
<pattern id="leafy" width="22" height="20" patternUnits="userSpaceOnUse"><ellipse cx="6" cy="6" rx="3.4" ry="5" fill="#8FD0A0" opacity="0.65" transform="rotate(-20 6 6)"/><ellipse cx="17" cy="15" rx="3.4" ry="5" fill="#8FD0A0" opacity="0.65" transform="rotate(20 17 15)"/></pattern>
</defs>'''

def trunk(x, base, w, h):
    return (f'<path d="M{x-w/2} {base} L{x-w/2+3} {base-h} H{x+w/2-3} L{x+w/2} {base} Z" fill="{TRUNK}"/>'
            f'<path d="M{x-w/6:.1f} {base-4} v-{h*0.45:.0f} M{x+w/6:.1f} {base-6} v-{h*0.35:.0f}" stroke="{TRUNK_D}" stroke-width="2.2" stroke-linecap="round"/>')

def blob(x, y, r, n=7, seed=1):
    rnd = random.Random(seed); out = [f'<circle cx="{x}" cy="{y}" r="{r*0.82:.1f}"/>']
    for k in range(n):
        a = 2 * math.pi * k / n; rr = r * rnd.uniform(0.32, 0.42)
        out.append(f'<circle cx="{x+(r-rr)*math.cos(a):.1f}" cy="{y+(r-rr)*0.92*math.sin(a):.1f}" r="{rr:.1f}"/>')
    return ''.join(out)

def tree_round(x, base, r, col=TR_DK, deco='plaid', seed=1):
    cy = base - r * 1.55
    p = [f'<ellipse cx="{x}" cy="{base+2}" rx="{r*0.9:.0f}" ry="{r*0.18:.1f}" fill="#2F7D52" opacity="0.25"/>', trunk(x, base, r * 0.55, r * 0.9)]
    p.append(f'<g fill="{col}">{blob(x, cy, r, seed=seed)}</g>')
    if deco in ('plaid', 'hatch', 'leafy'):
        p.append(f'<g fill="url(#{deco})">{blob(x, cy, r, seed=seed)}</g>')
    rnd = random.Random(seed + 9)
    if deco in ('dots', 'apples', 'stars'):
        for _ in range(6 if deco != 'dots' else 8):
            a = rnd.uniform(0, 6.28); rr = r * math.sqrt(rnd.uniform(0.05, 0.6))
            px, py = x + rr * math.cos(a), cy + rr * math.sin(a)
            if deco == 'dots':
                p.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{r*0.09:.1f}" fill="#F3E36A"/>')
            elif deco == 'apples':
                p.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{r*0.08:.1f}" fill="#F7C9D2"/><path d="M{px:.1f} {py-r*0.08:.1f} v-3" stroke="{TRUNK_D}" stroke-width="1.4"/>')
            else:
                k = r * 0.1
                p.append(f'<path d="M{px:.1f} {py-k:.1f} l{k*0.3:.1f} {k*0.7:.1f} {k*0.75:.1f} 0 -{k*0.6:.1f} {k*0.45:.1f} {k*0.25:.1f} {k*0.75:.1f} -{k*0.7:.1f} -{k*0.45:.1f} -{k*0.7:.1f} {k*0.45:.1f} {k*0.25:.1f} -{k*0.75:.1f} -{k*0.6:.1f} -{k*0.45:.1f} {k*0.75:.1f} 0 z" fill="#F7E27A"/>')
    return ''.join(p)

def tree_fir(x, base, h, col=TR_PINE):
    w = h * 0.55; th = h * 0.16
    p = [f'<ellipse cx="{x}" cy="{base+2}" rx="{w*0.55:.0f}" ry="{w*0.1:.1f}" fill="#2F7D52" opacity="0.25"/>', trunk(x, base, w * 0.3, th + 6)]
    tiers = 4; top = base - h; pts = [f'M{x} {top}']
    for i in range(1, tiers + 1):
        yy = top + (h - th) * i / tiers; ww = w * (0.35 + 0.65 * i / tiers) / 2
        pts.append(f'L{x+ww:.1f} {yy:.1f} L{x+ww*0.55:.1f} {yy-4:.1f}')
    rev = []
    for i in range(tiers, 0, -1):
        yy = top + (h - th) * i / tiers; ww = w * (0.35 + 0.65 * i / tiers) / 2
        rev.append(f'L{x-ww*0.55:.1f} {yy-4:.1f} L{x-ww:.1f} {yy:.1f}' if i != tiers else f'L{x-ww:.1f} {yy:.1f}')
    d = ' '.join(pts[:-1]) + f' L{x+w/2:.1f} {base-th:.1f} L{x-w/2:.1f} {base-th:.1f} ' + ' '.join(rev[1:]) + ' Z'
    p.append(f'<path d="{d}" fill="{col}"/><path d="{d}" fill="url(#hatch)"/>')
    return ''.join(p)

def bush(x, y, w, h, col=TR_MID):
    d = f'M{x-w/2} {y} C{x-w/2} {y-h*0.7} {x-w*0.3} {y-h} {x-w*0.1} {y-h*0.85} C{x} {y-h*1.15} {x+w*0.35} {y-h*1.05} {x+w*0.38} {y-h*0.7} C{x+w*0.55} {y-h*0.65} {x+w/2} {y-h*0.2} {x+w/2} {y} Z'
    return f'<ellipse cx="{x}" cy="{y+2}" rx="{w*0.52:.0f}" ry="5" fill="#2F7D52" opacity="0.22"/><path d="{d}" fill="{col}"/><path d="{d}" fill="url(#hatch)"/>'

def daisy(x, y, k=1.0):
    return ''.join(f'<circle cx="{x+math.cos(a)*2.6*k:.1f}" cy="{y+math.sin(a)*2.6*k:.1f}" r="{1.7*k:.1f}" fill="{WHITE}"/>' for a in [i * 1.2566 for i in range(5)]) + f'<circle cx="{x}" cy="{y}" r="{1.3*k:.1f}" fill="{MUST}"/>'

def mushroom(x, y, k=1.0):
    return f'<rect x="{x-2*k:.1f}" y="{y-6*k:.1f}" width="{4*k:.1f}" height="{6*k:.1f}" rx="1.4" fill="{CREAM}"/><path d="M{x-6*k:.1f} {y-5*k:.1f} q{6*k:.1f} -9 {12*k:.1f} 0 z" fill="#E9A43C"/>'


def cafe_far(x, base, k=1.0):
    """Lucky Bean cafe seen far away across the park (same look as the street facade)."""
    w, h = 92, 58
    p = [f'<g transform="translate({x} {base}) scale({k})">']
    p.append(f'<ellipse cx="0" cy="3" rx="56" ry="6" fill="#2F7D52" opacity="0.2"/>')
    p.append(f'<rect x="{-w/2}" y="{-h}" width="{w}" height="{h}" fill="#F6CBB8"/>')
    # roof with dormers + chimney
    p.append(f'<rect x="20" y="{-h-34}" width="9" height="16" fill="{CHAR}"/>')
    p.append(f'<path d="M{-w/2-4} {-h} L{-w/2+8} {-h-24} H{w/2-8} L{w/2+4} {-h} Z" fill="{CHAR}"/><path d="M{-w/2-4} {-h} L{-w/2+8} {-h-24} H{w/2-8} L{w/2+4} {-h} Z" fill="url(#scallopW)" opacity="0.55"/>')
    for dx in (-18, 14):
        p.append(f'<path d="M{dx-6} {-h-6} V{-h-16} L{dx} {-h-22} L{dx+6} {-h-16} V{-h-6} Z" fill="#F6EFE3"/><rect x="{dx-3}" y="{-h-15}" width="6" height="8" fill="#AFD3DE"/>')
    # upper windows
    for dx in (-30, -10, 10, 30):
        p.append(f'<path d="M{dx-5} {-h+22} V{-h+12} a5 5 0 0 1 10 0 V{-h+22} Z" fill="#FBE3B0"/>')
    # sign + awning + shopfront
    p.append(f'<rect x="-26" y="{-h+27}" width="52" height="7" rx="2" fill="{MUST}"/>')
    p.append(f'<rect x="{-w/2}" y="{-26}" width="{w}" height="26" fill="{TEAL_D}"/>')
    p.append(''.join(f'<path d="M{-w/2+i*11.5:.1f} -28 h11.5 v4 a5.75 5.75 0 0 1 -11.5 0 z" fill="{CORAL if i % 2 else "#F6EFE3"}"/>' for i in range(8)))
    p.append(f'<rect x="-40" y="-18" width="26" height="16" fill="#FBE3B0"/><rect x="14" y="-18" width="26" height="16" fill="#FBE3B0"/><rect x="-6" y="-20" width="12" height="20" fill="#5E9C9E"/><circle cx="3" cy="-10" r="1.2" fill="{MUST}"/>')
    # two tiny terrace tables
    p.append(f'<rect x="-52" y="-6" width="10" height="2" fill="{CHAR}"/><rect x="-48" y="-4" width="2" height="6" fill="{CHAR}"/><rect x="42" y="-6" width="10" height="2" fill="{CHAR}"/><rect x="46" y="-4" width="2" height="6" fill="{CHAR}"/>')
    p.append('</g>')
    return ''.join(p)

def street_row():
    """Across the road: the same high street as the home screen (cafe + neighbours, sidewalk, road)."""
    p = []
    p.append(f'<path d="M0 150 C80 136 160 146 240 138 S350 132 390 140 V250 H0 Z" fill="#B9DCC6"/>')
    # neighbours
    p.append(f'<rect x="-6" y="170" width="70" height="70" fill="#E9DCC8"/><path d="M-10 170 L29 146 L68 170 Z" fill="{TEAL_D}"/>'
             + ''.join(f'<rect x="{x}" y="186" width="12" height="16" fill="#FBE3B0"/>' for x in (6, 26, 46)) + f'<rect x="-6" y="220" width="70" height="20" fill="{CORAL}" opacity="0.6"/>')
    p.append(f'<rect x="68" y="182" width="78" height="58" fill="#CFE3E3"/><rect x="68" y="176" width="78" height="8" fill="{CHAR}"/>'
             + ''.join(f'<rect x="{x}" y="194" width="14" height="14" fill="#FBE3B0"/>' for x in (78, 100, 122)) + f'<rect x="72" y="222" width="70" height="18" fill="{TEAL}"/>')
    p.append(f'<rect x="262" y="178" width="74" height="62" fill="#F2E6CF"/><path d="M258 178 L299 158 L340 178 Z" fill="#8E9AA6"/>'
             + ''.join(f'<rect x="{x}" y="190" width="12" height="15" fill="#FBE3B0"/>' for x in (272, 293, 314)) + f'<rect x="266" y="220" width="66" height="20" fill="#E8C27A"/>')
    p.append(f'<rect x="340" y="186" width="56" height="54" fill="#DCCFE0"/><rect x="340" y="180" width="56" height="7" fill="{CHAR}"/>' + ''.join(f'<rect x="{x}" y="198" width="12" height="14" fill="#FBE3B0"/>' for x in (350, 370)))
    p.append(cafe_far(206, 240, 1.0))
    # sidewalk, kerb, road with lane marks, crosswalk, a taxi
    p.append(f'<rect y="240" width="390" height="10" fill="#E9E1D2"/><rect y="250" width="390" height="3" fill="#CFC5B2"/>')
    p.append(f'<rect y="253" width="390" height="30" fill="#C9CFD3"/>' + ''.join(f'<rect x="{x}" y="267" width="16" height="2.4" rx="1" fill="{WHITE}"/>' for x in range(4, 390, 34) if not 180 < x < 236))
    p.append(''.join(f'<rect x="{x}" y="255" width="5" height="26" fill="{WHITE}" opacity="0.9"/>' for x in range(186, 232, 9)))
    p.append(f'<g transform="translate(318 274)"><rect x="-18" y="-10" width="36" height="10" rx="4" fill="{MUST}"/><path d="M-11 -10 l4 -7 h14 l4 7 z" fill="{MUST}"/><rect x="-7" y="-16" width="6" height="5" fill="#CFE3E6"/><rect x="2" y="-16" width="6" height="5" fill="#CFE3E6"/><rect x="-3" y="-20" width="7" height="3" fill="{CHAR}"/><circle cx="-10" cy="0" r="3.4" fill="{CHAR}"/><circle cx="10" cy="0" r="3.4" fill="{CHAR}"/></g>')
    # park kerb + low hedge with a gate opening facing the crosswalk
    p.append(f'<rect y="283" width="390" height="5" fill="#E9E1D2"/>')
    p.append(f'<path d="M0 300 V292 Q12 284 24 292 Q36 284 48 292 Q60 284 72 292 Q84 284 96 292 Q108 284 120 292 Q132 284 144 292 Q156 284 168 292 V300 Z" fill="#3F9A66"/>')
    p.append(f'<path d="M244 300 V292 Q256 284 268 292 Q280 284 292 292 Q304 284 316 292 Q328 284 340 292 Q352 284 364 292 Q376 284 390 292 V300 Z" fill="#3F9A66"/>')
    p.append(f'<rect x="172" y="282" width="6" height="20" rx="2" fill="{CREAM}"/><rect x="236" y="282" width="6" height="20" rx="2" fill="{CREAM}"/><circle cx="175" cy="281" r="4" fill="{MUST}"/><circle cx="239" cy="281" r="4" fill="{MUST}"/>')
    return ''.join(p)

def park_bg():
    p = [DEFS2, f'<rect width="390" height="844" fill="#9AD3E6"/>']
    p.append(''.join(f'<g transform="translate({x} {y}) scale({k})"><ellipse cx="0" cy="0" rx="40" ry="12" fill="{WHITE}"/><ellipse cx="-14" cy="-9" rx="18" ry="12" fill="{WHITE}"/><ellipse cx="14" cy="-10" rx="15" ry="11" fill="{WHITE}"/></g>' for x, y, k in ((300, 64, 0.8), (96, 112, 0.7))))
    p.append(street_row())
    p.append(f'<rect y="300" width="390" height="544" fill="url(#ging)"/>')
    # path: from the park gate (facing the crosswalk) winding down through the lawn
    p.append(f'<path d="M207 300 C200 360 250 400 230 450 S120 520 130 600 S60 680 -20 700" stroke="#F3E9A6" stroke-width="22" fill="none" stroke-linecap="round" opacity="0.9"/>')
    # pond bottom-left
    p.append(f'<path d="M-20 760 C40 730 120 742 150 790 C170 830 120 860 -20 860 Z" fill="#9CD7EC"/>')
    p.append(''.join(f'<ellipse cx="{x}" cy="{y}" rx="9" ry="5" fill="#4FAE76"/><path d="M{x} {y} l7 -3" stroke="#9CD7EC" stroke-width="2"/>' for x, y in ((40, 790), (92, 812))))
    # trees inside the park edge, leaving the cafe view open in the middle
    p.append(tree_fir(26, 330, 110) + tree_round(110, 326, 26, TR_LT, 'leafy', 2) + tree_round(310, 330, 30, TR_DK, 'apples', 3) + tree_fir(368, 336, 120, TR_MID))
    # bench inside the park, under the big tree on the right, facing the lawn
    bx, by = 316, 428
    p.append(f'<ellipse cx="{bx}" cy="{by+12}" rx="42" ry="6" fill="#2F7D52" opacity="0.22"/><rect x="{bx-36}" y="{by-26}" width="72" height="6" rx="2" fill="#F6EFE3"/><rect x="{bx-36}" y="{by-17}" width="72" height="6" rx="2" fill="#F6EFE3"/>'
             f'<path d="M{bx-40} {by-10} h80 l-4 8 h-72 z" fill="{TRUNK}"/><rect x="{bx-32}" y="{by-2}" width="4" height="12" fill="{CHAR}"/><rect x="{bx+28}" y="{by-2}" width="4" height="12" fill="{CHAR}"/>'
             f'<path d="M{bx+8} {by-12} h12 l-1.4 -12 h-9.2 z" fill="{WHITE}"/><rect x="{bx+7}" y="{by-26}" width="14" height="3" rx="1" fill="{TEAL_D}"/>')
    p.append(tree_round(-2, 500, 46, TR_MID, 'dots', 6) + bush(360, 650, 70, 40, TR_LT))
    rnd = random.Random(21)
    for _ in range(9):
        p.append(daisy(rnd.uniform(20, 370), rnd.uniform(330, 760), rnd.uniform(0.8, 1.3)))
    p.append(mushroom(150, 352, 1.1) + mushroom(164, 356, 0.8) + mushroom(330, 710, 1.2))
    p.append(''.join(f'<path d="M{x} {y} l3 -5 l3 5" stroke="#4FAE76" stroke-width="1.6" fill="none" stroke-linecap="round"/>' for x, y in ((70, 390), (190, 420), (290, 500), (160, 640), (280, 760), (60, 560))))
    return ''.join(p)

def front_layer():
    """Foreground trees overlapping the bottom edge (drawn after characters)."""
    return tree_round(-14, 900, 62, TR_DK, 'plaid', 8) + tree_fir(392, 880, 200, '#2B8A58')

def kiri_rear(x, y, s=1.0, wig=8):
    """Kiri crouched seen from behind: back of the head, ears, round back, raised wiggling rump + tail."""
    i = (f'<ellipse cx="0" cy="0.6" rx="15" ry="3" fill="#000" opacity="0.12"/>'
         f'<path d="M-17 -12 q-3 4 0 8 M-20 -14 q-4 6 0 12 M17 -12 q3 4 0 8 M20 -14 q4 6 0 12" stroke="{CHAR}" stroke-width="1" fill="none" stroke-linecap="round" opacity="0.45"/>'
         # head (further away, lower: crouched)
         f'<path d="M-7.6 -30 L-6.6 -38.2 L-1.8 -33 Z M7.6 -30 L6.6 -38.2 L1.8 -33 Z" fill="{C}"/><path d="M-6.4 -31.8 L-5.9 -36 L-3.6 -33 Z M6.4 -31.8 L5.9 -36 L3.6 -33 Z" fill="{D}" opacity="0.7"/>'
         f'<ellipse cx="0" cy="-29" rx="8.4" ry="7"  fill="{C}"/>'
         f'<path d="M-2.4 -35 v3 M0 -35.6 v3.4 M2.4 -35 v3" stroke="{D}" stroke-width="1.1" stroke-linecap="round"/>'
         # shoulders + back
         f'<ellipse cx="0" cy="-20" rx="10.6" ry="7.6" fill="{C}"/>'
         f'<g transform="rotate({wig} 0 -8)">'
         f'<ellipse cx="0" cy="-10" rx="13.6" ry="10" fill="{C}"/>'
         f'<path d="M-9 -15 q9 -3.4 18 0 M-10.6 -10 q10.6 -3.4 21.2 0 M-8 -21.6 q8 -3 16 0" stroke="{D}" stroke-width="1.5" fill="none" stroke-linecap="round"/>'
         f'<path d="M0 -12 C3 -22 12 -30 8 -40 C6 -44 2 -43 3.4 -40" stroke="{C}" stroke-width="4.2" fill="none" stroke-linecap="round"/>'
         f'<path d="M6.6 -30 l3.4 0.8 M8.4 -36 l3 -0.6" stroke="{D}" stroke-width="1.3" stroke-linecap="round"/>'
         f'<ellipse cx="-7.4" cy="-1.4" rx="4.6" ry="3" fill="{C}"/><ellipse cx="7.4" cy="-1.4" rx="4.6" ry="3" fill="{C}"/>'
         f'<ellipse cx="-7.4" cy="-0.4" rx="3.4" ry="1.7" fill="{W}"/><ellipse cx="7.4" cy="-0.4" rx="3.4" ry="1.7" fill="{W}"/>'
         f'</g>')
    return f'<g transform="translate({x} {y}) scale({s})">{i}</g>'

def kiri_hold(x, y, s, prey_svg_fn):
    """Kiri sitting facing us, hugging a pigeon to its chest, eyes happily closed."""
    head = (f'<path d="M-6.4 -27 L-5.4 -34.6 L-1.2 -29.6 Z M6.4 -27 L5.4 -34.6 L1.2 -29.6 Z" fill="{C}"/><path d="M-5.2 -28.6 L-4.8 -32.2 L-2.6 -29.8 Z M5.2 -28.6 L4.8 -32.2 L2.6 -29.8 Z" fill="{PEACH}"/>'
            f'<ellipse cx="0" cy="-23" rx="8.8" ry="7.4" fill="{C}"/>'
            f'<path d="M-2 -30 v2.6 M0 -30.4 v2.8 M2 -30 v2.6" stroke="{D}" stroke-width="1" stroke-linecap="round"/>'
            f'<ellipse cx="0" cy="-20.4" rx="3" ry="2.1" fill="{W}"/>'
            f'<path d="M-4.6 -23.2 q1 -1.2 2 0 M2.6 -23.2 q1 -1.2 2 0" stroke="{CHAR}" stroke-width="0.9" fill="none" stroke-linecap="round"/>'
            f'<path d="M-0.7 -21.6 h1.4 l-0.7 0.8 z" fill="{CHAR}"/><ellipse cx="-5.4" cy="-20.6" rx="1.5" ry="0.9" fill="{CORAL}" opacity="0.7"/><ellipse cx="5.4" cy="-20.6" rx="1.5" ry="0.9" fill="{CORAL}" opacity="0.7"/>')
    body = (f'<ellipse cx="0" cy="0.6" rx="14" ry="2.6" fill="#000" opacity="0.12"/>'
            f'<path d="M8 -1 C18 0 20 -9 14 -13" stroke="{C}" stroke-width="3.4" fill="none" stroke-linecap="round"/>'
            f'<path d="M-10.4 0 C-12 -10 -8 -17.6 0 -18 C8 -17.6 12 -10 10.4 0 Z" fill="{C}"/>'
            f'<path d="M-10 -8 q2 -1 3.4 0 M-10.4 -4 q2 -1 3.4 0 M7 -8 q2 -1 3.4 0 M7 -4 q2 -1 3.4 0" stroke="{D}" stroke-width="1.2" fill="none" stroke-linecap="round"/>'
            f'<ellipse cx="0" cy="-8" rx="5" ry="6" fill="{W}"/>'
            f'<ellipse cx="-5.4" cy="-0.6" rx="3.4" ry="1.8" fill="{W}"/><ellipse cx="5.4" cy="-0.6" rx="3.4" ry="1.8" fill="{W}"/>')
    paws = (f'<path d="M-9 -15 Q-8 -9 -2.6 -8.4" stroke="{C}" stroke-width="3.6" fill="none" stroke-linecap="round"/><ellipse cx="-2" cy="-8.4" rx="2.2" ry="1.7" fill="{W}"/>'
            f'<path d="M9 -15 Q8 -9 2.6 -8.4" stroke="{C}" stroke-width="3.6" fill="none" stroke-linecap="round"/><ellipse cx="2" cy="-8.4" rx="2.2" ry="1.7" fill="{W}"/>')
    t = f'translate({x} {y}) scale({s})'
    return f'<g transform="{t}">{body}{head}</g>' + prey_svg_fn(x, y - 4 * s, s) + f'<g transform="{t}">{paws}</g>'


COLLAR = '#2F6FB8'
def _stripes_back(ys, half):
    return ''.join(f'<path d="M{-half(y):.1f} {y+2.4:.1f} Q0 {y-2.6:.1f} {half(y):.1f} {y+2.4:.1f}" stroke="{D}" stroke-width="1.6" fill="none" stroke-linecap="round"/>' for y in ys)

def kiri_walk_rear(x, y, s=1.0, step=1):
    """Kiri walking away on four legs, seen from behind and slightly above (tail up, collar)."""
    lh = -2.6 if step else 0; rh = 0 if step else -2.6
    i = (f'<ellipse cx="0" cy="0.8" rx="15" ry="3.2" fill="#000" opacity="0.13"/>'
         # front legs (further away)
         f'<path d="M-5.4 -24 V{-16-2*step}" stroke="{D}" stroke-width="3.8" stroke-linecap="round"/><path d="M5.4 -24 V{-16-2*(1-step)}" stroke="{D}" stroke-width="3.8" stroke-linecap="round"/>'
         # hind legs (near)
         f'<path d="M-7.4 -10 V{lh-1.4}" stroke="{C}" stroke-width="5.4" stroke-linecap="round"/><path d="M7.4 -10 V{rh-1.4}" stroke="{C}" stroke-width="5.4" stroke-linecap="round"/>'
         f'<ellipse cx="-7.4" cy="{lh-0.6}" rx="3.2" ry="{1.4 if lh else 1.7}" fill="{W}"/><ellipse cx="7.4" cy="{rh-0.6}" rx="3.2" ry="{1.4 if rh else 1.7}" fill="{W}"/>'
         # body: wide rump tapering to the shoulders
         f'<path d="M-12.6 -9 C-14.6 -18 -10 -28 -6.6 -32 C-3 -34.6 3 -34.6 6.6 -32 C10 -28 14.6 -18 12.6 -9 C10.6 -3.4 -10.6 -3.4 -12.6 -9 Z" fill="{C}"/>'
         + _stripes_back((-26, -21, -16, -11), lambda yy: 6 + (yy + 30) * 0.32) +
         f'<path d="M0 -31 V-24" stroke="{D}" stroke-width="1.6" stroke-linecap="round"/>'
         # head (back of), collar
         f'<path d="M-6.2 -37 L-5.4 -45.4 L-1 -40 Z M6.2 -37 L5.4 -45.4 L1 -40 Z" fill="{C}"/><path d="M-5 -38.8 L-4.6 -42.6 L-2.6 -40 Z M5 -38.8 L4.6 -42.6 L2.6 -40 Z" fill="{D}" opacity="0.6"/>'
         f'<ellipse cx="0" cy="-37.6" rx="7.6" ry="6.6" fill="{C}"/>'
         f'<path d="M-2 -43 v2.6 M0 -43.6 v3 M2 -43 v2.6" stroke="{D}" stroke-width="1.1" stroke-linecap="round"/>'
         
         # tail up with white tip
         f'<path d="M0 -8 C-2 -16 6 -22 10 -26 C14 -30 12 -36 9 -37" stroke="{C}" stroke-width="4.2" fill="none" stroke-linecap="round"/>'
         f'<path d="M12.2 -32.6 C12.6 -35.4 11 -36.8 9 -37" stroke="{W}" stroke-width="3.6" fill="none" stroke-linecap="round"/>'
         f'<path d="M2 -18.6 l3.2 0.6 M5.6 -22.4 l3 0.8" stroke="{D}" stroke-width="1.3" stroke-linecap="round"/>')
    return f'<g transform="translate({x} {y}) scale({s})">{i}</g>'

def kiri_catch_rear(x, y, s, prey):
    """Kiri crouched from behind (round loaf like a back view), head bent down over a caught pigeon
    whose head and flapping wing poke out past the right shoulder; tail curls with a white tip."""
    t = f'translate({x} {y}) scale({s})'
    body = (f'<g transform="{t}"><ellipse cx="0" cy="0.6" rx="18" ry="3.4" fill="#000" opacity="0.13"/>'
            f'<path d="M-15 -8 C-17.6 -22 -10 -32 -2 -32.6 C8 -33 16.6 -25 16 -12 C15.6 -4 10 -1 0 -1 C-9 -1 -14 -3 -15 -8 Z" fill="{C}"/>'
            + _stripes_back((-26, -21, -16, -11, -6.4), lambda yy: 8 + (yy + 32) * 0.3) +
            f'<path d="M7 -30 q3 4 2.4 9 M11 -26 q2.6 3.6 2 8" stroke="{D}" stroke-width="1.5" fill="none" stroke-linecap="round"/>'
            # head bent down, slightly to the left
            f'<path d="M-10.8 -33.6 L-11.6 -41.6 L-5.8 -37.2 Z M-0.6 -35.4 L1.6 -42.8 L3.4 -35 Z" fill="{C}"/><path d="M-10 -35 L-10.4 -38.8 L-7.4 -36.6 Z M0.6 -36 L1.8 -39.6 L2.6 -36 Z" fill="{D}" opacity="0.6"/>'
            f'<ellipse cx="-4.2" cy="-33" rx="7.8" ry="6.6" fill="{C}" transform="rotate(-10 -4.2 -33)"/>'
            f'<path d="M-6.4 -38.6 v2.6 M-4.2 -39.2 v3 M-2 -38.8 v2.6" stroke="{D}" stroke-width="1.1" stroke-linecap="round"/>'
            
            # curled tail with white tip, wiggling
            f'<path d="M6 -2.6 C8 4 -2 6.4 -10 4.4" stroke="{C}" stroke-width="4.6" fill="none" stroke-linecap="round"/>'
            f'<path d="M-6.6 5.2 C-8.4 5.4 -10 5 -11.4 4" stroke="{W}" stroke-width="4.6" fill="none" stroke-linecap="round"/>'
            f'<path d="M0.4 3.4 l0.4 2.4 M3.6 1.6 l1.2 2" stroke="{D}" stroke-width="1.2" stroke-linecap="round"/>'
            f'<path d="M-16 6 q-3 2 -4 5 M-19 2 q-4 1 -6 4" stroke="{CHAR}" stroke-width="0.9" fill="none" stroke-linecap="round" opacity="0.45"/></g>')
    paw = (f'<g transform="{t}"><path d="M12 -22 Q16 -24 19 -21" stroke="{C}" stroke-width="4" fill="none" stroke-linecap="round"/>'
           f'<ellipse cx="19.6" cy="-20.6" rx="2.4" ry="1.8" fill="{W}"/></g>')
    return prey + body + paw

KS = 4.2
SPOTS = {0: (120, 428, 'peck', False), 1: (250, 392, 'stand', True), 2: (300, 560, 'peck', True), 3: (88, 580, 'stand', False), 4: (200, 498, 'stand', True)}
def depth(y): return round(1.2 + (y - 380) / 400 * 0.7, 2)
def shadow(x, y, rx): return f'<ellipse cx="{x}" cy="{y+2}" rx="{rx:.0f}" ry="{rx*0.28:.1f}" fill="#2F7D52" opacity="0.28"/>'

def kiri_park(catch=False):
    p = [park_bg()]; tags = {}
    if not catch:
        for mi, (x, y, pose, fl) in sorted(SPOTS.items(), key=lambda kv: kv[1][1]):
            s = depth(y); p.append(shadow(x, y, 15 * s) + pg2(x, y, s, *MEMBERS[mi], pose=pose, flip=fl)); tags[mi] = [x, y + 8]
        p.append(kiri_walk_rear(200, 800, KS, step=1))
        p.append(f'<path d="M150 610 q-6 -10 0 -18 M244 610 q6 -10 0 -18" stroke="{CHAR}" stroke-width="2" fill="none" stroke-linecap="round" opacity="0.3"/>')
    else:
        for mi, (x, y, pose, fl) in SPOTS.items():
            if mi != 1:
                p.append(feather(x - 8, y - 2, 30, '#E8EEF0') + feather(x + 6, y, -50, '#E8EEF0'))
        cx, cy, ks = 186, 676, KS * 0.82   # loaf body is wider in units; keeps on-screen size equal to the walking pose
        prey = pg2(cx + 50, cy - 34, PS * 1.15, *MEMBERS[1], pose='flap', eyes='wide')
        p.append(kiri_catch_rear(cx, cy, ks, prey))
        p.append(feather(286, 520, -30, '#F3F0EA') + feather(232, 500, 40, '#F3F0EA') + feather(316, 590, 70, '#F3F0EA'))
        p.append(f'<path d="M310 552 l12 -6 M316 572 l12 0 M312 592 l11 5" stroke="{CHAR}" stroke-width="2.4" stroke-linecap="round" opacity="0.45"/>')
        p.append(f'<path d="M130 520 c-5 -7 -14 -3 -10 4 l10 10 10 -10 c4 -7 -5 -11 -10 -4 z" fill="{CORAL}"/>')
        for mi, x, y, fl in ((0, 66, 330, True), (2, 330, 236, False), (3, 44, 520, True), (4, 330, 420, False)):
            p.append(pg2(x, y, PS, *MEMBERS[mi], pose='fly', flip=fl)); tags[mi] = [x, y + 6]
        tags[1] = [262, 642]
    p.append(front_layer())
    json.dump(tags, open(f'{OUT}/kiri8_{"b" if catch else "a"}.json', 'w'))
    return ''.join(p)

if __name__ == '__main__':
    for n, c in (('kiri8_a', False), ('kiri8_b', True)):
        open(f'{OUT}/{n}.html', 'w').write(page(wrap(kiri_park(c))))
    print('ok')
