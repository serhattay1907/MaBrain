# 🧠 MabrAIn

**Modüler Çok-Ajanlı Kişisel Asistan Sistemi**

MabrAIn, merkezi bir orkestratör olan **Obsidian** tarafından yönetilen, her biri farklı uzmanlığa ve görsel kimliğe sahip yapay zeka ajanlarından oluşan, kişisel kullanım odaklı masaüstü asistan sistemidir.

---

## 🤖 Ajanlar

| Ajan | Uzmanlık | Renk |
|------|----------|-------|
| **Conscience** | Dosya yönetimi ve görev organizasyonu | `#6B5B95` |
| **Daily** | Hatırlatmalar ve günlük rutinler | `#FFB347` |
| **News** | Finansal piyasalar ve güncel teknoloji haberleri | `#4A90E2` |

---

## 🛠 Teknoloji Yığını

*   **Backend:** Python 3.11+, LangGraph, Anthropic API (Claude Sonnet)
*   **Frontend:** Electron, React, TypeScript, Tailwind CSS
*   **Veri/Bellek:** SQLite (Hatırlatmalar), ChromaDB (Vektör belleği)
*   **Multimodal:** Whisper.cpp (STT), Piper TTS (Türkçe destekli)
*   **İletişim:** FastAPI ve WebSocket altyapısı

---

## ⚙️ Kurulum

### Gereksinimler
*   Python 3.11+
*   Node.js 20+
*   Anthropic API Key ([console.anthropic.com](https://console.anthropic.com))

### Adımlar
```bash
# Repo'yu klonla
git clone [https://github.com/KULLANICI_ADI/mabrain.git](https://github.com/KULLANICI_ADI/mabrain.git)
cd mabrain

# Python bağımlılıklarını kur
cd backend
python -m venv venv
source venv/bin/activate # Windows: venv\Scripts\activate
pip install -r requirements.txt

# .env dosyasını yapılandır
cp .env.example .env
# ANTHROPIC_API_KEY değerini gir

# Test et
python hello_world.py
