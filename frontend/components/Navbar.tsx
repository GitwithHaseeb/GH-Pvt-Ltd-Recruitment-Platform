"use client";

import Link from "next/link";
import Logo from "./Logo";

export default function Navbar() {
  return (
    <header className="border-b border-white/10 bg-black/30">
      <nav className="container-x flex items-center justify-between py-4">
        <Link href="/">
          <Logo />
        </Link>
        <div className="flex gap-4 text-sm">
          <Link href="/about">About</Link>
          <Link href="/services">Services</Link>
          <Link href="/clients">Clients</Link>
          <Link href="/careers">Careers</Link>
          <Link href="/apply" className="rounded bg-neon px-3 py-1 text-black">Apply Now</Link>
        </div>
      </nav>
    </header>
  );
}
