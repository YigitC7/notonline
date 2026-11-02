# 📝 NotOnline

**NotOnline**, Python ve Flask kullanılarak tek başıma geliştirdiğim web tabanlı bir online not tutma uygulamasıdır.

Kullanıcıların not defterleri oluşturmasına, notlarını çevrimiçi olarak saklamasına ve başkalarıyla paylaşmasına olanak tanır.

NotOnline'ın öne çıkan özelliklerinden biri, oluşturulan not defterlerinin **herkese açık (Public)** hâle getirilebilmesi veya diğer kullanıcılara **yazma yetkisi** verilerek ortak bir şekilde düzenlenebilmesidir.

Proje şu an temel özellikleriyle çalışan bir beta sürümündedir. Gelişmiş kullanıcı yönetimi ve güvenlik mekanizmaları henüz tamamlanmamıştır.

## ✨ Öne Çıkan Özellikler

- 📚 Online not defteri oluşturma ve düzenleme
- 🌍 Not defterlerini herkese açık hâle getirme
- 👥 Diğer kullanıcılara yazma yetkisi verme
- 🔐 Parolaların Argon2 ile güvenli şekilde hashlenmesi
- 🔒 Not verilerinin Fernet ile şifrelenmesi
- 🗄️ SQLite tabanlı veri saklama
- 🌐 Flask tabanlı web altyapısı

## 🛠️ Kullanılan Teknolojiler

| Teknoloji | Kullanım Alanı |
|---|---|
| Python | Ana programlama dili |
| Flask | Web sunucusu ve uygulama altyapısı |
| SQLite3 | Veritabanı yönetimi |
| Argon2-CFFI | Parola hashleme |
| Cryptography | Veri şifreleme |

## 📊 Yazılım Değerlendirmesi

| Kategori | Durum |
|---|---|
| Uygulama Güvenliği | Temel |
| Yazılım Mimarisi | Güçlü |
| Kullanıcı Hesap Yönetimi | Geliştirilmeli |
| Kullanışlılık | Yeterli |
| Optimizasyon | Yeterli |

*Bu değerlendirme projenin mevcut geliştirme aşamasını yansıtmaktadır.*

## ⚙️ Kurulum

Gerekli Python paketlerini yüklemek için:

```bash
pip install flask argon2-cffi cryptography
```

Ardından projeyi çalıştırmak için:

```bash
python server.py
```

## 🚧 Sürüm Bilgisi

**Mevcut sürüm:** `v0.0.1 Beta`

**İlk çalışan sürüm:** `v0.0.1 Beta`

> ⚠️ NotOnline henüz geliştirme aşamasındadır. İlk beta sürümü kesin ve güvenilir kullanım için hazır değildir. Bazı özellikler eksik olabilir ve güvenlik iyileştirmelerine ihtiyaç duyulmaktadır.

## 👨‍💻 Geliştirici

NotOnline, bireysel olarak geliştirdiğim açık kaynaklı bir yazılım projesidir.
