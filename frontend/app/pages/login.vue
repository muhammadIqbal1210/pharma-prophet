<template>
  <div class="auth-wrapper">
    <div class="auth-card">
      <h2>Login PharmaCast</h2>
      <p class="subtitle">Silakan masuk ke akun kasir/admin Anda</p>
      
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label>Email</label>
          <input v-model="form.email" type="email" placeholder="contoh@email.com" required />
        </div>

        <div class="form-group">
          <label>Password</label>
          <input v-model="form.password" type="password" placeholder="••••••••" required />
        </div>

        <button type="submit" :disabled="loading">
          {{ loading ? 'Memverifikasi...' : 'Masuk' }}
        </button>
      </form>

      <p v-if="errorMsg" class="error-text">{{ errorMsg }}</p>
      
      <p class="auth-footer">
        Belum punya akun? <NuxtLink to="/register">Daftar di sini</NuxtLink>
      </p>
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