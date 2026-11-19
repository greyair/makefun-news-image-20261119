#!/usr/bin/env python3
"""Build the 19 Nov 2026 front page: hero illustration + accurate headlines.

Deterministic: no timestamps, no randomness, no network. Output entry.png 1024x1024.
Run: python3 build_image.py
"""
from PIL import Image, ImageDraw, ImageFont
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

FONTS = {
    "serif_bold": "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
    "sans_bold": "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "sans": "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "sans_italic": "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf",
}

PAGE_W, PAGE_H = 1024, 1024
MARGIN = 36
PAPER_BG = (245, 238, 220)
INK = (18, 24, 38)
ACCENT = (178, 34, 28)
MUTED = (88, 88, 84)
BODY_INK = (52, 52, 48)
HAIRLINE = (200, 190, 165)
CAPTION_TOP = 622
HERO_TOP = 162
HERO_HEIGHT = 452
GRID_TOP = 652
ROW_HEIGHT = 112
FOOTER_RULE_Y = 992
FOOTER_TEXT_Y = 1000

# Articles: tag, title (with explicit line break), body
ARTICLES = [
    {"tag": "SUMMIT", "title": "Trump, Xi and Putin meet\nin Shenzhen",
     "body": "The three leaders held their first three-way summit, with Ukraine and Iran on the agenda."},
    {"tag": "UKRAINE", "title": "Crimea Bridge hit for a\nthird time in a week",
     "body": "Ukraine struck the Kerch Bridge again; traffic across the strait was suspended."},
    {"tag": "GULF", "title": "Iran strikes Gulf states;\ntanker hit in Hormuz",
     "body": "Tehran fired at US bases in Kuwait and Bahrain after the US hit Qeshm Island."},
    {"tag": "COURT", "title": "World court rules on\nRohingya genocide case",
     "body": "The ICJ ruled Thursday on Gambia's case accusing Myanmar of genocide."},
    {"tag": "BANGLADESH", "title": "Yunus's home torched;\n28 districts in violence",
     "body": "Attackers set fire to Muhammad Yunus's ancestral home as unrest spread."},
    {"tag": "MARKETS", "title": "Anthropic prices record\nIPO at $83 a share",
     "body": "The AI firm priced its Nasdaq debut above its range, the biggest AI listing yet."},
]


def load_font(name, size):
    return ImageFont.truetype(FONTS[name], size)


def wrap_text(canvas, text, fnt, width):
    """Greedy word wrap: return the lines that fit within width pixels."""
    lines, current = [], ""
    for word in text.split():
        trial = (current + " " + word).strip()
        if canvas.textlength(trial, font=fnt) <= width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def render_masthead(canvas):
    canvas.text((MARGIN, 22), "T H E   W O R L D   I N   O N E   I M A G E", font=load_font("sans_bold", 19), fill=ACCENT)
    canvas.text((MARGIN, 48), "19 NOVEMBER 2026", font=load_font("serif_bold", 62), fill=INK)
    canvas.text((MARGIN, 118), "Thursday  •  Shenzhen summit  •  Crimea Bridge  •  Gulf strikes", font=load_font("sans", 19), fill=MUTED)
    canvas.line([(MARGIN, 148), (PAGE_W - MARGIN, 148)], fill=INK, width=3)
    canvas.line([(MARGIN, 153), (PAGE_W - MARGIN, 153)], fill=INK, width=1)


def render_hero(page, canvas):
    """Hero illustration, cropped to fill the banner, with the caption below it."""
    hero = Image.open(os.path.join(BASE_DIR, "media-generation-news-hero-20261119-0.png")).convert("RGB")
    hw, hh = hero.size
    target_w, target_h = PAGE_W - 2 * MARGIN, HERO_HEIGHT
    scale = max(target_w / hw, target_h / hh)
    scaled = hero.resize((int(hw * scale), int(hh * scale)), Image.LANCZOS)
    x0 = (scaled.width - target_w) // 2
    y0 = (scaled.height - target_h) // 2
    page.paste(scaled.crop((x0, y0, x0 + target_w, y0 + target_h)), (MARGIN, HERO_TOP))
    canvas.rectangle([(MARGIN, HERO_TOP), (PAGE_W - MARGIN, HERO_TOP + target_h)], outline=INK, width=2)
    canvas.text((MARGIN, CAPTION_TOP), "A three-way summit, a bridge hit again and strikes across the Gulf — the world on 19 November 2026.",
                font=load_font("sans_italic", 16), fill=MUTED)


def render_articles(canvas):
    """Six articles in a 2-column x 3-row grid, each with tag, title, body."""
    col_w = (PAGE_W - 2 * MARGIN - 28) // 2
    for i, article in enumerate(ARTICLES):
        col = i % 2
        row = i // 2
        x = MARGIN + col * (col_w + 28)
        y = GRID_TOP + row * ROW_HEIGHT
        canvas.text((x, y), article["tag"], font=load_font("sans_bold", 15), fill=ACCENT)
        yy = y + 22
        for line in article["title"].split("\n"):
            canvas.text((x, yy), line, font=load_font("serif_bold", 21), fill=INK)
            yy += 25
        # body, wrapped to 2 lines max
        lines = wrap_text(canvas, article["body"], load_font("sans", 15), col_w)[:2]
        for line in lines:
            canvas.text((x, yy), line, font=load_font("sans", 15), fill=BODY_INK)
            yy += 19
        if row < 2:
            canvas.line([(x, y + ROW_HEIGHT - 14), (x + col_w, y + ROW_HEIGHT - 14)], fill=HAIRLINE, width=1)


def render_footer(canvas):
    canvas.line([(MARGIN, FOOTER_RULE_Y), (PAGE_W - MARGIN, FOOTER_RULE_Y)], fill=INK, width=1)
    canvas.text((MARGIN, FOOTER_TEXT_Y), "Sources: Reuters · AP · AFP · BBC — 19 Nov 2026", font=load_font("sans", 13), fill=MUTED)


def build_front_page():
    page = Image.new("RGB", (PAGE_W, PAGE_H), PAPER_BG)
    canvas = ImageDraw.Draw(page)
    render_masthead(canvas)
    render_hero(page, canvas)
    render_articles(canvas)
    render_footer(canvas)
    out = os.path.join(BASE_DIR, "entry.png")
    page.save(out, "PNG", optimize=True)
    print(out, page.size, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    build_front_page()
