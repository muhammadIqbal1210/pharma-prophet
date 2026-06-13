// composables/useAuth.ts
export const useAuth = () => {
  const tokenCookie = useCookie('auth_token', {
    maxAge: 60 * 60 * 24,
    sameSite: 'lax',
  })

  const userCookie = useCookie('auth_user', {
    maxAge: 60 * 60 * 24,
    sameSite: 'lax',
  })

  const userState = useState('user_data', () => userCookie.value || null)
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
      
      tokenCookie.value = response.access_token
      userCookie.value = response.user || null
      userState.value = response.user || null
      
      return { success: true }
    } catch (error: any) {
      throw error.data?.detail || 'Email atau password salah'
    }
  }

  // 3. Fungsi Logout
  const logout = () => {
    tokenCookie.value = null
    userCookie.value = null
    userState.value = null
    navigateTo('/login')
  }

  const currentUser = computed(() => (userState.value || userCookie.value) as Record<string, any> | null)
  const isAdmin = computed(() => String(currentUser.value?.role || '').toLowerCase() === 'admin')

  // 4. Cek Status Login
  const isLoggedIn = computed(() => !!tokenCookie.value)

  return {
    register,
    login,
    logout,
    isLoggedIn,
    userState,
    currentUser,
    isAdmin,
  }
}