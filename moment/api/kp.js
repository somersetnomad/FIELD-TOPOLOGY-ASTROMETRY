// Latest planetary Kp index from NOAA SWPC, for the FTA Storm Rule.
module.exports = async (req, res) => {
  try {
    const r = await fetch('https://services.swpc.noaa.gov/products/noaa-planetary-k-index.json');
    const data = await r.json();
    let time, kp;
    const last = data[data.length - 1];
    if (Array.isArray(last)) { time = last[0]; kp = parseFloat(last[1]); }
    else { time = last.time_tag; kp = parseFloat(last.Kp != null ? last.Kp : last.kp_index); }
    if (!isFinite(kp)) throw new Error('no kp');
    res.setHeader('Cache-Control', 's-maxage=600, stale-while-revalidate=1800');
    return res.status(200).json({ kp, time, source: 'NOAA SWPC' });
  } catch (e) {
    res.setHeader('Cache-Control', 'no-store');
    return res.status(502).json({ kp: null });
  }
};
