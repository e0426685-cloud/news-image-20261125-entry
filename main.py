#!/usr/bin/env python3
"""The World Today - Wednesday 25 November 2026.

A one-image broadsheet front page, drawn entirely with the Python
standard library.  A tiny 5x7 bitmap font renders every letter, and a
minimal PNG writer (zlib + struct) encodes the finished page.
No third-party packages are used anywhere.
"""

import os
import struct
import zlib

W, H = 1024, 1024

INK = (18, 18, 18)
PAPER = (250, 247, 238)
RED = (158, 27, 34)
NAVY = (24, 52, 96)
SKY = (126, 178, 214)
SEA = (38, 92, 140)
STEEL = (90, 104, 116)
GOLD = (176, 138, 44)
GREY = (110, 108, 100)
LIGHT = (232, 228, 218)

# ---------------------------------------------------------------- font ----
# Each glyph is seven rows of five bits, "1" = ink.
GLYPHS = {
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
    " ": ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    ".": ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ",": ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    '"': ("01010", "01010", "00000", "00000", "00000", "00000", "00000"),
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
    "+": ("00000", "00100", "00100", "01110", "00100", "00100", "00000"),
    "$": ("00100", "01111", "10100", "01110", "00101", "11110", "00100"),
    "=": ("00000", "00000", "11111", "00000", "11111", "00000", "00000"),
    "*": ("00000", "10101", "01110", "11111", "01110", "10101", "00000"),
    "#": ("01010", "01010", "11111", "01010", "11111", "01010", "01010"),
    "<": ("00010", "00100", "01000", "10000", "01000", "00100", "00010"),
    ">": ("01000", "00100", "00010", "00001", "00010", "00100", "01000"),
}

