<script setup>
definePageMeta({
  layout: 'sidebar',
  composables: 'useAuth'
})

const route = useRoute()
const router = useRouter()
const config = useRuntimeConfig()
const { token } = useAuth()

const productId = route.params.id
const isSubmitting = ref(false)
const errorMessage = ref('')

// Ambil data produk yang akan diedit
const { data: product, pending, error } = await useFetch(`${config.public.apiBase}/product/${productId}`, {
  method: 'GET',
  headers: { Authorization: `Bearer ${token.value}` }
})

// Form diisi dengan data yang sudah ada
const form = ref({
  nama_produk: '',
  kategori: 'Obat',
  satuan: 'Strip',
  harga_jual: 0,
  stok_saat_ini: 0,
  stok_minimum: 0,
  deskripsi: ''
})

// Isi form setelah data produk dimuat
watch(product, (val) => {
  if (val) {
    form.value = {
      nama_produk: val.nama_produk ?? '',
      kategori: val.kategori ?? 'Obat',
      satuan: val.satuan ?? 'Strip',
      harga_jual: val.harga_jual ?? 0,
      stok_saat_ini: val.stok_saat_ini ?? 0,
      stok_minimum: val.stok_minimum ?? 0,
      deskripsi: val.deskripsi ?? ''
    }
  }
}, { immediate: true })

const submitForm = async () => {
  isSubmitting.value = true
  errorMessage.value = ''
  try {
    await $fetch(`${config.public.apiBase}/product/${productId}`, {
      method: 'PUT',
      headers: { Authorization: `Bearer ${token.value}` },
      body: form.value
    })
    router.push('/admin/products')
  } catch (err) {
    errorMessage.value = err.data?.detail || err.message || 'Terjadi kesalahan saat menyimpan data.'
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <div class="space-y-6 max-w-4xl mx-auto">
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-slate-900">Edit Produk</h1>
        <p class="text-sm text-slate-500">Perbarui detail informasi produk yang ada di sistem.</p>
      </div>
      <NuxtLink to="/admin/products" class="text-sm font-semibold text-slate-500 hover:text-slate-800 transition">
        Batal &amp; Kembali
      </NuxtLink>
    </div>

    <div v-if="pending" class="text-center py-12 text-slate-500">
      <p class="animate-pulse font-medium text-sm">Memuat data produk...</p>
    </div>

    <div v-else-if="error" class="bg-rose-50 text-rose-600 p-4 rounded-xl border border-rose-100 text-sm">
      Gagal memuat data produk: {{ error.message }}
    </div>

    <div v-else class="bg-white rounded-2xl border border-slate-200 overflow-hidden shadow-sm p-6 lg:p-8">
      <form @submit.prevent="submitForm" class="space-y-6">

        <div v-if="errorMessage" class="bg-rose-50 text-rose-600 p-4 rounded-xl border border-rose-100 text-sm font-medium">
          {{ errorMessage }}
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="space-y-2 md:col-span-2">
            <label class="text-sm font-bold text-slate-700">Nama Produk</label>
            <input v-model="form.nama_produk" type="text" required placeholder="Mis. Paracetamol 500mg"
              class="w-full border border-slate-300 rounded-xl px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 transition text-sm bg-white" />
          </div>

          <div class="space-y-2">
            <label class="text-sm font-bold text-slate-700">Kategori</label>
            <select v-model="form.kategori"
              class="w-full border border-slate-300 rounded-xl px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 transition text-sm bg-white">
              <option value="Obat">Obat</option>
              <option value="Alkes">Alat Kesehatan (Alkes)</option>
            </select>
          </div>

          <div class="space-y-2">
            <label class="text-sm font-bold text-slate-700">Satuan</label>
            <select v-model="form.satuan"
              class="w-full border border-slate-300 rounded-xl px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 transition text-sm bg-white">
              <option value="Tablet">Tablet</option>
              <option value="Strip">Strip</option>
              <option value="Botol">Botol</option>
              <option value="Pcs">Pcs</option>
            </select>
          </div>

          <div class="space-y-2 md:col-span-2">
            <label class="text-sm font-bold text-slate-700">Harga Jual (Rp)</label>
            <input v-model.number="form.harga_jual" type="number" min="1" required placeholder="Mis. 5000"
              class="w-full border border-slate-300 rounded-xl px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 transition text-sm bg-white" />
          </div>

          <div class="space-y-2">
            <label class="text-sm font-bold text-slate-700">Stok Saat Ini</label>
            <input v-model.number="form.stok_saat_ini" type="number" min="0" required
              class="w-full border border-slate-300 rounded-xl px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 transition text-sm bg-white" />
          </div>

          <div class="space-y-2">
            <label class="text-sm font-bold text-slate-700">Batas Stok Minimum</label>
            <input v-model.number="form.stok_minimum" type="number" min="0" required
              class="w-full border border-slate-300 rounded-xl px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 transition text-sm bg-white" />
          </div>

          <div class="space-y-2 md:col-span-2">
            <label class="text-sm font-bold text-slate-700">Deskripsi (Opsional)</label>
            <textarea v-model="form.deskripsi" rows="3"
              placeholder="Deskripsi mengenai produk, aturan pakai, atau catatan khusus."
              class="w-full border border-slate-300 rounded-xl px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 transition text-sm resize-none bg-white"></textarea>
          </div>
        </div>

        <div class="pt-6 border-t border-slate-100 flex justify-end gap-3">
          <NuxtLink to="/admin/products"
            class="px-4 py-2.5 border border-slate-200 rounded-xl text-slate-600 hover:bg-slate-50 font-bold text-sm transition">
            Batal
          </NuxtLink>
          <button type="submit" :disabled="isSubmitting"
            class="px-4 py-2.5 bg-emerald-600 text-white font-bold rounded-xl hover:bg-emerald-700 transition disabled:opacity-50 disabled:cursor-not-allowed text-sm flex items-center gap-2 shadow-sm">
            <Icon v-if="isSubmitting" name="lucide:loader-2" class="animate-spin text-base" />
            <Icon v-else name="lucide:save" class="text-base" />
            Simpan Perubahan
          </button>
        </div>

      </form>
    </div>
  </div>
</template>
