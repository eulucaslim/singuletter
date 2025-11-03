"use client"

import { useState, useEffect } from "react"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Checkbox } from "@/components/ui/checkbox"
import { Label } from "@/components/ui/label"
import { AlertCircle, CheckCircle } from "lucide-react"
import api from "@/lib/api-client"
import axios from "axios"

interface Category {
  id: number
  name: string
}

export default function CategoriesPage() {
  const router = useRouter()
  const [selectedCategories, setSelectedCategories] = useState<Category[]>([])
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")
  const [success, setSuccess] = useState(false)
  const [userId, setUserId] = useState<string>("")

  useEffect(() => {
    const accessToken = localStorage.getItem("access")
    if (!accessToken) {
      router.push("/login")
      return
    }

    const { user_id } = parseJwt(accessToken)
    setUserId(user_id)
    getAllCategories()
    loadPreferences()
  }, [router])

  const loadPreferences = async () => {
    try {
      const response = await api.get(`users/me/preferences/`)
      setSelectedCategories(response.data.categories || [])
      selectedCategories.map(item => toggleCategory(item))
    } catch (err) {
      console.error("Erro ao carregar preferências:", err)
    }
  }
  const parseJwt = (token: string) => {
    try {
      return JSON.parse(atob(token.split('.')[1]));
    } catch (e) {
      return null;
  }
  };

  const toggleCategory = (category: Category) => {
    setSelectedCategories((prev) =>
      prev.includes(category) ? prev.filter((c) => c.name !== category.name) : [...prev, category],
    )
    setSuccess(false)
  }

  const handleSelectAll = () => {
    if (selectedCategories.length === categories.length) {
      setSelectedCategories([])
    } else {
      setSelectedCategories(categories.map((c) => c))
    }
    setSuccess(false)
  }

  const getAllCategories = async () => {
    try {
      const response = await api.get(`preferences/`)
      setCategories(response.data || [])
    } catch (err) {
      console.error("Erro ao carregar categorias:", err)
    }
  }

  const handleSave = async () => {
    setLoading(true)
    setError("")
    setSuccess(false)

    try {
      await api.put(`users/me/preferences/`, { category_ids: selectedCategories.map(c => c.id) })

      setSuccess(true)
      setTimeout(() => {
        router.push("/news")
      }, 1500)
    } catch (err) {
      if (axios.isAxiosError(err)) {
        setError(err.response?.data?.error || "Erro ao salvar")
      } else {
        setError(err instanceof Error ? err.message : "Erro ao salvar")
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="min-h-[calc(100vh-64px)] bg-background py-12">
      <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
        <Card className="border-0 shadow-lg">
          <CardHeader className="pb-8">
            <CardTitle className="text-3xl">Suas Preferências</CardTitle>
            <CardDescription className="text-base mt-2">
              Selecione as categorias de notícias que você gostaria de acompanhar. Você pode alterar suas preferências a
              qualquer momento.
            </CardDescription>
          </CardHeader>
          <CardContent>
            {/* Success Message */}
            {success && (
              <div className="p-4 bg-green-50 dark:bg-green-900/20 text-green-800 dark:text-green-200 rounded-lg mb-6 border border-green-200 dark:border-green-800 flex items-center gap-2">
                <CheckCircle className="w-5 h-5" />
                <span>Preferências salvas com sucesso!</span>
              </div>
            )}

            {/* Error Message */}
            {error && (
              <div className="p-4 bg-red-50 dark:bg-red-900/20 text-red-800 dark:text-red-200 rounded-lg mb-6 border border-red-200 dark:border-red-800 flex items-center gap-2">
                <AlertCircle className="w-5 h-5" />
                <span>{error}</span>
              </div>
            )}

            {/* Select All Button */}
            <div className="mb-6 pb-6 border-b border-border">
              <Button variant="outline" onClick={handleSelectAll} disabled={loading} className="text-sm bg-transparent">
                {selectedCategories.length === categories.length ? "Desselecionar Tudo" : "Selecionar Tudo"}
              </Button>
            </div>

            {/* Categories Grid */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-8">
              {categories.map(( category ) => (
                <div key={category.name} className="flex items-center space-x-3 p-3 rounded-lg hover:bg-muted transition-colors">
                  <Checkbox
                    id={category.name}
                    checked={selectedCategories.some((c) => c.id === category.id)}
                    onCheckedChange={() => toggleCategory(category)}
                    disabled={loading}
                    className="w-5 h-5"
                  />
                  <Label htmlFor={category.name} className="cursor-pointer flex items-center gap-2 flex-1">
                    <span className="text-lg">{category.name}</span>
                  </Label>
                  {selectedCategories.includes(category) && <div className="w-2 h-2 rounded-full bg-primary"></div>}
                </div>
              ))}
            </div>

            {/* Stats and Info */}
            <div className="mb-8 p-4 bg-muted rounded-lg">
              <p className="text-sm text-foreground">
                <span className="font-semibold text-lg text-primary">{selectedCategories.length}</span>
                {" de "}
                <span className="font-semibold">{categories.length}</span>
                {" categorias selecionadas"}
              </p>
              {selectedCategories.length ? (
                <p className="text-xs text-muted-foreground mt-2">
                  Você receberá notícias de: {selectedCategories.map(item => item.name).join(', ')}
                </p>
              ) : (
                <p className="text-xs text-muted-foreground mt-2">
                  Não há notícias selecionadas!, Selecione alguma noticia
                </p>
              )
              }
            </div>

            {/* Action Buttons */}
            <div className="flex flex-col sm:flex-row gap-3">
              <Button
                onClick={handleSave}
                disabled={loading || selectedCategories.length === 0}
                className="flex-1"
                size="lg"
              >
                {loading ? "Salvando..." : "Salvar Preferências"}
              </Button>
              <Button
                onClick={() => router.push("/news")}
                variant="outline"
                disabled={loading}
                className="flex-1"
                size="lg"
              >
                Ir para Notícias
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Info Box */}
        <div className="mt-8 p-6 bg-primary/5 rounded-lg border border-primary/10">
          <h3 className="font-semibold text-foreground mb-2">Dica</h3>
          <p className="text-sm text-muted-foreground">
            Selecione pelo menos uma categoria para começar a receber notícias personalizadas. Quanto mais categorias
            você selecionar, mais diversificadas serão as notícias que receberá.
          </p>
        </div>
      </div>
    </main>
  )
}
