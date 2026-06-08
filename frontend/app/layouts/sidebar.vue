<script setup>
const route = useRoute()
const { currentUser, isAdmin, logout } = useAuth()

const pageTitle = computed(() => {
  if (route.path.startsWith('/dashboard')) return 'Dashboard'
  if (route.path.startsWith('/stock')) return 'Stok Obat'
  if (route.path.startsWith('/transactions')) return 'Transaksi'
  if (route.path.startsWith('/products')) return 'Produk'
  if (route.path.startsWith('/users')) return 'Manajemen User'
  return 'Panel Apotek'
})

const mainMenu = [
  { label: 'Dashboard', to: '/dashboard', icon: 'lucide:layout-dashboard' },
  { label: 'Stok Obat', to: '/stock', icon: 'lucide:box' },
  { label: 'Transaksi', to: '/transactions', icon: 'lucide:shopping-cart' },
  { label: 'Produk', to: '/products', icon: 'lucide:package' },
]

const adminMenu = [
  { label: 'Manajemen User', to: '/users', icon: 'lucide:users' },
  { label: 'Laporan', to: '/reports', icon: 'lucide:bar-chart-3' },
]
</script>

<template>
  <div class="flex min-h-screen bg-slate-100 text-slate-900">
    <aside class="w-72 shrink-0 border-r border-slate-200 bg-green-500 text-white shadow-2xl">
      <div class="p-6 border-b border-white/10">
        <div class="flex items-center gap-3">
          <img src="/ikon.jpg" alt="Logo Pharma Prophet" class="h-12 w-12 rounded-2xl object-cover" />
          <div>
            <h2 class="text-xl font-bold">PharmaCast</h2>
            <p class=" text-emerald-200 text-xs">Sistem Manajemen Inventory dan Penjualan Apotek</p>
          </div>
        </div>
      </div>

      <nav class="flex flex-1 flex-col gap-1 p-4">
        <p class="px-3 pb-2 text-slate-300 text-s">Menu Utama</p>
        <NuxtLink
          v-for="item in mainMenu"
          :key="item.to"
          :to="item.to"
          class="flex items-center gap-3 rounded-2xl px-4 py-3 text-md font-semibold text-slate-100 transition hover:bg-emerald-500/15 hover:text-emerald-200"
          active-class="bg-emerald-900/20 text-emerald-100"
        >
          <Icon :name="item.icon" class="text-l" />
          {{ item.label }}
        </NuxtLink>

        <template v-if="isAdmin">
          <p class="mt-3 px-3 text-slate-300">Admin</p>
          <NuxtLink
            v-for="item in adminMenu"
            :key="item.to"
            :to="item.to"
            class="flex items-center gap-3 rounded-2xl px-4 py-3 text-md font-semibold text-slate-100 transition hover:bg-rose-500/15 hover:text-rose-200"
            active-class="bg-rose-500/20 text-rose-100"
          >
            <Icon :name="item.icon" class="text-xl" />
            {{ item.label }}
          </NuxtLink>
        </template>
      </nav>

      <div class="border-t border-white/10 p-4">
        <button
          type="button"
          @click="logout"
          class="flex w-full items-start gap-2 rounded-2xl bg-white/8 px-4 py-3 text-sm font-semibold text-white transition hover:bg-rose-500/20 hover:text-rose-100"
        >
          <Icon name="lucide:log-out" class="text-xl" />
          Logout
        </button>
      </div>
      
        <div class="mt-5 rounded-2xl border border-white/10 bg-white/8 p-4">
          <p class="text-[11px]  tracking-[0.3em] text-slate-300">Login sebagai</p>
          <p class="mt-1 text-lg font-semibold text-white">{{ isAdmin ? 'Admin' : 'Apoteker' }}</p>
        </div>
    </aside>

    <div class="flex min-h-screen flex-1 flex-col overflow-hidden">
      <header class="border-b border-slate-200 bg-white/90 px-6 py-4 shadow-sm backdrop-blur">
        <div class="flex items-center justify-between gap-4">
          <div>
            <p class="text-xs uppercase tracking-[0.35em] text-emerald-600">Pharma Prophet</p>
            <h1 class="text-xl font-bold text-slate-800">{{ pageTitle }}</h1>
          </div>
          <div class="rounded-2xl bg-emerald-50 px-4 py-2 text-sm text-emerald-700 shadow-sm">
            Hi {{ currentUser?.nama_lengkap || currentUser?.username || 'Apoteker' }}, optimalkan stok hari ini.
          </div>
        </div>
      </header>

      <main class="flex-1 overflow-y-auto p-6">
        <slot />
      </main>
    </div>
  </div>
</template>
