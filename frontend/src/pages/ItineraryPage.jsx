import React, { useState, useEffect } from 'react';
import { useLocation, useParams, useNavigate } from 'react-router-dom';
import {
  Calendar,
  Clock,
  MapPin,
  Sparkles,
  CloudRain,
  Save,
  Printer,
  Plus,
  Trash2,
  Edit2,
  Check,
  AlertTriangle,
  ArrowRight,
  ShieldCheck,
  Compass
} from 'lucide-react';
import api from '../api/client';
import { useAuth } from '../context/AuthContext';
import InteractiveMap from '../components/InteractiveMap';
import ExpenseChart from '../components/ExpenseChart';

export default function ItineraryPage() {
  const { id } = useParams();
  const location = useLocation();
  const navigate = useNavigate();
  const { user, isAuthenticated } = useAuth();

  // Load from navigation state if newly created, or fetch from API if viewing saved trip
  const [itinerary, setItinerary] = useState(location.state?.itineraryData || null);
  const [tripConfig, setTripConfig] = useState(location.state?.plannedTripConfig || null);
  const [savedTripData, setSavedTripData] = useState(location.state?.tripData || null);

  const [activeDayIndex, setActiveDayIndex] = useState(0);
  const [loading, setLoading] = useState(!itinerary && !savedTripData && id !== 'new');
  const [replanning, setReplanning] = useState(false);
  const [replanAlert, setReplanAlert] = useState(null);
  const [savingTrip, setSavingTrip] = useState(false);
  const [savedSuccess, setSavedSuccess] = useState(false);

  // Edit Activity Modal state
  const [editingActivity, setEditingActivity] = useState(null);
  const [showAddModal, setShowAddModal] = useState(false);
  const [newActivityName, setNewActivityName] = useState('');
  const [newActivityDesc, setNewActivityDesc] = useState('');
  const [newActivitySlot, setNewActivitySlot] = useState('Afternoon');
  const [newActivityDuration, setNewActivityDuration] = useState(2);
  const [newActivityOutdoor, setNewActivityOutdoor] = useState(true);

  useEffect(() => {
    if (id && id !== 'new' && !itinerary && !savedTripData) {
      // Fetch saved trip by id
      api.get(`/trips/${id}`)
        .then(res => {
          setSavedTripData(res.data);
          // Assemble itinerary structure
          setItinerary({
            destination_name: res.data.destination_name,
            origin: res.data.origin,
            duration_days: res.data.total_days,
            travellers_count: res.data.travellers_count,
            total_budget: res.data.total_budget,
            estimated_total_expense: res.data.total_budget,
            expense_breakdown: {
              transportation: res.data.total_budget * 0.28,
              accommodation: res.data.total_budget * 0.32,
              food: res.data.total_budget * 0.20,
              sightseeing: res.data.total_budget * 0.12,
              miscellaneous: res.data.total_budget * 0.08,
              total: res.data.total_budget,
              currency: 'INR'
            },
            days: res.data.days,
            travel_tips: [
              'Keep verified identification cards accessible.',
              'Schedule visits during early morning hours to avoid peak footfalls.'
            ],
            source: 'TripMind Saved Itinerary'
          });
        })
        .catch(err => console.warn('Failed to fetch trip:', err))
        .finally(() => setLoading(false));
    } else if (savedTripData && !itinerary) {
      setItinerary({
        destination_name: savedTripData.destination_name,
        origin: savedTripData.origin,
        duration_days: savedTripData.total_days,
        travellers_count: savedTripData.travellers_count,
        total_budget: savedTripData.total_budget,
        estimated_total_expense: savedTripData.total_budget,
        expense_breakdown: {
          transportation: savedTripData.total_budget * 0.28,
          accommodation: savedTripData.total_budget * 0.32,
          food: savedTripData.total_budget * 0.20,
          sightseeing: savedTripData.total_budget * 0.12,
          miscellaneous: savedTripData.total_budget * 0.08,
          total: savedTripData.total_budget,
          currency: 'INR'
        },
        days: savedTripData.days,
        travel_tips: ['Saved trip itinerary loaded from your cloud database.'],
        source: 'TripMind Saved Itinerary'
      });
      setLoading(false);
    }
  }, [id, savedTripData, itinerary]);

  // If no itinerary data in state (e.g. user refreshed on /itinerary/new), load fallback demo
  useEffect(() => {
    if (!itinerary && !loading) {
      api.post('/itinerary/generate', {
        destination_name: 'Manali',
        origin: 'Delhi',
        duration_days: 4,
        travellers_count: 2,
        budget: 25000,
        travel_interests: ['Mountains', 'Adventure', 'Nature']
      }).then(res => setItinerary(res.data));
    }
  }, [itinerary, loading]);

  if (loading || !itinerary) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-20 text-center space-y-4">
        <Sparkles className="w-10 h-10 text-cyan-400 mx-auto animate-spin" />
        <h2 className="text-xl font-bold text-white">Loading your intelligent itinerary...</h2>
        <p className="text-xs text-slate-400">Optimizing routes, checking weather conditions, and balancing budgets.</p>
      </div>
    );
  }

  const currentDay = itinerary.days[activeDayIndex] || itinerary.days[0];

  // Dynamic Weather Alert Simulation & Replanning
  const handleSimulateWeatherReplan = async () => {
    setReplanning(true);
    try {
      const affectedDayNumber = currentDay.day_number;
      const res = await api.post('/itinerary/replan', {
        destination_name: itinerary.destination_name,
        current_days: itinerary.days,
        affected_day: affectedDayNumber,
        reason: 'Heavy Monsoon Rainfall & Landslide Warning',
        weather_condition: 'Heavy Rain',
        total_budget: itinerary.total_budget
      });

      setItinerary({
        ...itinerary,
        days: res.data
      });

      setReplanAlert({
        day: affectedDayNumber,
        message: `Day ${affectedDayNumber} schedule successfully adapted to rain-safe indoor cultural attractions, museums, and cozy tea tasting lounges.`
      });
    } catch (err) {
      console.warn('Weather replanning failed:', err);
    } finally {
      setReplanning(false);
    }
  };

  // Activity Edit & Delete Handlers
  const handleDeleteActivity = (actIndex) => {
    const updatedDays = [...itinerary.days];
    updatedDays[activeDayIndex].activities.splice(actIndex, 1);
    setItinerary({ ...itinerary, days: updatedDays });
  };

  const handleAddActivitySubmit = (e) => {
    e.preventDefault();
    if (!newActivityName.trim()) return;

    const newAct = {
      id: `custom-act-${Date.now()}`,
      time_slot: newActivitySlot,
      attraction_name: newActivityName.trim(),
      description: newActivityDesc.trim() || 'Custom scheduled travel activity.',
      duration_hours: Number(newActivityDuration),
      estimated_cost: 100,
      is_outdoor: newActivityOutdoor,
      sequence_order: (currentDay.activities.length || 0) + 1,
      category: 'Sightseeing'
    };

    const updatedDays = [...itinerary.days];
    updatedDays[activeDayIndex].activities.push(newAct);
    setItinerary({ ...itinerary, days: updatedDays });

    setNewActivityName('');
    setNewActivityDesc('');
    setShowAddModal(false);
  };

  // Save Trip to Database
  const handleSaveTrip = async () => {
    if (!isAuthenticated) {
      navigate('/login');
      return;
    }
    setSavingTrip(true);
    try {
      await api.post('/trips', {
        destination_name: itinerary.destination_name,
        title: `Trip to ${itinerary.destination_name}`,
        origin: itinerary.origin || 'Delhi',
        start_date: tripConfig?.start_date || new Date().toISOString().split('T')[0],
        total_days: itinerary.duration_days,
        travellers_count: itinerary.travellers_count,
        transport_mode: tripConfig?.transport_mode || 'Train',
        accommodation_type: tripConfig?.accommodation_type || 'Standard (3-star)',
        food_preference: tripConfig?.food_preference || 'Both',
        total_budget: itinerary.total_budget,
        status: 'Upcoming',
        days_data: itinerary.days,
        expense_breakdown: itinerary.expense_breakdown
      });
      setSavedSuccess(true);
      setTimeout(() => setSavedSuccess(false), 4000);
    } catch (err) {
      console.warn('Error saving trip:', err);
    } finally {
      setSavingTrip(false);
    }
  };

  const handlePrint = () => {
    window.print();
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
      {/* Top Banner / Actions */}
      <div className="p-6 rounded-3xl bg-gradient-to-r from-slate-900 via-slate-900 to-cyan-950/40 border border-slate-800 shadow-xl flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1.5">
            <span className="px-2.5 py-0.5 rounded text-[10px] font-bold bg-cyan-950 text-cyan-400 border border-cyan-800">
              {itinerary.source}
            </span>
            <span className="text-xs text-slate-400">
              {itinerary.duration_days} Days • {itinerary.travellers_count} Travellers • From {itinerary.origin}
            </span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-white">
            Trip to {itinerary.destination_name}
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Total Budget: <strong className="text-white">₹{Math.round(itinerary.total_budget).toLocaleString()}</strong> | Estimated Expense: <strong className="text-cyan-400">₹{Math.round(itinerary.estimated_total_expense).toLocaleString()}</strong>
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-2.5 print:hidden">
          <button
            onClick={handleSaveTrip}
            disabled={savingTrip}
            className="flex items-center gap-1.5 px-4 py-2 rounded-xl text-xs font-bold text-slate-950 bg-gradient-to-r from-cyan-400 to-teal-400 hover:from-cyan-300 hover:to-teal-300 transition-all shadow-md shadow-cyan-500/20 disabled:opacity-50"
          >
            {savedSuccess ? (
              <>
                <Check className="w-3.5 h-3.5" />
                Saved to My Trips!
              </>
            ) : (
              <>
                <Save className="w-3.5 h-3.5" />
                {savingTrip ? 'Saving...' : 'Save Trip'}
              </>
            )}
          </button>

          <button
            onClick={handlePrint}
            className="flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs font-semibold text-slate-200 bg-slate-800 hover:bg-slate-700 border border-slate-700 transition-colors"
          >
            <Printer className="w-3.5 h-3.5" />
            Print / PDF
          </button>

          <button
            onClick={() => navigate('/assistant', { state: { itineraryContext: itinerary } })}
            className="flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs font-semibold text-cyan-300 bg-cyan-950/60 hover:bg-cyan-900/60 border border-cyan-800 transition-colors"
          >
            <Sparkles className="w-3.5 h-3.5" />
            Ask AI Assistant
          </button>
        </div>
      </div>

      {/* Weather Replanning Trigger Banner */}
      <div className="p-4 rounded-2xl bg-gradient-to-r from-blue-950/60 via-slate-900 to-slate-900 border border-blue-800/60 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 text-xs print:hidden">
        <div className="flex items-center gap-2.5">
          <div className="w-9 h-9 rounded-xl bg-blue-900/40 border border-blue-700/60 flex items-center justify-center text-blue-400 flex-shrink-0">
            <CloudRain className="w-5 h-5" />
          </div>
          <div>
            <h4 className="font-bold text-white text-xs">Simulate Weather Alert & Replanning</h4>
            <p className="text-[11px] text-slate-400">
              Experience dynamic AI itinerary adaptation when bad weather threatens outdoor sightseeing on Day {currentDay.day_number}.
            </p>
          </div>
        </div>

        <button
          onClick={handleSimulateWeatherReplan}
          disabled={replanning}
          className="px-4 py-2 rounded-xl text-xs font-bold text-white bg-blue-600 hover:bg-blue-500 transition-all shadow-md shadow-blue-600/20 disabled:opacity-50 whitespace-nowrap"
        >
          {replanning ? 'Replanning with Indoor Sights...' : `🌧️ Replan Day ${currentDay.day_number} for Rain`}
        </button>
      </div>

      {/* Replan Notification Banner */}
      {replanAlert && (
        <div className="p-4 rounded-xl bg-emerald-950/60 border border-emerald-800/80 text-emerald-300 text-xs flex items-center justify-between gap-2 animate-fade-in">
          <div className="flex items-center gap-2">
            <Check className="w-4 h-4 text-emerald-400" />
            <span>{replanAlert.message}</span>
          </div>
          <button onClick={() => setReplanAlert(null)} className="text-emerald-400 hover:text-white">✕</button>
        </div>
      )}

      {/* Main Layout: Itinerary Timeline & Sidebar (Map + Expense Chart) */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column (2 Cols): Day-wise Schedule */}
        <div className="lg:col-span-2 space-y-5">
          {/* Day Navigation Tabs */}
          <div className="flex items-center gap-2 overflow-x-auto pb-1 no-scrollbar">
            {itinerary.days.map((day, idx) => {
              const active = idx === activeDayIndex;
              return (
                <button
                  key={day.day_number}
                  onClick={() => setActiveDayIndex(idx)}
                  className={`px-4 py-2 rounded-xl text-xs font-bold whitespace-nowrap transition-all ${
                    active
                      ? 'bg-cyan-500 text-slate-950 shadow-md shadow-cyan-500/20'
                      : 'bg-slate-900 text-slate-300 hover:bg-slate-800 border border-slate-800'
                  }`}
                >
                  Day {day.day_number}
                </button>
              );
            })}
          </div>

          {/* Active Day Card */}
          <div className="p-6 rounded-2xl bg-slate-900/90 border border-slate-800 shadow-xl space-y-5">
            <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-2 pb-4 border-b border-slate-800">
              <div>
                <span className="text-[11px] font-bold text-cyan-400 uppercase tracking-wider block">
                  Day {currentDay.day_number} Overview
                </span>
                <h3 className="text-lg font-bold text-white">{currentDay.title}</h3>
              </div>
              <div className="flex items-center gap-2 print:hidden">
                <button
                  onClick={() => setShowAddModal(true)}
                  className="flex items-center gap-1 px-3 py-1.5 rounded-lg text-xs font-semibold bg-slate-800 hover:bg-slate-700 text-slate-200"
                >
                  <Plus className="w-3.5 h-3.5 text-cyan-400" /> Add Activity
                </button>
              </div>
            </div>

            {/* Activities Sequence */}
            <div className="space-y-3">
              {currentDay.activities.map((act, actIdx) => (
                <div
                  key={act.id || actIdx}
                  className="p-4 rounded-xl bg-slate-950/80 border border-slate-800/90 hover:border-slate-700 transition-all flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 text-xs"
                >
                  <div className="flex items-start gap-3">
                    <div className="w-8 h-8 rounded-lg bg-cyan-950/80 border border-cyan-800 text-cyan-300 font-extrabold flex items-center justify-center flex-shrink-0">
                      {act.sequence_order || actIdx + 1}
                    </div>

                    <div className="space-y-1">
                      <div className="flex flex-wrap items-center gap-2">
                        <span className="font-bold text-white text-sm">{act.attraction_name}</span>
                        <span className="px-2 py-0.5 rounded text-[10px] font-semibold bg-slate-800 text-slate-300">
                          {act.time_slot}
                        </span>
                        <span className={`px-2 py-0.5 rounded text-[10px] font-semibold ${
                          act.is_outdoor
                            ? 'bg-amber-950/70 text-amber-300 border border-amber-800/60'
                            : 'bg-blue-950/70 text-blue-300 border border-blue-800/60'
                        }`}>
                          {act.is_outdoor ? '☀️ Outdoor' : '🏛️ Indoor Safe'}
                        </span>
                      </div>
                      <p className="text-xs text-slate-300 leading-relaxed">{act.description}</p>
                    </div>
                  </div>

                  <div className="flex items-center gap-3 sm:text-right whitespace-nowrap self-end sm:self-center">
                    <div>
                      <span className="block font-semibold text-slate-200">
                        {act.estimated_cost > 0 ? `₹${act.estimated_cost}` : 'Free'}
                      </span>
                      <span className="text-[10px] text-slate-400">⏱️ {act.duration_hours} hrs</span>
                    </div>

                    <div className="flex items-center gap-1 print:hidden">
                      <button
                        onClick={() => handleDeleteActivity(actIdx)}
                        title="Remove activity"
                        className="p-1.5 rounded-lg text-slate-400 hover:text-red-400 hover:bg-slate-800 transition-colors"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>

            {/* Food Recommendations & Transit Tips */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-4 border-t border-slate-800 text-xs">
              <div className="p-3.5 rounded-xl bg-slate-950 border border-slate-800/80 space-y-1">
                <span className="font-bold text-white text-xs block">🍲 Recommended Dining</span>
                <ul className="list-disc list-inside text-slate-400 space-y-0.5">
                  {currentDay.food_recommendations?.map((item, i) => (
                    <li key={i}>{item}</li>
                  ))}
                </ul>
              </div>

              <div className="p-3.5 rounded-xl bg-slate-950 border border-slate-800/80 space-y-1">
                <span className="font-bold text-white text-xs block">🚕 Local Transit Advice</span>
                <p className="text-slate-400">{currentDay.transport_tips}</p>
              </div>
            </div>
          </div>
        </div>

        {/* Right Column (1 Col): Interactive Leaflet Map & Expense Breakdown */}
        <div className="space-y-6">
          {/* Map */}
          <div>
            <h3 className="text-sm font-bold text-white mb-2 flex items-center gap-1.5">
              <MapPin className="w-4 h-4 text-cyan-400" />
              Day {currentDay.day_number} Sights & Route Map
            </h3>
            <InteractiveMap attractions={currentDay.activities} />
          </div>

          {/* Expense Breakdown */}
          <ExpenseChart breakdown={itinerary.expense_breakdown} />

          {/* Travel Tips Card */}
          <div className="p-5 rounded-2xl bg-slate-900/80 border border-slate-800 text-xs space-y-2.5">
            <h4 className="font-bold text-white flex items-center gap-1.5">
              <ShieldCheck className="w-4 h-4 text-emerald-400" />
              Essential Travel Advisories
            </h4>
            <ul className="space-y-1.5 text-slate-300">
              {itinerary.travel_tips?.map((tip, idx) => (
                <li key={idx} className="flex items-start gap-1.5">
                  <span className="text-cyan-400">•</span>
                  <span>{tip}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>

      {/* Add Activity Modal */}
      {showAddModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm">
          <div className="w-full max-w-md rounded-2xl bg-slate-900 border border-slate-700 p-6 space-y-4">
            <h3 className="text-lg font-bold text-white">Add Custom Activity to Day {currentDay.day_number}</h3>

            <form onSubmit={handleAddActivitySubmit} className="space-y-3 text-xs">
              <div>
                <label className="block text-slate-300 font-semibold mb-1">Attraction or Activity Name</label>
                <input
                  type="text"
                  required
                  placeholder="e.g. Local Cafe Walk or Photography Point"
                  value={newActivityName}
                  onChange={(e) => setNewActivityName(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl p-2.5 text-white"
                />
              </div>

              <div>
                <label className="block text-slate-300 font-semibold mb-1">Short Description</label>
                <textarea
                  rows="2"
                  placeholder="Brief note on what to see or do..."
                  value={newActivityDesc}
                  onChange={(e) => setNewActivityDesc(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl p-2 text-white"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-slate-300 font-semibold mb-1">Time Slot</label>
                  <select
                    value={newActivitySlot}
                    onChange={(e) => setNewActivitySlot(e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded-xl p-2 text-white"
                  >
                    <option value="Morning">Morning</option>
                    <option value="Afternoon">Afternoon</option>
                    <option value="Evening">Evening</option>
                    <option value="Night">Night</option>
                  </select>
                </div>

                <div>
                  <label className="block text-slate-300 font-semibold mb-1">Duration (Hours)</label>
                  <input
                    type="number"
                    min="0.5"
                    max="8"
                    step="0.5"
                    value={newActivityDuration}
                    onChange={(e) => setNewActivityDuration(e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded-xl p-2 text-white"
                  />
                </div>
              </div>

              <div className="flex items-center gap-2 pt-1">
                <input
                  type="checkbox"
                  id="outdoor-check"
                  checked={newActivityOutdoor}
                  onChange={(e) => setNewActivityOutdoor(e.target.checked)}
                  className="accent-cyan-400"
                />
                <label htmlFor="outdoor-check" className="text-slate-300 cursor-pointer">
                  Outdoor activity (affected by weather alerts)
                </label>
              </div>

              <div className="pt-2 flex justify-end gap-2">
                <button
                  type="button"
                  onClick={() => setShowAddModal(false)}
                  className="px-4 py-2 rounded-xl bg-slate-800 text-slate-300"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 rounded-xl font-bold bg-cyan-400 text-slate-950"
                >
                  Add Activity
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
