<script setup>
definePageMeta({
  layout: 'sidebar', // Menggunakan layouts/sidebar.vue
  composables: 'useAuth'    // Menggunakan middleware/auth.ts
})

const config = useRuntimeConfig()
const { currentUser } = useAuth()

// 1. Cukup ambil data transaksi saja (Karena data produk sudah di-include oleh backend FastAPI-mu!)
const { data: rawTransactions, pending: transactionsPending, error: transactionsError } = await useFetch(`${config.public.apiBase}/transaction/`, {
  method: 'GET',
  headers: {
    Authorization: `Bearer ${currentUser.value?.token}`
  }
})

// 2. Kita ratakan (flatten) atau mapping strukturnya agar mudah dibaca di tabel template
const transactions = computed(() => {
  if (!rawTransactions.value) return []

  // Kita petakan agar jika 1 transaksi berisi beberapa item obat, semuanya ter-render rapi di tabel
  const list = []
  rawTransactions.value.forEach(t => {
    if (t.items && t.items.length > 0) {
      t.items.forEach(item => {
        list.push({
          id_nota: t.id,
          tanggal: t.tanggal,
          total_harga_nota: t.total_harga,
          jumlah_beli: item.jumlah,
          harga_satuan: item.harga_satuan,
          // Mengambil nama produk langsung dari object child 'product' bawaan FastAPI
          nama_produk: item.product?.nama_produk || `Produk ID #${item.product_id}`
        })
      })
    } else {
      // Jika transaksi tidak memiliki item obat sama sekali
      list.push({
        id_nota: t.id,
        tanggal: t.tanggal,
        total_harga_nota: t.total_harga,
        jumlah_beli: 0,
        harga_satuan: 0,
        nama_produk: '-'
      })
    }
  })
  return list
})
</script>

<template>
  <div class="space-y-6">
    <div>
      <h1 class="text-2xl font-bold text-slate-900">Manajemen Transaksi</h1>
      <p class="text-sm text-slate-500">Kelola dan pantau data transaksi penjualan obat apotek.</p>
    </div>

    <div v-if="transactionsPending" class="text-center py-12 text-slate-500">
      <p class="animate-pulse font-medium text-sm">Sedang memuat data transaksi...</p>
    </div>

    <div v-else-if="transactionsError" class="bg-rose-50 text-rose-600 p-4 rounded-xl border border-rose-100 text-sm">
      Gagal memuat data: {{ transactionsError.message || 'Terjadi kesalahan pada server.' }}
    </div>

    <div v-else class="bg-white rounded-2xl border border-slate-200 overflow-hidden shadow-sm">
      <table class="w-full text-left border-collapse">
        <thead class="bg-slate-50 border-b border-slate-200">
          <tr>
            <th class="p-4 text-xs font-bold text-slate-500 uppercase tracking-wider">ID Nota</th>
            <th class="p-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Nama Produk</th>
            <th class="p-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Jumlah Beli</th>
            <th class="p-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Harga Satuan</th>
            <th class="p-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Total Nota</th>
            <th class="p-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Tanggal Transaksi</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-100 text-sm text-slate-700">
          <tr v-for="(tx, index) in transactions" :key="index" class="hover:bg-slate-50/80 transition">
            <td class="p-4 font-mono text-xs text-slate-500">#TRX-{{ tx.id_nota }}</td>
            <td class="p-4 font-semibold text-slate-900">{{ tx.nama_produk }}</td>
            <td class="p-4 font-medium text-slate-800">{{ tx.jumlah_beli }} Pcs</td>
            <td class="p-4 text-slate-600">Rp {{ Number(tx.harga_satuan).toLocaleString('id-ID') }}</td>
            <td class="p-4 font-bold text-emerald-600">Rp {{ Number(tx.total_harga_nota).toLocaleString('id-ID') }}</td>
            <td class="p-4 text-slate-500 font-mono text-xs">
              {{ tx.tanggal ? new Date(tx.tanggal).toLocaleString('id-ID') : '-' }}
            </td>
          </tr>

          <tr v-if="!transactions.length">
            <td colspan="6" class="p-8 text-center text-slate-400">Tidak ada riwayat transaksi penjualan obat.</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>