# ------------------------------------------------------------- canvas -----
class Canvas:
    def __init__(self, w, h, bg):
        self.w, self.h = w, h
        self.px = bytearray(bg * w * h)

    def set(self, x, y, colour):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i:i + 3] = bytes(colour)

    def rect(self, x, y, w, h, colour):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self.set(xx, yy, colour)

    def hline(self, x, y, w, colour, t=1):
        self.rect(x, y, w, t, colour)

    def vline(self, x, y, h, colour, t=1):
        self.rect(x, y, t, h, colour)

    def text(self, x, y, s, scale, colour):
        s = s.upper()
        cx = x
        for ch in s:
            glyph = GLYPHS.get(ch, GLYPHS["?"])
            for r, row in enumerate(glyph):
                for c, bit in enumerate(row):
                    if bit == "1":
                        self.rect(cx + c * scale, y + r * scale,
                                  scale, scale, colour)
            cx += 6 * scale
        return cx

    def text_w(self, s, scale):
        return len(s) * 6 * scale - scale

    def centre(self, y, s, scale, colour):
        self.text((self.w - self.text_w(s, scale)) // 2, y, s, scale, colour)

    def wrap(self, x, y, s, scale, max_w, colour, leading=None):
        """Greedy word wrap; returns the y just below the last line."""
        if leading is None:
            leading = 7 * scale + 4
        words = s.upper().split()
        line, cy = "", y
        for word in words:
            trial = (line + " " + word).strip()
            if self.text_w(trial, scale) <= max_w:
                line = trial
            else:
                if line:
                    self.text(x, cy, line, scale, colour)
                    cy += leading
                line = word
        if line:
            self.text(x, cy, line, scale, colour)
            cy += leading
        return cy


# -------------------------------------------------------------- picture ----
def draw_sea_scene(cv, x, y, w, h):
    """A stylised Gulf of Finland scene: sky, sun, sea and a cargo ship."""
    cv.rect(x, y, w, h, SKY)
    # sun
    cv.rect(x + w - 130, y + 22, 54, 54, GOLD)
    # distant clouds
    for cx, cw in ((x + 40, 150), (x + 260, 110), (x + 480, 170)):
        cv.rect(cx, y + 30, cw, 14, PAPER)
        cv.rect(cx + 24, y + 18, cw - 60, 12, PAPER)
    # sea
    sea_y = y + int(h * 0.62)
    cv.rect(x, sea_y, w, h - int(h * 0.62), SEA)
    for wy in range(sea_y + 12, y + h - 8, 20):
        cv.rect(x + 30, wy, 180, 4, (120, 180, 215))
        cv.rect(x + w - 260, wy + 9, 200, 4, (120, 180, 215))
    # cargo ship
    sx, sy = x + 300, sea_y - 6
    cv.rect(sx, sy - 58, 330, 58, (32, 34, 38))          # hull
    cv.rect(sx + 330, sy - 58, 46, 20, (32, 34, 38))     # bow
    cv.rect(sx + 40, sy - 96, 90, 38, (200, 205, 210))   # bridge
    cv.rect(sx + 52, sy - 88, 66, 8, NAVY)               # bridge windows
    cv.rect(sx + 150, sy - 78, 130, 20, RED)             # containers
    cv.rect(sx + 150, sy - 58, 130, 20, GOLD)
    cv.rect(sx + 292, sy - 78, 38, 20, STEEL)
    for px in range(sx + 20, sx + 320, 28):               # portholes
        cv.rect(px, sy - 34, 8, 8, (200, 205, 210))
    cv.rect(sx + 58, sy - 116, 10, 20, INK)              # funnel
    # drone dots above the ship
    for dx, dy in ((120, -100), (180, -112), (240, -96)):
        cv.rect(sx + dx, sy + dy, 8, 8, INK)
        cv.rect(sx + dx - 6, sy + dy + 3, 20, 2, INK)
    # frame
    cv.rect(x, y, w, 3, INK)
    cv.rect(x, y + h - 3, w, 3, INK)
    cv.rect(x, y, 3, h, INK)
    cv.rect(x + w - 3, y, 3, h, INK)


# ---------------------------------------------------------------- png ------
def _chunk(kind, data):
    out = struct.pack(">I", len(data)) + kind + data
    out += struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
    return out


def write_png(cv, path):
    raw = bytearray()
    for yy in range(cv.h):
        raw.append(0)
        raw += cv.px[yy * cv.w * 3:(yy + 1) * cv.w * 3]
    ihdr = struct.pack(">IIBBBBB", cv.w, cv.h, 8, 2, 0, 0, 0)
    png = b"\x89PNG\r\n\x1a\n"
    png += _chunk(b"IHDR", ihdr)
    png += _chunk(b"IDAT", zlib.compress(bytes(raw), 6))
    png += _chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)


