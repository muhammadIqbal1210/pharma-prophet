<script setup>
definePageMeta({
  layout: 'sidebar', // Menggunakan layouts/sidebar.vue
  composables: 'useAuth'    // Menggunakan middleware/auth.ts
})

const config = useRuntimeConfig()
const { currentUser, token } = useAuth()

// --- STATE REAKTIF MODAL & FORM STOK ---
const isModalOpen = ref(false)
const form = ref({
  product_id: '',
  type: 'Masuk',
  jumlah: '',
  expired_date: '',
  deskripsi: ''
})

// 1. Ambil data stok (Ditambahkan trailing slash '/' agar terhindar dari redirect 307)
const { data: rawStock, pending: stockPending, error: stockError, refresh } = await useFetch(`${config.public.apiBase}/stock/`, {
  method: 'GET',
  headers: {
    Authorization: `Bearer ${token.value}`
  }
})

// 2. Ambil data master produk untuk kebutuhan Dropdown Select & mapping nama
const { data: allProducts } = await useFetch(`${config.public.apiBase}/product/`, {
  method: 'GET',
  headers: {
    Authorization: `Bearer ${token.value}`
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

// --- AKSI KEDUA: SIMPAN DATA STOK BARU ---
const handleAddStock = async () => {
  try {
    const waktuSekarang = new Date().toISOString()
    // Validasi data angka sebelum dikirim
    const payload = {
      ...form.value,
      product_id: Number(form.value.product_id),
      jumlah: Number(form.value.jumlah),
      tanggal_update: waktuSekarang,
      // Jika tipe Keluar, set expired_date menjadi null atau kosongkan jika tidak diisi
      expired_date: form.value.expired_date || null
    }

    await $fetch(`${config.public.apiBase}/stock/`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token.value}`,
        'Content-Type': 'application/json'
      },
      body: payload
    })

    alert('Data mutasi stok berhasil ditambahkan!')
    
    // Reset Form & Tutup Modal
    form.value = { product_id: '', type: 'Masuk', jumlah: '', expired_date: '', deskripsi: '' }
    isModalOpen.value = false
    refresh() // Muat ulang data tabel otomatis
  } catch (error) {
    const rawDetail = error.response?._data?.detail
    const errorMessage = Array.isArray(rawDetail) ? rawDetail[0]?.msg : rawDetail || error.message
    alert('Gagal menambah stok: ' + errorMessage)
  }
}

// --- AKSI KETIGA: HAPUS RIWAYAT STOK ---
const deleteStock = async (id) => {
  if (confirm('Apakah Anda yakin ingin menghapus data log stok ini?')) {
    try {
      await $fetch(`${config.public.apiBase}/stock/${id}/`, {
        method: 'DELETE',
        headers: { Authorization: `Bearer ${token.value}` }
      })
      alert('Data riwayat stok berhasil dihapus.')
      refresh()
    } catch (err) {
      alert('Gagal menghapus data stok.')
    }
  }
}

</script>

<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <div>
        <h1 class="text-2xl font-bold text-slate-900">Riwayat Stok Produk</h1>
        <p class="text-sm text-slate-500">Pantau perubahan stok produk dari waktu ke waktu.</p>
      </div>
      <button @click="isModalOpen = true" class="px-4 py-2.5 bg-emerald-600 text-white font-semibold rounded-xl hover:bg-emerald-700 transition text-sm flex items-center gap-1.5 shadow-sm">
        <Icon name="lucide:pill" class="text-base" />
        Tambah Stok
      </button>
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
            <th class="p-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Tanggal Update</th>
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
            <td class="p-4 text-slate-500 font-mono text-xs">
                {{ item.tanggal_update ? new Date(item.tanggal_update).toLocaleString('id-ID') : '-' }}
            </td>
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

    <div v-if="isModalOpen" class="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/50 backdrop-blur-sm">
      <div class="bg-white w-full max-w-md rounded-2xl shadow-xl p-6 border border-slate-100 space-y-4">
        
        <div class="flex justify-between items-center border-b pb-3">
          <div>
            <h3 class="text-lg font-bold text-slate-900">Tambah Mutasi Stok</h3>
            <p class="text-xs text-slate-400 mt-0.5">Catat penambahan atau pengeluaran stok obat baru.</p>
          </div>
          <button @click="isModalOpen = false" class="text-slate-400 hover:text-slate-600 transition">✕</button>
        </div>

        <form @submit.prevent="handleAddStock" class="space-y-4">
          <div>
            <label class="block text-xs font-bold text-slate-500 uppercase tracking-wider">Pilih Produk</label>
            <select v-model="form.product_id" required class="w-full mt-1 px-4 py-2.5 border border-slate-200 rounded-xl bg-white focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500 outline-none text-sm transition">
              <option value="" disabled>-- Pilih Obat dari Master Data --</option>
              <option v-for="p in allProducts" :key="p.id" :value="p.id">
                {{ p.nama_produk }}
              </option>
            </select>
          </div>
          
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-xs font-bold text-slate-500 uppercase tracking-wider">Jenis Mutasi</label>
              <select v-model="form.type" required class="w-full mt-1 px-4 py-2.5 border border-slate-200 rounded-xl bg-white focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500 outline-none text-sm font-bold transition">
                <option value="Masuk">Masuk</option>
                <option value="Keluar">Keluar</option>
              </select>
            </div>
            <div>
              <label class="block text-xs font-bold text-slate-500 uppercase tracking-wider">Jumlah</label>
              <input v-model="form.jumlah" type="number" min="1" required placeholder="Pcs" class="w-full mt-1 px-4 py-2.5 border border-slate-200 rounded-xl focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500 outline-none text-sm transition" />
            </div>
          </div>
          
          <div>
            <label class="block text-xs font-bold text-slate-500 uppercase tracking-wider">Expired Date (Opsional)</label>
            <input v-model="form.expired_date" type="date" class="w-full mt-1 px-4 py-2.5 border border-slate-200 rounded-xl focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500 outline-none text-sm transition" />
          </div>
          
          <div>
            <label class="block text-xs font-bold text-slate-500 uppercase tracking-wider">Deskripsi / Keterangan</label>
            <textarea v-model="form.deskripsi" placeholder="Contoh: Pengadaan rutin distributor atau obat rusak" rows="2" class="w-full mt-1 px-4 py-2.5 border border-slate-200 rounded-xl focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500 outline-none text-sm transition"></textarea>
          </div>

          <div class="flex justify-end gap-2 pt-3 border-t mt-2">
            <button type="button" @click="isModalOpen = false" class="px-4 py-2.5 border border-slate-200 rounded-xl text-slate-600 hover:bg-slate-50 font-semibold text-xs transition">
              Batal
            </button>
            <button type="submit" class="px-5 py-2.5 bg-emerald-600 text-white rounded-xl hover:bg-emerald-700 font-semibold text-xs shadow-md transition">
              Simpan Mutasi
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>