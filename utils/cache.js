const cache = new Map();

export function setCache(key, value) {
  cache.set(key, { value, time: Date.now() });
}

export function getCache(key) {
  const item = cache.get(key);
  if (!item) return null;

  // 10 دقائق
  if (Date.now() - item.time > 600000) {
    cache.delete(key);
    return null;
  }

  return item.value;
}
