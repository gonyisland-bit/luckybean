"""Nordic hand-drawn town kit for Lucky Bean F-series (sibling of 오늘줍기 / nestrip)."""
import glob, math, os, random
FONTS = glob.glob('/root/.claude/skills/synced/*/canvas-design/canvas-fonts')[0]
OUT = '/home/claude/lb_art/out'
os.makedirs(OUT, exist_ok=True)

BG = '#EFEEEA'; MAP = '#DCDDD8'; WHITE = '#FFFFFF'
TEAL = '#5E9C9E'; TEAL_D = '#3F7F82'; TEAL_L = '#A9CCCB'; TEAL_XL = '#CFE3E3'
MUST = '#EDB43E'; MUST_L = '#F3D27C'; CORAL = '#F2A48C'; PEACH = '#F6CBB8'
ORANGE = '#E8793A'; RED = '#D9533D'; CREAM = '#F5EEE2'; GREY = '#B9BFC0'; GREY_L = '#D7DBDB'
CHAR = '#3B3B3D'; BROWN = '#8A5A3C'; KRAFT = '#C9A06A'; KRAFT_D = '#B08850'; LBLUE = '#CFE3E6'
CAT = '#E8913A'; CATC = '#F7E7D0'

DEFS = f'''
<pattern id="stripeW" width="8" height="8" patternUnits="userSpaceOnUse"><rect width="8" height="3" fill="#FFFFFF" opacity="0.55"/></pattern>
<pattern id="stripeV" width="10" height="10" patternUnits="userSpaceOnUse"><rect width="4" height="10" fill="#FFFFFF" opacity="0.5"/></pattern>
<pattern id="scallopW" width="12" height="9" patternUnits="userSpaceOnUse"><path d="M0 9 a6 6 0 0 1 12 0" fill="none" stroke="#FFFFFF" stroke-width="1.6" opacity="0.7"/></pattern>
<pattern id="dotsW" width="8" height="8" patternUnits="userSpaceOnUse"><circle cx="4" cy="4" r="1.3" fill="#FFFFFF" opacity="0.6"/></pattern>
<pattern id="check" width="28" height="28" patternUnits="userSpaceOnUse"><rect width="28" height="28" fill="#DCE6E5"/><rect width="28" height="9" fill="{TEAL_L}" opacity="0.55"/><rect width="9" height="28" fill="{TEAL_L}" opacity="0.55"/></pattern>
<pattern id="tentStripe" width="40" height="40" patternUnits="userSpaceOnUse"><rect width="40" height="40" fill="{CREAM}"/><rect width="20" height="40" fill="{CORAL}"/></pattern>
<pattern id="wallpaper" width="24" height="24" patternUnits="userSpaceOnUse"><rect width="24" height="24" fill="{TEAL_XL}"/><path d="M12 5 l3 5 -3 5 -3 -5 z" fill="{TEAL_L}" opacity="0.7"/></pattern>
<pattern id="planksF" width="60" height="16" patternUnits="userSpaceOnUse"><rect width="60" height="16" fill="#D9BE98"/><rect y="15" width="60" height="1.2" fill="#C4A57C"/><rect x="40" width="1.2" height="16" fill="#C4A57C"/></pattern>
<pattern id="kraftLines" width="10" height="10" patternUnits="userSpaceOnUse"><rect width="10" height="10" fill="{KRAFT}"/><rect y="4" width="10" height="0.8" fill="{KRAFT_D}" opacity="0.4"/></pattern>
<filter id="hand" x="-2%" y="-2%" width="104%" height="104%"><feTurbulence type="fractalNoise" baseFrequency="0.04" numOctaves="2" seed="4" result="w"/><feDisplacementMap in="SourceGraphic" in2="w" scale="1.6" xChannelSelector="R" yChannelSelector="G"/></filter>
<filter id="grain" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="7"/><feColorMatrix values="0 0 0 0 0.3  0 0 0 0 0.3  0 0 0 0 0.3  0 0 0 0.5 -0.2"/></filter>
<radialGradient id="glow"><stop offset="0" stop-color="#FFE7A8" stop-opacity="0.75"/><stop offset="1" stop-color="#FFE7A8" stop-opacity="0"/></radialGradient>
'''

