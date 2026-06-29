<script setup>
import { ref, computed, watch } from 'vue'

definePageMeta({
  layout: 'sidebar',
  composables: 'useAuth' // Catatan: Biasanya menggunakan property 'middleware', bukan 'composables' untuk route guard
})

const config = useRuntimeConfig()
const { token } = useAuth()

// Ambil data produk dari backend
const { data: products, pending, error, refresh } = await useFetch(`${config.public.apiBase}/product`, {
  method: 'GET',
  headers: {
    Authorization: `Bearer ${token.value}`
  }
})

// --- STATE PAGINATION ---
const currentPage = ref(1)
const pageSize = ref(10) // Batas data per halaman

// Memotong data produk berdasarkan halaman aktif
const displayedProducts = computed(() => {
  if (!products.value) return []
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return products.value.slice(start, end)
})

// Menghitung total data asli untuk komponen pagination
const totalItems = computed(() => {
  return products.value ? products.value.length : 0
})

// Pembalas emit ketika tombol angka halaman diklik
const handlePageChange = (newPage) => {
  currentPage.value = newPage
}

// Reset halaman ke 1 jika data produk diperbarui/di-refresh dari server
watch(products, () => {
  currentPage.value = 1
}, { deep: true })

// Fungsi Hapus Produk
const deleteProduct = async (id) => {
  if (!confirm('Apakah Anda yakin ingin menghapus produk ini? Tindakan ini tidak dapat dibatalkan.')) return
  try {
    await $fetch(`${config.public.apiBase}/product/${id}`, {
      method: 'DELETE',
      headers: { Authorization: `Bearer ${token.value}` }
    })
    alert('Produk berhasil dihapus.')
    refresh()
  } catch (err) {
    alert(err.data?.detail || 'Gagal menghapus produk.')
  }
}
</script>

<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <div>
        <h1 class="text-2xl font-bold text-slate-900">Manajemen Produk</h1>
        <p class="text-sm text-slate-500">Kelola produk yang tersedia di dalam sistem.</p>
      </div>
      <NuxtLink to="/admin/products/create" class="px-4 py-2.5 bg-emerald-600 text-white font-semibold rounded-xl hover:bg-emerald-700 transition text-sm flex items-center gap-1">
        <Icon name="lucide:package-plus" class="text-base" />
        Tambah Produk
      </NuxtLink>
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
            <th class="p-4 text-xs font-bold text-slate-500 uppercase tracking-wider text-center">Aksi</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-100 text-sm text-slate-700">
          <tr v-for="product in displayedProducts" :key="product.id" class="hover:bg-slate-50/80 transition">
            <td class="p-4 font-mono text-slate-600 text-xs">{{ product.nama_produk }}</td>
            <td class="p-4 font-semibold text-slate-900">{{ product.kategori }}</td>
            <td class="p-4 text-slate-500">{{ product.harga_jual }}</td>
            <td class="p-4">{{ product.stok_saat_ini }}</td>
            <td class="p-4">{{ product.stok_minimum }}</td>
            <td class="p-4">{{ product.deskripsi }}</td>
            <td class="p-4 text-center space-x-3">
                <NuxtLink :to="`/admin/products/${product.id}/edit`" class="p-2 text-indigo-600 hover:bg-indigo-50 rounded-lg transition" title="Edit">
                    <Icon name="lucide:edit" class="text-lg" />
                </NuxtLink>
                <NuxtLink :to="`/admin/products/${product.id}/delete`" class="p-2 text-rose-600 hover:bg-rose-50 rounded-lg transition" title="Delete">
                    <Icon name="lucide:trash-2" class="text-lg" />
                </NuxtLink>
            </td>
          </tr>
          
          <tr v-if="!displayedProducts.length">
            <td colspan="7" class="p-8 text-center text-slate-400">Tidak ada data produk yang ditemukan.</td>
          </tr>
        </tbody>
      </table>

    </div>
      <div v-if="products?.length" class="flex justify-end bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
        <Pagination 
          :totalItems="totalItems" 
          :pageSize="pageSize" 
          :currentPage="currentPage"
          @page-changed="handlePageChange"
        />
      </div>
  </div>
</template>