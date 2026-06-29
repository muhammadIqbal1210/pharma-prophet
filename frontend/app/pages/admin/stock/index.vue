<script setup>
definePageMeta({
  layout: 'sidebar',
  composables: 'useAuth'
})

const config = useRuntimeConfig()
const { token } = useAuth()

// --- STATE MODAL & FORM ---
const isModalOpen = ref(false)
const isEditMode = ref(false)
const editingStockId = ref(null)

const form = ref({
  product_id: '',
  type: 'Masuk',
  jumlah: '',
  expired_date: '',
  deskripsi: ''
})

// --- FETCH DATA ---
const { data: rawStock, pending: stockPending, error: stockError, refresh } = await useFetch(`${config.public.apiBase}/stock/`, {
  method: 'GET',
  headers: { Authorization: `Bearer ${token.value}` }
})

const { data: allProducts } = await useFetch(`${config.public.apiBase}/product/`, {
  method: 'GET',
  headers: { Authorization: `Bearer ${token.value}` }
})

// --- COMPUTED: gabungkan dengan nama produk ---
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

// --- STATE PAGINATION ---
const currentPage = ref(1)
const pageSize = ref(10)

const displayedStock = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return combinedStocks.value.slice(start, end)
})

const handleStockPageChange = (newPage) => {
  currentPage.value = newPage
}

watch(rawStock, () => {
  currentPage.value = 1
})

// --- MODAL HELPERS ---
const openAddModal = () => {
  isEditMode.value = false
  editingStockId.value = null
  form.value = { product_id: '', type: 'Masuk', jumlah: '', expired_date: '', deskripsi: '' }
  isModalOpen.value = true
}

const openEditModal = (item) => {
  isEditMode.value = true
  editingStockId.value = item.id
  form.value = {
    product_id: item.product_id,
    type: item.type,
    jumlah: item.jumlah,
    expired_date: item.expired_date ? item.expired_date.split('T')[0] : '',
    deskripsi: item.deskripsi || ''
  }
  isModalOpen.value = true
}

const closeModal = () => {
  isModalOpen.value = false
}

// --- AKSI: SIMPAN (Tambah / Edit) ---
const handleSubmitStock = async () => {
  try {
    const payload = {
      ...form.value,
      product_id: Number(form.value.product_id),
      jumlah: Number(form.value.jumlah),
      expired_date: form.value.expired_date || null
    }

    if (isEditMode.value) {
      await $fetch(`${config.public.apiBase}/stock/${editingStockId.value}`, {
        method: 'PUT',
        headers: { Authorization: `Bearer ${token.value}`, 'Content-Type': 'application/json' },
        body: payload
      })
      alert('Data mutasi stok berhasil diperbarui!')
    } else {
      await $fetch(`${config.public.apiBase}/stock/`, {
        method: 'POST',
        headers: { Authorization: `Bearer ${token.value}`, 'Content-Type': 'application/json' },
        body: payload
      })
      alert('Data mutasi stok berhasil ditambahkan!')
    }

    closeModal()
    refresh()
  } catch (error) {
    const rawDetail = error.response?._data?.detail
    const errorMessage = Array.isArray(rawDetail) ? rawDetail[0]?.msg : rawDetail || error.message
    alert('Gagal menyimpan stok: ' + errorMessage)
  }
}

// --- AKSI: HAPUS ---
const deleteStock = async (id) => {
  if (!confirm('Apakah Anda yakin ingin menghapus data log stok ini?')) return
  try {
    await $fetch(`${config.public.apiBase}/stock/${id}/`, {
      method: 'DELETE',
      headers: { Authorization: `Bearer ${token.value}` }
    })
    alert('Data riwayat stok berhasil dihapus.')
    refresh()
  } catch (err) {
    alert(err.data?.detail || 'Gagal menghapus data stok.')
  }
}
</script>

