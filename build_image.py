#!/usr/bin/env python3
"""Build the 19 Nov 2026 front page: hero illustration + accurate headlines.

Deterministic: no timestamps, no randomness, no network. Output entry.png 1024x1024.
Run: python3 build_image.py
"""
from PIL import Image, ImageDraw, ImageFont
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_I = "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf"

W, H = 1024, 1024
M = 36
PAPER = (245, 238, 220)
INK = (18, 24, 38)
RED = (178, 34, 28)
GREY = (88, 88, 84)
SUMMARY_INK = (52, 52, 48)
RULE_LIGHT = (200, 190, 165)
CAPTION_Y = 622

# Stories: (kicker, headline, summary)
STORIES = [
    ("SUMMIT", "Trump, Xi and Putin meet\nin Shenzhen",
     "The three leaders held their first three-way summit, with Ukraine and Iran on the agenda."),
    ("UKRAINE", "Crimea Bridge hit for a\nthird time in a week",
     "Ukraine struck the Kerch Bridge again; traffic across the strait was suspended."),
    ("GULF", "Iran strikes Gulf states;\ntanker hit in Hormuz",
     "Tehran fired at US bases in Kuwait and Bahrain after the US hit Qeshm Island."),
    ("COURT", "World court rules on\nRohingya genocide case",
     "The ICJ ruled Thursday on Gambia's case accusing Myanmar of genocide."),
    ("BANGLADESH", "Yunus's home torched;\n28 districts in violence",
     "Attackers set fire to Muhammad Yunus's ancestral home as unrest spread."),
    ("MARKETS", "Anthropic prices record\nIPO at $83 a share",
     "The AI firm priced its Nasdaq debut above its range, the biggest AI listing yet."),
]


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap: return the lines that fit within width pixels."""
    lines, cur = [], ""
    for word in text.split():
        t = (cur + " " + word).strip()
        if draw.textlength(t, font=fnt) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_masthead(d):
    d.text((M, 22), "T H E   W O R L D   I N   O N E   I M A G E", font=font(SANS_B, 19), fill=RED)
    d.text((M, 48), "19 NOVEMBER 2026", font=font(SERIF_B, 62), fill=INK)
    d.text((M, 118), "Thursday  •  Shenzhen summit  •  Crimea Bridge  •  Gulf strikes", font=font(SANS, 19), fill=GREY)
    d.line([(M, 148), (W - M, 148)], fill=INK, width=3)
    d.line([(M, 153), (W - M, 153)], fill=INK, width=1)


def draw_hero(img, d):
    """Hero illustration, cropped to fill 1024x452, with the caption below it."""
    hero = Image.open(os.path.join(HERE, "media-generation-news-hero-20261119-0.png")).convert("RGB")
    hw, hh = hero.size
    target_w, target_h = W - 2 * M, 452
    scale = max(target_w / hw, target_h / hh)
    hero2 = hero.resize((int(hw * scale), int(hh * scale)), Image.LANCZOS)
    x0 = (hero2.width - target_w) // 2
    y0 = (hero2.height - target_h) // 2
    img.paste(hero2.crop((x0, y0, x0 + target_w, y0 + target_h)), (M, 162))
    d.rectangle([(M, 162), (W - M, 162 + target_h)], outline=INK, width=2)
    d.text((M, CAPTION_Y), "A three-way summit, a bridge hit again and strikes across the Gulf — the world on 19 November 2026.",
           font=font(SANS_I, 16), fill=GREY)


def draw_stories(d):
    """Six stories in a 2-column x 3-row grid, each with kicker, headline, summary."""
    col_w = (W - 2 * M - 28) // 2
    row_h = 112
    top = 652
    for i, (kick, head, summ) in enumerate(STORIES):
        col = i % 2
        row = i // 2
        x = M + col * (col_w + 28)
        y = top + row * row_h
        d.text((x, y), kick, font=font(SANS_B, 15), fill=RED)
        yy = y + 22
        for line in head.split("\n"):
            d.text((x, yy), line, font=font(SERIF_B, 21), fill=INK)
            yy += 25
        # summary, wrapped to 2 lines max
        lines = wrap(d, summ, font(SANS, 15), col_w)[:2]
        for line in lines:
            d.text((x, yy), line, font=font(SANS, 15), fill=SUMMARY_INK)
            yy += 19
        if row < 2:
            d.line([(x, y + row_h - 14), (x + col_w, y + row_h - 14)], fill=RULE_LIGHT, width=1)


def draw_footer(d):
    d.line([(M, 992), (W - M, 992)], fill=INK, width=1)
    d.text((M, 1000), "Sources: Reuters · AP · AFP · BBC — 19 Nov 2026", font=font(SANS, 13), fill=GREY)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_masthead(d)
    draw_hero(img, d)
    draw_stories(d)
    draw_footer(d)
    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG", optimize=True)
    print(out, img.size, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
