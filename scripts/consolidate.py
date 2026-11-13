"""Build an unofficial consolidated text of UU 11/2008 (UU ITE) from its two amending laws.

How it works (plain language):
1. Read the base law (sources/uu-11-2008.txt) into a list of Pasal, each with its BAB.
2. Read each amending law's Pasal I. It is split into numbered change points ("Angka 1", "Angka 2", ...).
   Every change point that touches the body of the law restates the whole new Pasal
   ("... sehingga Pasal X berbunyi sebagai berikut"), so we never edit inside a sentence:
   we only replace a whole Pasal, or insert a new one after an existing one.
3. changes.csv is the ledger: one row per Pasal touched by each change point, written by hand
   from reading the amending laws. The script checks the ledger against the source text
   before applying anything, so a missing or extra row stops the build.
4. status.csv holds what happened later without rewriting the text: provisions that expired,
   were revoked by the new KUHP, open questions, and Constitutional Court (MK) rulings.
   These become notes under each Pasal. The text itself is not changed by them.
5. Write data/consolidation/uu-ite/uu-ite-konsolidasi.md.

Run from the repo root:  python3 scripts/consolidate.py
"""

import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FOLDER = ROOT / "data" / "consolidation" / "uu-ite"
BASE = FOLDER / "sources" / "uu-11-2008.txt"
AMENDMENTS = {"UU 19/2016": FOLDER / "sources" / "uu-19-2016.txt",  # applied in this order
              "UU 1/2024": FOLDER / "sources" / "uu-1-2024.txt"}
OUTPUT = FOLDER / "uu-ite-konsolidasi.md"
AS_OF = "14 November 2026"

PASAL_HEADER = re.compile(r"^Pasal (\d+[A-Z]?)$")


def body_lines(path):
    """The file's lines without the # source notes at the top."""
    return [line for line in path.read_text(encoding="utf-8").splitlines() if not line.startswith("#")]


def read_base():
    """Return the Pasal in order as dicts: number, bab (e.g. 'BAB VII — PERBUATAN YANG DILARANG'), text."""
    pasals, bab, lines = [], None, body_lines(BASE)
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("BAB "):
            bab, i = f"{line} — {lines[i + 1].strip()}", i + 2
            continue
        m = PASAL_HEADER.match(line)
        if m:
            pasals.append({"number": m.group(1), "bab": bab, "text": [], "history": [], "status": []})
        elif line:
            pasals[-1]["text"].append(line)
        i += 1
    return pasals


def read_amendment(path):
    """Return {angka: {"instruction": text, "pasal": {number: [lines]}}} from Pasal I of an amending law."""
    lines = body_lines(path)
    start, end = lines.index("Pasal I"), lines.index("Pasal II")
    points, current, pasal = {}, None, None
    for line in lines[start + 1:end]:
        line = line.strip()
        if not line:
            continue
        if re.fullmatch(r"Angka \d+", line):
            current, pasal = int(line.split()[1]), None
            points[current] = {"instruction": "", "pasal": {}}
        elif current is None:
            continue  # the opening sentence "Beberapa ketentuan ... diubah sebagai berikut:"
        elif PASAL_HEADER.match(line):
            pasal = PASAL_HEADER.match(line).group(1)
            points[current]["pasal"][pasal] = []
        elif pasal is None:
            points[current]["instruction"] += line
        else:
            points[current]["pasal"][pasal].append(line)
    return points


