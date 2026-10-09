"""Lumen 'Ember Ridge' press kit — assembled, authored and finished in pdfcraft.

Inputs: designcraft brand guidelines PDF, vectorcraft identity PDF (logo artwork), photocraft hero, lightcraft select.
Run:  python -I -X utf8 build_presskit.py <pdfcraft-cli.exe>
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from mcpclient import Craft  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.dirname(HERE)
OUT = os.path.join(HERE, "out")
GUIDE = os.path.join(P, "designcraft", "out", "lumen-brand-guidelines-v1.0.pdf")
IDENT = os.path.join(P, "vectorcraft", "out", "lumen-identity-presentation.pdf")
HERO = os.path.join(P, "photocraft", "out", "web", "ember-ridge-hero.jpg")
LABEL = os.path.join(P, "lightcraft", "out", "web-jpeg-srgb-2048", "LUM_0002_label-detail.jpg")
KIT = os.path.join(OUT, "lumen-press-kit-2026-10.pdf")
ROAST, CLAY, EMBER = "#1d1410", "#b06a45", "#f2843a"

RELEASE = (
    "Portland, Oregon, 8 October 2026. Lumen Coffee Roasters today releases Ember Ridge, a washed single-origin "
    "coffee from the Guji zone of southern Ethiopia, grown at 2,100 metres.\n\n"
    "Ember Ridge is roasted light-medium to keep the character of the farm in the cup: bergamot, ripe apricot and "
    "cacao nib, with a bright, tea-like body and a long cocoa finish. It suits filter brewing and espresso.\n\n"
    "\u201cWe roast lighter than most because we want you to taste where the coffee came from,\u201d said Mara Okafor, "
    "Head Roaster at Lumen. \u201cEmber Ridge is the clearest example of that idea we have roasted so far.\u201d\n\n"
    "Ember Ridge is sold as whole bean in 340 g (12 oz) bags, roasted to order and shipped within a week of "
    "roasting. The launch also introduces the new Lumen identity: a sun ring for light and a bean for the craft.\n\n"
    "Press contact: Mara Okafor, mara@lumen-coffee.example, +1 (555) 014-2290. Images and logo artwork follow in "
    "this kit. Lumen Coffee Roasters is a fictional brand created as a production test of the Artcraft tools."
)


def main(exe):
    os.makedirs(os.path.join(OUT, "sections"), exist_ok=True)
    log = {}
    with Craft([exe, "mcp", "--root", P]) as c:
        call = c.call
        # 1 Combine: the 12-page guidelines, then the logo artwork pages from the identity master
        tmp = os.path.join(OUT, "_combined.pdf")
        log["combine"] = call("doc_combine", {"paths": [GUIDE, IDENT], "pages": ["1-12", "1,2,3,4,6,12"], "out": tmp})
        doc = call("doc_open", {"path": tmp})
        d = doc["doc"] if isinstance(doc, dict) and "doc" in doc else doc.get("id")
        print("combined:", json.dumps(log["combine"])[:200], "doc", d)

        # 2 Author the press-release page in front (A4 landscape like the guidelines)
        call("page_insert_blank", {"doc": d, "at": 1, "width": 842, "height": 595})
        t = lambda **kw: call("page_add_text", dict(doc=d, page=1, **kw))
        t(text="PRESS RELEASE", at=[48, 44], font="Helvetica", size=8.5, bold=True, color=EMBER)
        t(text="FOR IMMEDIATE RELEASE", at=[150, 44], font="Helvetica", size=8.5, color=CLAY)
        t(text="Lumen launches Ember Ridge, a washed single origin from Guji, Ethiopia", rect=[48, 66, 470, 140],
          font="Helvetica", size=22, bold=True, color=ROAST)
        t(text=RELEASE, rect=[48, 150, 470, 545], font="Times", size=9.5, color=ROAST)
        call("page_add_image", {"doc": d, "page": 1, "path": HERO, "rect": [500, 48, 794, 244]})
        call("page_add_image", {"doc": d, "page": 1, "path": LABEL, "rect": [500, 256, 642, 434]})
        t(text="Ember Ridge, Lot 07\nWashed \u00b7 2,100 m\n340 g whole bean\nRoasted to order", rect=[652, 256, 794, 330],
          font="Helvetica", size=8.5, color=ROAST)
        t(text="https://lumen-coffee.example", at=[500, 452], font="Helvetica", size=9, bold=True, color=CLAY)
        t(text="Lumen Coffee Roasters  \u00b7  Press kit  \u00b7  October 2026", at=[48, 562], font="Helvetica", size=7, color=CLAY)

        # 3 Navigation: bookmarks and page labels
        log["bookmark"] = call("bookmark_add", {"doc": d, "page": 1, "title": "Press release: Ember Ridge", "position": 1})
        call("bookmark_rename", {"doc": d, "path": [2], "title": "Brand guidelines v1.0"})
        call("bookmark_rename", {"doc": d, "path": [3], "title": "Logo artwork (vector, from the identity master)"})
        for title, page in (("Contents", 3), ("01 Who we are", 4), ("02 Logo", 5), ("03 Colour", 8), ("04 Typography", 9),
                            ("05 Photography", 10), ("06 Packaging", 11), ("07 Motion and social", 12)):
            call("bookmark_add", {"doc": d, "page": page, "title": title, "parent": [2]})
        n_pages = len(call("doc_info", {"doc": d})["pages"])
        print("pages:", n_pages)
        call("page_number", {"doc": d, "from": 1, "to": 1, "prefix": "PR", "style": "none"})
        call("page_number", {"doc": d, "from": 2, "to": 13, "start": 1})
        call("page_number", {"doc": d, "from": 14, "to": n_pages, "prefix": "A-", "start": 1})
        call("doc_header_footer", {"doc": d, "pages": list(range(14, n_pages + 1)), "font_size": 7, "color": CLAY,
                                   "footer_left": "Lumen Coffee Roasters \u00b7 Press kit \u00b7 Logo artwork",
                                   "footer_right": "Use the supplied files only. Do not redraw.", "margins": [24, 24, 36, 36]})
        log["links"] = call("links_from_urls", {"doc": d})

        # 4 Metadata and accessibility
        for k, v in (("Title", "Lumen Coffee Roasters \u2014 Ember Ridge press kit"), ("Author", "Lumen in-house studio"),
                     ("Subject", "Launch of Ember Ridge single origin; brand guidelines v1.0; logo artwork"),
                     ("Keywords", "Lumen, Ember Ridge, coffee, press kit, brand guidelines")):
            call("doc_set_info", {"doc": d, "key": k, "value": v})
        log["a11y_before"] = call("accessibility_check", {"doc": d})
        for rule, value in (("title", None), ("primary-language", "en-US")):
            try:
                p = {"doc": d, "rule": rule}
                if value:
                    p["value"] = value
                log["fix:" + rule] = call("accessibility_fix", p)
            except RuntimeError as e:
                log["fix:" + rule] = str(e)[-200:]
        log["a11y_after"] = call("accessibility_check", {"doc": d})

        # 5 Save the kit, then derivatives
        log["save"] = call("doc_save", {"doc": d, "path": KIT, "full": True})
        log["bookmarks"] = call("bookmark_list", {"doc": d})
        log["product_sheet"] = call("page_extract", {"doc": d, "pages": [1, 11], "out": os.path.join(OUT, "ember-ridge-product-sheet.pdf")})
        log["split"] = call("doc_split", {"doc": d, "bookmarks": True, "out_dir": os.path.join(OUT, "sections")})
        # distribution copy: anyone can open and print; editing and copying need the permissions password (env LUMEN_PDF_OWNER_PW)
        call("doc_protect", {"doc": d, "permissions_password": os.environ["LUMEN_PDF_OWNER_PW"], "printing": "high", "changes": "none",
                             "copy": False, "accessibility": True})
        log["save_protected"] = call("doc_save", {"doc": d, "path": os.path.join(OUT, "lumen-press-kit-2026-10_distribution.pdf"), "full": True})
    os.remove(os.path.join(OUT, "_combined.pdf"))
    json.dump(log, open(os.path.join(OUT, "build-log.json"), "w"), indent=1, default=str)
    for k in ("save", "product_sheet", "split", "save_protected", "fix:title", "fix:primary-language"):
        print(k, json.dumps(log.get(k))[:260])
    s = lambda r: {k: r.get(k) for k in ("passed", "failed", "manual", "summary")} if isinstance(r, dict) else str(r)[:200]
    print("a11y before:", s(log["a11y_before"]), "\na11y after:", s(log["a11y_after"]))


if __name__ == "__main__":
    main(sys.argv[1])
