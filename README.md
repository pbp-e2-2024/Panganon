## **1. Nama-nama anggota kelompok**
- Brian Altan (2306152166)
- Muhammad Ruzbehan Baqli (2306245062)
- Gabriel Selwas Aboyaman Fenanlampir (2306315516)
- Rosanne Valerie (2306222986)
- Ilham Ghani Adrin Sapta (2306201792)

## **2. Deskripsi aplikasi (cerita aplikasi yang diajukan serta kebermanfaatannya)**
**Panganon** adalah aplikasi pencarian tempat makan di Medan yang membantu pengguna menemukan makanan favorit sesuai dengan selera dan kebutuhan mereka. Aplikasi ini menawarkan pencarian berdasarkan **kategori makanan**, **status halal**, **jam operasional** tempat makan tersebut, dan **jarak terdekat** melalui fitur GPS. Selain itu, pengguna bisa berbagi **ulasan**, **rekomendasi**, serta **memesan makanan** langsung dari restoran yang bekerja sama. Panganon mempermudah pengalaman kuliner warga Medan dan turis, membantu mereka menemukan tempat terbaik untuk menikmati makanan lokal dengan mudah dan cepat.

## **3. Daftar modul yang akan diimplementasikan**
### **Modul Wajib**
- **Main (Home Page)**  
Halaman utama aplikasi yang menjadi titik awal bagi pengguna.
- **Modul Authentication**  
Pengguna harus mendaftar atau masuk terlebih dahulu sebelum dapat menggunakan fitur-fitur aplikasi lainnya.

### **Modul Utama**
- **Modul Daftar Makanan**  
Pengguna dapat mencari tempat makan berdasarkan kategori makanan, status halal, dan lokasi terdekat menggunakan GPS.
- **Modul Forum**  
Fitur ini memungkinkan pengguna untuk berinteraksi dengan pengguna lain, berbagi rekomendasi tempat makan, atau berdiskusi tentang topik terkait kuliner.
- **Modul Favorites**  
Pengguna dapat menandai tempat makan yang telah dikunjungi sebagai favorit. Modul ini juga memungkinkan pengguna memberikan *rating* dan ulasan untuk membantu orang lain memilih restoran terbaik.
- **Modul Pemesanan Makanan**  
Pengguna dapat memesan makanan langsung melalui aplikasi untuk restoran yang telah bekerja sama dengan platform ini.
- **Modul User Toko**  
Pengguna dapat mendaftarkan toko mereka sebagai akun penjual dapat menambah makanan pada tokonya.

## **4. Sumber initial dataset kategori utama produk**
Untuk mengumpulkan *dataset*, kami menggunakan **Selenium** untuk melakukan proses *scraping* pada **Google Maps**. Selenium memungkinkan otomatisasi proses pengambilan data dengan mensimulasikan aktivitas pengguna sungguhan. Data yang kami peroleh mencakup **nama restoran**, **rating**, **jumlah rating**, **kisaran harga**, **alamat**, **jam buka**, **layanan** yang ditawarkan, *link* ke halaman toko pada Google Maps dan **letak koordinat** geografis toko.

## **5. Role atau peran pengguna beserta deskripsinya (karena bisa saja lebih dari satu jenis pengguna yang mengakses aplikasi)**
### **Admin**
- Mengelola dan memverifikasi data tempat makan yang terdaftar.
- Mengelola *role* pengguna (memblokir pengguna yang melanggar kebijakan, menambahkan *role* toko).
- Mengelola diskusi di forum dan ulasan pengguna.  

### **User-Customer**
- Mencari tempat makan berdasarkan kategori, status halal, atau lokasi terdekat.
- Menambahkan tempat makan ke daftar favorit.
- Memberikan ulasan dan *rating* untuk tempat makan.
- Mengikuti diskusi di forum.
- Melakukan pemesanan makanan secara daring (untuk restoran yang mendukung).

### **User-Toko**
- Mengelola profil restoran mereka (jam buka, menu, layanan yang ditawarkan, dll).
- Mengelola pesanan yang masuk melalui aplikasi.
- Melihat ulasan dan *rating* yang diberikan oleh pengguna.

## **6. Tautan deployment aplikasi**
[Panganon](http://brian-altan-panganon.pbp.cs.ui.ac.id/)