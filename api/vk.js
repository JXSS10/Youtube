import fetch from "node-fetch";

export default async function handler(req, res) {
  const videoUrl = req.query.url;

  if (!videoUrl || !videoUrl.includes("vk.com")) {
    return res.status(400).json({ error: "Invalid VK URL" });
  }

  try {
    // Force desktop mode — لأن m.vk.com لا يحتوي روابط الفيديو
    const cleanURL = videoUrl.replace("m.vk.com", "vk.com");

    const page = await fetch(cleanURL, {
      headers: {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
      }
    });

    const html = await page.text();

    // 1️⃣ محاولة استخراج الروابط من JSON (Desktop)
    let matches = [...html.matchAll(/"url(\d+)":"([^"]+)"/g)];

    if (matches.length === 0) {
      // 2️⃣ محاولة ثانية للبحث عن صيغة أخرى
      matches = [...html.matchAll(/"url_(\d+)":"([^"]+)"/g)];
    }

    if (matches.length === 0) {
      // 3️⃣ محاولة ثالثة: روابط player_inline
      matches = [...html.matchAll(/"cache(\d+)":"([^"]+)"/g)];
    }

    if (matches.length === 0) {
      return res.status(400).json({ error: "Video links not found (VK changed layout)" });
    }

    // ترتيب أجود فيديو
    const videos = matches.map(m => ({
      quality: parseInt(m[1]),
      url: m[2].replace(/\\/g, "") // إزالة backslashes
    }));

    videos.sort((a, b) => b.quality - a.quality);

    const best = videos[0];

    // إرسال الفيديو مباشرة
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
