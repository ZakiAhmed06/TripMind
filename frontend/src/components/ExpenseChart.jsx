import React from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from 'recharts';

const COLORS = ['#06b6d4', '#3b82f6', '#10b981', '#f59e0b', '#8b5cf6'];

export default function ExpenseChart({ breakdown }) {
  if (!breakdown) return null;

  const data = [
    { name: 'Transit', value: Number(breakdown.transportation || 0) },
    { name: 'Stay', value: Number(breakdown.accommodation || 0) },
    { name: 'Food', value: Number(breakdown.food || 0) },
    { name: 'Sightseeing', value: Number(breakdown.sightseeing || 0) },
    { name: 'Misc', value: Number(breakdown.miscellaneous || 0) },
  ].filter(d => d.value > 0);

  const total = Number(breakdown.total || data.reduce((a, b) => a + b.value, 0));

  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      const item = payload[0];
      const pct = ((item.value / total) * 100).toFixed(1);
      return (
        <div className="bg-slate-900 border border-slate-700 p-2.5 rounded-lg shadow-xl text-xs">
          <p className="font-semibold text-white">{item.name}</p>
          <p className="text-cyan-400 font-bold">₹{item.value.toLocaleString()} ({pct}%)</p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="bg-slate-900/70 border border-slate-800 rounded-xl p-5 shadow-lg">
      <div className="flex items-center justify-between mb-2">
        <h3 className="text-sm font-bold text-slate-200">Expense Allocation</h3>
        <span className="text-xs font-semibold px-2 py-0.5 rounded bg-cyan-950 text-cyan-400 border border-cyan-800/60">
          Total: ₹{total.toLocaleString()}
        </span>
      </div>
      <p className="text-[11px] text-slate-400 mb-4">Predicted itemized breakdown via Scikit-Learn Random Forest Regressor.</p>

      <div className="h-56 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={data}
              cx="50%"
              cy="50%"
              innerRadius={52}
              outerRadius={75}
              paddingAngle={4}
              dataKey="value"
            >
              {data.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip content={<CustomTooltip />} />
            <Legend
              verticalAlign="bottom"
              height={36}
              formatter={(value, entry) => (
                <span className="text-[11px] text-slate-300 font-medium">{value}</span>
              )}
            />
          </PieChart>
        </ResponsiveContainer>
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-3 gap-2 mt-2 pt-3 border-t border-slate-800 text-[11px]">
        {data.map((item, idx) => (
          <div key={item.name} className="flex items-center gap-1.5">
            <div className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: COLORS[idx % COLORS.length] }} />
            <span className="text-slate-400">{item.name}:</span>
            <span className="font-semibold text-slate-200">₹{item.value.toLocaleString()}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
