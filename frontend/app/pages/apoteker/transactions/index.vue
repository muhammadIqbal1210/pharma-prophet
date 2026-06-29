<script setup>
definePageMeta({
  layout: 'sidebar', // Menggunakan layouts/sidebar.vue
  composables: 'useAuth'    // Menggunakan middleware/auth.ts
})

const config = useRuntimeConfig()
const { currentUser, token } = useAuth()

// --- STATE UTAMA ---
const isModalOpen = ref(false)

// Struktur data form transaksi disesuaikan dengan skema bersarang (nested) FastAPI
const form = ref({
  total_harga: 0,
  items: [
    { product_id: '', jumlah: 1, harga_satuan: 0 }
  ]
})

// --- FETCH DATA ---
// 1. Ambil data riwayat transaksi
const { data: rawTransactions, pending: transactionsPending, error: transactionsError, refresh } = await useFetch(`${config.public.apiBase}/transaction/`, {
  method: 'GET',
  headers: {
    Authorization: `Bearer ${token.value}`
  }
})

// 2. Ambil master produk untuk pilihan dropdown di form & mencari harga satuan otomatis
const { data: allProducts } = await useFetch(`${config.public.apiBase}/product/`, {
  method: 'GET',
  headers: {
    Authorization: `Bearer ${token.value}`
  }
})


// --- MAPPING TABEL (Satu ID Nota = Satu Baris) ---
const transactions = computed(() => {
  if (!rawTransactions.value) return []

  return rawTransactions.value.map(t => {
    let detailProdukString = '-'
    let totalQtyNota = 0

    if (t.items && t.items.length > 0) {
      // Petakan setiap item menjadi format "Nama Produk (Qty x @Rp Harga)"
      const itemTextArray = t.items.map(item => {
        const nama = item.product?.nama_produk || `Produk ID #${item.product_id}`
        totalQtyNota += item.jumlah // Akumulasi total kuantitas per nota
        
        // Format harga ke rupiah tanpa desimal panjang
        const hargaFormatted = Number(item.harga_satuan).toLocaleString('id-ID')
        
        return `${nama} (${item.jumlah}x @Rp ${hargaFormatted})`
      })
      
      // Gabungkan menjadi string: "Paracetamol 500 Mg (4x @Rp 10.000), Amoxilin (4x @Rp 10.000)"
      detailProdukString = itemTextArray.join(', ')
    }

    return {
      id_nota: t.id,
      tanggal: t.tanggal,
      total_harga_nota: t.total_harga,
      jumlah_beli: totalQtyNota,
      produk_display: detailProdukString,
      items_raw: t.items || [] // Disimpan jika nanti ingin render komponen badge/pill manual
    }
  })
})

// --- LOGIKA FORM DINAMIS (MANIPULASI ITEM) ---
const addItem = () => {
  form.value.items.push({ product_id: '', jumlah: 1, harga_satuan: 0 })
}

const removeItem = (index) => {
  if (form.value.items.length > 1) {
    form.value.items.splice(index, 1)
  }
}

// Otomatis update harga satuan saat produk dipilih di dropdown
const handleProductChange = (index) => {
  const selectedProdId = form.value.items[index].product_id
  const product = allProducts.value?.find(p => p.id === Number(selectedProdId))
  if (product) {
    form.value.items[index].harga_satuan = Number(product.harga_jual || product.harga || 0)
  }
}

// Hitung total harga keseluruhan nota secara reaktif
watch(() => form.value.items, (newItems) => {
  form.value.total_harga = newItems.reduce((acc, item) => {
    return acc + (Number(item.jumlah) * Number(item.harga_satuan))
  }, 0)
}, { deep: true })

