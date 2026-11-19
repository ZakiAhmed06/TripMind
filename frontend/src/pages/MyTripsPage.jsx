import React, { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import {
  Briefcase,
  Calendar,
  MapPin,
  Trash2,
  ArrowRight,
  Plus,
  Compass,
  CheckCircle,
  Clock
} from 'lucide-react';
import api from '../api/client';
import { useAuth } from '../context/AuthContext';

export default function MyTripsPage() {
  const navigate = useNavigate();
  const { user, isAuthenticated } = useAuth();
  const [trips, setTrips] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedFilter, setSelectedFilter] = useState('All');

  useEffect(() => {
    fetchTrips();
  }, []);

  const fetchTrips = async () => {
    setLoading(true);
    try {
      const res = await api.get('/trips');
      setTrips(res.data);
    } catch (err) {
      console.warn('Trips fetch error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteTrip = async (tripId, e) => {
    e.stopPropagation();
    if (!window.confirm('Are you sure you want to delete this trip itinerary?')) return;
    try {
      await api.delete(`/trips/${tripId}`);
      setTrips(trips.filter(t => t.id !== tripId));
    } catch (err) {
      console.warn('Failed to delete trip:', err);
    }
  };

  const filteredTrips = selectedFilter === 'All'
    ? trips
    : trips.filter(t => t.status.toLowerCase() === selectedFilter.toLowerCase());

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Header */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-cyan-950 text-cyan-400 text-xs font-semibold mb-2">
            <Briefcase className="w-3.5 h-3.5" />
            User-Isolated Private Cloud Storage
          </div>
          <h1 className="text-3xl font-extrabold text-white">My Trips</h1>
          <p className="text-xs sm:text-sm text-slate-400 mt-1">
            Access your saved and completed travel itineraries with real-time route maps and expense logs.
          </p>
        </div>

        <Link
          to="/plan"
          className="flex items-center gap-2 px-5 py-2.5 rounded-xl text-xs font-bold text-slate-950 bg-gradient-to-r from-cyan-400 to-blue-400 hover:from-cyan-300 hover:to-blue-300 transition-all shadow-md shadow-cyan-500/20"
        >
          <Plus className="w-4 h-4" />
          Plan New Itinerary
        </Link>
      </div>

      {/* Filter Tabs */}
      <div className="flex items-center gap-2 border-b border-slate-800 pb-2">
        {['All', 'Upcoming', 'Completed', 'Draft'].map((tab) => (
          <button
            key={tab}
            onClick={() => setSelectedFilter(tab)}
            className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold transition-all ${
              selectedFilter === tab
                ? 'bg-slate-800 text-cyan-400 border border-slate-700'
                : 'text-slate-400 hover:text-white'
            }`}
          >
            {tab}
          </button>
        ))}
      </div>

      {/* Trips Grid */}
      {loading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {[1, 2, 3].map(n => (
            <div key={n} className="h-60 rounded-2xl bg-slate-900 border border-slate-800 animate-pulse" />
          ))}
        </div>
      ) : filteredTrips.length === 0 ? (
        <div className="p-12 text-center rounded-2xl bg-slate-900/60 border border-slate-800 space-y-4">
          <Briefcase className="w-12 h-12 text-slate-600 mx-auto" />
          <h3 className="text-lg font-bold text-slate-300">No {selectedFilter !== 'All' ? selectedFilter : ''} trips found</h3>
          <p className="text-xs text-slate-400 max-w-sm mx-auto">
            Design an intelligent itinerary using our Smart Trip Planner, complete with weather-adapted scheduling.
          </p>
          <Link
            to="/plan"
            className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl text-xs font-bold text-slate-950 bg-cyan-400 hover:bg-cyan-300 transition-colors"
          >
            <Plus className="w-3.5 h-3.5" /> Plan a Trip Now
          </Link>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredTrips.map(trip => (
            <div
              key={trip.id}
              onClick={() => navigate(`/itinerary/${trip.id}`, { state: { tripData: trip } })}
              className="group relative p-6 rounded-2xl bg-slate-900/90 hover:bg-slate-800/90 border border-slate-800 hover:border-cyan-500/50 transition-all cursor-pointer shadow-xl flex flex-col justify-between"
            >
              <div>
                <div className="flex items-center justify-between mb-3">
                  <span className={`px-2.5 py-0.5 rounded text-[10px] font-bold ${
                    trip.status === 'Completed'
                      ? 'bg-emerald-950 text-emerald-400 border border-emerald-800'
                      : 'bg-cyan-950 text-cyan-400 border border-cyan-800'
                  }`}>
                    {trip.status}
                  </span>
                  <span className="text-xs font-bold text-white">
                    ₹{Math.round(trip.total_budget).toLocaleString()}
                  </span>
                </div>

                <h3 className="text-lg font-bold text-white group-hover:text-cyan-400 transition-colors">
                  {trip.title}
                </h3>

                <div className="flex items-center gap-1 text-xs text-slate-400 mt-1 mb-3">
                  <MapPin className="w-3.5 h-3.5 text-cyan-400" />
                  <span>{trip.destination_name} ({trip.origin} → {trip.destination_name})</span>
                </div>

                <div className="grid grid-cols-2 gap-2 p-2.5 rounded-xl bg-slate-950 border border-slate-800/80 text-[11px] text-slate-300 mb-4">
                  <div>
                    <span className="text-slate-500 block text-[10px]">Duration</span>
                    <span>{trip.total_days} Days</span>
                  </div>
                  <div>
                    <span className="text-slate-500 block text-[10px]">Travellers</span>
                    <span>{trip.travellers_count} People</span>
                  </div>
                  <div>
                    <span className="text-slate-500 block text-[10px]">Transport</span>
                    <span>{trip.transport_mode}</span>
                  </div>
                  <div>
                    <span className="text-slate-500 block text-[10px]">Hotel Tier</span>
                    <span className="truncate block">{trip.accommodation_type}</span>
                  </div>
                </div>
              </div>

              <div className="pt-3 border-t border-slate-800 flex items-center justify-between text-xs">
                <button
                  onClick={(e) => handleDeleteTrip(trip.id, e)}
                  title="Delete trip"
                  className="p-1.5 rounded-lg text-slate-500 hover:text-red-400 hover:bg-slate-800 transition-colors"
                >
                  <Trash2 className="w-4 h-4" />
                </button>

                <span className="text-cyan-400 font-bold group-hover:translate-x-1 transition-transform flex items-center gap-1">
                  View Itinerary
                  <ArrowRight className="w-3.5 h-3.5" />
                </span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
