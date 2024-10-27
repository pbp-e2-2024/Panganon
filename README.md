## **1. Nama-nama anggota kelompok**
- Brian Altan (2306152166)
- Muhammad Ruzbehan Baqli (2306245062)
- Gabriel Selwas Aboyaman Fenanlampir (2306315516)
- Rosanne Valerie (2306222986)
- Ilham Ghani Adrin Sapta (2306201792)

## **2. Deskripsi aplikasi (cerita aplikasi yang diajukan serta kebermanfaatannya)**
**Panganon** adalah aplikasi pencarian tempat makan di Medan yang membantu pengguna menemukan makanan favorit sesuai dengan selera dan kebutuhan mereka. Aplikasi ini menawarkan pencarian berdasarkan **kategori makanan**, **status halal**, **jam operasional** tempat makan tersebut, dan **jarak terdekat** melalui fitur GPS. Selain itu, pengguna bisa berbagi **ulasan**, **rekomendasi**, serta **memesan makanan** langsung dari restoran yang bekerja sama. Panganon mempermudah pengalaman kuliner warga Medan dan turis, membantu mereka menemukan tempat terbaik untuk menikmati makanan lokal dengan mudah dan cepat.

## **3. Daftar modul yang akan diimplementasikan**
### **Modul Utama**

- **Modul Daftar Toko**  
  Pengguna dapat mencari tempat makan berdasarkan kategori makanan, status halal, dan lokasi.

  *Dikerjakan oleh Ilham Ghani Adrin Sapta*

- **Modul Forum**  
  Fitur ini memungkinkan pengguna untuk berinteraksi dengan pengguna lain, berbagi rekomendasi tempat makan, atau berdiskusi tentang topik terkait kuliner.

  *Dikerjakan oleh Brian Altan*
- **Modul Favorites**  
  Pengguna dapat menandai tempat makan yang telah dikunjungi sebagai favorit. Modul ini juga memungkinkan pengguna memberikan *rating* dan ulasan untuk membantu orang lain memilih restoran terbaik.

  *Dikerjakan oleh Gabriel Selwas Aboyaman Fenanlampir* 

- **Modul About Me**  
  Pengguna dapat melakukan kostumisasi laman tentang dirinya untuk menampilkan informasi seperti preferensi makanan, pesan di forum yang ia kirim, hal-hal yang disukai, review makanan, dan lain-lainnya.

  *Dikerjakan oleh Rosanne Valerie*  
- **Modul Event**  
  Pengguna dapat membuat, melihat, memperbarui, dan menghapus acara kuliner. Fitur ini memungkinkan pengguna untuk membuat acara seperti festival makanan, melihat daftar acara yang akan datang, merevisi deskripsi acara, serta menghapus acara kuliner jika diperlukan.

  *Dikerjakan oleh Muhammad Ruzbehan Baqli*  

## **4. Sumber initial dataset kategori utama produk**
Untuk mengumpulkan *dataset*, kami menggunakan **Selenium** untuk melakukan proses *scraping* pada **Google Maps**. Selenium memungkinkan otomatisasi proses pengambilan data dengan mensimulasikan aktivitas pengguna sungguhan. Data yang kami peroleh mencakup **nama restoran**, **rating**, **jumlah rating**, **kisaran harga**, **alamat**, **jam buka**, **layanan** yang ditawarkan, *link* ke halaman toko pada Google Maps dan **letak koordinat** geografis toko.

## **5. Role atau peran pengguna beserta deskripsinya (karena bisa saja lebih dari satu jenis pengguna yang mengakses aplikasi)**
### **Admin**
- Mengelola data tempat makan yang terdaftar.
- Mengelola akun pengguna.
- Mengelola diskusi di forum dan ulasan pengguna.  
- Mengelola event yang terdaftar.

### **User**
- Mencari tempat makan berdasarkan kategori, status halal, atau lokasi.
- Menambahkan tempat makan ke daftar favorit.
- Membuat profil about me.
- Membuat atau mengikuti diskusi di forum.
- Membuat berita festival makan di event.

## **6. Tautan deployment aplikasi**
[Panganon](http://brian-altan-panganon.pbp.cs.ui.ac.id/)