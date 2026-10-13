"""Botswana: the official "Laws of Botswana" sites of the Attorney General's Chambers (www.elaws.gov.bw, and the
older www.laws.gov.bw) were unreachable when this corpus was built. Sources used:

  * Parliament of Botswana (live): the Constitution PDF, https://www.parliament.gov.bw/images/constitution.pdf
  * Internet Archive captures of www.laws.gov.bw "Principal legislation" chapter PDFs (Laws of Botswana, revised
    edition, captured 2007-2010);
  * Internet Archive captures of Acts published by government ministries/agencies:
      - Environment Information System, www1.eis.gov.bw/EIS/Policies/Environmental Policies/CAP xx-yy <Act>.pdf
      - Ministry of Finance, www.finance.gov.bw/images/LawRegulations/<Act>.pdf
The archived URL is recorded for every file. Cache: _raw/bw/. Usage: python bw_fetch.py
"""
import json
import os
import re
import sys
from urllib.parse import unquote

import requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bw_text import fetch, UA  # noqa: E402

RAW = os.environ.get("BW_RAW", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "_raw", "bw"))
CDX = ("https://web.archive.org/cdx/search/cdx?url=%s&matchType=prefix&output=json&fl=original,timestamp"
       "&filter=mimetype:application/pdf&filter=statuscode:200&limit=20000")
PREFIXES = [("laws.gov.bw/Docs/Principal", "laws.gov.bw"),
            ("www1.eis.gov.bw/EIS/Policies/Environmental%20Policies/CAP", "eis.gov.bw"),
            ("www.finance.gov.bw/images/LawRegulations/", "finance.gov.bw")]


def cdx(prefix):
    for i in range(4):
        try:
            return requests.get(CDX % prefix, headers={"User-Agent": UA}, timeout=600).json()[1:]
        except Exception as e:  # noqa
            print("cdx retry", prefix, e)
    return []


def main():
    items = []
    f = fetch("https://www.parliament.gov.bw/images/constitution.pdf", os.path.join(RAW, "pdf", "constitution.pdf"),
              delay=3, check_pdf=True, timeout=300)
    items.append({"origin": "parliament.gov.bw", "url": "https://www.parliament.gov.bw/images/constitution.pdf", "file": f})
    for prefix, origin in PREFIXES:
        best = {}
        for orig, ts in cdx(prefix):
            key = re.sub(r"^https?://(www\.)?", "", orig).replace(":80/", "/").lower()
            if not key.endswith(".pdf"):
                continue
            if key not in best or ts > best[key][1]:
                best[key] = (orig, ts)
        for key, (orig, ts) in sorted(best.items()):
            name = re.sub(r"[^A-Za-z0-9]+", "_", unquote(key.rsplit("/", 1)[1]))[:110]
            arch = "https://web.archive.org/web/%sid_/%s" % (ts, orig)
            f = fetch(arch, os.path.join(RAW, "pdf", origin.split(".")[0] + "-" + name + ".pdf"), delay=4,
                      check_pdf=True, timeout=300)
            items.append({"origin": origin, "url": orig.replace(":80/", "/"),
                          "archived": "https://web.archive.org/web/%s/%s" % (ts, orig), "file": f})
            print("ok " if f else "FAIL", orig)
    json.dump(items, open(os.path.join(RAW, "index.json"), "w"), indent=1)


if __name__ == "__main__":
    os.makedirs(RAW, exist_ok=True)
    main()
