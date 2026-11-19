import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import {
  Compass,
  Sparkles,
  ArrowRight,
  TrendingUp,
  CloudRain,
  MapPin,
  ShieldCheck,
  CheckCircle,
  Cpu,
  Zap,
  BarChart3,
  Search
} from 'lucide-react';
import api from '../api/client';
import DestinationCard from '../components/DestinationCard';

export default function LandingPage() {
  const navigate = useNavigate();
  const [featured, setFeatured] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get('/destinations?limit=6')
      .then(res => setFeatured(res.data))
      .catch(err => console.warn('Featured destinations error:', err))
      .finally(() => setLoading(false));
  }, []);

  const handleQuickSearch = (e) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      navigate(`/explore?search=${encodeURIComponent(searchQuery.trim())}`);
    } else {
      navigate('/explore');
    }
  };

  return (
    <div className="flex flex-col min-h-screen">
      {/* Hero Section */}
      <section className="relative overflow-hidden pt-12 pb-24 md:pt-20 md:pb-32 px-4 sm:px-6 lg:px-8">
        {/* Glow gradients background */}
        <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[350px] bg-gradient-to-tr from-cyan-500/15 via-blue-600/15 to-transparent blur-[120px] pointer-events-none -z-10" />

        <div className="max-w-5xl mx-auto text-center space-y-6">
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-cyan-950/60 border border-cyan-800/60 text-cyan-400 text-xs font-semibold backdrop-blur-md animate-fade-in shadow-inner">
            <Sparkles className="w-3.5 h-3.5" />
            Empowered by Scikit-Learn ML & Gemini 2.5 Generative AI
          </div>

          <h1 className="text-4xl sm:text-6xl md:text-7xl font-extrabold tracking-tight text-white leading-tight">
            Your Journey,{' '}
            <span className="bg-gradient-to-r from-cyan-400 via-teal-300 to-blue-400 bg-clip-text text-transparent">
              Intelligently Planned.
            </span>
          </h1>

          <p className="max-w-2xl mx-auto text-base sm:text-lg text-slate-300 leading-relaxed font-normal">
            TripMind unifies traditional Machine Learning and Large Language Models to curate ranked destinations, predict realistic travel expenses, generate day-wise itineraries, and dynamically adapt to weather alerts.
          </p>

          {/* Quick Search & Planning Bar */}
          <div className="max-w-2xl mx-auto pt-4">
            <form onSubmit={handleQuickSearch} className="flex flex-col sm:flex-row items-center gap-2 p-2 rounded-2xl bg-slate-900/90 border border-slate-700/80 shadow-2xl backdrop-blur-md">
              <div className="flex items-center gap-2 px-3 w-full sm:flex-1">
                <Search className="w-5 h-5 text-cyan-400 flex-shrink-0" />
                <input
                  type="text"
                  placeholder="Where do you want to explore? (e.g. Manali, Goa, Munnar)..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full bg-transparent text-sm text-white placeholder-slate-400 focus:outline-none py-2"
                />
              </div>
              <button
                type="submit"
                className="w-full sm:w-auto px-6 py-3 rounded-xl font-bold text-sm text-slate-950 bg-gradient-to-r from-cyan-400 to-blue-400 hover:from-cyan-300 hover:to-blue-300 transition-all shadow-md shadow-cyan-500/20 whitespace-nowrap"
              >
                Search Destinations
              </button>
            </form>
          </div>

          {/* Call to Actions */}
          <div className="flex flex-wrap items-center justify-center gap-3 pt-2">
            <Link
              to="/plan"
              className="flex items-center gap-2 px-6 py-3 rounded-xl text-sm font-bold text-slate-950 bg-gradient-to-r from-cyan-400 to-teal-400 hover:from-cyan-300 hover:to-teal-300 transition-all shadow-lg shadow-cyan-500/20"
            >
              <Sparkles className="w-4 h-4" />
              Launch Smart Trip Planner
              <ArrowRight className="w-4 h-4" />
            </Link>
            <Link
              to="/explore"
              className="px-6 py-3 rounded-xl text-sm font-semibold text-slate-200 bg-slate-900/80 hover:bg-slate-800 border border-slate-700/80 transition-all"
            >
              Browse 300+ Indian Destinations
            </Link>
          </div>

          {/* Quick Metrics */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 pt-10 max-w-3xl mx-auto border-t border-slate-800/80">
            <div>
              <div className="text-2xl sm:text-3xl font-extrabold text-white">315+</div>
              <div className="text-xs text-slate-400">Curated Destinations</div>
            </div>
            <div>
              <div className="text-2xl sm:text-3xl font-extrabold text-cyan-400">98.3%</div>
              <div className="text-xs text-slate-400">ML Budget R² Accuracy</div>
            </div>
            <div>
              <div className="text-2xl sm:text-3xl font-extrabold text-teal-400">1,500+</div>
              <div className="text-xs text-slate-400">Catalogued Sights</div>
            </div>
            <div>
              <div className="text-2xl sm:text-3xl font-extrabold text-blue-400">Instant</div>
              <div className="text-xs text-slate-400">Dynamic Replanning</div>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="py-16 bg-slate-900/40 border-y border-slate-800/80 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="text-center max-w-2xl mx-auto mb-12">
            <h2 className="text-xs font-bold text-cyan-400 tracking-wider uppercase mb-2">Architectural Workflow</h2>
            <h3 className="text-3xl font-extrabold text-white">How TripMind Works</h3>
            <p className="text-sm text-slate-400 mt-2">
              Combining Scikit-Learn predictive modeling and Google Gemini Generative AI for verified, grounded travel itineraries.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {/* Step 1 */}
            <div className="relative p-6 rounded-2xl bg-slate-900/90 border border-slate-800 hover:border-cyan-500/40 transition-all group shadow-xl">
              <div className="w-12 h-12 rounded-xl bg-cyan-950/80 border border-cyan-700/50 flex items-center justify-center text-cyan-400 mb-4 group-hover:scale-110 transition-transform">
                <Compass className="w-6 h-6" />
              </div>
              <div className="text-xs font-bold text-cyan-400 mb-1">STEP 01</div>
              <h4 className="text-lg font-bold text-white mb-2">Content-Based ML Ranking</h4>
              <p className="text-xs text-slate-400 leading-relaxed">
                Our recommendation engine transforms your travel interests, duration, and budget into multi-attribute feature vectors, matching them using cosine similarity with 300+ destinations.
              </p>
            </div>

            {/* Step 2 */}
            <div className="relative p-6 rounded-2xl bg-slate-900/90 border border-slate-800 hover:border-blue-500/40 transition-all group shadow-xl">
              <div className="w-12 h-12 rounded-xl bg-blue-950/80 border border-blue-700/50 flex items-center justify-center text-blue-400 mb-4 group-hover:scale-110 transition-transform">
                <BarChart3 className="w-6 h-6" />
              </div>
              <div className="text-xs font-bold text-blue-400 mb-1">STEP 02</div>
              <h4 className="text-lg font-bold text-white mb-2">Random Forest Expense & Crowd ML</h4>
              <p className="text-xs text-slate-400 leading-relaxed">
                Trained Random Forest models predict realistic travel expenses and crowd footfalls across transit modes, hotel categories, seasons, and days—verified by backend logic.
              </p>
            </div>

            {/* Step 3 */}
            <div className="relative p-6 rounded-2xl bg-slate-900/90 border border-slate-800 hover:border-teal-500/40 transition-all group shadow-xl">
              <div className="w-12 h-12 rounded-xl bg-teal-950/80 border border-teal-700/50 flex items-center justify-center text-teal-400 mb-4 group-hover:scale-110 transition-transform">
                <Sparkles className="w-6 h-6" />
              </div>
              <div className="text-xs font-bold text-teal-400 mb-1">STEP 03</div>
              <h4 className="text-lg font-bold text-white mb-2">GenAI + RAG & Dynamic Weather Replan</h4>
              <p className="text-xs text-slate-400 leading-relaxed">
                Gemini 2.5 Flash constructs structured day-wise plans grounded in FAISS vector knowledge. If weather APIs report heavy rainfall, the system automatically adapts to indoor sights.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Featured Destinations */}
      <section className="py-16 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto w-full">
        <div className="flex flex-col sm:flex-row items-start sm:items-end justify-between gap-4 mb-8">
          <div>
            <h2 className="text-xs font-bold text-cyan-400 tracking-wider uppercase mb-1">Top Recommendations</h2>
            <h3 className="text-2xl sm:text-3xl font-extrabold text-white">Popular Destinations in India</h3>
          </div>
          <Link
            to="/explore"
            className="flex items-center gap-1.5 text-xs font-semibold text-cyan-400 hover:text-cyan-300"
          >
            Explore all 300+ destinations
            <ArrowRight className="w-4 h-4" />
          </Link>
        </div>

        {loading ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {[1, 2, 3, 4, 5, 6].map(n => (
              <div key={n} className="h-72 rounded-2xl bg-slate-900 border border-slate-800 animate-pulse" />
            ))}
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {featured.map(dest => (
              <DestinationCard key={dest.id} destination={dest} />
            ))}
          </div>
        )}
      </section>

      {/* Standout Features Grid */}
      <section className="py-16 bg-slate-900/60 border-t border-slate-800 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="text-center max-w-2xl mx-auto mb-12">
            <h3 className="text-2xl sm:text-3xl font-extrabold text-white">Why TripMind Outperforms Traditional Planners</h3>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <div className="p-5 rounded-xl bg-slate-950 border border-slate-800/80">
              <Cpu className="w-6 h-6 text-cyan-400 mb-3" />
              <h4 className="font-bold text-white text-sm mb-1.5">No LLM Financial Hallucinations</h4>
              <p className="text-xs text-slate-400 leading-relaxed">
                Trip budgets are evaluated by trained Scikit-Learn Regressors and verified by backend mathematical sanity logic.
              </p>
            </div>
            <div className="p-5 rounded-xl bg-slate-950 border border-slate-800/80">
              <CloudRain className="w-6 h-6 text-blue-400 mb-3" />
              <h4 className="font-bold text-white text-sm mb-1.5">Dynamic Weather Adaptation</h4>
              <p className="text-xs text-slate-400 leading-relaxed">
                Integrates Open-Meteo live forecasts to replace outdoor hikes with cultural galleries when rainfall is forecast.
              </p>
            </div>
            <div className="p-5 rounded-xl bg-slate-950 border border-slate-800/80">
              <Zap className="w-6 h-6 text-teal-400 mb-3" />
              <h4 className="font-bold text-white text-sm mb-1.5">FAISS Grounded RAG</h4>
              <p className="text-xs text-slate-400 leading-relaxed">
                Retrieves verified facts, safety advisories, and cultural background from indexed regional documents.
              </p>
            </div>
            <div className="p-5 rounded-xl bg-slate-950 border border-slate-800/80">
              <TrendingUp className="w-6 h-6 text-emerald-400 mb-3" />
              <h4 className="font-bold text-white text-sm mb-1.5">Route TSP Optimization</h4>
              <p className="text-xs text-slate-400 leading-relaxed">
                Uses Haversine distance matrices and 2-opt search heuristics to order sights sequentially and minimize transit time.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Final Call to Action */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 text-center max-w-4xl mx-auto">
        <div className="p-8 sm:p-12 rounded-3xl bg-gradient-to-r from-cyan-950/40 via-blue-950/40 to-slate-900 border border-cyan-800/40 shadow-2xl space-y-4">
          <h2 className="text-3xl sm:text-4xl font-extrabold text-white">Ready for your next unforgettable journey?</h2>
          <p className="text-sm text-slate-300 max-w-xl mx-auto">
            Design your personalized, ML-budgeted travel plan in under 60 seconds.
          </p>
          <div className="pt-2">
            <Link
              to="/plan"
              className="inline-flex items-center gap-2 px-8 py-3.5 rounded-xl font-bold text-sm text-slate-950 bg-gradient-to-r from-cyan-400 to-blue-400 hover:from-cyan-300 hover:to-blue-300 transition-all shadow-lg shadow-cyan-500/25"
            >
              Start Planning Now
              <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
}
