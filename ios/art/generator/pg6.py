"""Side-view pigeon guest, nestrip-style base (flat geometric, orange eye, teal neck band, wing bars,
dark tail tip, red legs + leg band). Feet at (0,0), facing right."""
from f_kit import *
from ios import MEMBERS, SEGC, shade

LEG = '#D9584A'
EYE = '#E8793A'
NECK = '#3E9C98'
NECK_PINK = '#F2A7A0'
BAR = '#2E2E30'
TAILTIP = '#3A3B3E'
BEAK = '#3B3B3D'

# size tokens (S: background/extra, M: in-game hero, L: close-up / reveal)
S, M, L = 1.4, 1.9, 3.0

def _band_for(body):
    for i, (b, _) in enumerate(MEMBERS):
        if b == body:
            return SEGC[i]
    return MUST

# head geometry: centre (15,-31), r 7.2
HX, HY, HR = 15, -31, 7.2

def _acc(acc):
    if acc == 'beret':
        return (f'<ellipse cx="{HX-1}" cy="{HY-6.6}" rx="9.4" ry="3.8" fill="{CORAL}" transform="rotate(-10 {HX-1} {HY-6.6})"/>'
                f'<rect x="{HX-1.8}" y="{HY-12.6}" width="2.6" height="3.4" rx="1.2" fill="{CORAL}"/>')
    if acc == 'ribbon':
        x, y = HX - 6.4, HY - 4.6
        return (f'<path d="M{x} {y} l-6.4 -5 v10 z M{x} {y} l6 -5.6 v10.4 z" fill="{RED}"/><circle cx="{x}" cy="{y}" r="2.2" fill="{RED}"/>')
    if acc == 'scarf':
        return (f'<path d="M5 -25 Q12 -19.5 19.5 -24.5 L19.5 -19.5 Q12 -14 5 -19.8 Z" fill="{MUST}"/>'
                f'<path d="M7 -20.5 l-6 11 l5.2 -0.6 l3.6 -9.6 z" fill="{MUST}"/><path d="M4 -12 h5" stroke="{shade(MUST,0.8)}" stroke-width="1.2"/>')
    if acc == 'glasses':
        return (f'<circle cx="{HX+1.6}" cy="{HY-0.6}" r="3.6" fill="{WHITE}" fill-opacity="0.25" stroke="{BEAK}" stroke-width="1.3"/>'
                f'<path d="M{HX-2} {HY-1} L{HX-7} {HY-2.4}" stroke="{BEAK}" stroke-width="1.3" stroke-linecap="round"/>')
    if acc == 'cap':
        return (f'<path d="M{HX-7.6} {HY-2.6} Q{HX-1} {HY-15} {HX+6.4} {HY-4.2} Z" fill="{TEAL_D}"/>'
                f'<path d="M{HX+4.6} {HY-5} l9 0.6 l-8.6 2.8 z" fill="{TEAL_D}"/><circle cx="{HX-1}" cy="{HY-10.6}" r="1.6" fill="{MUST}"/>')
    return ''

def _head(body, acc, eyes='open', dark=False):
    h = [f'<circle cx="{HX}" cy="{HY}" r="{HR}" fill="{body}"/>']
    ex, ey = HX + 1.6, HY - 0.6
    if eyes == 'closed':
        h.append(f'<path d="M{ex-2} {ey} q2 1.8 4 0" stroke="{BEAK}" stroke-width="1.2" fill="none" stroke-linecap="round"/>')
    elif eyes == 'wide':
        h.append(f'<circle cx="{ex}" cy="{ey}" r="3.1" fill="{WHITE}"/><circle cx="{ex}" cy="{ey}" r="2.2" fill="{EYE}"/><circle cx="{ex}" cy="{ey}" r="0.9" fill="{BEAK}"/><circle cx="{ex+0.9}" cy="{ey-0.9}" r="0.5" fill="{WHITE}"/>')
    else:
        h.append(f'<circle cx="{ex}" cy="{ey}" r="2.2" fill="{EYE}"/><circle cx="{ex}" cy="{ey}" r="1" fill="{BEAK}"/><circle cx="{ex+0.8}" cy="{ey-0.8}" r="0.5" fill="{WHITE}"/>')
    # beak + cere
    h.append(f'<path d="M{HX+5.6} {HY-1} L{HX+12.4} {HY+1.6} L{HX+5.2} {HY+2.4} Z" fill="{BEAK}"/><ellipse cx="{HX+6.4}" cy="{HY-0.4}" rx="1.5" ry="1.1" fill="{WHITE}"/>')
    h.append(_acc(acc))
    return ''.join(h)

