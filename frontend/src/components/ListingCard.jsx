function formatPrice(price) {
  if (!price) return 'Price N/A';
  if (price >= 1_000_000) return `$${(price / 1_000_000).toFixed(1)}M`;
  if (price >= 1_000) return `$${(price / 1_000).toFixed(0)}K`;
  return `$${price.toLocaleString()}`;
}

export default function ListingCard({ listing, onClick }) {
  return (
    <div
      onClick={() => onClick(listing)}
      className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden cursor-pointer hover:shadow-md transition-shadow"
    >
      <div className="h-48 bg-gray-200 relative">
        {listing.image_urls?.[0] ? (
          <img
            src={listing.image_urls[0]}
            alt={listing.title}
            className="w-full h-full object-cover"
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center text-gray-400">
            No Image
          </div>
        )}
        <div className="absolute top-2 right-2 bg-blue-600 text-white text-xs font-bold px-2 py-1 rounded">
          {listing.source_name}
        </div>
      </div>

      <div className="p-4">
        <h3 className="font-semibold text-gray-900 text-lg truncate">{listing.title}</h3>
        <p className="text-sm text-gray-500 mt-1">
          {listing.city}, {listing.state} {listing.zip_code}
        </p>

        <div className="mt-3 flex items-center justify-between">
          <span className="text-xl font-bold text-blue-600">{formatPrice(listing.price)}</span>
          {listing.cap_rate && (
            <span className="text-sm font-medium text-green-600 bg-green-50 px-2 py-1 rounded">
              {listing.cap_rate}% Cap
            </span>
          )}
        </div>

        <div className="mt-3 flex gap-4 text-sm text-gray-600">
          {listing.num_units && (
            <span>{listing.num_units} Units</span>
          )}
          {listing.year_built && (
            <span>Built {listing.year_built}</span>
          )}
          {listing.square_footage && (
            <span>{listing.square_footage.toLocaleString()} SF</span>
          )}
        </div>

        {listing.price_per_unit && (
          <p className="mt-2 text-xs text-gray-400">
            {formatPrice(listing.price_per_unit)}/unit
          </p>
        )}
      </div>
    </div>
  );
}
