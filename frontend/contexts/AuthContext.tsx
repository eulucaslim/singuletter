'use client'

import { createContext, useContext, useState, ReactNode, useEffect } from 'react'


export type Token = {
  access: string
  refresh: string
}

type AuthContextType = {
  accessToken: boolean
  login: (token: Token) => void
  logout: () => void
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [accessToken, setAccessToken] = useState(false)

  useEffect(() => {
    const token = localStorage.getItem('access')
    setAccessToken(!!token)
  }, [])

  const login = (token: Token) => {
    localStorage.setItem('access', token.access)
    localStorage.setItem('refresh', token.refresh)
    setAccessToken(true)
  }

  const logout = () => {
    localStorage.removeItem('access')
    localStorage.removeItem('refresh')
    setAccessToken(false)
  }

  return (
    <AuthContext.Provider value={{ accessToken, login, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth deve ser usado dentro de um AuthProvider')
  }
  return context
}