import React from 'react';
import { cn } from '../lib/utils';

const GlassCard = ({ children, className, title, icon: Icon, action }) => {
  return (
    <div className={cn("glass-panel p-6 flex flex-col gap-4", className)}>
      {(title || Icon || action) && (
        <div className="flex items-center justify-between pb-3 border-b border-white/10">
          <div className="flex items-center gap-3">
            {Icon && <Icon className="w-5 h-5 text-cyan-400" />}
            {title && <h3 className="font-semibold text-lg tracking-wide">{title}</h3>}
          </div>
          {action && <div>{action}</div>}
        </div>
      )}
      <div className="flex-grow">
        {children}
      </div>
    </div>
  );
};

export default GlassCard;
