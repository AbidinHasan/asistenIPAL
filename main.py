from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import telebot
import time
import threading
from telebot import types
import os
from datetime import datetime
import socket
from config import TOKENS
from msds import *
from foto import *
from adminID import *
from stok import *

bot = telebot.TeleBot(token=TOKENS)


def is_admin(user_id):
    return user_id in admin_id

#Pesan Broadcast auto
#GUNAKAN TREADHING UNTUK MENYALAKAN  (hapus #)

def kirim_ke_semua():
    print("pesan broadcase berhasil")
    try:
        with open("ID_SHARE.txt", "r") as f:
            semua_id = f.read().splitlines()
        for chat_id in semua_id:
            bot.send_message(chat_id, "INFO!!!! \nREPORT MINGGUAN SUDAH UPDATE") #Isi pesan disini
            time.sleep(3)
            print("terkirim cuy")
    except Exception as e:
        print("Gagal Kirim cuyyy iki alasane :", e)
    print("wes kabeh")

@bot.message_handler(commands=['ser'])
def eksekusi(message):
    threading.Thread(target=kirim_ke_semua, daemon=True).start()    #untuk aktifkan
    bot.reply_to(message, "Broadcast ke semua orang sukses")

#membuat Tombol
def gen_markup(): 
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(waktu)
    print("menampilkan tombol")
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Tentang IPAL", callback_data="cb1"),
            InlineKeyboardButton("Foto IPAL", callback_data="cb2"))

    markup.add(InlineKeyboardButton("Video IPAL", callback_data="cb3"), 
            InlineKeyboardButton("REPORT MINGGUAN", callback_data="cb4"))
    
    markup.add(InlineKeyboardButton("(WI) WORK INSTRUCTION", callback_data="cb6"))
    markup.add(InlineKeyboardButton("Hasil LAB 🔬", callback_data="cb5"),
               InlineKeyboardButton("MSDS",callback_data="cb8"))
    markup.add(InlineKeyboardButton("UPLOAD 🚀", callback_data="cb7"),
               InlineKeyboardButton("STOK",callback_data="cb9"))
    return markup

#Tombol WI
# pilih WI

# Trigger dari callback
@bot.callback_query_handler(func=lambda call: call.data == "cb6")
def tombolWI(call):
    bot.answer_callback_query(call.id)
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(waktu)
    print("mencari WI")
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("BAK EQUALISASI",callback_data="wi1"),
            types.InlineKeyboardButton("BAK NETRALISATOR",callback_data="wi2"))
    
    markup.add(types.InlineKeyboardButton("BAK FLOKULATOR 1",callback_data="wi3"),
            types.InlineKeyboardButton("BAK KOAGULATOR 1",callback_data="wi4"))
    
    markup.add(types.InlineKeyboardButton("BAK AN AEROB",callback_data="wi5"),
            types.InlineKeyboardButton("BAK AEROB",callback_data="wi6"))
    
    markup.add(types.InlineKeyboardButton("BAK KOAGULATOR 2",callback_data="wi7"),
            types.InlineKeyboardButton("BAK FLOKULATOR 2",callback_data="wi8"))
    
    markup.add(types.InlineKeyboardButton("BAK THIKENER",callback_data="wi9"),
            types.InlineKeyboardButton("FILTER PRESS",callback_data="wi10"))
    
    markup.add(types.InlineKeyboardButton("POLIMER ANION",callback_data="wi11"),
            types.InlineKeyboardButton("POLIMER CATION",callback_data="wi12"))
    markup.add(types.InlineKeyboardButton("Kembali ↩️", callback_data="wi13"))
    
    kata = "PILIH WORK INSTRUCTION :"
    bot.send_message(call.message.chat.id, kata, reply_markup=markup )

    
    bot.delete_message(call.message.chat.id, call.message.message_id)


# Trigger msds
@bot.callback_query_handler(func=lambda call: call.data == "cb8")
def tombolWI(call):
    bot.answer_callback_query(call.id)
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(waktu)
    print("mencari MSDS")
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("WTC-01",callback_data="ms1"))
    markup.add(types.InlineKeyboardButton("ULTRA NUTRI BIO S",callback_data="ms2"))
    markup.add(types.InlineKeyboardButton("ULTRA BIOTIFIX",callback_data="ms3"))
    markup.add(types.InlineKeyboardButton("CAUSTIC SODA",callback_data="ms4"))
    markup.add(types.InlineKeyboardButton("Kembali ↩️", callback_data="wi13"))

    kata = "MATERIAL SAFETY DATA SHEET :"
    bot.send_message(call.message.chat.id, kata, reply_markup=markup )
    bot.delete_message(call.message.chat.id, call.message.message_id)


#Masukkan saran
@bot.message_handler(func=lambda msg: not msg.text.startswith('/'), content_types=['text'])
def simpan_text_user(message):
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(waktu)
    print("user memberi pesan")
    user = message.from_user
    with open("log_pesan.txt", "a") as file:
        file.write(f"{user.id} ({user.first_name}): {message.text}\n")
    kata = f'Pesan dari {user.first_name} :\n{message.text}'
    bot.reply_to(message, "Masukkan diterima bolo ✅")
    bot.send_message(admin_num, kata)



#Simpan Dokumen yg dikirim
@bot.message_handler(content_types=['document'])
def handle_document(message):
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(waktu)
    print("Kirim dokumen")
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    filename = message.document.file_name
    with open("/storage/emulated/0/serverbot/dokumen/" + f"file_dari_user_{filename}", 'wb') as new_file:
        new_file.write(downloaded_file)

    bot.reply_to(message, f"File '{filename}' tersimpan")


#Tolak video
@bot.message_handler(content_types=['video'])
def handle_video(message):
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(waktu)
    print("deteksi video")
    bot.reply_to(message, f"Sorry, tidak bisa menerima video bolo 🥲")
    

#Save foto yg dikirim
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(waktu)
    print("Kirim foto")
    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    # Ambil waktu sekarang dan ID user
    jam = datetime.now()
    cetakjam = jam.strftime("%H-%M-%S")
    timestamp = int(time.time())
    user_id = message.from_user.id
    nama = message.from_user.first_name

    # Buat nama file unik
    filename = f"foto_{message.caption}_{cetakjam}_{nama}_{user_id}_{timestamp}.jpg"

    # Simpan file
    with open("/storage/emulated/0/serverbot/foto/" + filename, 'wb') as new_file:
        new_file.write(downloaded_file)

    bot.reply_to(message, "Foto tersimpan")







@bot.callback_query_handler(func=lambda call: call.data == "wi13")
def tombolWI(call):
    bot.answer_callback_query(call.id)
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(waktu)
    print("GAK SIDO, menampilkan tombol kembali")
    markup = types.InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(types.InlineKeyboardButton("Tentang IPAL", callback_data="cb1"),
            types.InlineKeyboardButton("Foto IPAL", callback_data="cb2"))

    markup.add(types.InlineKeyboardButton("Video IPAL", callback_data="cb3"), 
            types.InlineKeyboardButton("REPORT MINGGUAN", callback_data="cb4"))
    
    markup.add(types.InlineKeyboardButton("(WI) WORK INSTRUCTION", callback_data="cb6"))

    markup.add(types.InlineKeyboardButton("Hasil LAB 🔬", callback_data="cb5"),
               types.InlineKeyboardButton("MSDS",callback_data="cb8"))
    
    markup.add(types.InlineKeyboardButton("UPLOAD 🚀", callback_data="cb7"),
               types.InlineKeyboardButton("STOK",callback_data="cb9"))
    
    kata = "MENU AWAL :"
    bot.send_message(call.message.chat.id, kata, reply_markup=markup)

    bot.delete_message(call.message.chat.id, call.message.message_id)
    



