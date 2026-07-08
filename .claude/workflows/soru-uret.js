// DKAB Soru Üretim Orchestrator'ı
// Akış (pipeline/knowledge/00_KARAR_KAYDI.md §C):
//   test-kurgu -> blueprint + kaynak_baglami
//     -> pipeline(her sipariş): soru-metni -> seçenekler
//        -> çapraz-okuma (adversarial verify) -> düzeltici loop (≤3 tur, KANON G9)
//   -> return {blueprint, sorular, raporlar}  (montaj/docx main-loop'ta Python ile yapılır)
//
// args: { sinif, unite, sinav_turu, soru_sayisi, tymm_yolu, ders_kitabi_yolu, blueprint_ref }
// Çalıştırma: Workflow({ name: 'soru-uret', args: {...} })

export const meta = {
  name: 'soru-uret',
  description: 'DKAB testi üretir: blueprint -> soru metni+kök -> şıklar -> acımasız çapraz okuma -> düzeltici döngü',
  phases: [
    { title: 'Kurgu', detail: 'test-kurgu: kaynağı oku, blueprint + kazanım bağlamı' },
    { title: 'Yaz', detail: 'her sipariş: soru-metni -> seçenekler (pipeline)' },
    { title: 'Denetle', detail: 'çapraz-okuma: D1-D11 acımasız değerlendirme' },
    { title: 'Düzelt', detail: 'düzeltici: açık D-kodlarını gerçekten kapat (≤3 tur)' },
  ],
}

// --- ortak şema parçaları (StructuredOutput'u yönlendiren pratik alt küme;
//     kanonik tam şema pipeline/schemas/*.json'da, subagent'ler onu okur) ---
const VURGU = { type: ['object', 'null'], properties: { sozcuk: { type: 'string' }, bicim: { type: 'string', enum: ['alti_cizili'] } } }
const KAZANIM = { type: 'object', properties: { kod: { type: 'string' }, baslik: { type: 'string' }, serbest_konu: { type: 'string' } }, required: ['kod', 'serbest_konu'] }
const SECENEKLER = { type: 'object', properties: { A: { type: 'string' }, B: { type: 'string' }, C: { type: 'string' }, D: { type: 'string' }, E: { type: 'string' } }, required: ['A', 'B', 'C', 'D', 'E'] }

const SORU_METNI_OUT = {
  type: 'object', additionalProperties: true,
  required: ['sinif', 'sinav_turu', 'unite', 'kazanim', 'bloom', 'zorluk', 'metin', 'metin_turu', 'kelime_sayisi', 'band', 'kok', 'kok_tipi', 'kalip'],
  properties: {
    sinif: { type: 'integer' }, sinav_turu: { type: 'string' }, unite: { type: 'integer' },
    kazanim: KAZANIM, dab_kodu: { type: 'string' }, bloom: { type: 'string' }, zorluk: { type: 'string' },
    metin: { type: 'string' }, metin_turu: { type: 'string' }, gorsel: { type: ['object', 'null'] },
    kelime_sayisi: { type: 'integer' }, band: { type: 'string' }, hedef_kelime: { type: 'integer' },
    kok: { type: 'string' }, kok_tipi: { type: 'string' }, kalip: { type: 'string' }, vurgu: VURGU,
  },
}

const SORU_TAM = {
  type: 'object', additionalProperties: true,
  required: ['metin', 'kok', 'kok_tipi', 'secenekler', 'dogru', 'cozum', 'kelime_sayisi', 'band'],
  properties: {
    ...SORU_METNI_OUT.properties,
    secenekler: SECENEKLER,
    dogru: { type: 'string', enum: ['A', 'B', 'C', 'D', 'E'] },
    cozum: { type: 'string' },
    revizyon_gecmisi: { type: 'array', items: { type: 'object', additionalProperties: true } },
  },
}

const KONTROL = { type: 'object', properties: { gecti: { type: 'boolean' }, kanit: { type: 'string' }, oneri: { type: 'string' } }, required: ['gecti', 'kanit', 'oneri'] }
const RAPOR_OUT = {
  type: 'object', additionalProperties: true,
  required: ['kontroller', 'madde_puani', 'etiket', 'en_kritik_sorunlar'],
  properties: {
    soru_id: { type: 'string' },
    kontroller: {
      type: 'object', additionalProperties: true,
      required: ['D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10_olgusal', 'D11_dini_kunye'],
      properties: {
        D1: KONTROL, D2: KONTROL, D3: KONTROL, D4: KONTROL, D5: KONTROL, D6: KONTROL,
        D7: KONTROL, D8: KONTROL, D9: KONTROL, D10_olgusal: KONTROL, D11_dini_kunye: KONTROL,
      },
    },
    band_uyum: { type: 'boolean' }, zorluk_uyum: { type: 'boolean' }, bloom_uyum: { type: 'boolean' },
    madde_puani: { type: 'integer' }, etiket: { type: 'string' },
    en_kritik_sorunlar: { type: 'array', items: { type: 'string' } },
  },
}

