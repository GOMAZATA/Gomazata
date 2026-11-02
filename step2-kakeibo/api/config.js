// ブラウザに Supabase の接続先を渡す。
// どちらも公開してよい値（anon キーは RLS で守られる前提の鍵）。
export default function handler(req, res) {
  const { SUPABASE_URL, SUPABASE_ANON_KEY } = process.env;
  if (!SUPABASE_URL || !SUPABASE_ANON_KEY) {
    res.status(500).json({ error: "SUPABASE_URL と SUPABASE_ANON_KEY を Vercel の環境変数に設定してください。" });
    return;
  }
  res.setHeader("Cache-Control", "no-store");
  res.status(200).json({ supabaseUrl: SUPABASE_URL, supabaseAnonKey: SUPABASE_ANON_KEY });
}
