#!/usr/bin/env python3
"""Render THE WORLD IN ONE PAGE for Friday 20 November 2026.

Deterministic: no network, no clock, no randomness. PIL + DejaVu only.
Run: python3 gen.py  -> writes entry.png (1024x1024) next to this file.
"""

import hashlib
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 28
FONT_DIR = "/usr/share/fonts/truetype/dejavu"

PAPER = (246, 241, 227)
INK = (26, 26, 24)
RULE = (26, 26, 24)
MUTED = (90, 84, 70)
RED = (163, 22, 33)
DARK = (24, 24, 30)
LAND = (221, 213, 189)
LAND_LINE = (107, 93, 67)
SEA = (233, 230, 216)
BOX_LINE = (120, 112, 92)
TICKER_BG = (24, 24, 30)

# (number, longitude, latitude, headline)
# Longitudes/latitudes are approximate; a few crowded spots are nudged
# so the numbered dots stay readable on a schematic map.
STORIES = [
    (1, 96.0, 21.0, "ICJ rules Myanmar committed genocide against Rohingya"),
    (2, 114.0, 22.5, "Trump, Xi, Putin hold first trilateral summit in Shenzhen"),
    (3, -72.0, 46.0, "US stocks fall for fifth straight day; S&P -2.02%, Nasdaq -2.25%"),
    (4, -64.0, 40.0, "Anthropic closes 17% above IPO price in Nasdaq debut"),
    (5, 45.0, 23.5, "Houthi missile damages Riyadh's tallest tower"),
    (6, 49.0, 27.5, "Saudi Arabia intercepts another Houthi missile and five drones"),
    (7, 36.5, 45.3, "Ukraine hits Kerch Bridge for third time in a week"),
    (8, 30.5, 50.4, "Russia launches overnight attack on Kyiv; six killed"),
    (9, -2.0, 53.0, "UK pledges 1,000+ drones for Ukraine in a £260M package"),
    (10, -88.0, 48.0, "GTA 6 launch tops $2.3 billion in sales"),
    (11, -80.0, 41.0, "IMF warns global public debt nearing 100% of world GDP"),
    (12, 12.5, 41.5, "Italy fines Meta 805 million euros over Android photo access"),
    (13, -70.0, 33.0, "FAA ground stop strands 1.5 million travelers"),
    (14, 36.8, -1.3, "Kenya discharges last Ebola patient, 37 days after first case"),
    (15, -62.0, 33.0, "US Senate passes bipartisan energy-permitting bill 62-33"),
    (16, -89.0, 14.0, "El Salvador's Bukele to run for third presidential term"),
    (17, 38.7, 9.0, "COP31: Africa seeks tripled climate finance"),
    (18, 3.5, 48.0, "France to deploy 70,000 police for cost-of-living protests"),
    (19, 165.5, -21.5, "5.6-magnitude earthquake strikes near New Caledonia"),
    (20, 21.0, 52.2, "Poland investigates unknown objects as air-threat warning lifted"),
    (21, 9.0, 53.5, "EU to summon Russian envoy over embassy damage in Kyiv strikes"),
    (22, -92.0, 42.0, "US Senate rejects Iran war-powers resolution 51-48"),
    (23, -84.0, 52.0, "Trump announces posthumous pardon for Pete Rose"),
    (24, 151.0, -34.0, "US sanctions Comancheros and 'Ndrangheta"),
    (25, -17.4, 14.7, "Senegal boat capsizing kills four"),
    (26, 34.5, 31.5, "Gaza rescue crews respond on foot as vehicle fleet collapses"),
    (27, -122.0, 37.0, "China-linked spies exploited VMware vCenter zero-day before patch"),
    (28, -60.0, 47.0, "N-able zero-days exploited to mine crypto on 21 servers"),
    (29, -7.0, 47.0, "IEA warns AI data centers could push emissions sharply higher by 2030"),
    (30, -76.0, 31.0, "Virginia pulls out of Trump's school choice tax-credit program"),
    (31, -88.0, 35.0, "Ella Langley sweeps the CMA Awards"),
    (32, 56.5, 26.5, "Tanker catches fire after hitting a mine east of Strait of Hormuz"),
    (33, 7.5, 43.0, "Genoa airport suspends flights after unidentified drones detected"),
    (34, 33.8, -13.9, "Malawi fuel crisis triggers violence and economic strain"),
    (35, -58.4, -34.6, "Argentina Senate approves permanent disability framework"),
    (36, 77.2, 28.6, "India relaxes vessel-age restrictions to expand national fleet"),
]