def _neck(acc):
    if acc == 'scarf':
        return ''
    return (f'<path d="M6 -27.5 Q12 -29.5 18 -25.5 Q18.5 -19 13 -16.5 Q7.5 -16 5 -19.5 Z" fill="{NECK}"/>'
            f'<path d="M8 -20.4 Q12 -22 16.6 -20.6 Q15 -18 12 -17.4 Q9.4 -17.6 8 -20.4 Z" fill="{NECK_PINK}"/>')

def _bars(dark):
    c = '#1E1E20' if dark else BAR
    return (f'<path d="M-4.2 -25 q2.6 4.4 0.6 9.6" stroke="{c}" stroke-width="2.2" fill="none" stroke-linecap="round"/>'
            f'<path d="M0.6 -25.4 q2.6 4.4 0.6 9.6" stroke="{c}" stroke-width="2.2" fill="none" stroke-linecap="round"/>')

def _tail(body):
    return (f'<path d="M-12 -21.6 L-19 -21.6 L-19 -14.6 L-11 -14.6 Z" fill="{shade(body,0.9)}"/>'
            f'<rect x="-24.4" y="-21.6" width="6.4" height="7" rx="1" fill="{TAILTIP}"/>')

def _legs(band, tucked=False):
    if tucked:
        return f'<path d="M-3 -8 l-5 3 M1 -8 l-5 3" stroke="{LEG}" stroke-width="2.2" stroke-linecap="round"/>'
    return (f'<path d="M-2.4 -9 V0 M1.8 -9 V0" stroke="{LEG}" stroke-width="2.4" stroke-linecap="round"/>'
            f'<path d="M-5.6 0.4 H-0.4 M-1.2 0.4 H4.8" stroke="{LEG}" stroke-width="2.4" stroke-linecap="round"/>'
            f'<rect x="0.3" y="-4.4" width="3" height="2.2" rx="0.6" fill="{band}"/>')

def _body(body):
    return (f'<ellipse cx="0" cy="-17.6" rx="15" ry="10.8" fill="{body}"/>'
            f'<path d="M-12 -21 Q-6 -27.6 4 -27 Q7 -21 4 -14 Q-6 -10 -12 -14 Z" fill="{shade(body,0.92)}"/>')

def straw(x1, y1, x2, y2, col=CORAL, curly=False, w=4.4):
    out = f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{WHITE}" stroke-width="{w}" stroke-linecap="round"/><path d="M{x1} {y1} L{x2} {y2}" stroke="{col}" stroke-width="{w}" stroke-dasharray="{w} {w}" stroke-linecap="butt"/>'
    if curly:
        out += (f'<path d="M{x2} {y2} q8 4 4 10 q-6 6 2 10 q8 4 2 10 q-6 6 2 10" stroke="{WHITE}" stroke-width="{w}" fill="none" stroke-linecap="round"/>'
                f'<path d="M{x2} {y2} q8 4 4 10 q-6 6 2 10 q8 4 2 10 q-6 6 2 10" stroke="{col}" stroke-width="{w}" stroke-dasharray="{w} {w}" fill="none"/>')
    return out