#Awal mulai
@bot.message_handler(commands=['start'])
def welcome(message):
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(waktu)
    p = message.from_user
    userid = message.from_user.id
    nama=message.from_user.first_name
    namaet = p.username if p.username else "(Tidak ada usename)"

    try:
        with open("/storage/emulated/0/serverbot/ID_LOGIN.txt", "r") as f:
            semua_id = f.read().splitlines()
    except FileNotFoundError:
        semua_id = []

    data_user = f"{userid}_({namaet})_{nama}"

    if data_user not in semua_id:
        with open("/storage/emulated/0/serverbot/ID_LOGIN.txt", "a") as f:
            f.write(data_user + "\n")
        print("User baru login")
    else:
        print("User lama")

    welcome_text = f'Halo {nama} Selamat datang di IPAL'
    bot.send_message(message.chat.id, welcome_text, reply_markup=gen_markup())
    bot.delete_message(message.chat.id, message.message_id)
    notif = f"Siapa yg login : ({nama}) id : ({userid}) username : ({namaet})"
    bot.send_message(admin_num, notif)
    print(notif)
    
    

#Tampilkan Tombol
@bot.message_handler(commands=['pilihan'])  
def tampilkan_opsi(message):
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(waktu)
    nama = message.from_user.first_name
    noid = message.from_user.id
    p = message.from_user
    namaet = p.username if p.username else "(Tidak punya username)"
    notif = f"({namaet}) id: ({noid}) jalok tombol"
    print(notif)
    

    try:
        with open("/storage/emulated/0/serverbot/ID_LOGIN.txt", "r") as f:
            semua_id = f.read().splitlines()
    except FileNotFoundError:
        semua_id = []

    data_user = f"{noid}_({namaet})_{nama}"

    if data_user not in semua_id:
        with open("/storage/emulated/0/serverbot/ID_LOGIN.txt", "a") as f:
            f.write(data_user + "\n")
        print("User baru login")
    else:
        print("User lama")

    surat = "Monggo dipilih :"
    bot.send_message(message.chat.id, surat, reply_markup=gen_markup())
    bot.delete_message(message.chat.id, message.message_id)
    bot.send_message(admin_id, notif)
    #threading.Thread(target=hapus_tombol_otomatis, args=(sent.chat.id, sent.message_id, 100)).start()

#===========================Class Execution===================================================
#Foto
# iki data ne utk diisi konten
def tampilkan_foto(chat_id):
    print('Akses gambar')

    kata = f"Equalisasi \nTempat balancing material limbah agar tercampur rata"
    kata2 = f"Root Blower \nMengaduk atau pelarutan oksigen yang ada pada air limbah"
    kata3 = f"Clarifier \nTempat sedimentasi lumpur, memastikan lumpur tidak ikut overflow ke tahap selanjutnya"
    kata4 = f"Bak Aerasi atau Aerob \nPengolahan limbah menggunakan mikro organisme,yang membutuhkan oksigen"
    kata5 = f"Pengolahan aerasi melalui clarifier biologi, bak kimia, dan clarifier kimia"
    kata6 = f"Air hasil pengolahan masuk ke bak fishpond"
    kata7 = f"Ikan sebagai monitoring parameter lingkungan"
    kata8 = f"Ruangan IPAL dan Gudang persediaan IPAL"
    kata9 = f"Tempat untuk preparation bahan kimia untuk pengolahan WWTP"
    kata10 = f"Filter Sand & Carbon"
    kata11 = f"Thikener \nPenampungan sludge dari clarifier"
    kata12 = f"Clarifier biologi"
    kata13 = f"Panel WWTP & STP"

    delay = (2)
    bot.send_photo(chat_id, photo=url_ekual, caption=kata)
    time.sleep(delay)
    bot.send_photo(chat_id, photo=url_rootBlow, caption=kata2)
    time.sleep(delay)
    bot.send_photo(chat_id, photo=url_cf, caption=kata3)
    time.sleep(delay)
    bot.send_photo(chat_id, photo=url_Aerob, caption=kata4)
    time.sleep(delay)
    bot.send_photo(chat_id, photo=url_aerasiDnCf, caption=kata5)
    time.sleep(delay)
    bot.send_photo(chat_id, photo=url_fishpond, caption=kata6)
    time.sleep(delay)
    bot.send_photo(chat_id, photo=url_ikan, caption=kata7)
    time.sleep(delay)
    bot.send_photo(chat_id, photo=url_ipalroom, caption=kata8)
    time.sleep(delay)
    bot.send_photo(chat_id, photo=url_PrepKimia, caption=kata9)
    time.sleep(delay)
    bot.send_photo(chat_id, photo=url_filter, caption=kata10)
    time.sleep(delay)
    bot.send_photo(chat_id, photo=url_thikener, caption=kata11)
    time.sleep(delay)
    bot.send_photo(chat_id, photo=url_kimia2, caption=kata12)
    time.sleep(delay)
    bot.send_photo(chat_id, photo=url_panel, caption=kata13)

    

# Trigger dari command
@bot.message_handler(commands=['foto'])
def handle_lihat_foto_command(message):
    nama = message.from_username
    
    noid = message.from_user.id
    print(f"{nama},id: {noid} mengakses lewat command")
    tampilkan_foto(message.chat.id)

# Trigger dari callback
@bot.callback_query_handler(func=lambda call: call.data == "cb2")
def handle_lihat_foto_callback(call):
    bot.answer_callback_query(call.id)
    

    loading_markup = InlineKeyboardMarkup()
    loading_markup.add(InlineKeyboardButton("⏳ Tunggu sek kawan", callback_data="disabled"))
    bot.edit_message_reply_markup(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=loading_markup
    )

    tampilkan_foto(call.message.chat.id)
    
    bot.delete_message(call.message.chat.id, call.message.message_id)
    


#Tentang ipal

# Trigger dari callback
@bot.callback_query_handler(func=lambda call: call.data == "cb1")
def handle_lihat_tentang_callback(call):
    print("Tentang IPAL")
    bot.answer_callback_query(call.id)
    

    loading_markup = InlineKeyboardMarkup()
    loading_markup.add(InlineKeyboardButton("⏳ Tunggu sek kawan", callback_data="disabled"))
    bot.edit_message_reply_markup(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=loading_markup
    )
    welcome_text = (f"*IPAL* adalah singkatan dari Instalasi Pengolahan Air Limbah. Ini adalah sistem atau fasilitas yang dirancang untuk mengolah air limbah (baik dari rumah tangga, industri, maupun komersial) sebelum air tersebut dibuang ke lingkungan, seperti sungai, danau, atau laut, agar tidak mencemari lingkungan.\n\n*Fungsi Utama IPAL :*\n\n1. Mengurangi pencemaran lingkungan \n– Limbah yang dibuang langsung tanpa diolah bisa mencemari air tanah dan perairan.\n2. Melindungi kesehatan manusia dan hewan \n– Air limbah sering mengandung bakteri, virus, bahan kimia beracun, dan logam berat.\nMemenuhi standar baku mutu air limbah \n– Agar sesuai dengan peraturan pemerintah sebelum dibuang ke lingkungan.\n\n*Jenis-jenis IPAL :*\n\n*IPAL Domestik:* Untuk limbah rumah tangga (seperti dari toilet, dapur, kamar mandi).\n\n*IPAL Industri:* Untuk limbah dari pabrik atau kegiatan industri (yang biasanya lebih kompleks dan mengandung bahan kimia khusus).\n\n*Proses dalam IPAL biasanya melibatkan :*\n\nProses fisik (penyaringan, pengendapan)\nProses kimia (netralisasi, koagulasi, flokulasi)\nProses biologi (menggunakan mikroorganisme untuk mengurai zat organik)")
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Kembali ↩️", callback_data="wi13"))
    
    
    bot.send_message(call.message.chat.id, welcome_text, reply_markup=markup, parse_mode="Markdown" )


    bot.delete_message(call.message.chat.id, call.message.message_id)
    


