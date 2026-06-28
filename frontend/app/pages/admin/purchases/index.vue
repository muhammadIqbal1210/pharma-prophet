<script setup>
definePageMeta({
  layout: 'sidebar',
  composables: 'useAuth'
})

const config = useRuntimeConfig()
const { currentUser } = useAuth()

// --- STATE UTAMA ---
const isModalOpen = ref(false)
const formData = reactive({
  supplier_name: '',
  items: [
    { product_id: '', jumlah: 1, harga_satuan: 0 }
  ]
})

// --- FETCH DATA ---
// 1. Ambil data pembelian dari backend FastAPI
const { data: rawPurchases, pending: purchasesPending, error: purchasesError, refresh: refreshPurchases } = await useFetch(`${config.public.apiBase}/purchase/`, {
  method: 'GET',
  headers: {
    Authorization: `Bearer ${currentUser.value?.token}`
  }
})

// 2. Ambil master produk untuk pilihan dropdown di form modal
const { data: rawProducts } = await useFetch(`${config.public.apiBase}/product/`, {
  method: 'GET',
  headers: {
    Authorization: `Bearer ${currentUser.value?.token}`
  }
})

// --- MAPPING TABEL (Satu ID Nota = Satu Baris) ---
const purchases = computed(() => {
  if (!rawPurchases.value) return []

  return rawPurchases.value.map(p => {
    let detailProdukString = '-'
    let totalQtyNota = 0

    if (p.items && p.items.length > 0) {
      // Petakan setiap item menjadi format "Nama Produk (Qty x @Rp Harga)"
      const itemTextArray = p.items.map(item => {
        const nama = item.product?.nama_produk || `Produk ID #${item.product_id}`
        totalQtyNota += item.jumlah // Akumulasi total kuantitas per nota pasokan
        
        // Format harga beli satuan ke rupiah
        const hargaBeliFormatted = Number(item.harga_satuan || 0).toLocaleString('id-ID')
        
        return `${nama} (${item.jumlah}x @Rp ${hargaBeliFormatted})`
      })
      
      // Gabungkan array menjadi satu string terpisah koma
      detailProdukString = itemTextArray.join(', ')
    }

    return {
      id_nota: p.id,
      tanggal: p.tanggal,
      supplier_name: p.supplier_name || '-',
      total_harga_nota: p.total_harga,
      jumlah_beli: totalQtyNota,
      produk_display: detailProdukString
    }
  })
})

// --- LOGIKA FORM MODAL ---
const openModal = () => {
  formData.supplier_name = ''
  formData.items = [{ product_id: '', jumlah: 1, harga_satuan: 0 }]
  isModalOpen.value = true
}

const addItem = () => {
  formData.items.push({ product_id: '', jumlah: 1, harga_satuan: 0 })
}

const removeItem = (index) => {
  if (formData.items.length > 1) {
    formData.items.splice(index, 1)
  }
}

