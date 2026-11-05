# Maaşım kaç ekmek?

**Site:** https://birtohum.github.io/maasim-kac-ekmek/

Maaşını ve fırınındaki ekmek fiyatını yaz: kaç ekmek ettiğini, asgari ücretin son zamdan bu yana ne kadar eridiğini, on yıllık seriyi bugünün parasıyla ve aynı maaşın market rafındaki karşılığını gösterir.

## Veri

- **Net asgari ücret** (bekâr işçi, aylık), 2016–2026: Çalışma ve Sosyal Güvenlik Bakanlığı tabloları ([Vikipedi'deki kaynaklı derlemesi](https://tr.wikipedia.org/wiki/T%C3%BCrkiye%27de_asgari_%C3%BCcret)). 2016–2021 değerleri asgari geçim indirimi dahil; 2022'den beri asgari ücret gelir ve damga vergisinden muaf, net = brüt × 0,85. 2016 öncesi tablolar AGİ'yi farklı gösterdiği için seri 2016'da başlıyor.
- **Aylık TÜFE değişimi:** TÜİK, [TCMB'nin tablosundan](https://www.tcmb.gov.tr/wps/wcm/connect/TR/TCMB+TR/Main+Menu/Istatistikler/Enflasyon+Verileri/Tuketici+Fiyatlari). Aylık değişimler zincirlenip her ayın ücreti son açıklanan ayın fiyatlarına taşınıyor. GitHub Actions her ay TÜFE açıklanınca seriyi yeniden hesaplıyor.
- **Market fiyatları:** [Sepet Enflasyonu](https://birtohum.github.io/sepet-enflasyonu/) sitesinin her gün ŞOK Market'ten okuduğu raf fiyatları, tarayıcıda canlı okunuyor.
- **Ekmek fiyatı** kullanıcıdan alınıyor. Türkiye'de ekmek fiyatı il ve fırına göre değişiyor; geçmiş yıllar için tutarlı ve kaynaklı tek bir seri bulamadığım için uydurmadım.

## Sınırlar

TÜFE ortalama bir sepetin fiyatı; ekmek ya da kira bir yerde daha hızlı artmış olabilir. Grafiğin “ekmek” birimi bugünkü ekmek fiyatını sabit alır, geçmişteki gerçek ekmek fiyatı değildir.

## Çalıştırma

```bash
python araclar/uret.py                 # site/veri/asgari.json
python -m unittest discover -s testler
cd site && python -m http.server
```

Lisans: MIT.