// F4 — çok-mercekli doğrulama paneli: uzman merceklerin çıktı şeması
const LENS_OUT = {
  type: 'object', additionalProperties: true,
  required: ['gecti', 'sorunlar'],
  properties: {
    gecti: { type: 'boolean' },
    sorunlar: { type: 'array', items: { type: 'string' } },
    oneriler: { type: 'array', items: { type: 'string' } },
  },
}
const LENS_TEKDOGRU = `MERCEK — TEK-DOĞRU AVUKATI. Görevin: doğru dışındaki HER şıkkı sırayla savunmaya çalışmak. Metnin HERHANGİ bir cümlesince doğrulanabilen ya da "ikinci doğru" sayılabilecek bir çeldirici bulursan gecti=false yap ve hangi şık / neden olduğunu 'sorunlar'a yaz. ÖZELLİKLE "vurgu/ana fikir/asıl anlatılan" köklerinde: metinde geçen ama "asıl vurgu değil" diye elenen çeldirici = FAIL (F2). Şüphede kal.
SORU: `
const LENS_DERINLIK = `MERCEK — BİLİŞSEL-DERİNLİK HAKEMİ. Görevin: madde paragraf-eşleştirme / eş-anlamlı-bulma ile çözülebiliyor mu diye sınamak. Etiket Analiz/Değerlendirme ise gerçekten iki+ öğe sentezi / geçersiz-çıkarım-eleme / karşılaştırmadan sonuç / ilke-uygulama gerekiyor mu? Salt "bul" ise (özellikle Analiz etiketli) gecti=false ve nedenini yaz (F1/V9/V9b). Olumsuz "yerini bul" kökü Analiz etiketliyse FAIL.
SORU: `
const LENS_EDITOR = `MERCEK — EDİTÖR. Görevin: (a) gövdede işlevsiz dolgu/süs cümle, (b) gövdedeki bir cümlenin birebir/yakın parafrazı olan şık (doğru dahil), (c) "Doğru cevap X:" biçim ihlali ya da çözümde harf tutarsızlığı, (d) şık paralelliği/terminoloji/ayet künyesi kusuru, (e) testte aynı kaynaktan (aynı sure/ayet grubu) tekrar. Kusur varsa gecti=false ve 'sorunlar'a somut yaz (F3).
SORU: `

const KURGU_OUT = {
  type: 'object', additionalProperties: true,
  required: ['blueprint', 'kaynak_baglami'],
  properties: {
    blueprint: {
      type: 'object', additionalProperties: true,
      required: ['blueprint_ref', 'sinif', 'unite', 'sinav_turu', 'soru_sayisi', 'siparisler', 'dagilim_ozeti'],
      properties: {
        blueprint_ref: { type: 'string' }, sinif: { type: 'integer' }, unite: { type: 'integer' },
        sinav_turu: { type: 'string' }, soru_sayisi: { type: 'integer' },
        kazanim_kapsami: { type: 'array', items: { type: 'string' } },
        siparisler: {
          type: 'array',
          items: {
            type: 'object', additionalProperties: true,
            required: ['sira', 'band', 'hedef_kelime', 'kok_tipi', 'zorluk', 'kalip', 'metin_turu', 'bloom', 'kazanim_kod', 'hedef_dogru_harf'],
            properties: {
              sira: { type: 'integer' }, band: { type: 'string' }, hedef_kelime: { type: 'integer' },
              kok_tipi: { type: 'string' }, zorluk: { type: 'string' }, kalip: { type: 'string' },
              metin_turu: { type: 'string' }, bloom: { type: 'string' }, dab_kodu: { type: 'string' },
              kazanim_kod: { type: 'string' }, serbest_konu: { type: 'string' },
              hedef_dogru_harf: { type: 'string', enum: ['A', 'B', 'C', 'D', 'E'] },
            },
          },
        },
        dagilim_ozeti: { type: 'object', additionalProperties: true },
      },
    },
    kaynak_baglami: {
      type: 'object', additionalProperties: true,
      required: ['kazanimlar'],
      properties: {
        kazanimlar: { type: 'array', items: { type: 'object', additionalProperties: true } },
        ders_kitabi_ozeti: { type: 'string' }, uyarilar: { type: 'string' },
      },
    },
  },
}

