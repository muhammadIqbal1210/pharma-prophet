// composables/useAuth.ts
export const useAuth = () => {
  const tokenCookie = useCookie('auth_token', {
    maxAge: 60 * 60 * 24, // Cookie hangus dalam 1 hari
    sameSite: 'lax',
  })
  
  const userState = useState('user_data', () => null)
  const config = useRuntimeConfig()

  // 1. Fungsi Register
  const register = async (userData: object) => {
    try {
      await $fetch(`${config.public.apiBase}/auth/register`, {
        method: 'POST',
        body: userData
      })
      return { success: true }
    } catch (error: any) {
      const message = error?.data?.detail || error?.message || 'Pendaftaran gagal'
      throw message
    }
  }

  // 2. Fungsi Login
  const login = async (credentials: object) => {
    try {
      const response: any = await $fetch(`${config.public.apiBase}/auth/login`, {
        method: 'POST',
        body: credentials
      })
      
      // Simpan token ke cookie
      tokenCookie.value = response.access_token
      
      // Arahkan langsung ke dashboard
      navigateTo('/dashboard')
      return { success: true }
    } catch (error: any) {
      throw error.data?.detail || 'Email atau password salah'
    }
  }

  // 3. Fungsi Logout
  const logout = () => {
    tokenCookie.value = null
    userState.value = null
    navigateTo('/login')
  }

  // 4. Cek Status Login
  const isLoggedIn = computed(() => !!tokenCookie.value)

  return {
    register,
    login,
    logout,
    isLoggedIn,
    userState
  }
}