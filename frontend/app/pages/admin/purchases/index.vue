<script setup>
definePageMeta({
  layout: 'sidebar',
  composables: 'useAuth'
})

const config = useRuntimeConfig()
const { token } = useAuth()

// --- STATE UTAMA ---
const isModalOpen = ref(false)
const isEditMode = ref(false)
const editingPurchaseId = ref(null)

const formData = reactive({
  supplier_name: '',
  items: [{ product_id: '', jumlah: 1, harga_satuan: 0 }]
})

// --- STATE PAGINATION ---
const currentPage = ref(1)
const pageSize = ref(10)

// --- FETCH DATA ---
const { data: rawPurchases, pending: purchasesPending, error: purchasesError, refresh: refreshPurchases } = await useFetch(`${config.public.apiBase}/purchase/`, {
  method: 'GET',
  headers: { Authorization: `Bearer ${token.value}` }
})

const { data: rawProducts } = await useFetch(`${config.public.apiBase}/product/`, {
  method: 'GET',
  headers: { Authorization: `Bearer ${token.value}` }
})

// --- MAPPING DATA ---
const allPurchases = computed(() => {
  if (!rawPurchases.value) return []
  return rawPurchases.value.map(p => {
    let detailProdukString = '-'
    let totalQtyNota = 0
    if (p.items && p.items.length > 0) {
      const itemTextArray = p.items.map(item => {
        const nama = item.product?.nama_produk || `Produk ID #${item.product_id}`
        totalQtyNota += item.jumlah
        const hargaFormatted = Number(item.harga_satuan || 0).toLocaleString('id-ID')
        return `${nama} (${item.jumlah}x @Rp ${hargaFormatted})`
      })
      detailProdukString = itemTextArray.join(', ')
    }
    return {
      id_nota: p.id,
      tanggal: p.tanggal,
      supplier_name: p.supplier_name || '-',
      total_harga_nota: p.total_harga,
      jumlah_beli: totalQtyNota,
      produk_display: detailProdukString,
      rawItems: p.items || []
    }
  })
})

// --- PAGINATION ---
const displayedPurchases = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return allPurchases.value.slice(start, end)
})

const handlePageChange = (newPage) => { currentPage.value = newPage }

watch(rawPurchases, () => { currentPage.value = 1 })

// --- MODAL HELPERS ---
const openAddModal = () => {
  isEditMode.value = false
  editingPurchaseId.value = null
  formData.supplier_name = ''
  formData.items = [{ product_id: '', jumlah: 1, harga_satuan: 0 }]
  isModalOpen.value = true
}

const openEditModal = (p) => {
  isEditMode.value = true
  editingPurchaseId.value = p.id_nota
  formData.supplier_name = p.supplier_name === '-' ? '' : p.supplier_name
  formData.items = p.rawItems.map(i => ({
    product_id: i.product_id,
    jumlah: i.jumlah,
    harga_satuan: i.harga_satuan
  }))
  if (formData.items.length === 0) {
    formData.items = [{ product_id: '', jumlah: 1, harga_satuan: 0 }]
  }
  isModalOpen.value = true
}

const closeModal = () => { isModalOpen.value = false }

const addItem = () => {
  formData.items.push({ product_id: '', jumlah: 1, harga_satuan: 0 })
}

const removeItem = (index) => {
  if (formData.items.length > 1) formData.items.splice(index, 1)
}

// --- SUBMIT (Tambah / Edit) ---
const submitPurchase = async () => {
  if (formData.items.some(i => !i.product_id || i.jumlah <= 0 || i.harga_satuan <= 0)) {
    alert('Pastikan semua item memiliki produk, jumlah, dan harga beli yang valid.')
    return
  }
  try {
    const payload = {
      supplier_name: formData.supplier_name,
      items: formData.items.map(i => ({
        product_id: parseInt(i.product_id),
        jumlah: parseInt(i.jumlah),
        harga_satuan: parseFloat(i.harga_satuan)
      }))
    }

    if (isEditMode.value) {
      await $fetch(`${config.public.apiBase}/purchase/${editingPurchaseId.value}`, {
        method: 'PUT',
        headers: { Authorization: `Bearer ${token.value}`, 'Content-Type': 'application/json' },
        body: payload
      })
      alert('Pembelian stok berhasil diperbarui!')
    } else {
      await $fetch(`${config.public.apiBase}/purchase/`, {
        method: 'POST',
        headers: { Authorization: `Bearer ${token.value}`, 'Content-Type': 'application/json' },
        body: payload
      })
      alert('Pembelian stok berhasil dicatat!')
    }

    closeModal()
    refreshPurchases()
  } catch (err) {
    alert(err.data?.detail || 'Terjadi kesalahan saat menyimpan pembelian.')
  }
}

