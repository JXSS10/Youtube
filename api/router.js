import { detectPlatform } from "../utils/validator.js";

export default async function handler(req, res) {
  const { url } = req.query;

  const platform = detectPlatform(url);

  if (!platform)
    return res.status(400).json({ error: "Unsupported platform" });

  if (platform === "youtube")
    return import("./yt.js").then(m => m.default(req, res));

  if (platform === "tiktok")
    return import("./tiktok.js").then(m => m.default(req, res));

  if (platform === "facebook")
    return import("./fb.js").then(m => m.default(req, res));
}
