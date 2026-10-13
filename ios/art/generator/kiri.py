"""Kiri pose set: small dot eyes, natural poses. Feet at (0,0), ~36 units tall."""
from f_kit import *
from ios2 import kiri_walk2

C = CAT; D = '#C9722A'; W = CATC
def ears(x1, y1, x2, y2, inner=True):
    # two triangular ears given left/right base centres
    out = (f'<path d="M{x1-3.4} {y1} L{x1-2.4} {y1-7.5} L{x1+1.6} {y1-2} Z M{x2-1.6} {y2-2} L{x2+2.4} {y2-7.5} L{x2+3.4} {y2} Z" fill="{C}"/>')
    if inner:
        out += f'<path d="M{x1-2.2} {y1-1.2} L{x1-1.8} {y1-4.6} L{x1} {y1-2.2} Z M{x2} {y2-2.2} L{x2+1.8} {y2-4.6} L{x2+2.2} {y2-1.2} Z" fill="{PEACH}"/>'
    return out
def dot(x, y): return f'<circle cx="{x}" cy="{y}" r="0.7" fill="{CHAR}"/>'
def shut(x, y): return f'<path d="M{x-1} {y} q1 0.9 2 0" stroke="{CHAR}" stroke-width="0.85" fill="none" stroke-linecap="round"/>'
def nose(x, y): return f'<path d="M{x-0.8} {y} h1.6 l-0.8 0.9 z" fill="{CHAR}"/>'
def g(inner, x, y, s, flip=False): return f'<g transform="translate({x} {y}) scale({-s if flip else s} {s})">{inner}</g>'

def loaf(x, y, s=1.0, flip=False):
    i = (f'<ellipse cx="-2" cy="-9" rx="15" ry="9.5" fill="{C}"/>'
         f'<path d="M-11 -17 q1 4 0 7 M-6 -18.4 q1 4 0 7 M-1 -18 q1 4 0 6.6" stroke="{D}" stroke-width="1.3" fill="none" stroke-linecap="round"/>'
         f'<path d="M-15 -3 C-17 2 -4 3 4 1.6" stroke="{C}" stroke-width="3.4" fill="none" stroke-linecap="round"/><path d="M-9 1.4 l1.4 1.4 M-5 1.8 l1.2 1.4" stroke="{D}" stroke-width="1"/>'
         f'<ellipse cx="9" cy="-6" rx="4.2" ry="4.6" fill="{W}"/><ellipse cx="7.5" cy="-0.8" rx="2.8" ry="1.5" fill="{W}"/><ellipse cx="12.4" cy="-0.8" rx="2.8" ry="1.5" fill="{W}"/>'
         + ears(6, -22, 14, -22.4) +
         f'<circle cx="10" cy="-17.4" r="7.4" fill="{C}"/><path d="M8.6 -24 v2.4 M10.4 -24.3 v2.6 M12.2 -24 v2.4" stroke="{D}" stroke-width="0.9" stroke-linecap="round"/>'
         f'<ellipse cx="11.2" cy="-14.6" rx="3" ry="2" fill="{W}"/>' + shut(7.6, -17.8) + shut(13.2, -17.8) + nose(11.2, -15.8))
    return g(i, x, y, s, flip)

def stretch(x, y, s=1.0, flip=False):
    i = (f'<path d="M-15 -20 C-22 -28 -19 -37 -13 -35" stroke="{C}" stroke-width="3.2" fill="none" stroke-linecap="round"/>'
         f'<path d="M-11 -16 L-13 0" stroke="{D}" stroke-width="3.4" stroke-linecap="round"/><path d="M-7 -15 L-6 0" stroke="{C}" stroke-width="3.6" stroke-linecap="round"/>'
         f'<ellipse cx="-1" cy="-13" rx="15" ry="6" fill="{C}" transform="rotate(20 -1 -13)"/>'
         f'<path d="M-8 -19.6 q1.6 2.6 0.6 5 M-3 -17.8 q1.6 2.6 0.6 5 M2 -15.6 q1.4 2.4 0.4 4.6" stroke="{D}" stroke-width="1.3" fill="none" stroke-linecap="round"/>'
         f'<path d="M8 -6 L20 -1" stroke="{D}" stroke-width="3.2" stroke-linecap="round"/><path d="M7 -5 L22 0" stroke="{C}" stroke-width="3.4" stroke-linecap="round"/><ellipse cx="22.6" cy="-0.2" rx="2.2" ry="1.3" fill="{W}"/>'
         + ears(14.5, -13.5, 21, -13.6) +
         f'<circle cx="17.6" cy="-8.6" r="6" fill="{C}"/><ellipse cx="20.6" cy="-6.4" rx="2.6" ry="1.8" fill="{W}"/>' + shut(15.6, -9.4) + shut(19.8, -9.6) +
         f'<ellipse cx="20.8" cy="-5.2" rx="1" ry="1.2" fill="{CHAR}"/>')
    return g(i, x, y, s, flip)