def _wing_up(body, dark, big=1.0):
    wc = shade(body, 0.86)
    c = '#1E1E20' if dark else BAR
    g = (f'<path d="M-6 -21 C-17 -28 -19 -44 -10 -53 C-3 -48 3 -36 6 -23 Z" fill="{wc}"/>'
         + ''.join(f'<ellipse cx="{ex}" cy="{ey}" rx="3.2" ry="5.4" fill="{wc}" transform="rotate({ea} {ex} {ey})"/>' for ex, ey, ea in ((-14.6, -45, 30), (-16.4, -37.6, 14), (-15, -30, 0)))
         + f'<path d="M-6 -35 q4 -0.6 7 2.6 M-9 -41 q4 -0.6 7 2.6" stroke="{c}" stroke-width="2" fill="none" stroke-linecap="round"/>')
    if big != 1.0:
        g = f'<g transform="translate(0 -22) scale({big}) translate(0 22)">{g}</g>'
    return g

def _wing_back(body, big=1.0):
    g = f'<path d="M-4 -22 C-20 -30 -28 -42 -20 -48 C-10 -40 -2 -32 2 -24 Z" fill="{shade(body,0.74)}"/>'
    if big != 1.0:
        g = f'<g transform="translate(0 -22) scale({big}) translate(0 22)">{g}</g>'
    return g

def pg2(x, y, s=1.0, body='#A9B2BA', acc=None, pose='stand', flip=False, eyes=None, item=None, band=None):
    band = band or _band_for(body)
    dark = sum(int(body[i:i+2], 16) for i in (1, 3, 5)) < 400
    t = f'translate({x} {y}) scale({-s if flip else s} {s})'
    e = eyes or 'open'
    p = [f'<g transform="{t}">']
    if pose == 'stand':
        p += [_tail(body), _legs(band), _body(body), _bars(dark), _neck(acc), _head(body, acc, e)]
    elif pose == 'sit':
        p += ['<g transform="translate(0 8)">', _tail(body),
              f'<ellipse cx="0" cy="-15.6" rx="16" ry="10.4" fill="{body}"/>',
              f'<path d="M-12.6 -19 Q-6 -25.6 4 -25 Q7 -19 4 -12 Q-6 -8 -12.6 -12 Z" fill="{shade(body,0.92)}"/>',
              '<g transform="translate(0 2)">', _bars(dark), '</g>', _neck(acc), _head(body, acc, e), '</g>']
    elif pose == 'peck':
        p += [_legs(band), '<g transform="rotate(32 0 -12)">', _tail(body), _body(body), _bars(dark), _neck(acc), _head(body, acc, e), '</g>']
    elif pose == 'flap':
        p += [_wing_back(body), _tail(body), _legs(band), _body(body), _wing_up(body, dark), _neck(acc), _head(body, acc, e)]
        p.append(f'<path d="M-30 -40 q-6 6 -4 14 M10 -56 q6 3 7 10" stroke="{BEAK}" stroke-width="1.4" fill="none" stroke-linecap="round" opacity="0.45"/>')
    elif pose == 'fly':
        p += ['<g transform="rotate(-16 0 -16)">', _wing_back(body, 1.3), _tail(body), _legs(band, tucked=True), _body(body), _wing_up(body, dark, 1.3), _neck(acc), _head(body, acc, e), '</g>']
        p.append(f'<path d="M-32 -8 h-10 M-30 -2 h-14 M-32 4 h-8" stroke="{BEAK}" stroke-width="1.4" stroke-linecap="round" opacity="0.35"/>')
    elif pose == 'upright':
        p += [f'<path d="M-2 -9 V0 M2.4 -9 V0" stroke="{LEG}" stroke-width="2.4" stroke-linecap="round"/><path d="M-5 0.4 H0 M-0.6 0.4 H5.4" stroke="{LEG}" stroke-width="2.4" stroke-linecap="round"/><rect x="0.9" y="-4.4" width="3" height="2.2" rx="0.6" fill="{band}"/>',
              f'<path d="M-6 -12 L-12 -1 L-10 -0.4 L-4 -9 Z" fill="{TAILTIP}"/>',
              f'<ellipse cx="0" cy="-20" rx="11.4" ry="15" fill="{body}"/>',
              f'<path d="M-10 -28 Q-4 -33 2 -30 Q4 -20 1 -10 Q-6 -9 -10 -14 Z" fill="{shade(body,0.92)}"/>',
              '<g transform="translate(-1 -1)"><path d="M-5 -28 q2.2 4 0.4 9 M-1 -28.4 q2.2 4 0.4 9" stroke="#1E1E20" stroke-width="2" fill="none" stroke-linecap="round"/></g>',
              '<g transform="translate(-11 -9)">', _neck(acc), _head(body, acc, 'wide'), '</g>',
              f'<path d="M-19 -30 l-5 -2 M-20 -22 l-6 0 M-19 -14 l-5 2 M15 -32 l5 -3 M16 -24 l6 -1 M15 -16 l5 1" stroke="{BEAK}" stroke-width="1.4" stroke-linecap="round" opacity="0.6"/>',
              f'<path d="M12 -55 q2.6 4 0 5.6 q-2.6 -1.6 0 -5.6 z" fill="{LBLUE}"/>']
    if item == 'straw':
        p.append(straw(HX + 11, HY + 1.6, HX + 20, HY + 28, CORAL))
    elif item == 'curly':
        p.append(straw(HX + 11, HY + 1.6, HX + 17, HY + 22, MUST, curly=True))
    p.append('</g>')
    return ''.join(p)

