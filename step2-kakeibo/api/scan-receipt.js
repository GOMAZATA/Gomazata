// レシート画像を Claude に読ませて、金額・日付・お店・カテゴリを返す。
// ANTHROPIC_API_KEY はサーバー側（Vercel の環境変数）にだけ置き、ブラウザには出さない。
import Anthropic from "@anthropic-ai/sdk";
import { createClient } from "@supabase/supabase-js";

const anthropic = new Anthropic();
const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_ANON_KEY);

const CATEGORIES = ["food", "daily", "move", "fun", "home", "other"];
const MEDIA_TYPES = ["image/jpeg", "image/png", "image/webp"];
const MAX_BASE64_LENGTH = 4_000_000; // Vercel の本文上限 4.5MB に収める

const SCHEMA = {
  type: "object",
  properties: {
    is_receipt: { type: "boolean", description: "画像がレシートや領収書ならtrue" },
    total: { type: "integer", description: "支払った合計金額（税込・円）。読めなければ0" },
    date: { type: "string", description: "購入日 YYYY-MM-DD。読めなければ空文字" },
    store: { type: "string", description: "お店の名前（20文字以内）。読めなければ空文字" },
    category: { type: "string", enum: CATEGORIES },
  },
  required: ["is_receipt", "total", "date", "store", "category"],
  additionalProperties: false,
};

const SYSTEM = `あなたは日本のレシートを家計簿に記帳する係です。画像から次を読み取ります。
- total: 実際に支払った合計（「合計」「お買上計」「領収金額」など）。お預り・お釣り・小計・ポイントは使わない。
- date: 購入日。和暦や「24/11/2」のような書き方は西暦のYYYY-MM-DDに直す。年が書かれていなければ今日の日付から推測する。
- store: お店の名前。
- category: food=食料品・外食・カフェ、daily=ドラッグストア・日用品・服、move=交通・ガソリン・駐車場、fun=本・趣味・娯楽、home=家賃・光熱費・家具家電、other=それ以外。
レシートでない画像なら is_receipt を false にする。`;

export default async function handler(req, res) {
  if (req.method !== "POST") {
    res.status(405).json({ error: "POST で送ってください。" });
    return;
  }

  // ログイン中の人だけが使える（知らない人に API 代を使われないように）
  const token = (req.headers.authorization || "").replace(/^Bearer /, "");
  const { data: auth, error: authError } = token ? await supabase.auth.getUser(token) : { data: null };
  if (authError || !auth?.user) {
    res.status(401).json({ error: "ログインし直してください。" });
    return;
  }

  const { image, mediaType = "image/jpeg", today } = req.body || {};
  if (typeof image !== "string" || !image || image.length > MAX_BASE64_LENGTH || !MEDIA_TYPES.includes(mediaType)) {
    res.status(400).json({ error: "画像が読み込めませんでした。撮り直してください。" });
    return;
  }
  const todayText = /^\d{4}-\d{2}-\d{2}$/.test(today || "") ? today : new Date().toISOString().slice(0, 10);

  try {
    const response = await anthropic.beta.messages.create({
      model: "claude-opus-5-5",
      max_tokens: 4000,
      betas: ["server-side-fallback-2026-07-01"],
      fallbacks: "default",
      output_config: { effort: "low", format: { type: "json_schema", schema: SCHEMA } },
      system: SYSTEM,
      messages: [
        {
          role: "user",
          content: [
            { type: "image", source: { type: "base64", media_type: mediaType, data: image } },
            { type: "text", text: `今日は ${todayText} です。このレシートを読み取ってください。` },
          ],
        },
      ],
    });

    if (response.stop_reason === "refusal") {
      res.status(422).json({ error: "この画像は読み取れませんでした。手で入力してください。" });
      return;
    }
    const text = response.content.find((block) => block.type === "text")?.text;
    const result = JSON.parse(text);

    if (!result.is_receipt || result.total <= 0) {
      res.status(422).json({ error: "レシートの合計金額が見つかりませんでした。明るい場所で全体が入るように撮ってください。" });
      return;
    }
    res.status(200).json({
      total: result.total,
      date: /^\d{4}-\d{2}-\d{2}$/.test(result.date) ? result.date : "",
      store: result.store.slice(0, 40),
      category: CATEGORIES.includes(result.category) ? result.category : "other",
    });
  } catch (err) {
    if (err instanceof Anthropic.RateLimitError) {
      res.status(429).json({ error: "混み合っています。少し待ってからもう一度撮ってください。" });
    } else if (err instanceof Anthropic.AuthenticationError) {
      console.error("ANTHROPIC_API_KEY is invalid");
      res.status(500).json({ error: "読み取りの設定に問題があります（APIキーを確認してください）。" });
    } else if (err instanceof Anthropic.APIError) {
      console.error("Claude API error", err.status, err.message);
      res.status(502).json({ error: "読み取りに失敗しました。もう一度試してください。" });
    } else {
      console.error(err);
      res.status(500).json({ error: "読み取りに失敗しました。もう一度試してください。" });
    }
  }
}
