<script setup>
definePageMeta({
  layout: 'sidebar', // Menggunakan layouts/sidebar.vue
  composables: 'useAuth'    // Menggunakan middleware/auth.ts
})

const config = useRuntimeConfig()
const { currentUser } = useAuth()

// 1. Ambil data transaksi langsung dari backend FastAPI
const { data: rawTransactions, pending: transactionsPending, error: transactionsError } = await useFetch(`${config.public.apiBase}/transaction/`, {
  method: 'GET',
  headers: {
    Authorization: `Bearer ${currentUser.value?.token}`
  }
})

// 2. Mapping data: Satu ID Nota = Satu Baris dengan format Nama Produk (Qty x @Rp Harga)
const transactions = computed(() => {
  if (!rawTransactions.value) return []

  return rawTransactions.value.map(t => {
    let detailProdukString = '-'
    let totalQtyNota = 0

    if (t.items && t.items.length > 0) {
      // Petakan setiap item menjadi format "Nama Obat (Qty x @Rp Harga)"
      const itemTextArray = t.items.map(item => {
        const nama = item.product?.nama_produk || `Produk ID #${item.product_id}`
        totalQtyNota += item.jumlah // Akumulasi total kuantitas per nota
        
        // Format harga satuan ke rupiah
        const hargaFormatted = Number(item.harga_satuan || 0).toLocaleString('id-ID')
        
        return `${nama} (${item.jumlah}x @Rp ${hargaFormatted})`
      })
      
      // Gabungkan array menjadi satu string dipisahkan koma
      detailProdukString = itemTextArray.join(', ')
    }

    return {
      id_nota: t.id,
      tanggal: t.tanggal,
      total_harga_nota: t.total_harga,
      jumlah_beli: totalQtyNota,
      produk_display: detailProdukString
    }
  })
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
            <th class="p-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Daftar Produk & Harga Satuan</th>
            <th class="p-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Total Qty</th>
            <th class="p-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Total Nota</th>
            <th class="p-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Tanggal Transaksi</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-100 text-sm text-slate-700">
          <tr v-for="tx in transactions" :key="tx.id_nota" class="hover:bg-slate-50/80 transition">
            <td class="p-4 font-mono text-xs text-slate-500">#TRX-{{ tx.id_nota }}</td>
            
            <td class="p-4 text-slate-900 font-medium max-w-md leading-relaxed">
              {{ tx.produk_display }}
            </td>
            
            <td class="p-4 font-medium text-slate-800">{{ tx.jumlah_beli }} Pcs</td>
            
            <td class="p-4 font-bold text-emerald-600">Rp {{ Number(tx.total_harga_nota).toLocaleString('id-ID') }}</td>
            
            <td class="p-4 text-slate-500 font-mono text-xs">
              {{ tx.tanggal ? new Date(tx.tanggal).toLocaleString('id-ID') : '-' }}
            </td>
          </tr>

          <tr v-if="!transactions.length">
            <td colspan="5" class="p-8 text-center text-slate-400">Tidak ada riwayat transaksi penjualan obat.</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>