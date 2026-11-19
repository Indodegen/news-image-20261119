#!/usr/bin/env python3
"""THE WORLD TODAY -- Thursday 19 November 2026.

Draws a 1024x1024 newspaper front-page infographic summarising the
day's top world news, using only the Python standard library.

No network, no external files, no randomness, no timestamps:
running the program twice produces byte-identical PNG output.

Usage:
    python3 main.py
    # writes entry.png into $MAKEFUN_OUTPUT_DIR (default /output)
"""

import math
import os
import struct
import zlib

W = 1024
H = 1024

# ---------------------------------------------------------------- palette
# A fresh palette for 19 November: deep teal masthead, crimson accents,
# warm cream paper, drawn fresh for this day's entry.
PAPER = (250, 246, 236)
CARD = (255, 255, 255)
TEAL = (15, 59, 58)
TEAL_LIGHT = (38, 99, 96)
CRIMSON = (192, 57, 43)
CRIMSON_DARK = (150, 40, 28)
INK = (28, 28, 28)
GREY = (110, 108, 100)
LINE = (222, 214, 196)
GOLD = (201, 162, 39)
SKY = (214, 232, 228)

# ------------------------------------------------------------------- font
# Hand-written 5x7 bitmap glyphs. '#' = ink, '.' = blank.
# Uppercase A-Z, digits 0-9 and punctuation . , ' : ; ! ? - / ( ) & % $ + =
FONT = {
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    "C": ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    "D": ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    "G": ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    "H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    "I": ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    "J": ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    "K": ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    "M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    "N": ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "Q": ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    "V": ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    "W": ("10001", "10001", "10001", "10101", "10101", "11011", "10001"),
    "X": ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    "Y": ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    "Z": ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    "0": ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    "2": ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    "3": ("11111", "00010", "00100", "00010", "00001", "10001", "01110"),
    "4": ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    "5": ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    "6": ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
    "7": ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    "8": ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    "9": ("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
    ".": ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ",": ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    ":": ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    ";": ("00000", "01100", "01100", "00000", "01100", "00100", "01000"),
    "!": ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    "?": ("01110", "10001", "00001", "00110", "00100", "00000", "00100"),
    "-": ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    "/": ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    "(": ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ")": ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    "&": ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    "%": ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    "$": ("00100", "01111", "10100", "01110", "00101", "11110", "00100"),
    "+": ("00000", "00100", "00100", "11111", "00100", "00100", "00000"),
    "=": ("00000", "00000", "11111", "00000", "11111", "00000", "00000"),
    " ": ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
}

# ------------------------------------------------------------------ canvas
class Canvas:
    def __init__(self, w, h, bg):
        self.w = w
        self.h = h
        self.px = bytearray(w * h * 3)
        self.fill_rect(0, 0, w, h, bg)

    def set(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i], self.px[i + 1], self.px[i + 2] = color

    def fill_rect(self, x, y, w, h, color):
        x0 = max(0, x)
        y0 = max(0, y)
        x1 = min(self.w, x + w)
        y1 = min(self.h, y + h)
        for yy in range(y0, y1):
            base = (yy * self.w + x0) * 3
            for xx in range(x0, x1):
                i = base + (xx - x0) * 3
                self.px[i], self.px[i + 1], self.px[i + 2] = color

    def rect(self, x, y, w, h, color, t=1):
        self.fill_rect(x, y, w, t, color)
        self.fill_rect(x, y + h - t, w, t, color)
        self.fill_rect(x, y, t, h, color)
        self.fill_rect(x + w - t, y, t, h, color)

    def hline(self, x, y, length, color, t=1):
        self.fill_rect(x, y, length, t, color)

    def vline(self, x, y, length, color, t=1):
        self.fill_rect(x, y, t, length, color)

    def line(self, x0, y0, x1, y1, color, t=1):
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        x, y = x0, y0
        half = t // 2
        while True:
            self.fill_rect(x - half, y - half, t, t, color)
            if x == x1 and y == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x += sx
            if e2 <= dx:
                err += dx
                y += sy

    def fill_circle(self, cx, cy, r, color):
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                if (xx - cx) ** 2 + (yy - cy) ** 2 <= r * r:
                    self.set(xx, yy, color)

    def circle(self, cx, cy, r, color, t=2):
        for yy in range(cy - r - t, cy + r + t + 1):
            for xx in range(cx - r - t, cx + r + t + 1):
                d = ((xx - cx) ** 2 + (yy - cy) ** 2) ** 0.5
                if abs(d - r) <= t / 2.0:
                    self.set(xx, yy, color)

    def fill_half_circle(self, cx, cy, r, color):
        # Upper half of a filled circle (a dome).
        for yy in range(cy - r, cy + 1):
            for xx in range(cx - r, cx + r + 1):
                if (xx - cx) ** 2 + (yy - cy) ** 2 <= r * r:
                    self.set(xx, yy, color)

    def fill_triangle(self, p0, p1, p2, color):
        xs = [p0[0], p1[0], p2[0]]
        ys = [p0[1], p1[1], p2[1]]
        for yy in range(min(ys), max(ys) + 1):
            row = []
            for (ax, ay), (bx, by) in ((p0, p1), (p1, p2), (p2, p0)):
                if ay == by:
                    continue
                if min(ay, by) <= yy < max(ay, by):
                    xx = ax + (yy - ay) * (bx - ax) / (by - ay)
                    row.append(xx)
            if len(row) >= 2:
                for xx in range(int(min(row)), int(max(row)) + 1):
                    self.set(xx, yy, color)


# -------------------------------------------------------------------- text
def text_width(text, scale):
    return len(text) * (5 * scale + scale)


def draw_text(c, x, y, text, scale, color):
    cx = x
    for ch in text:
        glyph = FONT.get(ch, FONT[" "])
        for row in range(7):
            bits = glyph[row]
            for col in range(5):
                if bits[col] == "1":
                    c.fill_rect(cx + col * scale, y + row * scale,
                                scale, scale, color)
        cx += 5 * scale + scale
    return cx


def draw_text_centered(c, y, text, scale, color, cx=W // 2):
    w = text_width(text, scale)
    draw_text(c, cx - w // 2, y, text, scale, color)


def wrap_text(text, max_width, scale):
    """Greedy word wrap; returns a list of lines fitting max_width px."""
    char_w = 5 * scale + scale
    max_chars = max(1, max_width // char_w)
    lines = []
    for para in text.split("\n"):
        words = para.split(" ")
        cur = ""
        for word in words:
            trial = word if not cur else cur + " " + word
            if len(trial) <= max_chars:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                while len(word) > max_chars:
                    lines.append(word[:max_chars])
                    word = word[max_chars:]
                cur = word
        if cur:
            lines.append(cur)
    return lines


# ------------------------------------------------------------------- icons
def icon_controller(c, cx, cy, s):
    # Game controller: wide body, two grips, D-pad, four buttons.
    c.fill_rect(cx - s, cy - 22, 2 * s, 44, TEAL)             # body
    c.fill_triangle((cx - s, cy + 10), (cx - s + 26, cy + 10),
                    (cx - s + 4, cy + 34), TEAL)              # left grip
    c.fill_triangle((cx + s, cy + 10), (cx + s - 26, cy + 10),
                    (cx + s - 4, cy + 34), TEAL)              # right grip
    c.fill_rect(cx - s + 8, cy - 22, 2 * s - 16, 6, TEAL_LIGHT)
    # D-pad on the left
    c.fill_rect(cx - s + 12, cy - 12, 8, 24, CARD)
    c.fill_rect(cx - s + 4, cy - 4, 24, 8, CARD)
    # four action buttons on the right
    c.fill_circle(cx + s - 22, cy - 12, 5, CRIMSON)
    c.fill_circle(cx + s - 22, cy + 8, 5, GOLD)
    c.fill_circle(cx + s - 34, cy - 2, 5, CARD)
    c.fill_circle(cx + s - 10, cy - 2, 5, TEAL_LIGHT)
    # two analogue sticks
    c.fill_circle(cx - 12, cy + 8, 7, TEAL_LIGHT)
    c.fill_circle(cx + 12, cy + 8, 7, TEAL_LIGHT)
    c.fill_circle(cx - 12, cy + 8, 3, CARD)
    c.fill_circle(cx + 12, cy + 8, 3, CARD)
    # tiny "VI" tag above the body
    draw_text(c, cx - 12, cy - 40, "VI", 2, CRIMSON)


def icon_capitol(c, cx, cy, s):
    # Capitol dome: half-circle dome, lantern, columns, stepped base.
    c.fill_rect(cx - 2, cy - s - 14, 4, 16, TEAL)             # flag pole
    c.fill_triangle((cx + 2, cy - s - 14), (cx + 2, cy - s - 4),
                    (cx + 18, cy - s - 9), CRIMSON)           # flag
    c.fill_rect(cx - 6, cy - s, 12, 6, GOLD)                 # lantern
    c.fill_half_circle(cx, cy - s + 6, s - 8, TEAL)           # dome
    c.fill_rect(cx - s + 4, cy - s + 6, 2 * s - 8, 4, TEAL_LIGHT)
    for dx in (-30, -12, 6, 24):                             # columns
        c.fill_rect(cx + dx, cy - s + 12, 6, s - 4, TEAL)
    c.fill_rect(cx - s - 2, cy + 6, 2 * s + 4, 6, TEAL)       # entablature
    c.fill_rect(cx - s - 6, cy + 12, 2 * s + 12, 5, CRIMSON)  # step 1
    c.fill_rect(cx - s - 10, cy + 17, 2 * s + 20, 5, TEAL)    # step 2


def icon_missiles(c, cx, cy, s):
    # Two missiles crossing, with a burst where they meet.
    # Missile 1: top-left to bottom-right.
    c.line(cx - s + 6, cy - s + 14, cx + s - 16, cy + s - 24, TEAL, 7)
    c.fill_triangle((cx + s - 16, cy + s - 24),
                    (cx + s - 2, cy + s - 10),
                    (cx + s - 28, cy + s - 8), CRIMSON)       # nose cone 1
    c.fill_triangle((cx - s + 6, cy - s + 14),
                    (cx - s + 16, cy - s + 4),
                    (cx - s + 18, cy - s + 22), GOLD)         # fins 1
    # Missile 2: top-right to bottom-left.
    c.line(cx + s - 6, cy - s + 14, cx - s + 16, cy + s - 24, CRIMSON, 7)
    c.fill_triangle((cx - s + 16, cy + s - 24),
                    (cx - s + 2, cy + s - 10),
                    (cx - s + 28, cy + s - 8), TEAL)          # nose cone 2
    c.fill_triangle((cx + s - 6, cy - s + 14),
                    (cx + s - 16, cy - s + 4),
                    (cx + s - 18, cy - s + 22), GOLD)         # fins 2
    # burst at the crossing point
    c.fill_circle(cx, cy, 11, GOLD)
    c.fill_circle(cx, cy, 6, CRIMSON)
    c.fill_circle(cx, cy, 2, CARD)


def icon_eu_stars(c, cx, cy, s):
    # EU circle of stars on a teal disc, "EU" in the middle.
    c.fill_circle(cx, cy, s, TEAL)
    c.circle(cx, cy, s, TEAL_LIGHT, 3)
    for i in range(12):
        a = math.radians(i * 30 - 90)
        sx = int(cx + (s - 12) * math.cos(a))
        sy = int(cy + (s - 12) * math.sin(a))
        c.fill_circle(sx, sy, 4, GOLD)
    draw_text(c, cx - 12, cy - 7, "EU", 2, GOLD)


def icon_voyager(c, cx, cy, s):
    # Voyager probe: big dish, body, boom with RTG, trailing stars.
    c.fill_circle(cx - s - 6, cy - s + 2, 3, GOLD)            # star
    c.fill_circle(cx + s + 2, cy - s + 14, 2, TEAL_LIGHT)     # star
    c.fill_circle(cx + s - 2, cy + s - 6, 3, CRIMSON)         # star
    # dish: wide cone opening up-right, gold rim along the opening
    c.fill_triangle((cx - 20, cy - 2), (cx + 30, cy - 50),
                    (cx + 46, cy - 8), TEAL)
    c.fill_triangle((cx - 20, cy - 2), (cx + 30, cy - 50),
                    (cx + 16, cy - 38), TEAL_LIGHT)
    c.line(cx + 30, cy - 50, cx + 46, cy - 8, GOLD, 3)
    c.fill_circle(cx + 38, cy - 29, 3, GOLD)                 # feed horn
    # body bus
    c.fill_rect(cx - 26, cy - 2, 34, 16, TEAL)
    c.fill_rect(cx - 26, cy - 2, 34, 4, GOLD)
    # boom to the RTG
    c.line(cx - 26, cy + 6, cx - s - 2, cy + 22, TEAL, 4)
    c.fill_rect(cx - s - 8, cy + 16, 12, 12, CRIMSON)
    # antenna mast
    c.line(cx + 4, cy - 2, cx + 18, cy - s + 6, TEAL, 3)
    c.fill_circle(cx + 18, cy - s + 6, 3, GOLD)


def icon_cyclone(c, cx, cy, s):
    # Cyclone spiral: expanding dotted arcs around a calm gold eye,
    # with rain streaks falling on both sides.
    for r in range(10, s + 6, 9):
        for deg in range(0, 300, 8):
            a = math.radians(deg + r * 8)
            xx = int(cx + r * math.cos(a))
            yy = int(cy + r * 0.85 * math.sin(a))
            c.fill_circle(xx, yy, 3, CRIMSON if r % 18 else TEAL)
    c.fill_circle(cx, cy, 8, GOLD)
    c.fill_circle(cx, cy, 4, CRIMSON)
    for dx in (-s - 2, s + 2):
        c.line(cx + dx, cy - s + 18, cx + dx - 6, cy - s + 34,
               TEAL_LIGHT, 3)


ICONS = [icon_controller, icon_capitol, icon_missiles, icon_eu_stars,
         icon_voyager, icon_cyclone]

# ------------------------------------------------------------------ stories
STORIES = [
    ("GTA VI ROLLS OUT WORLDWIDE",
     "AFTER 13 YEARS OF WAITING, GRAND THEFT AUTO VI BEGINS ITS GLOBAL "
     "ROLLOUT. PLAYERS RETURN TO VICE CITY."),
    ("JEFFRIES NOMINATED AS SPEAKER",
     "DEMOCRATS NOMINATE HAKEEM JEFFRIES AS SPEAKER OF THE HOUSE. HE WOULD "
     "BE THE FIRST AFRICAN-AMERICAN SPEAKER."),
    ("US AND IRAN STRIKE AGAIN",
     "US AND IRAN STRIKE EACH OTHER AGAIN. IRAN HITS BAHRAIN AND KUWAIT; "
     "THE US STRIKES MISSILE SITES ON QESHM ISLAND."),
    ("EU PROPOSES 45BN LOAN FOR UKRAINE",
     "THE EU PROPOSES A 45 BILLION EURO LOAN FOR UKRAINE, TO BE REPAID ONCE "
     "RUSSIA PAYS REPARATIONS."),
    ("VOYAGER 1 REACHES ONE LIGHT-DAY",
     "NASA'S VOYAGER 1 IS BELIEVED TO REACH ONE LIGHT-DAY FROM EARTH, "
     "NEARLY 50 YEARS AFTER LAUNCH."),
    ("CYCLONE AKVAN NEARS INDIA",
     "CYCLONE AKVAN NEARS INDIA'S EAST COAST. IT IS EXPECTED TO CROSS "
     "BETWEEN MACHILIPATNAM AND PURI."),
]


# ------------------------------------------------------------------ drawing
def badge(c, cx, cy, r, number, scale=3):
    c.fill_circle(cx, cy, r, CRIMSON)
    c.circle(cx, cy, r, CRIMSON_DARK, 2)
    txt = str(number)
    w = text_width(txt, scale)
    draw_text(c, cx - w // 2, cy - (7 * scale) // 2, txt, scale, CARD)


def draw_grid_cell(c, x, y, w, h, number, headline, summary, icon):
    c.fill_rect(x, y, w, h, CARD)
    c.rect(x, y, w, h, LINE, 2)
    c.fill_rect(x, y, w, 5, CRIMSON if number % 2 else TEAL)
    badge(c, x + w - 34, y + 34, 20, number, scale=3)
    # Headline across the top, wrapped to leave room for the badge.
    hlines = wrap_text(headline, w - 32 - 62, 3)
    for i, ln in enumerate(hlines[:2]):
        draw_text(c, x + 16, y + 18 + i * 24, ln, 3, TEAL)
    c.hline(x + 16, y + 18 + len(hlines[:2]) * 24 + 2, 120, GOLD, 4)
    # Icon left, summary right, below the headline.
    body_y = y + 18 + len(hlines[:2]) * 24 + 18
    icon(c, x + 62, body_y + 42, 34)
    blines = wrap_text(summary, w - 140 - 16, 2)
    for i, ln in enumerate(blines[:5]):
        draw_text(c, x + 140, body_y + i * 20, ln, 2, INK)


def draw():
    c = Canvas(W, H, PAPER)

    # ---- masthead ------------------------------------------------------
    c.fill_rect(0, 0, W, 172, TEAL)
    c.fill_rect(0, 0, W, 6, GOLD)
    draw_text_centered(c, 22, "THE WORLD TODAY", 5, CARD)
    draw_text_centered(c, 72, "THURSDAY, 19 NOVEMBER 2026", 4, GOLD)
    c.fill_rect(92, 116, W - 184, 3, CRIMSON)
    draw_text_centered(c, 132, "SIX STORIES FROM AROUND THE WORLD",
                       2, (196, 216, 212))
    c.fill_rect(0, 166, W, 6, CRIMSON)

    # ---- lead story: GTA VI --------------------------------------------
    lx, ly, lw, lh = 16, 184, 992, 188
    c.fill_rect(lx, ly, lw, lh, CARD)
    c.rect(lx, ly, lw, lh, TEAL, 3)
    c.fill_rect(lx, ly, lw, 6, CRIMSON)
    badge(c, lx + lw - 46, ly + 46, 24, 1, scale=3)
    ICONS[0](c, 168, ly + 96, 46)
    draw_text(c, lx + 16, ly + 152, "LEAD STORY", 2, CRIMSON)
    hx = 252
    draw_text(c, hx, ly + 30, STORIES[0][0], 4, TEAL)
    c.fill_rect(hx, ly + 72, 420, 4, GOLD)
    lines = wrap_text(STORIES[0][1], lw - (hx - lx) - 28, 2)
    for i, ln in enumerate(lines[:3]):
        draw_text(c, hx, ly + 92 + i * 22, ln, 2, INK)

    # ---- four stories in a 2 x 2 grid ----------------------------------
    # Headline on top, icon left and summary right below it.
    gx = [16, 520]
    gy = [384, 584]
    cw, ch = 488, 188
    for k in range(4):
        idx = k + 1
        draw_grid_cell(c, gx[k % 2], gy[k // 2], cw, ch, idx + 1,
                       STORIES[idx][0], STORIES[idx][1], ICONS[idx])

    # ---- story 6: wide row ---------------------------------------------
    sx, sy, sw, sh = 16, 784, 992, 150
    c.fill_rect(sx, sy, sw, sh, CARD)
    c.rect(sx, sy, sw, sh, LINE, 2)
    c.fill_rect(sx, sy, 6, sh, CRIMSON)
    badge(c, sx + sw - 40, sy + 38, 20, 6, scale=3)
    ICONS[5](c, 108, sy + sh // 2, 40)
    draw_text(c, 196, sy + 20, STORIES[5][0], 4, TEAL)
    c.fill_rect(196, sy + 62, 380, 4, GOLD)
    lines = wrap_text(STORIES[5][1], sw - 196 - 24, 2)
    for i, ln in enumerate(lines[:3]):
        draw_text(c, 196, sy + 80 + i * 22, ln, 2, INK)

    # ---- footer ---------------------------------------------------------
    fy = 946
    c.fill_rect(0, fy, W, 4, CRIMSON)
    draw_text_centered(c, fy + 14,
                       "SUMMARISED FROM REPORTS PUBLISHED ON 19 NOVEMBER 2026",
                       2, GREY)
    draw_text_centered(c, fy + 42, "THURSDAY, 19 NOVEMBER 2026 - SIX "
                       "STORIES - ONE DAY", 2, TEAL)
    c.fill_rect(0, H - 10, W, 10, TEAL)
    return c


# ---------------------------------------------------------------------- PNG
def chunk(kind, data):
    out = struct.pack(">I", len(data)) + kind + data
    out += struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
    return out


def save_png(canvas, path):
    raw = bytearray()
    for y in range(canvas.h):
        raw.append(0)  # filter: none
        start = y * canvas.w * 3
        raw += canvas.px[start:start + canvas.w * 3]
    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", canvas.w, canvas.h,
                                      8, 2, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    png += chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)
    return len(png)


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    canvas = draw()
    path = os.path.join(out_dir, "entry.png")
    size = save_png(canvas, path)
    print("wrote %s (%d bytes, %dx%d)" % (path, size, W, H))


if __name__ == "__main__":
    main()
