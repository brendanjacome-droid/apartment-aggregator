import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';

function formatPrice(price) {
  if (!price) return 'N/A';
  if (price >= 1_000_000) return `$${(price / 1_000_000).toFixed(1)}M`;
  if (price >= 1_000) return `$${(price / 1_000).toFixed(0)}K`;
  return `$${price.toLocaleString()}`;
}

export default function MapView({ listings, onSelect }) {
  const validListings = listings.filter(l => l.latitude && l.longitude);

  return (
    <div className="h-[500px] rounded-lg overflow-hidden border border-gray-200">
      <MapContainer
        center={[39.8283, -98.5795]}
        zoom={4}
        scrollWheelZoom={true}
        style={{ height: '100%', width: '100%' }}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        {validListings.map((listing) => (
          <Marker
            key={listing.id}
            position={[listing.latitude, listing.longitude]}
            eventHandlers={{ click: () => onSelect(listing) }}
          >
            <Popup>
              <div className="text-sm">
                <strong>{listing.title}</strong><br />
                {listing.city}, {listing.state}<br />
                {formatPrice(listing.price)} | {listing.num_units} units
              </div>
            </Popup>
          </Marker>
        ))}
      </MapContainer>
    </div>
  );
}
