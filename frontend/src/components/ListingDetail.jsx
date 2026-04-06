function formatPrice(price) {
  if (!price) return 'N/A';
  return '$' + price.toLocaleString(undefined, { maximumFractionDigits: 0 });
}

export default function ListingDetail({ listing, onClose }) {
  if (!listing) return null;

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto">
      <div className="fixed inset-0 bg-black/50" onClick={onClose} />
      <div className="relative min-h-screen flex items-start justify-center p-4 pt-16">
        <div className="relative bg-white rounded-xl shadow-2xl max-w-3xl w-full max-h-[85vh] overflow-y-auto">
          <button
            onClick={onClose}
            className="absolute top-4 right-4 z-10 bg-white rounded-full p-2 shadow-md hover:bg-gray-100"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>

          {listing.image_urls?.[0] && (
            <img
              src={listing.image_urls[0]}
              alt={listing.title}
              className="w-full h-64 object-cover rounded-t-xl"
            />
          )}

          <div className="p-6">
            <div className="flex items-start justify-between">
              <div>
                <h2 className="text-2xl font-bold text-gray-900">{listing.title}</h2>
                <p className="text-gray-500 mt-1">{listing.address}</p>
                <p className="text-gray-500">{listing.city}, {listing.province_state} {listing.postal_code} {listing.country}</p>
              </div>
              <span className="text-sm bg-blue-100 text-blue-700 px-3 py-1 rounded-full font-medium">
                {listing.source_name}
              </span>
            </div>

            <div className="mt-4 text-3xl font-bold text-blue-600">
              {formatPrice(listing.price)}
            </div>

            <div className="mt-6 grid grid-cols-2 sm:grid-cols-3 gap-4">
              <Stat label="Units" value={listing.num_units} />
              <Stat label="Price/Unit" value={listing.price_per_unit ? formatPrice(listing.price_per_unit) : null} />
              <Stat label="Cap Rate" value={listing.cap_rate ? `${listing.cap_rate}%` : null} />
              <Stat label="NOI" value={listing.noi ? formatPrice(listing.noi) : null} />
              <Stat label="Occupancy" value={listing.occupancy_rate ? `${listing.occupancy_rate}%` : null} />
              <Stat label="Year Built" value={listing.year_built} />
              <Stat label="Floors" value={listing.num_floors} />
              <Stat label="Sq Ft" value={listing.square_footage?.toLocaleString()} />
              <Stat label="Type" value={listing.property_type} />
            </div>

            {listing.description && (
              <div className="mt-6">
                <h3 className="font-semibold text-gray-700 mb-2">Description</h3>
                <p className="text-gray-600 text-sm leading-relaxed">{listing.description}</p>
              </div>
            )}

            {(listing.broker_name || listing.broker_phone || listing.broker_email) && (
              <div className="mt-6 bg-gray-50 rounded-lg p-4">
                <h3 className="font-semibold text-gray-700 mb-2">Broker Contact</h3>
                {listing.broker_name && <p className="text-sm text-gray-600">{listing.broker_name}</p>}
                {listing.broker_phone && <p className="text-sm text-gray-600">{listing.broker_phone}</p>}
                {listing.broker_email && (
                  <p className="text-sm text-blue-600">
                    <a href={`mailto:${listing.broker_email}`}>{listing.broker_email}</a>
                  </p>
                )}
              </div>
            )}

            {listing.listing_url && (
              <div className="mt-4">
                <a
                  href={listing.listing_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-600 hover:underline text-sm"
                >
                  View Original Listing
                </a>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

function Stat({ label, value }) {
  if (!value) return null;
  return (
    <div className="bg-gray-50 rounded-lg p-3">
      <div className="text-xs text-gray-500 uppercase tracking-wide">{label}</div>
      <div className="text-lg font-semibold text-gray-900 mt-1">{value}</div>
    </div>
  );
}
