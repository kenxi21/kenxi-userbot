# 🚀 KENXI USERBOT - King of Ubot

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Pyrogram](https://img.shields.io/badge/Pyrogram-2.0.106-green.svg)
![License](https://img.shields.io/badge/License-Private-red.svg)

**The Ultimate Telegram Userbot dengan Multi-Session Management**

[Features](#-fitur-utama) • [Installation](#-instalasi) • [Commands](#-daftar-command) • [Usage](#-cara-penggunaan)

</div>

---

## 📖 Deskripsi

KENXI Userbot adalah Telegram Userbot premium yang dilengkapi dengan **Multi-Session Management System**. Bot ini memungkinkan Anda untuk mengelola multiple userbot sekaligus dengan satu helper bot, lengkap dengan sistem admin, auto-reply, group monitoring, broadcast, dan banyak fitur lainnya.

### 🌟 Kenapa KENXI?

- ✅ **Multi-Session Support** - Kelola ratusan userbot dalam satu sistem
- ✅ **Admin Management** - Role-based access control untuk tim
- ✅ **Auto Expiry** - Session otomatis expire dan cleanup
- ✅ **Comprehensive Logging** - Track semua aktivitas userbot
- ✅ **Broadcast System** - Kirim pesan ke semua grup sekaligus
- ✅ **Auto-Reply PM** - Balas PM otomatis dengan anti-spam
- ✅ **Group Monitoring** - Deteksi join/leave grup otomatis
- ✅ **50+ Commands** - Fitur lengkap untuk daily usage
- ✅ **Stable & Fast** - Zero lag dengan uptime 99.9%

---

## 🎯 Fitur Utama

### 1. 🤖 Multi-Userbot Management
- Login multiple userbot dengan API credentials berbeda
- Auto-start semua userbot saat sistem startup
- Session expiry tracking (default: 30 hari)
- Auto-cleanup expired sessions dengan notifikasi
- Owner dan Admin memiliki dashboard terpisah

### 2. 👥 Admin System
- **Owner**: Full access ke semua fitur dan userbot
- **Admin**: Dapat login userbot dan manage miliknya sendiri
- Command `/admin` untuk promote user
- Command `/unadmin` untuk demote admin
- Auto-notification saat status berubah

### 3. 💬 Auto-Reply System
- Auto-reply incoming PM dengan custom message
- Maximum 3 replies per user (anti-spam protection)
- `.stoppm` - Stop auto-reply untuk user tertentu
- `.unstoppm` - Aktifkan kembali auto-reply
- `.listpm` - Lihat daftar stopped users
- `.clearpm` - Clear semua stopped users
- Toggle global on/off

### 4. 📊 Group Monitoring
- Scan semua grup aktif
- Auto-detect join/leave grup
- Background monitoring setiap 5 menit
- Database logging untuk semua aktivitas
- Real-time notifications

### 5. 📢 Broadcast System
- Broadcast pesan ke semua grup sekaligus
- Test mode (kirim ke 3 grup pertama)
- Intelligent FloodWait handling
- Progress tracking real-time
- Success/failed statistics

### 6. 📝 Comprehensive Logging
- Log mentions/tags dari grup
- Log join/leave events
- Log private messages
- Statistics dashboard
- Database-backed persistent storage

### 7. 💳 Payment/QRIS System
- Set payment info dengan foto QRIS
- Custom payment text/caption
- Delete payment data
- Quick `.pay` command untuk share ke chat

#### Broadcast (GCAST)
| Command | Deskripsi | Contoh |
|---------|-----------|--------|
| `.gcast <teks/reply>` | Broadcast ke semua GRUP | `.gcast Halo` (atau reply) |
| `.gucast <teks/reply>` | Broadcast ke semua PM (User) | `.gucast Halo gan` |
| `.jaseball <teks>` | Broadcast sederhana (teks only) | `.jaseball Promo` |

#### Animation & Spammands
- 10+ animasi emoji built-in
- Adjustable animation speeds
- Stop command untuk hentikan animasi
- No flood errors

### 9. 📨 Spam & Broadcast
- Delay spam dengan custom interval
- FloodWait handling otomatis
- Slowmode detection
- Emergency stop mechanism

### 10. 🔐 Security & Safety
- Session encryption via Pyrogram
- 2FA (Two-Factor Authentication) support
- Automatic error recovery
- Graceful shutdown handling
- Database transaction safety

---

## 📋 Requirements

- Python 3.9 atau lebih tinggi
- Telegram API ID & Hash ([my.telegram.org](https://my.telegram.org))
- Bot Token dari [@BotFather](https://t.me/BotFather)
- Virtual environment (recommended)

---

## 📱 Contact & Support

- **Owner:** [@MAU_BOBO](https://t.me/MAU_BOBO)
- **Channel:** @kenxiubot
- **Support:** DM owner untuk bantuan

---

## 📜 License

© 2026 KENXI Userbot. All rights reserved.

**Private License** - Tidak untuk distribusi tanpa izin owner.

---

## 🙏 Credits

- **Developer:** @MAU_BOBO
- **Framework:** [Pyrogram](https://github.com/pyrogram/pyrogram)
- **Database:** SQLite3
- **Language:** Python 3.9+

---

## 🚀 Changelog

### Version 1.0 (2026-01-04)
- ✅ Initial release
- ✅ Multi-userbot management system
- ✅ Admin role system
- ✅ 50+ commands
- ✅ Comprehensive logging
- ✅ Auto-reply PM
- ✅ Group monitoring
- ✅ Broadcast system
- ✅ Payment system

---

<div align="center">

**Made with ❤️ by KENXI Team**

⭐ **If you like this project, give it a star!** ⭐

</div>
