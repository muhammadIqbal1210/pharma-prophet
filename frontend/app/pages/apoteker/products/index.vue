<script setup>
definePageMeta({
  layout: 'sidebar', // Menggunakan layouts/sidebar.vue
  composables: 'useAuth'    // Menggunakan middleware/auth.ts
})
const config = useRuntimeConfig()
const { currentUser } = useAuth()

// ambil data produk dari backend
const { data: products, pending, error, refresh } = await useFetch(`${config.public.apiBase}/product/`, {
  method: 'GET',
  headers: {
    Authorization: `Bearer ${currentUser.value?.token}`
  }
})
</script>
<template>
  <div class="space-y-6">
    <div>
      <h1 class="text-2xl font-bold text-slate-900">Daftar Produk</h1>
      <p class="text-sm text-slate-500">Lihat daftar produk yang tersedia di apotek.</p>
    </div>

    <div v-if="pending" class="text-center py-12 text-slate-500">
      <p class="animate-pulse font-medium text-sm">Sedang memuat data dari server...</p>
    </div>

    <div v-else-if="error" class="bg-rose-50 text-rose-600 p-4 rounded-xl border border-rose-100 text-sm">
      Gagal memuat data: {{ error.message || 'Terjadi kesalahan pada server.' }}
    </div>

    <div v-else class="bg-white rounded-2xl border border-slate-200 overflow-hidden shadow-sm">
      <table class="w-full text-left border-collapse">
        <thead class="bg-slate-50 border-b border-slate-200">
          <tr>
            <th class="p-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Nama Produk</th>
            <th class="p-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Kategori</th>
            <th class="p-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Harga Jual</th>
            <th class="p-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Stok saat ini</th>
            <th class="p-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Stok Minimum</th>
            <th class="p-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Deskripsi</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-100 text-sm text-slate-700">
          <tr v-for="product in products" :key="product.id" class="hover:bg-slate-50/80 transition">
            <td class="p-4 font-mono text-slate-600 text-xs">{{ product.nama_produk }}</td>
            <td class="p-4 font-semibold text-slate-900">{{ product.kategori }}</td>
            <td class="p-4 text-slate-500">{{ product.harga_jual }}</td>
            <td class="p-4">{{ product.stok_saat_ini }}</td>
            <td class="p-4">{{ product.stok_minimum }}</td>
            <td class="p-4">{{ product.deskripsi }}</td>
            </tr>
            <tr v-if="!products?.length">
              <td colspan="7" class="p-8 text-center text-slate-400">Tidak ada data produk yang ditemukan.</td>
            </tr>
        </tbody>
        </table>
    </div>
    </div>
</template>