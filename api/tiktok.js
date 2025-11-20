import { fetchFile } from "../utils/fetcher.js";

export default async function tiktok(req, res) {
  const { url } = req.query;

  const api = `https://api.tikmate.app/api/lookup?url=${encodeURIComponent(url)}`;
  const data = await (await fetch(api)).json();

  const video = await fetchFile(data.video_url);

  res.setHeader("Content-Type", "video/mp4");
  video.pipe(res);
}