// --- AKSI: SIMPAN TRANSAKSI KE SERVER ---
const handleSaveTransaction = async () => {
  try {
    const payload = {
      tanggal: new Date().toISOString(),
      total_harga: Number(form.value.total_harga),
      items: form.value.items.map(item => ({
        product_id: Number(item.product_id),
        jumlah: Number(item.jumlah),
        harga_satuan: Number(item.harga_satuan)
      }))
    }

    await $fetch(`${config.public.apiBase}/transaction/`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token.value}`,
        'Content-Type': 'application/json'
      },
      body: payload
    })

    alert('Transaksi penjualan berhasil dicatat!')
    
    // Reset state & form
    form.value = { total_harga: 0, items: [{ product_id: '', jumlah: 1, harga_satuan: 0 }] }
    isModalOpen.value = false
    refresh()
  } catch (error) {
    const rawDetail = error.response?._data?.detail
    const errorMessage = Array.isArray(rawDetail) ? rawDetail[0]?.msg : rawDetail || error.message
    alert('Gagal menyimpan transaksi: ' + errorMessage)
  }
}
</script>

<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <div>
        <h1 class="text-2xl font-bold text-slate-900">Manajemen Transaksi</h1>
        <p class="text-sm text-slate-500">Kelola dan pantau data transaksi penjualan obat apotek.</p>
      </div>
      <button @click="isModalOpen = true" class="px-4 py-2.5 bg-emerald-600 text-white font-semibold rounded-xl hover:bg-emerald-700 transition text-sm flex items-center gap-1.5 shadow-sm">
        <Icon name="lucide:plus-circle" class="text-base" />
        Catat Transaksi Baru
      </button>
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

    <div v-if="isModalOpen" class="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/50 backdrop-blur-sm p-4">
      <div class="bg-white w-full max-w-2xl rounded-2xl shadow-xl flex flex-col max-h-[90vh] border border-slate-100 animate-fade-in">
        
        <div class="p-6 border-b flex justify-between items-center">
          <div>
            <h3 class="text-lg font-bold text-slate-900">Catat Penjualan Obat Baru</h3>
            <p class="text-xs text-slate-400 mt-0.5">Input list resep/obat yang dibeli oleh pasien saat ini.</p>
          </div>
          <button @click="isModalOpen = false" class="text-slate-400 hover:text-slate-600 text-lg">✕</button>
        </div>

        <div class="p-6 overflow-y-auto space-y-4 flex-1">
          <div v-for="(item, index) in form.items" :key="index" class="p-4 bg-slate-50 rounded-xl border border-slate-200/60 relative space-y-3">
            
            <button v-if="form.items.length > 1" type="button" @click="removeItem(index)" class="absolute top-3 right-3 text-rose-500 hover:text-rose-700 text-xs font-bold transition">
              Hapus Item
            </button>

            <span class="inline-block px-2 py-0.5 bg-slate-200 text-slate-700 font-mono text-[10px] font-bold rounded">
              Item #{{ index + 1 }}
            </span>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
              <div class="md:col-span-1">
                <label class="block text-[11px] font-bold text-slate-500 uppercase tracking-wider">Pilih Produk</label>
                <select v-model="item.product_id" @change="handleProductChange(index)" required class="w-full mt-1 px-3 py-2 border border-slate-200 rounded-xl bg-white text-sm outline-none transition focus:border-emerald-500">
                  <option value="" disabled>-- Pilih Obat --</option>
                  <option v-for="p in allProducts" :key="p.id" :value="p.id">
                    {{ p.nama_produk }}
                  </option>
                </select>
              </div>

              <div>
                <label class="block text-[11px] font-bold text-slate-500 uppercase tracking-wider">Jumlah Beli</label>
                <input v-model="item.jumlah" type="number" min="1" required placeholder="Pcs" class="w-full mt-1 px-3 py-2 border border-slate-200 rounded-xl text-sm outline-none transition focus:border-emerald-500" />
              </div>

              <div>
                <label class="block text-[11px] font-bold text-slate-500 uppercase tracking-wider">Harga Satuan (Rp)</label>
                <input v-model="item.harga_satuan" type="number" readonly class="w-full mt-1 px-3 py-2 border border-slate-200 rounded-xl bg-slate-100 text-slate-500 text-sm font-semibold outline-none cursor-not-allowed" />
              </div>
            </div>
          </div>

          <button type="button" @click="addItem" class="w-full py-2.5 border border-dashed border-slate-300 text-slate-500 hover:text-emerald-600 hover:border-emerald-500 rounded-xl text-xs font-bold transition flex items-center justify-center gap-1">
            <Icon name="lucide:plus" class="text-sm" /> Tambah Item Obat Lain
          </button>
        </div>

        <div class="p-6 border-t bg-slate-50/50 flex flex-col sm:flex-row justify-between items-center gap-4">
          <div class="text-left w-full sm:w-auto">
            <p class="text-xs font-semibold text-slate-400 uppercase tracking-wider">Total Nilai Nota</p>
            <h3 class="text-xl font-bold text-emerald-600">Rp {{ form.total_harga.toLocaleString('id-ID') }}</h3>
          </div>
          
          <div class="flex gap-2 w-full sm:w-auto justify-end">
            <button type="button" @click="isModalOpen = false" class="px-4 py-2.5 border border-slate-200 rounded-xl text-slate-600 hover:bg-slate-50 font-semibold text-xs transition">
              Batal
            </button>
            <button @click="handleSaveTransaction" type="button" class="px-5 py-2.5 bg-emerald-600 text-white rounded-xl hover:bg-emerald-700 font-semibold text-xs shadow-md transition">
              Simpan & Cetak Nota
            </button>
          </div>
        </div>

      </div>
    </div>

  </div>
</template>