def house(x, base, w, h, body, roof_col, roof='gable', roof_h=None, cols=2, rows=1, win='#F6F2EA', door=None, chimney=False, tex='stripe', arch=False):
    p = []
    rh = roof_h if roof_h is not None else w * 0.45
    if chimney:
        p.append(f'<rect x="{x+w*0.68}" y="{base-h-rh*0.9}" width="{w*0.12}" height="{rh*0.7}" fill="{CHAR}"/>')
    p.append(f'<rect x="{x}" y="{base-h}" width="{w}" height="{h}" fill="{body}"/>')
    if roof == 'gable':
        d = f'M{x-3} {base-h} L{x+w/2} {base-h-rh} L{x+w+3} {base-h} Z'
    elif roof == 'flat':
        d = f'M{x-4} {base-h} L{x+2} {base-h-rh} L{x+w-2} {base-h-rh} L{x+w+4} {base-h} Z'
    else:  # scallop awning-like
        d = f'M{x-4} {base-h} L{x-4} {base-h-rh} L{x+w+4} {base-h-rh} L{x+w+4} {base-h} Z'
    p.append(f'<path d="{d}" fill="{roof_col}"/>')
    pat = {'stripe': 'stripeW', 'scallop': 'scallopW', 'dots': 'dotsW', None: None}[tex]
    if pat:
        p.append(f'<path d="{d}" fill="url(#{pat})"/>')
    ww, wh = w * 0.18, h * 0.2
    usable_h = h * (0.55 if door else 0.8)
    for c in range(cols):
        for r in range(rows):
            cx = x + w * (c + 0.5) / cols - ww / 2
            cy = base - h + 8 + r * (usable_h / max(rows, 1))
            if arch:
                p.append(f'<path d="M{cx:.1f} {cy+wh:.1f} V{cy+ww/2:.1f} A{ww/2:.1f} {ww/2:.1f} 0 0 1 {cx+ww:.1f} {cy+ww/2:.1f} V{cy+wh:.1f} Z" fill="{win}"/>')
            else:
                p.append(f'<rect x="{cx:.1f}" y="{cy:.1f}" width="{ww:.1f}" height="{wh:.1f}" fill="{win}"/>')
    if door:
        dw, dh = w * 0.2, h * 0.34
        dx = x + w / 2 - dw / 2
        p.append(f'<path d="M{dx:.1f} {base} V{base-dh+dw/2:.1f} A{dw/2:.1f} {dw/2:.1f} 0 0 1 {dx+dw:.1f} {base-dh+dw/2:.1f} V{base} Z" fill="{door}"/>')
    return ''.join(p)

def tree(x, base, r, col=TEAL, trunk=CHAR):
    return f'<rect x="{x-1.6}" y="{base-r*1.1}" width="3.2" height="{r*1.1}" fill="{trunk}"/><ellipse cx="{x}" cy="{base-r*1.5}" rx="{r*0.85}" ry="{r}" fill="{col}"/>'

def pine(x, base, w, h, col=TEAL_D, trunk=CHAR):
    return (f'<rect x="{x-1.4}" y="{base-h*0.2}" width="2.8" height="{h*0.2}" fill="{trunk}"/>'
            f'<path d="M{x} {base-h} L{x+w*0.35} {base-h*0.6} L{x+w*0.2} {base-h*0.6} L{x+w*0.5} {base-h*0.2} L{x-w*0.5} {base-h*0.2} L{x-w*0.2} {base-h*0.6} L{x-w*0.35} {base-h*0.6} Z" fill="{col}"/>')

def hatch(cx, cy, col=TEAL_L, n=9, spread=16):
    rnd = random.Random(int(cx * 13 + cy * 7))
    out = []
    for _ in range(n):
        x = cx + rnd.uniform(-spread, spread); y = cy + rnd.uniform(-spread * 0.4, spread * 0.4)
        out.append(f'<path d="M{x:.1f} {y:.1f} l2 -3 l2 3" stroke="{col}" stroke-width="1.2" fill="none" stroke-linecap="round"/>')
    return ''.join(out)

def car(x, y, col, w=34, kind='car', flip=False):
    h = w * 0.34
    t = f' transform="translate({2*x+w} 0) scale(-1 1)"' if flip else ''
    if kind == 'bus':
        body = f'<rect x="{x}" y="{y-h*1.5}" width="{w}" height="{h*1.5}" rx="5" fill="{col}"/>' + ''.join(f'<rect x="{x+4+i*w/5:.1f}" y="{y-h*1.3:.1f}" width="{w/7:.1f}" height="{h*0.6:.1f}" rx="1.5" fill="{CREAM}"/>' for i in range(4))
    else:
        body = (f'<path d="M{x} {y-h*0.3} Q{x} {y-h} {x+w*0.2} {y-h} L{x+w*0.3} {y-h*1.7} L{x+w*0.72} {y-h*1.7} L{x+w*0.82} {y-h} Q{x+w} {y-h} {x+w} {y-h*0.3} Z" fill="{col}"/>'
                f'<rect x="{x+w*0.35}" y="{y-h*1.55}" width="{w*0.15}" height="{h*0.5}" fill="{CREAM}"/><rect x="{x+w*0.53}" y="{y-h*1.55}" width="{w*0.15}" height="{h*0.5}" fill="{CREAM}"/>')
        if kind == 'taxi':
            body += f'<rect x="{x+w*0.44}" y="{y-h*2}" width="{w*0.12}" height="{h*0.3}" fill="{CHAR}"/>'
    wheels = f'<circle cx="{x+w*0.22}" cy="{y-h*0.15}" r="{h*0.32}" fill="{CHAR}"/><circle cx="{x+w*0.78}" cy="{y-h*0.15}" r="{h*0.32}" fill="{CHAR}"/>'
    return f'<g{t}>{body}{wheels}</g>'

