# Bilgi Tabanı (knowledge/) — Okuma Sırası

DKAB soru üretim ajanları bu dosyaları kaynak alır. **Okuma önceliği yukarıdan aşağıya**; çelişkide üstteki geçerlidir.

| # | Dosya | İçerik | Kim okur |
|---|---|---|---|
| 0 | **00_KARAR_KAYDI.md** | **BAĞLAYICI KANON** — 12 çelişki çözümü, 16 boşluk politikası, veri sözleşmesi, puanlama. Her ajan ÖNCE bunu okur. | Hepsi |
| 1 | kriterler_D1-D9.md | Yapısal madde-yazım rubriği (D1–D9), makine-denetlenebilir, örnekli. | çapraz-okuma, düzeltici, seçenekler |
| 2 | osym_stil_tyt.md | ÖSYM TYT DKAB stil DNA'sı (metin türü, kök kalıbı, şık tekniği frekanslarla). | soru-metni, seçenekler, test-kurgu |
| 3 | osym_stil_ayt.md | ÖSYM AYT DKAB stil DNA'sı (daha analitik/çıkarımsal). | soru-metni, seçenekler, test-kurgu |
| 4 | soru_kalip_havuzu.md | Metin türü + kök kalıbı havuzu, yönlendirme ifadeleri, anti-tekdüzelik. | test-kurgu, soru-metni |
| 5 | kelime_bandi_ve_zorluk.md | Kelime bandı dağılımı, zorluk, kök polaritesi, blueprint formatı. | test-kurgu |
| 6 | dini_dil_kurallari.md | Dinî dil/terminoloji kuralları + kazanım kod yapısı (11. sınıf). | Hepsi |
| 7 | dab_becerileri_bloom.md | DAB alan becerileri + Bloom düzeyleri + beceri→kalıp eşlemesi. | test-kurgu, soru-metni |
| — | tr_stopwords.txt | D1/D6 deterministik ön-eleme için Türkçe durak-kelime listesi. | çapraz-okuma |

Şemalar: `../schemas/{blueprint,soru,rapor}.schema.json` — ajanlar arası bağlayıcı veri sözleşmesi.

## Bilinen eksikler (üretimden önce kapatılacak)
- **9/10. sınıf kazanım kodları**: `dini_dil_kurallari.md` yalnız 11. sınıfı içeriyor. 9/10 üretiminden önce ilgili `tymm/` dosyasından çıkarılıp `kazanim_kodlari.md`'ye yazılmalı (KARAR_KAYDI G6). 11. sınıf pilotu için gerekli değil.
- **Ayet/meal referans DB'si**: D11 şimdilik LLM-hakem makullük denetimi + şüpheli künye işaretleme ile çalışıyor; kesin doğrulama için ileride bir meal DB'si eklenebilir.
