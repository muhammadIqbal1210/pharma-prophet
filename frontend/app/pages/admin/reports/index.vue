<script setup>
definePageMeta({
  layout: 'sidebar',
  composables: 'useAuth'
})

const config = useRuntimeConfig()
const { currentUser } = useAuth()

// --- STATE FILTER PERIODE ---
const dateNow = new Date().toISOString().split('T')[0]
const startDate = ref('2024-01-01') // Sesuaikan default awal
const endDate = ref(dateNow)

// --- FETCH DATA SUMMARY ---
// Mengambil data omzet dan total transaksi
const { data: summary, refresh: refreshSummary } = await useFetch(`${config.public.apiBase}/transaction/report/summary`, {
  headers: { Authorization: `Bearer ${currentUser.value?.token}` },
  query: { start_date: startDate, end_date: endDate }
})

// --- FETCH DATA RIWAYAT (DETAIL) ---
// Mengambil list transaksi untuk tabel di bawah
const { data: rawTransactions, refresh: refreshList } = await useFetch(`${config.public.apiBase}/transaction/`, {
  headers: { Authorization: `Bearer ${currentUser.value?.token}` }
})

// --- COMPUTED LOGIC ---
const transactions = computed(() => {
  if (!rawTransactions.value) return []
  // Filter list transaksi berdasarkan range tanggal di frontend
  return rawTransactions.value.filter(t => {
    const tDate = t.tanggal.split('T')[0]
    return tDate >= startDate.value && tDate <= endDate.value
  })
})

const totalItemTerjual = computed(() => {
  return transactions.value.reduce((acc, t) => {
    const qty = t.items?.reduce((sum, item) => sum + item.jumlah, 0) || 0
    return acc + qty
  }, 0)
})

const rataRataTransaksi = computed(() => {
  if (!summary.value?.total_transaksi) return 0
  return (summary.value.total_omzet || 0) / summary.value.total_transaksi
})

// --- FUNGSI ACTION ---
const handlePrint = () => {
  window.print()
}

const exportPDF = () => {
  alert('Fitur Ekspor PDF sedang menyiapkan dokumen...')
  // Di sini biasanya memanggil library jspdf atau endpoint backend khusus pdf
}

// Otomatis refresh data saat tanggal diubah
watch([startDate, endDate], () => {
  refreshSummary()
  refreshList()
})
</script>

<template>
  <div class="space-y-8 print:p-0">
    <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 print:hidden">
      <div>
        <h1 class="text-2xl font-bold text-slate-900 tracking-tight">Laporan Penjualan</h1>
        <p class="text-slate-500">Pantau performa finansial dan volume transaksi apotek.</p>
      </div>
      
      <div class="flex items-center gap-3">
        <div class="flex items-center bg-white border border-slate-200 rounded-xl px-3 py-2 gap-2 shadow-sm">
          <input v-model="startDate" type="date" class="text-sm font-medium text-slate-700 outline-none bg-transparent" />
          <span class="text-slate-400">-</span>
          <input v-model="endDate" type="date" class="text-sm font-medium text-slate-700 outline-none bg-transparent" />
        </div>

        <button @click="handlePrint" class="p-2.5 bg-white border border-slate-200 rounded-xl hover:bg-slate-50 transition shadow-sm text-slate-600">
          <Icon name="lucide:printer" class="text-xl" />
        </button>
        
        <button @click="exportPDF" class="px-5 py-2.5 bg-slate-900 text-white rounded-xl font-semibold text-sm hover:bg-slate-800 transition shadow-lg shadow-slate-200 flex items-center gap-2">
          Ekspor PDF
        </button>
      </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div class="bg-white p-6 rounded-3xl border border-slate-100 shadow-sm space-y-2">
        <p class="text-sm font-semibold text-slate-400">Total Pendapatan</p>
        <h2 class="text-2xl font-bold text-slate-900">Rp. {{ (summary?.total_omzet || 0).toLocaleString('id-ID') }}</h2>
        <div class="h-1.5 w-12 bg-emerald-500 rounded-full"></div>
      </div>

      <div class="bg-white p-6 rounded-3xl border border-slate-100 shadow-sm space-y-2">
        <p class="text-sm font-semibold text-slate-400">Item Terjual</p>
        <h2 class="text-2xl font-bold text-slate-900">{{ totalItemTerjual }} <span class="text-sm font-medium text-slate-400 font-mono">Pcs</span></h2>
        <div class="h-1.5 w-12 bg-blue-500 rounded-full"></div>
      </div>

      <div class="bg-white p-6 rounded-3xl border border-slate-100 shadow-sm space-y-2">
        <p class="text-sm font-semibold text-slate-400">Rata-rata Transaksi</p>
        <h2 class="text-2xl font-bold text-slate-900">Rp. {{ Math.round(rataRataTransaksi).toLocaleString('id-ID') }}</h2>
        <div class="h-1.5 w-12 bg-amber-500 rounded-full"></div>
      </div>

      <div class="bg-white p-6 rounded-3xl border border-slate-100 shadow-sm space-y-2">
        <p class="text-sm font-semibold text-slate-400">Total Transaksi</p>
        <h2 class="text-2xl font-bold text-slate-900">{{ summary?.total_transaksi || 0 }} <span class="text-sm font-medium text-slate-400 font-mono">Nota</span></h2>
        <div class="h-1.5 w-12 bg-purple-500 rounded-full"></div>
      </div>
    </div>

    <div class="space-y-4">
      <div class="flex items-center gap-2">
        <Icon name="lucide:history" class="text-slate-400" />
        <h3 class="text-lg font-medium text-slate-900">Riwayat Penjualan</h3>
      </div>

      <div class="bg-white rounded-2xl border border-slate-200 overflow-hidden shadow-sm">
        <table class="w-full text-left border-collapse">
          <thead class="bg-slate-50/50 border-b border-slate-100">
            <tr>
              <th class="p-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Waktu</th>
              <th class="p-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Item Terjual</th>
              <th class="p-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Total Bayar</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-50">
            <tr v-for="t in transactions" :key="t.id" class="hover:bg-slate-50/80 transition">
              <td class="p-4">
                <p class="font-bold text-slate-700 text-sm">{{ new Date(t.tanggal).toLocaleDateString('id-ID') }}</p>
                <p class="text-xs font-medium text-slate-400 font-mono">{{ new Date(t.tanggal).toLocaleTimeString('id-ID', { hour: '2-digit', minute: '2-digit' }) }}</p>
              </td>
              <td class="p-5">
                <div class="flex flex-wrap gap-1.5">
                  <span v-for="item in t.items" :key="item.id" 
                        class="px-3 py-1 bg-slate-100 text-slate-600 rounded-full text-[10px] font-bold uppercase tracking-tight border border-slate-200">
                    {{ item.product?.nama_produk }} ({{ item.jumlah }})
                  </span>
                </div>
              </td>
              <td class="p-4 text-right">
                <p class="font-bold text-slate-900 text-sm">Rp. {{ t.total_harga.toLocaleString('id-ID') }}</p>
              </td>
            </tr>

            <tr v-if="!transactions.length">
              <td colspan="7" class="p-8 text-center text-slate-400 font-medium italic">
                Tidak ada riwayat penjualan pada periode ini.
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>