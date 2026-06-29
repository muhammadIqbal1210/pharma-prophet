<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
)

definePageMeta({
  layout: 'sidebar'
})

const config = useRuntimeConfig()
const { currentUser, token } = useAuth()

const products = ref([])
// Diubah menjadi null di awal agar sistem tahu belum ada produk spesifik yang dipilih
const selectedProductId = ref(null) 
const selectedTimeRange = ref(90)

const activeForecast = ref(null)
const isLoading = ref(false)
const isLoadingStats = ref(false)
const errorMessage = ref('')

// --- COMPUTED PROPERTIES ---

const totalProducts = computed(() => products.value.length)

const stokKrisis = computed(() => {
  return products.value.filter(p => p.stok_saat_ini < p.stok_minimum).length
})

// Mengurutkan produk berdasarkan prioritas pembelian (Paling Butuh -> Aman)
const prioritizedProducts = computed(() => {
  return [...products.value].sort((a, b) => {
    // Rasio stok saat ini dibanding stok minimum. Semakin kecil rasionya, semakin kritis.
    const ratioA = a.stok_minimum > 0 ? (a.stok_saat_ini / a.stok_minimum) : 1
    const ratioB = b.stok_minimum > 0 ? (b.stok_saat_ini / b.stok_minimum) : 1
    return ratioA - ratioB
  })
})

const currentProductForecast30 = computed(() => {
  return activeForecast.value ? Math.round(activeForecast.value.forecast_30_days) : 0
})

const currentProductName = computed(() => {
  if (activeForecast.value) {
    return activeForecast.value.product_name
  }
  const prod = products.value.find(p => p.id === selectedProductId.value)
  return prod ? prod.nama_produk : '-'
})

// --- METHODS ---

// Fetch semua produk
async function loadProducts() {
  isLoadingStats.value = true
  try {
    const headers = { 
      Authorization: `Bearer ${token.value}` 
    }
    const data = await $fetch(`${config.public.apiBase}/product/`, {
      method: 'GET',
      headers
    })
    products.value = Array.isArray(data) ? data : []
    
    // INFO: selectedProductId sengaja dibiarkan null agar tampilan pertama adalah list prioritas
  } catch (err) {
    console.error('Gagal mengambil data produk:', err)
    errorMessage.value = 'Gagal mengambil data produk.'
  } finally {
    isLoadingStats.value = false
  }
}

// Fetch forecast untuk produk spesifik
async function fetchForecast() {
  if (!selectedProductId.value) return
  isLoading.value = true
  errorMessage.value = ''
  try {
    const headers = { 
      Authorization: `Bearer ${token.value}` 
    }
    const data = await $fetch(`${config.public.apiBase}/forecast/${selectedProductId.value}`, {
      method: 'GET',
      headers
    })
    activeForecast.value = data
  } catch (err) {
    console.error('Gagal memproses prediksi:', err)
    activeForecast.value = null
    errorMessage.value = 'Data transaksi tidak mencukupi untuk melakukan prediksi Prophet (butuh minimal 2 hari penjualan).'
  } finally {
    isLoading.value = false
  }
}

// Pantau perubahan dropdown produk untuk langsung fetch data otomatis
watch(selectedProductId, (newId) => {
  if (newId) {
    fetchForecast()
  } else {
    activeForecast.value = null
  }
})