# Video
def tampilkan_video(chat_id):
    print("sedang akses video")
    url = "https://ik.imagekit.io/galleryBiden/aerob.mp4?updatedAt=1748960489775"
    bot.send_video(chat_id, video=url)

# Trigger dari command
@bot.message_handler(commands=['video'])
def handle_lihat_video_command(message):
    tampilkan_video(message.chat.id)

# Trigger dari callback
@bot.callback_query_handler(func=lambda call: call.data == "cb3")
def handle_lihat_video_callback(call):
    bot.answer_callback_query(call.id)
    

    loading_markup = InlineKeyboardMarkup()
    loading_markup.add(InlineKeyboardButton("⏳ Tunggu sek kawan", callback_data="disabled"))
    bot.edit_message_reply_markup(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=loading_markup
    )

    tampilkan_video(call.message.chat.id)

    bot.delete_message(call.message.chat.id, call.message.message_id)
    



# Laporan
def tampilkan_laporan(chat_id):
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(waktu)
    print("Kirim file Laporan")
    filenya = "/storage/emulated/0/serverbot/REPORT MINGGUAN IPAL.xlsx"
    with open (filenya, "rb" ) as Laporan_xsl:
        bot.send_document(chat_id, document=Laporan_xsl)
    file2 = "/storage/emulated/0/serverbot/Data Loging IPAL.xlsx"
    with open (file2, "rb") as Laporan2 :
        bot.send_document(chat_id, Laporan2)

# Trigger dari command
@bot.message_handler(commands=['lapor'])
def handle_lihat_laporan_command(message):
    tampilkan_laporan(message.chat.id)

# Trigger dari callback
@bot.callback_query_handler(func=lambda call: call.data == "cb4")
def handle_lihat_laporan_callback(call):
    bot.answer_callback_query(call.id)


    loading_markup = InlineKeyboardMarkup()
    loading_markup.add(InlineKeyboardButton("⏳ Tunggu sek kawan", callback_data="disabled"))
    bot.edit_message_reply_markup(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=loading_markup
    )

    tampilkan_laporan(call.message.chat.id)

    bot.delete_message(call.message.chat.id, call.message.message_id)
    


# Laporan LAB
def tampilkan_hasillab(chat_id):
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(waktu)
    print("info LAB resmi")
    url = "https://ik.imagekit.io/galleryBiden/dokumen/HASIL%20LAB%20IPAL%20APRIL%202025.pdf?updatedAt=1749008361205"
    bot.send_document(chat_id, document=url)

# Trigger dari command
@bot.message_handler(commands=['lab'])
def handle_lihat_lab_command(message):
    tampilkan_hasillab(message.chat.id)

# Trigger dari callback
@bot.callback_query_handler(func=lambda call: call.data == "cb5")
def handle_lihat_lab_callback(call):
    bot.answer_callback_query(call.id)
    

    loading_markup = InlineKeyboardMarkup()
    loading_markup.add(InlineKeyboardButton("⏳ Cari hasil LAB terbaru", callback_data="disabled"))
    bot.edit_message_reply_markup(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=loading_markup
    )
    kata = "Halis LAB terbaru :"
    bot.send_message(call.message.chat.id, kata)
    tampilkan_hasillab(call.message.chat.id,)
    
    bot.delete_message(call.message.chat.id, call.message.message_id)

@bot.callback_query_handler(func=lambda call: call.data == "cb7")
def upload(call):
    print("uplod")
    bot.answer_callback_query(call.id)
    

    loading_markup = InlineKeyboardMarkup()
    loading_markup.add(InlineKeyboardButton("⏳ Sek bos", callback_data="disabled"))
    bot.edit_message_reply_markup(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=loading_markup
    )
    kata = "Kirim : ... \n\n/edit      /help"
    
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("↩️ Back", callback_data="wi13"))
    
    bot.send_message(call.message.chat.id, kata, reply_markup=markup )
    
    bot.delete_message(call.message.chat.id, call.message.message_id)




# WI EQUAL
@bot.callback_query_handler(func=lambda call: call.data == "wi1")
def wi(call):
    bot.answer_callback_query(call.id)
    print("golek WI")

    loading_markup = InlineKeyboardMarkup()
    loading_markup.add(InlineKeyboardButton("⏳ Mencari data WI", callback_data="disabled"))
    bot.edit_message_reply_markup(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=loading_markup
    )
    
    link = "https://ik.imagekit.io/galleryBiden/dokumen/BPK_WI_082%20Pengeporasian%20IPAL%20WWTP%20-%20Bak%20Ekualisasi.pdf?updatedAt=1749008427848"
    bot.send_document(call.message.chat.id, link)

    bot.delete_message(call.message.chat.id, call.message.message_id)



# WI NETRALISATOR
@bot.callback_query_handler(func=lambda call: call.data == "wi2")
def wi(call):
    bot.answer_callback_query(call.id)
    print("golek WI")

    loading_markup = InlineKeyboardMarkup()
    loading_markup.add(InlineKeyboardButton("⏳ Mencari data WI", callback_data="disabled"))
    bot.edit_message_reply_markup(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=loading_markup
    )
    
    link = "ttps://ik.imagekit.io/galleryBiden/dokumen/BPK_WI_083%20Pengeporasian%20IPAL%20WWTP%20-%20Bak%20Netralisasi.pdf?updatedAt=1749008427260"
    bot.send_document(call.message.chat.id, link)

    bot.delete_message(call.message.chat.id, call.message.message_id)



# WI FLOKULATOR 1
@bot.callback_query_handler(func=lambda call: call.data == "wi3")
def wi(call):
    bot.answer_callback_query(call.id)
    print("golek WI")

    loading_markup = InlineKeyboardMarkup()
    loading_markup.add(InlineKeyboardButton("⏳ Mencari data WI", callback_data="disabled"))
    bot.edit_message_reply_markup(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=loading_markup
    )
    
    link = "https://ik.imagekit.io/galleryBiden/dokumen/BPK_WI_085%20Pengeporasian%20IPAL%20WWTP%20-%20Bak%20Flokulator-1.pdf?updatedAt=1749008422600"
    bot.send_document(call.message.chat.id, link)

    bot.delete_message(call.message.chat.id, call.message.message_id)

    

# WI KOAGULATOR 1
@bot.callback_query_handler(func=lambda call: call.data == "wi4")
def wi(call):
    bot.answer_callback_query(call.id)
    print("golek WI")

    loading_markup = InlineKeyboardMarkup()
    loading_markup.add(InlineKeyboardButton("⏳ Mencari data WI", callback_data="disabled"))
    bot.edit_message_reply_markup(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=loading_markup
    )
    
    link = "https://ik.imagekit.io/galleryBiden/dokumen/BPK_WI_084%20Pengeporasian%20IPAL%20WWTP%20-%20Bak%20Koagulator-1.pdf?updatedAt=1749008977528"
    bot.send_document(call.message.chat.id, link)

    bot.delete_message(call.message.chat.id, call.message.message_id)



# WI ANAEROB
@bot.callback_query_handler(func=lambda call: call.data == "wi5")
def wi(call):
    bot.answer_callback_query(call.id)
    print("golek WI")

    loading_markup = InlineKeyboardMarkup()
    loading_markup.add(InlineKeyboardButton("⏳ Mencari data WI", callback_data="disabled"))
    bot.edit_message_reply_markup(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=loading_markup
    )
    
    link = "https://ik.imagekit.io/galleryBiden/dokumen/BPK_WI_086%20Pengeporasian%20IPAL%20WWTP%20-%20Bak%20AnAerob.pdf?updatedAt=1749008421821"
    bot.send_document(call.message.chat.id, link)

    bot.delete_message(call.message.chat.id, call.message.message_id)



