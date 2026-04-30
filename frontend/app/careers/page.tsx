import Link from "next/link";

const roles = [
  {
    title: "Senior AI/ML Engineer",
    exp: "5+ years",
    summary: "Lead model architecture, production deployment, and technical mentorship."
  },
  {
    title: "Junior Python Developer",
    exp: "1+ years",
    summary: "Build APIs, improve code quality, and collaborate across backend and data teams."
  },
  {
    title: "ML Ops Engineer",
    exp: "3+ years",
    summary: "Own CI/CD pipelines, model observability, and reliable ML delivery workflows."
  },
  {
    title: "Backend Engineer (Python)",
    exp: "3+ years",
    summary: "Design scalable services, optimize databases, and maintain high system reliability."
  },
  {
    title: "Data Scientist",
    exp: "2+ years",
    summary: "Build predictive models and convert data insights into product decisions."
  }
];

export default function CareersPage() {
  return (
    <section className="space-y-8">
      <h1 className="text-3xl font-bold">Careers</h1>
      <p className="max-w-4xl text-white/80">
        We are hiring people who care about building serious production systems. At GH Pvt Ltd, you work directly on international
        projects, learn modern AI/ML practices, and contribute to systems used by real businesses.
      </p>
      <div className="rounded-lg border border-white/20 bg-card p-5">
        <h2 className="text-xl font-semibold">Hiring Process</h2>
        <p className="mt-2 text-sm text-white/70">
          Submit your profile, get ATS-based evaluation, pass technical and project-fit reviews, then receive final selection updates.
          We keep the process transparent, merit-based, and performance-focused.
        </p>
      </div>
      <div className="grid gap-3">
        {roles.map((role) => (
          <div key={role.title} className="rounded border border-white/20 bg-card p-4">
            <h3 className="text-lg font-semibold">{role.title}</h3>
            <p className="mt-1 text-sm text-neon">Experience: {role.exp}</p>
            <p className="mt-2 text-sm text-white/70">{role.summary}</p>
          </div>
        ))}
      </div>
      <Link href="/apply" className="inline-block rounded bg-neon px-4 py-2 font-semibold text-black">Apply Now</Link>
    </section>
  );
}
