<script setup>
definePageMeta({
  layout: 'sidebar', // Menggunakan layouts/sidebar.vue
  composables: 'useAuth'    // Menggunakan middleware/auth.ts
})

const config = useRuntimeConfig()
const { currentUser } = useAuth()

import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
)

// --- 1. FETCH SEMUA DATA YANG DIBUTUHKAN ---
// Ambil Data Transaksi
const { data: rawTransactions } = await useFetch(`${config.public.apiBase}/transaction/`, {
  method: 'GET',
  headers: { Authorization: `Bearer ${currentUser.value?.token}` }
})

// Ambil Data Master Produk
const { data: allProducts } = await useFetch(`${config.public.apiBase}/product/`, {
  method: 'GET',
  headers: { Authorization: `Bearer ${currentUser.value?.token}` }
})

// Ambil Data Mutasi Stok
const { data: rawStock } = await useFetch(`${config.public.apiBase}/stock/`, {
  method: 'GET',
  headers: { Authorization: `Bearer ${currentUser.value?.token}` }
})

// --- 2. LOGIKA KARTU METRIK UTAMA (TOP CARDS) ---
const totalProduk = computed(() => allProducts.value?.length || 0)

const stokKrisisCount = computed(() => {
  if (!allProducts.value) return 0
  // Memfilter produk yang stok_saat_ini kurang dari atau sama dengan stok_minimum
  return allProducts.value.filter(p => p.stok_saat_ini <= p.stok_minimum).length
})

const totalTransaksi = computed(() => rawTransactions.value?.length || 0)


// --- 3. LOGIKA PANEL BAWAH (PANEL KIRI DAN KANAN) ---

// Panel: Peringatan Stok Rendah (Diurutkan dari yang paling tipis)
const stokRendahList = computed(() => {
  if (!allProducts.value) return []
  return allProducts.value
    .filter(p => p.stok_saat_ini <= p.stok_minimum)
    .sort((a, b) => a.stok_saat_ini - b.stok_saat_ini)
    .slice(0, 5) // Batasi 5 teratas
})

// Panel: Stok Terbaru (Mutasi stok masuk/keluar teranyar)
const stokTerbaruList = computed(() => {
  if (!rawStock.value || !allProducts.value) return []
  return [...rawStock.value]
    .sort((a, b) => new Date(b.tanggal_update) - new Date(a.tanggal_update))
    .slice(0, 5)
    .map(s => {
      const prod = allProducts.value.find(p => p.id === s.product_id)
      return {
        ...s,
        nama_produk: prod ? prod.nama_produk : `Produk #${s.product_id}`
      }
    })
})

// Panel: Aktivitas Anda (Log riwayat gabungan ringkas)
const aktivitasList = computed(() => {
  const aktivitas = []
  
  // Ambil data transaksi terakhir
  if (rawTransactions.value) {
    rawTransactions.value.forEach(t => {
      t.items?.forEach(item => {
        aktivitas.push({
          tipe: 'Penjualan',
          teks: `Terjual ${item.product?.nama_produk || 'Obat'} sebanyak ${item.jumlah} ${item.product?.satuan || 'Pcs'}`,
          tanggal: t.tanggal
        })
      })
    })
  }

  // Ambil data tambah stok terakhir
  if (rawStock.value && allProducts.value) {
    rawStock.value.forEach(s => {
      const prod = allProducts.value.find(p => p.id === s.product_id)
      if (s.type === 'Masuk') {
        aktivitas.push({
          tipe: 'Stok',
          teks: `Tambah Stok ${prod?.nama_produk || 'Obat'} sebanyak ${s.jumlah} ${prod?.satuan || 'Pcs'}`,
          tanggal: s.tanggal_update
        })
      }
    })
  }

  // Urutkan berdasarkan tanggal terbaru
  return aktivitas.sort((a, b) => new Date(b.tanggal) - new Date(a.tanggal)).slice(0, 3)
})

// Panel: Produk Terlaris (Dihitung dari akumulasi jumlah transaksi sukses)
const produkTerlarisList = computed(() => {
  if (!rawTransactions.value) return []
  const counts = {}

  rawTransactions.value.forEach(t => {
    t.items?.forEach(item => {
      const nama = item.product?.nama_produk || `Produk ID #${item.product_id}`
      const satuan = item.product?.satuan || 'Pcs'
      if (!counts[nama]) {
        counts[nama] = { jumlah: 0, satuan }
      }
      counts[nama].jumlah += item.jumlah
    })
  })

  return Object.keys(counts)
    .map(name => ({ nama_produk: name, jumlah: counts[name].jumlah, satuan: counts[name].satuan }))
    .sort((a, b) => b.jumlah - a.jumlah)
    .slice(0, 4)
})