# WI AEROB
@bot.callback_query_handler(func=lambda call: call.data == "wi6")
def wi(call):
    bot.answer_callback_query(call.id)
    print("golek WI")

    loading_markup = InlineKeyboardMarkup()
    loading_markup.add(InlineKeyboardButton("⏳ Mencari data WI", callback_data="disabled"))
    bot.edit_message_reply_markup(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=loading_markup
    )
    
    link = "https://ik.imagekit.io/galleryBiden/dokumen/BPK_WI_087%20Pengeporasian%20IPAL%20WWTP%20-%20Bak%20Aerob.pdf?updatedAt=1749008421451"
    bot.send_document(call.message.chat.id, link)

    bot.delete_message(call.message.chat.id, call.message.message_id)
    


# WI KOAGULATOR 2
@bot.callback_query_handler(func=lambda call: call.data == "wi7")
def wi(call):
    bot.answer_callback_query(call.id)
    print("golek WI")

    loading_markup = InlineKeyboardMarkup()
    loading_markup.add(InlineKeyboardButton("⏳ Mencari data WI", callback_data="disabled"))
    bot.edit_message_reply_markup(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=loading_markup
    )
    
    link = "https://ik.imagekit.io/galleryBiden/dokumen/BPK_WI_088%20Pengeporasian%20IPAL%20WWTP%20-%20Bak%20Koagulator-2.pdf?updatedAt=1749008422032"
    bot.send_document(call.message.chat.id, link)

    bot.delete_message(call.message.chat.id, call.message.message_id)



# WI FLOKULATOR 2
@bot.callback_query_handler(func=lambda call: call.data == "wi8")
def wi(call):
    bot.answer_callback_query(call.id)
    print("golek WI")

    loading_markup = InlineKeyboardMarkup()
    loading_markup.add(InlineKeyboardButton("⏳ Mencari data WI", callback_data="disabled"))
    bot.edit_message_reply_markup(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=loading_markup
    )
    
    link = "https://ik.imagekit.io/galleryBiden/dokumen/BPK_WI_089%20Pengeporasian%20IPAL%20WWTP%20-%20Bak%20Flokulator-2.pdf?updatedAt=1749008422136"
    bot.send_document(call.message.chat.id, link)

    bot.delete_message(call.message.chat.id, call.message.message_id)



# WI THIKENER
@bot.callback_query_handler(func=lambda call: call.data == "wi9")
def wi(call):
    bot.answer_callback_query(call.id)
    print("golek WI")

    loading_markup = InlineKeyboardMarkup()
    loading_markup.add(InlineKeyboardButton("⏳ Mencari data WI", callback_data="disabled"))
    bot.edit_message_reply_markup(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=loading_markup
    )
    
    link = "https://ik.imagekit.io/galleryBiden/dokumen/BPK_WI_090%20Pengeporasian%20IPAL%20WWTP%20-%20Bak%20Thickener.pdf?updatedAt=1749008422393"
    bot.send_document(call.message.chat.id, link)

    bot.delete_message(call.message.chat.id, call.message.message_id)



# WI FILTER PRESS
@bot.callback_query_handler(func=lambda call: call.data == "wi10")
def wi(call):
    bot.answer_callback_query(call.id)
    print("golek WI")

    loading_markup = InlineKeyboardMarkup()
    loading_markup.add(InlineKeyboardButton("⏳ Mencari data WI", callback_data="disabled"))
    bot.edit_message_reply_markup(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=loading_markup
    )
    
    link = "https://ik.imagekit.io/galleryBiden/dokumen/BPK_WI_091%20Pengeporasian%20IPAL%20WWTP%20-%20Filter%20Press.pdf?updatedAt=1749008422299"
    bot.send_document(call.message.chat.id, link)

    bot.delete_message(call.message.chat.id, call.message.message_id)



# WI POLIMER ANION
@bot.callback_query_handler(func=lambda call: call.data == "wi11")
def wi(call):
    bot.answer_callback_query(call.id)
    print("golek WI")

    loading_markup = InlineKeyboardMarkup()
    loading_markup.add(InlineKeyboardButton("⏳ Mencari data WI", callback_data="disabled"))
    bot.edit_message_reply_markup(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=loading_markup
    )
    
    link = "https://ik.imagekit.io/galleryBiden/dokumen/BPK_WI_092%20Pengeporasian%20IPAL%20WWTP%20-%20Polimer%20Anion.pdf?updatedAt=1749008422324"
    bot.send_document(call.message.chat.id, link)

    bot.delete_message(call.message.chat.id, call.message.message_id)



# WI POLIMER CATION
@bot.callback_query_handler(func=lambda call: call.data == "wi12")
def wi(call):
    bot.answer_callback_query(call.id)
    print("golek WI")

    loading_markup = InlineKeyboardMarkup()
    loading_markup.add(InlineKeyboardButton("⏳ Mencari data WI", callback_data="disabled"))
    bot.edit_message_reply_markup(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=loading_markup
    )
    
    link = "https://ik.imagekit.io/galleryBiden/dokumen/BPK_WI_093%20Pengeporasian%20IPAL%20WWTP%20-%20Polimer%20Cation.pdf?updatedAt=1749008422488"
    bot.send_document(call.message.chat.id, link)

    bot.delete_message(call.message.chat.id, call.message.message_id)
    

# msds wtc01
@bot.callback_query_handler(func=lambda call: call.data == "ms1")
def msds(call):
    bot.answer_callback_query(call.id)
    print("golek MSDS")

    loading_markup = InlineKeyboardMarkup()
    loading_markup.add(InlineKeyboardButton("⏳ Material Safety Data Sheet", callback_data="disabled"))
    bot.edit_message_reply_markup(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=loading_markup
    )
    
    link = pac
    bot.send_document(call.message.chat.id, link)
    bot.delete_message(call.message.chat.id, call.message.message_id)

# msds nutrisi
@bot.callback_query_handler(func=lambda call: call.data == "ms2")
def msds(call):
    bot.answer_callback_query(call.id)
    print("golek MSDS")

    loading_markup = InlineKeyboardMarkup()
    loading_markup.add(InlineKeyboardButton("⏳ Material Safety Data Sheet", callback_data="disabled"))
    bot.edit_message_reply_markup(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=loading_markup
    )
    
    link = nutrisi
    bot.send_document(call.message.chat.id, link)
    bot.delete_message(call.message.chat.id, call.message.message_id)

# msds bakteri
@bot.callback_query_handler(func=lambda call: call.data == "ms3")
def msds(call):
    bot.answer_callback_query(call.id)
    print("golek MSDS")

    loading_markup = InlineKeyboardMarkup()
    loading_markup.add(InlineKeyboardButton("⏳ Material Safety Data Sheet", callback_data="disabled"))
    bot.edit_message_reply_markup(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=loading_markup
    )
    
    link = bakteriStater
    bot.send_document(call.message.chat.id, link)
    bot.delete_message(call.message.chat.id, call.message.message_id)

# msds NAOH
@bot.callback_query_handler(func=lambda call: call.data == "ms4")
def msds(call):
    bot.answer_callback_query(call.id)
    print("golek MSDS")

    loading_markup = InlineKeyboardMarkup()
    loading_markup.add(InlineKeyboardButton("⏳ Material Safety Data Sheet", callback_data="disabled"))
    bot.edit_message_reply_markup(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=loading_markup
    )
    
    link = naoh
    bot.send_document(call.message.chat.id, link)
    bot.delete_message(call.message.chat.id, call.message.message_id)