// --- DELETE ---
const deletePurchase = async (id) => {
  if (!confirm('Apakah Anda yakin ingin menghapus pembelian ini? Stok produk akan dikembalikan.')) return
  try {
    await $fetch(`${config.public.apiBase}/purchase/${id}`, {
      method: 'DELETE',
      headers: { Authorization: `Bearer ${token.value}` }
    })
    alert('Pembelian berhasil dihapus dan stok telah dikembalikan.')
    refreshPurchases()
  } catch (err) {
    alert(err.data?.detail || 'Gagal menghapus pembelian.')
  }
}
</script>

<template>
  <div class="space-y-6">
    <!-- HEADER -->
    <div class="flex justify-between items-center">
      <div>
        <h1 class="text-2xl font-bold text-slate-900">Pembelian Stok</h1>
        <p class="text-sm text-slate-500">Kelola dan pantau pembelian obat & alkes dari supplier.</p>
      </div>
      <button @click="openAddModal"
        class="px-4 py-2.5 bg-emerald-600 text-white rounded-xl font-semibold text-sm hover:bg-emerald-700 transition shadow-lg shadow-green-100 flex items-center gap-1.5">
        <Icon name="lucide:plus-circle" class="text-base" />
        Catat Pembelian Stok
      </button>
    </div>

    <!-- MODAL TAMBAH / EDIT -->
    <div v-if="isModalOpen" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4 backdrop-blur-sm">
      <div class="bg-white rounded-2xl shadow-xl w-full max-w-2xl overflow-hidden flex flex-col max-h-[90vh] border border-slate-100">
        <div class="p-6 border-b border-slate-100 flex justify-between items-center bg-slate-50">
          <div>
            <h2 class="text-lg font-bold text-slate-900">{{ isEditMode ? 'Edit Pembelian Stok' : 'Form Pembelian Stok' }}</h2>
            <p class="text-xs text-slate-400 mt-0.5">{{ isEditMode ? 'Perbarui data nota pembelian.' : 'Catat pembelian baru dari supplier.' }}</p>
          </div>
          <button @click="closeModal" class="text-slate-400 hover:text-rose-500 transition">
            <Icon name="lucide:x" class="text-2xl" />
          </button>
        </div>

        <div class="p-6 overflow-y-auto flex-1 space-y-4">
          <div>
            <label class="block text-xs font-bold text-slate-500 uppercase tracking-wider mb-1">Nama Supplier (Opsional)</label>
            <input v-model="formData.supplier_name" type="text"
              class="w-full border border-slate-200 rounded-xl px-4 py-2.5 outline-none focus:ring-2 focus:ring-indigo-500 text-sm bg-white"
              placeholder="PT. Kimia Farma" />
          </div>

          <div class="space-y-3">
            <label class="block text-xs font-bold text-slate-500 uppercase tracking-wider">Daftar Item Pasokan</label>
            <div v-for="(item, index) in formData.items" :key="index"
              class="flex flex-col md:flex-row gap-3 items-end bg-slate-50 p-4 rounded-xl border border-slate-200/60 relative">

              <div class="w-full md:flex-1">
                <label class="block text-[11px] font-bold text-slate-500 uppercase tracking-wider mb-1">Produk</label>
                <select v-model="item.product_id"
                  class="w-full border border-slate-200 rounded-xl px-3 py-2.5 bg-white outline-none focus:ring-2 focus:ring-indigo-500 text-sm">
                  <option disabled value="">Pilih Produk</option>
                  <option v-for="p in rawProducts" :key="p.id" :value="p.id">
                    {{ p.nama_produk }} (Stok: {{ p.stok_saat_ini }})
                  </option>
                </select>
              </div>

              <div class="w-full md:w-24">
                <label class="block text-[11px] font-bold text-slate-500 uppercase tracking-wider mb-1">Jumlah</label>
                <input v-model="item.jumlah" type="number" min="1"
                  class="w-full border border-slate-200 rounded-xl px-3 py-2.5 bg-white outline-none focus:ring-2 focus:ring-indigo-500 text-sm" />
              </div>

              <div class="w-full md:flex-1">
                <label class="block text-[11px] font-bold text-slate-500 uppercase tracking-wider mb-1">Harga Beli Satuan (Rp)</label>
                <input v-model="item.harga_satuan" type="number" min="0"
                  class="w-full border border-slate-200 rounded-xl px-3 py-2.5 bg-white outline-none focus:ring-2 focus:ring-indigo-500 text-sm"
                  placeholder="Rp" />
              </div>

              <button @click="removeItem(index)" v-if="formData.items.length > 1"
                class="p-2.5 text-rose-500 hover:bg-rose-50 rounded-xl border border-slate-200 bg-white transition shrink-0">
                <Icon name="lucide:trash-2" class="text-lg" />
              </button>
            </div>

            <button type="button" @click="addItem"
              class="text-xs font-bold text-emerald-600 hover:text-emerald-800 flex items-center gap-1">
              <Icon name="lucide:plus-circle" class="text-base" /> Tambah Item Lain
            </button>
          </div>
        </div>

        <div class="p-6 border-t border-slate-100 bg-slate-50 flex justify-end gap-3">
          <button @click="closeModal"
            class="px-5 py-2.5 text-slate-600 font-semibold text-sm hover:bg-slate-200 rounded-xl transition">
            Batal
          </button>
          <button @click="submitPurchase"
            class="px-5 py-2.5 bg-emerald-600 text-white font-bold text-sm hover:bg-emerald-700 rounded-xl transition shadow-lg shadow-emerald-100">
            {{ isEditMode ? 'Simpan Perubahan' : 'Simpan Pembelian' }}
          </button>
        </div>
      </div>
    </div>

    <!-- LOADING -->
    <div v-if="purchasesPending" class="text-center py-12 text-slate-500">
      <p class="animate-pulse font-medium text-sm">Sedang memuat data pembelian...</p>
    </div>

    <!-- ERROR -->
    <div v-else-if="purchasesError" class="bg-rose-50 text-rose-600 p-4 rounded-xl border border-rose-100 text-sm">
      Gagal memuat data: {{ purchasesError.message || 'Terjadi kesalahan pada server.' }}
    </div>

    <!-- TABLE + PAGINATION -->
    <div v-else class="space-y-4">
      <div class="bg-white rounded-2xl border border-slate-200 overflow-hidden shadow-sm">
        <table class="w-full text-left border-collapse">
          <thead class="bg-slate-50 border-b border-slate-200">
            <tr>
              <th class="p-4 text-xs font-bold text-slate-500 uppercase tracking-wider">ID Nota</th>
              <th class="p-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Supplier</th>
              <th class="p-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Daftar Produk & Harga Pasok</th>
              <th class="p-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Total Qty</th>
              <th class="p-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Total Nota</th>
              <th class="p-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Tanggal</th>
              <th class="p-4 text-xs font-bold text-slate-500 uppercase tracking-wider text-center">Aksi</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100 text-sm text-slate-700">
            <tr v-for="p in displayedPurchases" :key="p.id_nota" class="hover:bg-slate-50/80 transition">
              <td class="p-4 font-mono text-xs text-slate-500">#PRC-{{ p.id_nota }}</td>
              <td class="p-4 font-semibold text-slate-700">{{ p.supplier_name }}</td>
              <td class="p-4 text-slate-900 font-medium max-w-md leading-relaxed">{{ p.produk_display }}</td>
              <td class="p-4 font-medium text-slate-800">{{ p.jumlah_beli }} Pcs</td>
              <td class="p-4 font-bold text-green-600">Rp {{ Number(p.total_harga_nota).toLocaleString('id-ID') }}</td>
              <td class="p-4 text-slate-500 font-mono text-xs">
                {{ p.tanggal ? new Date(p.tanggal).toLocaleString('id-ID') : '-' }}
              </td>
              <td class="p-4 text-center">
                <div class="flex justify-center items-center gap-2">
                  <button @click="openEditModal(p)" class="p-2 text-indigo-600 hover:bg-indigo-50 rounded-lg transition" title="Edit">
                    <Icon name="lucide:edit" class="text-lg" />
                  </button>
                  <button @click="deletePurchase(p.id_nota)" class="p-2 text-rose-600 hover:bg-rose-50 rounded-lg transition" title="Hapus">
                    <Icon name="lucide:trash-2" class="text-lg" />
                  </button>
                </div>
              </td>
            </tr>

            <tr v-if="!displayedPurchases.length">
              <td colspan="7" class="p-8 text-center text-slate-400">Tidak ada riwayat pembelian stok.</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- PAGINATION -->
      <div v-if="allPurchases.length > 0" class="flex justify-end bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
        <Pagination
          :totalItems="allPurchases.length"
          :pageSize="pageSize"
          :currentPage="currentPage"
          @page-changed="handlePageChange"
        />
      </div>
    </div>
  </div>
</template>