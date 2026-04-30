const services = [
  {
    title: "Computer Vision",
    desc: "Detection, segmentation, quality inspection, and visual intelligence solutions for real-world workflows."
  },
  {
    title: "Natural Language Processing",
    desc: "RAG assistants, document intelligence, classification pipelines, and multilingual language systems."
  },
  {
    title: "Predictive Models",
    desc: "Demand forecasting, churn prediction, risk scoring, and optimization models with business-driven KPIs."
  },
  {
    title: "MLOps",
    desc: "Model lifecycle automation, CI/CD for ML, monitoring, retraining strategy, and reliable deployment practices."
  },
  {
    title: "Python Backends",
    desc: "High-performance APIs, workflow engines, async processing, and secure data-heavy enterprise applications."
  }
];

export default function ServicesPage() {
  return (
    <section className="space-y-8">
      <h1 className="text-3xl font-bold">Services</h1>
      <p className="max-w-4xl text-white/80">
        We provide end-to-end AI/ML software services for organizations that need both speed and engineering maturity.
        Every engagement is built around measurable outcomes, reliable delivery, and production readiness.
      </p>
      <div className="grid gap-3 md:grid-cols-2">
        {services.map((service) => (
          <div key={service.title} className="rounded border border-white/20 bg-card p-4">
            <h3 className="text-lg font-semibold">{service.title}</h3>
            <p className="mt-2 text-sm text-white/70">{service.desc}</p>
          </div>
        ))}
      </div>
    </section>
  );
}