# Folder tempat dokumen disimpan
FOLDER_PATH = "/storage/emulated/0/serverbot/dokumen"
FOLDER_FOTO = "/storage/emulated/0/serverbot/foto"

# Command untuk kirim semua dokumen
@bot.message_handler(commands=['bidintex'])
def kirim_saran(message):
    print("Ambil file tersembunyi")
    FOLDER_SARAN = "/storage/emulated/0/serverbot/log_pesan.txt"
    chat_id = message.chat.id
    try:
        with open(FOLDER_SARAN, 'rb') as doc:
            bot.send_document(chat_id, doc)

    except Exception as e:
        bot.send_message(chat_id, f"Gagal")
    bot.send_message(chat_id, "Komplit")
    bot.delete_message(message.chat.id, message.message_id)


@bot.message_handler(commands=['bidin'])
def kirim_semua_dokumen(message):
    print("Ambil file tersembunyi")
    chat_id = message.chat.id

    for file_name in os.listdir(FOLDER_PATH):
        file_path = os.path.join(FOLDER_PATH, file_name)

        if os.path.isfile(file_path) and any(file_name):
            try:
                with open(file_path, 'rb') as doc:
                    bot.send_document(chat_id, doc)
            
            except Exception as e:
                bot.send_message(chat_id, f"Gagal mengirim {file_name}: {str(e)}")
    bot.send_message(chat_id, "Komplit")
    bot.delete_message(message.chat.id, message.message_id)


# Command untuk kirim semua foto
@bot.message_handler(commands=['bidinfoto'])
def kirim_semua_dokumen(message):
    print("Ambil foto tersembunyi")
    chat_id = message.chat.id
    nama = message.from_user.username
    print ("username : @",nama)



    for file_name in os.listdir(FOLDER_FOTO):
        file_path = os.path.join(FOLDER_FOTO, file_name)

        if os.path.isfile(file_path) and any(file_name):
            try:
                with open(file_path, 'rb') as photo:
                    bot.send_document(chat_id, photo)
    
                    
            except Exception as e:
                bot.send_message(chat_id, f"Gagal mengirim {file_name}: {str(e)}")
    bot.send_message(chat_id, "Komplit")
    bot.delete_message(message.chat.id, message.message_id)


#Help
@bot.message_handler(commands=['help'])
def handle_tolong(message):
    print("help cuy")
    user_id = message.from_user.id

    if not is_admin(user_id):
       bot.reply_to(message, "Akses tidak diijinkan")
       return

    teks = f"/bidin -> buka isi dokumen \n\n/bidinfoto -> buka isi foto \n\n/bidintex -> buka pesan user \n\n/ser -> broadcast woro woro"
    bot.send_message(message.chat.id, teks)


# Fungsi cek koneksi TCP
def check_tcp_latency(host, port):
    start = time.time()
    try:
        sock = socket.create_connection((host, int(port)), timeout=5)
        sock.close()
        latency = round((time.time() - start) * 1000, 2)
        timestamp = datetime.now().strftime("%d-%m-%Y 🕒 %H:%M:%S")
        result_lines = ["======================"]
        
        if latency < 60:
            status = "🟢 good"
        elif latency <= 99:
            status = "🟡 hmmm"
        else:
            status = "🔴 burik"
        result_lines.append(f"\n\n⏳ {latency} ms → {status}")
        return f"\n🗓️ {timestamp}".join(result_lines)
    except Exception as e:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"❌ Waduhhh\n📄 {e}\n🗓️ {timestamp}"

# Handler untuk command /tcp
@bot.message_handler(commands=['ping'])
def handle_tcp(message):
    user = message.from_user
    namaet = user.username
    noid = user.id
    notif = f"({namaet}) id: ({noid}) ping jaringan"
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(waktu)
    print("pingggggg")
    bot.send_message(message.chat.id, f"🔄 ping server... tunggu sebentar...")
    host, port = "google.com", "80"
    result = check_tcp_latency(host, port)
    bot.send_message(message.chat.id, result)
    bot.delete_message(message.chat.id, message.message_id)
    bot.send_message(admin_num, notif)


#fungsi penulisan & pembacaan ada di stok.py
# Format semua stok
@bot.message_handler(commands=['stok'])
def start(message):
    user_id = message.from_user.id

    if not is_admin(user_id):
       bot.reply_to(message, "Akses tidak diijinkan")
       return
    
    write_nutrisi(user_id, 0)
    write_pac(user_id, 0)
    write_polimerani(user_id, 0)
    write_bakteri(user_id, 0)
    write_polimerCAT(user_id, 0)
    write_chlorine(user_id, 0)
    write_codHR(user_id, 0)
    write_codLR(user_id, 0)
    write_karung(user_id, 0)
    write_naoh(user_id, 0)

    bot.reply_to(message, "Semua stok direset silahkan update.")

# Set poin nutrisi
@bot.message_handler(commands=['setnutri'])
def input_angka(message):
    user_id = message.from_user.id
    if not is_admin(user_id):
       bot.reply_to(message, "Akses tidak diijinkan")
       return


    try:
        angka = int(message.text.split()[1])
        user_id = message.from_user.id
        write_nutrisi(user_id, angka)
        bot.reply_to(message, f"Nilai di-set ke: {angka}")
    except:
        bot.reply_to(message, "Format salah. Gunakan: /setnutri <angka>")

# Tambah angka
@bot.message_handler(commands=['+nutri'])
def tambah(message):
    user_id = message.from_user.id
    if not is_admin(user_id):
       bot.reply_to(message, "Akses tidak diijinkan")
       return

    try:
        angka = int(message.text.split()[1])
        user_id = message.from_user.id
        current = read_nutrisi(user_id)
        new_value = current + angka
        write_nutrisi(user_id, new_value)
        bot.reply_to(message, f"Ditambah {angka}. Total: {new_value}")
    except:
        bot.reply_to(message, "Format salah. Gunakan: /+nutri <angka>")

# Kurang angka
@bot.message_handler(commands=['-nutri'])
def kurang(message):
    user_id = message.from_user.id
    if not is_admin(user_id):
       bot.reply_to(message, "Akses tidak diijinkan")
       return

    try:
        angka = int(message.text.split()[1])
        user_id = message.from_user.id
        current = read_nutrisi(user_id)
        new_value = current - angka
        write_nutrisi(user_id, new_value)
        bot.reply_to(message, f"Dikurangi {angka}. Total: {new_value}")
    except:
        bot.reply_to(message, "Format salah. Gunakan: /-nutri <angka>")

# Set poin pac
@bot.message_handler(commands=['setpac'])
def input_angka(message):
    user_id = message.from_user.id
    if not is_admin(user_id):
       bot.reply_to(message, "Akses tidak diijinkan")
       return


    try:
        angka = int(message.text.split()[1])
        user_id = message.from_user.id
        write_pac(user_id, angka)
        bot.reply_to(message, f"Nilai di-set ke: {angka}")
    except:
        bot.reply_to(message, "Format salah. Gunakan: /setnutri <angka>")

# Tambah angka
@bot.message_handler(commands=['+pac'])
def tambah(message):
    user_id = message.from_user.id
    if not is_admin(user_id):
       bot.reply_to(message, "Akses tidak diijinkan")
       return

    try:
        angka = int(message.text.split()[1])
        user_id = message.from_user.id
        current = read_pac(user_id)
        new_value = current + angka
        write_pac(user_id, new_value)
        bot.reply_to(message, f"Ditambah {angka}. Total: {new_value}")
    except:
        bot.reply_to(message, "Format salah. Gunakan: /+nutri <angka>")

