import Logo from "./Logo";

export default function Footer() {
  return (
    <footer className="mt-16 border-t border-white/10 py-8">
      <div className="container-x flex flex-col items-start justify-between gap-4 md:flex-row">
        <Logo />
        <p className="text-sm text-white/70">Production-grade AI/ML services for US/UAE clients.</p>
      </div>
    </footer>
  );
}