# -------------------------------------------------------------- layout -----
def build(path):
    cv = Canvas(W, H, PAPER)
    mx = 36                      # margin
    cw = W - 2 * mx              # content width

    # ---- masthead ----
    cv.centre(26, "THE WORLD TODAY", 7, INK)
    cv.hline(mx, 96, cw, INK, 3)
    cv.centre(106, "WEDNESDAY 25 NOVEMBER 2026", 2, RED)
    cv.centre(128, "ONE IMAGE  -  THE WHOLE WORLD  -  FREE", 1, GREY)
    cv.hline(mx, 148, cw, INK, 5)
    cv.hline(mx, 157, cw, INK, 1)

    # ---- lead story ----
    y = 172
    cv.text(mx, y, "LEAD STORY", 1, RED)
    y += 16
    y = cv.wrap(mx, y, "ZELENSKIY CONFIRMS UKRAINE HIT RUSSIAN SHIP IN GULF OF FINLAND", 4, cw, INK)
    y += 6
    y = cv.wrap(mx, y,
                "President Volodymyr Zelenskiy said Kyiv was behind Saturday's drone "
                "strike on a Russian cargo vessel. Ally Norway urged caution over "
                "such operations as the war at sea widens.", 2, cw, INK)
    y += 10

    # ---- picture ----
    draw_sea_scene(cv, mx, y, cw, 200)
    pic_bottom = y + 200
    cv.text(mx, pic_bottom + 8,
            "A CARGO SHIP IN THE GULF OF FINLAND, AFTER SATURDAY'S DRONE STRIKE.",
            1, GREY)

    # ---- three columns ----
    col_y = pic_bottom + 34
    col_w = (cw - 48) // 3
    cols = [
        ("MIDDLE EAST",
         "HOUTHIS HIT RIYADH TOWER, 11 WOUNDED",
         "Saudi civil defence said eleven people were hurt when a Houthi drone "
         "struck the capital's tallest tower. The Saudi-led coalition condemned "
         "the attack as Yemeni government forces said Aden would not fall."),
        ("WASHINGTON",
         "TRUMP AWARDS GIULIANI MEDAL OF FREEDOM",
         "Donald Trump presented former New York mayor Rudy Giuliani with the "
         "Presidential Medal of Freedom, the nation's highest civilian honour, "
         "in a White House ceremony."),
        ("TECHNOLOGY",
         "HUAWEI GUILTY OF TRADE SECRET THEFT",
         "A US jury convicted China's Huawei of stealing trade secrets in a "
         "sprawling criminal trial, but acquitted the company of racketeering. "
         "The verdict closes one chapter of a long-running case."),
    ]
    for i, (kicker, head, body) in enumerate(cols):
        x = mx + i * (col_w + 24)
        cv.text(x, col_y, kicker, 1, RED)
        yy = cv.wrap(x, col_y + 16, head, 2, col_w, INK)
        cv.wrap(x, yy + 4, body, 1, col_w, INK)
        if i < 2:
            cv.vline(x + col_w + 12, col_y, 210, LIGHT, 1)

    # ---- lower strip: sport, business, world ----
    strip_y = col_y + 232
    cv.hline(mx, strip_y, cw, INK, 2)
    strip_y += 14
    lower = [
        ("SPORT",
         "ENGLAND LEVEL T20 SERIES",
         "England beat Australia by eight wickets in the second T20 international, "
         "chasing 185 to level the five-match series."),
        ("BUSINESS",
         "DELL LIFTS FORECASTS ON AI BOOM",
         "Dell raised its annual forecasts after a record quarter driven by "
         "surging AI server demand. Nvidia shares fell 7 percent."),
        ("WORLD IN BRIEF",
         "NATO JETS FOR POLAND, NEPAL QUAKE",
         "NATO plans early-warning aircraft for Poland. A 5.6-magnitude quake "
         "hit Nepal's Koshi province. France ordered Sarkozy's case to trial."),
    ]
    for i, (kicker, head, body) in enumerate(lower):
        x = mx + i * (col_w + 24)
        cv.text(x, strip_y, kicker, 1, RED)
        yy = cv.wrap(x, strip_y + 16, head, 2, col_w, INK)
        cv.wrap(x, yy + 4, body, 1, col_w, INK)
        if i < 2:
            cv.vline(x + col_w + 12, strip_y, 130, LIGHT, 1)

    # ---- footer ----
    fy = H - 44
    cv.hline(mx, fy, cw, INK, 3)
    cv.centre(fy + 10, "THE WORLD TODAY  -  WEDNESDAY 25 NOVEMBER 2026  -  PRINTED IN ONE IMAGE",
              1, GREY)

    write_png(cv, path)


def output_path():
    """Where the finished image goes.

    Grade time runs in a sandbox where the judge reads only
    /output/entry.png, so that is the default.  For local verification
    the directory can be overridden with MAKEFUN_OUTPUT_DIR; the
    directory is created if it does not exist.
    """
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    return os.path.join(out_dir, "entry.png")


if __name__ == "__main__":
    path = output_path()
    build(path)
    print(f"wrote {path}")
