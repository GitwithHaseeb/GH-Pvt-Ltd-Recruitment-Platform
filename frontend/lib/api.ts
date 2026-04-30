const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000";

export async function getPositions() {
  const res = await fetch(`${API_BASE}/api/positions`, { cache: "no-store" });
  if (!res.ok) throw new Error("Failed to fetch positions");
  return res.json();
}

export async function submitApplication(form: FormData) {
  const res = await fetch(`${API_BASE}/api/apply/form`, {
    method: "POST",
    body: form
  });
  if (!res.ok) throw new Error("Application submission failed");
  return res.json();
}

export async function fetchAdminMetrics(auth: string) {
  const res = await fetch(`${API_BASE}/api/admin/metrics`, {
    headers: { Authorization: `Basic ${auth}` },
    cache: "no-store"
  });
  if (!res.ok) throw new Error("Failed to fetch admin metrics");
  return res.json();
}

export async function runPipeline(auth: string) {
  const res = await fetch(`${API_BASE}/api/run-pipeline`, {
    method: "POST",
    headers: { Authorization: `Basic ${auth}` }
  });
  if (!res.ok) throw new Error("Failed to trigger pipeline");
  return res.json();
}