def cat_sit(x, y, s=1.0, col=CAT, eyes='open'):
    e = (f'<circle cx="-3" cy="-19" r="1.1" fill="{CHAR}"/><circle cx="3" cy="-19" r="1.1" fill="{CHAR}"/>' if eyes == 'open'
         else f'<path d="M-4.4 -19 q1.4 1.2 2.8 0 M1.6 -19 q1.4 1.2 2.8 0" stroke="{CHAR}" stroke-width="0.9" fill="none" stroke-linecap="round"/>')
    return f'''<g transform="translate({x} {y}) scale({s})">
<path d="M7 -1 C16 0 17 -9 12 -13" stroke="{col}" stroke-width="3" stroke-linecap="round" fill="none"/>
<path d="M-8 0 C-9.5 -8 -6.5 -15 0 -15.5 C6.5 -15 9.5 -8 8 0 Z" fill="{col}"/>
<ellipse cx="0" cy="-5.5" rx="3.6" ry="4.6" fill="{CATC}"/>
<path d="M-6.6 -20 L-5.6 -27.5 L-1.6 -23 Z M6.6 -20 L5.6 -27.5 L1.6 -23 Z" fill="{col}"/>
<ellipse cx="0" cy="-19" rx="7.2" ry="6.2" fill="{col}"/>
{e}<path d="M-1 -16.6 h2 l-1 1.1 z" fill="{CHAR}"/>
</g>'''

def cat_walk(x, y, s=1.0, col=CAT):
    return f'''<g transform="translate({x} {y}) scale({s})">
<path d="M12 -8 C20 -12 21 -22 17 -26" stroke="{col}" stroke-width="3" stroke-linecap="round" fill="none"/>
<rect x="-10" y="-5" width="3" height="8" rx="1.5" fill="{col}"/><rect x="-5" y="-5" width="3" height="8" rx="1.5" fill="{col}"/><rect x="5" y="-5" width="3" height="8" rx="1.5" fill="{col}"/><rect x="9" y="-5" width="3" height="8" rx="1.5" fill="{col}"/>
<ellipse cx="1" cy="-8" rx="13" ry="6.4" fill="{col}"/>
<path d="M-17 -15 L-16 -22 L-12 -17 Z M-9 -16 L-9.6 -23 L-12.6 -17.4 Z" fill="{col}"/>
<circle cx="-13" cy="-12" r="6" fill="{col}"/><circle cx="-15" cy="-12.6" r="0.9" fill="{CHAR}"/><circle cx="-11" cy="-12.6" r="0.9" fill="{CHAR}"/>
</g>'''

def cat_curl(x, y, s=1.0, col=CAT):
    return f'''<g transform="translate({x} {y}) scale({s})">
<ellipse cx="0" cy="0" rx="22" ry="17" fill="{col}"/>
<path d="M-18 8 C-6 20 16 18 22 4" stroke="{col}" stroke-width="7" stroke-linecap="round" fill="none"/>
<path d="M-6 -16 q4 6 0 12 M4 -16 q4 6 0 12 M14 -10 q3 5 0 9" stroke="#C9722A" stroke-width="2" fill="none" stroke-linecap="round"/>
<circle cx="-12" cy="2" r="10" fill="{col}"/>
<path d="M-20 -4 L-21 -12 L-14 -7 Z M-8 -7 L-6 -14 L-3 -6 Z" fill="{col}"/>
<path d="M-16 3 q2 1.4 4 0 M-10 3 q2 1.4 4 0" stroke="{CHAR}" stroke-width="1" fill="none" stroke-linecap="round"/>
</g>'''

