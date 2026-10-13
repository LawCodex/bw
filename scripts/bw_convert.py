"""Botswana: convert the downloaded PDFs (Laws of Botswana chapters) to Markdown.
One file per chapter: when several sources hold the same chapter, the most recent capture is kept.
Bills, the alphabetical index and PDFs without a usable text layer are skipped. Usage: python bw_convert.py <repo_dir>"""
import datetime
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bw_text import pdf_text, clean_pages, structure, write_md, slug, text_quality  # noqa: E402

RAW = os.environ.get("BW_RAW", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "_raw", "bw"))
TODAY = datetime.date.today().isoformat()
SMALL = {"and", "of", "the", "for", "to", "in", "on", "or", "by", "at", "a", "an", "with", "from"}


def tcase(s):
    w = s.lower().split()
    return " ".join(x if (i and x in SMALL) else re.sub(r"^([(\"']*)(\w)", lambda m: m.group(1) + m.group(2).upper(), x)
                    for i, x in enumerate(w))


def main(repo):
    items = json.load(open(os.path.join(RAW, "index.json")))
    best = {}
    for it in items:
        f = it.get("file")
        if not f or re.search(r"(?i)bill|alphabetical_index|classified_table|vol1_constitution", f):
            continue
        pages, _ = pdf_text(f)
        full = "\n".join(pages)
        if len(re.sub(r"\s", "", full)) < 800 or text_quality(full) < 0.7:
            print("SKIP (no usable text layer):", os.path.basename(f))
            continue
        head = [x.strip() for x in "\n".join(pages[:2]).splitlines() if x.strip()][:12]
        cap = re.search(r"CHAPTER\s+(\d{1,2}:\d{2})", "\n".join(head))
        if "constitution" in os.path.basename(f) and it["origin"] == "parliament.gov.bw":
            key, title = "constitution", "Constitution of Botswana"
        elif cap:
            key = cap.group(1)
            k = next((i for i, x in enumerate(head) if cap.group(1) in x), 0)
            rest = re.sub(r".*CHAPTER\s+\d{1,2}:\d{2}\s*", "", head[k]).strip()
            if rest:  # title on the same line as the chapter number
                head = head[:k + 1] + [rest] + head[k + 1:]
            tl = []
            for x in head[k + 1:k + 4]:
                if re.match(r"(?i)^(ARRANGEMENT|SECTION|PART)\b|^\d", x):
                    break
                tl.append(x)
                if x.count("(") <= " ".join(tl).count(")") and not x.endswith(("AND", "OF", "-", ",")):
                    break
            title = " ".join(tl) or key
            title = tcase(title) if title.isupper() else title
            if re.search(r"(?i)^index\b", title):
                continue
        else:
            key = os.path.basename(f)
            title = re.sub(r"(?i)^(laws|eis|finance)-|_pdf\.pdf$|\.pdf$", "", key).replace("_", " ")
            title = tcase(re.sub(r"(?i)^(cap \d+ \d+ |pr vol \w+ chp \d+ \d+ |principal vol\d+ chpt\d+ \d+ |chpt\d+ \d+ )", "", title))
        ts = (re.search(r"/web/(\d+)/", it.get("archived", "")) or re.search(r"(\d)", "9" * 14)).group(1)
        if it["origin"] == "parliament.gov.bw":
            ts = "99999999999999"
        if key not in best or ts > best[key][0]:
            best[key] = (ts, it, pages, title)
    n = 0
    for key, (ts, it, pages, title) in sorted(best.items()):
        if key == "constitution":
            path = os.path.join(repo, "constitution", "constitution-of-botswana.md")
            ident, typ = "Cap. 00:00 (Constitution)", "constitution"
        elif re.match(r"\d+:\d+$", key):
            path = os.path.join(repo, "chapters", "cap-%s-%s.md" % (key.replace(":", "-"), slug(title)[:70]))
            ident, typ = "Cap. " + key, "act"
        else:
            path = os.path.join(repo, "acts", slug(title)[:80] + ".md")
            ident, typ = "", "act"
        acts = re.search(r"^(Act|Acts|Proclamation|Law)\s+\d+.*?\d{4}", "\n".join(pages[:2]), re.M)
        meta = {"title": title, "identifier": ident, "type": typ, "jurisdiction": "bw", "language": "en",
                "status": "unknown", "source": it["url"], "archived_source": it.get("archived"), "retrieved": TODAY,
                "note": "Laws of Botswana (revised edition) chapter as published by %s%s" % (
                    it["origin"], ", Internet Archive capture of %s-%s-%s" % (ts[:4], ts[4:6], ts[6:8]) if it.get("archived") else "")}
        write_md(path, meta, title, structure(clean_pages(pages), "en"))
        n += 1
    print("written", n)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
