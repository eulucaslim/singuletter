'use client'

import { useRouter } from 'next/navigation'
import { Button } from "@/components/ui/button"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { useState } from 'react'

type FilterButtonProps = {
  defaultPeriod?: 'day' | 'week' | 'month'
  onSelect?: (period: 'day' | 'week' | 'month') => void
}

export function FilterButton({ defaultPeriod = 'day', onSelect }: FilterButtonProps) {
  const [selectedPeriod, setSelectedPeriod] = useState(defaultPeriod)

  const handleSelect = (period: 'day' | 'week' | 'month') => {
    setSelectedPeriod(period)
    if (onSelect) {
      onSelect(period)
    }
  }

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button className="mt-4" variant="outline">
          Filtrar por período
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent>
        <DropdownMenuItem onClick={() => handleSelect('day')}>Hoje</DropdownMenuItem>
        <DropdownMenuItem onClick={() => handleSelect('week')}>Esta semana</DropdownMenuItem>
        <DropdownMenuItem onClick={() => handleSelect('month')}>Este mês</DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  )
}