LEADS = [
    "Trump, Xi and Putin hold their first three-way summit in Shenzhen and issue a joint "
    "peace declaration after about 70 minutes, with no breakthrough on Ukraine, Iran or "
    "nuclear arms.",
    "The International Court of Justice rules 9-6 that Myanmar committed genocide against "
    "the Rohingya, the court's first such finding against a state.",
    "US stocks fall for a fifth straight day: the S&P 500 loses 2.02% and the Nasdaq "
    "2.25%, while Japan's Nikkei drops 5.1% after Anthropic's Nasdaq debut.",
]

BRIEF = [
    "GTA 6 launch tops $2.3 billion in sales.",
    "Anthropic closes 17% above its IPO price on Nasdaq.",
    "Kenya discharges its last Ebola patient.",
    "IMF warns global public debt is nearing 100% of world GDP.",
]

TICKER = [
    ("S&P 500", "7,175.83", "-2.02%"),
    ("Nasdaq", "23,879.20", "-2.25%"),
    ("Brent", "$89.05", "-0.44%"),
    ("Bitcoin", "$61,709", "-0.32%"),
    ("VIX", "28.44", "+15.8%"),
]

# Coarse continent outlines (lon, lat), schematic only.
CONTINENTS = [
    # North America
    [(-168, 66), (-150, 70), (-135, 69), (-125, 71), (-115, 68), (-105, 68),
     (-95, 69), (-88, 68), (-82, 66), (-78, 62), (-70, 60), (-60, 55),
     (-55, 52), (-60, 47), (-65, 44), (-70, 42), (-74, 39), (-76, 35),
     (-80, 32), (-81, 26), (-84, 30), (-90, 21), (-94, 18), (-97, 16),
     (-92, 15), (-87, 13), (-83, 9), (-79, 9), (-82, 14), (-88, 14),
     (-95, 16), (-100, 18), (-105, 20), (-110, 23), (-114, 28), (-117, 32),
     (-122, 37), (-124, 42), (-124, 48), (-128, 52), (-135, 57), (-145, 60),
     (-155, 58), (-162, 58), (-168, 66)],
    # South America
    [(-79, 9), (-76, 10), (-72, 12), (-66, 11), (-60, 9), (-54, 6),
     (-50, 2), (-50, -2), (-44, -3), (-38, -5), (-35, -8), (-38, -14),
     (-40, -21), (-46, -26), (-52, -32), (-57, -38), (-62, -41), (-65, -45),
     (-68, -50), (-70, -54), (-73, -50), (-73, -44), (-72, -36), (-71, -28),
     (-70, -19), (-75, -15), (-79, -8), (-81, -4), (-80, 1), (-79, 9)],
    # Africa
    [(-6, 35), (-10, 31), (-14, 28), (-16, 21), (-17, 15), (-17, 8),
     (-13, 5), (-8, 4), (-3, 5), (2, 6), (6, 4), (9, 4), (9, -1),
     (12, -5), (13, -10), (12, -16), (13, -22), (16, -28), (19, -34),
     (25, -34), (29, -29), (32, -26), (35, -22), (36, -18), (40, -15),
     (40, -10), (45, -11), (48, -5), (51, 2), (51, 11), (46, 11),
     (43, 12), (40, 15), (38, 18), (36, 22), (34, 27), (32, 31),
     (29, 32), (25, 32), (20, 33), (15, 33), (11, 34), (10, 37),
     (5, 37), (0, 36), (-6, 35)],
    # Europe
    [(-10, 36), (-9, 38), (-9, 43), (-4, 44), (-2, 47), (-4, 49),
     (-1, 50), (1, 51), (3, 53), (5, 53), (8, 55), (8, 57), (10, 59),
     (6, 61), (10, 63), (14, 66), (18, 69), (22, 70), (26, 71),
     (30, 70), (32, 68), (30, 64), (28, 60), (24, 59), (21, 58),
     (19, 56), (16, 56), (12, 55), (10, 57), (8, 55), (5, 53),
     (2, 51), (0, 50), (-2, 49), (-4, 48), (-2, 45), (-1, 43),
     (0, 40), (0, 37), (-4, 36), (-9, 37), (-10, 36)],
    # Asia
    [(30, 70), (35, 69), (42, 68), (48, 68), (54, 69), (60, 69),
     (66, 71), (72, 72), (78, 72), (84, 74), (90, 75), (96, 76),
     (102, 77), (108, 76), (114, 74), (120, 73), (126, 72), (132, 71),
     (138, 72), (144, 71), (150, 70), (156, 69), (162, 67), (168, 66),
     (173, 65), (178, 65), (172, 62), (166, 60), (160, 56), (156, 52),
     (152, 56), (146, 59), (141, 54), (140, 48), (138, 45), (134, 42),
     (130, 40), (127, 36), (126, 33), (122, 31), (120, 27), (117, 24),
     (113, 22), (109, 20), (108, 17), (106, 11), (104, 9), (101, 8),
     (99, 10), (97, 14), (95, 16), (92, 21), (89, 22), (87, 21),
     (84, 19), (81, 16), (79, 13), (77, 9), (76, 11), (74, 14),
     (73, 19), (71, 21), (69, 22), (67, 25), (64, 25), (61, 25),
     (58, 26), (56, 27), (53, 27), (51, 29), (49, 30), (47, 30),
     (44, 29), (42, 27), (40, 24), (39, 21), (37, 21), (36, 25),
     (35, 29), (34, 31), (33, 35), (32, 36), (30, 36), (28, 38),
     (27, 40), (29, 41), (31, 43), (33, 45), (33, 48), (31, 52),
     (30, 55), (29, 60), (29, 64), (30, 67), (30, 70)],
    # Australia
    [(113, -22), (114, -27), (115, -32), (116, -35), (120, -34), (124, -33),
     (128, -32), (132, -32), (135, -35), (138, -35), (140, -38), (144, -38),
     (148, -38), (150, -37), (152, -33), (153, -28), (152, -24), (150, -22),
     (147, -19), (144, -15), (142, -11), (141, -14), (137, -12), (135, -15),
     (132, -11), (130, -13), (127, -14), (124, -16), (121, -18), (117, -20),
     (113, -22)],
    # New Zealand
    [(167, -45), (170, -43), (173, -41), (176, -38), (178, -38), (176, -40),
     (174, -42), (171, -43), (168, -45)],
    # United Kingdom
    [(-5, 50), (-4, 51), (-3, 53), (-5, 55), (-4, 57), (-2, 58),
     (0, 57), (1, 55), (1, 52), (0, 51), (-2, 50), (-5, 50)],
]


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def wrap(draw, text, fnt, width):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_center(draw, y, text, fnt, fill=INK):
    draw.text((W / 2, y), text, font=fnt, fill=fill, anchor="mt")


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    serif_b = font("DejaVuSerif-Bold.ttf", 50)
    sans_b = font("DejaVuSans-Bold.ttf", 15)
    sans = font("DejaVuSans.ttf", 13)
    small_b = font("DejaVuSans-Bold.ttf", 11)
    small = font("DejaVuSans.ttf", 11)
    tiny_b = font("DejaVuSans-Bold.ttf", 10)
    num_b = font("DejaVuSans-Bold.ttf", 8)
    ticker_b = font("DejaVuSans-Bold.ttf", 12)

    # ---- Masthead -------------------------------------------------------
    draw_center(d, 26, "THE WORLD IN ONE PAGE", serif_b)
    d.line([(MARGIN, 96), (W - MARGIN, 96)], fill=RULE, width=3)
    d.line([(MARGIN, 101), (W - MARGIN, 101)], fill=RULE, width=1)
    d.text((MARGIN, 106), "FRIDAY EDITION", font=tiny_b, fill=MUTED)
    d.text((W - MARGIN, 106), "FREE — EVERYWHERE", font=tiny_b, fill=MUTED, anchor="rt")
    draw_center(d, 106, "FRIDAY 20 NOVEMBER 2026 — 36 STORIES, 6 CONTINENTS", sans_b)

    # ---- The Day in Three ----------------------------------------------
    box_y0, box_y1 = 132, 296
    d.rectangle([MARGIN, box_y0, W - MARGIN, box_y1], outline=BOX_LINE, width=2)
    d.rectangle([MARGIN, box_y0, W - MARGIN, box_y0 + 26], fill=DARK)
    d.text((MARGIN + 10, box_y0 + 6), "THE DAY IN THREE", font=sans_b, fill=(250, 248, 240))
    y = box_y0 + 34
    for i, lead in enumerate(LEADS, 1):
        d.text((MARGIN + 10, y), "%d." % i, font=sans_b, fill=RED)
        lines = wrap(d, lead, sans, W - 2 * MARGIN - 44)
        for ln in lines:
            d.text((MARGIN + 34, y), ln, font=sans, fill=INK)
            y += 17
        y += 6

    # ---- Map ------------------------------------------------------------
    map_x0, map_y0, map_x1, map_y1 = MARGIN, 318, W - MARGIN, 500
    d.text((MARGIN, 300), "WHERE IT HAPPENED", font=sans_b, fill=INK)
    d.text((W - MARGIN, 300), "36 STORIES, NUMBERED", font=tiny_b, fill=MUTED, anchor="rt")
    d.rectangle([map_x0, map_y0, map_x1, map_y1], fill=SEA, outline=BOX_LINE, width=2)

    def proj(lon, lat):
        x = map_x0 + (lon + 180.0) / 360.0 * (map_x1 - map_x0)
        yy = map_y0 + (75.0 - lat) / 135.0 * (map_y1 - map_y0)
        return x, yy

    for poly in CONTINENTS:
        pts = [proj(lon, lat) for lon, lat in poly]
        d.polygon(pts, fill=LAND, outline=LAND_LINE)

    for n, lon, lat, _ in STORIES:
        x, yy = proj(lon, lat)
        r = 6
        d.ellipse([x - r, yy - r, x + r, yy + r], fill=RED, outline=(255, 255, 255), width=1)
        d.text((x, yy), str(n), font=num_b, fill=(255, 255, 255), anchor="mm")

    # ---- Story columns ---------------------------------------------------
    col_y0 = 514
    col_w = 312
    col_xs = [MARGIN, MARGIN + col_w + 16, MARGIN + 2 * (col_w + 16)]
    for c in range(3):
        group = STORIES[c * 12:(c + 1) * 12]
        y = col_y0
        for n, _lon, _lat, head in group:
            label = "%d." % n
            lw = d.textlength(label, font=small_b)
            d.text((col_xs[c], y), label, font=small_b, fill=RED)
            lines = wrap(d, head, small, col_w - lw - 6)
            for ln in lines:
                d.text((col_xs[c] + lw + 6, y), ln, font=small, fill=INK)
                y += 13
            y += 5

    # ---- In Brief --------------------------------------------------------
    brief_y0, brief_y1 = 890, 952
    d.rectangle([MARGIN, brief_y0, W - MARGIN, brief_y1], outline=BOX_LINE, width=2)
    d.rectangle([MARGIN, brief_y0, W - MARGIN, brief_y0 + 22], fill=DARK)
    d.text((MARGIN + 10, brief_y0 + 4), "IN BRIEF", font=sans_b, fill=(250, 248, 240))
    bw = (W - 2 * MARGIN) // 2
    for i, item in enumerate(BRIEF):
        bx = MARGIN + 10 + (i % 2) * bw
        by = brief_y0 + 30 + (i // 2) * 15
        d.text((bx, by), "—", font=small_b, fill=RED)
        d.text((bx + 14, by), item, font=small, fill=INK)

    # ---- Market ticker ---------------------------------------------------
    tick_y0, tick_y1 = 962, 1004
    d.rectangle([MARGIN, tick_y0, W - MARGIN, tick_y1], fill=TICKER_BG)
    parts = ["%s %s %s" % (name, val, chg) for name, val, chg in TICKER]
    ticker_text = " | ".join(parts)
    d.text((W / 2, (tick_y0 + tick_y1) / 2), ticker_text, font=ticker_b,
           fill=(245, 242, 232), anchor="mm")

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG")
    h = hashlib.sha256(open(out, "rb").read()).hexdigest()
    print("wrote %s  sha256=%s" % (out, h))


if __name__ == "__main__":
    main()