const submitPurchase = async () => {
  try {
    // Validasi input form
    if(formData.items.some(i => !i.product_id || i.jumlah <= 0 || i.harga_satuan <= 0)) {
      alert("Pastikan semua item memiliki produk, jumlah, dan harga beli yang valid")
      return
    }

    const payload = {
      supplier_name: formData.supplier_name,
      items: formData.items.map(i => ({
        product_id: parseInt(i.product_id),
        jumlah: parseInt(i.jumlah),
        harga_satuan: parseFloat(i.harga_satuan)
      }))
    }

    await $fetch(`${config.public.apiBase}/purchase/`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${currentUser.value?.token}`,
        'Content-Type': 'application/json'
      },
      body: payload
    })

    isModalOpen.value = false
    refreshPurchases()
    alert('Pembelian stok berhasil dicatat!')
  } catch (err) {
    alert(err.data?.detail || 'Terjadi kesalahan saat mencatat pembelian')
  }
}
</script>

<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <div>
        <h1 class="text-2xl font-bold text-slate-900">Pembelian Stok</h1>
        <p class="text-sm text-slate-500">Kelola dan pantau pembelian obat & alkes dari supplier.</p>
      </div>
      <button @click="openModal" class="px-4 py-2.5 bg-green-600 text-white rounded-xl font-semibold text-sm hover:bg-green-700 transition shadow-lg shadow-green-100 flex items-center gap-1.5">
        <Icon name="lucide:plus-circle" class="text-base" />
        Catat Pembelian Stok
      </button>
    </div>

    <div v-if="isModalOpen" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4 backdrop-blur-sm">
      <div class="bg-white rounded-2xl shadow-xl w-full max-w-2xl overflow-hidden flex flex-col max-h-[90vh] border border-slate-100">
        <div class="p-6 border-b border-slate-100 flex justify-between items-center bg-slate-50">
          <h2 class="text-lg font-bold text-slate-900">Form Pembelian Stok</h2>
          <button @click="isModalOpen = false" class="text-slate-400 hover:text-rose-500 transition">
            <Icon name="lucide:x" class="text-2xl" />
          </button>
        </div>
        
        <div class="p-6 overflow-y-auto flex-1 space-y-4">
          <div>
            <label class="block text-xs font-bold text-slate-500 uppercase tracking-wider mb-1">Nama Supplier (Opsional)</label>
            <input v-model="formData.supplier_name" type="text" class="w-full border border-slate-200 rounded-xl px-4 py-2.5 outline-none focus:ring-2 focus:ring-indigo-500 text-sm bg-white" placeholder="PT. Kimia Farma" />
          </div>

          <div class="space-y-4">
            <label class="block text-xs font-bold text-slate-500 uppercase tracking-wider">Daftar Item Pasokan</label>
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

              <div class="w-full md:w-24">
                <label class="block text-[11px] font-bold text-slate-500 uppercase tracking-wider mb-1">Jumlah</label>
                <input v-model="item.jumlah" type="number" min="1" class="w-full border border-slate-200 rounded-xl px-3 py-2.5 bg-white outline-none focus:ring-2 focus:ring-indigo-500 text-sm" />
              </div>

              <div class="w-full md:flex-1">
                <label class="block text-[11px] font-bold text-slate-500 uppercase tracking-wider mb-1">Harga Beli Satuan (Rp)</label>
                <input v-model="item.harga_satuan" type="number" min="0" class="w-full border border-slate-200 rounded-xl px-3 py-2.5 bg-white outline-none focus:ring-2 focus:ring-indigo-500 text-sm" placeholder="Rp" />
              </div>

              <button @click="removeItem(index)" v-if="formData.items.length > 1" class="p-2.5 text-rose-500 hover:bg-rose-50 rounded-xl border border-slate-200 bg-white transition shrink-0">
                <Icon name="lucide:trash-2" class="text-lg" />
              </button>
            </div>
            
            <button type="button" @click="addItem" class="text-xs font-bold text-indigo-600 hover:text-indigo-800 flex items-center gap-1">
              <Icon name="lucide:plus-circle" class="text-base" /> Tambah Item Lain
            </button>
          </div>
        </div>

        <div class="p-6 border-t border-slate-100 bg-slate-50 flex justify-end gap-3">
          <button @click="isModalOpen = false" class="px-5 py-2.5 text-slate-600 font-semibold text-sm hover:bg-slate-200 rounded-xl transition">Batal</button>
          <button @click="submitPurchase" class="px-5 py-2.5 bg-indigo-600 text-white font-bold text-sm hover:bg-indigo-700 rounded-xl transition shadow-lg shadow-indigo-100">
            Simpan Pembelian
          </button>
        </div>
      </div>
    </div>

    <div v-if="purchasesPending" class="text-center py-12 text-slate-500">
      <p class="animate-pulse font-medium text-sm">Sedang memuat data pembelian...</p>
    </div>

    <div v-else-if="purchasesError" class="bg-rose-50 text-rose-600 p-4 rounded-xl border border-rose-100 text-sm">
      Gagal memuat data: {{ purchasesError.message || 'Terjadi kesalahan pada server.' }}
    </div>

    <div v-else class="bg-white rounded-2xl border border-slate-200 overflow-hidden shadow-sm">
      <table class="w-full text-left border-collapse">
        <thead class="bg-slate-50 border-b border-slate-200">
          <tr>
            <th class="p-4 text-xs font-bold text-slate-500 uppercase tracking-wider">ID Nota</th>
            <th class="p-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Supplier</th>
            <th class="p-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Daftar Produk & Harga Pasok</th>
            <th class="p-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Total Qty</th>
            <th class="p-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Total Nota</th>
            <th class="p-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Tanggal</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-100 text-sm text-slate-700">
          <tr v-for="p in purchases" :key="p.id_nota" class="hover:bg-slate-50/80 transition">
            <td class="p-4 font-mono text-xs text-slate-500">#PRC-{{ p.id_nota }}</td>
            <td class="p-4 font-semibold text-slate-700">{{ p.supplier_name }}</td>
            
            <td class="p-4 text-slate-900 font-medium max-w-md leading-relaxed">
              {{ p.produk_display }}
            </td>
            
            <td class="p-4 font-medium text-slate-800">{{ p.jumlah_beli }} Pcs</td>
            <td class="p-4 font-bold text-green-600">Rp {{ Number(p.total_harga_nota).toLocaleString('id-ID') }}</td>
            <td class="p-4 text-slate-500 font-mono text-xs">
              {{ p.tanggal ? new Date(p.tanggal).toLocaleString('id-ID') : '-' }}
            </td>
          </tr>

          <tr v-if="!purchases.length">
            <td colspan="6" class="p-8 text-center text-slate-400">Tidak ada riwayat pembelian stok.</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>