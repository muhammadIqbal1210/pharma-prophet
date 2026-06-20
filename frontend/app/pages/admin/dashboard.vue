<script setup>
definePageMeta({
  layout: 'sidebar'
})

const config = useRuntimeConfig()
const { currentUser } = useAuth()
const tokenCookie = useCookie('auth_token')

// penembakan API mentah agar status pending & error-nya terpusat satu pintu
const { data: dashboardData, pending, error } = await useAsyncData('admin-dashboard', async () => {
  const headers = { 
    Authorization: `Bearer ${tokenCookie.value || currentUser.value?.token}` 
  }

  // Ambil semua data mentah secara paralel
  const [users, products, transactions, stockData] = await Promise.all([
    $fetch(`${config.public.apiBase}/auth/users`, { method: 'GET', headers }),
    $fetch(`${config.public.apiBase}/product`, { method: 'GET', headers }),
    $fetch(`${config.public.apiBase}/transaction`, { method: 'GET', headers }),
    $fetch(`${config.public.apiBase}/stock`, { method: 'GET', headers })
  ])

  // Ambil maksimal 5 user terakhir untuk komponen tabel di bawah
  const latestUsers = Array.isArray(users) ? users.slice(-5).reverse() : []

  return {
    totalUsers: users?.length || users?.total_users || 0,
    totalProducts: products?.length || products?.total_stock || 0,
    totalTransactions: transactions?.length || transactions?.today_transactions || 0,
    lowStockCount: stockData?.length || stockData?.low_stock_count || 0,
    latestUsers: latestUsers
  }
})
</script>

<template>
  <div class="space-y-8">
    <div>
      <h1 class="text-2xl font-bold text-slate-900 tracking-tight">
        Selamat Datang Kembali, {{ currentUser?.nama_lengkap || 'Admin' }}!
      </h1>
      <p class="text-sm text-slate-500">Berikut ringkasan indikator penting operasional apotek saat ini.</p>
    </div>

    <div v-if="pending" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <div v-for="i in 4" :key="i" class="bg-white p-6 rounded-2xl border border-slate-200 animate-pulse space-y-3">
        <div class="h-4 bg-slate-200 rounded w-2/3"></div>
        <div class="h-8 bg-slate-300 rounded w-1/3"></div>
      </div>
    </div>

    <div v-else-if="error" class="bg-rose-50 text-rose-600 p-4 rounded-xl border border-rose-100 text-sm">
      Gagal memuat ringkasan data: {{ error.message || 'Terjadi kesalahan koneksi ke server backend.' }}
    </div>

    <div v-else class="space-y-8">
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        
        <div class="bg-white p-6 rounded-2xl shadow-sm border border-slate-200 flex items-center justify-between">
          <div>
            <p class="text-xs font-medium text-slate-400 uppercase">Total Pengguna</p>
            <h3 class="text-3xl font-bold text-slate-800 mt-1">{{ dashboardData?.totalUsers }}</h3>
          </div>
          <div class="p-3 bg-emerald-50 text-emerald-600 rounded-xl text-xl flex items-center justify-center">
            <Icon name="lucide:users" />
          </div>
        </div>

        <div class="bg-white p-6 rounded-2xl shadow-sm border border-slate-200 flex items-center justify-between">
          <div>
            <p class="text-xs font-medium text-slate-400 uppercase">Total Jenis Obat</p>
            <h3 class="text-3xl font-bold text-slate-800 mt-1">{{ dashboardData?.totalProducts }}</h3>
          </div>
          <div class="p-3 bg-blue-50 text-blue-600 rounded-xl text-xl flex items-center justify-center">
            <Icon name="lucide:box" />
          </div>
        </div>

        <div class="bg-white p-6 rounded-2xl shadow-sm border border-slate-200 flex items-center justify-between">
          <div>
            <p class="text-sm font-medium text-slate-400">Total Transaksi</p>
            <h3 class="text-3xl font-bold text-slate-800 mt-1">{{ dashboardData?.totalTransactions }}</h3>
          </div>
          <div class="p-3 bg-amber-50 text-amber-600 rounded-xl text-xl flex items-center justify-center">
            <Icon name="lucide:shopping-cart" />
          </div>
        </div>

        <div class="bg-white p-6 rounded-2xl shadow-sm border border-slate-200 flex items-center justify-between">
          <div>
            <p class="text-sm font-medium text-slate-400">Stok Hampir Habis</p>
            <h3 class="text-3xl font-bold text-rose-600 mt-1">{{ dashboardData?.lowStockCount }}</h3>
          </div>
          <div class="p-3 bg-rose-50 text-rose-600 rounded-xl text-xl flex items-center justify-center">
            <Icon name="lucide:alert-triangle" />
          </div>
        </div>

      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div class="bg-white p-6 rounded-2xl shadow-sm border border-slate-200 lg:col-span-2 space-y-4">
          <div class="flex justify-between items-center">
            <h3 class="text-lg font-bold text-slate-800">Pengguna Baru Terdaftar</h3>
            <NuxtLink to="/admin/users" class="text-sm font-semibold text-emerald-600 hover:text-emerald-700">
              Lihat Semua
            </NuxtLink>
          </div>
          
          <div class="overflow-hidden border-t border-slate-100 pt-2">
            <table class="w-full text-left border-collapse text-sm">
              <thead>
                <tr class="text-slate-400 font-medium">
                  <th class="py-3">Nama</th>
                  <th class="py-3">Email</th>
                  <th class="py-3">Role</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-100 text-slate-700">
                <tr v-for="latestUser in dashboardData?.latestUsers" :key="latestUser.id">
                  <td class="py-3 font-semibold text-slate-900">{{ latestUser.nama_lengkap || latestUser.name }}</td>
                  <td class="py-3 text-slate-500">{{ latestUser.email }}</td>
                  <td class="py-3 capitalize">
                    <span :class="latestUser.role === 'admin' ? 'text-purple-600 bg-purple-50' : 'text-blue-600 bg-blue-50'" class="px-2 py-0.5 rounded-full text-xs font-semibold">
                      {{ latestUser.role }}
                    </span>
                  </td>
                </tr>
                <tr v-if="!dashboardData?.latestUsers?.length">
                  <td colspan="3" class="py-4 text-center text-slate-400">Belum ada aktivitas pendaftaran baru.</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <div class="bg-white p-6 rounded-2xl shadow-sm border border-slate-200 flex flex-col justify-between">
          <div class="space-y-3">
            <h3 class="text-lg font-bold text-slate-800">Status PharmaCast ML</h3>
            <p class="text-xs text-slate-500">Kondisi performa kecerdasan buatan sistem inventory hari ini.</p>
            <div class="border-t border-slate-100 pt-3 space-y-2">
              <div class="flex justify-between text-sm">
                <span class="text-slate-500">Akurasi Prediksi</span>
                <span class="font-bold text-emerald-600">94.2%</span>
              </div>
              <div class="flex justify-between text-sm">
                <span class="text-slate-500">Update Terakhir</span>
                <span class="font-medium text-slate-700">Hari Ini, 08:00 WIB</span>
              </div>
            </div>
          </div>
          <NuxtLink to="/admin/prediksi" class="w-full py-2.5 mt-4 text-center block bg-slate-50 border border-slate-200 text-slate-700 font-semibold rounded-xl hover:bg-slate-100 text-sm transition">
            Buka Panel Prediksi Stok
          </NuxtLink>
        </div>
      </div>
    </div>
  </div>
</template>