"use client";

import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";
import { formatDate } from "@/lib/utils";

interface DowntimeChartProps {
  data: { date: string; hours: number }[];
}

export function DowntimeChart({ data }: DowntimeChartProps) {
  const formatted = data.map((d) => ({
    ...d,
    label: formatDate(d.date),
  }));

  return (
    <div className="h-[300px] w-full">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={formatted}>
          <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
          <XAxis dataKey="label" stroke="#94a3b8" fontSize={10} interval="preserveStartEnd" />
          <YAxis stroke="#94a3b8" fontSize={12} />
          <Tooltip
            contentStyle={{ backgroundColor: "#1e293b", border: "1px solid #334155", borderRadius: "8px" }}
          />
          <Line type="monotone" dataKey="hours" stroke="#F97316" strokeWidth={2} dot={false} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
