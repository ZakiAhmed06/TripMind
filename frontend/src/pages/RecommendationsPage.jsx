import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Sparkles, Compass, Filter, ArrowRight } from 'lucide-react';
import api from '../api/client';
import DestinationCard from '../components/DestinationCard';
import { useAuth } from '../context/AuthContext';

export default function RecommendationsPage() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [budget, setBudget] = useState(25000);
  const [duration, setDuration] = useState(4);
  const [interests, setInterests] = useState(['Mountains', 'Adventure', 'Nature']);

  useEffect(() => {
    fetchRecommendations();
  }, [budget, duration]);

  const fetchRecommendations = async () => {
    setLoading(true);
    try {
      const res = await api.post('/recommendations', {
        origin: user?.preferences?.default_origin || 'Delhi',
        budget: budget,
        duration_days: duration,
        travellers_count: 2,
        interests: interests
      });
      setRecommendations(res.data.recommendations);
    } catch (err) {
      console.warn('Recommendation fetch error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      <div>
        <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-cyan-950 text-cyan-400 text-xs font-semibold mb-2">
          <Sparkles className="w-3.5 h-3.5" />
          Ranked via Content-Based Cosine Similarity & Attribute Weighting
        </div>
        <h1 className="text-3xl font-extrabold text-white">Recommended Destinations</h1>
        <p className="text-sm text-slate-400 max-w-2xl mt-1">
          Our machine learning algorithm ranks these destinations according to interest alignment, budget feasibility, and climate suitability.
        </p>
      </div>

      {/* Quick Filter Bar */}
      <div className="p-4 rounded-2xl bg-slate-900/90 border border-slate-800 flex flex-wrap items-center justify-between gap-4 text-xs">
        <div className="flex flex-wrap items-center gap-4">
          <div>
            <span className="text-slate-400 block mb-1">Target Budget</span>
            <select
              value={budget}
              onChange={(e) => setBudget(Number(e.target.value))}
              className="bg-slate-950 border border-slate-800 rounded-lg px-2.5 py-1.5 text-white"
            >
              <option value="15000">₹15,000 (Budget)</option>
              <option value="25000">₹25,000 (Standard)</option>
              <option value="40000">₹40,000 (Premium)</option>
              <option value="60000">₹60,000 (Luxury)</option>
            </select>
          </div>

          <div>
            <span className="text-slate-400 block mb-1">Duration</span>
            <select
              value={duration}
              onChange={(e) => setDuration(Number(e.target.value))}
              className="bg-slate-950 border border-slate-800 rounded-lg px-2.5 py-1.5 text-white"
            >
              <option value="3">3 Days (Weekend)</option>
              <option value="4">4 Days (Standard)</option>
              <option value="6">6 Days (Extended)</option>
            </select>
          </div>
        </div>

        <button
          onClick={() => navigate('/plan')}
          className="px-4 py-2 rounded-xl text-xs font-bold text-slate-950 bg-cyan-400 hover:bg-cyan-300 transition-colors flex items-center gap-1.5"
        >
          Customize in Trip Planner
          <ArrowRight className="w-3.5 h-3.5" />
        </button>
      </div>

      {/* Cards Grid */}
      {loading ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {[1, 2, 3, 4, 5, 6].map(n => (
            <div key={n} className="h-72 rounded-2xl bg-slate-900 border border-slate-800 animate-pulse" />
          ))}
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {recommendations.map(dest => (
            <DestinationCard
              key={dest.destination_id}
              destination={dest}
              matchScore={dest.match_percentage}
            />
          ))}
        </div>
      )}
    </div>
  );
}
