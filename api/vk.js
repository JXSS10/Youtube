import fetch from "node-fetch";

export default async function handler(req, res) {
  const videoUrl = req.query.url;

  if (!videoUrl || !videoUrl.includes("vk.com")) {
    return res.status(400).json({ error: "Invalid VK URL" });
  }

  try {
    // جلب HTML الصفحة
    const page = await fetch(videoUrl);
    const html = await page.text();

    // البحث عن روابط الفيديو داخل الـ JSON
    const matches = [...html.matchAll(/"url_\d+":\s*"([^"]+)"/g)];

    if (!matches.length) {
      return res.status(400).json({ error: "No video links found" });
    }

    // اختيار أعلى جودة متاحة
    const videos = matches.map(m => ({
      quality: parseInt(m[0].match(/url_(\d+)/)[1]),
      url: m[1]
    }));

    videos.sort((a, b) => b.quality - a.quality);

    const best = videos[0];

    // Header التحميل
    res.setHeader("Content-Type", "video/mp4");
    res.setHeader(
      "Content-Disposition",
      `attachment; filename="vk_${best.quality}p.mp4"`
    );

    const stream = await fetch(best.url);
    stream.body.pipe(res);

  } catch (err) {
    res.status(500).json({ error: err.message });
  }
}
