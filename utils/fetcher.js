import fetch from "node-fetch";

export async function fetchFile(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error("Cannot fetch file");
  return res.body;
}