# Kurang angka
@bot.message_handler(commands=['-pac'])
def kurang(message):
    user_id = message.from_user.id
    if not is_admin(user_id):
       bot.reply_to(message, "Akses tidak diijinkan")
       return

    try:
        angka = int(message.text.split()[1])
        user_id = message.from_user.id
        current = read_pac(user_id)
        new_value = current - angka
        write_pac(user_id, new_value)
        bot.reply_to(message, f"Dikurangi {angka}. Total: {new_value}")
    except:
        bot.reply_to(message, "Format salah. Gunakan: /-nutri <angka>")

# Set poin======= anion
@bot.message_handler(commands=['setani'])
def input_angka(message):
    user_id = message.from_user.id
    if not is_admin(user_id):
       bot.reply_to(message, "Akses tidak diijinkan")
       return


    try:
        angka = int(message.text.split()[1])
        user_id = message.from_user.id
        write_polimerani(user_id, angka)
        bot.reply_to(message, f"Nilai di-set ke: {angka}")
    except:
        bot.reply_to(message, "Format salah. Gunakan: /setnutri <angka>")

# Tambah angka
@bot.message_handler(commands=['+ani'])
def tambah(message):
    user_id = message.from_user.id
    if not is_admin(user_id):
       bot.reply_to(message, "Akses tidak diijinkan")
       return

    try:
        angka = int(message.text.split()[1])
        user_id = message.from_user.id
        current = read_polimerani(user_id)
        new_value = current + angka
        write_polimerani(user_id, new_value)
        bot.reply_to(message, f"Ditambah {angka}. Total: {new_value}")
    except:
        bot.reply_to(message, "Format salah. Gunakan: /+nutri <angka>")

# Kurang angka
@bot.message_handler(commands=['-ani'])
def kurang(message):
    user_id = message.from_user.id
    if not is_admin(user_id):
       bot.reply_to(message, "Akses tidak diijinkan")
       return

    try:
        angka = int(message.text.split()[1])
        user_id = message.from_user.id
        current = read_nutrisi(user_id)
        new_value = current - angka
        write_polimerani(user_id, new_value)
        bot.reply_to(message, f"Dikurangi {angka}. Total: {new_value}")
    except:
        bot.reply_to(message, "Format salah. Gunakan: /-nutri <angka>")

# Set poin======== cation
@bot.message_handler(commands=['setcat'])
def input_angka(message):
    user_id = message.from_user.id
    if not is_admin(user_id):
       bot.reply_to(message, "Akses tidak diijinkan")
       return


    try:
        angka = int(message.text.split()[1])
        user_id = message.from_user.id
        write_polimerCAT(user_id, angka)
        bot.reply_to(message, f"Nilai di-set ke: {angka}")
    except:
        bot.reply_to(message, "Format salah. Gunakan: /setnutri <angka>")

# Tambah angka
@bot.message_handler(commands=['+cat'])
def tambah(message):
    user_id = message.from_user.id
    if not is_admin(user_id):
       bot.reply_to(message, "Akses tidak diijinkan")
       return

    try:
        angka = int(message.text.split()[1])
        user_id = message.from_user.id
        current = read_polimerCAT(user_id)
        new_value = current + angka
        write_polimerCAT(user_id, new_value)
        bot.reply_to(message, f"Ditambah {angka}. Total: {new_value}")
    except:
        bot.reply_to(message, "Format salah. Gunakan: /+nutri <angka>")

# Kurang angka
@bot.message_handler(commands=['-cat'])
def kurang(message):
    user_id = message.from_user.id
    if not is_admin(user_id):
       bot.reply_to(message, "Akses tidak diijinkan")
       return

    try:
        angka = int(message.text.split()[1])
        user_id = message.from_user.id
        current = read_polimerCAT(user_id)
        new_value = current - angka
        write_polimerCAT(user_id, new_value)
        bot.reply_to(message, f"Dikurangi {angka}. Total: {new_value}")
    except:
        bot.reply_to(message, "Format salah. Gunakan: /-nutri <angka>")

# Set poin======= chlorine
@bot.message_handler(commands=['setclr'])
def input_angka(message):
    user_id = message.from_user.id
    if not is_admin(user_id):
       bot.reply_to(message, "Akses tidak diijinkan")
       return


    try:
        angka = int(message.text.split()[1])
        user_id = message.from_user.id
        write_chlorine(user_id, angka)
        bot.reply_to(message, f"Nilai di-set ke: {angka}")
    except:
        bot.reply_to(message, "Format salah. Gunakan: /setnutri <angka>")

# Tambah angka
@bot.message_handler(commands=['+clr'])
def tambah(message):
    user_id = message.from_user.id
    if not is_admin(user_id):
       bot.reply_to(message, "Akses tidak diijinkan")
       return

    try:
        angka = int(message.text.split()[1])
        user_id = message.from_user.id
        current = read_chlorine(user_id)
        new_value = current + angka
        write_chlorine(user_id, new_value)
        bot.reply_to(message, f"Ditambah {angka}. Total: {new_value}")
    except:
        bot.reply_to(message, "Format salah. Gunakan: /+nutri <angka>")

# Kurang angka
@bot.message_handler(commands=['-clr'])
def kurang(message):
    user_id = message.from_user.id
    if not is_admin(user_id):
       bot.reply_to(message, "Akses tidak diijinkan")
       return

    try:
        angka = int(message.text.split()[1])
        user_id = message.from_user.id
        current = read_chlorine(user_id)
        new_value = current - angka
        write_chlorine(user_id, new_value)
        bot.reply_to(message, f"Dikurangi {angka}. Total: {new_value}")
    except:
        bot.reply_to(message, "Format salah. Gunakan: /-nutri <angka>")

# Set poin======== cod lr
@bot.message_handler(commands=['setlr'])
def input_angka(message):
    user_id = message.from_user.id
    if not is_admin(user_id):
       bot.reply_to(message, "Akses tidak diijinkan")
       return


    try:
        angka = int(message.text.split()[1])
        user_id = message.from_user.id
        write_codLR(user_id, angka)
        bot.reply_to(message, f"Nilai di-set ke: {angka}")
    except:
        bot.reply_to(message, "Format salah. Gunakan: /setnutri <angka>")

# Tambah angka
@bot.message_handler(commands=['+lr'])
def tambah(message):
    user_id = message.from_user.id
    if not is_admin(user_id):
       bot.reply_to(message, "Akses tidak diijinkan")
       return

    try:
        angka = int(message.text.split()[1])
        user_id = message.from_user.id
        current = read_codLR(user_id)
        new_value = current + angka
        write_codLR(user_id, new_value)
        bot.reply_to(message, f"Ditambah {angka}. Total: {new_value}")
    except:
        bot.reply_to(message, "Format salah. Gunakan: /+nutri <angka>")

# Kurang angka
@bot.message_handler(commands=['-lr'])
def kurang(message):
    user_id = message.from_user.id
    if not is_admin(user_id):
       bot.reply_to(message, "Akses tidak diijinkan")
       return

    try:
        angka = int(message.text.split()[1])
        user_id = message.from_user.id
        current = read_codLR(user_id)
        new_value = current - angka
        write_codLR(user_id, new_value)
        bot.reply_to(message, f"Dikurangi {angka}. Total: {new_value}")
    except:
        bot.reply_to(message, "Format salah. Gunakan: /-nutri <angka>")

# Set poin======= cod hr
@bot.message_handler(commands=['sethr'])
def input_angka(message):
    user_id = message.from_user.id
    if not is_admin(user_id):
       bot.reply_to(message, "Akses tidak diijinkan")
       return


    try:
        angka = int(message.text.split()[1])
        user_id = message.from_user.id
        write_codHR(user_id, angka)
        bot.reply_to(message, f"Nilai di-set ke: {angka}")
    except:
        bot.reply_to(message, "Format salah. Gunakan: /setnutri <angka>")

