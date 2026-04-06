import { useState, useEffect, useCallback } from 'react';
import { fetchListings } from '../api/client';

export function useListings(initialFilters = {}) {
  const [data, setData] = useState({ items: [], total: 0, page: 1, per_page: 20, total_pages: 0 });
  const [filters, setFilters] = useState(initialFilters);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const result = await fetchListings(filters);
      setData(result);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }, [filters]);

  useEffect(() => {
    load();
  }, [load]);

  const updateFilters = useCallback((newFilters) => {
    setFilters(prev => ({ ...prev, ...newFilters, page: 1 }));
  }, []);

  const setPage = useCallback((page) => {
    setFilters(prev => ({ ...prev, page }));
  }, []);

  return { data, filters, loading, error, updateFilters, setPage, reload: load };
}
