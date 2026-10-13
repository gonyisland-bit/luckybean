"""Review fixes: evening reveal, new icons (kiri rear / espresso)."""
import math
from f_kit import *
from ios import MEMBERS, svg_raw
from ios4 import gauge
from ios6 import facade_strip, pavement, shadow, OUT
from pg6 import pg2, S as PS, L as PL
import kiri8

def reveal_evening():
    p = [facade_strip(120), pavement(120)]
    # evening tint, no blur: flat multiply + a lamp whose cone and pool stay crisp
    p.append(f'<rect width="390" height="844" fill="#9FB0CF" style="mix-blend-mode:multiply"/><rect width="390" height="844" fill="#2B3F6E" opacity="0.08"/>')
    p.append(''.join(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#FFD98A"/>' for x, y, w, h in ((14, 0, 110, 92), (266, 0, 110, 92), (170, 0, 50, 110))))
    p.append(f'<path d="M36 150 L40 700 H350 L66 150 Z" fill="#FFE9A8" opacity="0.3"/>')
    p.append(f'<ellipse cx="195" cy="655" rx="155" ry="38" fill="#FFE9A8" opacity="0.55"/>')
    p.append(f'<rect x="42" y="152" width="6" height="300" fill="{CHAR}"/><path d="M32 152 h26 l-4 -10 h-18 z" fill="{CHAR}"/><rect x="38" y="134" width="14" height="10" fill="#FFF3C4"/><path d="M45 142 q14 -18 30 -6" stroke="{CHAR}" stroke-width="4" fill="none" stroke-linecap="round"/>')
    for (x, y, mi, fl) in ((60, 600, 0, False), (110, 700, 1, False), (290, 700, 3, True), (338, 600, 4, True)):
        p.append(shadow(x, y, 20) + pg2(x, y, PS, *MEMBERS[mi], pose='flap', flip=fl))
    p.append(shadow(195, 640, 34) + pg2(195, 640, PL, *MEMBERS[2], pose='upright'))
    return ''.join(p)

def ic_kiri():
    return (kiri8.DEFS2 + f'<circle cx="60" cy="62" r="50" fill="url(#ging)"/><path d="M14 86 C40 70 70 80 100 66" stroke="#F3E9A6" stroke-width="9" fill="none" stroke-linecap="round" opacity="0.9"/>'
            + pg2(84, 44, 0.75, *MEMBERS[1], pose='peck', flip=True) + kiri8.kiri_walk_rear(56, 104, 1.75, step=1))

def ic_esp():
    return gauge(60, 54, 34, 9.0) + f'<rect x="38" y="92" width="44" height="7" rx="3" fill="{CHAR}"/><path d="M52 99 v10 h16 v-10" fill="none" stroke="{WHITE}" stroke-width="3"/>' + pg2(104, 114, 0.9, *MEMBERS[2], pose='stand', flip=True)

if __name__ == '__main__':
    open(f'{OUT}/reveal7.html', 'w').write(page(wrap(reveal_evening())))
    for n, f in (('i6_kiri', ic_kiri), ('i6_esp', ic_esp)):
        open(f'{OUT}/{n}.html', 'w').write(f'<!doctype html><html><head><meta charset="utf-8"><style>html,body{{margin:0;background:transparent}}</style></head><body style="width:120px;height:120px">{svg_raw("<rect width=\"120\" height=\"120\" fill=\"none\"/>" + f(), 120, 120)}</body></html>')
    print('ok')