// --- CHART CONFIGURATION ---
const chartData = computed(() => {
  if (!activeForecast.value) {
    return { labels: [], datasets: [] }
  }

  const historical = activeForecast.value.historical_data || []
  const forecast = activeForecast.value.forecast_data || []

  const allLabels = []
  const historicalPoints = []
  const forecastPoints = []

  historical.forEach(pt => {
    allLabels.push(pt.ds)
    historicalPoints.push(pt.y)
    forecastPoints.push(null)
  })

  if (historical.length > 0 && forecast.length > 0) {
    const lastHist = historical[historical.length - 1]
    forecastPoints[forecastPoints.length - 1] = lastHist.y
  }

  const limitedForecast = forecast.slice(0, selectedTimeRange.value)
  limitedForecast.forEach(pt => {
    allLabels.push(pt.ds)
    historicalPoints.push(null)
    // Pembulatan angka desimal Prophet ke angka bulat terdekat
    forecastPoints.push(pt.yhat !== null ? Math.round(pt.yhat) : null)
  })

  return {
    labels: allLabels.map(d => {
      const dateObj = new Date(d)
      return dateObj.toLocaleDateString('id-ID', { day: 'numeric', month: 'short' })
    }),
    datasets: [
      {
        label: 'Penjualan Historis',
        data: historicalPoints,
        borderColor: '#10b981',
        backgroundColor: 'rgba(16, 185, 129, 0.1)',
        borderWidth: 2.5,
        tension: 0.3,
        fill: true,
        pointRadius: 2,
        pointHoverRadius: 5
      },
      {
        label: `Prediksi Prophet (${selectedTimeRange.value} Hari)`,
        data: forecastPoints,
        borderColor: '#f59e0b',
        backgroundColor: 'rgba(245, 158, 11, 0.05)',
        borderWidth: 2.5,
        borderDash: [6, 4],
        tension: 0.3,
        fill: false,
        pointRadius: 0,
        pointHoverRadius: 5
      }
    ]
  }
})

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'top',
      labels: {
        font: { family: 'sans-serif', weight: '600', size: 11 },
        usePointStyle: true
      }
    },
    tooltip: {
      padding: 12,
      cornerRadius: 8,
      backgroundColor: 'rgba(15, 23, 42, 0.9)'
    }
  },
  scales: {
    y: {
      grid: { color: 'rgba(226, 232, 240, 0.6)' },
      ticks: {
        font: { size: 10 },
        callback: function(value) { if (value % 1 === 0) return value }
      }
    },
    x: {
      grid: { display: false },
      ticks: { maxTicksLimit: 12, font: { size: 10 } }
    }
  }
}

onMounted(() => {
  loadProducts()
})
</script>