def curl(x, y, s=1.0, flip=False):
    i = (f'<ellipse cx="2" cy="-9" rx="17" ry="9.6" fill="{C}"/>'
         f'<path d="M-2 -17.6 q1.4 4 0 7 M4 -18.4 q1.4 4 0 7 M10 -17 q1.2 3.6 0 6" stroke="{D}" stroke-width="1.3" fill="none" stroke-linecap="round"/>'
         + ears(-12, -12, -5, -14.4) +
         f'<circle cx="-8.6" cy="-8.4" r="7" fill="{C}"/><ellipse cx="-11" cy="-5.6" rx="2.6" ry="1.8" fill="{W}"/>' + shut(-11.6, -8.8) + shut(-6.4, -9) +
         f'<path d="M-15 -1.6 C-8 3.4 12 3.4 19 -5" stroke="{C}" stroke-width="5" fill="none" stroke-linecap="round"/><path d="M4 1.6 l0.6 -2 M9 0.6 l0.4 -2" stroke="{D}" stroke-width="1.1"/>'
         f'<path d="M22 -20 q2 -2 4 0 M26 -25 q1.6 -1.6 3.2 0" stroke="{GREY}" stroke-width="1" fill="none" stroke-linecap="round"/>')
    return g(i, x, y, s, flip)

def back(x, y, s=1.0, flip=False):
    i = (f'<path d="M6 -1 C16 0 19 -7 14 -11" stroke="{C}" stroke-width="3.2" fill="none" stroke-linecap="round"/>'
         f'<path d="M-9 0 C-11 -10 -7 -19 0 -19.5 C7 -19 11 -10 9 0 Z" fill="{C}"/>'
         f'<path d="M-7 -7 q7 3 14 0 M-6.6 -12 q6.6 2.6 13.2 0" stroke="{D}" stroke-width="1.3" fill="none" stroke-linecap="round"/>'
         f'<path d="M-6.6 -25 L-5.6 -32.6 L-1.6 -28 Z M6.6 -25 L5.6 -32.6 L1.6 -28 Z" fill="{C}"/><path d="M-5.4 -27 L-5 -30.4 L-3.2 -28 Z M5.4 -27 L5 -30.4 L3.2 -28 Z" fill="{D}"/>'
         f'<ellipse cx="0" cy="-23.6" rx="7.4" ry="6.4" fill="{C}"/><path d="M-2 -29 v3.2 M0 -29.6 v3.6 M2 -29 v3.2" stroke="{D}" stroke-width="1" stroke-linecap="round"/>')
    return g(i, x, y, s, flip)

def box_peek(x, y, s=1.0, flip=False):
    i = (f'<path d="M14 -8 C23 -8 25 -17 20 -21" stroke="{C}" stroke-width="3.2" fill="none" stroke-linecap="round"/><path d="M20.6 -14 l2 -0.8 M22 -10.6 l2 0" stroke="{D}" stroke-width="1"/>'
         + ears(-3.6, -22, 3.6, -22) +
         f'<ellipse cx="0" cy="-20" rx="6.8" ry="4.6" fill="{C}"/>' + dot(-2.4, -21.6) + dot(2.4, -21.6) +
         f'<rect x="-14" y="-20" width="28" height="20" fill="{KRAFT}"/><rect x="-3" y="-20" width="6" height="20" fill="{CREAM}" opacity="0.45"/>'
         f'<path d="M-14 -20 l-7 -5 h9 l5 5 z M14 -20 l7 -5 h-9 l-5 5 z" fill="{KRAFT_D}"/>')
    return g(i, x, y, s, flip)

def paw_tap(x, y, s=1.0, flip=False):
    i = (f'<path d="M-8 -2 C-16 -1 -18 -10 -13 -14" stroke="{C}" stroke-width="3.2" fill="none" stroke-linecap="round"/>'
         f'<path d="M-8 0 C-10 -10 -4 -20 4 -20 C9 -18 9 -8 8 0 Z" fill="{C}"/>'
         f'<path d="M-6 -9 q2 -1 4 0 M-6.4 -5 q2 -1 4 0" stroke="{D}" stroke-width="1.2" fill="none" stroke-linecap="round"/>'
         f'<ellipse cx="5" cy="-11" rx="3" ry="4" fill="{W}"/>'
         f'<path d="M5 0 V-8" stroke="{C}" stroke-width="3.4" stroke-linecap="round"/><ellipse cx="5.6" cy="0" rx="2.4" ry="1.3" fill="{W}"/>'
         f'<path d="M7 -13 Q13 -16 16.5 -12.6" stroke="{C}" stroke-width="3.4" fill="none" stroke-linecap="round"/><circle cx="17" cy="-12.4" r="1.8" fill="{W}"/>'
         + ears(3.4, -27.6, 10.2, -27.2) +
         f'<circle cx="6.4" cy="-23.6" r="6.6" fill="{C}"/><path d="M5 -29.6 v2.2 M6.8 -29.9 v2.4" stroke="{D}" stroke-width="0.9" stroke-linecap="round"/>'
         f'<ellipse cx="10.2" cy="-21.6" rx="2.5" ry="1.8" fill="{W}"/>' + dot(8.6, -24.6) + nose(11.4, -22.6) +
         f'<g transform="rotate(14 24 0)"><path d="M19 0 h9 l1.2 -11 h-11.4 z" fill="{WHITE}"/><ellipse cx="23.5" cy="-11" rx="5.7" ry="1.4" fill="#8A5A3C"/><rect x="19.4" y="-7" width="9.4" height="2.4" fill="{TEAL}"/></g>'
         f'<path d="M17 -18 l1.6 -2.4 M20.6 -16.8 l2.4 -1.4" stroke="{CHAR}" stroke-width="1" stroke-linecap="round"/>')
    return g(i, x, y, s, flip)

