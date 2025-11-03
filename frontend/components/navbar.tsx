"use client"

import Link from "next/link"
import { Logo } from "./logo"
import { Button } from "@/components/ui/button"
import { useRouter } from "next/navigation"
import { useAuth } from "@/contexts/AuthContext"

export function Navbar() {
  const router = useRouter()
  const { accessToken, logout } = useAuth();


  const handleLogout = () => {
    logout()
    router.push("/")
  }

  return (
    <nav className="border-b border-border bg-card">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <Link href="/news" className="hover:opacity-80 transition-opacity">
            <Logo />
          </Link>

          <div className="flex items-center gap-4">
            { accessToken ? (
              <>
                <Link href="/news" className="text-sm text-muted-foreground hover:text-foreground transition-colors">
                  Notícias
                </Link>
                <Link
                  href="/preferences"
                  className="text-sm text-muted-foreground hover:text-foreground transition-colors"
                >
                  Categorias
                </Link>
                <Button onClick={handleLogout} variant="outline" size="sm">
                  Logout
                </Button>
              </>
            ) : (
              <>
                <Link href="/login">
                  <Button variant="ghost" size="sm">
                    Login
                  </Button>
                </Link>
                <Link href="/register">
                  <Button size="sm">Registrar</Button>
                </Link>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  )
}
