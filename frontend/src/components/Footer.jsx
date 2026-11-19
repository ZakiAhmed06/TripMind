import React from 'react';
import { Compass, Heart, Github, ExternalLink, ShieldCheck, Cpu } from 'lucide-react';

export default function Footer() {
  return (
    <footer className="bg-slate-950 border-t border-slate-800/80 text-slate-400 py-12 px-4 sm:px-6 lg:px-8 mt-auto">
      <div className="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
        {/* Brand */}
        <div className="md:col-span-1 space-y-3">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-tr from-cyan-500 to-blue-600 flex items-center justify-center">
              <Compass className="w-5 h-5 text-white" />
            </div>
            <span className="text-lg font-bold text-white tracking-tight">TripMind</span>
          </div>
          <p className="text-xs leading-relaxed text-slate-400">
            Intelligent travel planning combining Scikit-Learn Machine Learning, Google Gemini Generative AI, and live Open-Meteo weather integrations.
          </p>
          <div className="flex items-center gap-2 text-xs text-cyan-400">
            <Cpu className="w-4 h-4" />
            <span>AI + ML Architecture</span>
          </div>
        </div>

        {/* Modules */}
        <div>
          <h4 className="text-sm font-semibold text-slate-200 uppercase tracking-wider mb-3">AI / ML Engines</h4>
          <ul className="space-y-2 text-xs">
            <li>Content-Based Destination Ranking</li>
            <li>Random Forest Expense Predictor</li>
            <li>Crowd Density Classifier</li>
            <li>FAISS Vector RAG Search</li>
            <li>Dynamic Weather Replanning</li>
          </ul>
        </div>

        {/* Navigation */}
        <div>
          <h4 className="text-sm font-semibold text-slate-200 uppercase tracking-wider mb-3">Explore</h4>
          <ul className="space-y-2 text-xs">
            <li><a href="/explore" className="hover:text-cyan-400 transition-colors">Destinations Directory</a></li>
            <li><a href="/plan" className="hover:text-cyan-400 transition-colors">Smart Trip Planner</a></li>
            <li><a href="/assistant" className="hover:text-cyan-400 transition-colors">AI Concierge Assistant</a></li>
            <li><a href="/trips" className="hover:text-cyan-400 transition-colors">Saved Itineraries</a></li>
          </ul>
        </div>

        {/* Engineering Specs */}
        <div>
          <h4 className="text-sm font-semibold text-slate-200 uppercase tracking-wider mb-3">Technology Stack</h4>
          <div className="flex flex-wrap gap-1.5 text-[11px]">
            <span className="px-2 py-0.5 rounded bg-slate-900 border border-slate-800 text-slate-300">FastAPI</span>
            <span className="px-2 py-0.5 rounded bg-slate-900 border border-slate-800 text-slate-300">React + Vite</span>
            <span className="px-2 py-0.5 rounded bg-slate-900 border border-slate-800 text-slate-300">Scikit-Learn</span>
            <span className="px-2 py-0.5 rounded bg-slate-900 border border-slate-800 text-slate-300">Gemini 2.5</span>
            <span className="px-2 py-0.5 rounded bg-slate-900 border border-slate-800 text-slate-300">FAISS</span>
            <span className="px-2 py-0.5 rounded bg-slate-900 border border-slate-800 text-slate-300">Leaflet</span>
            <span className="px-2 py-0.5 rounded bg-slate-900 border border-slate-800 text-slate-300">PostgreSQL</span>
          </div>
          <p className="text-[11px] text-slate-500 mt-3 flex items-center gap-1">
            <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
            Isolated user authentication via JWT & bcrypt
          </p>
        </div>
      </div>

      <div className="max-w-7xl mx-auto pt-6 border-t border-slate-800/60 flex flex-col sm:flex-row items-center justify-between text-xs text-slate-400 gap-3">
        <p>© 2026 TripMind Platform. Production-Grade Portfolio & Final-Year Engineering Project.</p>
        <p className="flex items-center gap-1">
          Designed with <Heart className="w-3.5 h-3.5 text-rose-500 fill-rose-500" /> for intelligent exploration
        </p>
      </div>
    </footer>
  );
}
