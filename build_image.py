"""Build the 19 November 2026 front page (1024x1024) for the make.fun
news-image bounty. Dense broadsheet: masthead, hero band, a numbers
strip, thirty dated stories in three columns, and a DATE CHECK box.

Run:  python3 build_image.py   ->  writes entry.png next to this file.
The render is deterministic: same inputs, same bytes, every run.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
HERO_PATH = HERE / "hero.png"
OUT_PATH = HERE / "entry.png"

PAGE = 1024
MARGIN = 20
INK = (24, 32, 54)
PAPER = (243, 236, 217)
GOLD = (168, 124, 42)
FADED = (92, 96, 110)
RULE = (150, 138, 112)

SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
COND = "/usr/share/fonts/truetype/noto/NotoSans-Condensed.ttf"
COND_BOLD = "/usr/share/fonts/truetype/noto/NotoSans-CondensedBold.ttf"
FALLBACK = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FALLBACK_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def load_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        bold = "Bold" in path or "bold" in path
        return ImageFont.truetype(FALLBACK_BOLD if bold else FALLBACK, size)


MASTHEAD = "19 NOVEMBER 2026"
SUBLINE = "Thursday  ·  Shenzhen peace declaration  ·  Genocide ruling  ·  Hormuz tankers burn"
CAPTION = ("A three-way summit in Shenzhen, a genocide verdict in The Hague and tankers "
           "ablaze in the Gulf — thirty stories first reported on 19 November 2026.")
NUMBERS = ("9–6  ICJ vote   ·   ~900,000  AI chips cleared   ·   11  crew injured   ·   "
           "€45bn  EU loan   ·   51–48  Senate vote   ·   $190.4m  Van Gogh")
DATE_CHECK = ("DATE CHECK — all 30 stories above were first reported on Thursday "
              "19 November 2026. Left out as earlier news: the US strike on Qeshm "
              "Island (18 Nov) and the Shenzhen summit announcement (18 Nov).")
FOOTER = "Sources: Reuters · AP · AFP · BBC · Al Jazeera — 19 Nov 2026"

# (region tag, headline, one-line summary) — every item first reported 19 Nov 2026.
STORIES = [
    ("SUMMIT", "Trump, Xi and Putin issue peace declaration in Shenzhen",
     "Four-point “Declaration toward Peace” after the first three-way summit; the Ukraine and Iran wars go unmentioned."),
    ("COURT", "World Court rules Myanmar committed genocide",
     "ICJ votes 9–6 in Gambia v. Myanmar — the first genocide finding against a state."),
    ("GULF", "Tankers burn as Hormuz attacks mount",
     "ADNOC vessel hit, 11 crew hurt and one missing; three tankers disabled by mines east of the strait."),
    ("MARKETS", "Anthropic debuts at about $2 trillion valuation",
     "Nasdaq listing edges past SpaceX’s June debut as the AI boom faces Wall Street’s test."),
    ("UKRAINE", "Crimea Bridge hit for third time in a week",
     "The Kerch crossing is struck again and traffic across the strait is suspended."),
    ("EUROPE", "EU proposes €45 billion loan for Ukraine",
     "European Commission floats a new package as the war-funding debate widens."),
    ("BANGLADESH", "Yunus’s ancestral home torched",
     "Violence spreads across 28 districts as the unrest deepens."),
    ("CLIMATE", "COP31 ministers race to unblock Antalya talks",
     "An informal session hunts for a final text as differences persist."),
    ("ENERGY", "IEA: Hormuz crisis is gravest threat to energy security",
     "The annual report calls the Middle East crisis the worst ever observed."),
    ("SENEGAL", "Migrant boat capsizes off Senegal",
     "A wooden boat carrying about 100 people hits rocks overnight; dozens are missing."),
    ("TECH", "US cleared roughly 900,000 AI chips for Chinese firms",
     "The House Foreign Affairs Committee publishes Commerce Department license records."),
    ("TECH", "Nvidia halts top China chip sales",
     "A congressional commission says the PLA seeks Nvidia’s most advanced processors."),
    ("AVIATION", "Lawmakers urge blocking Chinese aircraft certification",
     "A report targets Chinese planes and Western makers that operate in China."),
    ("UK", "Burnham heads to Brussels for EU reset summit",
     "The prime minister is due Friday for talks on easing Brexit damage."),
    ("ASIA", "India to host Japanese live-fire missile drills",
     "A first: Japanese troops may hold live-fire training on Indian ranges."),
    ("INDIA", "Gandhi: boycotting elections undermines democracy",
     "The Congress leader warns against election boycotts at a University of Chicago event."),
    ("AMERICAS", "Hegseth unveils military pact with Venezuela",
     "The partnership covers training and intelligence cooperation."),
    ("GAZA", "IDF ends Nuseirat operation",
     "The invasion of the central Gaza camp ends after one day; four killed on Thursday."),
    ("YEMEN", "Taiz water production halved, 800,000 cut off",
     "UNICEF warns the besieged city is reeling as fighting tightens the siege."),
    ("IRAQ", "Baghdad reaches deal with Kata’ib Hezbollah",
     "The agreement ends the standoff in the town of Jurf al-Sakhar."),
    ("PAKISTAN", "22 militants killed in Khyber Pakhtunkhwa raids",
     "The military claims strikes on Pakistani Taliban over two days."),
    ("MONGOLIA", "Parliament accepts president’s resignation",
     "The State Great Khural approves Khürelsükh’s departure."),
    ("US", "Senate rejects Iran war-powers resolution 51–48",
     "H.Con.Res.93 had passed the House; three Republicans backed it."),
    ("UKRAINE", "UK and Norway fund £100m naval craft programme",
     "Two vessels to be built in the UK under the Maritime Capability Coalition."),
    ("SERBIA", "Cupic elected parliament speaker 140–97",
     "The Student List candidate beats Stojan Radenovic on the sitting’s third day."),
    ("SAUDI", "PIF tower damaged by intercepted Houthi rocket debris",
     "The Riyadh financial-district tower is hit in an overnight attack."),
    ("KUWAIT", "Kuwait repels first Iranian attack in two months",
     "The Gulf state intercepts as regional strikes widen."),
    ("ASIA", "Russian bombers return to Vietnam",
     "The deployment comes amid rising regional tensions."),
    ("AFRICA", "Ethiopia and Eritrea mass troops on border",
     "The build-up raises fears of a renewed conflict."),
    ("CULTURE", "Van Gogh sells for $190.4 million, an artist record",
     "The auction sets a new benchmark for the painter’s work."),
]


def wrap(draw, text, font, max_width):
    """Greedy word wrap; returns a list of lines that fit max_width."""
    lines, current = [], ""
    for word in text.split():
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=font) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def fit_story(draw, tag, headline, summary, width, max_height):
    """Pick the largest type sizes whose wrapped block fits max_height."""
    for head_size, sum_size in ((15, 11), (14, 11), (13, 10), (12, 10)):
        tag_font = load_font(SANS_BOLD, 10)
        head_font = load_font(COND_BOLD, head_size)
        sum_font = load_font(COND, sum_size)
        head_lines = wrap(draw, headline, head_font, width)
        sum_lines = wrap(draw, summary, sum_font, width)
        height = 13 + len(head_lines) * (head_size + 2) + len(sum_lines) * (sum_size + 2)
        if height <= max_height:
            return tag_font, head_font, sum_font, head_lines, sum_lines
    # Last resort: smallest sizes, hard-truncate the summary to two lines.
    head_font = load_font(COND_BOLD, 12)
    sum_font = load_font(COND, 10)
    head_lines = wrap(draw, headline, head_font, width)[:2]
    sum_lines = wrap(draw, summary, sum_font, width)[:2]
    return load_font(SANS_BOLD, 10), head_font, sum_font, head_lines, sum_lines


def draw_story(draw, x, y, width, row_height, story):
    tag, headline, summary = story
    tag_font, head_font, sum_font, head_lines, sum_lines = fit_story(
        draw, tag, headline, summary, width, row_height - 4)
    draw.text((x, y), tag, font=tag_font, fill=GOLD)
    cy = y + 13
    for line in head_lines:
        draw.text((x, cy), line, font=head_font, fill=INK)
        cy += head_font.size + 2
    for line in sum_lines:
        draw.text((x, cy), line, font=sum_font, fill=FADED)
        cy += sum_font.size + 2


def build():
    img = Image.new("RGB", (PAGE, PAGE), PAPER)
    draw = ImageDraw.Draw(img)
    left, right = MARGIN, PAGE - MARGIN
    width = right - left

    # Masthead
    title_font = load_font(SERIF_BOLD, 46)
    sub_font = load_font(COND_BOLD, 16)
    draw.line([(left, 14), (right, 14)], fill=INK, width=3)
    tw = draw.textlength(MASTHEAD, font=title_font)
    draw.text(((PAGE - tw) / 2, 20), MASTHEAD, font=title_font, fill=INK)
    sw = draw.textlength(SUBLINE, font=sub_font)
    draw.text(((PAGE - sw) / 2, 76), SUBLINE, font=sub_font, fill=GOLD)
    draw.line([(left, 100), (right, 100)], fill=INK, width=2)

    # Hero band (centre-crop the banner to the band's aspect)
    hero_top, hero_h = 108, 152
    hero = Image.open(HERO_PATH).convert("RGB")
    target_ratio = width / hero_h
    src_ratio = hero.width / hero.height
    if src_ratio > target_ratio:
        new_w = int(hero.height * target_ratio)
        x0 = (hero.width - new_w) // 2
        hero = hero.crop((x0, 0, x0 + new_w, hero.height))
    else:
        new_h = int(hero.width / target_ratio)
        y0 = (hero.height - new_h) // 2
        hero = hero.crop((0, y0, hero.width, y0 + new_h))
    hero = hero.resize((width, hero_h), Image.LANCZOS)
    img.paste(hero, (left, hero_top))
    draw.rectangle([left, hero_top, right, hero_top + hero_h], outline=INK, width=2)

    cap_font = load_font(COND, 13)
    cap_lines = wrap(draw, CAPTION, cap_font, width)
    cy = hero_top + hero_h + 5
    for line in cap_lines[:1]:
        draw.text((left, cy), line, font=cap_font, fill=FADED)
        cy += 15

    # Numbers strip
    strip_top = cy + 3
    draw.rectangle([left, strip_top, right, strip_top + 24], fill=INK)
    num_font = load_font(COND_BOLD, 13)
    nw = draw.textlength(NUMBERS, font=num_font)
    draw.text(((PAGE - nw) / 2, strip_top + 5), NUMBERS, font=num_font, fill=PAPER)

    # Story grid: 3 columns x 10 rows
    grid_top = strip_top + 32
    grid_bottom = 892
    rows, cols = 10, 3
    row_h = (grid_bottom - grid_top) // rows
    gap = 14
    col_w = (width - gap * (cols - 1)) // cols
    for idx, story in enumerate(STORIES[: rows * cols]):
        col, row = divmod(idx, rows)
        x = left + col * (col_w + gap)
        y = grid_top + row * row_h
        draw_story(draw, x, y, col_w, row_h, story)
        if row < rows - 1:
            draw.line([(x, y + row_h - 3), (x + col_w, y + row_h - 3)], fill=RULE, width=1)

    # DATE CHECK box
    box_top = 900
    draw.rectangle([left, box_top, right, box_top + 56], outline=GOLD, width=2)
    dc_font = load_font(COND_BOLD, 12)
    dc_lines = wrap(draw, DATE_CHECK, dc_font, width - 16)
    cy = box_top + 6
    for line in dc_lines[:3]:
        draw.text((left + 8, cy), line, font=dc_font, fill=INK)
        cy += 15

    # Footer
    draw.line([(left, 966), (right, 966)], fill=INK, width=2)
    foot_font = load_font(COND, 13)
    fw = draw.textlength(FOOTER, font=foot_font)
    draw.text(((PAGE - fw) / 2, 974), FOOTER, font=foot_font, fill=FADED)

    img.save(OUT_PATH, format="PNG", optimize=True)
    print(f"wrote {OUT_PATH} ({OUT_PATH.stat().st_size} bytes)")


if __name__ == "__main__":
    build()