# Tambah angka
@bot.message_handler(commands=['+hr'])
def tambah(message):
    user_id = message.from_user.id
    if not is_admin(user_id):
       bot.reply_to(message, "Akses tidak diijinkan")
       return

    try:
        angka = int(message.text.split()[1])
        user_id = message.from_user.id
        current = read_codHR(user_id)
        new_value = current + angka
        write_codHR(user_id, new_value)
        bot.reply_to(message, f"Ditambah {angka}. Total: {new_value}")
    except:
        bot.reply_to(message, "Format salah. Gunakan: /+nutri <angka>")

# Kurang angka
@bot.message_handler(commands=['-hr'])
def kurang(message):
    user_id = message.from_user.id
    if not is_admin(user_id):
       bot.reply_to(message, "Akses tidak diijinkan")
       return

    try:
        angka = int(message.text.split()[1])
        user_id = message.from_user.id
        current = read_codHR(user_id)
        new_value = current - angka
        write_codHR(user_id, new_value)
        bot.reply_to(message, f"Dikurangi {angka}. Total: {new_value}")
    except:
        bot.reply_to(message, "Format salah. Gunakan: /-nutri <angka>")

# Set poin====== Naoh
@bot.message_handler(commands=['setnaoh'])
def input_angka(message):
    user_id = message.from_user.id
    if not is_admin(user_id):
       bot.reply_to(message, "Akses tidak diijinkan")
       return


    try:
        angka = int(message.text.split()[1])
        user_id = message.from_user.id
        write_naoh(user_id, angka)
        bot.reply_to(message, f"Nilai di-set ke: {angka}")
    except:
        bot.reply_to(message, "Format salah. Gunakan: /setnutri <angka>")

# Tambah angka
@bot.message_handler(commands=['+naoh'])
def tambah(message):
    user_id = message.from_user.id
    if not is_admin(user_id):
       bot.reply_to(message, "Akses tidak diijinkan")
       return

    try:
        angka = int(message.text.split()[1])
        user_id = message.from_user.id
        current = read_naoh(user_id)
        new_value = current + angka
        write_naoh(user_id, new_value)
        bot.reply_to(message, f"Ditambah {angka}. Total: {new_value}")
    except:
        bot.reply_to(message, "Format salah. Gunakan: /+nutri <angka>")

# Kurang angka
@bot.message_handler(commands=['-naoh'])
def kurang(message):
    user_id = message.from_user.id
    if not is_admin(user_id):
       bot.reply_to(message, "Akses tidak diijinkan")
       return

    try:
        angka = int(message.text.split()[1])
        user_id = message.from_user.id
        current = read_naoh(user_id)
        new_value = current - angka
        write_naoh(user_id, new_value)
        bot.reply_to(message, f"Dikurangi {angka}. Total: {new_value}")
    except:
        bot.reply_to(message, "Format salah. Gunakan: /-nutri <angka>")

# Set poin====== karung
@bot.message_handler(commands=['setsak'])
def input_angka(message):
    user_id = message.from_user.id
    if not is_admin(user_id):
       bot.reply_to(message, "Akses tidak diijinkan")
       return


    try:
        angka = int(message.text.split()[1])
        user_id = message.from_user.id
        write_karung(user_id, angka)
        bot.reply_to(message, f"Nilai di-set ke: {angka}")
    except:
        bot.reply_to(message, "Format salah. Gunakan: /setnutri <angka>")

# Tambah angka
@bot.message_handler(commands=['+sak'])
def tambah(message):
    user_id = message.from_user.id
    if not is_admin(user_id):
       bot.reply_to(message, "Akses tidak diijinkan")
       return

    try:
        angka = int(message.text.split()[1])
        user_id = message.from_user.id
        current = read_karung(user_id)
        new_value = current + angka
        write_karung(user_id, new_value)
        bot.reply_to(message, f"Ditambah {angka}. Total: {new_value}")
    except:
        bot.reply_to(message, "Format salah. Gunakan: /+nutri <angka>")

# Kurang angka
@bot.message_handler(commands=['-sak'])
def kurang(message):
    user_id = message.from_user.id
    if not is_admin(user_id):
       bot.reply_to(message, "Akses tidak diijinkan")
       return

    try:
        angka = int(message.text.split()[1])
        user_id = message.from_user.id
        current = read_karung(user_id)
        new_value = current - angka
        write_karung(user_id, new_value)
        bot.reply_to(message, f"Dikurangi {angka}. Total: {new_value}")
    except:
        bot.reply_to(message, "Format salah. Gunakan: /-nutri <angka>")

# Set poin======== bakteri
@bot.message_handler(commands=['setbtr'])
def input_angka(message):
    user_id = message.from_user.id
    if not is_admin(user_id):
       bot.reply_to(message, "Akses tidak diijinkan")
       return


    try:
        angka = float(message.text.split()[1])
        user_id = message.from_user.id
        write_bakteri(user_id, angka)
        bot.reply_to(message, f"Nilai di-set ke: {angka}")
    except:
        bot.reply_to(message, "Format salah. Gunakan: /setnutri <angka>")

# Tambah angka
@bot.message_handler(commands=['+btr'])
def tambah(message):
    user_id = message.from_user.id
    if not is_admin(user_id):
       bot.reply_to(message, "Akses tidak diijinkan")
       return

    try:
        angka = float(message.text.split()[1])
        user_id = message.from_user.id
        current = read_bakteri(user_id)
        new_value = current + angka
        write_bakteri(user_id, new_value)
        bot.reply_to(message, f"Ditambah {angka}. Total: {new_value}")
    except:
        bot.reply_to(message, "Format salah. Gunakan: /+nutri <angka>")

# Kurang angka
@bot.message_handler(commands=['-btr'])
def kurang(message):
    user_id = message.from_user.id
    if not is_admin(user_id):
       bot.reply_to(message, "Akses tidak diijinkan")
       return

    try:
        angka = float(message.text.split()[1])
        user_id = message.from_user.id
        current = read_bakteri(user_id)
        new_value = current - angka
        write_bakteri(user_id, new_value)
        bot.reply_to(message, f"Dikurangi {angka}. Total: {new_value}")
    except:
        bot.reply_to(message, "Format salah. Gunakan: /-nutri <angka>")


