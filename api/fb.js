import { fetchFile } from "../utils/fetcher.js";

export default async function fb(req, res) {
  const { url } = req.query;

  const api = `https://fbdownloader.net/api?url=${encodeURIComponent(url)}`;
  const json = await (await fetch(api)).json();

  const video = await fetchFile(json.hd || json.sd);

  res.setHeader("Content-Type", "video/mp4");
  video.pipe(res);
}