// ---------------------------------------------------------------------------
// Subagent sistem promptları. Custom agentType bu session registry'sinde
// tanınmadığı için, .claude/agents/*.md içerikleri build adımında buraya gömülür
// (pipeline/build_workflow.py) ve general-purpose ajana sistem promptu olarak verilir.
const AJAN = {/*__AJAN__*/};
function gorev(rol, metin) {
  const sistem = AJAN[rol] || '';
  return sistem + '\n\n============================\n=== BU ÇAĞRININ GÖREV GİRDİSİ ===\n============================\n' + metin;
}

let a = args || {}
if (typeof a === 'string') { try { a = JSON.parse(a) } catch (e) { a = {} } }  // args string olarak gelirse çöz
const sinif = a.sinif ?? 11
const unite = a.unite ?? 2
const sinav_turu = a.sinav_turu ?? 'TYT'
const soru_sayisi = a.soru_sayisi ?? 12
const blueprint_ref = a.blueprint_ref ?? `DKAB${sinif}-U${unite}-T1`
const tymm_yolu = a.tymm_yolu ?? ''
const ders_kitabi_yolu = a.ders_kitabi_yolu ?? ''

phase('Kurgu')
log(`Blueprint kuruluyor: ${sinif}. sınıf Ünite ${unite}, ${soru_sayisi} soru (${sinav_turu})`)
if (!tymm_yolu || !ders_kitabi_yolu) {
  log('UYARI: tymm_yolu/ders_kitabi_yolu boş — içerik kaynağa dayanmayabilir (grounding yok). uret.py args ile yol geç.')
}

const kurgu = await agent(
  gorev('test_kurgu', `Bu test için blueprint ve kaynak bağlamını üret.
Girdi: ${JSON.stringify({ sinif, unite, sinav_turu, soru_sayisi, tymm_yolu, ders_kitabi_yolu, blueprint_ref })}
KAYNAK OKUMA: tymm_yolu ve ders_kitabi_yolu .txt ise doğrudan Read et (pdftotext ÇALIŞTIRMA); .pdf ise pdftotext ile çıkar. Resmî kazanımları (uydurmadan) ve anahtar kavramları çıkar.
BLUEPRINT: dengeli-ama-standart-olmayan kur (KANON K3/K7/K8/K9 + v2 sıkılaştırmaları).
soru_sayisi BAĞLAYICITIR: TAM ${soru_sayisi} sipariş üret (ne az ne fazla). ${soru_sayisi} < 9 ise (küçük/smoke test) üç bandı (30-70/70-100/100-150) mümkün olduğunca eşit paylaştır (ör. 3 soruda her banttan ~1), yine de en az 1 olumsuz kök + zorluk/kalıp çeşitliliğini koru.
V1 (ZORUNLU): her siparişe 'hedef_dogru_harf' ata; test genelinde A-E DENGELİ olsun (hiçbir harf %28'i aşmasın; mekanik A,B,C,D,E deseni değil, karışık).
V8: kazanımları eşit dağıt (her kazanım ortalama ±1 soru; fark ≤2).
V9: Analiz/Değerlendirme oranını yüksek tut (testin ≥%50'si gerçek çıkarım/analiz).
Çıktı: {blueprint, kaynak_baglami}. blueprint.siparisler tam ${soru_sayisi} eleman ve her birinde hedef_dogru_harf içermeli.`),
  { agentType: 'general-purpose', schema: KURGU_OUT, phase: 'Kurgu' }
)

if (!kurgu || !kurgu.blueprint || !kurgu.blueprint.siparisler) {
  return { hata: 'test-kurgu blueprint üretemedi', kurgu }
}

let siparisler = kurgu.blueprint.siparisler
if (siparisler.length > soru_sayisi) {
  log(`Blueprint ${siparisler.length} sipariş üretti; istenen ${soru_sayisi}'e kırpılıyor (soru_sayisi bağlayıcı).`)
  siparisler = siparisler.slice(0, soru_sayisi)
}
const kaynak = kurgu.kaynak_baglami
log(`Blueprint hazır: ${siparisler.length} sipariş. Sorular üretiliyor...`)

// kazanım koduna göre ilgili bağlamı bul
function kazanimBaglami(kod) {
  const liste = (kaynak && kaynak.kazanimlar) || []
  const m = liste.find(k => (k.kod || '').includes(kod) || kod.includes(k.kod || '###'))
  return {
    kazanim: m || { kod, serbest_konu: kod },
    ders_kitabi_ozeti: (kaynak && kaynak.ders_kitabi_ozeti) || '',
    uyarilar: (kaynak && kaynak.uyarilar) || '',
  }
}

