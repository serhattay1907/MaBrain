# MabrAIn

**Modüler Çok-Ajanlı Kişisel Asistan Sistemi**

> Her biri kendi uzmanlık alanına ve görsel kimliğe sahip yapay zeka ajanlarının **Obsidian** adı verilen merkezi bir orkestratör altında koordineli çalıştığı, kişisel kullanım odaklı masaüstü asistan sistemi.

---

## Mevcut Durum

| Faz | Durum | Açıklama |
|-----|-------|----------|
| **Faz 0** | ✅ Tamamlandı | Ortam, klasör yapısı, hello world |
| **Faz 1** | 🔨 Devam ediyor | CLI + Conscience ajanı + tool calling |
| **Faz 2** | ⏳ Bekliyor | Electron UI + Daily ajanı |
| **Faz 3** | ⏳ Bekliyor | News ajanı + ChromaDB + ses |
| **Faz 4** | ⏳ Bekliyor | Paketleme + dağıtım |

---

## Ajanlar

| Ajan | Domain | Renk |
|------|--------|-------|
| **Conscience** | Dosya yönetimi, görev organizasyonu | `#6B5B95` |
| **Daily** | Hatırlatmalar, günlük rutin | `#FFB347` |
| **News** | Haber, finans, güncel olaylar | `#4A90E2` |

---

## Teknoloji Yığını

- **Backend:** Python 3.11+, LangGraph, Anthropic API (Claude Sonnet)
- **UI:** Electron + React + TypeScript + Tailwind CSS
- **Veritabanı:** SQLite (hatırlatmalar), ChromaDB (vektör bellek — Faz 3)
- **Ses:** Whisper.cpp (STT), Piper TTS (Türkçe)
- **İletişim:** FastAPI + WebSocket

---

## Kurulum (Faz 0)

### Gereksinimler

- Python 3.11+
- Node.js 20+
- Anthropic API key ([console.anthropic.com](https://console.anthropic.com))

### Adımlar

```bash
# 1. Repo'yu klonla
git clone https://github.com/KULLANICI_ADI/mabrain.git
cd mabrain

# 2. Python ortamını kur
cd backend
python -m venv venv
source venv/bin/activate        # Linux/Mac
# venv\Scripts\activate         # Windows
pip install -r requirements.txt

# 3. .env dosyasını oluştur
cp .env.example .env
# .env dosyasını aç ve ANTHROPIC_API_KEY değerini gir

# 4. Hello World testi
python hello_world.py
```

### CLI Testi (Faz 1)

```bash
cd backend
python cli.py
```

**Örnek komutlar:**
```
Sen: ~/test klasöründeki dosyaları listele
Sen: yarın saat 10'a TEKNOFEST toplantısı için hatırlatma kur
Sen: bugün teknoloji haberleri neler
```

---

## Güvenlik Notu

- `.env` dosyasını **asla** commit etme — `.gitignore` ile korunuyor
- Conscience ajanı yalnızca `ALLOWED_FOLDERS` içindeki dizinlere erişebilir
- Sistem ve kritik dizinler hard-coded olarak engellendi

---

## Mimari

```
mabrain/
├── backend/
│   ├── obsidian/        # Orkestratör (router + memory)
│   ├── agents/          # Conscience, Daily, News
│   ├── services/        # LLM, ChromaDB, TTS, STT
│   ├── tools/           # File, Reminder, Web tools
│   ├── core/            # Config, Logger, Budget, Safety
│   ├── hello_world.py   # Faz 0 test
│   └── cli.py           # Faz 1 CLI
├── ui/                  # Electron + React (Faz 2)
├── docs/adr/            # Architecture Decision Records
└── tests/               # Eval testleri
```

---

## Kapsam Dışı (V1)

Bu özellikler kasıtlı olarak V2/V3'e ertelendi:

- Holografik 3D beyin görselleştirmesi
- Mobil uygulama, akıllı saat entegrasyonu
- Google Calendar/Gmail bağlantısı
- Sürekli mikrofon dinleme (wake word)
- Çoklu kullanıcı desteği

---

*Geliştirici: Volkan · TEKNOFEST 2026 Aytunga ekibi ile paralel yürütülüyor*
