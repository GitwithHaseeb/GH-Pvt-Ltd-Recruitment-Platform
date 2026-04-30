"use client";

import { Bar, BarChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

type Props = { scores: number[] };

export default function ATSChart({ scores }: Props) {
  const bins = [0, 20, 40, 60, 80, 100];
  const data = bins.slice(0, -1).map((b, i) => ({
    range: `${b}-${bins[i + 1]}`,
    count: scores.filter((s) => s >= b && s < bins[i + 1]).length
  }));

  return (
    <div className="h-64 w-full rounded-lg bg-card p-3">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data}>
          <XAxis dataKey="range" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="count" fill="#00f5d4" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
