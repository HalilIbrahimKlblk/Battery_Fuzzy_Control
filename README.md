# 🔋 Elektrikli Araçlar İçin Bulanık Mantık Tabanlı Batarya Sıcaklık Yönetimi

Bu proje, Elektrikli Araçlarda (EV) batarya sıcaklığını optimize etmek amacıyla **Bulanık Mantık (Fuzzy Logic)** kullanılarak geliştirilmiş akıllı bir kontrol ve simülasyon panelidir. Sistem, sürüş ve çevre koşullarını analiz ederek batarya soğutma pompasının (kompresör) anlık gücünü belirler.

Bulanık Mantık Dersi Dönem Projesi kapsamında geliştirilmiştir.

---

## ✨ Özellikler

* **Çoklu Sensör Girdisi:** Araç ve çevre durumunu simüle eden 6 farklı giriş parametresi.
* **Mamdani Çıkarım Modeli:** Scikit-Fuzzy kütüphanesi altyapısıyla çalışan 20 adet özel bulanık mantık kuralı.
* **Modern Web Arayüzü:** Streamlit ile geliştirilmiş, özel CSS ile desteklenmiş, kullanıcı dostu interaktif kontrol paneli.
* **Canlı Telemetri ve Loglama:** Simülasyon boyunca yapılan değişiklikleri kayıt altına alan, termal reaksiyon statülerini gösteren ve verileri `.csv` olarak dışa aktarabilen log sistemi.
* **Dinamik Görselleştirme:** Matplotlib kullanılarak anlık değerlerin üyelik fonksiyonları (Membership Functions) üzerindeki konumunun ve durulaştırma (Defuzzification) grafiğinin çizdirilmesi.
* **Akademik Test Senaryoları:** Şehir içi sürüş, otoyol rejimi, hızlı şarj gibi hazır senaryolarla sistem validasyonu.

---

## 🛠️ Kullanılan Teknolojiler

* **Dil:** Python 3.9+
* **Arayüz:** Streamlit
* **Bulanık Mantık Motoru:** scikit-fuzzy
* **Veri ve Görselleştirme:** NumPy, Pandas, Matplotlib

---

## ⚙️ Kurulum ve Çalıştırma

Projeyi yerel bilgisayarınızda çalıştırmak için aşağıdaki adımları izleyin.

**1. Gerekli kütüphaneleri yükleyin:**
Proje dizininde bir terminal açın ve aşağıdaki komutu çalıştırarak bağımlılıkları indirin:
```bash
pip install streamlit numpy matplotlib scikit-fuzzy pandas
streamlit run app.py
