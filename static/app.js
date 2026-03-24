document.addEventListener("DOMContentLoaded", async () => {
  const endpoint = "/api/metrics";
  try {
    const response = await fetch(endpoint);
    if (!response.ok) return;
    const data = await response.json();
    const el = document.createElement("div");
    el.className = "container";
    el.style.paddingBottom = "1.2rem";
    el.innerHTML = `<p style="color:#64748b;margin:0;">Live Metrics → Total Records: <strong style="color:#0f172a;">${data.total}</strong></p>`;
    document.body.appendChild(el);
  } catch (_err) {}
});
