"""Asgari ücretin bugünkü parayla değerini hesaplar: site/veri/asgari.json

Kaynaklar
- Net asgari ücret (bekâr işçi, aylık): Çalışma ve Sosyal Güvenlik Bakanlığı tabloları
  (Vikipedi "Türkiye'de asgari ücret" maddesinde kaynaklı olarak derlenmiş). 2016-2021 değerleri
  asgari geçim indirimi (AGİ) dahil; 2022'den itibaren asgari ücret vergiden muaf, net = brüt x 0,85.
  2016 öncesi tablolar AGİ'yi farklı biçimde gösterdiği için seri 2016'da başlar.
- Aylık TÜFE değişimi: TÜİK, TCMB'nin "Tüketici Fiyatları" tablosundan.
"""
from __future__ import annotations

import html
import json
import re
import sys
import urllib.request
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
HEDEF = KOK / "site" / "veri" / "asgari.json"
TCMB = ("https://www.tcmb.gov.tr/wps/wcm/connect/TR/TCMB+TR/Main+Menu/"
        "Istatistikler/Enflasyon+Verileri/Tuketici+Fiyatlari")

# (başlangıç ayı, brüt, net) - bekâr işçi
ASGARI = [
    ("2016-01", 1647.00, 1300.99), ("2017-01", 1777.50, 1404.06), ("2018-01", 2029.50, 1603.12),
    ("2019-01", 2558.40, 2020.90), ("2020-01", 2943.00, 2324.71), ("2021-01", 3577.50, 2825.90),
    ("2022-01", 5004.00, 4253.40), ("2022-07", 6471.00, 5500.35), ("2023-01", 10008.00, 8506.80),
    ("2023-07", 13414.50, 11402.32), ("2024-01", 20002.50, 17002.12), ("2025-01", 26005.50, 22104.67),
    ("2026-01", 33030.00, 28075.50),
]


def tufe_cek() -> list[tuple[str, float]]:
    istek = urllib.request.Request(TCMB, headers={"User-Agent": "maasim-kac-ekmek (github.com/birtohum)"})
    sayfa = urllib.request.urlopen(istek, timeout=60).read().decode("utf-8", "replace")
    aylar = {}
    for tr in re.findall(r"<tr[^>]*>(.*?)</tr>", sayfa, re.S):
        h = [html.unescape(re.sub(r"<[^>]+>", "", x)).strip() for x in re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", tr, re.S)]
        if len(h) >= 3 and re.fullmatch(r"\d{2}-\d{4}", h[0]):
            ay, yil = h[0].split("-")
            try:
                aylar[f"{yil}-{ay}"] = float(h[2].replace(",", "."))
            except ValueError:
                pass
    return sorted(aylar.items())


def hesapla(tufe: list[tuple[str, float]]) -> dict:
    # Endeks: 2015-12 = 1, aylık değişimler zincirlenir
    endeks, e = {}, 1.0
    for ay, yuzde in tufe:
        if ay < "2016-01":
            continue
        e *= 1 + yuzde / 100
        endeks[ay] = e
    aylar = sorted(endeks)
    son = aylar[-1]
    seri = []
    for ay in aylar:
        net = [n for b, _, n in ASGARI if b <= ay][-1]
        seri.append({"ay": ay, "net": net, "bugun": round(net * endeks[son] / endeks[ay], 2)})
    return {"son_tufe_ayi": son, "asgari": [{"bas": b, "brut": br, "net": n} for b, br, n in ASGARI],
            "seri": seri, "kaynak": {"asgari": "https://tr.wikipedia.org/wiki/T%C3%BCrkiye%27de_asgari_%C3%BCcret", "tufe": TCMB}}


def main() -> int:
    tufe = tufe_cek()
    if len(tufe) < 120:
        print("TÜFE tablosu okunamadı; dosya değiştirilmedi")
        return 1
    veri = hesapla(tufe)
    HEDEF.write_text(json.dumps(veri, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    s = veri["seri"]
    print("son TÜFE ayı", veri["son_tufe_ayi"], "| ilk", s[0], "| son", s[-1])
    return 0


if __name__ == "__main__":
    sys.exit(main())
