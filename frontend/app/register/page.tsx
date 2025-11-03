"use client"

import type React from "react"

import { useState } from "react"
import { useRouter } from "next/navigation"
import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Label } from "@/components/ui/label"
import api from "@/lib/api-client"
import axios from "axios"

interface User {
  username: string
  email: string
  password: string
}

export default function RegisterPage() {
  const router = useRouter()
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")
  const [formData, setFormData] = useState<User>({
    username: "",
    email: "",
    password: "",
  })

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }))
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError("")

    try {
      console.log(formData)
      const registerResponse = await api.post("/users/", formData)

      localStorage.setItem("user", JSON.stringify(registerResponse.data))
      
      const userInfo = JSON.parse(localStorage.getItem("user")!)

      const loginResponse = await api.post("/login/", {
        username: userInfo.username,
        password: formData.password,
      })

      localStorage.setItem("access", loginResponse.data.access)
      localStorage.setItem("refresh", loginResponse.data.refresh)

      router.push("/news")
    } catch (err) {
      if (axios.isAxiosError(err)) {
        setError(err.response?.data?.error || "Erro ao registrar")
      } else {
        setError(err instanceof Error ? err.message : "Erro ao registrar")
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="min-h-[calc(100vh-64px)] flex items-center justify-center px-4">
      <div className="w-full max-w-md">
        <Card>
          <CardHeader className="text-center">
            <CardTitle className="text-2xl">Criar Conta</CardTitle>
            <CardDescription>Registre-se para começar a receber notícias</CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-6">
              {error && <div className="p-3 bg-destructive/10 text-destructive text-sm rounded-md">{error}</div>}

              <div className="space-y-2">
                <Label htmlFor="username">Usuário</Label>
                <Input
                  id="username"
                  name="username"
                  type="text"
                  placeholder="seu_usuario"
                  value={formData.username}
                  onChange={handleChange}
                  required
                  disabled={loading}
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="email">Email</Label>
                <Input
                  id="email"
                  name="email"
                  type="email"
                  placeholder="seu@email.com"
                  value={formData.email}
                  onChange={handleChange}
                  required
                  disabled={loading}
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="password">Senha</Label>
                <Input
                  id="password"
                  name="password"
                  type="password"
                  placeholder="••••••••"
                  value={formData.password}
                  onChange={handleChange}
                  required
                  disabled={loading}
                />
              </div>

              <Button type="submit" className="w-full" disabled={loading}>
                {loading ? "Registrando..." : "Criar Conta"}
              </Button>
            </form>

            <div className="mt-6 text-center text-sm text-muted-foreground">
              Já tem uma conta?{" "}
              <Link href="/login" className="text-primary hover:underline">
                Faça login aqui
              </Link>
            </div>
          </CardContent>
        </Card>
      </div>
    </main>
  )
}
