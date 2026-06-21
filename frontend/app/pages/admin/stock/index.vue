<script setup>
definePageMeta({
  layout: 'sidebar', // Menggunakan layouts/sidebar.vue
  composables: 'useAuth'    // Menggunakan middleware/auth.ts
})

const config = useRuntimeConfig()
const { currentUser } = useAuth()

// 1. Ambil data stok 
const { data: rawStock, pending: stockPending, error: stockError, refresh } = await useFetch(`${config.public.apiBase}/stock/`, {
  method: 'GET',
  headers: {
    Authorization: `Bearer ${currentUser.value?.token}`
  }
})

// 2. Ambil data master produk untuk mencocokkan nama produknya
const { data: allProducts } = await useFetch(`${config.public.apiBase}/product/`, {
  method: 'GET',
  headers: {
    Authorization: `Bearer ${currentUser.value?.token}`
  }
})

// 3. Gabungkan data riwayat stok dengan master produk berdasarkan product_id
const combinedStocks = computed(() => {
  if (!rawStock.value || !allProducts.value) return []

  return rawStock.value.map(item => {
    const matched = allProducts.value.find(p => p.id === item.product_id)
    return {
      ...item,
      nama_produk: matched ? matched.nama_produk : `Produk ID #${item.product_id}`
    }
  })
})

// Fungsi menghapus data stok
const deleteStock = async (id) => {
  if (confirm('Apakah Anda yakin ingin menghapus data stok ini?')) {
    try {
      await $fetch(`${config.public.apiBase}/stock/${id}/`, {
        method: 'DELETE',
        headers: { Authorization: `Bearer ${currentUser.value?.token}` }
      })
      alert('Data stok berhasil dihapus')
      refresh()
    } catch (err) {
      alert('Gagal menghapus data stok')
    }
  }
}
</script>

<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <div>
        <h1 class="text-2xl font-bold text-slate-900">Manajemen Stok</h1>
        <p class="text-sm text-slate-500">Kelola stok produk yang tersedia di dalam sistem.</p>
      </div>
    </div>

    <div v-if="stockPending" class="text-center py-12 text-slate-500">
      <p class="animate-pulse font-medium text-sm">Sedang memuat data dari server...</p>
    </div>

    <div v-else-if="stockError" class="bg-rose-50 text-rose-600 p-4 rounded-xl border border-rose-100 text-sm">
      Gagal memuat data: {{ stockError.message || 'Terjadi kesalahan pada server.' }}
    </div>

    <div v-else class="bg-white rounded-2xl border border-slate-200 overflow-hidden shadow-sm">
      <table class="w-full text-left border-collapse">
        <thead class="bg-slate-50 border-b border-slate-200">
          <tr>
            <th class="p-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Nama Produk</th>
            <th class="p-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Type</th>
            <th class="p-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Jumlah</th>
            <th class="p-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Expired Date</th>
            <th class="p-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Deskripsi</th>
            <th class="p-4 text-xs font-bold text-slate-500 uppercase tracking-wider text-center">Aksi</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-100 text-sm text-slate-700">
          <tr v-for="item in combinedStocks" :key="item.id" class="hover:bg-slate-50/80 transition">
            <td class="p-4 font-semibold text-slate-900">{{ item.nama_produk }}</td>
            <td class="p-4">
              <span :class="item.type === 'Masuk' ? 'bg-emerald-50 text-emerald-700 border-emerald-100' : 'bg-rose-50 text-rose-700 border-rose-100'" 
                    class="px-2.5 py-0.5 text-xs font-bold rounded-md border">
                {{ item.type }}
              </span>
            </td>
            <td class="p-4 font-semibold text-slate-900">{{ item.jumlah }}</td>
            <td class="p-4 text-slate-500 font-mono text-xs">
              {{ item.expired_date ? new Date(item.expired_date).toLocaleDateString('id-ID') : '-' }}
            </td>
            <td class="p-4 text-slate-500 max-w-xs truncate">{{ item.deskripsi || '-' }}</td>
            <td class="p-4 text-center space-x-3">
                <NuxtLink :to="`/admin/stock/${item.id}/edit`" class="text-indigo-600 hover:text-indigo-900 font-semibold text-xs">Edit</NuxtLink>
                <button @click="deleteStock(item.id)" class="text-rose-600 hover:text-rose-900 font-semibold text-xs">Hapus</button>
            </td>
          </tr>
          
          <tr v-if="!combinedStocks.length">
            <td colspan="6" class="p-8 text-center text-slate-400">Tidak ada data stok yang ditemukan.</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>