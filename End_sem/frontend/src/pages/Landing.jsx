import React from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import {
  ArrowRight,
  BarChart3,
  Bot,
  Gauge,
  UploadCloud,
  Zap,
  Shield,
} from 'lucide-react';
import Logo from '../components/Logo';
import { cn } from '../lib/utils';

function Feature({ icon: Icon, title, children }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: '-40px' }}
      transition={{ duration: 0.4, ease: [0.22, 1, 0.36, 1] }}
      className={cn(
        'rounded-2xl border border-white/[0.08] bg-white/[0.03] p-5 sm:p-6 backdrop-blur-sm',
        'hover:border-cyan-500/25 hover:bg-white/[0.05] transition-colors'
      )}
    >
      <div className="mb-4 inline-flex rounded-lg border border-cyan-500/20 bg-cyan-500/10 p-2.5 text-cyan-400">
        <Icon className="h-5 w-5" aria-hidden />
      </div>
      <h3 className="text-lg font-semibold text-white mb-2">{title}</h3>
      <p className="text-sm text-zinc-400 leading-relaxed">{children}</p>
    </motion.div>
  );
}

export default function Landing() {
  return (
    <div className="min-h-screen bg-[#05050c] text-zinc-200 relative overflow-hidden">
      <div
        className="pointer-events-none absolute inset-0 opacity-[0.4]"
        style={{
          backgroundImage:
            'linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px)',
          backgroundSize: '56px 56px',
        }}
      />
      <div className="pointer-events-none absolute -top-48 left-1/2 -translate-x-1/2 h-[520px] w-[520px] rounded-full bg-cyan-500/20 blur-[140px]" />
      <div className="pointer-events-none absolute bottom-0 right-0 h-[400px] w-[400px] rounded-full bg-violet-600/15 blur-[120px]" />

      <header className="relative z-10 border-b border-white/[0.06] bg-[#070712]/80 backdrop-blur-xl">
        <div className="mx-auto flex h-16 max-w-6xl items-center justify-between px-4 sm:px-6">
          <Logo to="/" size="md" />
          <div className="flex items-center gap-3">
            <a
              href="#product"
              className="hidden sm:inline text-sm text-zinc-400 hover:text-white transition-colors px-2"
            >
              Product
            </a>
            <Link
              to="/overview"
              className="inline-flex items-center gap-2 rounded-lg bg-cyan-500/15 px-4 py-2 text-sm font-medium text-cyan-300 border border-cyan-500/35 hover:bg-cyan-500/25 transition-colors"
            >
              Open workspace
              <ArrowRight className="h-4 w-4" aria-hidden />
            </Link>
          </div>
        </div>
      </header>

      <main>
        <section className="relative z-10 mx-auto max-w-6xl px-4 pt-14 pb-16 sm:px-6 sm:pt-24 sm:pb-28">
          <div className="max-w-3xl">
            <motion.p
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.35 }}
              className="text-sm font-medium text-cyan-400/90 mb-4 flex items-center gap-2"
            >
              <Gauge className="h-4 w-4 shrink-0" aria-hidden />
              EV charging demand intelligence
            </motion.p>
            <motion.h1
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.45, delay: 0.05 }}
              className="text-[1.65rem] sm:text-4xl md:text-5xl lg:text-6xl font-semibold tracking-tight text-white leading-[1.12]"
            >
              Forecast load, validate models, and plan grid upgrades in one place.
            </motion.h1>
            <motion.p
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.4, delay: 0.12 }}
              className="mt-5 sm:mt-6 text-base sm:text-lg text-zinc-400 leading-relaxed max-w-2xl"
            >
              Voltgent combines batch analytics, ensemble ML inference, and an agentic planner so operations teams can move from raw telemetry to actionable infrastructure decisions without switching tools.
            </motion.p>
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.4, delay: 0.2 }}
              className="mt-8 sm:mt-10 flex flex-col sm:flex-row flex-wrap items-stretch sm:items-center gap-3 sm:gap-4"
            >
              <Link
                to="/batch"
                className="inline-flex items-center gap-2 rounded-xl bg-white text-zinc-950 px-6 py-3 text-sm font-semibold hover:bg-zinc-100 transition-colors"
              >
                Upload data
                <UploadCloud className="h-4 w-4" aria-hidden />
              </Link>
              <Link
                to="/overview"
                className="inline-flex items-center gap-2 rounded-xl border border-white/15 px-6 py-3 text-sm font-medium text-white hover:bg-white/5 transition-colors"
              >
                View live dashboard
                <BarChart3 className="h-4 w-4" aria-hidden />
              </Link>
            </motion.div>
            <div className="mt-12 sm:mt-14 flex flex-wrap gap-6 sm:gap-8 text-sm text-zinc-500 border-t border-white/[0.08] pt-8 sm:pt-10">
              <div className="flex items-center gap-2">
                <Shield className="h-4 w-4 text-emerald-400/90" aria-hidden />
                <span>Workspace runs against your API</span>
              </div>
              <div className="flex items-center gap-2">
                <Zap className="h-4 w-4 text-cyan-400/90" aria-hidden />
                <span>Single-point and batch inference</span>
              </div>
            </div>
          </div>
        </section>

        <section id="product" className="relative z-10 border-t border-white/[0.06] bg-zinc-950/40 py-20 sm:py-24">
          <div className="mx-auto max-w-6xl px-4 sm:px-6">
            <h2 className="text-2xl sm:text-3xl font-semibold text-white tracking-tight">
              Built for operational clarity
            </h2>
            <p className="mt-3 text-zinc-400 max-w-2xl">
              Four connected surfaces share the same data contract: upload once, explore everywhere.
            </p>
            <div className="mt-12 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
              <Feature icon={BarChart3} title="Overview">
                Rolling demand curves, price correlation, and health metrics so you always know how the model behaves on your data.
              </Feature>
              <Feature icon={Zap} title="Predict">
                Adjust lags, price, and grid parameters, then run inference and compare against the daily profile.
              </Feature>
              <Feature icon={UploadCloud} title="Ingest">
                CSV and Excel pipelines with validation charts when labels are present, plus a clear path to downstream planning.
              </Feature>
              <Feature icon={Bot} title="Agent">
                After ingest, trigger the planner to synthesize recommendations and stress scenarios from your batch context.
              </Feature>
            </div>
          </div>
        </section>

        <section className="relative z-10 py-16 sm:py-20">
          <div className="mx-auto max-w-6xl px-4 sm:px-6">
            <div className="rounded-2xl border border-cyan-500/20 bg-gradient-to-br from-cyan-500/10 via-transparent to-violet-600/10 p-8 sm:p-12 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-8">
              <div>
                <h2 className="text-xl sm:text-2xl font-semibold text-white">Ready to open the workspace?</h2>
                <p className="mt-2 text-zinc-400 max-w-xl">
                  Start from overview metrics or go straight to ingest if you already have a telemetry file prepared.
                </p>
              </div>
              <Link
                to="/overview"
                className="inline-flex shrink-0 items-center justify-center gap-2 rounded-xl bg-cyan-500 px-6 py-3 text-sm font-semibold text-zinc-950 hover:bg-cyan-400 transition-colors"
              >
                Enter Voltgent
                <ArrowRight className="h-4 w-4" aria-hidden />
              </Link>
            </div>
          </div>
        </section>
      </main>

      <footer className="relative z-10 border-t border-white/[0.06] py-8">
        <div className="mx-auto max-w-6xl px-4 sm:px-6 flex flex-col sm:flex-row items-center justify-between gap-4 text-sm text-zinc-500">
          <Logo to="/" size="sm" wordmarkClassName="text-sm text-zinc-400" />
          <p>Voltgent. EV demand analytics and planning.</p>
        </div>
      </footer>
    </div>
  );
}
