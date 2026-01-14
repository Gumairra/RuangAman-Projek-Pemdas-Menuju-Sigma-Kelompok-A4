🏠 RuangAman
Sistem Monitoring Suhu dan Asap Ruangan Berbasis Raspberry Pi

📌 Deskripsi Proyek
RuangAman adalah sistem monitoring suhu dan asap ruangan yang dirancang untuk menjaga keamanan dan kenyamanan ruangan secara otomatis. Sistem ini memanfaatkan sensor suhu dan sensor asap untuk mendeteksi kondisi lingkungan, kemudian memberikan respon berupa indikator visual, pendinginan ruangan, dan alarm peringatan apabila terdeteksi kondisi berbahaya. Sistem ini dikembangkan menggunakan Raspberry Pi sebagai pusat pengendali dan bahasa pemrograman Python sebagai pengolah data sensor.

🎯 Tujuan
- Memantau suhu ruangan secara real-time
- Mendeteksi keberadaan asap di dalam ruangan
- Memberikan peringatan dini terhadap kondisi berbahaya
- Mengotomatiskan respon sistem tanpa intervensi pengguna

🏗️ Arsitektur Sistem
Sistem RuangAman dibagi ke dalam empat zona utama:
- Zona Client: Menampilkan informasi kondisi ruangan kepada pengguna
- Zona Backend: Mengatur alur data dan komunikasi sistem
- Zona Engine: Melakukan pembacaan sensor dan pengambilan keputusan
Alur sistem berjalan dari zona client ke zona backend, kemudian ke zona engine untuk pemrosesan data, hasilnya dikembalikan ke zona client berbentuk informasi.

🔧 Hardware yang Digunakan
-  Raspberry Pi 4
- Sensor DHT22 (suhu dan kelembaban)
- Sensor MQ-2 (asap/gas)
- MCP3002 (ADC)
- LED Hijau, Kuning, dan Merah
- Kipas 5V
- Buzzer
- Resistor, kabel jumper, dan breadboard
- Power supply 5V

💻 Software yang Digunakan
- Python 3
- RPi.GPIO
- Adafruit_DHT
- spidev
- Sistem Operasi Raspberry Pi OS

⚙️ Logika Sistem
Sistem menentukan kondisi ruangan berdasarkan suhu dan asap sebagai berikut:
- Suhu ≤ 30°C dan tidak ada asap → kondisi aman
- Suhu ≤ 30°C dan ada asap → kondisi peringatan
- nSuhu > 30°C dan tidak ada asap → kondisi peringatan
- Suhu > 30°C dan ada asap → kondisi bahaya
Setiap kondisi akan memicu respon sistem yang berbeda berupa LED, kipas, dan buzzer.

👤 Pengembang (A4 - Menuju Sigma)
- Reza Maulana Yazi (152024012)
- Fadhlan Baihaki A 152024021)
- Fakhri Nazhirul Hakim (152024039)
- R. Gumairra Ramnoya A (152024045)
- Nur Hikma Missgyarti (152024098)
- Joddy Lukmanul Hakim (152024117)
Program Studi: Informasi
Mata Kuliah: Praktikum Pemrograman Dasar