<template>
  <div class="p-1 space-y-6 max-w-7xl mx-auto bg-slate-50 min-h-screen">
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
      <div>
        <h1 class="text-2xl font-bold text-slate-900 tracking-tight">Analisis Prediksi AI</h1>
        <p class="text-sm font-normal text-slate-500 mt-1">Estimasi kebutuhan stok menggunakan Artificial Intelligence.</p>
      </div>
      <button 
        v-if="selectedProductId" 
        @click="selectedProductId = null"
        class="bg-white border border-slate-200 text-slate-700 hover:bg-slate-50 font-bold text-sm px-4 py-2 rounded-xl transition-all shadow-sm flex items-center gap-2"
      >
        <Icon name="lucide:arrow-left" class="text-lg" />
        <span>Kembali ke Prioritas</span>
      </button>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div class="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm flex justify-between items-center">
        <div class="space-y-1">
          <p class="text-xs font-bold uppercase tracking-wider text-slate-400">Total Produk</p>
          <div class="text-3xl font-bold text-slate-900">
            <span v-if="isLoadingStats" class="animate-pulse">...</span>
            <span v-else>{{ totalProducts }}</span>
          </div>
          <p class="text-xs font-semibold text-slate-400">dalam database</p>
        </div>
        <div class="w-12 h-12 rounded-xl bg-slate-100 flex items-center justify-center text-slate-500">
          <Icon name="lucide:package" class="text-2xl" />
        </div>
      </div>

      <div class="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm flex justify-between items-center">
        <div class="space-y-1">
          <p class="text-xs font-bold uppercase tracking-wider text-slate-400">Stok Krisis</p>
          <div class="text-3xl font-bold text-rose-600">
            <span v-if="isLoadingStats" class="animate-pulse">...</span>
            <span v-else>{{ stokKrisis }}</span>
          </div>
          <p class="text-xs font-semibold text-rose-400">perlu perhatian</p>
        </div>
        <div class="w-12 h-12 rounded-xl bg-rose-50 flex items-center justify-center text-rose-500">
          <Icon name="lucide:alert-triangle" class="text-2xl" />
        </div>
      </div>

      <div class="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm flex justify-between items-center">
        <div class="space-y-1">
          <p class="text-xs font-bold uppercase tracking-wider text-slate-400">Prediksi 30 Hari</p>
          <div class="text-2xl font-bold text-emerald-600">
            <span v-if="isLoading" class="animate-pulse">...</span>
            <span v-else-if="selectedProductId && activeForecast">{{ currentProductForecast30 }}</span>
            <span v-else>-</span>
          </div>
          <p class="text-xs font-semibold text-slate-500 truncate max-w-[180px]">{{ selectedProductId ? currentProductName : 'Pilih produk di bawah' }}</p>
        </div>
        <div class="w-12 h-12 rounded-xl bg-emerald-50 flex items-center justify-center text-emerald-500">
          <Icon name="lucide:cpu" class="text-2xl" />
        </div>
      </div>
    </div>

    <div class="bg-white rounded-2xl p-4 border border-slate-200 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div class="flex flex-wrap items-center gap-6">
        <div class="flex items-center gap-2">
          <label for="product-select" class="text-sm font-bold text-slate-600 shrink-0">Produk :</label>
          <select
            id="product-select"
            v-model="selectedProductId"
            class="bg-slate-50 border border-slate-200 rounded-xl px-4 py-2 text-sm font-medium text-slate-700 outline-none focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500 transition-all min-w-[240px]"
          >
            <option :value="null">-- Lihat Semua Daftar Prioritas --</option>
            <option v-for="p in products" :key="p.id" :value="p.id">
              {{ p.nama_produk }}
            </option>
          </select>
        </div>

        <div v-if="selectedProductId" class="flex items-center gap-2">
          <label for="time-select" class="text-sm font-bold text-slate-600 shrink-0">Waktu :</label>
          <select
            id="time-select"
            v-model="selectedTimeRange"
            class="bg-slate-50 border border-slate-200 rounded-xl px-4 py-2 text-sm font-medium text-slate-700 outline-none focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500 transition-all"
          >
            <option :value="30">30 Hari</option>
            <option :value="60">60 Hari</option>
            <option :value="90">90 Hari</option>
          </select>
        </div>
      </div>

      <button
        v-if="selectedProductId"
        @click="fetchForecast"
        :disabled="isLoading"
        class="bg-emerald-600 hover:bg-emerald-700 disabled:bg-emerald-300 text-white font-bold text-sm px-6 py-2.5 rounded-xl transition-all shadow-sm flex items-center gap-2 justify-center"
      >
        <Icon v-if="isLoading" name="lucide:loader" class="animate-spin text-lg" />
        <span>Tampilkan Forecast</span>
      </button>
    </div>

    <div v-if="!selectedProductId" class="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
      <div class="p-6 border-b border-slate-100">
        <h3 class="text-lg font-bold text-slate-900">Rekomendasi Prioritas Pembelian</h3>
        <p class="text-xs text-slate-500 mt-1">Daftar produk diurutkan berdasarkan tingkat kekosongan stok terparah.</p>
      </div>

      <div class="overflow-x-auto">
        <table class="w-full text-left border-collapse">
          <thead>
            <tr class="bg-slate-50 border-b border-slate-200 text-xs font-bold text-slate-400 uppercase tracking-wider">
              <th class="p-4 pl-6">Nama Produk</th>
              <th class="p-4">Stok Saat Ini</th>
              <th class="p-4">Stok Minimum</th>
              <th class="p-4">Status</th>
              <th class="p-4 text-center pr-6">Aksi</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100 text-sm font-medium text-slate-700">
            <tr v-if="isLoadingStats" class="text-center text-slate-400">
              <td colspan="5" class="p-8">Memuat data produk...</td>
            </tr>
            <tr v-else-if="prioritizedProducts.length === 0" class="text-center text-slate-400">
              <td colspan="5" class="p-8">Tidak ada data produk ditemukan.</td>
            </tr>
            <tr 
              v-for="p in prioritizedProducts" 
              :key="p.id" 
              class="hover:bg-slate-50/80 transition-colors"
            >
              <td class="p-4 pl-6 font-bold text-slate-900">{{ p.nama_produk }}</td>
              <td class="p-4">
                <span :class="p.stok_saat_ini < p.stok_minimum ? 'text-rose-600 font-bold' : 'text-slate-600'">
                  {{ p.stok_saat_ini }}
                </span>
              </td>
              <td class="p-4 text-slate-500">{{ p.stok_minimum }}</td>
              <td class="p-4">
                <span 
                  v-if="p.stok_saat_ini <= 0" 
                  class="bg-rose-100 text-rose-700 text-xs font-bold px-2.5 py-1 rounded-full"
                >
                  Habis Total
                </span>
                <span 
                  v-else-if="p.stok_saat_ini < p.stok_minimum" 
                  class="bg-amber-100 text-amber-700 text-xs font-bold px-2.5 py-1 rounded-full"
                >
                  Kritis
                </span>
                <span 
                  v-else 
                  class="bg-emerald-100 text-emerald-700 text-xs font-bold px-2.5 py-1 rounded-full"
                >
                  Aman
                </span>
              </td>
              <td class="p-4 text-center pr-6">
                <button 
                  @click="selectedProductId = p.id"
                  class="text-emerald-600 hover:text-emerald-700 font-bold text-xs inline-flex items-center gap-1 bg-emerald-50 hover:bg-emerald-100 px-3 py-1.5 rounded-lg transition-all"
                >
                  <span>Analisis AI</span>
                  <Icon name="lucide:chevron-right" class="text-sm" />
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div v-else class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <div class="lg:col-span-2 bg-white rounded-2xl p-6 border border-slate-200 shadow-sm flex flex-col h-[400px]">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-lg font-bold text-slate-900">Grafik Prediksi Kebutuhan Stok</h3>
          <span class="text-xs bg-emerald-50 text-emerald-700 font-semibold px-2.5 py-1 rounded-full border border-emerald-100">
            Prophet Model
          </span>
        </div>

        <div class="relative flex-1">
          <div v-if="isLoading" class="absolute inset-0 flex flex-col items-center justify-center bg-white/80 z-10 gap-3">
            <Icon name="lucide:loader" class="text-3xl text-emerald-600 animate-spin" />
            <p class="text-sm font-medium text-slate-500">Menganalisis tren penjualan...</p>
          </div>

          <div v-else-if="errorMessage" class="absolute inset-0 flex flex-col items-center justify-center text-center p-6 bg-rose-50/50 rounded-xl z-10 border border-rose-100">
            <Icon name="lucide:alert-circle" class="text-4xl text-rose-500 mb-2" />
            <h4 class="font-bold text-rose-900 mb-1">Terjadi Masalah</h4>
            <p class="text-xs text-rose-600 max-w-md">{{ errorMessage }}</p>
          </div>

          <Line v-else :data="chartData" :options="chartOptions" />
        </div>
      </div>

      <div class="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm flex flex-col justify-between">
        <div>
          <h3 class="text-lg font-bold text-slate-900 mb-4">Rangkuman Proyeksi AI</h3>
          <p class="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-6">Metrik Kebutuhan</p>

          <div class="space-y-6">
            <div class="flex items-start gap-4">
              <div class="w-10 h-10 rounded-xl bg-indigo-50 flex items-center justify-center text-indigo-500 shrink-0 mt-0.5">
                <Icon name="lucide:calendar-range" class="text-xl" />
              </div>
              <div class="space-y-1">
                <h4 class="text-sm font-bold text-slate-800">Total Prediksi 60 hari</h4>
                <p class="text-xs text-slate-500 leading-relaxed">
                  Prophet memproyeksikan kebutuhan 
                  <span class="font-bold text-indigo-600">
                    {{ activeForecast ? Math.round(activeForecast.forecast_60_days) : 0 }}
                  </span> 
                  unit untuk 60 hari ke depan.
                </p>
              </div>
            </div>

            <div class="flex items-start gap-4">
              <div class="w-10 h-10 rounded-xl bg-amber-50 flex items-center justify-center text-amber-500 shrink-0 mt-0.5">
                <Icon name="lucide:calendar-days" class="text-xl" />
              </div>
              <div class="space-y-1">
                <h4 class="text-sm font-bold text-slate-800">Total Prediksi 90 hari</h4>
                <p class="text-xs text-slate-500 leading-relaxed">
                  Prophet memproyeksikan kebutuhan 
                  <span class="font-bold text-amber-600">
                    {{ activeForecast ? Math.round(activeForecast.forecast_90_days) : 0 }}
                  </span> 
                  unit untuk 90 hari ke depan.
                </p>
              </div>
            </div>
          </div>
        </div>

        <div class="mt-8 pt-6 border-t border-slate-100 space-y-4">
          <div>
            <p class="text-xs font-bold text-slate-400 uppercase tracking-wider">Rekomendasi Pembelian</p>
            <div class="flex items-baseline gap-2 mt-1">
              <span class="text-3xl font-bold text-slate-900">
                {{ activeForecast ? Math.round(activeForecast.recommended_order) : 0 }}
              </span>
              <span class="text-xs font-semibold text-slate-500">Unit (Estimasi 30 Hari)</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>