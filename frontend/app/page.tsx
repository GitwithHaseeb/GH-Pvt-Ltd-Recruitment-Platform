import ApplyModal from "@/components/ApplyModal";

export default function HomePage() {
  return (
    <section className="space-y-8">
      <div className="space-y-4">
        <h1 className="text-4xl font-bold">GH Pvt Ltd - Production-Grade AI/ML Solutions for Global Clients</h1>
        <p className="max-w-4xl text-white/80">
          GH Pvt Ltd is an AI/ML-focused software house building enterprise platforms for high-growth clients in the US and UAE.
          We design and deploy intelligent systems across computer vision, NLP, predictive analytics, and production-grade Python backends.
        </p>
        <p className="max-w-4xl text-white/70">
          From architecture to deployment, our team focuses on measurable business outcomes: faster operations, better decision intelligence,
          scalable cloud-native systems, and reliable MLOps pipelines for long-term growth.
        </p>
      </div>

      <div className="grid gap-4 md:grid-cols-3">
        <div className="rounded-lg border border-white/20 bg-card p-5">
          <h3 className="text-lg font-semibold">Enterprise Delivery</h3>
          <p className="mt-2 text-sm text-white/70">
            End-to-end project execution with robust quality controls, secure architecture patterns, and full lifecycle ownership.
          </p>
        </div>
        <div className="rounded-lg border border-white/20 bg-card p-5">
          <h3 className="text-lg font-semibold">AI/ML Excellence</h3>
          <p className="mt-2 text-sm text-white/70">
            Advanced model development, data pipelines, and real-world optimization tuned for production reliability.
          </p>
        </div>
        <div className="rounded-lg border border-white/20 bg-card p-5">
          <h3 className="text-lg font-semibold">Global Client Focus</h3>
          <p className="mt-2 text-sm text-white/70">
            Delivery mindset aligned with US/UAE market standards, communication expectations, and operational scale.
          </p>
        </div>
      </div>

      <div className="rounded-lg border border-neon/40 bg-card p-6">
        <h2 className="text-2xl font-semibold">Build Your Career With GH Pvt Ltd</h2>
        <p className="mt-3 max-w-4xl text-white/75">
          We are actively hiring engineers, researchers, and product-minded builders who want to work on high-impact AI/ML systems.
          Our recruitment pipeline includes ATS scoring, intelligent role matching, and a transparent selection workflow built for fairness.
        </p>
        <p className="mt-2 max-w-4xl text-white/70">
          If you are serious about production engineering, clean code, and global delivery standards, this is the team to grow with.
        </p>
      </div>

      <ApplyModal />
    </section>
  );
}
