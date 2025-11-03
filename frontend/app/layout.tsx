import { AuthProvider } from "@/contexts/AuthContext"
import { Analytics } from "@vercel/analytics/next"
import type React from "react"
import { Geist, Geist_Mono } from "next/font/google"
import type { Metadata } from "next"
import { Navbar } from "@/components/navbar"
import "./globals.css"

const _geist = Geist({ subsets: ["latin"] })
const _geistMono = Geist_Mono({ subsets: ["latin"] })

export const metadata: Metadata = {
  title: "SinguLetter",
  description: "Receba notícias de acordo com suas preferências",
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="pt-BR">
      <body className={`font-sans antialiased`}>
        <AuthProvider>
        <Navbar/>
        {children}
        <Analytics />
        </AuthProvider>
      </body>
    </html>
  )
}
