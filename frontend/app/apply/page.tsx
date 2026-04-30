import ApplyModal from "@/components/ApplyModal";
import ApplicationForm from "@/components/ApplicationForm";

export default function ApplyPage({ searchParams }: { searchParams?: { mode?: string } }) {
  const mode = searchParams?.mode || "";
  return (
    <section className="space-y-8">
      <h1 className="text-3xl font-bold">Apply to GH Pvt Ltd</h1>
      <p className="max-w-4xl text-white/80">
        Choose your preferred application channel. You can email your CV directly or use our online application form for faster
        ATS processing and role matching. Please share accurate details so our recruitment engine can evaluate your profile correctly.
      </p>
      <div className="rounded-lg border border-white/20 bg-card p-4 text-sm text-white/70">
        Tip: Mention your strongest technical skills, years of experience, and target position clearly to improve screening accuracy.
      </div>
      {mode === "form" ? <ApplicationForm /> : <ApplyModal />}
    </section>
  );
}
