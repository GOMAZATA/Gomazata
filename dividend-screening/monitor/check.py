#!/usr/bin/env python3
"""高配当ウォッチリストの判定。

使い方: python3 check.py prices.json
prices.json の形式:
{"date": "2026-11-07",
 "prices": {"1928": {"price": 3350, "source": "URL", "dps": 145,
                     "warning": "減配・下方修正などがあれば1行で"}}}
 - dps は配当予想が変わったときだけ入れる（watchlist.csv / holdings.csv の値を上書き）

holdings.csv（任意・非公開。.gitignore 済みでコミットしない）:
 code,name,shares,cost_per_share,account,dps
 - watchlist.csv にない保有銘柄も判定対象になる（tier=hold）
 - account が NISA の配当は非課税、それ以外は20.315%課税として計算

出力:
 - reports/<date>.md          … 公開してよい一覧（保有情報を含まない）
 - reports/private_<date>.md  … 保有銘柄の評価額・受取配当（コミットしない）
 - state.json の更新、標準出力に通知内容
"""
import csv, json, sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
LEVELS = ["待機", "接近", "買い目安", "強い買い"]
TAX = 0.20315


def level(price, dps):
    y = dps / price
    if y >= 0.045: return "強い買い"
    if y >= 0.04: return "買い目安"
    if y >= 0.04 / 1.03: return "接近"   # 4%になる株価の+3%以内
    return "待機"


def load_holdings():
    hp = os.path.join(HERE, "holdings.csv")
    if not os.path.exists(hp):
        return {}
    hold = {}
    for h in csv.DictReader(open(hp, encoding="utf-8")):
        c = h["code"]
        if c in hold:  # 同じ銘柄を複数口座で保有
            hold[c]["lots"].append(h)
        else:
            hold[c] = {"name": h["name"], "dps": h.get("dps", ""), "lots": [h]}
    return hold


def main(path):
    data = json.load(open(path, encoding="utf-8"))
    date = data["date"]; prices = data["prices"]
    wl = list(csv.DictReader(open(os.path.join(HERE, "watchlist.csv"), encoding="utf-8")))
    hold = load_holdings()
    known = {w["code"] for w in wl}
    for c, h in hold.items():
        if c not in known:
            wl.append({"code": c, "name": h["name"], "tier": "hold", "dps": h["dps"] or "", "ref_price": ""})
    sp = os.path.join(HERE, "state.json")
    state = json.load(open(sp, encoding="utf-8"))
    alerts, rows, hrows = [], [], []
    tot = {"value": 0, "pre": 0, "post": 0}
    for w in wl:
        c = w["code"]; p = prices.get(c)
        public = w["tier"] != "hold"
        tag = ""
        if c in hold:
            tag = f" [保有{sum(int(l['shares']) for l in hold[c]['lots'])}株]"
        if not w["dps"]:
            dps = None
        else:
            dps = float(w["dps"])
        if not p or not p.get("price"):
            if public:
                rows.append(f"| {c} | {w['name']} | 取得失敗 | {w['dps']} | - | - | - | {state.get(c,{}).get('level','-')} |")
            if c in hold:
                hrows.append(f"| {c} | {w['name']} | 取得失敗 | | | | | |")
            continue
        price = float(p["price"])
        if p.get("dps") is not None and (dps is None or float(p["dps"]) != dps):
            alerts.append(f"⚠️ {w['name']}({c}){tag} 配当予想の変更: {dps if dps is not None else '未登録'}円 → {float(p['dps']):g}円")
            dps = float(p["dps"])
        if p.get("warning"):
            alerts.append(f"⚠️ {w['name']}({c}){tag} {p['warning']}")
        lv = level(price, dps) if dps else "配当なし/未確認"
        if dps:
            prev = state.get(c, {}).get("level")
            y = dps / price * 100
            if prev in LEVELS and LEVELS.index(lv) > LEVELS.index(prev) and lv in ("接近", "買い目安", "強い買い"):
                mark = "🟡" if lv == "接近" else "🟢"
                alerts.append(f"{mark} {w['name']}({c}){tag} が「{lv}」に入りました: 株価{price:,.0f}円・利回り{y:.2f}%（4%になる株価 {dps/0.04:,.0f}円）[{w['tier']}]")
            elif prev is None and lv == "強い買い" and public:
                alerts.append(f"🟢 {w['name']}({c}) は初回から「強い買い」です: 株価{price:,.0f}円・利回り{y:.2f}%")
            if public:
                chg = (price / float(w["ref_price"]) - 1) * 100 if w.get("ref_price") else 0
                rows.append(f"| {c} | {w['name']} | {price:,.1f} | {dps:g} | {y:.2f}% | {dps/0.04:,.0f} | {chg:+.1f}% | {lv} |")
            if public:  # 保有のみの銘柄は公開の state.json に残さない
                state[c] = {"level": lv, "price": price, "date": date}
        if c in hold:
            for l in hold[c]["lots"]:
                sh = int(l["shares"]); cost = l.get("cost_per_share") or ""
                nisa = "NISA" in (l.get("account") or "")
                pre = (dps or 0) * sh
                post = pre if nisa else pre * (1 - TAX)
                pl = f"{(price-float(cost))*sh:+,.0f}円" if cost else "-"
                yoc = f"{dps/float(cost)*100:.2f}%" if (cost and dps) else "-"
                tot["value"] += price * sh; tot["pre"] += pre; tot["post"] += post
                hrows.append(f"| {c} | {w['name']} | {l.get('account','')} | {sh} | {price*sh:,.0f}円 | {pl} | {pre:,.0f}円 | {post:,.0f}円 | {yoc} | {lv} |")
    json.dump(state, open(sp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    os.makedirs(os.path.join(HERE, "reports"), exist_ok=True)
    pub_alerts = [a for a in alerts if "[保有" not in a]
    rep = [f"# 高配当ウォッチ {date}", "", "## 通知"] + ([f"- {a}" for a in pub_alerts] or ["- なし"]) + [
        "", "## 一覧", "| コード | 銘柄 | 株価 | 予想配当 | 利回り | 4%になる株価 | 基準株価比 | 判定 |", "|---|---|---|---|---|---|---|---|"] + rows + [
        "", "判定：強い買い＝利回り4.5%以上／買い目安＝4%以上／接近＝4%になる株価の+3%以内。投資助言ではありません。"]
    open(os.path.join(HERE, "reports", f"{date}.md"), "w", encoding="utf-8").write("\n".join(rep) + "\n")
    if hold:
        prv = [f"# 保有銘柄 {date}（非公開・コミットしない）", "", "## 通知"] + ([f"- {a}" for a in alerts if "[保有" in a] or ["- なし"]) + [
            "", "| コード | 銘柄 | 口座 | 株数 | 評価額 | 評価損益 | 年間配当(税引前) | 年間配当(税引後) | 取得価格ベース利回り | 判定 |",
            "|---|---|---|---|---|---|---|---|---|---|"] + hrows + [
            "", f"合計：評価額 {tot['value']:,.0f}円／年間配当 税引前 {tot['pre']:,.0f}円・税引後 {tot['post']:,.0f}円（NISAは非課税で計算）"]
        open(os.path.join(HERE, "reports", f"private_{date}.md"), "w", encoding="utf-8").write("\n".join(prv) + "\n")
    print("ALERTS:" if alerts else "ALERTS: なし")
    for a in alerts: print(a)


if __name__ == "__main__":
    main(sys.argv[1])
