<script setup>
definePageMeta({
  layout: 'sidebar', // Menggunakan layouts/sidebar.vue
  composables: 'useAuth'    // Menggunakan middleware/auth.ts
})

const config = useRuntimeConfig()
const { currentUser, token } = useAuth()

// --- STATE EDIT MODAL ---
const isEditModalOpen = ref(false)
const editingTransactionId = ref(null)
const formData = reactive({
  items: [
    { product_id: '', jumlah: 1 }
  ]
})

// --- STATE PAGINATION ---
const currentPage = ref(1)
const pageSize = ref(10) // Batas data per halaman

// 1. Ambil data transaksi langsung dari backend FastAPI
const { data: rawTransactions, pending: transactionsPending, error: transactionsError, refresh: refreshTransactions } = await useFetch(`${config.public.apiBase}/transaction/`, {
  method: 'GET',
  headers: {
    Authorization: `Bearer ${token.value}`
  }
})

// 2. Ambil master produk untuk pilihan dropdown di form modal edit
const { data: rawProducts } = await useFetch(`${config.public.apiBase}/product/`, {
  method: 'GET',
  headers: {
    Authorization: `Bearer ${token.value}`
  }
})

// 3. Mapping data asal secara utuh (Semua Transaksi)
const allTransactions = computed(() => {
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

// 4. Memotong data (slicing) untuk ditampilkan di tabel saat ini
const transactions = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return allTransactions.value.slice(start, end)
})

// Pembalas emit ketika tombol angka halaman diklik
const handlePageChange = (newPage) => {
  currentPage.value = newPage
}

// Reset halaman ke 1 jika data diperbarui
watch(rawTransactions, () => {
  currentPage.value = 1
})

// --- LOGIKA EDIT & HAPUS ---
const openEditModal = (tx) => {
  editingTransactionId.value = tx.id_nota
  const originalTx = rawTransactions.value.find(t => t.id === tx.id_nota)
  if (originalTx) {
    formData.items = originalTx.items.map(item => ({
      product_id: item.product_id,
      jumlah: item.jumlah
    }))
    isEditModalOpen.value = true
  }
}

const addItem = () => {
  formData.items.push({ product_id: '', jumlah: 1 })
}

const removeItem = (index) => {
  if (formData.items.length > 1) {
    formData.items.splice(index, 1)
  }
}

const submitEditTransaction = async () => {
  try {
    if (formData.items.some(i => !i.product_id || i.jumlah <= 0)) {
      alert("Pastikan semua item memiliki produk dan jumlah yang valid")
      return
    }

    const payload = {
      items: formData.items.map(i => ({
        product_id: parseInt(i.product_id),
        jumlah: parseInt(i.jumlah)
      }))
    }

    await $fetch(`${config.public.apiBase}/transaction/${editingTransactionId.value}`, {
      method: 'PUT',
      headers: {
        Authorization: `Bearer ${token.value}`,
        'Content-Type': 'application/json'
      },
      body: payload
    })

    isEditModalOpen.value = false
    refreshTransactions()
    alert('Transaksi berhasil diperbarui!')
  } catch (err) {
    alert(err.data?.detail || 'Terjadi kesalahan saat memperbarui transaksi')
  }
}

const deleteTransaction = async (id) => {
  if (!confirm('Apakah Anda yakin ingin menghapus transaksi ini? Tindakan ini akan mengembalikan stok produk.')) {
    return
  }
  try {
    await $fetch(`${config.public.apiBase}/transaction/${id}`, {
      method: 'DELETE',
      headers: {
        Authorization: `Bearer ${token.value}`
      }
    })
    refreshTransactions()
    alert('Transaksi berhasil dihapus!')
  } catch (err) {
    alert(err.data?.detail || 'Terjadi kesalahan saat menghapus transaksi')
  }
}
</script>