def animal_head(kind, x, y, s=1.0):
    k = {'bear': ('#9A6A4A', 'round'), 'rabbit': ('#F4F1EC', 'long'), 'fox': (ORANGE, 'point'), 'dog': ('#D9B98C', 'flop'), 'pigeon': ('#A9B2BA', 'bird')}[kind]
    col, ear = k
    p = [f'<g transform="translate({x} {y}) scale({s})">']
    if ear == 'round':
        p.append(f'<circle cx="-9" cy="-9" r="4.6" fill="{col}"/><circle cx="9" cy="-9" r="4.6" fill="{col}"/>')
    elif ear == 'long':
        p.append(f'<ellipse cx="-4.4" cy="-16" rx="3.4" ry="9" fill="{col}"/><ellipse cx="4.4" cy="-16" rx="3.4" ry="9" fill="{col}"/><ellipse cx="-4.4" cy="-16" rx="1.4" ry="6" fill="{PEACH}"/><ellipse cx="4.4" cy="-16" rx="1.4" ry="6" fill="{PEACH}"/>')
    elif ear == 'point':
        p.append(f'<path d="M-11 -4 L-9 -17 L-2 -9 Z M11 -4 L9 -17 L2 -9 Z" fill="{col}"/>')
    elif ear == 'flop':
        p.append(f'<ellipse cx="-11" cy="-1" rx="4.4" ry="8" fill="#9A6A4A" transform="rotate(16 -11 -1)"/><ellipse cx="11" cy="-1" rx="4.4" ry="8" fill="#9A6A4A" transform="rotate(-16 11 -1)"/>')
    if ear == 'bird':
        p.append(f'<ellipse cx="0" cy="0" rx="11" ry="12" fill="{col}"/><ellipse cx="0" cy="6" rx="8" ry="5" fill="#8FA7A0" opacity="0.7"/><path d="M-1.4 0 l1.4 -3 l1.4 3 z" fill="{ORANGE}" transform="translate(0 2)"/>')
    else:
        p.append(f'<circle cx="0" cy="0" r="11" fill="{col}"/>')
        if kind == 'fox':
            p.append(f'<path d="M-11 1 Q-5 2 0 9 Q5 2 11 1 Q9 10 0 11 Q-9 10 -11 1 Z" fill="{CREAM}"/>')
        if kind == 'bear':
            p.append(f'<ellipse cx="0" cy="4" rx="4.6" ry="3.4" fill="#D9BE98"/>')
    p.append(f'<circle cx="-3.6" cy="-1.5" r="1.2" fill="{CHAR}"/><circle cx="3.6" cy="-1.5" r="1.2" fill="{CHAR}"/>')
    if kind != 'pigeon':
        p.append(f'<ellipse cx="0" cy="2.6" rx="1.4" ry="1" fill="{CHAR}"/>')
    p.append('</g>')
    return ''.join(p)

def person(x, base, s=1.0, shirt=CREAM, apron=TEAL_D, hair=CHAR):
    return f'''<g transform="translate({x} {base}) scale({s})">
<rect x="-11" y="-30" width="22" height="30" rx="6" fill="{shirt}"/>
<rect x="-7" y="-24" width="14" height="24" rx="2" fill="{apron}"/>
<rect x="-3" y="-35" width="6" height="6" fill="#E8B994"/>
<circle cx="0" cy="-42" r="9" fill="#E8B994"/>
<path d="M-9.6 -42 C-10 -54 10 -54 9.6 -42 L7 -45 L2 -43 L-3 -45 L-7 -43 Z" fill="{hair}"/>
<circle cx="-3.2" cy="-41" r="0.9" fill="{CHAR}"/><circle cx="3.2" cy="-41" r="0.9" fill="{CHAR}"/>
</g>'''

def pigeon(x, y, s=1.0):
    return f'''<g transform="translate({x} {y}) scale({s})"><path d="M-10 -2 l-7 -2 l3 5 z" fill="#8C96A0"/><ellipse cx="0" cy="-4" rx="10" ry="7" fill="#A9B2BA"/><circle cx="8" cy="-11" r="4.6" fill="#A9B2BA"/><path d="M12 -11 l4 1 -4 1 z" fill="{ORANGE}"/><circle cx="9" cy="-12" r="0.8" fill="{CHAR}"/><path d="M5 -8 q3 3 0 6" stroke="#7FA79A" stroke-width="2" fill="none"/><path d="M-1 3 v2.4 M3 3 v2.4" stroke="{ORANGE}" stroke-width="1.2" stroke-linecap="round"/></g>'''

def wrap(inner, w=390, h=844, bg=BG):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
<defs>{DEFS}</defs><rect width="{w}" height="{h}" fill="{bg}"/>
<g filter="url(#hand)">{inner}</g>
<rect width="{w}" height="{h}" filter="url(#grain)" opacity="0.14" style="mix-blend-mode:multiply"/></svg>'''

def page(svg, w=390, h=844):
    return f'<!doctype html><html><head><meta charset="utf-8"><style>html,body{{margin:0;background:{BG}}}</style></head><body style="width:{w}px;height:{h}px">{svg}</body></html>'