def avatar(i):
    """120x120 head-and-chest crop for circular avatars (use at 100% width)."""
    body, acc = MEMBERS[i]
    return pg2(22, 146, 3.1, body, acc, 'stand')

if __name__ == '__main__':
    from ios import svg_raw
    OUTD = '/home/claude/lb_art/ios'
    poses = [('stand', None), ('sit', None), ('peck', None), ('flap', None), ('fly', 'straw'), ('upright', None), ('sleep', None), ('curly', 'curly')]
    for i, (n, item) in enumerate(poses):
        body, acc = MEMBERS[i % 5]
        if n == 'sleep':
            g = pg2(96, 150, 2.6, body, acc, 'sit', eyes='closed')
        elif n == 'curly':
            g = pg2(84, 140, 2.4, body, acc, 'flap', item='curly', eyes='wide')
        elif n == 'fly':
            g = pg2(100, 130, 2.4, body, acc, n, item=item)
        else:
            g = pg2(96, 156, 2.6, body, acc, n, item=item)
        open(f'{OUTD}/ps_{n}.html', 'w').write(f'<!doctype html><html><head><meta charset="utf-8"><style>html,body{{margin:0;background:transparent}}</style></head><body style="width:200px;height:170px">{svg_raw("<rect width=\"200\" height=\"170\" fill=\"none\"/>" + g, 200, 170)}</body></html>')
    for i in range(5):
        open(f'{OUTD}/av6_{i}.html', 'w').write(f'<!doctype html><html><head><meta charset="utf-8"><style>html,body{{margin:0;background:transparent}}</style></head><body style="width:120px;height:120px">{svg_raw("<rect width=\"120\" height=\"120\" fill=\"none\"/>" + avatar(i), 120, 120)}</body></html>')
    # nestrip reference check
    open(f'{OUTD}/pg_ref.html', 'w').write(f'<!doctype html><html><head><meta charset="utf-8"></head><body style="margin:0;width:600px;height:220px;background:#CFE3E6">{svg_raw("<rect width=\"600\" height=\"220\" fill=\"#CFE3E6\"/>" + "".join(pg2(70 + i*115, 190, 3.2, *MEMBERS[i]) for i in range(5)), 600, 220)}</body></html>')
    print('ok')
