export default function ClientsPage() {
  const clients = [
    { name: "US FinTech Partner", detail: "Fraud detection and risk analytics modernization." },
    { name: "UAE HealthTech Client", detail: "Medical workflow intelligence and automation." },
    { name: "US Retail Analytics", detail: "Demand prediction and customer segmentation systems." },
    { name: "UAE Logistics AI", detail: "Routing optimization and operational visibility platforms." }
  ];
  return (
    <section className="space-y-8">
      <h1 className="text-3xl font-bold">Clients</h1>
      <p className="max-w-4xl text-white/80">
        GH Pvt Ltd partners with organizations that require dependable engineering for mission-critical AI systems.
        We align with client teams as a long-term technology partner, not only a short-term vendor.
      </p>
      <div className="grid gap-3 md:grid-cols-2">
        {clients.map((client) => (
          <div key={client.name} className="rounded border border-white/20 bg-card p-4">
            <h3 className="font-semibold">{client.name}</h3>
            <p className="mt-2 text-sm text-white/70">{client.detail}</p>
          </div>
        ))}
      </div>
    </section>
  );
}
