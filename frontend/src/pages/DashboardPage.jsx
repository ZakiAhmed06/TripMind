import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import {
  Compass,
  Sparkles,
  MapPin,
  Calendar,
  Briefcase,
  TrendingUp,
  ArrowRight,
  Plus,
  Cloud,
  CheckCircle2,
  DollarSign
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import api from '../api/client';
import DestinationCard from '../components/DestinationCard';

export default function DashboardPage() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [trips, setTrips] = useState([]);
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadDashboardData() {
      try {
        const [tripsRes, recsRes] = await Promise.all([
          api.get('/trips'),
          api.post('/recommendations', {
            origin: user?.preferences?.default_origin || 'Delhi',
            budget: 25000,
            duration_days: 4,
            travellers_count: 2,
            interests: user?.preferences?.preferred_categories?.split(',') || ['Mountains', 'Adventure', 'Nature']
          })
        ]);
        setTrips(tripsRes.data);
        setRecommendations(recsRes.data.recommendations.slice(0, 3));
      } catch (err) {
        console.warn('Dashboard data fetch error:', err);
      } finally {
        setLoading(false);
      }
    }
    loadDashboardData();
  }, [user]);

  const upcomingTrips = trips.filter(t => t.status === 'Upcoming');

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Welcome Banner */}
      <div className="relative overflow-hidden p-6 sm:p-8 rounded-3xl bg-gradient-to-r from-slate-900 via-slate-900 to-cyan-950/40 border border-slate-800 shadow-xl flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
        <div className="space-y-2">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-cyan-950/80 border border-cyan-800/60 text-cyan-400 text-xs font-semibold">
            <Sparkles className="w-3.5 h-3.5" />
            TripMind Intelligent Traveler
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-white">
            Welcome back, {user?.full_name || 'Traveler'}!
          </h1>
          <p className="text-xs sm:text-sm text-slate-300 max-w-xl">
            Your personalized AI travel planner has curated ranked recommendations and stands ready to optimize your upcoming travel itineraries.
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-3">
          <Link
            to="/plan"
            className="flex items-center gap-2 px-5 py-2.5 rounded-xl text-xs font-bold text-slate-950 bg-gradient-to-r from-cyan-400 to-blue-400 hover:from-cyan-300 hover:to-blue-300 transition-all shadow-md shadow-cyan-500/20"
          >
            <Plus className="w-4 h-4" />
            Plan New Trip
          </Link>
          <Link
            to="/assistant"
            className="flex items-center gap-2 px-4 py-2.5 rounded-xl text-xs font-semibold text-slate-200 bg-slate-800/80 hover:bg-slate-700 border border-slate-700 transition-colors"
          >
            Ask AI Concierge
          </Link>
        </div>
      </div>

      {/* Metrics Row */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="p-4 rounded-2xl bg-slate-900/80 border border-slate-800">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs">Upcoming Trips</span>
            <Briefcase className="w-4 h-4 text-cyan-400" />
          </div>
          <div className="text-2xl font-extrabold text-white">{upcomingTrips.length}</div>
          <span className="text-[11px] text-slate-500">Active itineraries</span>
        </div>

        <div className="p-4 rounded-2xl bg-slate-900/80 border border-slate-800">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs">Saved Plans</span>
            <CheckCircle2 className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="text-2xl font-extrabold text-white">{trips.length}</div>
          <span className="text-[11px] text-slate-500">Total in My Trips</span>
        </div>

        <div className="p-4 rounded-2xl bg-slate-900/80 border border-slate-800">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs">Recommended</span>
            <Sparkles className="w-4 h-4 text-teal-400" />
          </div>
          <div className="text-2xl font-extrabold text-white">{recommendations.length}</div>
          <span className="text-[11px] text-slate-500">Based on your interests</span>
        </div>

        <div className="p-4 rounded-2xl bg-slate-900/80 border border-slate-800">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs">Preferred Style</span>
            <Compass className="w-4 h-4 text-blue-400" />
          </div>
          <div className="text-sm font-bold text-white truncate">
            {user?.preferences?.travel_style || 'Balanced Explorer'}
          </div>
          <span className="text-[11px] text-slate-500 truncate block">
            {user?.preferences?.preferred_categories?.split(',').slice(0, 2).join(', ') || 'Mountains, Adventure'}
          </span>
        </div>
      </div>

      {/* Upcoming Trips Section */}
      <section className="space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-bold text-white flex items-center gap-2">
            <Calendar className="w-4 h-4 text-cyan-400" />
            Your Upcoming Trips
          </h2>
          <Link to="/trips" className="text-xs text-cyan-400 hover:text-cyan-300 font-semibold">
            View All Trips →
          </Link>
        </div>

        {upcomingTrips.length === 0 ? (
          <div className="p-8 text-center rounded-2xl bg-slate-900/50 border border-slate-800/80 space-y-3">
            <Briefcase className="w-10 h-10 text-slate-600 mx-auto" />
            <h3 className="text-base font-bold text-slate-300">No trips planned yet</h3>
            <p className="text-xs text-slate-400 max-w-sm mx-auto">
              Start planning your next getaway with machine learning destination ranking and expense forecasting.
            </p>
            <Link
              to="/plan"
              className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl text-xs font-bold text-slate-950 bg-cyan-400 hover:bg-cyan-300 transition-colors"
            >
              <Plus className="w-3.5 h-3.5" /> Plan Your First Trip
            </Link>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {upcomingTrips.slice(0, 3).map(trip => (
              <div
                key={trip.id}
                onClick={() => navigate('/itinerary/' + trip.id, { state: { tripData: trip } })}
                className="group p-5 rounded-2xl bg-slate-900/90 border border-slate-800 hover:border-cyan-500/50 transition-all cursor-pointer shadow-lg flex flex-col justify-between"
              >
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-cyan-950 text-cyan-400 border border-cyan-800/60">
                      {trip.status}
                    </span>
                    <span className="text-xs font-semibold text-slate-400">
                      ₹{Math.round(trip.total_budget).toLocaleString()}
                    </span>
                  </div>
                  <h3 className="text-base font-bold text-white group-hover:text-cyan-400 transition-colors">
                    {trip.title}
                  </h3>
                  <div className="flex items-center gap-1 text-xs text-slate-400 mt-1">
                    <MapPin className="w-3.5 h-3.5 text-cyan-500" />
                    <span>{trip.destination_name}</span>
                  </div>
                </div>

                <div className="pt-4 mt-4 border-t border-slate-800 flex items-center justify-between text-xs text-slate-400">
                  <span>{trip.total_days} Days • {trip.travellers_count} Travellers</span>
                  <span className="text-cyan-400 font-semibold group-hover:translate-x-1 transition-transform flex items-center gap-0.5">
                    View <ArrowRight className="w-3 h-3" />
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}
      </section>

      {/* Recommended Destinations */}
      <section className="space-y-4 pt-4">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-lg font-bold text-white flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-cyan-400" />
              Machine Learning Recommendations for You
            </h2>
            <p className="text-xs text-slate-400">Ranked by cosine similarity and budget compatibility</p>
          </div>
          <Link to="/recommendations" className="text-xs text-cyan-400 hover:text-cyan-300 font-semibold">
            See All Ranked Destinations →
          </Link>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {recommendations.map(dest => (
            <DestinationCard key={dest.destination_id} destination={dest} matchScore={dest.match_percentage} />
          ))}
        </div>
      </section>
    </div>
  );
}
