export default function AboutPage() {
  return (
    <section className="space-y-8">
      <h1 className="text-3xl font-bold">About GH Pvt Ltd</h1>
      <p className="max-w-4xl text-white/80">
        GH Pvt Ltd is a specialized AI/ML engineering company delivering production-grade software for global clients. Our mission is
        to convert complex data and business problems into secure, scalable, and measurable digital products.
      </p>
      <div className="grid gap-4 md:grid-cols-3">
        <div className="rounded-lg border border-white/20 bg-card p-4">
          <h3 className="font-semibold">Mission</h3>
          <p className="mt-2 text-sm text-white/70">Build practical AI systems that improve revenue, speed, and operational quality.</p>
        </div>
        <div className="rounded-lg border border-white/20 bg-card p-4">
          <h3 className="font-semibold">Vision</h3>
          <p className="mt-2 text-sm text-white/70">Become a trusted global AI delivery partner for ambitious growth-stage companies.</p>
        </div>
        <div className="rounded-lg border border-white/20 bg-card p-4">
          <h3 className="font-semibold">Values</h3>
          <p className="mt-2 text-sm text-white/70">Ownership, transparency, engineering rigor, and client-first execution.</p>
        </div>
      </div>
      <div className="grid gap-4 md:grid-cols-2">
        <div className="rounded-lg border border-white/20 bg-card p-4">
          <h3 className="text-xl font-semibold">Ghania Tanveer (CEO)</h3>
          <p className="mt-2 text-sm text-white/70">
            Leads AI strategy, delivery excellence, and transformation initiatives across US/UAE client portfolios. Drives roadmap,
            quality benchmarks, and business alignment for enterprise AI adoption.
          </p>
        </div>
        <div className="rounded-lg border border-white/20 bg-card p-4">
          <h3 className="text-xl font-semibold">Muhammad Haseeb (CEO)</h3>
          <p className="mt-2 text-sm text-white/70">
            Leads platform architecture, engineering operations, and MLOps governance. Focused on resilient backend systems,
            performance at scale, and delivery processes that keep quality predictable.
          </p>
        </div>
      </div>
    </section>
  );
}