<template>
  <div class="space-y-6">
    <!-- HEADER -->
    <div class="flex justify-between items-center">
      <div>
        <h1 class="text-2xl font-bold text-slate-900">Riwayat Stok Produk</h1>
        <p class="text-sm text-slate-500">Pantau perubahan stok produk dari waktu ke waktu.</p>
      </div>
      <button @click="openAddModal" class="px-4 py-2.5 bg-emerald-600 text-white font-semibold rounded-xl hover:bg-emerald-700 transition text-sm flex items-center gap-1.5 shadow-sm">
        <Icon name="lucide:pill" class="text-base" />
        Tambah Stok
      </button>
    </div>

    <!-- LOADING -->
    <div v-if="stockPending" class="text-center py-12 text-slate-500">
      <p class="animate-pulse font-medium text-sm">Sedang memuat data dari server...</p>
    </div>

    <!-- ERROR -->
    <div v-else-if="stockError" class="bg-rose-50 text-rose-600 p-4 rounded-xl border border-rose-100 text-sm">
      Gagal memuat data: {{ stockError.message || 'Terjadi kesalahan pada server.' }}
    </div>

    <!-- TABLE + PAGINATION -->
    <div v-else class="space-y-4">
      <div class="bg-white rounded-2xl border border-slate-200 overflow-hidden shadow-sm">
        <table class="w-full text-left border-collapse">
          <thead class="bg-slate-50 border-b border-slate-200">
            <tr>
              <th class="p-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Nama Produk</th>
              <th class="p-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Tipe</th>
              <th class="p-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Jumlah</th>
              <th class="p-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Expired Date</th>
              <th class="p-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Deskripsi</th>
              <th class="p-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Tanggal Update</th>
              <th class="p-4 text-xs font-bold text-slate-500 uppercase tracking-wider text-center">Aksi</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100 text-sm text-slate-700">
            <tr v-for="item in displayedStock" :key="item.id" class="hover:bg-slate-50/80 transition">
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
              <td class="p-4 text-center">
                <div class="flex justify-center items-center gap-2">
                  <button @click="openEditModal(item)" class="p-2 text-indigo-600 hover:bg-indigo-50 rounded-lg transition" title="Edit">
                    <Icon name="lucide:edit" class="text-lg" />
                  </button>
                  <button @click="deleteStock(item.id)" class="p-2 text-rose-600 hover:bg-rose-50 rounded-lg transition" title="Hapus">
                    <Icon name="lucide:trash-2" class="text-lg" />
                  </button>
                </div>
              </td>
            </tr>

            <tr v-if="!displayedStock.length">
              <td colspan="7" class="p-8 text-center text-slate-400">Tidak ada data stok yang ditemukan.</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- PAGINATION -->
      <div v-if="combinedStocks.length > 0" class="flex justify-end bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
        <Pagination
          :totalItems="combinedStocks.length"
          :pageSize="pageSize"
          :currentPage="currentPage"
          @page-changed="handleStockPageChange"
        />
      </div>
    </div>

    <!-- MODAL TAMBAH / EDIT STOK -->
    <div v-if="isModalOpen" class="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/50 backdrop-blur-sm p-4">
      <div class="bg-white w-full max-w-md rounded-2xl shadow-xl p-6 border border-slate-100 space-y-4">

        <div class="flex justify-between items-center border-b pb-3">
          <div>
            <h3 class="text-lg font-bold text-slate-900">{{ isEditMode ? 'Edit Mutasi Stok' : 'Tambah Mutasi Stok' }}</h3>
            <p class="text-xs text-slate-400 mt-0.5">{{ isEditMode ? 'Perbarui data mutasi stok.' : 'Catat penambahan atau pengeluaran stok obat baru.' }}</p>
          </div>
          <button @click="closeModal" class="text-slate-400 hover:text-slate-600 transition text-xl leading-none">✕</button>
        </div>

        <form @submit.prevent="handleSubmitStock" class="space-y-4">
          <div>
            <label class="block text-xs font-bold text-slate-500 uppercase tracking-wider">Pilih Produk</label>
            <select v-model="form.product_id" required :disabled="isEditMode"
              class="w-full mt-1 px-4 py-2.5 border border-slate-200 rounded-xl bg-white focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500 outline-none text-sm transition disabled:bg-slate-50 disabled:text-slate-400">
              <option value="" disabled>-- Pilih Obat dari Master Data --</option>
              <option v-for="p in allProducts" :key="p.id" :value="p.id">
                {{ p.nama_produk }}
              </option>
            </select>
            <p v-if="isEditMode" class="text-[10px] text-slate-400 mt-1">Produk tidak dapat diubah saat mengedit.</p>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-xs font-bold text-slate-500 uppercase tracking-wider">Jenis Mutasi</label>
              <select v-model="form.type" required
                class="w-full mt-1 px-4 py-2.5 border border-slate-200 rounded-xl bg-white focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500 outline-none text-sm font-bold transition">
                <option value="Masuk">Masuk</option>
                <option value="Keluar">Keluar</option>
              </select>
            </div>
            <div>
              <label class="block text-xs font-bold text-slate-500 uppercase tracking-wider">Jumlah</label>
              <input v-model="form.jumlah" type="number" min="1" required placeholder="Pcs"
                class="w-full mt-1 px-4 py-2.5 border border-slate-200 rounded-xl focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500 outline-none text-sm transition bg-white" />
            </div>
          </div>

          <div>
            <label class="block text-xs font-bold text-slate-500 uppercase tracking-wider">Expired Date (Opsional)</label>
            <input v-model="form.expired_date" type="date"
              class="w-full mt-1 px-4 py-2.5 border border-slate-200 rounded-xl focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500 outline-none text-sm transition bg-white" />
          </div>

          <div>
            <label class="block text-xs font-bold text-slate-500 uppercase tracking-wider">Deskripsi / Keterangan</label>
            <textarea v-model="form.deskripsi" placeholder="Contoh: Pengadaan rutin distributor atau obat rusak" rows="2"
              class="w-full mt-1 px-4 py-2.5 border border-slate-200 rounded-xl focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500 outline-none text-sm transition bg-white"></textarea>
          </div>

          <div class="flex justify-end gap-2 pt-3 border-t mt-2">
            <button type="button" @click="closeModal"
              class="px-4 py-2.5 border border-slate-200 rounded-xl text-slate-600 hover:bg-slate-50 font-semibold text-xs transition">
              Batal
            </button>
            <button type="submit"
              class="px-5 py-2.5 bg-emerald-600 text-white rounded-xl hover:bg-emerald-700 font-semibold text-xs shadow-md transition">
              {{ isEditMode ? 'Simpan Perubahan' : 'Simpan Mutasi' }}
            </button>
          </div>
        </form>
      </div>
    </div>

  </div>
</template>