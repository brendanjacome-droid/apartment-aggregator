import { useState } from 'react';
import { useListings } from './hooks/useListings';
import SearchBar from './components/SearchBar';
import FilterPanel from './components/FilterPanel';
import ListingGrid from './components/ListingGrid';
import ListingDetail from './components/ListingDetail';
import MapView from './components/MapView';

export default function App() {
  const { data, filters, loading, error, updateFilters, setPage } = useListings({ per_page: 20 });
  const [selectedListing, setSelectedListing] = useState(null);
  const [view, setView] = useState('grid');

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white border-b border-gray-200 sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between mb-3">
            <h1 className="text-2xl font-bold text-gray-900">
              Apartment Building Aggregator
            </h1>
            <div className="flex gap-2">
              <button
                onClick={() => setView('grid')}
                className={`px-3 py-1.5 text-sm rounded-md ${view === 'grid' ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'}`}
              >
                Grid
              </button>
              <button
                onClick={() => setView('map')}
                className={`px-3 py-1.5 text-sm rounded-md ${view === 'map' ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'}`}
              >
                Map
              </button>
            </div>
          </div>
          <SearchBar onSearch={updateFilters} />
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-6">
        <div className="mb-4">
          <FilterPanel filters={filters} onFilterChange={updateFilters} />
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-4">
            {error}
          </div>
        )}

        {loading ? (
          <div className="flex items-center justify-center py-20">
            <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-blue-600"></div>
          </div>
        ) : view === 'grid' ? (
          <ListingGrid
            listings={data.items}
            total={data.total}
            page={data.page}
            totalPages={data.total_pages}
            onPageChange={setPage}
            onSelect={setSelectedListing}
          />
        ) : (
          <div>
            <div className="mb-4 text-sm text-gray-500">
              Showing {data.items.length} of {data.total.toLocaleString()} listings on map
            </div>
            <MapView listings={data.items} onSelect={setSelectedListing} />
          </div>
        )}
      </main>

      {selectedListing && (
        <ListingDetail
          listing={selectedListing}
          onClose={() => setSelectedListing(null)}
        />
      )}
    </div>
  );
}
