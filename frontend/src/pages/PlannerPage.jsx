import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import {
  Sparkles,
  MapPin,
  Calendar,
  Users,
  Wallet,
  Car,
  Hotel,
  Utensils,
  ArrowRight,
  Compass,
  CheckCircle,
  AlertCircle
} from 'lucide-react';
import api from '../api/client';
import { useAuth } from '../context/AuthContext';

const INTERESTS_OPTIONS = [
  { id: 'Mountains', label: 'Mountains', icon: '⛰️' },
  { id: 'Beaches', label: 'Beaches', icon: '🏖️' },
  { id: 'Adventure', label: 'Adventure', icon: '🧗' },
  { id: 'Nature', label: 'Nature', icon: '🌲' },
  { id: 'Photography', label: 'Photography', icon: '📷' },
  { id: 'Heritage', label: 'Heritage', icon: '🏰' },
  { id: 'Culture', label: 'Culture', icon: '🎭' },
  { id: 'Food', label: 'Food & Cuisine', icon: '🍲' },
  { id: 'Nightlife', label: 'Nightlife', icon: '🍸' },
  { id: 'Spiritual', label: 'Spiritual', icon: '🛕' },
  { id: 'Wildlife', label: 'Wildlife', icon: '🐅' },
];

export default function PlannerPage() {
  const navigate = useNavigate();
  const location = useLocation();
  const { user } = useAuth();

  const urlParams = new URLSearchParams(location.search);
  const preselected = location.state?.preselectedDestination || urlParams.get('destination') || '';

  const [destinationName, setDestinationName] = useState(preselected);
  const [origin, setOrigin] = useState(user?.preferences?.default_origin || 'Delhi');
  const [durationDays, setDurationDays] = useState(4);
  const [travellersCount, setTravellersCount] = useState(2);
  const [totalBudget, setTotalBudget] = useState(25000);
  const [transportMode, setTransportMode] = useState('Train');
  const [accommodationCategory, setAccommodationCategory] = useState('Standard (3-star)');
  const [foodPreference, setFoodPreference] = useState('Both');
  const [selectedInterests, setSelectedInterests] = useState(['Mountains', 'Nature', 'Adventure']);
  const [startDate, setStartDate] = useState(new Date().toISOString().split('T')[0]);

  const [destinationsList, setDestinationsList] = useState([]);
  const [predictingBudget, setPredictingBudget] = useState(false);
  const [predictedBudget, setPredictedBudget] = useState(null);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    // Load top destinations for dropdown suggestion
    api.get('/destinations?limit=40')
      .then(res => setDestinationsList(res.data))
      .catch(err => console.warn(err));
  }, []);

  // Update budget estimate via ML model whenever key parameters change
  useEffect(() => {
    const timer = setTimeout(async () => {
      try {
        setPredictingBudget(true);
        const res = await api.post('/budget/predict', {
          destination_name: destinationName || 'Manali',
          duration_days: durationDays,
          travellers_count: travellersCount,
          transport_mode: transportMode,
          hotel_category: accommodationCategory,
          season: 'Moderate',
          food_preference: foodPreference,
          sightseeing_count: durationDays * 2
        });
        setPredictedBudget(res.data);
      } catch (err) {
        console.warn('Real-time budget prediction error:', err);
      } finally {
        setPredictingBudget(false);
      }
    }, 400);

    return () => clearTimeout(timer);
  }, [destinationName, durationDays, travellersCount, transportMode, accommodationCategory, foodPreference]);

  const toggleInterest = (id) => {
    if (selectedInterests.includes(id)) {
      if (selectedInterests.length > 1) {
        setSelectedInterests(selectedInterests.filter(i => i !== id));
      }
    } else {
      setSelectedInterests([...selectedInterests, id]);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSubmitting(true);

    try {
      let finalDest = destinationName.trim();

      // If no destination specified, query recommendation engine first to pick top ML match
      if (!finalDest) {
        const recRes = await api.post('/recommendations', {
          origin: origin,
          budget: totalBudget,
          duration_days: durationDays,
          travellers_count: travellersCount,
          interests: selectedInterests
        });
        if (recRes.data.recommendations && recRes.data.recommendations.length > 0) {
          finalDest = recRes.data.recommendations[0].name;
        } else {
          finalDest = 'Manali';
        }
      }

      // Generate structured itinerary
      const itinRes = await api.post('/itinerary/generate', {
        destination_name: finalDest,
        origin: origin,
        start_date: startDate,
        duration_days: durationDays,
        travellers_count: travellersCount,
        budget: totalBudget,
        travel_interests: selectedInterests,
        transport_mode: transportMode,
        accommodation_category: accommodationCategory,
        food_preference: foodPreference
      });

      // Navigate to itinerary view with result
      navigate('/itinerary/new', { state: { itineraryData: itinRes.data, plannedTripConfig: {
        destination_name: finalDest,
        origin,
        start_date: startDate,
        total_days: durationDays,
        travellers_count: travellersCount,
        total_budget: totalBudget,
        transport_mode: transportMode,
        accommodation_type: accommodationCategory,
        food_preference: foodPreference
      }}});

    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to generate itinerary. Please try again.');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Header */}
      <div>
        <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-cyan-950 text-cyan-400 text-xs font-semibold mb-2">
          <Sparkles className="w-3.5 h-3.5" />
          Powered by ML Destination Ranking & Random Forest Regressor
        </div>
        <h1 className="text-3xl font-extrabold text-white">Smart Trip Planner</h1>
        <p className="text-sm text-slate-400 mt-1">
          Input your travel preferences below. Our backend algorithms will predict expenses, evaluate crowd dynamics, and generate your day-wise itinerary.
        </p>
      </div>

      {error && (
        <div className="p-4 rounded-xl bg-red-950/60 border border-red-800 text-red-300 text-xs flex items-center gap-2">
          <AlertCircle className="w-4 h-4 flex-shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* Main Form */}
      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="p-6 sm:p-8 rounded-2xl bg-slate-900/90 border border-slate-800 shadow-xl space-y-6">
          {/* Destination & Starting Point */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1.5">
                Starting Location (Origin City)
              </label>
              <div className="relative">
                <MapPin className="w-4 h-4 text-cyan-400 absolute left-3 top-1/2 -translate-y-1/2" />
                <input
                  type="text"
                  required
                  placeholder="e.g. Delhi, Mumbai, Bangalore"
                  value={origin}
                  onChange={(e) => setOrigin(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 focus:border-cyan-500 rounded-xl py-2.5 pl-9 pr-3 text-sm text-white placeholder-slate-500 focus:outline-none"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1.5">
                Target Destination (or leave empty for AI recommendation)
              </label>
              <div className="relative">
                <Compass className="w-4 h-4 text-blue-400 absolute left-3 top-1/2 -translate-y-1/2" />
                <input
                  type="text"
                  placeholder="e.g. Manali, Darjeeling, Goa (or leave blank)"
                  value={destinationName}
                  onChange={(e) => setDestinationName(e.target.value)}
                  list="dest-list"
                  className="w-full bg-slate-950 border border-slate-800 focus:border-cyan-500 rounded-xl py-2.5 pl-9 pr-3 text-sm text-white placeholder-slate-500 focus:outline-none"
                />
                <datalist id="dest-list">
                  {destinationsList.map(d => (
                    <option key={d.id} value={d.name}>{d.name} ({d.state})</option>
                  ))}
                </datalist>
              </div>
            </div>
          </div>

          {/* Dates & Duration & Travellers */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 pt-2 border-t border-slate-800/80">
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1.5">Start Date</label>
              <div className="relative">
                <Calendar className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
                <input
                  type="date"
                  value={startDate}
                  onChange={(e) => setStartDate(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 focus:border-cyan-500 rounded-xl py-2.5 pl-9 pr-3 text-xs text-white focus:outline-none"
                />
              </div>
            </div>

            <div>
              <div className="flex items-center justify-between text-xs font-semibold text-slate-300 mb-1.5">
                <span>Trip Duration</span>
                <span className="text-cyan-400 font-bold">{durationDays} Days</span>
              </div>
              <input
                type="range"
                min="2"
                max="10"
                value={durationDays}
                onChange={(e) => setDurationDays(Number(e.target.value))}
                className="w-full accent-cyan-400 cursor-pointer py-2"
              />
            </div>

            <div>
              <div className="flex items-center justify-between text-xs font-semibold text-slate-300 mb-1.5">
                <span>Travellers</span>
                <span className="text-cyan-400 font-bold">{travellersCount} People</span>
              </div>
              <input
                type="range"
                min="1"
                max="8"
                value={travellersCount}
                onChange={(e) => setTravellersCount(Number(e.target.value))}
                className="w-full accent-cyan-400 cursor-pointer py-2"
              />
            </div>
          </div>

          {/* Budget, Transport & Hotel */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 pt-2 border-t border-slate-800/80">
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1.5">
                Max Total Budget (INR)
              </label>
              <div className="relative">
                <Wallet className="w-4 h-4 text-emerald-400 absolute left-3 top-1/2 -translate-y-1/2" />
                <input
                  type="number"
                  min="5000"
                  max="500000"
                  step="1000"
                  value={totalBudget}
                  onChange={(e) => setTotalBudget(Number(e.target.value))}
                  className="w-full bg-slate-950 border border-slate-800 focus:border-cyan-500 rounded-xl py-2.5 pl-9 pr-3 text-sm text-white focus:outline-none"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1.5">Transport Mode</label>
              <select
                value={transportMode}
                onChange={(e) => setTransportMode(e.target.value)}
                className="w-full bg-slate-950 border border-slate-800 rounded-xl py-2.5 px-3 text-xs text-white focus:outline-none focus:border-cyan-500"
              >
                <option value="Train">Train (Comfort & Scenic)</option>
                <option value="Flight">Flight (Fastest)</option>
                <option value="Cab">Cab / Road Trip</option>
                <option value="Bus">Bus (Budget)</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1.5">Accommodation Tier</label>
              <select
                value={accommodationCategory}
                onChange={(e) => setAccommodationCategory(e.target.value)}
                className="w-full bg-slate-950 border border-slate-800 rounded-xl py-2.5 px-3 text-xs text-white focus:outline-none focus:border-cyan-500"
              >
                <option value="Standard (3-star)">Standard (3-star Hotel)</option>
                <option value="Budget">Budget (Homestay / Hostel)</option>
                <option value="Luxury (4/5-star)">Luxury (4/5-star Resort)</option>
              </select>
            </div>
          </div>

          {/* Food preference */}
          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1.5">Food Preference</label>
            <div className="grid grid-cols-3 gap-3">
              {['Veg', 'Non-Veg', 'Both'].map((f) => (
                <button
                  type="button"
                  key={f}
                  onClick={() => setFoodPreference(f)}
                  className={`py-2 text-xs font-semibold rounded-xl border transition-all ${
                    foodPreference === f
                      ? 'bg-cyan-500 text-slate-950 border-cyan-400 font-bold'
                      : 'bg-slate-950 text-slate-400 border-slate-800 hover:text-white'
                  }`}
                >
                  {f === 'Veg' ? '🥗 Vegetarian' : f === 'Non-Veg' ? '🍗 Non-Veg' : '🍲 Both'}
                </button>
              ))}
            </div>
          </div>

          {/* Travel Interests (11 Categories Multi-Select) */}
          <div className="pt-2 border-t border-slate-800/80">
            <label className="block text-xs font-semibold text-slate-300 mb-2">
              Select Your Travel Interests (Multi-select)
            </label>
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
              {INTERESTS_OPTIONS.map((item) => {
                const isChecked = selectedInterests.includes(item.id);
                return (
                  <button
                    type="button"
                    key={item.id}
                    onClick={() => toggleInterest(item.id)}
                    className={`flex items-center gap-2 p-2.5 rounded-xl border text-xs font-semibold transition-all text-left ${
                      isChecked
                        ? 'bg-cyan-950/80 border-cyan-500/80 text-cyan-300 shadow-sm'
                        : 'bg-slate-950/70 border-slate-800 text-slate-400 hover:text-white'
                    }`}
                  >
                    <span>{item.icon}</span>
                    <span className="truncate">{item.label}</span>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Live ML Prediction Banner */}
          {predictedBudget && (
            <div className="p-4 rounded-xl bg-slate-950 border border-slate-800/90 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 text-xs">
              <div>
                <span className="text-[11px] text-cyan-400 font-bold uppercase tracking-wider block">
                  ML Random Forest Budget Preview
                </span>
                <span className="text-slate-300">
                  Predicted Trip Cost:{' '}
                  <strong className="text-white text-sm">
                    ₹{predictedBudget.predicted_total_expense.toLocaleString()}
                  </strong>{' '}
                  (~₹{predictedBudget.per_person_expense.toLocaleString()} / person)
                </span>
              </div>
              <div className="text-[11px] text-slate-400">
                {predictedBudget.predicted_total_expense > totalBudget ? (
                  <span className="text-amber-400 font-medium">⚠️ Exceeds max budget; consider 3-star stay or train transit</span>
                ) : (
                  <span className="text-emerald-400 font-medium">✓ Fits comfortably within your ₹{totalBudget.toLocaleString()} budget</span>
                )}
              </div>
            </div>
          )}

          {/* Submit Action */}
          <button
            type="submit"
            disabled={submitting}
            className="w-full py-3.5 px-6 rounded-xl font-bold text-sm text-slate-950 bg-gradient-to-r from-cyan-400 via-teal-400 to-blue-400 hover:from-cyan-300 hover:to-blue-300 transition-all shadow-lg shadow-cyan-500/25 disabled:opacity-50 flex items-center justify-center gap-2"
          >
            {submitting ? (
              <span>Generating AI Itinerary & ML Optimizations...</span>
            ) : (
              <>
                <Sparkles className="w-4 h-4" />
                Generate Intelligent Itinerary
                <ArrowRight className="w-4 h-4" />
              </>
            )}
          </button>
        </div>
      </form>
    </div>
  );
}
