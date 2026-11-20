#!/usr/bin/env python3
"""Draw the Friday 20 November 2026 front page, one 1024x1024 PNG.

Everything is fixed in this file: no network, no clock, no random
numbers, no reading of the system time. Running it twice writes the
same bytes. It uses PIL and the DejaVu fonts shipped on this machine.
Run: python3 gen.py  ->  writes entry.png beside this file.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024
PAPER = (250, 246, 235)
INK = (22, 22, 26)
RED = (178, 34, 28)
DARKRED = (140, 24, 20)
GREY = (110, 108, 100)
SEA = (198, 222, 232)
LAND = (232, 222, 188)
LANDLINE = (170, 158, 120)
BOX = (255, 255, 255)
TICK = (18, 32, 48)

FONTDIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONTDIR, name), size)


F_TITLE = font("DejaVuSerif-Bold.ttf", 46)
F_DATE = font("DejaVuSans-Bold.ttf", 19)
F_LEAD = font("DejaVuSans-Bold.ttf", 16)
F_MAPHEAD = font("DejaVuSans-Bold.ttf", 15)
F_STORY = font("DejaVuSans.ttf", 12)
F_NUM = font("DejaVuSans-Bold.ttf", 11)
F_TICK = font("DejaVuSans-Bold.ttf", 13)
F_BRIEF = font("DejaVuSans.ttf", 13)
F_DOT = font("DejaVuSans-Bold.ttf", 10)

LEADS = [
    ("L1", "Trump, Xi and Putin hold their first three-way summit in "
           "Shenzhen and issue a joint peace declaration after about 70 "
           "minutes, with no breakthrough on Ukraine, Iran or nuclear arms."),
    ("L2", "The International Court of Justice rules 9-6 that Myanmar "
           "committed genocide against the Rohingya, the court's first "
           "such finding against a state."),
    ("L3", "US stocks fall for a fifth straight day: the S&P 500 loses "
           "2.02% and the Nasdaq 2.25%, while Japan's Nikkei drops 5.1% "
           "after Anthropic's Nasdaq debut."),
]

# num, lon, lat, section, headline
# Sections are kept as data (and used in stories.md); the columns
# print number + headline only, because this edition's wire order
# interleaves regions and section headers would overflow the columns.
STORIES = [
    (1, 96, 21, "ASIA", "ICJ: Myanmar committed genocide"),
    (2, 114, 22, "ASIA", "Trump, Xi, Putin meet in Shenzhen"),
    (3, -74, 40, "NORTH AMERICA", "US stocks fall for fifth straight day"),
    (4, -122, 37, "NORTH AMERICA", "Anthropic closes 17% above IPO price"),
    (5, 47, 25, "MIDDLE EAST", "Houthi missile damages Riyadh tower"),
    (6, 44, 27, "MIDDLE EAST", "Saudi intercepts missile and five drones"),
    (7, 34, 45, "EUROPE", "Ukraine hits Kerch Bridge a third time"),
    (8, 30, 50, "EUROPE", "Russia strikes Kyiv overnight; six killed"),
    (9, 0, 51, "EUROPE", "UK pledges 1,000+ drones for Ukraine"),
    (10, -80, 26, "NORTH AMERICA", "GTA 6 launch tops $2.3 billion"),
    (11, -77, 39, "NORTH AMERICA", "IMF: global debt nearing 100% of GDP"),
    (12, 12, 42, "EUROPE", "Italy fines Meta 805 million euros"),
    (13, -87, 41, "NORTH AMERICA", "FAA ground stop strands 1.5m travelers"),
    (14, 37, 0, "AFRICA", "Kenya discharges last Ebola patient"),
    (15, -84, 39, "NORTH AMERICA", "US Senate passes energy bill 62-33"),
    (16, -89, 14, "NORTH AMERICA", "Bukele to run for third term"),
    (17, 25, -5, "AFRICA", "COP31: Africa seeks tripled climate cash"),
    (18, 2, 49, "EUROPE", "France deploys 70,000 police for protests"),
    (19, 166, -22, "OCEANIA", "5.6 quake strikes near New Caledonia"),
    (20, 19, 52, "EUROPE", "Poland probes unknown objects in the sky"),
    (21, 4, 51, "EUROPE", "EU summons Russian envoy over Kyiv strikes"),
    (22, -75, 40, "NORTH AMERICA", "Senate rejects Iran war-powers bid 51-48"),
    (23, -82, 39, "NORTH AMERICA", "Trump pardons Pete Rose posthumously"),
    (24, 150, -34, "OCEANIA", "US sanctions Comancheros and 'Ndrangheta"),
    (25, -17, 15, "AFRICA", "Senegal boat capsizing kills four"),
    (26, 34, 31, "MIDDLE EAST", "Gaza rescue crews respond on foot"),
    (27, 116, 40, "ASIA", "China-linked spies hit VMware zero-day"),
    (28, -95, 29, "NORTH AMERICA", "Zero-days mined crypto on 21 servers"),
    (29, 5, 50, "EUROPE", "IEA: AI data centers may push emissions up"),
    (30, -79, 37, "NORTH AMERICA", "Virginia exits Trump school tax plan"),
    (31, -87, 36, "NORTH AMERICA", "Ella Langley sweeps the CMA Awards"),
    (32, 56, 26, "MIDDLE EAST", "Tanker catches fire after Hormuz mine hit"),
    (33, 9, 44, "EUROPE", "Genoa airport halts flights over drones"),
    (34, 34, -14, "AFRICA", "Malawi fuel crisis sparks violence"),
    (35, -58, -35, "SOUTH AMERICA", "Argentina OKs permanent disability rules"),
    (36, 77, 21, "ASIA", "India eases vessel-age limits for fleet"),
]

TICKER = (
    "S&P 500 7,175.83 -2.02%   |   Nasdaq 23,879.20 -2.25%   |   "
    "Brent $89.05 -0.44%   |   Bitcoin $61,709 -0.32%   |   VIX 28.44 +15.8%"
)
BRIEFS = [
    "Anthropic's Nasdaq debut: shares close 17% above the $83 IPO price.",
    "GTA 6 launch tops $2.3 billion in sales in its first days.",
    "COP31: African nations seek tripled climate finance.",
    "FAA ground stop strands 1.5 million travelers across the US.",
]

CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 68), (-95, 69), (-85, 66),
     (-75, 62), (-65, 60), (-55, 52), (-60, 45), (-70, 42), (-75, 35),
     (-80, 32), (-85, 30), (-90, 21), (-95, 19), (-100, 22), (-105, 20),
     (-110, 23), (-115, 29), (-120, 34), (-125, 40), (-130, 48),
     (-140, 58), (-155, 58), (-165, 60)],
    [(-80, 10), (-75, 5), (-70, 0), (-65, -5), (-60, -10), (-55, -15),
     (-50, -20), (-45, -25), (-40, -20), (-35, -10), (-40, -5), (-45, 0),
     (-50, 5), (-55, 5), (-60, 8), (-70, 10), (-78, 5)],
    [(-10, 50), (-5, 55), (0, 58), (5, 55), (10, 57), (15, 55), (20, 60),
     (25, 60), (30, 65), (35, 68), (40, 60), (35, 55), (30, 50), (25, 45),
     (20, 40), (15, 38), (10, 40), (5, 38), (0, 36), (-5, 36), (-10, 40)],
    [(-17, 15), (-10, 30), (0, 35), (10, 37), (20, 32), (30, 31), (35, 28),
     (32, 20), (40, 15), (43, 11), (48, 10), (51, 12), (45, 5), (40, 0),
     (35, -10), (30, -20), (25, -30), (20, -35), (15, -30), (12, -18),
     (10, -5), (8, 5), (0, 5), (-8, 5), (-15, 10)],
    [(40, 70), (60, 70), (80, 73), (100, 75), (120, 73), (140, 72),
     (160, 70), (170, 66), (162, 60), (158, 52), (150, 45), (142, 40),
     (135, 35), (130, 33), (127, 35), (122, 38), (120, 32), (115, 25),
     (110, 20), (105, 10), (100, 8), (95, 15), (90, 22), (85, 20),
     (80, 15), (75, 10), (70, 20), (65, 25), (60, 25), (55, 26),
     (50, 30), (45, 35), (40, 40), (38, 45), (35, 50)],
    [(113, -22), (120, -15), (130, -12), (135, -15), (140, -18), (145, -15),
     (150, -22), (153, -28), (150, -37), (145, -38), (140, -38),
     (135, -35), (130, -32), (125, -33), (120, -35), (115, -32), (113, -25)],
]


def wrap(draw, text, fnt, width, max_lines=2):
    words = text.split()
    lines = []
    cur = ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
            if len(lines) == max_lines:
                break
    if cur and len(lines) < max_lines:
        lines.append(cur)
    return lines


def lonlat_to_xy(lon, lat, box):
    x0, y0, x1, y1 = box
    x = x0 + (lon + 180.0) / 360.0 * (x1 - x0)
    y = y0 + (90.0 - lat) / 180.0 * (y1 - y0)
    return (x, y)


def draw_page():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # outer frame
    d.rectangle([8, 8, W - 9, H - 9], outline=INK, width=2)
    # masthead
    title = "THE WORLD IN ONE PAGE"
    tw = d.textlength(title, font=F_TITLE)
    d.text(((W - tw) / 2, 20), title, font=F_TITLE, fill=INK)
    date = "FRIDAY 20 NOVEMBER 2026  —  36 STORIES, 6 CONTINENTS"
    dw = d.textlength(date, font=F_DATE)
    d.text(((W - dw) / 2, 76), date, font=F_DATE, fill=RED)
    d.line([24, 104, W - 24, 104], fill=INK, width=2)
    # lead banner: three leads, each wrapped over up to two lines
    d.rectangle([24, 112, W - 24, 282], fill=BOX, outline=RED, width=2)
    d.text((36, 118), "THE DAY IN THREE", font=F_MAPHEAD, fill=RED)
    y = 142
    for tag, text in LEADS:
        d.ellipse([36, y + 2, 58, y + 24], fill=RED)
        tw2 = d.textlength(tag, font=F_NUM)
        d.text((47 - tw2 / 2, y + 6), tag, font=F_NUM, fill=(255, 255, 255))
        lines = wrap(d, text, F_LEAD, W - 24 - 78, max_lines=2)
        for li, line in enumerate(lines):
            d.text((70, y + li * 19), line, font=F_LEAD, fill=INK)
        y += 44
    # map box: land drawn in a true 2 to 1 box, centred, so shapes
    # are not squashed flat. Sea fills the whole box around it.
    mapbox = (24, 290, W - 24, 560)
    d.rectangle(mapbox, fill=SEA, outline=INK, width=2)
    d.text((36, 298), "WHERE IT HAPPENED", font=F_MAPHEAD, fill=INK)
    inner = (252, 300, 772, 560)
    for poly in CONTINENTS:
        pts = [lonlat_to_xy(lon, lat, inner) for lon, lat in poly]
        d.polygon(pts, fill=LAND, outline=LANDLINE)
    for num, lon, lat, _sect, _head in STORIES:
        x, y = lonlat_to_xy(lon, lat, inner)
        r = 9
        d.ellipse([x - r, y - r, x + r, y + r], fill=RED, outline=(255, 255, 255), width=1)
        s = str(num)
        sw = d.textlength(s, font=F_DOT)
        d.text((x - sw / 2, y - 6), s, font=F_DOT, fill=(255, 255, 255))
    # story columns, 12 stories each, number + headline only
    for ci, (cx, cw) in enumerate([(24, 304), (360, 304), (696, 304)]):
        chunk = STORIES[ci * 12:(ci + 1) * 12]
        y = 572
        for num, _lon, _lat, _sect, head in chunk:
            d.ellipse([cx, y + 2, cx + 18, y + 20], fill=INK)
            s = str(num)
            sw = d.textlength(s, font=F_NUM)
            d.text((cx + 9 - sw / 2, y + 5), s, font=F_NUM, fill=(255, 255, 255))
            lines = wrap(d, head, F_STORY, cw - 26, max_lines=2)
            for li, line in enumerate(lines):
                d.text((cx + 26, y + li * 13), line, font=F_STORY, fill=INK)
            y += len(lines) * 13 + 5
    # in brief box, filling the space under the story columns
    d.rectangle([24, 874, W - 24, 960], fill=BOX, outline=INK, width=1)
    d.text((36, 880), "IN BRIEF", font=F_MAPHEAD, fill=RED)
    by = 900
    for item in BRIEFS:
        d.text((36, by), "•  " + item, font=F_BRIEF, fill=INK)
        by += 14
    # ticker
    d.rectangle([24, 968, W - 24, 1000], fill=TICK)
    tw3 = d.textlength(TICKER, font=F_TICK)
    d.text(((W - tw3) / 2, 976), TICKER, font=F_TICK, fill=(255, 255, 255))
    return img


def main():
    img = draw_page()
    out = os.path.join(HERE, "entry.png")
    img.save(out, format="PNG", optimize=True)
    print(out, img.size, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
