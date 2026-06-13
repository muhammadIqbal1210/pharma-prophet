<script setup>
definePageMeta({
  layout: 'sidebar', // Menggunakan layouts/user-panel.vue
  composables: 'useAuth'    // Menggunakan middleware/auth.ts
})
</script>
<template>
  <div class="space-y-6">
    <div class="bg-gradient-to-r from-emerald-500 to-green-600 rounded-3xl p-6 text-white shadow-md">
      <h2 class="text-2xl font-bold mb-1">Selamat Datang di Panel Apoteker</h2>
      <p class="text-emerald-100 text-sm">Gunakan menu navigasi untuk mengelola stok obat dan transaksi penjualan hari ini.</p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div class="bg-white rounded-2xl p-6 shadow-sm border border-slate-100">
        <p class="text-sm font-medium text-slate-500 uppercase">Transaksi Hari Ini</p>
        <p class="text-2xl font-bold text-slate-900 mt-2">0</p>
      </div>
      <div class="bg-white rounded-2xl p-6 shadow-sm border border-slate-100">
        <p class="text-sm font-medium text-slate-500 uppercase">Obat Hampir Habis</p>
        <p class="text-2xl font-bold text-amber-600 mt-2">0</p>
      </div>
      <div class="bg-white rounded-2xl p-6 shadow-sm border border-slate-100">
        <p class="text-sm font-medium text-slate-500 uppercase">Total Produk Obat</p>
        <p class="text-2xl font-bold text-emerald-600 mt-2">0</p>
      </div>
    </div>
  </div>
</template>