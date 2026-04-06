import { useState } from 'react';

const US_STATES = [
  'AL','AK','AZ','AR','CA','CO','CT','DE','DC','FL','GA','HI','ID','IL','IN',
  'IA','KS','KY','LA','ME','MD','MA','MI','MN','MS','MO','MT','NE','NV','NH',
  'NJ','NM','NY','NC','ND','OH','OK','OR','PA','RI','SC','SD','TN','TX','UT',
  'VT','VA','WA','WV','WI','WY'
];

const CA_PROVINCES = ['AB','BC','MB','NB','NL','NS','NT','NU','ON','PE','QC','SK','YT'];

export default function FilterPanel({ filters, onFilterChange }) {
  const [isOpen, setIsOpen] = useState(false);

  const handleChange = (key, value) => {
    onFilterChange({ [key]: value || null });
  };

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="w-full px-4 py-3 flex items-center justify-between text-left font-medium text-gray-700 hover:bg-gray-50"
      >
        <span>Filters</span>
        <svg className={`w-5 h-5 transition-transform ${isOpen ? 'rotate-180' : ''}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
        </svg>
      </button>

      {isOpen && (
        <div className="p-4 border-t border-gray-200 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-600 mb-1">Country</label>
            <select
              value={filters.country || ''}
              onChange={(e) => handleChange('country', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">All Countries</option>
              <option value="CA">Canada</option>
              <option value="US">United States</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-600 mb-1">Province / State</label>
            <select
              value={filters.province_state || ''}
              onChange={(e) => handleChange('province_state', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">All</option>
              <optgroup label="Canada">
                {CA_PROVINCES.map(s => <option key={s} value={s}>{s}</option>)}
              </optgroup>
              <optgroup label="United States">
                {US_STATES.map(s => <option key={s} value={s}>{s}</option>)}
              </optgroup>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-600 mb-1">City</label>
            <input
              type="text"
              value={filters.city || ''}
              onChange={(e) => handleChange('city', e.target.value)}
              placeholder="Any city"
              className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-600 mb-1">Min Price</label>
            <input
              type="number"
              value={filters.min_price || ''}
              onChange={(e) => handleChange('min_price', e.target.value)}
              placeholder="No minimum"
              className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-600 mb-1">Max Price</label>
            <input
              type="number"
              value={filters.max_price || ''}
              onChange={(e) => handleChange('max_price', e.target.value)}
              placeholder="No maximum"
              className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-600 mb-1">Min Units</label>
            <input
              type="number"
              value={filters.min_units || ''}
              onChange={(e) => handleChange('min_units', e.target.value)}
              placeholder="No minimum"
              className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-600 mb-1">Max Units</label>
            <input
              type="number"
              value={filters.max_units || ''}
              onChange={(e) => handleChange('max_units', e.target.value)}
              placeholder="No maximum"
              className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-600 mb-1">Min Cap Rate (%)</label>
            <input
              type="number"
              step="0.1"
              value={filters.min_cap_rate || ''}
              onChange={(e) => handleChange('min_cap_rate', e.target.value)}
              placeholder="No minimum"
              className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-600 mb-1">Max Cap Rate (%)</label>
            <input
              type="number"
              step="0.1"
              value={filters.max_cap_rate || ''}
              onChange={(e) => handleChange('max_cap_rate', e.target.value)}
              placeholder="No maximum"
              className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-600 mb-1">Sort By</label>
            <select
              value={filters.sort_by || 'fetched_at'}
              onChange={(e) => handleChange('sort_by', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="fetched_at">Newest First</option>
              <option value="price">Price</option>
              <option value="num_units">Units</option>
              <option value="cap_rate">Cap Rate</option>
              <option value="city">City</option>
              <option value="province_state">Province/State</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-600 mb-1">Order</label>
            <select
              value={filters.sort_order || 'desc'}
              onChange={(e) => handleChange('sort_order', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="desc">Descending</option>
              <option value="asc">Ascending</option>
            </select>
          </div>
        </div>
      )}
    </div>
  );
}
