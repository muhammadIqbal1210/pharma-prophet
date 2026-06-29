<script setup>
definePageMeta({
  layout: 'sidebar', // Menggunakan layouts/sidebar.vue
  composables: 'useAuth'    // Menggunakan middleware/auth.ts
})

const config = useRuntimeConfig()
const { currentUser, token } = useAuth()

// --- STATE UTAMA ---
const isModalOpen = ref(false)
const isEditMode = ref(false)
const editingUserId = ref(null)

// State input form
const form = ref({
  nama_lengkap: '',
  username: '',
  email: '',
  password: '',
  role: 'apoteker'
})

// --- STATE PAGINATION ---
const currentPage = ref(1)
const pageSize = ref(10) // Batas data per halaman

// --- FETCH DATA ---
// Ambil data pengguna dari backend
const { data: users, pending, error, refresh } = await useFetch(`${config.public.apiBase}/auth/users`, {
  method: 'GET',
  headers: {
    Authorization: `Bearer ${token.value}`
  }
})

// --- MAPPING DATA UNTUK PAGINATION ---
// 1. Ambil seluruh data mentah pengguna dengan aman
const allUsers = computed(() => {
  return users.value || []
})

// 2. Potong data (slice) untuk ditampilkan hanya pada halaman aktif saat ini
const displayedUsers = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return allUsers.value.slice(start, end)
})

// Pembalas emit ketika tombol angka halaman diklik
const handlePageChange = (newPage) => {
  currentPage.value = newPage
}

// Reset halaman ke 1 jika data pengguna diperbarui dari server
watch(users, () => {
  currentPage.value = 1
})

// --- LOGIKA HAPUS USER ---
const deleteUser = (id) => {
  if (id === currentUser.value?.id) {
    alert('Anda tidak dapat menghapus diri Anda sendiri!')
    return
  }

  if (confirm('Apakah Anda yakin ingin menghapus user ini?')) {
    $fetch(`${config.public.apiBase}/auth/users/${id}`, {
      method: 'DELETE',
      headers: {
        Authorization: `Bearer ${token.value}`
      }
    }).then(() => {
      alert('User berhasil dihapus')
      refresh() // Refresh data tabel setelah penghapusan sukses
    }).catch((err) => {
      alert('Gagal menghapus user: ' + (err.response?._data?.detail || err.message))
    })
  }
}

// --- LOGIKA MODAL FORM ---
const openAddModal = () => {
  isEditMode.value = false
  editingUserId.value = null
  form.value = {
    nama_lengkap: '',
    username: '',
    email: '',
    password: '',
    role: 'apoteker'
  }
  isModalOpen.value = true
}

const openEditModal = (user) => {
  isEditMode.value = true
  editingUserId.value = user.id
  form.value = {
    nama_lengkap: user.nama_lengkap,
    username: user.username,
    email: user.email,
    password: '', // Kosong secara default saat mengedit
    role: user.role
  }
  isModalOpen.value = true
}

