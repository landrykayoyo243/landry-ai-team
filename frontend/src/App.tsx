export default function App() {
  return (
    <main className="min-h-screen bg-slate-950 text-slate-100">
      <div className="mx-auto flex max-w-5xl flex-col gap-8 px-6 py-20">
        <header className="rounded-2xl border border-slate-800 bg-slate-900/80 p-6 shadow-xl shadow-slate-950/40">
          <p className="text-sm uppercase tracking-[0.2em] text-cyan-400">LANDRY AI TEAM</p>
          <h1 className="mt-4 text-4xl font-bold">Multi-agents platform</h1>
          <p className="mt-3 max-w-2xl text-slate-300">
            Manager, Coder et Reviewer collaborent pour analyser, développer, auditer et livrer des projets logiciels.
          </p>
        </header>

        <section className="grid gap-6 md:grid-cols-3">
          <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6">
            <p className="text-sm uppercase tracking-widest text-violet-400">Manager</p>
            <h2 className="mt-3 text-xl font-semibold">Clarification & orchestration</h2>
          </div>
          <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6">
            <p className="text-sm uppercase tracking-widest text-emerald-400">Coder</p>
            <h2 className="mt-3 text-xl font-semibold">Implementation & tests</h2>
          </div>
          <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6">
            <p className="text-sm uppercase tracking-widest text-amber-400">Reviewer</p>
            <h2 className="mt-3 text-xl font-semibold">Audit & validation</h2>
          </div>
        </section>
      </div>
    </main>
  );
}
