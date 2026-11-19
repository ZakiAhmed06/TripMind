import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import {
  Compass,
  Search,
  Filter,
  MapPin,
  Calendar,
  X,
  Clock,
  Ticket,
  Sun,
  Shield,
  Sparkles,
  ArrowRight
} from 'lucide-react';
import api from '../api/client';
import DestinationCard from '../components/DestinationCard';
import WeatherBadge from '../components/WeatherBadge';

const CATEGORIES = [
  'All',
  'Mountains',
  'Beaches',
  'Heritage',
  'Adventure',
  'Wildlife',
  'Spiritual',
  'Nature',
  'Culture',
  'Nightlife',
  'Food',
  'Photography'
];

const STATES = [
  'All',
  'Himachal Pradesh',
  'Uttarakhand',
  'Rajasthan',
  'Goa',
  'Kerala',
  'Karnataka',
  'Tamil Nadu',
  'West Bengal',
  'Sikkim',
  'Meghalaya',
  'Assam',
  'Arunachal Pradesh',
  'Ladakh',
  'Jammu and Kashmir',
  'Maharashtra',
  'Madhya Pradesh',
  'Gujarat',
  'Odisha'
];

export default function ExplorePage() {
  const location = useLocation();
  const searchParams = new URLSearchParams(location.search);
  const initialSearch = searchParams.get('search') || '';

  const [destinations, setDestinations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState(initialSearch);
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [selectedState, setSelectedState] = useState('All');
  const [maxBudget, setMaxBudget] = useState(5000);
  const [selectedDestinationDetail, setSelectedDestinationDetail] = useState(null);
  const [loadingModal, setLoadingModal] = useState(false);

  useEffect(() => {
    fetchDestinations();
  }, [selectedCategory, selectedState, maxBudget]);

  const fetchDestinations = async () => {
    setLoading(true);
    try {
      const params = {
        limit: 100,
        category: selectedCategory !== 'All' ? selectedCategory : undefined,
        state: selectedState !== 'All' ? selectedState : undefined,
        max_budget: maxBudget,
        query: searchTerm.trim() || undefined
      };
      const res = await api.get('/destinations', { params });
      setDestinations(res.data);
    } catch (err) {
      console.warn('Destinations fetch error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    fetchDestinations();
  };

  const handleOpenDetails = async (dest) => {
    setLoadingModal(true);
    try {
      const res = await api.get(`/destinations/${dest.id || dest.destination_id}`);
      setSelectedDestinationDetail(res.data);
    } catch (err) {
      console.warn('Detail fetch error:', err);
    } finally {
      setLoadingModal(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Page Header */}
      <div>
        <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-cyan-950 text-cyan-400 text-xs font-semibold mb-2">
          <Compass className="w-3.5 h-3.5" />
          Catalog of 300+ Verified Indian Destinations
        </div>
        <h1 className="text-3xl font-extrabold text-white">Explore Destinations</h1>
        <p className="text-sm text-slate-400 max-w-2xl mt-1">
          Discover vetted tourist gems across Indian states, filter by travel style, budget, and season, and inspect verified local attractions.
        </p>
      </div>

      {/* Filter and Search Bar */}
      <div className="p-5 rounded-2xl bg-slate-900/90 border border-slate-800 shadow-xl space-y-4">
        {/* Search input */}
        <form onSubmit={handleSearchSubmit} className="flex gap-2">
          <div className="relative flex-1">
            <Search className="w-4 h-4 text-slate-500 absolute left-3.5 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              placeholder="Search by name, state, or keywords (e.g. Manali, Tea gardens, Forts)..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 focus:border-cyan-500 rounded-xl py-2.5 pl-10 pr-3 text-sm text-white placeholder-slate-500 focus:outline-none transition-colors"
            />
          </div>
          <button
            type="submit"
            className="px-5 py-2.5 rounded-xl font-bold text-xs text-slate-950 bg-gradient-to-r from-cyan-400 to-blue-400 hover:from-cyan-300 hover:to-blue-300 transition-all shadow-md shadow-cyan-500/20"
          >
            Search
          </button>
        </form>

        {/* Dropdowns and Budget Slider */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 pt-2 border-t border-slate-800/80">
          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1.5">State / Region</label>
            <select
              value={selectedState}
              onChange={(e) => setSelectedState(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-xl py-2 px-3 text-xs text-white focus:outline-none focus:border-cyan-500"
            >
              {STATES.map(s => <option key={s} value={s}>{s}</option>)}
            </select>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1.5">Category</label>
            <select
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-xl py-2 px-3 text-xs text-white focus:outline-none focus:border-cyan-500"
            >
              {CATEGORIES.map(c => <option key={c} value={c}>{c}</option>)}
            </select>
          </div>

          <div>
            <div className="flex items-center justify-between text-xs font-semibold text-slate-300 mb-1.5">
              <span>Max Daily Budget</span>
              <span className="text-cyan-400 font-bold">₹{maxBudget.toLocaleString()}/day</span>
            </div>
            <input
              type="range"
              min="1500"
              max="6000"
              step="250"
              value={maxBudget}
              onChange={(e) => setMaxBudget(Number(e.target.value))}
              className="w-full accent-cyan-400 cursor-pointer"
            />
          </div>
        </div>

        {/* Category Pills */}
        <div className="flex items-center gap-1.5 overflow-x-auto pb-1 pt-1 no-scrollbar">
          {CATEGORIES.map((cat) => {
            const isSelected = selectedCategory === cat;
            return (
              <button
                key={cat}
                onClick={() => setSelectedCategory(cat)}
                className={`px-3 py-1 rounded-lg text-xs font-semibold whitespace-nowrap transition-all ${
                  isSelected
                    ? 'bg-cyan-500 text-slate-950 shadow-sm'
                    : 'bg-slate-950 text-slate-400 hover:text-white border border-slate-800'
                }`}
              >
                {cat}
              </button>
            );
          })}
        </div>
      </div>

      {/* Results Header */}
      <div className="flex items-center justify-between text-xs text-slate-400">
        <span>Showing <strong className="text-white">{destinations.length}</strong> matching destinations</span>
        <span>Sorted by popularity rating</span>
      </div>

      {/* Cards Grid */}
      {loading ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {[1, 2, 3, 4, 5, 6].map(n => (
            <div key={n} className="h-72 rounded-2xl bg-slate-900 border border-slate-800 animate-pulse" />
          ))}
        </div>
      ) : destinations.length === 0 ? (
        <div className="p-12 text-center rounded-2xl bg-slate-900/60 border border-slate-800 space-y-3">
          <Compass className="w-10 h-10 text-slate-600 mx-auto" />
          <h3 className="text-base font-bold text-slate-300">No destinations found</h3>
          <p className="text-xs text-slate-400">Try broadening your search term or adjusting your budget slider.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {destinations.map(dest => (
            <DestinationCard
              key={dest.id}
              destination={dest}
              onSelectDetails={handleOpenDetails}
            />
          ))}
        </div>
      )}

      {/* Destination Attractions Modal */}
      {selectedDestinationDetail && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm animate-fade-in">
          <div className="relative w-full max-w-2xl max-h-[85vh] overflow-y-auto rounded-2xl bg-slate-900 border border-slate-700 shadow-2xl p-6 space-y-5">
            {/* Modal Header */}
            <div className="flex items-start justify-between gap-4">
              <div>
                <div className="flex items-center gap-2 mb-1">
                  <span className="px-2.5 py-0.5 rounded text-[10px] font-bold bg-cyan-950 text-cyan-400 border border-cyan-800">
                    {selectedDestinationDetail.category}
                  </span>
                  <span className="text-xs text-slate-400">
                    {selectedDestinationDetail.state}, India
                  </span>
                </div>
                <h3 className="text-2xl font-extrabold text-white">
                  {selectedDestinationDetail.name}
                </h3>
              </div>
              <button
                onClick={() => setSelectedDestinationDetail(null)}
                className="p-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-white"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <p className="text-xs text-slate-300 leading-relaxed">
              {selectedDestinationDetail.description}
            </p>

            {/* Quick Specs */}
            <div className="grid grid-cols-3 gap-3 p-3 rounded-xl bg-slate-950 border border-slate-800 text-xs">
              <div>
                <span className="text-slate-500 block text-[11px]">Best Season</span>
                <span className="font-semibold text-slate-200">{selectedDestinationDetail.best_season}</span>
              </div>
              <div>
                <span className="text-slate-500 block text-[11px]">Average Daily Budget</span>
                <span className="font-semibold text-cyan-400">₹{selectedDestinationDetail.average_budget} / person</span>
              </div>
              <div>
                <span className="text-slate-500 block text-[11px]">Popularity Score</span>
                <span className="font-semibold text-emerald-400">★ {selectedDestinationDetail.popularity_score} / 10</span>
              </div>
            </div>

            {/* Attractions List */}
            <div>
              <h4 className="text-sm font-bold text-white mb-3">
                Key Catalogued Attractions ({selectedDestinationDetail.attractions?.length || 0})
              </h4>
              <div className="space-y-2.5">
                {selectedDestinationDetail.attractions?.map((act, idx) => (
                  <div
                    key={act.id || idx}
                    className="p-3 rounded-xl bg-slate-950/70 border border-slate-800 flex items-start justify-between gap-3 text-xs"
                  >
                    <div className="space-y-1">
                      <div className="flex items-center gap-2">
                        <span className="font-bold text-white">{act.name}</span>
                        <span className={`px-1.5 py-0.5 rounded text-[10px] font-semibold ${
                          act.is_outdoor ? 'bg-amber-950 text-amber-300 border border-amber-800/60' : 'bg-blue-950 text-blue-300 border border-blue-800/60'
                        }`}>
                          {act.is_outdoor ? 'Outdoor' : 'Indoor'}
                        </span>
                      </div>
                      <p className="text-[11px] text-slate-400">{act.description}</p>
                    </div>

                    <div className="text-right whitespace-nowrap flex-shrink-0">
                      <span className="text-slate-300 block font-semibold">
                        {act.entry_fee > 0 ? `₹${act.entry_fee}` : 'Free Entry'}
                      </span>
                      <span className="text-[10px] text-slate-500">⏱️ {act.estimated_duration_hours}h</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Modal Actions */}
            <div className="pt-2 flex justify-end gap-3">
              <button
                onClick={() => setSelectedDestinationDetail(null)}
                className="px-4 py-2 rounded-xl text-xs font-semibold bg-slate-800 hover:bg-slate-700 text-slate-300"
              >
                Close
              </button>
              <a
                href={`/plan?destination=${encodeURIComponent(selectedDestinationDetail.name)}`}
                className="px-5 py-2 rounded-xl text-xs font-bold text-slate-950 bg-cyan-400 hover:bg-cyan-300 transition-colors flex items-center gap-1.5 shadow"
              >
                Plan Trip to {selectedDestinationDetail.name}
                <ArrowRight className="w-3.5 h-3.5" />
              </a>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
