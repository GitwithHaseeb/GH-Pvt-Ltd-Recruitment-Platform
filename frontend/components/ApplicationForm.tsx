"use client";

import { FormEvent, useState } from "react";
import { submitApplication } from "@/lib/api";

const positions = [
  "Senior AI/ML Engineer",
  "Junior Python Developer",
  "ML Ops Engineer",
  "Backend Engineer (Python)",
  "Data Scientist"
];

export default function ApplicationForm() {
  const [message, setMessage] = useState("");
  const [selectedFile, setSelectedFile] = useState("No file chosen");

  async function onSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    try {
      await submitApplication(formData);
      setMessage("Application submitted successfully.");
      setSelectedFile("No file chosen");
      e.currentTarget.reset();
    } catch {
      setMessage("Failed to submit application.");
    }
  }

  return (
    <form onSubmit={onSubmit} className="grid gap-3 rounded-lg border border-white/20 bg-card p-5">
      <input name="name" required placeholder="Full Name" className="rounded bg-black/40 p-2" />
      <input name="email" type="email" required placeholder="Email" className="rounded bg-black/40 p-2" />
      <input name="phone" type="tel" required placeholder="Phone" className="rounded bg-black/40 p-2" />
      <select name="position_applied" required className="rounded bg-black/40 p-2">
        {positions.map((p) => <option key={p} value={p}>{p}</option>)}
      </select>
      <textarea name="cover_letter" placeholder="Cover Letter (optional)" className="rounded bg-black/40 p-2" />
      <label className="text-sm text-white/80">Upload your CV/Resume (PDF or DOCX, max 5MB)</label>
      <label className="flex cursor-pointer items-center justify-center rounded border border-neon/60 bg-black/30 px-4 py-3 text-sm font-semibold text-neon hover:bg-black/50">
        Upload your CV/Resume
        <input
          name="resume"
          type="file"
          accept=".pdf,.docx"
          required
          className="hidden"
          onChange={(e) => setSelectedFile(e.target.files?.[0]?.name || "No file chosen")}
        />
      </label>
      <p className="text-xs text-white/60">{selectedFile}</p>
      <button className="rounded bg-neon px-4 py-2 font-semibold text-black">Submit Application</button>
      {message && <p className="text-sm text-white/80">{message}</p>}
    </form>
  );
}