def read_ledger():
    with open(FOLDER / "changes.csv", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def check_ledger(ledger, amendments):
    """Every restated Pasal in the sources has exactly one ledger row, and every ledger row points at one."""
    for law, points in amendments.items():
        rows = [r for r in ledger if r["law"] == law]
        assert {int(r["angka"]) for r in rows} == set(points), f"{law}: ledger angka differ from source angka"
        in_source = {(n, p) for n, pt in points.items() for p in pt["pasal"]}
        in_ledger = {(int(r["angka"]), r["target"]) for r in rows if r["action"] != "penjelasan"}
        assert in_source == in_ledger, f"{law}: source {sorted(in_source - in_ledger)} vs ledger {sorted(in_ledger - in_source)}"
        for r in rows:
            if r["action"] == "penjelasan":
                assert not points[int(r["angka"])]["pasal"], f"{law} angka {r['angka']} restates a Pasal but is marked penjelasan"


def apply(pasals, ledger, amendments):
    for law, points in amendments.items():
        for r in (r for r in ledger if r["law"] == law):
            where = f"{law} Pasal I angka {r['angka']}"
            numbers = [p["number"] for p in pasals]
            if r["action"] == "penjelasan":
                pasals[numbers.index(r["target"])]["history"].append(f"Penjelasan diubah oleh {where}; batang tubuh tetap.")
                continue
            new_text = points[int(r["angka"])]["pasal"][r["target"]]
            if r["action"] == "replace":
                assert r["target"] in numbers, f"{where}: replaces Pasal {r['target']}, which does not exist yet"
                p = pasals[numbers.index(r["target"])]
                p["text"], verb = new_text, "Diubah"
            elif r["action"] == "insert":
                assert r["target"] not in numbers, f"{where}: inserts Pasal {r['target']}, which already exists"
                anchor = pasals[numbers.index(r["anchor"])]
                p = {"number": r["target"], "bab": anchor["bab"], "text": new_text, "history": [], "status": []}
                pasals.insert(numbers.index(r["anchor"]) + 1, p)
                verb = "Disisipkan"
            else:
                raise SystemExit(f"Unknown action {r['action']!r} in changes.csv")
            p["history"].append(f"{verb} oleh {where}.")
    return pasals


def attach_status(pasals):
    by_number = {p["number"]: p for p in pasals}
    with open(FOLDER / "status.csv", newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            p = by_number[r["pasal"]]  # a typo in status.csv stops the build here
            if r["ayat"]:
                assert any(line.startswith(f"({r['ayat']})") for line in p["text"]), f"Pasal {r['pasal']} has no ayat ({r['ayat']})"
            label = r["kind"][0].upper() + r["kind"][1:]  # keeps "MK" in capitals
            where = f" (ayat ({r['ayat']}))" if r["ayat"] else ""
            p["status"].append(f"**{label}**{where}: {r['note']} _Sumber: {r['source']}._")


def render(pasals):
    out = [f"# UU 11/2008 tentang Informasi dan Transaksi Elektronik — naskah konsolidasi tidak resmi",
           "",
           f"Keadaan per {AS_OF}. Disusun dari UU 11/2008, UU 19/2016, dan UU 1/2024 (batang tubuh saja; Penjelasan tidak dikonsolidasi).",
           "Status setelah 2 Januari 2026 (KUHP baru dan UU 1/2026) dan putusan MK dicatat sebagai catatan di bawah tiap pasal, tanpa mengubah teks.",
           "",
           "> **Catatan Bab XI (Ketentuan Pidana).** Sejak 2 Januari 2026, UU 1/2026 tentang Penyesuaian Pidana Pasal I–III berlaku untuk ketentuan pidana di luar KUHP:",
           "> ancaman pidana minimum khusus dihapus, ancaman penjara dan denda kumulatif menjadi kumulatif-alternatif, dan besaran denda diganti kategori denda",
           "> menurut lama ancaman penjara (Lampiran I UU 1/2026). Angka rupiah di Bab XI di bawah adalah teks asli; kategori per pasal belum dicek ke Lampiran I.",
           "",
           "Riset pribadi, bukan nasihat hukum dan bukan naskah resmi. Independent personal research. Not affiliated with or endorsed by any employer.",
           ""]
    bab = None
    for p in pasals:
        if p["bab"] != bab:
            bab = p["bab"]
            out += [f"## {bab}", ""]
        out += [f"### Pasal {p['number']}", ""] + [line + "  " for line in p["text"]] + [""]
        for note in p["history"]:
            out.append(f"> _Riwayat:_ {note}  ")
        for note in p["status"]:
            out.append(f"> {note}  ")
        if p["history"] or p["status"]:
            out.append("")
    return "\n".join(out) + "\n"


def build():
    pasals = read_base()
    amendments = {law: read_amendment(path) for law, path in AMENDMENTS.items()}
    ledger = read_ledger()
    check_ledger(ledger, amendments)
    pasals = apply(pasals, ledger, amendments)
    attach_status(pasals)
    OUTPUT.write_text(render(pasals), encoding="utf-8")
    return pasals, amendments


if __name__ == "__main__":
    pasals, amendments = build()
    numbers = [p["number"] for p in pasals]
    # Self-check: nothing lost, new Pasal in the right place, last amendment wins.
    assert len(read_base()) == 54 and len(pasals) == 54 + 2 + 7, len(pasals)  # +45A,45B (2016); +13A,16A,16B,18A,27A,27B,40A (2024)
    assert numbers.index("13A") == numbers.index("13") + 1 and numbers.index("45B") == numbers.index("45A") + 1
    final45 = next(p for p in pasals if p["number"] == "45")["text"]
    assert final45 == amendments["UU 1/2024"][16]["pasal"]["45"], "Pasal 45 should be the UU 1/2024 version"
    assert next(p for p in pasals if p["number"] == "12")["history"] == [], "Pasal 12 was never amended"
    print(f"Consolidated {len(pasals)} Pasal ({sum(1 for p in pasals if p['history'])} with history) -> {OUTPUT.relative_to(ROOT)}")
