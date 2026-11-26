#!/usr/bin/env python3
"""Render the Sum 26 Round 4 news image (1024x1024, cream newspaper)."""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
CREAM = (247, 241, 227)
PAPER = (255, 253, 246)
INK = (20, 20, 20)
GREY = (90, 86, 76)
LINE = (201, 191, 168)
RED = (176, 30, 36)
BLACK = (15, 15, 15)
GREEN = (30, 107, 52)
BLUE = (31, 78, 121)
ORANGE = (180, 83, 9)

FDIR = "/usr/share/fonts/truetype/dejavu"
def font(name, size):
    return ImageFont.truetype(os.path.join(FDIR, name), size)

SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)

BADGE_FILL = {"CONFIRMED": GREEN, "REPORTED": BLUE, "CLAIM": RED,
              "OFFICIAL": BLACK, "ONGOING": ORANGE}

def wrap(text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if fnt.getlength(trial) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def fit_lines(text, fnt, max_w, max_lines):
    """Wrap text; shrink font until it fits max_lines (min size 7)."""
    size = fnt.size
    while size > 7:
        lines = wrap(text, fnt, max_w)
        if len(lines) <= max_lines:
            return lines, fnt
        size -= 1
        fnt = ImageFont.truetype(os.path.join(FDIR, fnt.path), size) \
            if hasattr(fnt, "path") else fnt
        # rebuild with same family
        fam = "DejaVuSerif-Bold.ttf" if "Serif-Bold" in str(getattr(fnt, "path", "")) else None
        break
    return wrap(text, fnt, max_w), fnt

def draw_badge(d, x, y, label):
    f = SANS_B(8)
    w = int(f.getlength(label)) + 10
    d.rounded_rectangle([x, y, x + w, y + 13], radius=2, fill=BADGE_FILL[label])
    d.text((x + 5, y + 2), label, font=f, fill=(255, 255, 255))
    return w

# ---------------- drawn scenes (flat-colour, one per card) ----------------
def scene_parade(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(23, 42, 74))
    for bx, bw, bh in [(0, 34, 44), (44, 26, 58), (78, 30, 38), (116, 28, 52),
                       (152, 30, 40), (190, 26, 56), (224, 30, 42), (262, 28, 50),
                       (296, 32, 36)]:
        d.rectangle([x + bx, y + h - bh, x + bx + bw, y + h], fill=(12, 24, 46))
        for wy in range(y + h - bh + 6, y + h - 4, 10):
            for wx in range(x + bx + 5, x + bx + bw - 4, 10):
                d.rectangle([wx, wy, wx + 4, wy + 5], fill=(255, 214, 90))
    d.ellipse([x + w // 2 - 52, y + 6, x + w // 2 + 52, y + 40], fill=(245, 245, 240))
    d.ellipse([x + w // 2 - 14, y + 24, x + w // 2 - 2, y + 34], fill=(176, 30, 36))
    d.ellipse([x + w // 2 + 4, y + 24, x + w // 2 + 16, y + 34], fill=(176, 30, 36))
    for rx in range(x + 8, x + w - 8, 26):
        d.line([rx, y + 4, rx - 8, y + 22], fill=(150, 170, 200), width=1)
    d.rectangle([x, y + h - 16, x + 168, y + h], fill=(176, 30, 36))
    d.text((x + 6, y + h - 14), "POSTPONED TO SATURDAY", font=SANS_B(9), fill=(255, 255, 255))
    d.ellipse([x + w - 34, y + h - 32, x + w - 6, y + h - 4], fill=(212, 175, 55))
    d.text((x + w - 29, y + h - 26), "100", font=SANS_B(10), fill=(20, 20, 20))

def scene_india(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(255, 243, 224))
    d.rectangle([x, y, x + w, y + h // 3], fill=(255, 153, 51))
    d.rectangle([x, y + 2 * h // 3, x + w, y + h], fill=(19, 136, 8))
    d.ellipse([x + w - 58, y + h // 2 - 16, x + w - 26, y + h // 2 + 16],
              outline=(0, 56, 147), width=2)
    for i in range(12):
        a = i * 30
        import math
        x1 = x + w - 42 + int(13 * math.cos(math.radians(a)))
        y1 = y + h // 2 + int(13 * math.sin(math.radians(a)))
        d.line([x + w - 42, y + h // 2, x1, y1], fill=(0, 56, 147), width=1)
    for i, cx in enumerate(range(x + 14, x + w - 78, 34)):
        d.rectangle([cx, y + h - 22, cx + 16, y + h - 8], fill=(240, 230, 210))
        d.ellipse([cx + 5, y + h - 30, cx + 11, y + h - 20], fill=(255, 180, 40))
    d.rectangle([x, y + 6, x + 74, y + 22], fill=(15, 15, 15))
    d.text((x + 6, y + 8), "18 YEARS", font=SANS_B(10), fill=(255, 255, 255))

def scene_chess(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(28, 52, 44))
    bs, ox, oy = 13, x + 12, y + 8
    for r in range(4):
        for c in range(4):
            col = (240, 235, 220) if (r + c) % 2 == 0 else (60, 60, 60)
            d.rectangle([ox + c * bs, oy + r * bs, ox + (c + 1) * bs, oy + (r + 1) * bs], fill=col)
    d.ellipse([ox + 1 * bs + 2, oy + 0 * bs + 2, ox + 2 * bs - 2, oy + 1 * bs - 2], fill=(20, 20, 20))
    d.ellipse([ox + 2 * bs + 2, oy + 3 * bs + 2, ox + 3 * bs - 2, oy + 4 * bs - 2], fill=(255, 255, 255))
    for i, cx in enumerate([x + 110, x + 218]):
        d.rectangle([cx, y + 10, cx + 92, y + 40], fill=(245, 245, 240))
        d.text((cx + 8, y + 13), "1:32", font=SANS_B(15), fill=(20, 20, 20))
    d.rectangle([x + 110, y + 48, x + 202, y + 64], fill=(176, 30, 36))
    d.text((x + 116, y + 50), "GAME 3", font=SANS_B(10), fill=(255, 255, 255))
    d.text((x + 208, y + 51), "GUKESH 1-1 SINDAROV", font=SANS_B(9), fill=(255, 255, 255))

def scene_bars(d, x, y, w, h, color=(176, 30, 36), label="14"):
    d.rectangle([x, y, x + w, y + h], fill=(232, 238, 245))
    for i, bh in enumerate([10, 16, 12, 22, 18, 26]):
        d.rectangle([x + 8 + i * 24, y + h - 4 - bh, x + 26 + i * 24, y + h - 4], fill=color)
    d.rectangle([x + w - 36, y + 2, x + w - 2, y + 18], fill=(255, 255, 255))
    d.text((x + w - 33, y + 3), label, font=SANS_B(13), fill=(20, 20, 20))

def scene_blast(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(52, 58, 74))
    for bx, bw, bh in [(0, 26, 18), (30, 22, 24), (56, 26, 15), (86, 24, 20), (114, 26, 16), (140, 20, 22)]:
        d.rectangle([x + bx, y + h - bh, x + bx + bw, y + h], fill=(24, 28, 40))
    cx, cy = x + w - 42, y + 14
    for dx, dy, r in [(0, 0, 9), (-8, 3, 6), (8, 3, 6), (0, -6, 6)]:
        d.ellipse([cx + dx - r, cy + dy - r, cx + dx + r, cy + dy + r], fill=(255, 140, 0))
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(255, 220, 80))

def scene_jets(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(210, 222, 235))
    d.rectangle([x, y + h - 8, x + w, y + h - 4], fill=(90, 90, 90))
    for jx, jy in [(20, 12), (70, 6), (115, 14)]:
        d.polygon([(x + jx, y + jy + 8), (x + jx + 26, y + jy + 4), (x + jx + 30, y + jy + 8),
                   (x + jx + 26, y + jy + 12)], fill=(60, 60, 70))
        d.polygon([(x + jx + 8, y + jy), (x + jx + 14, y + jy + 8), (x + jx + 10, y + jy + 10)], fill=(60, 60, 70))

def scene_talks(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 232, 214))
    d.rectangle([x + 10, y + 6, x + 46, y + 22], fill=(0, 102, 102))
    d.rectangle([x + 52, y + 6, x + 88, y + 22], fill=(200, 30, 30))
    d.rectangle([x + 94, y + 6, x + 130, y + 22], fill=(0, 60, 140))
    d.rectangle([x + 20, y + 24, x + w - 20, y + 28], fill=(120, 90, 50))
    d.rectangle([x + 26, y + 28, x + 30, y + h - 3], fill=(120, 90, 50))
    d.rectangle([x + w - 30, y + 28, x + w - 26, y + h - 3], fill=(120, 90, 50))

def scene_chart_down(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(245, 232, 232))
    pts = [(x + 6, y + 6), (x + 30, y + 10), (x + 54, y + 8), (x + 78, y + 16),
           (x + 102, y + 14), (x + 126, y + 24), (x + 150, y + 28)]
    d.line(pts, fill=(176, 30, 36), width=3)
    d.polygon([(x + 150, y + 28), (x + 140, y + 24), (x + 150, y + 20)], fill=(176, 30, 36))

def scene_chip(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 236, 226))
    d.rectangle([x + w // 2 - 16, y + 4, x + w // 2 + 16, y + h - 4], fill=(30, 60, 40))
    for px in range(x + w // 2 - 12, x + w // 2 + 13, 8):
        d.line([px, y + 2, px, y + 6], fill=(200, 170, 60), width=2)
        d.line([px, y + h - 6, px, y + h - 2], fill=(200, 170, 60), width=2)
    d.text((x + w // 2 - 13, y + h // 2 - 7), "NVDA", font=SANS_B(8), fill=(255, 255, 255))

def scene_growth(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 243, 232))
    for i, bh in enumerate([8, 12, 16, 20, 26]):
        d.rectangle([x + 10 + i * 28, y + h - 4 - bh, x + 30 + i * 28, y + h - 4], fill=(30, 107, 52))
    d.line([(x + 8, y + h - 8), (x + w - 8, y + 6)], fill=(30, 107, 52), width=3)
    d.polygon([(x + w - 8, y + 6), (x + w - 20, y + 6), (x + w - 10, y + 14)], fill=(30, 107, 52))

def scene_turkey(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(243, 236, 220))
    for cx in (x + 52, x + 108):
        d.ellipse([cx - 18, y + 10, cx + 18, y + 30], fill=(139, 90, 43))
        d.ellipse([cx - 5, y + 2, cx + 5, y + 12], fill=(120, 72, 30))
        d.ellipse([cx + 3, y + 6, cx + 7, y + 10], fill=(200, 60, 40))
    d.rectangle([x + 8, y + h - 6, x + w - 8, y + h - 3], fill=(120, 90, 50))

def scene_court(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(236, 232, 222))
    for cx in range(x + 18, x + w - 10, 26):
        d.rectangle([cx, y + 12, cx + 8, y + h - 6], fill=(120, 110, 90))
    d.polygon([(x + 6, y + 12), (x + w // 2, y + 2), (x + w - 6, y + 12)], fill=(90, 80, 60))
    d.rectangle([x + 6, y + h - 6, x + w - 6, y + h - 3], fill=(90, 80, 60))

def scene_eu(d, x, y, w, h):
    import math
    d.rectangle([x, y, x + w, y + h], fill=(0, 51, 153))
    cx, cy = x + w // 2, y + h // 2
    for i in range(12):
        a = math.radians(i * 30 - 90)
        sx, sy = cx + int(24 * math.cos(a)), cy + int(11 * math.sin(a))
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 204, 0))
    d.text((x + w - 46, y + 2), "EU 27", font=SANS_B(9), fill=(255, 255, 255))

def scene_riyadh(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(30, 30, 48))
    for bx, bw, bh in [(0, 22, 16), (26, 18, 22), (48, 20, 14), (72, 16, 24), (92, 18, 18), (114, 20, 12), (138, 18, 20)]:
        d.rectangle([x + bx, y + h - bh, x + bx + bw, y + h], fill=(70, 70, 95))
        for wy in range(y + h - bh + 4, y + h - 2, 6):
            d.rectangle([x + bx + 4, wy, x + bx + 7, wy + 3], fill=(255, 220, 120))
    d.arc([x + 10, y - 6, x + 70, y + 26], 200, 340, fill=(255, 255, 255), width=2)
    d.arc([x + 60, y - 2, x + 120, y + 30], 200, 340, fill=(255, 200, 80), width=2)
    d.ellipse([x + 130, y + 4, x + 136, y + 10], fill=(255, 120, 60))

def scene_taiwan(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 236, 245))
    d.rectangle([x + 8, y + 5, x + 44, y + 15], fill=(254, 0, 0))
    d.rectangle([x + 8, y + 17, x + 44, y + 27], fill=(255, 255, 255))
    d.rectangle([x + w - 52, y + 4, x + w - 8, y + h - 4], fill=(30, 60, 40))
    d.text((x + w - 49, y + h // 2 - 7), "15%", font=SANS_B(11), fill=(255, 255, 255))

# ---------------- story data (all verified first reported 26 Nov 2026) ----------------
HEROES = [
    dict(scene=scene_parade, badge="CONFIRMED", src="FOX WEATHER",
         head="Macy's 100th Thanksgiving parade put off to Saturday",
         deck="Nor'easter brings 60-70 mph gusts; balloons stay grounded past 34 mph. First weather delay in 100 years; NBC airs an encore of the 2025 parade."),
    dict(scene=scene_india, badge="CONFIRMED", src="PTI",
         head="India remembers 26/11, 18 years on",
         deck="Tributes for the 166 killed in Mumbai in 2008, as the nation also marks 77 years since its Constitution was adopted."),
    dict(scene=scene_chess, badge="CONFIRMED", src="FIDE",
         head="Gukesh v Sindarov: Game 3, scores level",
         deck="Two draws leave the Geneva title match 1-1. Sindarov has White today; first to 7.5 points takes the crown and $2.5m."),
]

MEDIUMS = [
    dict(scene=lambda d, x, y, w, h: scene_bars(d, x, y, w, h, (176, 30, 36), "14"),
         badge="CONFIRMED", src="REUTERS",
         head="US plans new tariffs on 14 partners",
         deck="New 20-40% maximum rates; struck deals cap them lower."),
    dict(scene=scene_blast, badge="CONFIRMED", src="REUTERS",
         head="Russian missiles hit Kyiv; mall struck",
         deck="Overnight barrage hits the capital as air defences work."),
    dict(scene=scene_jets, badge="REPORTED", src="REUTERS",
         head="Ukraine says it hit air base; 5 jets hurt",
         deck="Kyiv claims a strike on a Russian airfield damaged five jets."),
    dict(scene=scene_talks, badge="CONFIRMED", src="REUTERS",
         head="Abu Dhabi talks end; Russia holds line",
         deck="No breakthrough as Moscow sticks to its land claims."),
    dict(scene=scene_chart_down, badge="CONFIRMED", src="REUTERS",
         head="Stocks slide as tech sell-off deepens",
         deck="Chip shares lead the fall as AI-demand doubts spread across markets."),
    dict(scene=scene_chip, badge="REPORTED", src="REUTERS",
         head="S&P puts Nvidia rating on watch",
         deck="The chip giant's outlook is under review as shares slide."),
    dict(scene=scene_growth, badge="OFFICIAL", src="REUTERS",
         head="US growth revised sharply higher",
         deck="Growth estimate lifted as the economy beats forecasts."),
    dict(scene=scene_turkey, badge="OFFICIAL", src="REUTERS",
         head="Trump pardons turkeys Freedom, Feathers",
         deck="White House rite goes on as the parade waits out the storm."),
    dict(scene=scene_court, badge="CONFIRMED", src="REUTERS",
         head="Second judge blocks birthright order",
         deck="Another court halts the citizenship order; challenges mount."),
    dict(scene=scene_eu, badge="ONGOING", src="REUTERS",
         head="EU leaders meet on budget and Ukraine aid",
         deck="Brussels weighs a 45bn euro Ukraine loan and the budget."),
    dict(scene=scene_riyadh, badge="CONFIRMED", src="COALITION",
         head="Saudi defences down Houthi missiles over Riyadh",
         deck="Two ballistic missiles downed early Thursday, coalition says."),
    dict(scene=scene_taiwan, badge="CONFIRMED", src="REUTERS",
         head="Taiwan confident it keeps 15% US tariff",
         deck="Taipei says its earlier deal holds despite the new salvo."),
]

BRIEFS = [
    ("Murmansk", "Governor held in pre-trial detention in graft probe", "Reuters"),
    ("Washington", "CDC reports nine measles-related deaths in 2026", "Reuters"),
    ("Chicago", "Radar fault delays flights at O'Hare, FAA says", "Reuters"),
    ("Madrid", "Abrego Garcia lands in Spain after US departure deal", "Reuters"),
    ("Fort Hood", "Nidal Hasan seeks stay of execution for Fort Hood murders", "Reuters"),
    ("Nairobi", "Kenya cult leader Paul Mackenzie convicted of new charges", "Reuters"),
    ("Beijing", "How China got Nvidia AI chips despite US rules: explainer", "Reuters"),
    ("Warsaw", "Poland urges NATO to weigh downing missiles over Ukraine", "Reuters"),
    ("Spain", "Spain opens TikTok probe over child sex-abuse material", "AFP"),
    ("Madrid", "Sanchez defends housing and migration record on podcast", "EFE"),
    ("Jerusalem", "Israeli court urges dropping bribery charges vs Netanyahu", "Reuters"),
    ("Pyongyang", "North Korea orders Switzerland to shut Pyongyang office", "Reuters"),
    ("Lima", "Peru shuts dozens of ports as heavy swells batter coast", "Reuters"),
    ("Colombia", "Bomb in Colombian city wounds 23 as unrest spreads", "Reuters"),
    ("Seoul", "Bank of Korea raises rate to 3.25%, lifts 2027 growth outlook", "Reuters"),
    ("Bogota", "Two dozen hostages seized in Colombian supermarket", "AP"),
    ("Astana", "Kazakhstan seeks secret extradition of Chechen activist", "Lawyers"),
    ("Chennai", "Cabinet clears Rs 4,288-cr terminal at Kamarajar Port", "PTI"),
    ("New Delhi", "India adds 6,000 IIT seats for robotics, AI, space", "PTI"),
    ("New York", "US markets shut for Thanksgiving", "Reuters"),
    ("Japan", "India women beat Japan in hockey", "PTI"),
    ("South Africa", "South Africa sweep Test series", "AFP"),
    ("London", "Rugby captains gather for Nations finals", "Reuters"),
    ("France", "Frech's Mirroball win builds buzz for LA28 Paralympics", "Reuters"),
    ("Washington", "Trump to add sweeping tariffs, unfazed by midterms", "Reuters"),
    ("Quito", "Ecuador: US talks focus on reviewing operations", "Reuters"),
    ("Brasilia", "US plans surprise Brazil tariffs, 10% on aircraft", "Reuters"),
]

NUMBERS = [
    ("100", "YEARS OF MACY'S PARADE"),
    ("60-70", "MPH GUSTS FORECAST"),
    ("18", "YEARS SINCE 26/11"),
    ("1-1", "GUKESH-SINDAROV"),
    ("14", "TARIFF PARTNERS"),
    ("5", "PLANES 'DAMAGED'"),
]

TIMELINE = [
    ("00:00", "Thanksgiving in the US; Constitution Day in India"),
    ("02:30", "Abu Dhabi talks end; Russia holds land claims"),
    ("08:00", "India honours 166 victims of 26/11"),
    ("12:00", "Markets digest tech sell-off; Nvidia on watch"),
    ("14:00", "Game 3 in Geneva: Sindarov v Gukesh, 1-1"),
    ("23:00", "Thanksgiving evening: tables full, route empty"),
]

DATECHECK = [
    ("24 NOV", "Sooryavanshi's 204 off 53 (28 sixes) v UAE, Doha"),
    ("25 NOV", "Champions League MD5: Real Madrid 5-1 PSV; PSG 2-2 Roma"),
    ("25 NOV", "Bangladesh lifts garment wage 36% to 17,000 taka"),
    ("25 NOV", "Houthis claim Ras Tanura hit; coalition: 4 drones downed"),
    ("25 NOV", "Gukesh-Sindarov Game 2 ends in a 20-move draw"),
    ("25 NOV", "Cairo tanker fire kills 31 on Giza Ring Road"),
    ("25 NOV", "Shenzhou-24 docks; first Pakistani boards Tiangong"),
    ("25 NOV", "Solomon Islands signs security pact with Australia"),
    ("25 NOV", "Leaked data put Russian war dead near 500,000 (BBC)"),
    ("24 NOV", "Nigeria says 24 Kebbi schoolgirls freed"),
]

CONTINENTS = [
    [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-80, 73), (-75, 60), (-70, 45),
     (-80, 32), (-90, 20), (-97, 16), (-105, 20), (-120, 35), (-125, 48), (-150, 60)],
    [(-80, 10), (-60, 5), (-50, 0), (-40, -10), (-35, -20), (-50, -30), (-60, -40),
     (-70, -50), (-73, -35), (-75, -20), (-80, -5)],
    [(-17, 15), (-10, 30), (0, 35), (10, 37), (20, 32), (30, 31), (35, 28), (40, 15),
     (48, 11), (51, 10), (40, 0), (35, -15), (30, -25), (20, -35), (15, -30), (10, -15),
     (8, 4), (-8, 5)],
    [(-10, 36), (-9, 43), (-2, 48), (0, 51), (5, 53), (8, 57), (10, 59), (18, 56),
     (21, 55), (24, 59), (28, 60), (30, 70), (40, 68), (45, 60), (40, 50), (30, 46),
     (23, 40), (19, 42), (12, 44), (8, 44), (3, 42), (-2, 37)],
    [(40, 68), (60, 70), (80, 73), (100, 77), (120, 73), (140, 72), (160, 70), (178, 66),
     (170, 60), (160, 55), (150, 45), (140, 40), (130, 35), (127, 33), (122, 30), (120, 25),
     (110, 20), (105, 10), (100, 8), (95, 15), (90, 22), (85, 20), (80, 15), (75, 10),
     (72, 20), (65, 25), (58, 26), (52, 28), (48, 30), (43, 35), (40, 40)],
    [(113, -22), (114, -30), (115, -35), (125, -32), (130, -32), (135, -35), (140, -38),
     (145, -38), (150, -37), (153, -27), (150, -22), (146, -19), (142, -11), (136, -12),
     (132, -12), (126, -14), (122, -17), (118, -20)],
]
PINS = [  # (number, lon, lat)
    (1, -74, 41), (2, 72, 19), (3, 6, 46), (4, -77, 39), (5, 30, 50),
    (6, 34, 48), (7, 54, 24), (8, -73, 42), (9, -79, 37), (10, -75, 38),
    (11, -77, 41), (12, -73, 39), (13, 4, 51), (14, 47, 25), (15, 121, 25),
]

def main():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W - 1, H - 1], outline=LINE, width=2)

    # ---- masthead ----
    d.rectangle([0, 0, W, 56], fill=BLACK)
    d.text((14, 5), "THE WORLD IN ONE DAY", font=SERIF_B(27), fill=(255, 255, 255))
    d.text((14, 36), "THURSDAY 26 NOVEMBER 2026  ·  ALL STORIES REPORTED TODAY",
           font=SANS_B(10), fill=(220, 220, 220))
    for i, (num, lab) in enumerate([("42", "STORIES"), ("8", "REGIONS"), ("9", "SOURCES")]):
        bx = 724 + i * 98
        d.rectangle([bx, 6, bx + 92, 50], outline=(200, 200, 200), width=1)
        f = SERIF_B(17)
        d.text((bx + 46 - f.getlength(num) / 2, 9), num, font=f, fill=(255, 255, 255))
        f2 = SANS_B(7)
        d.text((bx + 46 - f2.getlength(lab) / 2, 33), lab, font=f2, fill=(200, 200, 200))

    # ---- ticker ----
    d.rectangle([0, 58, W, 76], fill=RED)
    t = "PARADE OFF  ·  INDIA REMEMBERS 26/11  ·  CHESS 1-1 IN GENEVA"
    f = SANS_B(12)
    d.text(((W - f.getlength(t)) / 2, 62), t, font=f, fill=(255, 255, 255))

    # ---- heroes ----
    hw = 328
    for i, hro in enumerate(HEROES):
        x = 12 + i * (hw + 8)
        y, ch = 80, 186
        d.rectangle([x, y, x + hw, y + ch], fill=PAPER, outline=LINE, width=1)
        hro["scene"](d, x + 1, y + 1, hw - 2, 72)
        bw = draw_badge(d, x + 8, y + 79, hro["badge"])
        f = SANS_B(8)
        d.text((x + hw - 8 - f.getlength("No. %d · %s" % (i + 1, hro["src"])), y + 80),
               "No. %d · %s" % (i + 1, hro["src"]), font=f, fill=GREY)
        hl = wrap(hro["head"], SERIF_B(16), hw - 16)
        yy = y + 98
        for ln in hl[:2]:
            d.text((x + 8, yy), ln, font=SERIF_B(16), fill=INK)
            yy += 18
        dl = wrap(hro["deck"], SANS(10), hw - 16)
        yy = y + 138
        for ln in dl[:3]:
            d.text((x + 8, yy), ln, font=SANS(10), fill=(50, 48, 44))
            yy += 12

    # ---- mediums ----
    mw, mh = 160, 116
    for i, med in enumerate(MEDIUMS):
        row, col = divmod(i, 6)
        x = 12 + col * (mw + 8)
        y = 272 + row * (mh + 8)
        d.rectangle([x, y, x + mw, y + mh], fill=PAPER, outline=LINE, width=1)
        med["scene"](d, x + 1, y + 1, mw - 2, 34)
        draw_badge(d, x + 6, y + 38, med["badge"])
        f = SANS_B(7)
        lab = "No. %d · %s" % (i + 4, med["src"])
        d.text((x + mw - 5 - f.getlength(lab), y + 40), lab, font=f, fill=GREY)
        hl = wrap(med["head"], SERIF_B(11), mw - 12)
        yy = y + 54
        for ln in hl[:3]:
            d.text((x + 6, yy), ln, font=SERIF_B(11), fill=INK)
            yy += 13
        dl = wrap(med["deck"], SANS(8), mw - 12)
        yy = y + 94
        for ln in dl[:2]:
            d.text((x + 6, yy), ln, font=SANS(8), fill=(50, 48, 44))
            yy += 10

    # ---- IN NUMBERS ----
    d.rectangle([12, 518, 1012, 556], fill=BLACK)
    for i, (num, lab) in enumerate(NUMBERS):
        cx = 12 + i * (1000 / 6) + (1000 / 6) / 2
        if i:
            d.line([12 + i * (1000 / 6), 522, 12 + i * (1000 / 6), 552], fill=(80, 80, 80), width=1)
        f = SERIF_B(17)
        d.text((cx - f.getlength(num) / 2, 522), num, font=f, fill=(250, 240, 210))
        f2 = SANS_B(7)
        d.text((cx - f2.getlength(lab) / 2, 543), lab, font=f2, fill=(200, 200, 200))

    # ---- UTC timeline ----
    d.text((12, 562), "THE DAY IN UTC", font=SANS_B(9), fill=INK)
    for i, (tm, txt) in enumerate(TIMELINE):
        x = 132 + i * 147
        f = SANS_B(9)
        d.text((x, 564), tm, font=f, fill=RED)
        tl = wrap(txt, SANS(8), 141)
        yy = 576
        for ln in tl[:2]:
            d.text((x, yy), ln, font=SANS(8), fill=INK)
            yy += 10
    d.line([12, 600, 1012, 600], fill=LINE, width=1)

    # ---- briefs ----
    d.text((12, 606), "THE BRIEFS — STORIES 16-42", font=SANS_B(11), fill=INK)
    d.text((1012 - SANS_B(8).getlength("CITY — HEADLINE — SOURCE"), 608),
           "CITY — HEADLINE — SOURCE", font=SANS_B(8), fill=GREY)
    left = BRIEFS[:15]
    right = BRIEFS[15:]
    for col_i, group in enumerate([left, right]):
        x0 = 12 if col_i == 0 else 516
        col_w = 496
        for j, (city, text, src) in enumerate(group):
            n = 16 + j + (0 if col_i == 0 else 15)
            y = 626 + j * 16
            fnum = SANS_B(9)
            d.text((x0, y), "%d." % n, font=fnum, fill=RED)
            nx = x0 + fnum.getlength("%d. " % n)
            line = "%s — %s" % (city, text)
            f = SANS(9)
            # shrink if needed so source still fits on the same line
            size = 9
            while size > 8 and f.getlength(line) + 8 + SANS_B(8).getlength(src) > col_w - (nx - x0):
                size -= 1
                f = SANS(size)
            d.text((nx, y), line, font=f, fill=INK)
            fs = SANS_B(8)
            d.text((x0 + col_w - fs.getlength(src), y + 1), src, font=fs, fill=GREY)

    # ---- world map (small panel, bottom of right briefs column) ----
    # Caption lives in its own header strip ABOVE the map drawing, so no
    # text ever overlaps the map. The map (continents + pins) is confined
    # to the strip below the header; pins keep their lon/lat positions.
    mx, my, mw2, mh2 = 516, 818, 496, 50
    hdr_h = 14
    map_y0 = my + hdr_h + 1          # 833: first row of the map area
    map_h = mh2 - hdr_h - 1          # 35: map area height
    d.rectangle([mx, my, mx + mw2, my + mh2], fill=(220, 232, 240), outline=LINE, width=1)
    d.rectangle([mx, my, mx + mw2, my + hdr_h], fill=(255, 255, 255))
    d.line([mx, my + hdr_h, mx + mw2, my + hdr_h], fill=LINE, width=1)
    d.text((mx + 4, my + 2), "WORLD MAP — PINS 1, 2, 3, 5, 7, 14, 15", font=SANS_B(8), fill=INK)
    for poly in CONTINENTS:
        pts = [(mx + (lon + 180) / 360 * mw2, map_y0 + (85 - lat) / 145 * map_h) for lon, lat in poly]
        d.polygon(pts, fill=(168, 178, 158))
    for num, lon, lat in [(1, -74, 41), (2, 72, 19), (3, 6, 46), (5, 30, 50),
                          (7, 54, 24), (14, 47, 25), (15, 121, 25)]:
        px = mx + (lon + 180) / 360 * mw2
        py = map_y0 + (85 - lat) / 145 * map_h
        d.ellipse([px - 5, py - 5, px + 5, py + 5], fill=RED, outline=(255, 255, 255), width=1)
        f = SANS_B(7)
        d.text((px - f.getlength(str(num)) / 2, py - 5), str(num), font=f, fill=(255, 255, 255))

    # Repaint the panel border LAST: the white header strip above is painted
    # over the panel's top edge and the top of its right edge, so the
    # outline must be redrawn on top for a complete frame on all four sides.
    d.rectangle([mx, my, mx + mw2, my + mh2], outline=LINE, width=1)

    # ---- DATE CHECK ----
    # Box geometry unchanged from R4 (same full-width rect, same spot);
    # colour scheme goes red -> black and every text line is centred
    # inside the box: the header across the whole box, each item line
    # centred inside its own half of the box.
    bx0, bx1, by0, by1 = 12, 1012, 874, 958
    d.rectangle([bx0, by0, bx1, by1], outline=(0, 0, 0), width=2,
                fill=(255, 255, 255))
    hf = SANS_B(11)
    ht = "DATE CHECK — NOT 26 NOVEMBER, EXCLUDED:"
    d.text(((bx0 + bx1 - hf.getlength(ht)) / 2, 880), ht, font=hf,
           fill=(0, 0, 0))
    for i, (dt, txt) in enumerate(DATECHECK):
        col = 0 if i < 5 else 1
        row = i if i < 5 else i - 5
        span = bx1 - bx0
        half_c = bx0 + span / 4 if col == 0 else bx0 + 3 * span / 4
        bf = SANS_B(8)
        tf = SANS(8)
        mark = "✕ " + dt
        w = bf.getlength(mark) + 4 + tf.getlength(txt)
        x = half_c - w / 2
        y = 898 + row * 12
        d.text((x, y), mark, font=bf, fill=(0, 0, 0))
        d.text((x + bf.getlength(mark) + 4, y), txt, font=tf,
               fill=(60, 55, 50))

    # ---- footer ----
    f = SANS_B(10)
    t = "Every story here happened or was first reported on Thursday 26 November 2026."
    d.text(((W - f.getlength(t)) / 2, 964), t, font=f, fill=INK)
    f = SANS(9)
    t = "Drawn by an AI agent for make.fun — news-image-20261126 · 42 stories, 8 regions, 9 sources"
    d.text(((W - f.getlength(t)) / 2, 980), t, font=f, fill=GREY)
    f = SANS(8)
    t = ("OFFICIAL = government or institution · CONFIRMED = wire or two sources · "
         "REPORTED = one named outlet · CLAIM = one side's account · "
         "Scenes are drawn illustrations, not photographs.")
    d.text(((W - f.getlength(t)) / 2, 995), t, font=f, fill=GREY)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, optimize=True)
    print("saved", out, img.size, os.path.getsize(out), "bytes")

if __name__ == "__main__":
    main()
