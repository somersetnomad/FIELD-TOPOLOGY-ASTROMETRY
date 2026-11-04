// Confirms a Stripe Checkout Session from the FTA Field Report payment link.
// Set STRIPE_SECRET_KEY (a restricted key with Checkout Sessions: Read) in Vercel to verify
// sessions with Stripe. Without it, any well-formed session ID unlocks the free tier.
const PAYMENT_LINK = process.env.FTA_PAYMENT_LINK || 'plink_1UY2Y2Q3IPp8LqoC2bT17LFv';

module.exports = async (req, res) => {
  res.setHeader('Cache-Control', 'no-store');
  const sid = String((req.query && req.query.session_id) || '');
  if (!/^cs_(live|test)_[A-Za-z0-9]{10,200}$/.test(sid)) return res.status(400).json({ ok: false, reason: 'bad_session' });
  const key = process.env.STRIPE_SECRET_KEY;
  if (!key) return res.status(200).json({ ok: true, verified: false });
  try {
    const r = await fetch('https://api.stripe.com/v1/checkout/sessions/' + sid, { headers: { Authorization: 'Bearer ' + key } });
    if (!r.ok) return res.status(200).json({ ok: false, reason: 'not_found' });
    const s = await r.json();
    const ok = s.status === 'complete' && (!PAYMENT_LINK || s.payment_link === PAYMENT_LINK);
    return res.status(200).json({ ok, verified: true });
  } catch (e) {
    return res.status(502).json({ ok: false, reason: 'stripe_unreachable' });
  }
};