// --- 4. LOGIKA GRAFIK TREN TRANSAKSI ---
const today = new Date()
const thirtyDaysAgo = new Date(today)
thirtyDaysAgo.setDate(today.getDate() - 30)

const startDate = ref(thirtyDaysAgo.toISOString().split('T')[0])
const endDate = ref(today.toISOString().split('T')[0])

const chartData = computed(() => {
  const start = new Date(startDate.value)
  const end = new Date(endDate.value)
  end.setHours(23, 59, 59, 999)

  const dateMap = {}
  let currDate = new Date(start)
  while (currDate <= end) {
    const dStr = currDate.toLocaleDateString('id-ID', { day: '2-digit', month: 'short' })
    dateMap[dStr] = 0
    currDate.setDate(currDate.getDate() + 1)
  }

  if (rawTransactions.value) {
    rawTransactions.value.forEach(t => {
      const d = new Date(t.tanggal)
      if (d >= start && d <= end) {
        const dStr = d.toLocaleDateString('id-ID', { day: '2-digit', month: 'short' })
        if (dateMap[dStr] !== undefined) {
          dateMap[dStr] += 1
        }
      }
    })
  }

  return {
    labels: Object.keys(dateMap),
    datasets: [
      {
        label: 'Jumlah Transaksi',
        backgroundColor: '#3b82f6',
        borderColor: '#3b82f6',
        data: Object.values(dateMap),
        tension: 0.4,
        fill: true,
        backgroundColor: 'rgba(59, 130, 246, 0.1)'
      }
    ]
  }
})

const chartOptions = ref({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { display: false },
    tooltip: {
      mode: 'index',
      intersect: false,
    }
  },
  scales: {
    y: {
      beginAtZero: true,
      ticks: { stepSize: 1 }
    }
  }
})
</script>

