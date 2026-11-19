import React, { useEffect, useRef } from 'react';
import L from 'leaflet';

export default function InteractiveMap({ attractions = [], center = [20.5937, 78.9629], zoom = 6 }) {
  const mapContainerRef = useRef(null);
  const mapInstanceRef = useRef(null);
  const layerGroupRef = useRef(null);

  useEffect(() => {
    if (!mapContainerRef.current) return;

    if (!mapInstanceRef.current) {
      // Initialize map
      const map = L.map(mapContainerRef.current, {
        center: center,
        zoom: zoom,
        zoomControl: true,
      });

      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors',
        maxZoom: 18,
      }).addTo(map);

      mapInstanceRef.current = map;
      layerGroupRef.current = L.layerGroup().addTo(map);
    }

    return () => {
      // Map cleanup on unmount
      if (mapInstanceRef.current) {
        mapInstanceRef.current.remove();
        mapInstanceRef.current = null;
      }
    };
  }, []);

  useEffect(() => {
    if (!mapInstanceRef.current || !layerGroupRef.current) return;

    const layerGroup = layerGroupRef.current;
    layerGroup.clearLayers();

    const validAttractions = attractions.filter(a => a.latitude && a.longitude);
    if (validAttractions.length === 0) return;

    const latLngs = [];

    validAttractions.forEach((act, idx) => {
      const lat = parseFloat(act.latitude);
      const lon = parseFloat(act.longitude);
      const seq = act.sequence_order || idx + 1;
      latLngs.push([lat, lon]);

      // Custom SVG Numbered Pin Marker
      const customIcon = L.divIcon({
        className: 'custom-leaflet-marker',
        html: `
          <div style="
            background: linear-gradient(135deg, #06b6d4, #2563eb);
            color: #ffffff;
            font-size: 11px;
            font-weight: 800;
            width: 28px;
            height: 28px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 4px 10px rgba(0,0,0,0.5), 0 0 0 2px #ffffff;
            border: 2px solid #0f172a;
          ">
            ${seq}
          </div>
        `,
        iconSize: [28, 28],
        iconAnchor: [14, 14],
      });

      const popupContent = `
        <div style="font-family: inherit; color: #0f172a; max-width: 200px;">
          <h4 style="margin: 0 0 4px 0; font-weight: 700; font-size: 13px;">${act.attraction_name || act.name}</h4>
          <p style="margin: 0 0 4px 0; font-size: 11px; color: #475569;">${act.description ? act.description.slice(0, 90) + '...' : ''}</p>
          <div style="display: flex; gap: 6px; font-size: 10px; font-weight: 600;">
            <span style="background: #e0f2fe; color: #0369a1; padding: 2px 6px; border-radius: 4px;">
              ${act.is_outdoor ? '☀️ Outdoor' : '🏛️ Indoor'}
            </span>
            <span style="background: #f1f5f9; color: #334155; padding: 2px 6px; border-radius: 4px;">
              ⏱️ ${act.duration_hours || 2}h
            </span>
          </div>
        </div>
      `;

      L.marker([lat, lon], { icon: customIcon })
        .bindPopup(popupContent)
        .addTo(layerGroup);
    });

    // Draw connecting route polyline
    if (latLngs.length > 1) {
      L.polyline(latLngs, {
        color: '#06b6d4',
        weight: 3.5,
        opacity: 0.8,
        dashArray: '6, 8',
        lineCap: 'round'
      }).addTo(layerGroup);
    }

    // Fit map bounds to encompass all points
    try {
      const bounds = L.latLngBounds(latLngs);
      mapInstanceRef.current.fitBounds(bounds, { padding: [45, 45], maxZoom: 14 });
    } catch (e) {
      // Single point zoom
      if (latLngs[0]) {
        mapInstanceRef.current.setView(latLngs[0], 12);
      }
    }
  }, [attractions]);

  return (
    <div className="relative w-full h-80 sm:h-96 rounded-xl overflow-hidden border border-slate-800 shadow-xl">
      <div ref={mapContainerRef} className="w-full h-full" />
      <div className="absolute top-3 right-3 z-[400] bg-slate-950/85 backdrop-blur-md px-3 py-1.5 rounded-lg border border-slate-700/70 text-[11px] font-semibold text-slate-300 shadow">
        🗺️ Sightseeing Route & Attractions
      </div>
    </div>
  );
}
