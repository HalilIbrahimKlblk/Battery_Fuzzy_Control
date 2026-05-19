# 🔋 Elektrikli Araçlar İçin Bulanık Mantık Tabanlı Batarya Sıcaklık Yönetimi

![Python Version](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-FF4B4B.svg)
![Scikit-Fuzzy](https://img.shields.io/badge/Scikit--Fuzzy-0.4.2-green.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

Bu proje, Elektrikli Araçlarda (EV) batarya sıcaklığını optimize etmek amacıyla **Bulanık Mantık (Fuzzy Logic)** kullanılarak geliştirilmiş akıllı bir kontrol ve simülasyon panelidir. Sistem sürüş dinamiklerini ve çevre koşullarını eşzamanlı analiz ederek batarya soğutma pompasının (kompresör) anlık güç ihtiyacını belirler.

> 🎓 *Bulanık Mantık Dersi Dönem Projesi kapsamında tasarlanmış ve geliştirilmiştir.*

---

## ✨ Öne Çıkan Özellikler

- 🎛️ **Çoklu Sensör Simülasyonu:** 6 farklı çevresel ve dinamik araç verisinin anlık girişi.
- 🧠 **Mamdani Çıkarım Modeli:** 20 adet özel tasarlanmış bulanık kural matrisi ile tam otonom karar mekanizması.
- 📊 **Dinamik Görselleştirme:** Matplotlib entegrasyonu ile anlık durulaştırma (defuzzification) grafiklerinin canlı çizimi.
- 💾 **Canlı Telemetri ve Loglama:** Her hesaplama adımının kayıt altına alınması ve `.csv` formatında dışa aktarılabilmesi.
- 🎨 **Modern ve Responsive UI:** Streamlit üzerine inşa edilmiş, özel CSS ile geliştirilmiş cam (glassmorphism) tasarımlı karanlık mod arayüzü.

---

## 📂 Proje Dosya Yapısı

Projeyi klonladığınızda karşılaşacağınız temel dizin yapısı aşağıdaki gibidir:

```text
📁 fuzzy-battery-thermal-management
├── 📄 app.py               # Ana simülasyon kodları, UI ve bulanık mantık kuralları
├── 📄 requirements.txt     # Projenin çalışması için gereken kütüphaneler listesi
├── 📄 README.md            # Proje dokümantasyonu (Bu dosya)
└── 📂 assets/              # (Opsiyonel) Projeye ait ekran görüntüleri veya loglar
```
---

## 🧠 Bulanık Mantık Mimarisi ve Parametreler

Sistem, karar verme sürecinde **Mamdani Çıkarım Yöntemini** kullanır. Aşağıdaki tablolarda sistemin girdi (Antecedent) ve çıktı (Consequent) değişkenleri detaylandırılmıştır.

### 📥 Girdi Değişkenleri (Antecedents)

| Sensör / Parametre | Değer Aralığı | Tanımlı Üyelik Kümeleri (Linguistic Terms) |
| :--- | :--- | :--- |
| **🌡️ Batarya Sıcaklığı** | `0 - 60 °C` | Düşük, Optimum, Yüksek, Kritik |
| **⚡ Motor Akım Yükü** | `% 0 - 100` | Sakin, Normal, Agresif |
| **🌍 Dış Ortam Sıcaklığı** | `-10 - 50 °C` | Soğuk, Ilık, Sıcak |
| **🚗 Araç Hızı** | `0 - 220 km/h` | Yavaş, Orta, Yüksek |
| **🔋 Şarj Seviyesi (SoC)** | `% 0 - 100` | Düşük, Orta, Tam Dolu |
| **❄️ Kabin Klima Talebi** | `% 0 - 100` | Kapalı, Düşük, Yüksek |

### 📤 Çıktı Değişkeni (Consequent)

| Karar Çıktısı | Değer Aralığı | Tanımlı Üyelik Kümeleri |
| :--- | :--- | :--- |
| **🗜️ Pompa Gücü (PWM)** | `% 0 - 100` | Pasif, Düşük, Orta, Yüksek, Maksimum |

### 📜 Kural Tabanı Örnekleri (Rule Base)

Sistem davranışını belirleyen toplam **20 adet çapraz denetimli kural** bulunmaktadır. Öne çıkan bazı kurallar şunlardır:
- **R01:** `EĞER` Sıcaklık DÜŞÜK `İSE` Pompa Gücü PASİF
- **R06:** `EĞER` Sıcaklık OPTİMUM `VE` Sürüş SAKİN `VE` Dış Ortam ILIK `İSE` Pompa Gücü DÜŞÜK
- **R09:** `EĞER` Sıcaklık KRİTİK `VE` Şarj TAM DOLU `VE` Yük AGRESİF `İSE` Pompa Gücü MAKSİMUM

*(Kuralların tamamı uygulama içerisindeki "Kural Tabanında Tanımlı Kurallar" sekmesinden incelenebilir.)*

---

## 🛠️ Kullanılan Teknolojiler ve Kütüphaneler

| Teknoloji | Kullanım Amacı |
| :--- | :--- |
| **Python** | Projenin temel programlama dili |
| **Streamlit** | İnteraktif web arayüzü ve dashboard tasarımı |
| **scikit-fuzzy** | Bulanık mantık (Fuzzy Logic) altyapısı ve çıkarım motoru |
| **Matplotlib** | Üyelik fonksiyonları ve durulaştırma (Defuzzification) grafikleri |
| **Pandas** | Telemetri verilerinin işlenmesi, tablo gösterimi ve CSV dışa aktarımı |

---

## 📸 Kullanım Senaryosu

1. Sol taraftaki **Giriş Değerleri** menüsünden araç hızını, batarya sıcaklığını, motor yükünü vb. parametreleri anlık olarak ayarlayın.
2. 🚀 **UYGULAMAYI BAŞLAT** butonuna basın.
3. Ana ekranda beliren **Sistem Modu**, **Kompresör Sinyal Genliği (PWM)** ve **Çıkış Grafiğini** analiz edin.
4. Alt kısımdaki **Log Tablosu** üzerinden yaptığınız farklı test senaryolarını (Şehir içi sürüş, hızlı şarj vb.) kıyaslayın ve cihazınıza indirin.

---

## ⚙️ Kurulum ve Çalıştırma

Projeyi yerel bilgisayarınızda çalıştırmak için aşağıdaki adımları sırasıyla izleyin:

### 1. Projeyi bilgisayarınıza klonlayın

### 2. Bağımlılıkları kurun

Projenin ihtiyaç duyduğu kütüphaneleri yüklemek için terminal (komut satırı) üzerinden aşağıdaki komutu çalıştırın:

```bash
pip install -r requirements.txt
```

### 3. Uygulamayı çalıştırın

Tüm kurulumlar tamamlandıktan sonra aynı terminal ekranında simülasyonu başlatmak için:

```bash
streamlit run app.py
```

> **Not:** Komutu girdikten sonra tarayıcınız otomatik olarak `http://localhost:8501` adresinde açılacaktır.
