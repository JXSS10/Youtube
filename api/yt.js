import ytdl from "ytdl-core";
import { getCache, setCache } from "../utils/cache.js";

export default async function yt(req, res) {
  const { url } = req.query;

  if (!ytdl.validateURL(url))
    return res.status(400).json({ error: "Invalid YouTube URL" });

  const c = getCache(url);
  if (c) return c.pipe(res);

  try {
    res.setHeader("Content-Type", "video/mp4");
    const stream = ytdl(url, { quality: "highest" });
    setCache(url, stream);
    stream.pipe(res);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
}