def jump(x, y, s=1.0, flip=False):
    body = (f'<path d="M-13 -15 C-22 -19 -24 -27 -20 -31" stroke="{C}" stroke-width="3.2" fill="none" stroke-linecap="round"/>'
            f'<path d="M-9 -12 L-20 -8" stroke="{D}" stroke-width="3.2" stroke-linecap="round"/><path d="M-9 -14 L-21 -13" stroke="{C}" stroke-width="3.4" stroke-linecap="round"/>'
            f'<ellipse cx="0" cy="-14" rx="15" ry="5.8" fill="{C}"/>'
            f'<path d="M-5 -19 q1 2.6 0 5 M0 -19.6 q1 2.6 0 5 M5 -19.2 q1 2.4 0 4.6" stroke="{D}" stroke-width="1.2" fill="none" stroke-linecap="round"/>'
            f'<path d="M9 -11 L20 -9" stroke="{D}" stroke-width="3.2" stroke-linecap="round"/><path d="M9 -13 L21 -15" stroke="{C}" stroke-width="3.4" stroke-linecap="round"/>'
            + ears(13.4, -22.6, 19.8, -22.8) +
            f'<circle cx="16.4" cy="-18.4" r="6" fill="{C}"/><ellipse cx="19.6" cy="-16.4" rx="2.4" ry="1.7" fill="{W}"/>' + dot(18, -19.6) + nose(20.8, -17.4))
    i = f'<ellipse cx="0" cy="0" rx="14" ry="2.4" fill="#000" opacity="0.08"/><g transform="translate(0 -14) rotate(-18)">{body}</g>'
    return g(i, x, y, s, flip)

def sit_front(x, y, s=1.0):
    i = (f'<path d="M7 -1 C17 0 18 -10 12 -14" stroke="{C}" stroke-width="3.2" stroke-linecap="round" fill="none"/>'
         f'<path d="M-8 0 C-9.5 -8 -6.5 -15 0 -15.5 C6.5 -15 9.5 -8 8 0 Z" fill="{C}"/>'
         f'<path d="M-7.6 -6 q2 -1 3 0 M5 -8 q2 -1 3 0" stroke="{D}" stroke-width="1.1" fill="none" stroke-linecap="round"/>'
         f'<ellipse cx="0" cy="-5.5" rx="3.6" ry="4.6" fill="{W}"/>' + ears(-4.2, -21, 4.2, -21) +
         f'<ellipse cx="0" cy="-19" rx="7.4" ry="6.3" fill="{C}"/><path d="M-1.6 -25 v2.4 M0 -25.3 v2.6 M1.6 -25 v2.4" stroke="{D}" stroke-width="0.9" stroke-linecap="round"/>'
         f'<ellipse cx="0" cy="-16.4" rx="2.6" ry="1.8" fill="{W}"/>' + dot(-3.4, -19.4) + dot(3.4, -19.4) + nose(0, -17.6))
    return g(i, x, y, s)

POSES = [('walk', lambda: kiri_walk2(100, 150, 3.0)), ('loaf', lambda: loaf(100, 150, 3.2)), ('stretch', lambda: stretch(96, 150, 3.0)),
         ('curl', lambda: curl(100, 146, 3.0)), ('back', lambda: back(96, 150, 3.2)), ('box', lambda: box_peek(96, 150, 3.2)),
         ('tap', lambda: paw_tap(84, 150, 3.0)), ('jump', lambda: jump(96, 158, 2.8)), ('sit', lambda: sit_front(96, 150, 3.4))]

if __name__ == '__main__':
    from ios import svg_raw
    for n, f in POSES:
        open(f'{OUT[:-4]}/ios/k_{n}.html', 'w').write(f'<!doctype html><html><head><meta charset="utf-8"><style>html,body{{margin:0;background:transparent}}</style></head><body style="width:200px;height:170px">{svg_raw("<rect width=\"200\" height=\"170\" fill=\"none\"/>"+f(),200,170)}</body></html>')
    print('ok')
