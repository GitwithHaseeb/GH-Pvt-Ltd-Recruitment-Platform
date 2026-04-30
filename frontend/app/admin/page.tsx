"use client";

import { useState } from "react";
import ATSChart from "@/components/ATSChart";
import { fetchAdminMetrics, runPipeline } from "@/lib/api";

export default function AdminPage() {
  const [user, setUser] = useState("admin");
  const [pass, setPass] = useState("admin123");
  const [data, setData] = useState<any>(null);

  const auth = typeof window !== "undefined" ? btoa(`${user}:${pass}`) : "";

  async function load() {
    const metrics = await fetchAdminMetrics(auth);
    setData(metrics);
  }

  async function trigger() {
    await runPipeline(auth);
    await load();
  }

  return (
    <section className="space-y-4">
      <h1 className="text-3xl font-bold">Admin Dashboard</h1>
      <div className="flex gap-2">
        <input value={user} onChange={(e) => setUser(e.target.value)} className="rounded bg-black/40 p-2" />
        <input value={pass} onChange={(e) => setPass(e.target.value)} type="password" className="rounded bg-black/40 p-2" />
        <button onClick={load} className="rounded bg-neon px-3 py-2 font-semibold text-black">Load Metrics</button>
        <button onClick={trigger} className="rounded border border-neon px-3 py-2">Run Recruitment</button>
      </div>
      {data && (
        <div className="space-y-4">
          <p>Total candidates: {data.total_candidates}</p>
          <ATSChart scores={data.ats_distribution || []} />
          <div className="rounded bg-card p-4">
            <h3 className="font-semibold">Selected Candidates</h3>
            {(data.selected_candidates || []).map((c: any) => (
              <p key={c.id}>{c.name} - {c.position_applied} ({c.ats_score})</p>
            ))}
          </div>
        </div>
      )}
    </section>
  );
}
