export function Logo() {
  return (
    <div className="flex items-center gap-2">
      {/* Minimalista Diamond SVG */}
      <div className="w-6 h-6 flex items-center justify-center">
        <svg
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="1.5"
          className="text-primary w-full h-full"
        >
          <path d="M12 2L22 12L12 22L2 12L12 2Z" strokeLinecap="round" strokeLinejoin="round" />
          <line x1="12" y1="2" x2="12" y2="22" strokeLinecap="round" />
        </svg>
      </div>
      <span className="text-lg font-semibold text-foreground">SinguLetter</span>
    </div>
  )
}