<template>
  <div class="space-y-6">
    <div>
      <h1 class="text-2xl font-bold text-slate-900 tracking-tight">
        Selamat Datang Kembali, {{ currentUser?.nama_lengkap || 'Apoteker' }}!
      </h1>
      <p class="text-sm text-slate-500">Berikut ringkasan indikator penting operasional apotek saat ini.</p>  
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div class="bg-white p-6 rounded-2xl border border-slate-200/60 flex justify-between items-start shadow-sm">
        <div class="space-y-1">
          <p class="text-xs font-medium text-slate-400 uppercase tracking-wider">Total Produk</p>
          <h3 class="text-3xl font-bold text-slate-800 mt-1">{{ totalProduk }}</h3>
          <p class="text-xs text-slate-500 font-medium">dalam database</p>
        </div>
        <div class="p-3 bg-blue-50 text-blue-600 rounded-xl text-2xl flex items-center justify-center">
          <Icon name="lucide:box" />
        </div>
      </div>

      <div class="bg-white p-6 rounded-2xl border border-slate-200/60 flex justify-between items-start shadow-sm">
        <div class="space-y-1">
          <p class="text-xs font-medium text-slate-400 uppercase tracking-wider">Stok Krisis</p>
          <h2 class="text-4xl font-bold text-rose-600">{{ stokKrisisCount }}</h2>
          <p class="text-xs text-slate-500 font-medium">perlu perhatian</p>
        </div>
        <div class="p-3 bg-rose-50 text-rose-600 rounded-xl text-xl flex items-center justify-center">
          <Icon name="lucide:alert-triangle" />
        </div>
      </div>

      <div class="bg-white p-6 rounded-2xl border border-slate-200/60 flex justify-between items-start shadow-sm">
        <div class="space-y-1">
          <p class="text-xs font-medium text-slate-400 uppercase tracking-wider">Transaksi</p>
          <h2 class="text-4xl font-bold text-slate-900">{{ totalTransaksi }}</h2>
          <p class="text-xs text-slate-500 font-medium">transaksi penjualan</p>
        </div>
        <div class="p-3 bg-amber-50 text-amber-600 rounded-xl text-2xl flex items-center justify-center">
          <Icon name="lucide:shopping-cart" />
        </div>
      </div>
    </div>

    <!-- Grafik Tren Transaksi -->
    <div class="bg-white shadow-sm p-6 rounded-2xl border border-slate-200 space-y-4">
      <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h3 class="text-base font-bold text-slate-900">Tren Transaksi Harian</h3>
          <p class="text-xs text-slate-500">Jumlah transaksi sukses per hari berdasarkan rentang waktu.</p>
        </div>
        <div class="flex items-center gap-2">
          <input type="date" v-model="startDate" class="text-sm border border-slate-300 rounded-lg px-3 py-1.5 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500" />
          <span class="text-slate-500 text-sm">s/d</span>
          <input type="date" v-model="endDate" class="text-sm border border-slate-300 rounded-lg px-3 py-1.5 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500" />
        </div>
      </div>
      <div class="h-72 w-full">
        <Line :data="chartData" :options="chartOptions" />
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
      
      <div class="bg-white shadow-sm p-6 rounded-2xl border border-slate-200 space-y-4">
        <h3 class="text-base font-bold text-slate-900">Peringatan Stok Rendah</h3>
        <div class="space-y-3">
          <div v-for="item in stokRendahList" :key="item.id" class="flex justify-between items-center text-sm font-semibold">
            <span class="text-slate-700">{{ item.nama_produk }}</span>
            <span class="text-rose-600 bg-rose-50 px-2.5 py-0.5 rounded-md border border-rose-100 text-xs font-medium font-mono">
              {{ item.stok_saat_ini }} {{ item.satuan || 'Strip' }}
            </span>
          </div>
          <p v-if="!stokRendahList.length" class="text-xs text-slate-400 italic">Semua aman, tidak ada stok krisis.</p>
        </div>
      </div>

      <div class="bg-white shadow-sm p-6 rounded-2xl border border-slate-200 space-y-4">
        <h3 class="text-base font-bold text-slate-900">Stok Terbaru</h3>
        <div class="space-y-3">
          <div v-for="item in stokTerbaruList" :key="item.id" class="flex justify-between items-center text-sm font-semibold">
            <div class="flex items-center gap-2">
              <span :class="item.type === 'Masuk' ? 'text-emerald-600' : 'text-rose-500'" class="text-xs font-semibold tracking-tight">
                [{{ item.type }}]
              </span>
              <span class="text-slate-700">{{ item.nama_produk }}</span>
            </div>
            <span class="text-slate-400 text-xs font-semibold">
              {{ new Date(item.tanggal_update).toLocaleDateString('id-ID', { day: '2-digit', month: '2-digit', year: '2-digit' }) }}
            </span>
          </div>
          <p v-if="!stokTerbaruList.length" class="text-xs text-slate-400 italic">Belum ada riwayat mutasi stok.</p>
        </div>
      </div>

      <div class="bg-white p-6 rounded-2xl border border-slate-200 space-y-4">
        <h3 class="text-base font-bold text-slate-900">Aktivitas Anda</h3>
        <div class="space-y-4">
          <div v-for="(act, idx) in aktivitasList" :key="idx" class="space-y-0.5">
            <p class="text-sm font-semibold text-slate-800">{{ act.teks }}</p>
            <p class="text-[11px] font-medium text-slate-400 font-mono">
              {{ new Date(act.tanggal).toLocaleDateString('id-ID', { year: 'numeric', month: '2-digit', day: '2-digit' }) }}
            </p>
          </div>
          <p v-if="!aktivitasList.length" class="text-xs text-slate-400 italic">Belum ada aktivitas tercatat.</p>
        </div>
      </div>

      <div class="bg-white shadow-sm p-6 rounded-2xl border border-slate-200 space-y-4">
        <h3 class="text-base font-bold text-slate-900">Produk Terlaris</h3>
        <div class="space-y-3">
          <div v-for="(item, idx) in produkTerlarisList" :key="idx" class="flex justify-between items-center text-sm font-semibold">
            <span class="text-slate-700">{{ item.nama_produk }}</span>
            <span class="text-slate-900 font-mono text-xs">
              {{ item.jumlah }} {{ item.satuan }}
            </span>
          </div>
          <p v-if="!produkTerlarisList.length" class="text-xs text-slate-400 italic">Belum ada item obat terjual.</p>
        </div>
      </div>

    </div>
  </div>
</template>