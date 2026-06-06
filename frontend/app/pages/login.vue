<template>
  <div class="flex items-center justify-center min-h-screen p-4">
    <div class="bg-white rounded-3xl shadow-xl p-10 w-full max-w-md animate-fade-in">
      
      <div class="flex flex-col items-center mb-8 border-b border-slate-100 pb-6">
        <div class="flex items-center gap-4 mb-4">
          <img src="/ikon.jpg" alt="Logo Pharma Prophet" class="w-16 h-16 object-contain">
          <div>
            <h1 class="text-2xl font-bold text-slate-950 tracking-tight">Pharma Prophet</h1>
            <p class="text-xs font-medium text-slate-500 tracking-wider">Sistem Prediksi Stok Apotek</p>
          </div>
        </div>
        <p class="text-sm font-medium text-slate-500">Masuk untuk mengakses Dashboard</p>
      </div>

      <div class="flex gap-2 rounded-xl border border-slate-400 mb-8">
        <div class="flex-1 text-center py-3 bg-gradient-to-r from-emerald-600 to-green-600 text-white font-semibold rounded-xl border border-slate-100 cursor-pointer">
          Masuk
        </div>
        <NuxtLink to="/register" class="flex-1 text-center py-3 text-slate-900 hover:text-slate-900 font-semibold rounded-xl hover:bg-white/50 transition cursor-pointer">
          Daftar
        </NuxtLink>
      </div>

      <form @submit.prevent="handleLogin" class="space-y-6">
      <div class="relative min-h-[56px]">
        <input 
          v-model="form.email" 
          type="email" 
          id="email"
          placeholder=" " 
          required 
          class="peer w-full px-4 py-3.5 bg-transparent border-2 border-slate-200 rounded-xl outline-none text-slate-900 font-normal text-base transition-colors duration-300 focus:border-emerald-500"
        />
        <label 
          for="email" 
          class="absolute left-3 px-1 bg-white text-slate-400 font-normal text-sm tracking-wider transition-all duration-300 pointer-events-none origin-[0_0]
                top-1/2 -translate-y-1/2 scale-100
                peer-focus:top-0 peer-focus:text-xs peer-focus:-translate-y-1/2 peer-focus:text-emerald-600 peer-focus:font-medium
                peer-[:not(:placeholder-shown)]:top-0 peer-[:not(:placeholder-shown)]:text-xs peer-[:not(:placeholder-shown)]:-translate-y-1/2 peer-[:not(:placeholder-shown)]:text-emerald-600 peer-[:not(:placeholder-shown)]:font-medium"
        >
          Masukkan Email Anda
        </label>
      </div>

      <div class="relative min-h-[56px]">
        <input 
          v-model="form.password" 
          type="password" 
          id="password"
          placeholder=" " 
          required 
          class="peer w-full px-4 py-3.5 bg-transparent border-2 border-slate-200 rounded-xl outline-none text-slate-900 font-normal text-base transition-colors duration-300 focus:border-emerald-500"
        />
        <label 
          for="password" 
          class="absolute left-3 px-1 bg-white text-slate-400 font-normal text-sm tracking-wider transition-all duration-300 pointer-events-none origin-[0_0]
                top-1/2 -translate-y-1/2 scale-100
                peer-focus:top-0 peer-focus:text-xs peer-focus:-translate-y-1/2 peer-focus:text-emerald-600 peer-focus:font-medium
                peer-[:not(:placeholder-shown)]:top-0 peer-[:not(:placeholder-shown)]:text-xs peer-[:not(:placeholder-shown)]:-translate-y-1/2 peer-[:not(:placeholder-shown)]:text-emerald-600 peer-[:not(:placeholder-shown)]:font-medium"
        >
          Password
        </label>
      </div>

      <button type="submit" :disabled="loading" 
              class="w-full py-4 bg-gradient-to-r from-emerald-600 to-green-600 text-white font-bold rounded-xl hover:shadow-lg hover:shadow-emerald-200 active:scale-[0.98] transition-all duration-150 disabled:opacity-60">
        {{ loading ? 'Memverifikasi...' : 'Masuk' }}
      </button>
    </form>

      <p v-if="errorMsg" class="mt-6 text-center text-sm font-semibold text-rose-600 bg-rose-50 p-4 rounded-xl border border-rose-100">{{ errorMsg }}</p>
    </div>
  </div>
</template>

<script setup>
const { login } = useAuth()
const form = ref({ email: '', password: '' })
const loading = ref(false)
const errorMsg = ref('')

const handleLogin = async () => {
  loading.value = true
  errorMsg.value = ''
  try {
    await login(form.value)
  } catch (err) {
    errorMsg.value = err
  } finally {
    loading.value = false
  }
}
</script>