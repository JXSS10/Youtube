export function detectPlatform(url) {
  if (/youtube\.com|youtu\.be/.test(url)) return "youtube";
  if (/tiktok\.com/.test(url)) return "tiktok";
  if (/facebook\.com|fb\.watch/.test(url)) return "facebook";
  return null;
}
