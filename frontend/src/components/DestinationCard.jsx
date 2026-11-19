import React from 'react';
import { useNavigate } from 'react-router-dom';
import { MapPin, Calendar, Tag, ArrowRight, Sparkles, Compass } from 'lucide-react';
import WeatherBadge from './WeatherBadge';

export default function DestinationCard({ destination, onSelectDetails, matchScore }) {
  const navigate = useNavigate();

  const handlePlanTrip = (e) => {
    e.stopPropagation();
    navigate('/plan', { state: { preselectedDestination: destination.name } });
  };

  const score = matchScore || destination.match_percentage || (destination.popularity_score ? Math.round(destination.popularity_score * 10) : null);

  return (
    <div
      onClick={() => onSelectDetails && onSelectDetails(destination)}
      className="group relative bg-slate-900/80 hover:bg-slate-800/90 border border-slate-800 hover:border-cyan-500/50 rounded-2xl overflow-hidden shadow-lg hover:shadow-cyan-500/10 transition-all duration-300 flex flex-col cursor-pointer"
    >
      {/* Image Container */}
      <div className="relative h-48 sm:h-52 w-full overflow-hidden bg-slate-800">
        <img
          src={destination.image_url || 'https://images.unsplash.com/photo-1506461883276-594a12b11cf3?auto=format&fit=crop&w=800&q=80'}
          alt={destination.name}
          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
          loading="lazy"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-slate-950 via-slate-950/20 to-transparent" />

        {/* Top Badges */}
        <div className="absolute top-3 left-3 flex flex-wrap items-center gap-1.5">
          <span className="px-2.5 py-1 rounded-full text-[11px] font-bold bg-slate-950/80 backdrop-blur-md text-cyan-300 border border-cyan-500/30">
            {destination.category}
          </span>
          {score && (
            <span className="flex items-center gap-1 px-2.5 py-1 rounded-full text-[11px] font-extrabold bg-cyan-500 text-slate-950 shadow-md">
              <Sparkles className="w-3 h-3" />
              {score}% Match
            </span>
          )}
        </div>

        {/* Weather snapshot on image bottom */}
        <div className="absolute bottom-2.5 right-3">
          <WeatherBadge destinationId={destination.id || destination.destination_id} />
        </div>
      </div>

      {/* Card Content */}
      <div className="p-4 sm:p-5 flex-1 flex flex-col justify-between">
        <div>
          <div className="flex items-start justify-between gap-2 mb-1.5">
            <h3 className="text-lg font-bold text-white group-hover:text-cyan-400 transition-colors line-clamp-1">
              {destination.name}
            </h3>
            <span className="text-xs font-semibold text-slate-400 whitespace-nowrap">
              ₹{Math.round(destination.average_budget || 2500)}/day
            </span>
          </div>

          <div className="flex items-center gap-1 text-xs text-slate-400 mb-2.5">
            <MapPin className="w-3.5 h-3.5 text-cyan-500 flex-shrink-0" />
            <span className="truncate">{destination.state}, India</span>
          </div>

          <p className="text-xs text-slate-300 leading-relaxed line-clamp-2 mb-3">
            {destination.match_explanation || destination.description}
          </p>
        </div>

        <div>
          {/* Metadata attributes */}
          <div className="flex items-center justify-between text-[11px] text-slate-400 py-2 border-t border-slate-800/80 mb-3">
            <span className="flex items-center gap-1">
              <Calendar className="w-3 h-3 text-slate-500" />
              {destination.recommended_season || destination.best_season || 'Oct - Mar'}
            </span>
            <span className="text-emerald-400 font-medium">
              ★ {destination.popularity_score || 9.0}/10 Popularity
            </span>
          </div>

          {/* Buttons */}
          <div className="grid grid-cols-2 gap-2 pt-1">
            <button
              onClick={() => onSelectDetails && onSelectDetails(destination)}
              className="py-1.5 px-3 rounded-lg text-xs font-semibold text-slate-200 bg-slate-800 hover:bg-slate-700 transition-colors"
            >
              Attractions
            </button>
            <button
              onClick={handlePlanTrip}
              className="py-1.5 px-3 rounded-lg text-xs font-bold text-slate-950 bg-gradient-to-r from-cyan-400 to-blue-400 hover:from-cyan-300 hover:to-blue-300 transition-all shadow-sm flex items-center justify-center gap-1"
            >
              Plan Trip
              <ArrowRight className="w-3 h-3" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
