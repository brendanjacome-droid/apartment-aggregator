const API_BASE = '/api';

export async function fetchListings(params = {}) {
  const searchParams = new URLSearchParams();
  Object.entries(params).forEach(([key, value]) => {
    if (value !== null && value !== undefined && value !== '') {
      searchParams.set(key, value);
    }
  });
  const res = await fetch(`${API_BASE}/listings?${searchParams}`);
  if (!res.ok) throw new Error(`Failed to fetch listings: ${res.statusText}`);
  return res.json();
}

export async function fetchListing(id) {
  const res = await fetch(`${API_BASE}/listings/${id}`);
  if (!res.ok) throw new Error(`Failed to fetch listing: ${res.statusText}`);
  return res.json();
}

export async function fetchSources() {
  const res = await fetch(`${API_BASE}/sources`);
  if (!res.ok) throw new Error(`Failed to fetch sources: ${res.statusText}`);
  return res.json();
}

export async function triggerFetch(sourceName) {
  const res = await fetch(`${API_BASE}/sources/${sourceName}/fetch`, { method: 'POST' });
  if (!res.ok) throw new Error(`Failed to trigger fetch: ${res.statusText}`);
  return res.json();
}

export async function fetchStats() {
  const res = await fetch(`${API_BASE}/stats`);
  if (!res.ok) throw new Error(`Failed to fetch stats: ${res.statusText}`);
  return res.json();
}
