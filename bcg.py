from pyrogram import Client, filters
from pyrogram.enums import ChatType
import asyncio

# --- MASUKKAN DATA DARI MY.TELEGRAM.ORG ---
api_id = 30046211         # Ganti dengan Angka API ID kamu
api_hash = "b087e9f54e05a223a4e87577f754fbd1"    # Ganti dengan API Hash kamu

app = Client("haii", api_id=api_id, api_hash=api_hash)

# ==========================================
# FITUR 1: ANTI VIEW-ONCE (TIDAK BERUBAH)
# ==========================================
@app.on_message(filters.private & ~filters.me & (filters.photo | filters.video))
async def anti_view_once(client, message):
    is_view_once = False
    if message.photo and message.photo.ttl_seconds:
        is_view_once = True
    elif message.video and message.video.ttl_seconds:
        is_view_once = True

    if is_view_once:
        file = await message.download()
        await client.send_document("me", file, caption=f"Diamankan dari: {message.from_user.first_name}")

# ==========================================
# FITUR 2: BROADCAST KHUSUS GRUP (.bcg)
# ==========================================
@app.on_message(filters.me & filters.command("bcg", prefixes="."))
async def broadcast_group(client, message):
    # Mengambil teks setelah perintah .bcg
    if len(message.text.split()) > 1:
        pesan_bc = message.text.split(None, 1)[1]
    else:
        await message.reply("❌ Format salah. Gunakan: `.bcg pesan promo kamu`")
        return

    await message.reply("⏳ Memulai broadcast ke semua GRUP...")
    sukses = 0
    gagal = 0
    
    # Looping ke semua riwayat chat
    async for dialog in client.get_dialogs():
        # Filter: Hanya Grup dan Supergroup
        if dialog.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
            try:
                await client.send_message(dialog.chat.id, pesan_bc)
                sukses += 1
                # Jeda 3 detik agar lebih aman dari banned (grup lebih ketat filternya)
                await asyncio.sleep(3) 
            except Exception:
                gagal += 1

    await message.reply(f"✅ Broadcast Grup Selesai!\n🚀 Berhasil: {sukses} grup\n❌ Gagal: {gagal} (Mungkin kamu di-mute/kick)")

print("🚀 Userbot Khusus Grup & Anti-View-Once Menyala!")
app.run()