// Fungsi kirim data ke Backend
const handleSubmitUser = async () => {
  try {
    if (isEditMode.value) {
      await $fetch(`${config.public.apiBase}/auth/users/${editingUserId.value}`, {
        method: 'PUT',
        headers: {
          Authorization: `Bearer ${token.value}`
        },
        body: form.value
      })
      alert('Data user berhasil diperbarui!')
    } else {
      await $fetch(`${config.public.apiBase}/auth/register`, {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${token.value}`
        },
        body: form.value
      })
      alert('Petugas apoteker baru berhasil ditambahkan!')
    }
    
    isModalOpen.value = false
    refresh()
  } catch (error) {
    const rawDetail = error.response?._data?.detail
    let cleanMessage = 'Terjadi kesalahan pada server.'

    if (Array.isArray(rawDetail)) {
      cleanMessage = rawDetail[0]?.msg || cleanMessage
    } else if (typeof rawDetail === 'string') {
      cleanMessage = rawDetail
    } else {
      cleanMessage = error.message
    }

    alert('Gagal memproses data: ' + cleanMessage)
  }
}
</script>

<template>
  <div class="space-y-6">
    <!-- HEADER PANEL -->
    <div class="flex justify-between items-center">
      <div>
        <h1 class="text-2xl font-bold text-slate-900">Manajemen Pengguna</h1>
        <p class="text-sm text-slate-500">Kelola akun staf apoteker yang terdaftar di dalam sistem.</p>
      </div>
      <button @click="openAddModal" class="px-4 py-2.5 bg-emerald-600 text-white font-semibold rounded-xl hover:bg-emerald-700 transition text-sm flex items-center gap-1.5 shadow-sm">
        <Icon name="lucide:user-plus" class="text-base" />
        Tambah Petugas
      </button>
    </div>

    <!-- DATA LOADING / ERROR STATS -->
    <div v-if="pending" class="text-center py-12 text-slate-500">
      <p class="animate-pulse font-medium text-sm">Sedang memuat data dari server...</p>
    </div>

    <div v-else-if="error" class="bg-rose-50 text-rose-600 p-4 rounded-xl border border-rose-100 text-sm">
      Gagal memuat data: {{ error.message || 'Terjadi kesalahan pada server.' }}
    </div>

    <!-- MAIN DATA TABLE VIEW WITH PAGINATION -->
    <div v-else class="space-y-4">
      <div class="bg-white rounded-2xl border border-slate-200 overflow-hidden shadow-sm">
        <table class="w-full text-left border-collapse">
          <thead class="bg-slate-50 border-b border-slate-200">
            <tr>
              <th class="p-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Username</th>
              <th class="p-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Nama Lengkap</th>
              <th class="p-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Email</th>
              <th class="p-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Hak Akses</th>
              <th class="p-4 text-xs font-bold text-slate-500 uppercase tracking-wider text-center">Aksi</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100 text-sm text-slate-700">
            <!-- Iterasi dirubah menggunakan data pagination 'displayedUsers' -->
            <tr v-for="user in displayedUsers" :key="user.id" class="hover:bg-slate-50/80 transition">
              <td class="p-4 font-mono text-slate-600 text-xs">{{ user.username }}</td>
              <td class="p-4 font-semibold text-slate-900">{{ user.nama_lengkap }}</td>
              <td class="p-4 text-slate-500">{{ user.email }}</td>
              <td class="p-4">
                <span :class="user.role === 'admin' ? 'bg-purple-50 text-purple-700 border-purple-100' : 'bg-teal-50 text-teal-700 border-teal-100'" 
                      class="px-2.5 py-1 text-xs font-bold rounded-lg border capitalize tracking-wide">
                  {{ user.role }}
                </span>
              </td>
              <td class="p-4 text-center space-x-3">
                <button @click="openEditModal(user)" class="text-indigo-600 hover:bg-indigo-50 rounded-lg transition" title="Edit">
                    <Icon name="lucide:edit" class="text-lg" />
                  </button>
                <button 
                  v-if="user.id !== currentUser?.id"
                  @click="deleteUser(user.id)" 
                  class="p-2 text-rose-600 hover:bg-rose-50 rounded-lg transition" title="Hapus">
                  <Icon name="lucide:trash-2" class="text-lg" />
                </button>
                <span v-else class="text-slate-400 text-xs font-semibold cursor-not-allowed" title="Anda tidak dapat menghapus akun sendiri">
                  (Aktif)
                </span>
              </td>
            </tr>
            
            <tr v-if="!displayedUsers.length">
              <td colspan="5" class="p-8 text-center text-slate-400">Tidak ada data pengguna yang ditemukan.</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- NAVIGASI PAGINATION DI BAWAH TABEL -->
      <div v-if="allUsers.length > 0" class="flex justify-end bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
        <Pagination 
          :totalItems="allUsers.length" 
          :pageSize="pageSize" 
          :currentPage="currentPage"
          @page-changed="handlePageChange"
        />
      </div>
    </div>

    <!-- MODAL REGISTRASI / EDIT USER -->
    <div v-if="isModalOpen" class="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/50 backdrop-blur-sm animate-fade-in p-4">
      <div class="bg-white w-full max-w-md rounded-2xl shadow-xl p-6 border border-slate-100 space-y-4">
        
        <div class="flex justify-between items-center border-b pb-3">
          <div>
            <h3 class="text-lg font-bold text-slate-900">{{ isEditMode ? 'Ubah Data Petugas' : 'Registrasi Apoteker Baru' }}</h3>
            <p class="text-xs text-slate-400 mt-0.5">Silakan isi formulir di bawah ini dengan benar.</p>
          </div>
          <button @click="isModalOpen = false" class="text-slate-400 hover:text-slate-600 transition">✕</button>
        </div>

        <form @submit.prevent="handleSubmitUser" class="space-y-4">
          <div>
            <label class="block text-xs font-bold text-slate-500 uppercase tracking-wider">Nama Lengkap</label>
            <input v-model="form.nama_lengkap" type="text" required placeholder="Contoh: Apt. Rudi Hermawan" class="w-full mt-1 px-4 py-2.5 border border-slate-200 rounded-xl focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500 outline-none text-sm transition bg-white" />
          </div>
          
          <div>
            <label class="block text-xs font-bold text-slate-500 uppercase tracking-wider">Username</label>
            <input v-model="form.username" type="text" required placeholder="rudi_farmasi" class="w-full mt-1 px-4 py-2.5 border border-slate-200 rounded-xl focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500 outline-none text-sm font-mono transition bg-white" />
          </div>
          
          <div>
            <label class="block text-xs font-bold text-slate-500 uppercase tracking-wider">Email Resmi</label>
            <input v-model="form.email" type="email" required placeholder="rudi@domain.com" class="w-full mt-1 px-4 py-2.5 border border-slate-200 rounded-xl focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500 outline-none text-sm transition bg-white" />
          </div>

          <div>
            <label class="block text-xs font-bold text-slate-500 uppercase tracking-wider">Hak Akses (Role)</label>
            <select v-model="form.role" required class="w-full mt-1 px-4 py-2.5 border border-slate-200 rounded-xl bg-white focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500 outline-none text-sm transition">
              <option value="admin">Admin</option>
              <option value="apoteker">Apoteker</option>
            </select>
          </div>
          
          <div>
            <label class="block text-xs font-bold text-slate-500 uppercase tracking-wider">
              Password {{ isEditMode ? 'Baru (Opsional)' : 'Awal' }}
            </label>
            <input v-model="form.password" type="password" :required="!isEditMode" placeholder="••••••••" class="w-full mt-1 px-4 py-2.5 border border-slate-200 rounded-xl focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500 outline-none text-sm transition bg-white" />
            <p v-if="isEditMode" class="text-[10px] text-slate-400 mt-1">Kosongkan kolom ini jika tidak ingin memperbarui password.</p>
          </div>

          <div class="flex justify-end gap-2 pt-3 border-t mt-2">
            <button type="button" @click="isModalOpen = false" class="px-4 py-2.5 border border-slate-200 rounded-xl text-slate-600 hover:bg-slate-50 font-semibold text-xs transition">
              Batal
            </button>
            <button type="submit" class="px-5 py-2.5 bg-emerald-600 text-white rounded-xl hover:bg-emerald-700 font-semibold text-xs shadow-md transition">
              {{ isEditMode ? 'Simpan Perubahan' : 'Simpan & Daftarkan' }}
            </button>
          </div>
        </form>
      </div>
    </div>

  </div>
</template>