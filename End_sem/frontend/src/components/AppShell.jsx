import React, { useState } from 'react';
import { NavLink, Outlet } from 'react-router-dom';
import {
  LayoutDashboard,
  Zap,
  UploadCloud,
  Bot,
  Menu,
  X,
} from 'lucide-react';
import Logo from './Logo';
import { cn } from '../lib/utils';

const navItems = [
  { name: 'Overview', path: '/overview', icon: LayoutDashboard, description: 'Model and data health' },
  { name: 'Predict', path: '/predict', icon: Zap, description: 'Single-point inference' },
  { name: 'Ingest', path: '/batch', icon: UploadCloud, description: 'Batch upload and validation' },
  { name: 'Agent', path: '/planner', icon: Bot, description: 'Infrastructure planning' },
];

export default function AppShell() {
  const [mobileOpen, setMobileOpen] = useState(false);

  const NavItems = ({ onNavigate }) => (
    <ul className="space-y-1">
      {navItems.map((item) => (
        <li key={item.path}>
          <NavLink
            to={item.path}
            onClick={onNavigate}
            className={({ isActive }) =>
              cn(
                'group flex gap-3 rounded-xl px-3 py-2.5 text-sm font-medium transition-colors border',
                isActive
                  ? 'bg-cyan-500/15 text-cyan-300 border-cyan-500/35 shadow-[0_0_24px_rgba(34,211,238,0.12)]'
                  : 'text-zinc-400 border-transparent hover:bg-white/[0.04] hover:text-zinc-200'
              )
            }
          >
            <item.icon className="h-4 w-4 shrink-0 mt-0.5 opacity-90" aria-hidden />
            <span className="min-w-0">
              <span className="block leading-tight">{item.name}</span>
              <span className="block text-[11px] font-normal text-zinc-500 group-hover:text-zinc-500 leading-snug mt-0.5">
                {item.description}
              </span>
            </span>
          </NavLink>
        </li>
      ))}
    </ul>
  );

  return (
    <div className="min-h-screen flex bg-[#05050c] text-zinc-200">
      {/* subtle grid */}
      <div
        className="pointer-events-none fixed inset-0 opacity-[0.35]"
        style={{
          backgroundImage:
            'linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px)',
          backgroundSize: '48px 48px',
        }}
      />
      <div className="pointer-events-none fixed -top-40 -left-32 h-96 w-96 rounded-full bg-cyan-500/15 blur-[120px]" />
      <div className="pointer-events-none fixed -bottom-48 -right-32 h-[28rem] w-[28rem] rounded-full bg-violet-600/15 blur-[140px]" />

      {/* Desktop sidebar */}
      <aside className="relative z-20 hidden lg:flex w-[260px] shrink-0 flex-col border-r border-white/[0.06] bg-[#070712]/90 backdrop-blur-xl">
        <div className="flex h-16 items-center gap-2 border-b border-white/[0.06] px-5">
          <Logo to="/" size="md" wordmarkClassName="text-[17px]" />
        </div>
        <nav className="flex-1 overflow-y-auto p-4">
          <p className="px-3 mb-2 text-[11px] font-semibold uppercase tracking-wider text-zinc-500">
            Workspace
          </p>
          <NavItems />
        </nav>
        <div className="p-4 border-t border-white/[0.06]">
          <NavLink
            to="/"
            className="text-xs text-zinc-500 hover:text-zinc-300 transition-colors px-3"
          >
            Back to marketing site
          </NavLink>
        </div>
      </aside>

      {/* Mobile header */}
      <div className="lg:hidden fixed top-0 left-0 right-0 z-30 flex h-14 items-center justify-between border-b border-white/[0.06] bg-[#070712]/95 backdrop-blur-xl px-4">
        <Logo to="/overview" size="sm" wordmarkClassName="text-base" />
        <button
          type="button"
          className="rounded-lg p-2 text-zinc-400 hover:bg-white/5 hover:text-white"
          aria-label={mobileOpen ? 'Close menu' : 'Open menu'}
          onClick={() => setMobileOpen((o) => !o)}
        >
          {mobileOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
        </button>
      </div>

      {mobileOpen && (
        <div className="lg:hidden fixed inset-0 z-20 pt-14 bg-black/60 backdrop-blur-sm" onClick={() => setMobileOpen(false)}>
          <div
            className="absolute right-0 top-14 h-[calc(100vh-3.5rem)] w-[min(100%,320px)] border-l border-white/[0.08] bg-[#070712] p-4 shadow-2xl"
            onClick={(e) => e.stopPropagation()}
          >
            <NavItems onNavigate={() => setMobileOpen(false)} />
            <NavLink
              to="/"
              onClick={() => setMobileOpen(false)}
              className="mt-6 block text-xs text-zinc-500 hover:text-zinc-300 px-3"
            >
              Back to marketing site
            </NavLink>
          </div>
        </div>
      )}

      <div className="relative z-10 flex min-h-screen flex-1 flex-col lg:pt-0 pt-14">
        <main className="flex-1 px-3 py-5 sm:px-5 sm:py-8 lg:px-10 lg:py-10 max-w-[1600px] w-full mx-auto pb-8">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
