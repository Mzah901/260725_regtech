"""Compare two texts word by word, ignoring numbering labels, page furniture and hyphenation.

Usage: python3 scripts/compare_words.py <ours.txt> <official.txt> [--show N]
(official.txt = text extracted from the official PDF; the lab used macOS PDFKit for this.)
Prints the number of matching words and every difference with a little context.
A difference where the two words look alike (OCR-style, e.g. "(21" vs "(2)") is marked "~"; others "!".
"""
import difflib
import re
import sys

LABEL = re.compile(r"^(\(\d+[a-z]?[\)1l]?|\d+[a-z]?\.|[a-z]\.|Angka|Pasal|BAB|[IVXL]+|\d+[A-Z]?|-|–)$")


def words(path):
    t = open(path, encoding="utf-8").read()
    t = "\n".join(l for l in t.splitlines() if not l.startswith("#"))
    t = re.sub(r"(\w)-\s*\n\s*(\w)", r"\1\2", t)            # rejoin words hyphenated across lines
    t = re.sub(r"/\s+", "/", t)                              # "dan/ atau" -> "dan/atau"
    t = re.sub(r"\s+", " ", t)
    return [w for w in t.split(" ") if w and not LABEL.match(w)]


if len(sys.argv) < 3:  # self-check: labels and line-break hyphens are ignored, real words are kept
    import tempfile, os
    a, b = (tempfile.NamedTemporaryFile("w", delete=False, suffix=".txt") for _ in range(2))
    a.write("Pasal 5\n(1) Setiap Orang dan/atau badan."); b.write("(1) Setiap Or-\nang dan/ atau badan."); a.close(); b.close()
    assert words(a.name) == words(b.name) == ["Setiap", "Orang", "dan/atau", "badan."], (words(a.name), words(b.name))
    os.unlink(a.name); os.unlink(b.name)
    sys.exit("compare_words self-check passed. Usage: python3 scripts/compare_words.py <ours.txt> <official.txt>")

ours, official = words(sys.argv[1]), words(sys.argv[2])
show = int(sys.argv[sys.argv.index("--show") + 1]) if "--show" in sys.argv else 10**9
sm = difflib.SequenceMatcher(a=ours, b=official, autojunk=False)
same = sum(b.size for b in sm.get_matching_blocks())
print(f"ours {len(ours)} words, official {len(official)} words, matching {same}")
n = 0
for op, a1, a2, b1, b2 in sm.get_opcodes():
    if op == "equal":
        continue
    a, b = " ".join(ours[a1:a2]), " ".join(official[b1:b2])
    mark = "~" if a and b and difflib.SequenceMatcher(a=a, b=b).ratio() >= 0.6 else "!"
    n += 1
    if n <= show:
        ctx = " ".join(ours[max(0, a1 - 5):a1])
        print(f"{mark} [{ctx}] ours: {a!r} | official: {b!r}")
print(f"{n} differences")