@bot.callback_query_handler(func=lambda call: call.data == "cb9")
def tombolWI(call):
    bot.answer_callback_query(call.id)
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(waktu)
    print("cek stok")
    
    markup = types.InlineKeyboardMarkup()
    user_id = call.message.from_user.id
    sisa1 = read_nutrisi(user_id)
    sisa2 = read_pac(user_id)
    sisa3 = read_polimerani(user_id)
    sisa4 = read_polimerCAT(user_id)
    sisa5 = read_chlorine(user_id)
    sisa6 = read_codLR(user_id)
    sisa7 = read_codHR(user_id)
    sisa8 = read_naoh(user_id)
    sisa9 = read_karung(user_id)
    sisa10 = read_bakteri(user_id)
    print(sisa10)
    #nutrisi
    if sisa1 <= 3:
        status = "🔴"
    elif sisa1 < 5:
        status = "🟡"
    else:
        status = "🟢"

    #pac
    if sisa2 <= 1:
        status2 = "🔴"
    elif sisa2 < 5:
        status2 = "🟡"
    else:
        status2 = "🟢"

    #polimer anion
    if sisa3 < 1:
        status3 = "🔴"
    elif sisa3 <= 1:
        status3 = "🟡"
    else:
        status3 = "🟢"
    
    #polimer cation
    if sisa4 < 1:
        status4 = "🔴"
    elif sisa4 <= 1:
        status4 = "🟡"
    else:
        status4 = "🟢"
    
    #chlorine
    if sisa5 < 1:
        status5 = "🔴"
    elif sisa5 <= 1:
        status5 = "🟡"
    else:
        status5 = "🟢"
    
    #cod lr
    if sisa6 <= 3:
        status6 = "🔴"
    elif sisa6 < 6:
        status6 = "🟡"
    else:
        status6 = "🟢"
    
    #cod hr
    if sisa7 <= 3:
        status7 = "🔴"
    elif sisa7 < 6:
        status7 = "🟡"
    else:
        status7 = "🟢"
    
    #naoh
    if sisa8 < 1:
        status8 = "🔴"
    elif sisa8 <= 1:
        status8 = "🟡"
    else:
        status8 = "🟢"
    
    #karung
    if sisa9 <= 1:
        status9 = "🔴"
    elif sisa9 < 5:
        status9 = "🟡"
    else:
        status9 = "🟢"
    
    #bakteri
    if sisa10 <= 1:
        status10 = "🔴"
    elif sisa10 < 5:
        status10 = "🟡"
    else:
        status10 = "🟢"
    

    kata = [f"ULTRA NUTRI BIO S      : {sisa1} jrg {status}\n"
            f"WTC-01                      : {sisa2} jrg {status2}\n"
            f"POLIMER ANION          : {sisa3} karung {status3}\n"
            f"POLIMER CATION         : {sisa4} karung {status4}\n"
            f"CHLORINE                   : {sisa5} jrg {status5}\n"
            f"REAGENT COD LR         : {sisa6} vial {status6}\n"
            f"REAGENT COD HR         : {sisa7} vial {status7}\n"
            f"CAUSTIC SODA           : {sisa8} karung {status8}\n"
            f"KARUNG                   : {sisa9} pcs {status9}\n"
            f"BAKTERI POWDER         : {sisa10} kg {status10}\n"
            
            ]

    
    markup.add(types.InlineKeyboardButton("Kembali ↩️", callback_data="wi13"))
    bot.send_message(call.message.chat.id, kata, reply_markup=markup )
    bot.delete_message(call.message.chat.id, call.message.message_id)

@bot.message_handler(commands=['edit'])
def edit(message):
    user_id = message.from_user.id
    print(user_id)
    if not is_admin(user_id):
       bot.reply_to(message, "Akses tidak diijinkan")
       return
    
    kata = [

        f"/stok utk format semua\n"
        f'\nNUTRISI\n'
        f"/setnutri set nilai\n"
        f'/+nutri tambah\n'
        f'/-nutri kurang\n'
        f'/resetnutri reset\n'
        f'\nPAC\n'
        f"/setpac set nilai\n"
        f'/+pac tambah\n'
        f'/-pac kurang\n'
        f'/resetpac reset\n'
        f'\nPOLIMER ANION\n'
        f"/setani set nilai\n"
        f'/+ani tambah\n'
        f'/-ani kurang\n'
        f'/resetani reset\n'
        f'\nPOLIMER CATION\n'
        f"/setcat set nilai\n"
        f'/+cat tambah\n'
        f'/-cat kurang\n'
        f'/resetcat reset\n'
        f'\nCHLORINE\n'
        f"/setclr set nilai\n"
        f'/+clr tambah\n'
        f'/-clr kurang\n'
        f'/resetclr reset\n'
        f'\nREAGEN COD LR\n'
        f"/setlr set nilai\n"
        f'/+lr tambah\n'
        f'/-lr kurang\n'
        f'/resetlr reset\n'
        f'\nREAGEN COD HR\n'
        f"/sethr set nilai\n"
        f'/+hr tambah\n'
        f'/-hr kurang\n'
        f'/resethr reset\n'
        f'\nNaOH\n'
        f"/setnaoh set nilai\n"
        f'/+naoh tambah\n'
        f'/-naoh kurang\n'
        f'/resetnaoh reset\n'
        f'\nKARUNG\n'
        f"/setsak set nilai\n"
        f'/+sak tambah\n'
        f'/-sak kurang\n'
        f'/resetsak reset\n'
        f'\nBAKTERI POWDER\n'
        f"/setbtr set nilai\n"
        f'/+btr tambah\n'
        f'/-btr kurang\n'
        f'/resetbtr reset\n'

    ]

    bot.send_message(message.chat.id, kata)

# Reset nilai
@bot.message_handler(commands=['resetnutri'])
def reset(message):
    user_id = message.from_user.id
    if not is_admin(user_id):
       bot.reply_to(message, "Akses tidak diijinkan")
       return

    write_nutrisi(user_id, 0)
    bot.reply_to(message, "Nilai telah di-reset ke 0.")

# Reset nilai pac
@bot.message_handler(commands=['resetpac'])
def reset(message):
    user_id = message.from_user.id
    if not is_admin(user_id):
       bot.reply_to(message, "Akses tidak diijinkan")
       return

    write_pac(user_id, 0)
    bot.reply_to(message, "Nilai telah di-reset ke 0.")

# Reset nilai anion
@bot.message_handler(commands=['resetani'])
def reset(message):
    user_id = message.from_user.id
    if not is_admin(user_id):
       bot.reply_to(message, "Akses tidak diijinkan")
       return

    write_polimerani(user_id, 0)
    bot.reply_to(message, "Nilai telah di-reset ke 0.")

# Reset nilai cation
@bot.message_handler(commands=['resetcat'])
def reset(message):
    user_id = message.from_user.id
    if not is_admin(user_id):
       bot.reply_to(message, "Akses tidak diijinkan")
       return

    write_polimerCAT(user_id, 0)
    bot.reply_to(message, "Nilai telah di-reset ke 0.")

# Reset nilai chlorine
@bot.message_handler(commands=['resetclr'])
def reset(message):
    user_id = message.from_user.id
    if not is_admin(user_id):
       bot.reply_to(message, "Akses tidak diijinkan")
       return

    write_chlorine(user_id, 0)
    bot.reply_to(message, "Nilai telah di-reset ke 0.")

# Reset nilai cod lr
@bot.message_handler(commands=['resetlr'])
def reset(message):
    user_id = message.from_user.id
    if not is_admin(user_id):
       bot.reply_to(message, "Akses tidak diijinkan")
       return

    write_codLR(user_id, 0)
    bot.reply_to(message, "Nilai telah di-reset ke 0.")

# Reset nilai cod hr
@bot.message_handler(commands=['resethr'])
def reset(message):
    user_id = message.from_user.id
    if not is_admin(user_id):
       bot.reply_to(message, "Akses tidak diijinkan")
       return

    write_codHR(user_id, 0)
    bot.reply_to(message, "Nilai telah di-reset ke 0.")

# Reset nilai Naoh
@bot.message_handler(commands=['resetnaoh'])
def reset(message):
    user_id = message.from_user.id
    if not is_admin(user_id):
       bot.reply_to(message, "Akses tidak diijinkan")
       return

    write_naoh(user_id, 0)
    bot.reply_to(message, "Nilai telah di-reset ke 0.")

# Reset nilai karung
@bot.message_handler(commands=['resetsak'])
def reset(message):
    user_id = message.from_user.id
    if not is_admin(user_id):
       bot.reply_to(message, "Akses tidak diijinkan")
       return

    write_karung(user_id, 0)
    bot.reply_to(message, "Nilai telah di-reset ke 0.")

# Reset nilai bakteri
@bot.message_handler(commands=['resetbtr'])
def reset(message):
    user_id = message.from_user.id
    if not is_admin(user_id):
       bot.reply_to(message, "Akses tidak diijinkan")
       return

    write_bakteri(user_id, 0)
    bot.reply_to(message, "Nilai telah di-reset ke 0.")


print("Bot berjalan.....")
bot.infinity_polling()