// her sipariş bağımsız: metin -> şıklar -> (denetle -> düzelt döngüsü)
const sonuclar = await pipeline(
  siparisler,

  // STAGE 1 — soru-metni
  (siparis) => {
    const bag = kazanimBaglami(siparis.kazanim_kod)
    return agent(
      gorev('soru_metni', `Bu blueprint siparişi için sorunun GÖVDE METNİNİ ve KÖKÜNÜ yaz (şık yazma).
SİPARİŞ: ${JSON.stringify(siparis)}
SINIF/SINAV: ${JSON.stringify({ sinif, sinav_turu, unite })}
KAZANIM BAĞLAMI: ${JSON.stringify(bag)}
Band sınırlarına ve hedef_kelime'ye uy; olumsuz kökte vurgu alanını doldur.`),
      { agentType: 'general-purpose', schema: SORU_METNI_OUT, phase: 'Yaz', label: `metin:${siparis.sira}` }
    )
  },

  // STAGE 2 — seçenekler
  (soruMetni, siparis) => {
    if (!soruMetni) return null
    return agent(
      gorev('secenekler', `Bu soruya 5 şık (A-E), doğru cevabı ve çözümü yaz. D1-D8 + v2 kurallarına uy.
V1: doğru şıkkı '${siparis.hedef_dogru_harf}' harfine yerleştir; dogru='${siparis.hedef_dogru_harf}'.
V2: cozum'u tam olarak "Doğru cevap ${siparis.hedef_dogru_harf}: ..." ile başlat; tüm harf atıfları nihai dizilişle tutarlı olsun.
V3-V6: çeldiriciler öğrenci yanılgısına dayalı (karikatür değil); doğru şık tek cümle parafrazı değil (sentez); tek savunulabilir doğru; uzunluk paritesi.
SORU (gövde+kök hazır): ${JSON.stringify(soruMetni)}`),
      { agentType: 'general-purpose', schema: SORU_TAM, phase: 'Yaz', label: `secenek:${siparis.sira}` }
    )
  },

  // STAGE 3 — çapraz-okuma + düzeltici döngüsü (loop-until-quality, ≤3 tur)
  async (soruTam, siparis, idx) => {
    if (!soruTam) return null
    const id = `${blueprint_ref}-${String(siparis.sira).padStart(3, '0')}`
    let soru = { ...soruTam, id, blueprint_ref, hedef_dogru_harf: siparis.hedef_dogru_harf }

    let rapor = await agent(
      gorev('capraz_okuma', `Bu soruyu ACIMASIZCA değerlendir (D1-D11). SORU: ${JSON.stringify(soru)}`),
      { agentType: 'general-purpose', schema: RAPOR_OUT, phase: 'Denetle', label: `denetle:${siparis.sira}` }
    )

    let tur = 0
    while (rapor && rapor.etiket !== 'Yayina_uygun' && tur < 3) {
      tur++
      const yeni = await agent(
        gorev('duzeltici', `Bu raporun açık D-kodlarını GERÇEK içerik değişikliğiyle kapat (kozmetik yama yasak, blueprint özelliklerini koru).
SORU: ${JSON.stringify(soru)}
RAPOR: ${JSON.stringify(rapor)}
TUR: ${tur}`),
        { agentType: 'general-purpose', schema: SORU_TAM, phase: 'Düzelt', label: `duzelt:${siparis.sira}.t${tur}` }
      )
      if (!yeni) break
      soru = { ...yeni, id, blueprint_ref, hedef_dogru_harf: siparis.hedef_dogru_harf }
      rapor = await agent(
        gorev('capraz_okuma', `Düzeltilmiş soruyu tekrar ACIMASIZCA değerlendir (D1-D11). SORU: ${JSON.stringify(soru)}`),
        { agentType: 'general-purpose', schema: RAPOR_OUT, phase: 'Denetle', label: `denetle:${siparis.sira}.t${tur}` }
      )
    }
    return { soru, rapor, tur }
  }
)

const temiz = sonuclar.filter(Boolean)
const yayina_uygun = temiz.filter(x => x.rapor && x.rapor.etiket === 'Yayina_uygun').length
log(`Tamamlandı: ${temiz.length}/${siparisler.length} soru üretildi, ${yayina_uygun} yayına uygun.`)

return {
  blueprint: kurgu.blueprint,
  sorular: temiz.map(x => x.soru),
  raporlar: temiz.map(x => ({ id: x.soru.id, etiket: x.rapor && x.rapor.etiket, puan: x.rapor && x.rapor.madde_puani, tur: x.tur, kritik: x.rapor && x.rapor.en_kritik_sorunlar })),
  ozet: { toplam: temiz.length, hedef: siparisler.length, yayina_uygun },
}
