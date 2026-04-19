import React, { useMemo, useState } from 'react';
import { Link } from 'react-router-dom';
import {
  AlertTriangle,
  ShieldCheck,
  CheckCircle,
  Database,
  Bot,
  ArrowRight,
  Loader2,
  Sparkles,
} from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import { runAgentPlanner } from '../api/client';
import GlassCard from '../components/GlassCard';
import StatCard from '../components/StatCard';
import { PageMotion } from '../components/PageMotion';
import { chartTooltipProps } from '../lib/chartTheme';
import { useDataContext } from '../App';

const BAR_COLORS = ['#22d3ee', '#a855f7', '#34d399'];

const AgentPlanner = () => {
  const { dataUploaded } = useDataContext();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleRunAgent = async () => {
    setLoading(true);
    setError(null);
    try {
      const result = await runAgentPlanner();
      setData(result);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          'Agent request failed. Ensure batch data was processed and the API is running.'
      );
    } finally {
      setLoading(false);
    }
  };

  const scoreBars = useMemo(() => {
    if (!data?.final_plan) return [];
    const { final_plan, iteration_count, simulated_impact } = data;
    const conf = (final_plan.confidence_score || 0) * 100;
    const rob = (simulated_impact?.robustness_score || 0) * 100;
    const loops = Math.min(100, (iteration_count || 0) * 25);
    return [
      { name: 'Plan confidence', value: Math.round(conf * 10) / 10 },
      { name: 'Stress robustness', value: Math.round(rob * 10) / 10 },
      { name: 'Iteration budget', value: Math.round(loops * 10) / 10 },
    ];
  }, [data]);

  if (!dataUploaded && !data) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[55vh] text-center page-transition px-4">
        <div className="rounded-2xl border border-red-500/25 bg-red-500/10 p-5 mb-8">
          <AlertTriangle className="w-10 h-10 text-red-400" aria-hidden />
        </div>
        <h1 className="text-2xl sm:text-3xl font-semibold tracking-tight text-white mb-3">Process data first</h1>
        <p className="text-zinc-400 max-w-lg mb-8 leading-relaxed">
          The planner reasons over batch predictions. Upload and run the ingest pipeline, then return here.
        </p>
        <Link
          to="/batch"
          className="inline-flex items-center gap-2 rounded-xl border border-cyan-500/40 bg-cyan-500/10 px-6 py-3 text-sm font-semibold text-cyan-300 hover:bg-cyan-500/20 transition-colors"
        >
          Go to ingest
          <ArrowRight className="w-4 h-4" aria-hidden />
        </Link>
      </div>
    );
  }

  if (!data && !loading && !error) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[55vh] text-center page-transition px-4">
        <div className="rounded-2xl border border-violet-500/30 bg-violet-500/10 p-6 mb-8 relative">
          <Bot className="w-12 h-12 text-violet-300" aria-hidden />
        </div>
        <h1 className="text-2xl sm:text-3xl font-semibold tracking-tight text-white mb-3">Infrastructure agent</h1>
        <p className="text-zinc-400 max-w-xl mb-10 leading-relaxed">
          LangGraph-style orchestration with retrieval and simulated stress checks. Runs on your processed batch context.
        </p>
        <button
          type="button"
          onClick={handleRunAgent}
          className="inline-flex items-center gap-2 rounded-xl bg-violet-500/20 border border-violet-500/45 px-8 py-3 text-sm font-semibold text-violet-100 hover:bg-violet-500/30 transition-colors"
        >
          <Sparkles className="w-4 h-4" aria-hidden />
          Run agent
        </button>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="min-h-[50vh] flex flex-col items-center justify-center gap-4">
        <Loader2 className="h-12 w-12 text-cyan-400 animate-spin" aria-hidden />
        <p className="text-sm text-zinc-400">Agent is reasoning</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex flex-col items-center justify-center p-12 text-center page-transition max-w-lg mx-auto">
        <AlertTriangle className="w-14 h-14 text-red-400 mb-4" aria-hidden />
        <h2 className="text-xl font-semibold text-white mb-2">Run failed</h2>
        <p className="text-zinc-400 mb-8 leading-relaxed">{error}</p>
        <button type="button" onClick={() => setError(null)} className="btn-glow text-sm">
          Dismiss
        </button>
      </div>
    );
  }

  const { insights, reasoning, final_plan, retrieved_knowledge, iteration_count, simulated_impact } = data;

  return (
    <PageMotion className="space-y-6 sm:space-y-8 page-transition pb-12 sm:pb-16">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <h1 className="text-3xl font-semibold tracking-tight text-white">Agent output</h1>
          <p className="text-zinc-400 mt-2 max-w-2xl leading-relaxed">
            Consolidated recommendations and stress context from the latest run.
          </p>
        </div>
        <button
          type="button"
          onClick={handleRunAgent}
          disabled={loading}
          className="inline-flex items-center gap-2 rounded-xl border border-white/15 px-4 py-2 text-sm font-medium text-zinc-200 hover:bg-white/5 transition-colors shrink-0"
        >
          {loading ? <Loader2 className="w-4 h-4 animate-spin" aria-hidden /> : <Sparkles className="w-4 h-4" aria-hidden />}
          Rerun
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <StatCard
          title="Risk level"
          value={final_plan.risk_level || 'Unknown'}
          icon={AlertTriangle}
          color={final_plan.risk_level === 'High' ? 'orange' : 'cyan'}
        />
        <StatCard
          title="Plan confidence"
          value={`${((final_plan.confidence_score || 0) * 100).toFixed(1)}%`}
          icon={ShieldCheck}
          color={final_plan.confidence_score > 0.8 ? 'green' : 'orange'}
        />
        <StatCard
          title="Optimization loops"
          value={iteration_count?.toString() || '0'}
          icon={Bot}
          color="magenta"
        />
      </div>

      {scoreBars.length > 0 && (
        <GlassCard title="Run scores" icon={Sparkles} className="min-h-[300px]">
          <div className="h-[260px] w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={scoreBars} margin={{ top: 8, right: 8, left: 0, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" opacity={0.35} />
                <XAxis dataKey="name" stroke="#71717a" tick={{ fill: '#a1a1aa', fontSize: 11 }} interval={0} />
                <YAxis stroke="#71717a" tick={{ fill: '#a1a1aa', fontSize: 11 }} domain={[0, 100]} />
                <Tooltip {...chartTooltipProps} />
                <Bar dataKey="value" radius={[6, 6, 0, 0]} name="Score">
                  {scoreBars.map((_, i) => (
                    <Cell key={i} fill={BAR_COLORS[i % BAR_COLORS.length]} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
          <p className="text-xs text-zinc-500 mt-2">
            Confidence and robustness are percentages. Iteration budget is a normalized view of loop count.
          </p>
        </GlassCard>
      )}

      {insights && Array.isArray(insights) && insights.length > 0 && (
        <GlassCard title="Insights" icon={CheckCircle}>
          <ul className="space-y-2">
            {insights.map((line, i) => (
              <li key={i} className="text-sm text-zinc-300 leading-relaxed pl-4 border-l-2 border-cyan-500/35">
                {line}
              </li>
            ))}
          </ul>
        </GlassCard>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        <GlassCard title="Reasoning trace" className="lg:col-span-8 border-cyan-500/15">
          <div className="space-y-4">
            <div className="p-4 bg-black/40 rounded-xl border border-white/5">
              <h4 className="text-sm font-semibold text-cyan-400 mb-3 uppercase tracking-wider flex items-center gap-2">
                <CheckCircle className="w-4 h-4" aria-hidden />
                Observations
              </h4>
              <ul className="list-disc list-inside text-sm text-zinc-300 space-y-1.5 ml-1">
                {(reasoning.observations || []).map((o, i) => (
                  <li key={i} className="leading-relaxed">
                    {o}
                  </li>
                ))}
              </ul>
            </div>

            <div className="p-4 bg-black/40 rounded-xl border border-white/5">
              <h4 className="text-sm font-semibold text-violet-400 mb-3 uppercase tracking-wider flex items-center gap-2">
                <Database className="w-4 h-4" aria-hidden />
                Inferences
              </h4>
              <ul className="list-disc list-inside text-sm text-zinc-300 space-y-1.5 ml-1">
                {(reasoning.inferences || []).map((inf, i) => (
                  <li key={i} className="leading-relaxed">
                    {inf}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </GlassCard>

        <div className="lg:col-span-4 flex flex-col gap-6">
          <GlassCard title="Retrieved knowledge" className="flex-1 bg-gradient-to-b from-black/50 to-black/30 border-t border-cyan-500/20">
            <div className="space-y-3 max-h-[320px] overflow-y-auto pr-1 custom-scrollbar">
              {(retrieved_knowledge || []).map((k, i) => (
                <div
                  key={i}
                  className="pl-3 border-l-2 border-cyan-500/35 text-xs text-zinc-400 font-mono leading-relaxed"
                >
                  {k}
                </div>
              ))}
            </div>
          </GlassCard>

          <GlassCard title="Stress simulation" className="border-t border-amber-500/25">
            <div className="space-y-4">
              <div>
                <p className="text-xs text-zinc-500 uppercase font-semibold tracking-wide">Scenario</p>
                <p className="text-sm text-white font-medium mt-1">{simulated_impact?.scenario || 'N/A'}</p>
              </div>
              <div>
                <p className="text-xs text-zinc-500 uppercase font-semibold tracking-wide">Impact</p>
                <p className="text-sm text-zinc-300 mt-1 leading-relaxed">{simulated_impact?.impact_analysis || 'N/A'}</p>
              </div>
              <div className="pt-3 border-t border-white/5 flex items-center justify-between">
                <span className="text-xs text-zinc-500 uppercase font-semibold tracking-wide">Robustness</span>
                <span className="text-lg font-semibold text-emerald-400 tabular-nums">
                  {((simulated_impact?.robustness_score || 0) * 100).toFixed(1)}%
                </span>
              </div>
            </div>
          </GlassCard>
        </div>

        <GlassCard
          title="Recommendations"
          className="lg:col-span-12 border-violet-500/25 bg-violet-950/20"
        >
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {(final_plan.recommendations || []).map((rec, idx) => (
              <div
                key={idx}
                className="bg-black/50 border border-white/10 rounded-xl p-5 relative overflow-hidden group hover:border-violet-500/35 transition-colors"
              >
                <div className="absolute top-0 right-0 px-3 py-1 bg-white/5 rounded-bl-xl text-xs font-semibold uppercase tracking-wider text-zinc-500 group-hover:bg-violet-500/15 group-hover:text-violet-200 transition-colors">
                  {(rec.priority || 'Normal') + ' priority'}
                </div>

                <h4 className="text-lg font-semibold text-white mb-1 flex items-center gap-2 mt-2">
                  <span className="w-7 h-7 rounded-lg bg-violet-500/20 text-violet-300 flex items-center justify-center text-xs border border-violet-500/40 font-mono">
                    {String(idx + 1).padStart(2, '0')}
                  </span>
                  {(rec.type || 'Action').replace(/_/g, ' ')}
                </h4>

                <p className="text-sm text-cyan-400/90 font-mono mb-4">{rec.location}</p>

                <div className="space-y-3">
                  <div>
                    <span className="text-xs text-zinc-500 uppercase block mb-1">Execution</span>
                    <p className="text-sm text-zinc-200 leading-relaxed">{rec.action}</p>
                  </div>
                  <div className="pl-3 border-l-2 border-zinc-700">
                    <span className="text-xs text-zinc-500 uppercase block mb-1">Justification</span>
                    <p className="text-sm text-zinc-400 leading-relaxed">{rec.justification}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </GlassCard>
      </div>
    </PageMotion>
  );
};

export default AgentPlanner;
