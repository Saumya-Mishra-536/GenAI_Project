import React from 'react';
import { cn } from '../lib/utils';

const StatCard = ({ title, value, subtitle, icon: Icon, color = "cyan" }) => {
  const colorMap = {
    cyan: "text-cyan-400 border-cyan-500/30 bg-cyan-500/10",
    magenta: "text-fuchsia-400 border-fuchsia-500/30 bg-fuchsia-500/10",
    green: "text-emerald-400 border-emerald-500/30 bg-emerald-500/10",
    orange: "text-orange-400 border-orange-500/30 bg-orange-500/10",
  };

  const style = colorMap[color] || colorMap.cyan;

  return (
    <div className="glass-panel p-5 relative overflow-hidden group">
      <div className={cn("absolute -right-6 -top-6 w-24 h-24 rounded-full blur-2xl opacity-20 group-hover:opacity-40 transition-opacity", style.split(' ')[0].replace('text-', 'bg-'))}></div>
      
      <div className="flex items-start justify-between relative z-10">
        <div>
          <p className="text-gray-400 text-sm font-medium mb-1">{title}</p>
          <h4 className={cn("text-3xl font-bold tracking-tight", style.split(' ')[0])}>{value}</h4>
          {subtitle && <p className="text-xs text-gray-500 mt-2">{subtitle}</p>}
        </div>
        {Icon && (
          <div className={cn("p-2 rounded-lg border", style)}>
            <Icon className="w-5 h-5" />
          </div>
        )}
      </div>
    </div>
  );
};

export default StatCard;
