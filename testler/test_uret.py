import sys, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "araclar"))
import uret


class Test(unittest.TestCase):
    def test_sabit_fiyatta_deger_degismez(self):
        aylar = [(f"{y}-{m:02d}", 0.0) for y in range(2016, 2018) for m in range(1, 13)]
        v = uret.hesapla(aylar)
        for x in v["seri"]:
            self.assertAlmostEqual(x["bugun"], x["net"], places=2)

    def test_enflasyon_gecmisi_bugune_tasir(self):
        aylar = [("2016-01", 0.0), ("2016-02", 10.0)]
        v = uret.hesapla(aylar)
        self.assertAlmostEqual(v["seri"][0]["bugun"], 1300.99 * 1.10, places=2)
        self.assertEqual(v["seri"][-1]["bugun"], v["seri"][-1]["net"])

    def test_2022_sonrasi_net_bruttun_yuzde_85i(self):
        for bas, brut, net in uret.ASGARI:
            if bas >= "2022":
                self.assertAlmostEqual(net, brut * 0.85, delta=0.01, msg=bas)


if __name__ == "__main__":
    unittest.main()