<template>
  <div class="space-y-6">
    <div>
      <h1 class="text-2xl font-bold text-slate-900">Manajemen Transaksi</h1>
      <p class="text-sm text-slate-500">Kelola dan pantau data transaksi penjualan obat apotek.</p>
    </div>

    <!-- Modal Edit Transaksi -->
    <div v-if="isEditModalOpen" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4 backdrop-blur-sm">
      <div class="bg-white rounded-2xl shadow-xl w-full max-w-2xl overflow-hidden flex flex-col max-h-[90vh] border border-slate-100">
        <div class="p-6 border-b border-slate-100 flex justify-between items-center bg-slate-50">
          <h2 class="text-lg font-bold text-slate-900">Form Edit Transaksi #TRX-{{ editingTransactionId }}</h2>
          <button @click="isEditModalOpen = false" class="text-slate-400 hover:text-rose-500 transition">
            <Icon name="lucide:x" class="text-2xl" />
          </button>
        </div>
        
        <div class="p-6 overflow-y-auto flex-1 space-y-4">
          <div class="space-y-4">
            <label class="block text-xs font-bold text-slate-500 uppercase tracking-wider">Daftar Item Transaksi</label>
            <div v-for="(item, index) in formData.items" :key="index" class="flex flex-col md:flex-row gap-3 items-end bg-slate-50 p-4 rounded-xl border border-slate-200/60 relative">
              
              <div class="w-full md:flex-1">
                <label class="block text-[11px] font-bold text-slate-500 uppercase tracking-wider mb-1">Produk</label>
                <select v-model="item.product_id" class="w-full border border-slate-200 rounded-xl px-3 py-2.5 bg-white outline-none focus:ring-2 focus:ring-indigo-500 text-sm">
                  <option disabled value="">Pilih Produk</option>
                  <option v-for="p in rawProducts" :key="p.id" :value="p.id">
                    {{ p.nama_produk }} (Stok: {{ p.stok_saat_ini }})
                  </option>
                </select>
              </div>

              <div class="w-full md:w-32">
                <label class="block text-[11px] font-bold text-slate-500 uppercase tracking-wider mb-1">Jumlah</label>
                <input v-model="item.jumlah" type="number" min="1" class="w-full border border-slate-200 rounded-xl px-3 py-2.5 bg-white outline-none focus:ring-2 focus:ring-indigo-500 text-sm" />
              </div>

              <button @click="removeItem(index)" v-if="formData.items.length > 1" class="p-2.5 text-rose-500 hover:bg-rose-50 rounded-xl border border-slate-200 bg-white transition shrink-0">
                <Icon name="lucide:trash-2" class="text-lg" />
              </button>
            </div>
            
            <button type="button" @click="addItem" class="text-xs font-bold text-emerald-600 hover:text-emerald-800 flex items-center gap-1">
              <Icon name="lucide:plus-circle" class="text-base" /> Tambah Item Lain
            </button>
          </div>
        </div>

        <div class="p-6 border-t border-slate-100 bg-slate-50 flex justify-end gap-3">
          <button @click="isEditModalOpen = false" class="px-5 py-2.5 text-slate-600 font-semibold text-sm hover:bg-slate-200 rounded-xl transition">Batal</button>
          <button @click="submitEditTransaction" class="px-5 py-2.5 bg-emerald-600 text-white font-bold text-sm hover:bg-emerald-700 rounded-xl transition shadow-lg shadow-emerald-100">
            Simpan Perubahan
          </button>
        </div>
      </div>
    </div>

    <!-- MAIN DATA VIEW -->
    <div v-if="transactionsPending" class="text-center py-12 text-slate-500">
      <p class="animate-pulse font-medium text-sm">Sedang memuat data transaksi...</p>
    </div>

    <div v-else-if="transactionsError" class="bg-rose-50 text-rose-600 p-4 rounded-xl border border-rose-100 text-sm">
      Gagal memuat data: {{ transactionsError.message || 'Terjadi kesalahan pada server.' }}
    </div>

    <div v-else class="space-y-4">
      <div class="bg-white rounded-2xl border border-slate-200 overflow-hidden shadow-sm">
        <table class="w-full text-left border-collapse">
          <thead class="bg-slate-50 border-b border-slate-200">
            <tr>
              <th class="p-4 text-xs font-bold text-slate-500 uppercase tracking-wider">ID Nota</th>
              <th class="p-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Daftar Produk & Harga Satuan</th>
              <th class="p-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Total Qty</th>
              <th class="p-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Total Nota</th>
              <th class="p-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Tanggal Transaksi</th>
              <th class="p-4 text-xs font-bold text-slate-500 uppercase tracking-wider text-center">Aksi</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100 text-sm text-slate-700">
            <!-- Render data dari computed 'transactions' (data yang sudah di-slice) -->
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

              <td class="p-4 text-center">
                <div class="flex justify-center items-center gap-2">
                  <button @click="openEditModal(tx)" class="p-2 text-indigo-600 hover:bg-indigo-50 rounded-lg transition" title="Edit Transaksi">
                    <Icon name="lucide:edit" class="text-lg" />
                  </button>
                  <button @click="deleteTransaction(tx.id_nota)" class="p-2 text-rose-600 hover:bg-rose-50 rounded-lg transition" title="Hapus Transaksi">
                    <Icon name="lucide:trash-2" class="text-lg" />
                  </button>
                </div>
              </td>
            </tr>

            <tr v-if="!transactions.length">
              <td colspan="6" class="p-8 text-center text-slate-400">Tidak ada riwayat transaksi penjualan obat.</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- NAVIGASI PAGINATION -->
      <div v-if="allTransactions.length > 0" class="flex justify-end bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
        <Pagination 
          :totalItems="allTransactions.length" 
          :pageSize="pageSize" 
          :currentPage="currentPage"
          @page-changed="handlePageChange"
        />
      </div>
    </div>
  </div>
</template>