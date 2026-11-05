# ごま家計簿 ステップ2 — ネットに公開する手順

ステップ1の家計簿を、スマホからどこでも使えるようにします。

```
スマホのブラウザ ──→ Vercel（画面と /api を置く場所）──→ Claude（レシートを読む）
        │
        └──────────→ Supabase（ログインと明細の保管庫）
```

- **Supabase**: ログイン（メールのリンク）と明細データを保存します。
- **Vercel**: アプリを公開します。`api/` フォルダの中身はサーバー側で動くので、Claude の API キーを安全に置けます。
- **Claude API**: レシート写真から合計金額・日付・お店・カテゴリを読み取ります。

かかるお金: Supabase と Vercel は無料枠で足ります。Claude API は使った分だけ課金されます（レシート1枚あたり数円ほど）。

---

## 1. Supabase を用意する（約10分）

1. https://supabase.com でアカウントを作り、「New project」を作る（リージョンは Tokyo がおすすめ）。
2. 左メニュー **SQL Editor** を開き、[`supabase/schema.sql`](supabase/schema.sql) の中身を貼り付けて **Run**。
   - 明細を入れる `entries` テーブルができます。
   - **RLS（行レベルセキュリティ）** も一緒に有効になり、自分の明細は自分しか読めません。
3. 左メニュー **Project Settings → API** で次の2つをメモ（あとで Vercel に入れます）。
   - Project URL（`https://xxxx.supabase.co`）
   - `anon` `public` キー
   - ⚠️ `service_role` キーは使いません。どこにも貼らないでください。

## 2. Claude の API キーを用意する（約5分）

1. https://console.anthropic.com でアカウントを作り、支払い方法を登録。
2. **API Keys** で新しいキーを作ってメモ。
3. 使いすぎ防止に **Limits** で月の上限金額（例: $5）を設定しておくと安心です。

## 3. Vercel で公開する（約10分）

1. https://vercel.com に GitHub アカウントでログイン。
2. **Add New → Project** で、このリポジトリ（Gomazata）を選ぶ。
3. **Root Directory** を `step2-kakeibo` に変更。
4. **Environment Variables** に入れる（`ALLOWED_EMAILS` は任意だけどおすすめ）。

   | 名前 | 値 |
   |---|---|
   | `SUPABASE_URL` | 手順1でメモした Project URL |
   | `SUPABASE_ANON_KEY` | 手順1でメモした anon キー |
   | `ANTHROPIC_API_KEY` | 手順2で作った API キー |
   | `ALLOWED_EMAILS` | レシート読み取りを使ってよいメールアドレス。複数ならカンマ区切り（例: `me@example.com,family@example.com`） |

5. **Deploy** を押す。`https://〇〇.vercel.app` のような URL ができます。

## 4. ログインのリンク先を登録する（2分）

Supabase の **Authentication → URL Configuration** を開いて:

- **Site URL** に Vercel の URL（`https://〇〇.vercel.app`）を入れる。
- **Redirect URLs** にも同じ URL を追加。

これを忘れると、メールのリンクを押しても家計簿に戻ってきません。

### 知らない人に使われないようにする（おすすめ）

このままだと、URL を知った人は誰でもメールアドレスを入れてアカウントを作れます（他の人の明細は RLS で見えません）。
自分と家族がログインできたら、Supabase の **Authentication → Sign In / Providers** で
**Allow new users to sign up** をオフにすると、新しい人はアカウントを作れなくなります。

レシート読み取りは、1人1日20回までに制限しています（`supabase/schema.sql` の `claim_scan`）。

## 5. 使ってみる

1. スマホで Vercel の URL を開く → メールアドレスを入れて「ログインリンクを送る」。
2. 届いたメールのリンクを押すとログイン完了。
3. 「レシートを撮って読み取る」→ カメラでレシートを撮影。
4. 金額・日付・お店・カテゴリが入るので、確かめて「記帳する」。
5. ホーム画面に追加しておくと、アプリのように開けます（Safari の共有ボタン →「ホーム画面に追加」）。

---

## 困ったとき

| 症状 | 確かめること |
|---|---|
| 「設定が終わっていません」と出る | Vercel の環境変数 `SUPABASE_URL` と `SUPABASE_ANON_KEY`。変えたら **Redeploy** が必要 |
| メールのリンクを押しても戻ってこない | 手順4の Site URL / Redirect URLs |
| メールが届かない | 迷惑メールフォルダ。Supabase 標準のメール送信は1時間に数通までの制限あり |
| 「読み取りの設定に問題があります」 | `ANTHROPIC_API_KEY` が正しいか、Anthropic Console に残高があるか |
| 「ログインし直してください」 | 一度ログアウトしてログインし直す |

## しくみ（ステップ3で深掘りすること）

- **鍵の置き場所**: `ANTHROPIC_API_KEY` は Vercel のサーバー側だけにあり、ブラウザには届きません。Supabase の anon キーはブラウザに渡りますが、RLS があるので他人の明細は読めません。
- **知らない人に API 代を使わせない**: `/api/scan-receipt` はログイン中の人のトークンを Supabase で確かめてから Claude を呼びます。
- **写真は保存しない**: レシート画像は読み取りに使うだけで、どこにも保存しません。
