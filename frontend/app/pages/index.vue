<template>
  <div class="min-h-screen bg-slate-50 text-slate-800 antialiased selection:bg-emerald-500 selection:text-white">
    <nav class="bg-white/80 backdrop-blur-md border-b border-slate-100 sticky top-0 z-50 transition-all duration-300">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <div class="flex items-center gap-3 group cursor-pointer">
            <img src="/ikon.jpg" alt="Logo" class="w-10 h-10 object-contain group-hover:animate-spin-slow transition duration-500" />
            <div class="flex flex-col">
              <span class="text-xl font-black text-slate-900 tracking-tight leading-none">Pharma<span class="text-emerald-600">Prophet</span></span>
              <span class="text-[10px] text-slate-400 font-medium tracking-wider mt-0.5">Predictive Intelligence</span>
            </div>
          </div>
          
          <div class="hidden md:flex gap-8 items-center">
            <a href="#features" class="text-sm font-semibold text-slate-600 hover:text-emerald-600 transition">Fitur Utama</a>
            <a href="#about" class="text-sm font-semibold text-slate-600 hover:text-emerald-600 transition">Keunggulan</a>
            <a href="#contact" class="text-sm font-semibold text-slate-600 hover:text-emerald-600 transition">Kontak</a>
          </div>
          
          <div class="flex items-center gap-3">
            <NuxtLink to="/login" class="px-4 py-2 text-sm font-semibold text-slate-700 hover:text-emerald-600 transition">
              Masuk
            </NuxtLink>
            <NuxtLink to="/register" class="px-4 py-2 text-sm font-semibold bg-slate-900 text-white rounded-xl hover:bg-slate-800 transition shadow-sm">
              Daftar
            </NuxtLink>
          </div>
        </div>
      </div>
    </nav>

    <section class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 lg:py-28 relative overflow-hidden">
      <div class="absolute top-0 right-0 -z-10 w-96 h-96 bg-emerald-100 rounded-full filter blur-3xl opacity-50 transform translate-x-1/3 -translate-y-1/3"></div>
      
      <div class="grid lg:grid-cols-12 gap-12 items-center">
        <div class="space-y-6 lg:col-span-7 text-center lg:text-left animate-fade-in">
          <h1 class="text-4xl sm:text-5xl lg:text-4xl font-bold text-slate-950 tracking-tight leading-[1.1]">
            Prediksi Stok Farmasi Jauh Lebih Akurat Dengan Kecerdasan Buatan
          </h1>
          <p class="text-lg text-slate-600 max-w-2xl mx-auto lg:mx-0 font-normal leading-relaxed">
            Kendalikan inventaris apotek Anda secara cerdas. Cegah *stockout*, hindari obat kedaluwarsa, dan optimalkan pengadaan barang secara otomatis berbasis data historis.
          </p>
          <div class="flex flex-col sm:flex-row gap-4 pt-4 justify-center lg:justify-start">
            <NuxtLink to="/register" class="px-8 py-3.5 bg-gradient-to-r from-emerald-500 to-teal-600 text-white rounded-xl font-semibold hover:shadow-lg hover:shadow-emerald-200 transition tracking-wide text-center">
              Mulai Uji Coba Gratis
            </NuxtLink>
            <button class="px-8 py-3.5 bg-white border border-slate-200 text-slate-700 rounded-xl font-semibold hover:bg-slate-50 transition text-center shadow-sm">
              Lihat Demo Sistem
            </button>
          </div>
        </div>

        <!-- <div class="lg:col-span-5 animate-slide-up">
          <div class="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-2xl relative">
            <div class="flex items-center justify-between border-b border-slate-800 pb-4 mb-6">
              <div class="flex items-center gap-2">
                <span class="w-3 h-3 rounded-full bg-rose-500"></span>
                <span class="w-3 h-3 rounded-full bg-amber-500"></span>
                <span class="w-3 h-3 rounded-full bg-emerald-500"></span>
              </div>
              <span class="text-xs font-mono text-slate-500 tracking-wider">PHARMACAST_PROPHET_V1</span>
            </div>
            
            <div class="space-y-4">
              <div class="p-4 bg-slate-800/50 border border-slate-800 rounded-xl flex justify-between items-center">
                <div>
                  <p class="text-xs text-slate-400 font-semibold uppercase tracking-wider">Akurasi Prediksi Model</p>
                  <p class="text-2xl font-black text-emerald-400 mt-1">94.82%</p>
                </div>
                <div class="text-3xl">🎯</div>
              </div>
              
              <div class="p-4 bg-slate-800/50 border border-slate-800 rounded-xl">
                <p class="text-xs text-slate-400 font-semibold uppercase tracking-wider mb-3">Tren Permintaan Paracetamol (7 Hari ke Depan)</p>
                <div class="h-24 flex items-end gap-2 pt-2">
                  <div class="w-full bg-slate-700 rounded-t h-[40%]"></div>
                  <div class="w-full bg-slate-700 rounded-t h-[55%]"></div>
                  <div class="w-full bg-slate-700 rounded-t h-[45%]"></div>
                  <div class="w-full bg-slate-700 rounded-t h-[70%]"></div>
                  <div class="w-full bg-emerald-500/80 rounded-t h-[85%] animate-pulse"></div>
                  <div class="w-full bg-emerald-500 rounded-t h-[90%] animate-pulse"></div>
                  <div class="w-full bg-emerald-400 rounded-t h-[95%] animate-pulse"></div>
                </div>
              </div>
            </div>
          </div>
        </div> -->
        <img src="/image.png" alt="Preview Dashboard" class="lg:col-span-5 animate-slide-up rounded-2xl shadow-xl shadow-slate-200 border border-slate-100 h-80 w-120" />
      </div>
    </section>

    <section id="features" class="bg-white border-y border-slate-100 py-24">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center max-w-3xl mx-auto mb-20">
          <h2 class="text-3xl sm:text-4xl font-bold text-slate-950 tracking-tight mb-4">Fitur Utama Platform</h2>
          <p class="text-slate-600 font-normal">Dirancang khusus untuk kebutuhan manajemen operasional apotek modern dan efisien.</p>
        </div>
        
        <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          <div class="border border-slate-100 bg-slate-50/50 p-8 rounded-2xl hover:bg-white hover:shadow-xl hover:shadow-slate-100 hover:border-emerald-500/20 transition-all duration-300 group">
            <h3 class="text-lg font-bold text-slate-900 mb-2">Peramalan Time-Series AI</h3>
            <p class="text-sm text-slate-600 leading-relaxed font-normal">
              Menggunakan library Prophet untuk mempelajari tren penjualan masa lalu guna memproyeksikan kebutuhan stok di masa depan secara berkala.
            </p>
          </div>

          <div class="border border-slate-100 bg-slate-50/50 p-8 rounded-2xl hover:bg-white hover:shadow-xl hover:shadow-slate-100 hover:border-emerald-500/20 transition-all duration-300 group">
            <div class="w-12 h-12 bg-emerald-100 text-emerald-700 rounded-xl flex items-center justify-center text-xl font-bold mb-6 group-hover:bg-emerald-500 group-hover:text-white transition duration-300">📦</div>
            <h3 class="text-lg font-bold text-slate-900 mb-2">Manajemen Inventori Cerdas</h3>
            <p class="text-sm text-slate-600 leading-relaxed font-normal">
              Pantau kuantitas obat secara *real-time*, dapatkan sistem peringatan dini ketika stok menyentuh batas minimum aman (*safetystock*).
            </p>
          </div>

          <div class="border border-slate-100 bg-slate-50/50 p-8 rounded-2xl hover:bg-white hover:shadow-xl hover:shadow-slate-100 hover:border-emerald-500/20 transition-all duration-300 group">
            <div class="w-12 h-12 bg-emerald-100 text-emerald-700 rounded-xl flex items-center justify-center text-xl font-bold mb-6 group-hover:bg-emerald-500 group-hover:text-white transition duration-300">💰</div>
            <h3 class="text-lg font-bold text-slate-900 mb-2">Optimasi Finansial Bisnis</h3>
            <p class="text-sm text-slate-600 leading-relaxed font-normal">
              Alokasikan modal belanja obat secara efisien. Hindari penumpukan dana mati akibat pembelian obat yang kurang laku di pasaran.
            </p>
          </div>

          <div class="border border-slate-100 bg-slate-50/50 p-8 rounded-2xl hover:bg-white hover:shadow-xl hover:shadow-slate-100 hover:border-emerald-500/20 transition-all duration-300 group">
            <div class="w-12 h-12 bg-emerald-100 text-emerald-700 rounded-xl flex items-center justify-center text-xl font-bold mb-6 group-hover:bg-emerald-500 group-hover:text-white transition duration-300">📈</div>
            <h3 class="text-lg font-bold text-slate-900 mb-2">Analisis Visual Komprehensif</h3>
            <p class="text-sm text-slate-600 leading-relaxed font-normal">
              Sajikan laporan transaksi penjualan, margin keuntungan, dan performa pergerakan obat melalui grafik interaktif yang mudah dipahami.
            </p>
          </div>

          <div class="border border-slate-100 bg-slate-50/50 p-8 rounded-2xl hover:bg-white hover:shadow-xl hover:shadow-slate-100 hover:border-emerald-500/20 transition-all duration-300 group">
            <div class="w-12 h-12 bg-emerald-100 text-emerald-700 rounded-xl flex items-center justify-center text-xl font-bold mb-6 group-hover:bg-emerald-500 group-hover:text-white transition duration-300">🔐</div>
            <h3 class="text-lg font-bold text-slate-900 mb-2">Keamanan & Otorisasi Ketat</h3>
            <p class="text-sm text-slate-600 leading-relaxed font-normal">
              Proteksi data medis privat apotek Anda menggunakan autentikasi JWT token yang aman dengan pembagian role akses pengguna yang terstruktur.
            </p>
          </div>

          <div class="border border-slate-100 bg-slate-50/50 p-8 rounded-2xl hover:bg-white hover:shadow-xl hover:shadow-slate-100 hover:border-emerald-500/20 transition-all duration-300 group">
            <div class="w-12 h-12 bg-emerald-100 text-emerald-700 rounded-xl flex items-center justify-center text-xl font-bold mb-6 group-hover:bg-emerald-500 group-hover:text-white transition duration-300">⚡</div>
            <h3 class="text-lg font-bold text-slate-900 mb-2">Responsif & Performa Kilat</h3>
            <p class="text-sm text-slate-600 leading-relaxed font-normal">
              Dibangun di atas arsitektur FastAPI (Python) dan Nuxt 3 (Vue) yang super ringan untuk pengalaman manajemen tanpa hambatan.
            </p>
          </div>
        </div>
      </div>
    </section>

    <section id="about" class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
      <div class="grid lg:grid-cols-2 gap-12 items-center">
        <div class="space-y-6">
          <h2 class="text-3xl sm:text-4xl font-bold text-slate-950 tracking-tight">Mengapa Memilih Solusi Kami?</h2>
          <p class="text-slate-600 font-normal leading-relaxed">
            Kami menjembatani kompleksitas analisis data sains kecerdasan buatan menjadi sebuah sistem antarmuka yang siap pakai oleh staf operasional klinis atau apotek terkini.
          </p>
          <div class="space-y-4 pt-2">
            <div class="flex gap-4 items-start">
              <div class="w-6 h-6 rounded-full bg-emerald-100 flex items-center justify-center text-emerald-600 shrink-0 font-bold text-sm">✓</div>
              <div>
                <h4 class="font-bold text-slate-900 text-base">Akurasi Terkalibrasi</h4>
                <p class="text-sm text-slate-600 font-normal">Algoritma secara konstan mengevaluasi galat eror untuk menghasilkan rekomendasi paling presisi.</p>
              </div>
            </div>
            <div class="flex gap-4 items-start">
              <div class="w-6 h-6 rounded-full bg-emerald-100 flex items-center justify-center text-emerald-600 shrink-0 font-bold text-sm">✓</div>
              <div>
                <h4 class="font-bold text-slate-900 text-base">Alur Kerja Ramah Pengguna</h4>
                <p class="text-sm text-slate-600 font-normal">Desain antarmuka minimalis terfokus, memangkas kurva belajar staf administrasi apotek.</p>
              </div>
            </div>
          </div>
        </div>
        
        <div class="bg-gradient-to-br from-emerald-500 to-teal-700 rounded-3xl p-10 text-white min-h-[350px] flex items-center relative shadow-xl shadow-emerald-100">
          <div class="space-y-4 max-w-md">
            <span class="text-4xl">💡</span>
            <h3 class="text-2xl font-bold tracking-tight">Efisiensi Rantai Pasok Farmasi Dimulai dari Sini</h3>
            <p class="text-emerald-100 text-sm leading-relaxed font-medium opacity-90">
              Hindari kerugian finansial akibat obat kedaluwarsa yang tidak terjual serta amankan ketersediaan obat-obatan kritis bagi pasien di saat yang krusial.
            </p>
          </div>
        </div>
      </div>
    </section>

    <section id="contact" class="bg-slate-900 text-white py-24 relative overflow-hidden">
      <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 text-center relative z-10 space-y-6">
        <h2 class="text-4xl font-bold tracking-tight sm:text-4xl">Digitalisasi Apotek Anda Hari Ini</h2>
        <p class="text-slate-400 text-lg max-w-2xl mx-auto font-normal">
          Tingkatkan akurasi manajemen operasional gudang farmasi Anda bersama keunggulan integrasi kecerdasan buatan PharmaProphet.
        </p>
        <div class="flex flex-col sm:flex-row gap-4 justify-center pt-6">
          <NuxtLink to="/register" class="px-10 py-4 bg-emerald-500 text-slate-950 font-medium rounded-xl hover:bg-emerald-400 transition shadow-lg tracking-wide text-center">
            Registrasi Akun Sekarang
          </NuxtLink>
        </div>
      </div>
    </section>

    <footer class="bg-slate-950 text-slate-400 border-t border-slate-900 py-12">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex flex-col sm:flex-row justify-between items-center gap-6 border-b border-slate-900 pb-8 mb-8">
          <div class="flex items-center gap-2">
            <div class="w-8 h-8 bg-emerald-500 rounded-lg flex items-center justify-center text-slate-950 font-black text-sm">Rx</div>
            <span class="text-lg font-black text-white tracking-tight">Pharma<span class="text-emerald-500">Prophet</span></span>
          </div>
          <p class="text-xs font-medium text-slate-500">&copy; 2026 PharmaProphet. Politeknik Negeri Padang. All rights reserved.</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<style scoped>
/* Smooth scrolling */
html {
  scroll-behavior: smooth;
}

/* Custom Animation classes */
@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.animate-slide-up {
  animation: slideUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

.animate-fade-in {
  animation: fadeIn 0.6s ease-out forwards;
}
</style>