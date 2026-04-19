import React from 'react';
import { Link } from 'react-router-dom';
import { cn } from '../lib/utils';

const sizes = {
  sm: 'h-7 w-7',
  md: 'h-9 w-9',
  lg: 'h-11 w-11',
};

export function Logo({
  className,
  size = 'md',
  showWordmark = true,
  to,
  wordmarkClassName,
}) {
  const mark = (
    <img
      src="/logo.svg"
      alt=""
      className={cn(sizes[size], 'shrink-0 select-none', className)}
      decoding="async"
    />
  );

  const text = showWordmark && (
    <span
      className={cn(
        'font-semibold tracking-tight text-white text-lg sm:text-xl',
        wordmarkClassName
      )}
    >
      Voltgent
    </span>
  );

  const inner = (
    <>
      {mark}
      {text}
    </>
  );

  if (to) {
    return (
      <Link
        to={to}
        className="flex items-center gap-2.5 min-w-0 focus:outline-none focus-visible:ring-2 focus-visible:ring-cyan-500/60 rounded-lg"
      >
        {inner}
      </Link>
    );
  }

  return <div className="flex items-center gap-2.5 min-w-0">{inner}</div>;
}

export default Logo;
