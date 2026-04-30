"use client";

import Link from "next/link";

export default function ApplyModal() {
  const gmailCompose =
    "https://mail.google.com/mail/?view=cm&fs=1&to=ghaniatanveer061@gmail.com,haseebch8130@gmail.com&su=Application%20for%20%5BPosition%5D%20-%20GH%20Pvt%20Ltd%20-%20%3CCandidate%20Name%3E&body=Dear%20Team%2C%20please%20find%20attached%20my%20CV.%20I%20am%20applying%20for%20%5BPosition%5D.";
  return (
    <div className="grid gap-4 md:grid-cols-2">
      <a href={gmailCompose} target="_blank" rel="noreferrer" className="rounded-lg border border-white/20 bg-card p-5">
        <h3 className="mb-2 text-lg font-semibold">Send CV via Email</h3>
        <p className="text-sm text-white/70">Opens Gmail compose directly in browser with pre-filled subject/body.</p>
        <span className="mt-3 inline-block rounded border border-neon/60 px-3 py-1 text-xs text-neon">
          Open Gmail Compose
        </span>
      </a>
      <Link href="/apply?mode=form" className="rounded-lg border border-white/20 bg-card p-5">
        <h3 className="mb-2 text-lg font-semibold">Fill Online Application</h3>
        <p className="text-sm text-white/70">Submit your profile and CV directly to our ATS pipeline.</p>
      </Link>
    </div>
  );
}
