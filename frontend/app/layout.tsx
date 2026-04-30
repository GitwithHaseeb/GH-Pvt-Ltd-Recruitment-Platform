import type { Metadata } from "next";
import "@/styles/globals.css";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import Link from "next/link";

export const metadata: Metadata = {
  title: "GH Pvt Ltd",
  description: "Production-grade AI/ML solutions"
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <Navbar />
        <main className="container-x py-8">{children}</main>
        <Link
          href="/apply"
          className="fixed bottom-6 right-6 rounded-full bg-neon px-5 py-3 font-semibold text-black shadow-lg"
        >
          Apply Now
        </Link>
        <Footer />
      </body>
    </html>
  );
}
