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

interface News {
  id: string
  title: string
  content: string
  category_name: string
  created_at: string
  url?: string
}


export default function NewsPage() {
  const router = useRouter()
  const [news, setNews] = useState<News[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")
  const [filter, setFilter] = useState<string>("all")

  useEffect(() => {

    const accessToken = localStorage.getItem("access")
    if (!accessToken) {
      router.push("/login")
      return
    }

    fetchNews()
  }, [router])

  const fetchNews = async () => {
    try {
      setLoading(true)
      const response = await api.get("/news")
      console.log("Response backend", response.data)
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

  const categories = Array.from(new Set(news.map((item) => item.category_name)))
  const filteredNews = filter === "all" ? news : news.filter((item) => item.category_name === filter)

  const getCategoryColor = (category: string) => {
    const colors: { [key: string]: string } = {
      Tecnologia: "bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200",
      Negócios: "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200",
      Saúde: "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200",
      Política: "bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200",
      Esportes: "bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-200",
      Entretenimento: "bg-pink-100 text-pink-800 dark:bg-pink-900 dark:text-pink-200",
    }
    return colors[category] || "bg-slate-100 text-slate-800 dark:bg-slate-700 dark:text-slate-200"
  }

  return (
    <main className="min-h-[calc(100vh-64px)] bg-background py-12">
      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2 text-balance">Notícias Recentes</h1>
          <p className="text-muted-foreground">Acompanhe as notícias das suas categorias preferidas</p>
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
              <Button onClick={() => router.push("/categories")} className="mt-4">
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
                    <Badge variant="secondary" className={getCategoryColor(item.category_name)}>
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
                  {item.url && (
                    <a
                      href={item.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center gap-2 text-primary hover:underline font-medium"
                    >
                      Leia a notícia completa
                      <ExternalLink className="w-4 h-4" />
                    </a>
                  )}
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
