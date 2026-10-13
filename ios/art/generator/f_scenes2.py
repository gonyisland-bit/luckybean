from f_kit import *

def euro_cafe(x, base, w=174):
    p = []
    h_up, h_band, h_gr = 66, 18, 78
    top = base - h_gr - h_band - h_up
    # mansard roof + dormers + chimney
    p.append(f'<rect x="{x+w-34}" y="{top-44}" width="14" height="30" fill="{CHAR}"/>')
    p.append(f'<path d="M{x-6} {top} L{x+12} {top-34} L{x+w-12} {top-34} L{x+w+6} {top} Z" fill="{CHAR}"/><path d="M{x-6} {top} L{x+12} {top-34} L{x+w-12} {top-34} L{x+w+6} {top} Z" fill="url(#scallopW)" opacity="0.6"/>')
    for dx in (w * 0.3, w * 0.7):
        cx = x + dx
        p.append(f'<path d="M{cx-11} {top-4} V{top-22} L{cx} {top-32} L{cx+11} {top-22} V{top-4} Z" fill="{CREAM}"/><rect x="{cx-6}" y="{top-22}" width="12" height="15" fill="{LBLUE}"/>')
    p.append(f'<rect x="{x-6}" y="{top-3}" width="{w+12}" height="6" fill="{CREAM}"/>')
    # upper floor
    p.append(f'<rect x="{x}" y="{top+3}" width="{w}" height="{h_up-3}" fill="{PEACH}"/>')
    for i in range(4):
        wx = x + 14 + i * (w - 28 - 22) / 3
        p.append(f'<path d="M{wx} {top+52} V{top+24} A11 11 0 0 1 {wx+22} {top+24} V{top+52} Z" fill="{CREAM}"/><path d="M{wx+3} {top+50} V{top+25} A8 8 0 0 1 {wx+19} {top+25} V{top+50} Z" fill="#FBE3B0"/><rect x="{wx+10}" y="{top+17}" width="2" height="34" fill="{CREAM}"/>')
        p.append(f'<rect x="{wx-3}" y="{top+52}" width="28" height="7" rx="2" fill="{TEAL_D}"/>' + ''.join(f'<circle cx="{wx+1+k*6.5}" cy="{top+51}" r="2.6" fill="{[RED, MUST, CORAL, RED][k]}"/>' for k in range(4)))
    # band / sign
    p.append(f'<rect x="{x-4}" y="{top+h_up}" width="{w+8}" height="{h_band}" fill="{TEAL_D}"/><rect x="{x+w/2-48}" y="{top+h_up+2}" width="96" height="{h_band-4}" rx="3" fill="{MUST}"/>')
    # ground floor
    g0 = top + h_up + h_band
    p.append(f'<rect x="{x}" y="{g0}" width="{w}" height="{h_gr}" fill="{TEAL_D}"/>')
    pane_w = (w - 16 - 8) / 3
    for i in range(3):
        px = x + 8 + i * (pane_w + 4)
        p.append(f'<rect x="{px:.1f}" y="{g0+18}" width="{pane_w:.1f}" height="{h_gr-24}" fill="#FBE3B0"/>')
        if i == 1:
            p.append(f'<rect x="{px+pane_w/2-12:.1f}" y="{g0+26}" width="24" height="{h_gr-32}" fill="{TEAL}"/><rect x="{px+pane_w/2-8:.1f}" y="{g0+30}" width="16" height="22" fill="#FBE3B0"/><circle cx="{px+pane_w/2+7:.1f}" cy="{g0+58}" r="1.6" fill="{MUST}"/>')
        else:
            p.append(f'<rect x="{px:.1f}" y="{g0+44}" width="{pane_w:.1f}" height="3" fill="{BROWN}"/>')
            p.append(''.join(f'<rect x="{px+6+k*12:.1f}" y="{g0+37}" width="7" height="7" rx="1.5" fill="{[WHITE, CORAL, TEAL][k%3]}"/>' for k in range(int(pane_w // 13))))
            p.append(f'<rect x="{px+pane_w/2-0.8:.1f}" y="{g0+18}" width="1.6" height="10" fill="{CHAR}"/><path d="M{px+pane_w/2-7:.1f} {g0+33} q7 -8 14 0 z" fill="{MUST}"/>')
        p.append(f'<path d="M{px+4:.1f} {g0+22} l10 0 l-10 14 z" fill="#FFFFFF" opacity="0.55"/>')
    # awning (scalloped)
    p.append(f'<rect x="{x-6}" y="{g0}" width="{w+12}" height="14" fill="url(#tentStripe)"/>')
    p.append(''.join(f'<circle cx="{x-6+7+k*14:.1f}" cy="{g0+14}" r="7" fill="{CORAL if k%2==0 else CREAM}"/>' for k in range(int((w + 12) // 14))))
    return ''.join(p)

def a_frame(x, base, s=1.0):
    return (f'<g transform="translate({x} {base}) scale({s})"><path d="M-12 0 L-8 -36 M12 0 L8 -36" stroke="{BROWN}" stroke-width="2.6" stroke-linecap="round"/>'
            f'<rect x="-10" y="-38" width="20" height="28" rx="2" fill="{CHAR}"/><rect x="-6" y="-33" width="12" height="1.6" fill="{CREAM}"/><rect x="-6" y="-28" width="9" height="1.6" fill="{CREAM}"/><path d="M-4 -22 h7 v4 a3.5 3 0 0 1 -7 0 z" fill="{CREAM}"/></g>')

def bistro(x, base, umb=CORAL):
    return (f'<rect x="{x-1}" y="{base-34}" width="2" height="34" fill="{CHAR}"/><path d="M{x-20} {base-30} Q{x} {base-48} {x+20} {base-30} Z" fill="{umb}"/><path d="M{x-20} {base-30} Q{x} {base-48} {x+20} {base-30} Z" fill="url(#stripeV)"/>'
            f'<ellipse cx="{x}" cy="{base-12}" rx="11" ry="3" fill="{WHITE}"/><rect x="{x-1}" y="{base-12}" width="2" height="12" fill="{CHAR}"/>'
            f'<path d="M{x-17} {base} v-10 h5 M{x+17} {base} v-10 h-5" stroke="{CHAR}" stroke-width="1.6" fill="none"/>')

def gazebo(x, base, w=64):
    return (f'<path d="M{x-w/2-6} {base-50} L{x} {base-76} L{x+w/2+6} {base-50} Z" fill="{TEAL}"/><path d="M{x-w/2-6} {base-50} L{x} {base-76} L{x+w/2+6} {base-50} Z" fill="url(#stripeW)"/>'
            f'<rect x="{x-w/2-6}" y="{base-52}" width="{w+12}" height="6" fill="{CREAM}"/>'
            f'<rect x="{x-w/2}" y="{base-46}" width="4" height="46" fill="{WHITE}"/><rect x="{x+w/2-4}" y="{base-46}" width="4" height="46" fill="{WHITE}"/><rect x="{x-2}" y="{base-46}" width="4" height="46" fill="{WHITE}"/>'
            f'<rect x="{x-w/2-4}" y="{base-4}" width="{w+8}" height="6" rx="2" fill="{GREY_L}"/>')

def f1v2_home():
    p = []
    p.append(f'<clipPath id="mapclip"><rect x="10" y="110" width="370" height="602" rx="26"/></clipPath>')
    p.append(f'<rect x="10" y="110" width="370" height="602" rx="26" fill="{MAP}"/>')
    p.append('<g clip-path="url(#mapclip)">')
    # park patch
    p.append(f'<path d="M14 540 H276 V716 H14 Z" fill="#C9DDC9"/>')
    p.append(f'<path d="M40 716 C70 660 120 640 150 640 C190 640 230 670 276 660" stroke="{CREAM}" stroke-width="10" fill="none" stroke-linecap="round"/>')
    p.append(f'<ellipse cx="70" cy="600" rx="34" ry="14" fill="{LBLUE}"/><ellipse cx="70" cy="600" rx="26" ry="9" fill="#BCD9DC"/>')
    # roads
    for d in ('M0 520 H400', 'M100 100 V520', 'M100 262 H400', 'M286 520 V720'):
        p.append(f'<path d="{d}" stroke="{WHITE}" stroke-width="20" fill="none" stroke-linecap="round"/>')
    p.append(''.join(f'<rect x="{x}" y="518" width="10" height="3" fill="{GREY_L}"/>' for x in range(10, 390, 24)))
    p.append(f'<rect x="110" y="496" width="270" height="14" fill="{CREAM}"/>')
    # railway + train
    p.append(f'<rect x="296" y="694" width="90" height="2" fill="{GREY}"/><rect x="296" y="702" width="90" height="2" fill="{GREY}"/>' + ''.join(f'<rect x="{x}" y="691" width="3" height="16" fill="{GREY}"/>' for x in range(298, 390, 10)))
    p.append(f'<rect x="318" y="678" width="40" height="20" rx="3" fill="{TEAL}"/><rect x="322" y="682" width="9" height="8" fill="{CREAM}"/><rect x="335" y="682" width="9" height="8" fill="{CREAM}"/><rect x="348" y="682" width="7" height="8" fill="{CREAM}"/><circle cx="326" cy="699" r="3.4" fill="{CHAR}"/><circle cx="350" cy="699" r="3.4" fill="{CHAR}"/>')
    # hatch
    for (hx, hy) in ((50, 470), (200, 160), (350, 190), (330, 470), (200, 600), (120, 690), (40, 680)):
        p.append(hatch(hx, hy))
    # TL: regulars' house
    p.append(house(24, 330, 56, 150, TEAL, CHAR, roof_h=26, cols=2, rows=4, door=MUST, chimney=True))
    p.append(tree(30, 420, 10) + pine(70, 440, 16, 38) + tree(36, 500, 9, TEAL_D) + pine(80, 236, 12, 30))
    # TR: records hall
    p.append(house(276, 244, 78, 90, GREY_L, CHAR, roof_h=28, cols=3, rows=2, door=ORANGE, arch=True))
    p.append(f'<circle cx="315" cy="146" r="9" fill="{WHITE}"/><path d="M315 146 v-5 M315 146 l3.4 2" stroke="{CHAR}" stroke-width="1.4" stroke-linecap="round"/>')
    p.append(tree(130, 244, 10) + pine(170, 248, 14, 34) + tree(214, 244, 11, TEAL_D) + tree(250, 248, 8) + tree(370, 244, 9))
    p.append(car(150, 268, MUST, kind='taxi') + car(316, 268, TEAL_D, w=30, flip=True))
    # CAFE
    p.append(euro_cafe(124, 498, 180))
    p.append(a_frame(318, 508, 1.0))
    p.append(bistro(350, 506, CORAL))
    p.append(tree(118, 498, 8) + pine(370, 470, 10, 26))
    p.append(cat_walk(86, 508, 0.8))
    p.append(car(30, 528, ORANGE, w=46, kind='bus') + car(200, 528, CORAL, w=32))
    # park content
    p.append(gazebo(170, 650, 70))
    p.append(f'<rect x="196" y="620" width="16" height="10" fill="{KRAFT}"/>')
    p.append(tree(30, 574, 11) + tree(240, 590, 12, TEAL_D) + pine(120, 590, 16, 40) + tree(254, 700, 10) + pine(26, 700, 14, 34) + tree(214, 712, 9))
    p.append(f'<rect x="96" y="690" width="34" height="5" rx="2" fill="{BROWN}"/><path d="M100 695 v8 M126 695 v8" stroke="{CHAR}" stroke-width="2"/>')
    p.append(pigeon(110, 686, 0.9))
    p.append(''.join(f'<circle cx="{x}" cy="{y}" r="2.6" fill="{c}"/>' for x, y, c in ((60, 640, RED), (66, 646, MUST), (230, 640, CORAL), (236, 634, RED), (150, 702, MUST), (44, 560, CORAL))))
    # station / map stop
    p.append(house(302, 640, 70, 58, PEACH, ORANGE, roof_h=24, cols=2, rows=1, door=TEAL_D, tex='scallop'))
    p.append(f'<rect x="300" y="548" width="3" height="40" fill="{CHAR}"/><rect x="290" y="540" width="40" height="26" rx="3" fill="{WHITE}"/><path d="M296 560 l8 -10 l8 6 l8 -8 l6 4" stroke="{TEAL}" stroke-width="2" fill="none" stroke-linecap="round"/><circle cx="318" cy="552" r="2.4" fill="{RED}"/>')
    p.append(tree(372, 600, 9))
    p.append('</g>')
    # bottom bar
    p.append(f'<rect x="10" y="724" width="370" height="106" rx="24" fill="{WHITE}"/>')
    for i, (k, bg) in enumerate((('bear', TEAL_XL), ('rabbit', PEACH), ('fox', MUST_L), ('dog', LBLUE), ('pigeon', GREY_L))):
        x = 44 + i * 40
        p.append(f'<circle cx="{x}" cy="786" r="17" fill="{bg}"/>' + animal_head(k, x, 788, 1.0))
    p.append(f'<circle cx="244" cy="786" r="17" fill="none" stroke="{GREY}" stroke-width="1.6" stroke-dasharray="3 3"/><path d="M244 780 v12 M238 786 h12" stroke="{GREY}" stroke-width="1.8" stroke-linecap="round"/>')
    return ''.join(p)

# ---------- cafe interior: game select ----------
def f1_cafe():
    p = []
    p.append(f'<rect width="390" height="560" fill="{PEACH}"/>')
    # big arched windows showing the street
    for i, wx in enumerate((22, 142, 262)):
        p.append(f'<path d="M{wx} 330 V150 A53 53 0 0 1 {wx+106} 150 V330 Z" fill="{CREAM}"/>')
        p.append(f'<path d="M{wx+6} 324 V152 A47 47 0 0 1 {wx+100} 152 V324 Z" fill="{LBLUE}"/>')
        p.append(f'<rect x="{wx+6}" y="282" width="94" height="42" fill="{MAP}"/><rect x="{wx+6}" y="300" width="94" height="10" fill="{WHITE}"/>')
        p.append([house(wx + 14, 282, 30, 46, MUST, CHAR, roof_h=12, cols=1, rows=2) + tree(wx + 70, 282, 10) + car(wx + 50, 308, ORANGE, w=28),
                  house(wx + 12, 282, 28, 56, CORAL, TEAL_D, roof_h=12, cols=1, rows=2) + house(wx + 48, 282, 34, 38, TEAL, CHAR, roof_h=14, cols=2, rows=1) + pigeon(wx + 80, 300, 0.8),
                  pine(wx + 22, 282, 18, 44) + house(wx + 44, 282, 40, 44, GREY_L, CHAR, roof_h=14, cols=2, rows=1) + car(wx + 14, 308, TEAL_D, w=28, flip=True)][i])
        p.append(f'<rect x="{wx+51}" y="104" width="4" height="220" fill="{CREAM}"/><rect x="{wx+6}" y="214" width="94" height="4" fill="{CREAM}"/>')
        p.append(f'<path d="M{wx+12} 160 l14 0 l-14 22 z" fill="#FFFFFF" opacity="0.5"/>')
    # roulette wheel on the wall between windows (decor = game)
    p.append(f'<rect x="0" y="330" width="390" height="10" fill="{CREAM}"/>')
    # pendant lamps
    for lx in (95, 215, 335):
        p.append(f'<rect x="{lx-1}" y="0" width="2" height="62" fill="{CHAR}"/><path d="M{lx-16} 80 Q{lx} 52 {lx+16} 80 Z" fill="{TEAL_D}"/><ellipse cx="{lx}" cy="104" rx="60" ry="40" fill="url(#glow)" opacity="0.5"/>')
    # floor
    p.append(f'<rect x="0" y="420" width="390" height="430" fill="url(#planksF)"/>')
    # counter (left) with espresso machine + barista
    p.append(person(70, 400, 1.35))
    p.append(f'<rect x="12" y="398" width="150" height="8" fill="{KRAFT}"/><rect x="16" y="406" width="142" height="70" fill="{TEAL}"/><rect x="16" y="406" width="142" height="70" fill="url(#dotsW)" opacity="0.5"/>')
    p.append(f'<rect x="104" y="358" width="50" height="40" rx="4" fill="{MUST}"/><rect x="100" y="352" width="58" height="8" rx="3" fill="{CHAR}"/><rect x="112" y="378" width="12" height="8" fill="{CHAR}"/><rect x="134" y="378" width="12" height="8" fill="{CHAR}"/><circle cx="129" cy="368" r="4" fill="{CREAM}"/>')
    p.append(f'<path d="M22 398 h14 v-8 a7 6 0 0 0 -14 0 z" fill="{WHITE}"/>')
    # roulette game table (right)
    p.append(f'<ellipse cx="300" cy="470" rx="62" ry="13" fill="{KRAFT}"/><rect x="295" y="474" width="10" height="44" fill="{BROWN}"/><rect x="275" y="514" width="50" height="5" fill="{BROWN}"/>')
    cx, cy = 300, 412
    p.append(f'<rect x="297" y="440" width="6" height="30" fill="{CHAR}"/><circle cx="{cx}" cy="{cy}" r="36" fill="{CREAM}"/>')
    for i, c in enumerate((TEAL, MUST, CORAL, ORANGE, LBLUE)):
        a0 = math.radians(-90 - 36 + i * 72); a1 = math.radians(-90 + 36 + i * 72)
        p.append(f'<path d="M{cx} {cy} L{cx+31*math.cos(a0):.1f} {cy+31*math.sin(a0):.1f} A31 31 0 0 1 {cx+31*math.cos(a1):.1f} {cy+31*math.sin(a1):.1f} Z" fill="{c}"/>')
    p.append(f'<circle cx="{cx}" cy="{cy}" r="7" fill="{CHAR}"/><path d="M{cx-5} {cy-44} h10 l-5 9 z" fill="{RED}"/>')
    # cup tray on small table (center front)
    p.append(f'<ellipse cx="196" cy="528" rx="56" ry="12" fill="{WHITE}"/><rect x="192" y="532" width="8" height="30" fill="{CHAR}"/>')
    for k, (c, dx) in enumerate(((TEAL, -34), (MUST, -12), (CORAL, 12), (ORANGE, 34))):
        p.append(f'<path d="M{196+dx-9} 526 L{196+dx-6} 506 L{196+dx+6} 506 L{196+dx+9} 526 Z" fill="{c}"/>')
    # boxes stack (front-left) with cat ears
    p.append(f'<rect x="26" y="500" width="54" height="44" fill="url(#kraftLines)"/><rect x="50" y="500" width="8" height="44" fill="#E7D3AE" opacity="0.7"/><rect x="36" y="462" width="40" height="38" fill="url(#kraftLines)"/><rect x="53" y="462" width="7" height="38" fill="#E7D3AE" opacity="0.7"/>')
    p.append(f'<path d="M44 462 L46 452 L52 460 Z M68 462 L66 452 L60 460 Z" fill="{CAT}"/><ellipse cx="56" cy="462" rx="11" ry="5" fill="{CAT}"/><circle cx="52" cy="460" r="1.2" fill="{CHAR}"/><circle cx="60" cy="460" r="1.2" fill="{CHAR}"/>')
    # bell (paw-shake) on counter
    p.append(f'<ellipse cx="48" cy="398" rx="10" ry="3" fill="{CHAR}"/><path d="M40 397 Q48 380 56 397 Z" fill="{MUST}"/><circle cx="48" cy="383" r="2" fill="{CHAR}"/>')
    return ''.join(p)

# ---------- park lounge ----------
def f1_park():
    p = []
    p.append(f'<rect width="390" height="560" fill="{LBLUE}"/>')
    p.append(f'<ellipse cx="80" cy="120" rx="40" ry="13" fill="{WHITE}"/><ellipse cx="104" cy="112" rx="26" ry="13" fill="{WHITE}"/><ellipse cx="300" cy="90" rx="32" ry="11" fill="{WHITE}"/>')
    p.append(f'<g opacity="0.5">' + house(10, 300, 40, 70, CORAL, CHAR, roof_h=18, cols=1, rows=2) + house(56, 300, 34, 50, MUST, CHAR, roof_h=14, cols=1, rows=1) + house(300, 300, 44, 80, GREY_L, CHAR, roof_h=18, cols=2, rows=2) + house(348, 300, 36, 56, TEAL, CHAR, roof_h=14, cols=1, rows=2) + '</g>')
    p.append(f'<path d="M0 300 C80 270 160 290 220 280 C290 268 340 285 390 276 V560 H0 Z" fill="#C9DDC9"/>')
    p.append(f'<path d="M0 340 C100 320 200 345 390 320 V560 H0 Z" fill="#B5D2B6"/>')
    for (hx, hy) in ((60, 380), (300, 370), (190, 520), (340, 500), (40, 520)):
        p.append(hatch(hx, hy, '#8FBF95'))
    p.append(f'<path d="M150 560 C170 470 210 440 220 400" stroke="{CREAM}" stroke-width="22" fill="none" stroke-linecap="round"/>')
    p.append(tree(40, 330, 16) + pine(352, 330, 22, 56) + tree(310, 340, 13, TEAL_D) + pine(90, 330, 18, 44))
    # fortune kiosk (left)
    p.append(f'<rect x="34" y="400" width="80" height="60" fill="{CREAM}"/><rect x="30" y="392" width="88" height="10" fill="{ORANGE}"/>')
    p.append(f'<path d="M26 392 L74 360 L122 392 Z" fill="url(#tentStripe)"/><rect x="44" y="414" width="60" height="30" fill="#FBE3B0"/>')
    p.append(f'<ellipse cx="74" cy="434" rx="14" ry="5" fill="{WHITE}"/><path d="M64 432 h20 v-6 a10 9 0 0 0 -20 0 z" fill="{WHITE}"/><path d="M70 422 q-3 -5 0 -9 M78 422 q-3 -5 0 -9" stroke="{TEAL}" stroke-width="1.6" fill="none" stroke-linecap="round"/>')
    p.append(f'<circle cx="74" cy="376" r="5" fill="{MUST}"/>')
    # coffee encyclopedia mini library (center back)
    p.append(f'<rect x="186" y="316" width="4" height="70" fill="{BROWN}"/><rect x="164" y="300" width="48" height="42" fill="{TEAL_D}"/><path d="M160 300 L188 284 L216 300 Z" fill="{CHAR}"/>')
    p.append(f'<rect x="168" y="304" width="40" height="34" fill="{CREAM}"/>' + ''.join(f'<rect x="{170+k*7}" y="{308 if k%2 else 311}" width="5" height="{11 if k%2 else 8}" fill="{[CORAL, MUST, TEAL, ORANGE, BROWN][k]}"/>' for k in range(5)) + ''.join(f'<rect x="{170+k*9}" y="324" width="7" height="11" fill="{[KRAFT, TEAL, MUST, CORAL][k]}"/>' for k in range(4)))
    # sound bench (right) with radio + cat
    p.append(f'<rect x="262" y="438" width="100" height="8" rx="3" fill="{BROWN}"/><rect x="262" y="420" width="100" height="6" rx="3" fill="{BROWN}"/><path d="M270 446 v20 M354 446 v20" stroke="{CHAR}" stroke-width="3"/>')
    p.append(f'<rect x="270" y="420" width="34" height="18" rx="4" fill="{CORAL}"/><circle cx="279" cy="429" r="5" fill="{CHAR}"/><rect x="288" y="424" width="12" height="3" fill="{CREAM}"/><rect x="282" y="412" width="1.6" height="9" fill="{CHAR}"/>')
    p.append(f'<path d="M310 410 q4 -6 8 0 M318 402 q4 -6 8 0" stroke="{TEAL_D}" stroke-width="1.8" fill="none" stroke-linecap="round"/><circle cx="312" cy="406" r="2" fill="{TEAL_D}"/><circle cx="326" cy="398" r="2" fill="{TEAL_D}"/>')
    p.append(cat_curl(338, 428, 0.85))
    p.append(pigeon(204, 470, 1.2) + pigeon(236, 486, 1.0))
    p.append(''.join(f'<circle cx="{x}" cy="{y}" r="3" fill="{c}"/>' for x, y, c in ((130, 480, RED), (138, 486, MUST), (250, 400, CORAL), (40, 480, MUST), (370, 470, RED))))
    return ''.join(p)

if __name__ == '__main__':
    for n, f in (('F1v2_home', f1v2_home), ('F1_cafe', f1_cafe), ('F1_park', f1_park)):
        open(f'{OUT}/{n}.html', 'w').write(page(wrap(f())))
    print('ok')
