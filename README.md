# Botswana (BW) — legislation as Markdown

Part of [LawCodex](https://github.com/LawCodex): the legislation of every country as plain Markdown in git.

**Partial corpus.** Legislation of the Republic of Botswana, in **English**: the **Constitution** (from the
Parliament of Botswana) and **125 chapters of the Laws of Botswana** (principal Acts in their revised-edition
form), recovered from Internet Archive captures of official government websites, because the official legislation
portal of the Attorney General's Chambers (Botswana e-Laws, www.elaws.gov.bw) and its predecessor (www.laws.gov.bw)
were unreachable when this corpus was built. Retrieved 2026-10-13.

| Category | Files | Source |
|---|---|---|
| Constitution | 1 | Parliament of Botswana (live) |
| Laws of Botswana chapters — AGC "Laws of Botswana" site (captures of 2007–2010) | 79 | www.laws.gov.bw (Internet Archive) |
| Laws of Botswana chapters — Environment Information System (environment-related Acts) | 27 | www1.eis.gov.bw (Internet Archive) |
| Laws of Botswana chapters / Acts — Ministry of Finance "Laws & Regulations" | 19 | www.finance.gov.bw (Internet Archive) |
| **Total** | **126** | |

## Structure

```
constitution/constitution-of-botswana.md      Constitution of Botswana (as published by Parliament)
chapters/cap-<nn>-<nn>-<slug>.md              Laws of Botswana, Chapter nn:nn (e.g. cap-38-04-fish-protection.md)
acts/<slug>.md                                Acts without a chapter number in the source (Financial Intelligence Act 2009)
```

Front matter: `identifier` (`Cap. 38:04`), `status: unknown`, `source` (original URL), `archived_source`
(Wayback Machine capture), `note` (which site and capture date). When the same chapter was available from several
sites, the most recent capture was kept. **The texts are those of the capture date** (many date from 2007) and do
not reflect later amendments. Text extracted with poppler `pdftotext`; CHAPTER/PART become headings and sections
`Section N — <title>`.

## Not covered / known gaps

* Most of the ~450 chapters of the Laws of Botswana, all recent Acts, and subsidiary legislation. The Internet
  Archive holds only scattered captures of www.elaws.gov.bw, mostly one-part fragments of chapters (not used).
* The Parliament website (parliament.gov.bw) publishes Bills, not enacted Acts.
* Skipped: Bills found on the Finance Ministry site (Income Tax Bill, Tax Administration Bill), indexes, and the
  Public Procurement Act PDF (no text layer).

## Sources and licence

| Source | URL |
|---|---|
| Parliament of Botswana — Constitution | https://www.parliament.gov.bw/images/constitution.pdf |
| Laws of Botswana (AGC), via Internet Archive | http://www.laws.gov.bw/Docs/Principal/... (see `archived_source` of each file) |
| Environment Information System, via Internet Archive | http://www1.eis.gov.bw/EIS/Policies/Environmental%20Policies/CAP%20... |
| Ministry of Finance — Laws & Regulations, via Internet Archive | https://www.finance.gov.bw/images/LawRegulations/... |

Official texts of the Government of Botswana. The e-Laws disclaimer describes the electronic versions as provided
"for information purposes only" and not the authorised version; it does not forbid copying. The archived files were
fetched one at a time (one request every 4 s) with an identifying User-Agent.

## Regenerate

```
pip install -r scripts/requirements.txt     # plus poppler (pdftotext, pdfinfo)
python scripts/bw_fetch.py                  # downloads into ../_raw/bw/
python scripts/bw_convert.py .
```
