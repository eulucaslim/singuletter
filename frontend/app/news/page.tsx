"use client"

import { useState, useEffect } from "react"
import { useRouter } from "next/navigation"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Skeleton } from "@/components/ui/skeleton"
import { Calendar, ExternalLink } from "lucide-react"
import api from "@/lib/api-client"
import axios from "axios"
import { FilterButton } from "@/components/filter-bottom"
import { Category } from "../preferences/page"

interface News {
  id: string
  title: string
  content: string
  category_name: string
  created_at: string
}


export default function NewsPage() {
  const router = useRouter()
  const [news, setNews] = useState<News[]>([])
  const [categories, setCategories] = useState<string[]>([])
  const [period, setPeriod] = useState<'day' | 'week' | 'month'>('week')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")
  const [filter, setFilter] = useState<string>("all")

  useEffect(() => {

    const accessToken = localStorage.getItem("access")
    if (!accessToken) {
      router.push("/login")
      return
    }
    fetchNews(period)
    fetchCategories()
  }, [router])

  const fetchNews = async (selectedPeriod: string) => {
    try {
      setLoading(true)
      const response = await api.get(`/news?period=${selectedPeriod}`)
      const results = Array.isArray(response.data.results) ? response.data.results : []
      setNews(results)
    } catch (err) {
      if (axios.isAxiosError(err)) {
        setError(err.response?.data?.error || "Erro ao buscar notícias")
      } else {
        setError(err instanceof Error ? err.message : "Erro ao carregar notícias")
      }
    } finally {
      setLoading(false)
    }
  }

  const fetchCategories = async () => {
    try {
      const response = await api.get('/users/me/preferences/')
      if (response.data.categories.length < 1) {
        const categoriesResponse = await api.get('/preferences/')
        setCategories(categoriesResponse.data.map((item: Category) => item.name))
      } else {
        setCategories(response.data.categories.map((item: Category)=> item.name) || []) 
      }

    } catch (err) {
      console.error("Erro ao buscar categorias:", err)
    }
  }

  const handlePeriodChange = (newPeriod: 'day' | 'week' | 'month') => {
    setPeriod(newPeriod)
    fetchNews(newPeriod)
  }

  const filteredNews = filter === "all" ? news : news.filter((item) => item.category_name === filter)

  return (
    <main className="min-h-[calc(100vh-64px)] bg-background py-12">
      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2 text-balance">Notícias Recentes</h1>
          <p className="text-muted-foreground">Acompanhe as notícias das suas categorias preferidas</p>
          <FilterButton
            defaultPeriod={period}
            onSelect={handlePeriodChange}
          />
        </div>

        {/* Filter Buttons */}
        {categories.length > 0 && (
          <div className="mb-8 flex flex-wrap gap-2">
            <Button variant={filter === "all" ? "default" : "outline"} size="sm" onClick={() => setFilter("all")}>
              Todas
            </Button>
            {categories.map((category) => (
              <Button
                key={category}
                variant={filter === category ? "default" : "outline"}
                size="sm"
                onClick={() => setFilter(category)}
              >
                {category}
              </Button>
            ))}
          </div>
        )}

        {/* Error State */}
        {error && (
          <div className="p-4 bg-destructive/10 text-destructive rounded-lg mb-6 border border-destructive/20">
            {error}
          </div>
        )}

        {/* Loading State */}
        {loading ? (
          <div className="space-y-4">
            {[...Array(4)].map((_, i) => (
              <Card key={i}>
                <CardHeader>
                  <Skeleton className="h-6 w-3/4 mb-2" />
                  <Skeleton className="h-4 w-1/3" />
                </CardHeader>
                <CardContent>
                  <Skeleton className="h-24 w-full" />
                </CardContent>
              </Card>
            ))}
          </div>
        ) : filteredNews.length === 0 ? (
          <Card>
            <CardContent className="py-16 text-center">
              <div className="text-4xl mb-4">📰</div>
              <p className="text-lg font-medium mb-2">Nenhuma notícia disponível</p>
              <p className="text-muted-foreground">
                Atualize suas preferências de categorias para receber notícias relevantes
              </p>
              <Button onClick={() => router.push("/preferences")} className="mt-4">
                Gerenciar Categorias
              </Button>
            </CardContent>
          </Card>
        ) : (
          <div className="space-y-4">
            {filteredNews.map((item) => (
              <Card key={item.id} className="hover:shadow-lg transition-shadow overflow-hidden">
                <CardHeader className="pb-3">
                  <div className="flex items-start justify-between gap-4 mb-3">
                    <div className="flex-1">
                      <CardTitle className="text-xl leading-tight text-balance hover:text-primary transition-colors">
                        {item.title}
                      </CardTitle>
                    </div>
                  </div>
                  <div className="flex flex-wrap items-center gap-2 text-sm text-muted-foreground">
                    <Badge variant="secondary" >
                      {item.category_name}
                    </Badge>
                    <span className="flex items-center gap-1">
                      <Calendar className="w-4 h-4" />
                      {new Date(item.created_at).toLocaleDateString("pt-BR")}
                    </span>
                    <span>•</span>
                  </div>
                </CardHeader>
                <CardContent>
                  <p className="text-foreground mb-4 leading-relaxed">{item.content}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        )}

        {/* Stats */}
        {!loading && filteredNews.length > 0 && (
          <div className="mt-12 pt-8 border-t border-border text-center text-muted-foreground">
            <p>
              Mostrando {filteredNews.length} notícias {filter !== "all" ? `de ${filter}` : ""}
            </p>
          </div>
        )}
      </div>
    </main>
  )
}
