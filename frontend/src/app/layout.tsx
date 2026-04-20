import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import Link from "next/link";
import { Activity, Home, FlaskConical, BookOpen } from "lucide-react";

const geistSans = Geist({ variable: "--font-sans", subsets: ["latin"] });
const geistMono = Geist_Mono({ variable: "--font-geist-mono", subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Interactome-AI | Drug Interaction Predictor",
  description:
    "AI-powered prediction of multi-drug adverse interactions using Graph Neural Networks. Analyze polypharmacy risks for safer medication management.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={`${geistSans.variable} ${geistMono.variable} antialiased min-h-screen`}>
        {/* ─── Navigation Bar ─────────────────────────────── */}
        <header className="hospital-gradient text-white sticky top-0 z-50 shadow-md">
          <div className="max-w-7xl mx-auto px-4 sm:px-6">
            <div className="flex items-center justify-between h-16">
              {/* Logo */}
              <Link href="/" className="flex items-center gap-2.5 font-bold text-lg tracking-tight">
                <div className="w-8 h-8 bg-white/20 rounded-lg flex items-center justify-center">
                  <Activity className="w-5 h-5" />
                </div>
                <span>Interactome<span className="font-light">-AI</span></span>
              </Link>

              {/* Nav Links */}
              <nav className="flex items-center gap-1">
                <Link
                  href="/"
                  className="flex items-center gap-1.5 px-3 py-2 rounded-lg text-sm font-medium text-white/80 hover:text-white hover:bg-white/10 transition-colors"
                >
                  <Home className="w-4 h-4" />
                  Home
                </Link>
                <Link
                  href="/predictor"
                  className="flex items-center gap-1.5 px-3 py-2 rounded-lg text-sm font-medium text-white/80 hover:text-white hover:bg-white/10 transition-colors"
                >
                  <FlaskConical className="w-4 h-4" />
                  Predict
                </Link>
                <Link
                  href="/insights"
                  className="flex items-center gap-1.5 px-3 py-2 rounded-lg text-sm font-medium text-white/80 hover:text-white hover:bg-white/10 transition-colors"
                >
                  <BookOpen className="w-4 h-4" />
                  About
                </Link>
              </nav>
            </div>
          </div>
        </header>

        {/* ─── Main Content ───────────────────────────────── */}
        <main className="min-h-[calc(100vh-4rem)]">
          {children}
        </main>

        {/* ─── Footer ─────────────────────────────────────── */}
        <footer className="border-t bg-white py-6 mt-8">
          <div className="max-w-7xl mx-auto px-4 sm:px-6">
            <div className="flex flex-col sm:flex-row justify-between items-center gap-3 text-sm text-muted-foreground">
              <p>© 2025 Interactome-AI — Drug Interaction Prediction Framework</p>
              <p className="text-xs">
                ⚠️ For informational purposes only. Not a substitute for professional medical advice.
              </p>
            </div>
          </div>
        </footer>
      </body>
    </html>
  );
}
