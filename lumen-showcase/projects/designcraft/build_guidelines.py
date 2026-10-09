"""Lumen Coffee Roasters — Brand Guidelines v1.0 (12 pages, A4 landscape), laid out in designcraft.

Places artwork from the other crafts: vectorcraft PDF pages (vector), photocraft hero, lightcraft selects,
effectcraft frames. Run:  python -I -X utf8 build_guidelines.py <designcraft-cli.exe>
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from mcpclient import Craft  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.dirname(HERE)
OUT = os.path.join(HERE, "out")
VEC_PDF = os.path.join(P, "vectorcraft", "out", "lumen-identity-presentation.pdf")
HERO = os.path.join(P, "photocraft", "out", "lumen-ember-ridge-hero-master.png")
STORY = os.path.join(P, "photocraft", "out", "social", "story", "ember-ridge-story-post.jpg")
LC = os.path.join(P, "lightcraft", "out", "web-jpeg-srgb-2048")
FXR = os.path.join(P, "effectcraft", "out", "review")
PW, PH, M, BL = 842, 595, 48, 8.5

c = None


def ex(cmd, p=None):
    return c.call("execute", {"command": cmd, "params": p or {}})


def tf(sp, rect, text, style, cols=None):
    f = ex("frame.create", {"spread": sp, "rect": rect, "content": "text", "text": text})
    ex("selection.set", {"ids": [f["id"]]})
    ex("style.paragraph.apply", {"name": style, "clearOverrides": True})
    if cols:
        ex("object.textFrameOptions", {"columns": cols, "gutter": 18, "ids": [f["id"]]})
    return f


def box(sp, rect, swatch):
    f = ex("frame.create", {"spread": sp, "rect": rect, "content": "unassigned"})
    ex("object.fill", {"swatch": swatch, "ids": [f["id"]]})
    ex("object.stroke", {"swatch": "[None]", "weight": 0, "ids": [f["id"]]})
    return f


def img(sp, rect, path, mode="fillProportionally", pdf_page=None):
    f = ex("frame.create", {"spread": sp, "rect": rect, "content": "graphic"})
    p = {"path": path, "frame": f["id"]}
    if pdf_page:
        p["pdfPage"] = pdf_page
        p["pdfCrop"] = "trim"
    ex("file.place", p)
    ex("object.fit", {"mode": mode, "ids": [f["id"]]})
    ex("object.stroke", {"swatch": "[None]", "weight": 0, "ids": [f["id"]]})
    return f


def rule(sp, y, x0=M, x1=PW - M, swatch="Lumen Ember", w=0.75):
    l = ex("line.create", {"spread": sp, "a": [x0, y], "b": [x1, y]})
    ex("object.stroke", {"swatch": swatch, "weight": w, "ids": [l["id"]]})
    return l


def header(sp, kicker, title, style="H1"):
    tf(sp, [M, M, PW - M, M + 14], kicker, "Kicker")
    tf(sp, [M, M + 16, PW - M, M + 60], title, style)
    rule(sp, M + 66)


def footer(sp, n):
    rule(sp, PH - 34, swatch="Lumen Clay", w=0.4)
    tf(sp, [M, PH - 30, 420, PH - 18], "Lumen Coffee Roasters  ·  Brand Guidelines v1.0  ·  October 2026", "Footer")
    tf(sp, [PW - M - 60, PH - 30, PW - M, PH - 18], f"{n:02d}", "Folio")


def main(exe):
    global c
    os.makedirs(os.path.join(OUT, "pages"), exist_ok=True)
    c = Craft([exe, "mcp"])
    log = {}
    ex("file.new", {"width": PW, "height": PH, "pages": 12, "facingPages": False, "margins": M, "columns": 12,
                    "gutter": 12, "bleed": BL, "title": "Lumen Brand Guidelines v1.0"})
    for name, cmyk in (("Lumen Roast", (60, 72, 75, 82)), ("Lumen Ember", (0, 58, 88, 0)), ("Lumen Gold", (0, 27, 92, 0)),
                       ("Lumen Crema", (0, 5, 14, 0)), ("Lumen Clay", (22, 58, 72, 10))):
        ex("swatch.create", {"name": name, "color": dict(zip("cmyk", cmyk)), "spot": name == "Lumen Ember"})

    lead = lambda v: {"kind": "points", "value": v}
    styles = {
        "H1": ({"fontFamily": "Bahnschrift", "fontStyle": "Bold", "size": 30, "leading": lead(34), "fill": "Lumen Roast"}, {"spaceAfter": 4}),
        "H1 Plain": ({"fontFamily": "Bahnschrift", "fontStyle": "Bold", "size": 30, "leading": lead(34), "fill": "Lumen Roast"}, {"spaceAfter": 4}),
        "Specimen": ({"fontFamily": "Bahnschrift", "fontStyle": "Bold", "size": 30, "leading": lead(34), "fill": "Lumen Roast"}, {"spaceAfter": 4}),
        "Kicker": ({"fontFamily": "Bahnschrift", "fontStyle": "SemiBold", "size": 8.5, "tracking": 300, "fill": "Lumen Ember",
                    "capitalization": "allCaps"}, {}),
        "Body": ({"fontFamily": "Georgia", "size": 10, "leading": lead(15), "fill": "Lumen Roast"}, {"spaceAfter": 7, "hyphenate": True}),
        "Lead": ({"fontFamily": "Georgia", "fontStyle": "Italic", "size": 15, "leading": lead(21), "fill": "Lumen Clay"}, {"spaceAfter": 10}),
        "Caption": ({"fontFamily": "Bahnschrift", "size": 7.5, "leading": lead(10), "fill": "Lumen Clay"}, {}),
        "Spec": ({"fontFamily": "Bahnschrift", "size": 9, "leading": lead(13.5), "fill": "Lumen Roast"}, {"spaceAfter": 5}),
        "Footer": ({"fontFamily": "Bahnschrift", "size": 7, "tracking": 80, "fill": "Lumen Clay"}, {}),
        "Folio": ({"fontFamily": "Bahnschrift", "fontStyle": "SemiBold", "size": 7, "fill": "Lumen Roast"}, {"align": "right"}),
        "Display": ({"fontFamily": "Georgia", "fontStyle": "Italic", "size": 40, "leading": lead(44), "fill": "Lumen Crema"}, {"align": "center"}),
        "Cover meta": ({"fontFamily": "Bahnschrift", "size": 9, "tracking": 300, "fill": "Lumen Gold", "capitalization": "allCaps"},
                       {"align": "center"}),
    }
    for name, (chars, para) in styles.items():
        log["style:" + name] = ex("style.paragraph.create", {"name": name, "chars": chars, "para": para})

    # 01 Cover
    box(0, [-BL, -BL, PW + BL, PH + BL], "Lumen Roast")
    img(0, [PW / 2 - 150, 70, PW / 2 + 150, 370], VEC_PDF, "fitProportionally", pdf_page=12)
    tf(0, [M, 395, PW - M, 445], "Brand Guidelines", "Display")
    tf(0, [M, 455, PW - M, 470], "Version 1.0  ·  October 2026  ·  For internal and agency use", "Cover meta")

    # 02 Contents
    header(1, "Lumen Coffee Roasters", "Contents", style="H1 Plain")
    footer(1, 2)

    # 03 Brand story
    header(2, "01 · Who we are", "Light, roasted with care")
    tf(2, [M, 130, 400, 200], "Lumen roasts single-origin coffee in small batches and sells it the week it is roasted.", "Lead")
    tf(2, [M, 210, 400, PH - 50],
       "Our name means light. We roast lighter than most, to keep the character of the farm in the cup: fruit, florals and a clean sweetness.\n"
       "Every lot carries its origin on the front of the bag: country, region, process and altitude. We list tasting notes in plain words and show the roast level on a five-step scale.\n"
       "The identity follows the same idea. A sun ring for light, a bean for the craft, and a warm palette taken from the roaster: dark roast, ember, gold and crema.\n"
       "These guidelines show how to use the logo, colour, type, photography, packaging and motion so that every Lumen touchpoint looks like it came from one place.",
       "Body", cols=2)
    img(2, [430, 130, PW - M, PH - 50], HERO)
    tf(2, [430, PH - 46, PW - M, PH - 36], "Hero: Ember Ridge stand-up pouch. Layered composite, photocraft.", "Caption")
    footer(2, 3)

    # 04 Primary logo
    header(3, "02 · Logo", "Primary logo")
    img(3, [M, 130, 330, 412], VEC_PDF, "fitProportionally", pdf_page=1)
    img(3, [360, 160, PW - M, 300], VEC_PDF, "fitProportionally", pdf_page=2)
    tf(3, [M, 420, 330, 470], "Stacked lockup. The first choice for packaging, signage and square formats.", "Spec")
    tf(3, [360, 320, PW - M, 400], "Horizontal lockup. Use it where height is limited: web headers, email, the band of the bag label. "
       "The mark and the wordmark never move relative to each other; use the supplied artwork only.", "Spec")
    footer(3, 4)

    # 05 Variations
    header(4, "02 · Logo", "Variations")
    cells = [(1 + 0, 3, "Mark only. Favicons, stamps, social avatars."), (1, 4, "App icon. Rounded square, Roast background."),
             (1, 5, "One colour. Black, for single-colour print and engraving."), (1, 6, "Reversed. Light wordmark on Lumen Roast.")]
    for i, (_, page, cap) in enumerate(cells):
        x0 = M + i * 189
        img(4, [x0, 130, x0 + 175, 305], VEC_PDF, "fitProportionally", pdf_page=page)
        tf(4, [x0, 315, x0 + 175, 360], cap, "Spec")
    footer(4, 5)

    # 06 Clear space
    header(5, "02 · Logo", "Clear space and minimum size")
    img(5, [M, 125, 400, PH - 50], VEC_PDF, "fitProportionally", pdf_page=7)
    tf(5, [430, 135, PW - M, PH - 60],
       "Clear space: keep an area of X on every side, where X is half the radius of the sun ring.\n"
       "Minimum size: 25 mm wide in print, 120 px wide on screen. Below that, use the mark only.\n"
       "Do not stretch, rotate, recolour outside the palette, add shadows or effects, or place the logo on busy imagery.\n"
       "On photography, place the logo on a calm area and use the reversed version on dark tones.", "Body")
    footer(5, 6)

    # 07 Colour
    header(6, "03 · Colour", "Colour palette")
    img(6, [M, 120, PW - M, 330], VEC_PDF, "fitProportionally", pdf_page=11)
    tf(6, [M, 352, PW - M, 366], "Proportion in a typical layout", "Kicker")
    x = M
    for sw, frac in (("Lumen Roast", 0.55), ("Lumen Crema", 0.25), ("Lumen Clay", 0.08), ("Lumen Ember", 0.08), ("Lumen Gold", 0.04)):
        w = (PW - 2 * M) * frac
        box(6, [x, 372, x + w, 402], sw)
        tf(6, [x, 406, x + w, 418], f"{sw.split()[1]} {int(frac * 100)} %", "Caption")
        x += w
    tf(6, [M, 432, PW - M, PH - 50], "Lumen Ember is a spot colour on packaging (one extra plate) and a process build elsewhere. "
       "Body type is always Lumen Roast on Crema or Crema on Roast; never set body type in Gold.", "Body")
    footer(6, 7)

    # 08 Typography
    header(7, "04 · Typography", "Typography")
    tf(7, [M, 125, 400, 190], "Bahnschrift", "Specimen")
    tf(7, [M, 190, 400, 260], "ABCDEFGHIJKLMNOPQRSTUVWXYZ\nabcdefghijklmnopqrstuvwxyz 0123456789", "Spec")
    tf(7, [M, 265, 400, 330], "Wordmark, headings, labels and data. Bold for headings, SemiBold for labels, Regular for data. "
       "Set labels in capitals with 300 tracking.", "Caption")
    tf(7, [430, 125, PW - M, 190], "Georgia Italic", "Lead")
    tf(7, [430, 170, PW - M, 260], "Georgia carries the voice: origins, tasting notes and longer copy. Italic for origin lines "
       "and pull quotes, Regular for body text at 10/15 pt.", "Body")
    tf(7, [430, 270, PW - M, 285], "Hierarchy", "Kicker")
    tf(7, [430, 290, PW - M, 330], "Ember Ridge", "Specimen")
    tf(7, [430, 330, PW - M, 352], "Ethiopia · Guji · Washed · 2,100 m", "Lead")
    tf(7, [430, 356, PW - M, 400], "Bergamot, ripe apricot, cacao nib. A bright, tea-like cup with a long cocoa finish.", "Body")
    footer(7, 8)

    # 09 Photography
    header(8, "05 · Photography", "Photography")
    pics = ["LUM_0001_wide.jpg", "LUM_0002_label-detail.jpg", "LUM_0003_beans-right.jpg", "LUM_0004_beans-left.jpg"]
    rects = [[M, 125, 470, 400], [480, 125, 620, 400], [630, 125, PW - M, 260], [630, 265, PW - M, 400]]
    for pic, r in zip(pics, rects):
        img(8, r, os.path.join(LC, pic))
    tf(8, [M, 412, PW - M, PH - 50],
       "Look: Lumen Warm Matte (lightcraft preset). White balance 6900 K, tint +4; highlights -18, shadows +10, blacks +8; "
       "colour grading: shadows 30° / 10, highlights 45° / 8; vignette -14; grain 12. Warm, soft contrast, lifted blacks, "
       "never cold or high-contrast. Keep backgrounds calm and let the product sit in a pool of warm light.", "Body")
    footer(8, 9)

    # 10 Packaging
    header(9, "06 · Packaging", "Bag label, 100 × 140 mm")
    img(9, [M, 120, 300, PH - 50], VEC_PDF, "fitProportionally", pdf_page=8)
    img(9, [330, 120, PW - M, 420], HERO)
    tf(9, [330, 430, PW - M, PH - 50],
       "Print: CMYK + Lumen Ember spot, 3 mm bleed, 5 mm safe area, die-cut with 5 mm corner radius. The dieline is a "
       "separate spot plate set to overprint and never prints. Supply the PDF/X-4 from the identity master. "
       "Roast date is stamped in the blank field after roasting.", "Body")
    footer(9, 10)

    # 11 Motion & social
    header(10, "07 · Motion and social", "Motion and social")
    frames = ["Logo_Sting_2.6.png", "Title_Card_Ember_Ridge_2.2.png", "Lower_Third_Mara_2.0.png", "End_Card_2.5.png"]
    for i, fr in enumerate(frames):
        cx, cy = M + (i % 2) * 262, 125 + (i // 2) * 150
        img(10, [cx, cy, cx + 250, cy + 140.6], os.path.join(FXR, fr))
    img(10, [580, 125, 660, 267], STORY)
    tf(10, [670, 125, PW - M, 420],
       "Logo sting 5 s, title card 4 s, lower thirds 6 s, end card 4 s. 1920 × 1080, 30 fps.\n"
       "Deliver H.264 for web and ProRes 4444 with alpha for overlays. The web sting is also a Lottie file.\n"
       "Stories: 1080 × 1920, keep type 250 px clear of the bottom edge.", "Spec")
    footer(10, 11)

    # 12 Back cover
    box(11, [-BL, -BL, PW + BL, PH + BL], "Lumen Roast")
    img(11, [PW / 2 - 60, 180, PW / 2 + 60, 300], VEC_PDF, "fitProportionally", pdf_page=3)
    tf(11, [M, 330, PW - M, 345], "lumen-coffee.example  ·  hello@lumen-coffee.example", "Cover meta")
    tf(11, [M, 360, PW - M, 375], "214 Foundry Lane, Portland, OR 97209  ·  Fictional brand for a production test", "Cover meta")

    # Contents from the H1 headings (with page numbers)
    log["toc"] = ex("toc.generate", {"styles": ["H1"], "title": "", "pageNumbers": True, "page": 2, "rect": [M, 130, 500, PH - 60]})
    log["preflight"] = ex("preflight.run", {"minPpi": 150})
    print("preflight:", json.dumps(log["preflight"])[:800])

    c.call("save_document", {"path": os.path.join(OUT, "lumen-brand-guidelines.designcraft")})
    log["pdf"] = ex("file.exportPdf", {"path": os.path.join(OUT, "lumen-brand-guidelines-v1.0.pdf"), "bookmarksPanel": True,
                                       "tagged": True, "title": "Lumen Brand Guidelines v1.0", "author": "Lumen in-house studio"})
    log["pdf_print"] = ex("file.exportPdf", {"path": os.path.join(OUT, "lumen-brand-guidelines-v1.0_print-x4.pdf"),
                                             "bleed": True, "marks": True, "standard": "x4"})
    log["idml"] = ex("file.exportIdml", {"path": os.path.join(OUT, "lumen-brand-guidelines-v1.0.idml")})
    for i in range(12):
        c.call("export_png", {"page": i, "path": os.path.join(OUT, "pages", f"page-{i + 1:02d}.png")})
    for k in ("pdf", "pdf_print", "idml"):
        print(k, json.dumps(log[k])[:300])
    json.dump(log, open(os.path.join(OUT, "build-log.json"), "w"), indent=1, default=str)
    c.close()


if __name__ == "__main__":
    main(sys.argv[1])
