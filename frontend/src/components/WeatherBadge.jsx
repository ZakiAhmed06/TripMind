import React, { useState, useEffect } from 'react';
import { Cloud, Sun, CloudRain, Wind, Snowflake, CloudLightning } from 'lucide-react';
import api from '../api/client';

export default function WeatherBadge({ destinationId, initialWeather }) {
  const [weather, setWeather] = useState(initialWeather || null);
  const [loading, setLoading] = useState(!initialWeather && !!destinationId);

  useEffect(() => {
    if (!initialWeather && destinationId) {
      api.get(`/weather/${destinationId}`)
        .then(res => setWeather(res.data))
        .catch(err => console.warn('Weather fetch error:', err))
        .finally(() => setLoading(false));
    }
  }, [destinationId, initialWeather]);

  if (loading) {
    return (
      <div className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-slate-800/80 text-[11px] text-slate-400 animate-pulse">
        <Cloud className="w-3.5 h-3.5" /> Loading weather...
      </div>
    );
  }

  if (!weather) return null;

  const temp = weather.temperature_avg || weather.temperature_max || 24;
  const summary = weather.summary || 'Pleasant';
  const rainProb = weather.precipitation_probability ?? 0;

  let Icon = Sun;
  if (rainProb > 40 || summary.toLowerCase().includes('rain')) {
    Icon = CloudRain;
  } else if (summary.toLowerCase().includes('cloud') || summary.toLowerCase().includes('overcast')) {
    Icon = Cloud;
  } else if (temp < 8) {
    Icon = Snowflake;
  }

  return (
    <div className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-slate-900/90 border border-slate-700/80 text-[11px] text-slate-200 shadow-sm backdrop-blur-sm">
      <Icon className="w-3.5 h-3.5 text-cyan-400" />
      <span className="font-bold text-white">{Math.round(temp)}°C</span>
      <span className="text-slate-400 truncate max-w-[100px]">{summary}</span>
      {rainProb > 25 && (
        <span className="text-[10px] text-blue-400 font-semibold bg-blue-950/60 px-1 rounded">
          {Math.round(rainProb)}% rain
        </span>
      )}
    </div>
  );
}
