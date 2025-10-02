import './globals.css'
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Urban Flood Risk Portal',
  description: 'Next.js shell embedding the Streamlit dashboard',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
