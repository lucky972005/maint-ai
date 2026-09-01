"use client";

import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";

interface TechnicianLeaderboardProps {
  data: { name: string; repairs: number }[];
}

export function TechnicianLeaderboard({ data }: TechnicianLeaderboardProps) {
  return (
    <div className="h-[300px] w-full">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data} layout="vertical">
          <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
          <XAxis type="number" stroke="#94a3b8" fontSize={12} />
          <YAxis dataKey="name" type="category" stroke="#94a3b8" fontSize={12} width={100} />
          <Tooltip
            contentStyle={{ backgroundColor: "#1e293b", border: "1px solid #334155", borderRadius: "8px" }}
          />
          <Bar dataKey="repairs" fill="#F97316" radius={[0, 4, 4, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
