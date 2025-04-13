import streamlit as st
import json
import os

st.title("🧠 Kişiselleştirilmiş Yapay Zeka Botu")

# Kullanıcı bilgilerini al
isim = st.text_input("İsminizi girin:")
ilgi = st.selectbox("En çok neyle ilgilenirsiniz?", ["", "müzik", "spor", "teknoloji", "sanat"])

if isim:
    dosya_adi = f"{isim.lower()}.json"
    gecmis_dosyasi = f"{isim.lower()}_gecmis.json"
    ogretilen_dosya = f"{isim.lower()}_ogretilen.json"

    # Kullanıcı daha önce kayıtlı mı?
    if os.path.exists(dosya_adi):
        with open(dosya_adi, "r") as dosya:
            kullanici = json.load(dosya)
        ilgi = kullanici["ilgi"]
        st.success(f"Tekrar hoş geldin {isim.capitalize()}! İlgi alanın: {ilgi}")
    else:
        if ilgi:
            kullanici = {"isim": isim.lower(), "ilgi": ilgi}
            with open(dosya_adi, "w") as dosya:
                json.dump(kullanici, dosya)
            st.success(f"Hoş geldin {isim.capitalize()}! Seni kaydettim 🎉")

    # Genel cevaplar
    cevaplar = {
        "hava nasıl": "Bugün hava parçalı bulutlu.",
        "nasılsın": "Ben bir yapay zekâyım, hep iyiyim!",
        "ne yapıyorsun": "Seninle sohbet etmek çok keyifli!"
    }

    # İlgi alanına özel cevaplar
    ilgi_cevaplar = {
        "müzik": f"{isim}, şu sıralar Spotify'da pop listeleri çok popüler!",
        "spor": f"{isim}, bugün Galatasaray maçı olduğunu biliyor muydun? ⚽",
        "teknoloji": f"{isim}, son çıkan yapay zekâ haberlerine göz attın mı?",
        "sanat": f"{isim}, İstanbul Modern’deki yeni sergiyi mutlaka görmelisin!"
    }

    # Önceden öğretilen sorular
    ogretilen_cevaplar = {}
    if os.path.exists(ogretilen_dosya):
        with open(ogretilen_dosya, "r") as dosya:
            ogretilen_cevaplar = json.load(dosya)

    # Geçmişi göster butonu
    if st.button("📜 Sohbet Geçmişini Göster"):
        if os.path.exists(gecmis_dosyasi):
            with open(gecmis_dosyasi, "r") as dosya:
                gecmis = json.load(dosya)
            for satir in gecmis:
                st.write(f"👤 {satir['soru']}")
                st.write(f"🤖 {satir['cevap']}")
        else:
            st.warning("Henüz geçmiş bulunamadı.")

    # Geçmişi temizle butonu
    if st.button("🧹 Sohbet Geçmişini Temizle"):
        if os.path.exists(gecmis_dosyasi):
            os.remove(gecmis_dosyasi)
            st.success("Sohbet geçmişi temizlendi.")

    # Bot'a soru sor
    soru = st.text_input("Bot'a bir şey sor:")

    if soru:
        soru = soru.lower()

        # Cevap üretme sırası
        if soru in cevaplar:
            cevap = cevaplar[soru]
        elif "ilgi" in soru or "öner" in soru:
            cevap = ilgi_cevaplar.get(ilgi, "Bu konuda pek bilgim yok ama öğrenmeye hazırım!")
        elif soru in ogretilen_cevaplar:
            cevap = ogretilen_cevaplar[soru]
        else:
            st.warning("Bu soruya henüz cevap veremiyorum. Aşağıya cevap girersen öğrenebilirim 👇")
            yeni_cevap = st.text_input("Bu soruya ne cevap vermemi istersin?")
            if yeni_cevap:
                ogretilen_cevaplar[soru] = yeni_cevap
                with open(ogretilen_dosya, "w") as dosya:
                    json.dump(ogretilen_cevaplar, dosya, indent=2)
                st.success("Yeni cevabı öğrendim, teşekkür ederim!")
                cevap = yeni_cevap

        # Eğer cevap belirlendiyse göster ve geçmişe ekle
        if "cevap" in locals():
            st.info(f"{isim}, {cevap}")

            yeni_kayit = {"soru": soru, "cevap": cevap}
            if os.path.exists(gecmis_dosyasi):
                with open(gecmis_dosyasi, "r") as dosya:
                    gecmis = json.load(dosya)
            else:
                gecmis = []
            gecmis.append(yeni_kayit)
            with open(gecmis_dosyasi, "w") as dosya:
                json.dump(gecmis, dosya, indent=2)
