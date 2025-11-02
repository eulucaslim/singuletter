import Link from "next/link"
import { Button } from "@/components/ui/button"

export default function Home() {
  return (
    <main className="min-h-[calc(100vh-64px)] flex items-center justify-center">
      <div className="text-center max-w-2xl mx-auto px-4">
        <div className="mb-8 flex justify-center">
          <div className="w-24 h-24">
            <svg
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="1"
              className="text-primary w-full h-full"
            >
              <path d="M12 2L22 12L12 22L2 12L12 2Z" strokeLinecap="round" strokeLinejoin="round" />
              <line x1="12" y1="2" x2="12" y2="22" strokeLinecap="round" />
            </svg>
          </div>
        </div>

        <h1 className="text-4xl md:text-5xl font-bold text-balance mb-4">
          Bem-vindo ao <span className="text-primary">SinguLetter</span>
        </h1>
        <p className="text-lg text-muted-foreground mb-8 text-balance">
          Receba notícias selecionadas de acordo com suas preferências de categorias
        </p>

        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Link href="/login">
            <Button size="lg" variant="outline">
              Login
            </Button>
          </Link>
          <Link href="/register">
            <Button size="lg">Criar Conta</Button>
          </Link>
        </div>
      </div>
    </main>
  )
}
