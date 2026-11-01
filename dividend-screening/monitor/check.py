#!/usr/bin/env python3
"""高配当ウォッチリストの判定。

使い方: python3 check.py prices.json
prices.json の形式:
{"date": "2026-11-04",
 "prices": {"1928": {"price": 3350, "source": "URL", "dps": 145,
                     "warning": "減配・下方修正などがあれば1行で"}}}
 - dps は配当予想が変わったときだけ入れる（watchlist.csv の値を上書き）
出力: reports/<date>.md を作り、state.json を更新し、通知すべき内容を標準出力に出す。
"""
import csv, json, sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
LEVELS = ["待機", "接近", "買い目安", "強い買い"]

def level(price, dps):
    y = dps / price
    if y >= 0.045: return "強い買い"
    if y >= 0.04: return "買い目安"
    if y >= 0.04 / 1.03: return "接近"   # 4%になる株価の+3%以内
    return "待機"

def main(path):
    data = json.load(open(path, encoding="utf-8"))
    date = data["date"]; prices = data["prices"]
    wl = list(csv.DictReader(open(os.path.join(HERE, "watchlist.csv"), encoding="utf-8")))
    sp = os.path.join(HERE, "state.json")
    state = json.load(open(sp, encoding="utf-8"))
    alerts, rows = [], []
    for w in wl:
        c = w["code"]; p = prices.get(c)
        dps = float(w["dps"])
        if not p or not p.get("price"):
            rows.append(f"| {c} | {w['name']} | 取得失敗 | {dps:g} | - | {dps/0.04:,.0f} | - | {state.get(c,{}).get('level','-')} |")
            continue
        price = float(p["price"])
        if p.get("dps") is not None and float(p["dps"]) != dps:
            alerts.append(f"⚠️ {w['name']}({c}) 配当予想の変更: {dps:g}円 → {float(p['dps']):g}円。watchlist.csvを更新してください")
            dps = float(p["dps"])
        lv = level(price, dps)
        prev = state.get(c, {}).get("level")
        y = dps / price * 100
        if p.get("warning"):
            alerts.append(f"⚠️ {w['name']}({c}) {p['warning']}")
        if prev is not None and LEVELS.index(lv) > LEVELS.index(prev) and lv in ("接近", "買い目安", "強い買い"):
            alerts.append(f"{'🟡' if lv=='接近' else '🟢'} {w['name']}({c}) が「{lv}」に入りました: 株価{price:,.0f}円・利回り{y:.2f}%（4%になる株価 {dps/0.04:,.0f}円）[{w['tier']}]")
        elif prev is None and lv == "強い買い":
            alerts.append(f"🟢 {w['name']}({c}) は初回から「強い買い」です: 株価{price:,.0f}円・利回り{y:.2f}%")
        chg = (price / float(w["ref_price"]) - 1) * 100
        rows.append(f"| {c} | {w['name']} | {price:,.1f} | {dps:g} | {y:.2f}% | {dps/0.04:,.0f} | {chg:+.1f}% | {lv} |")
        state[c] = {"level": lv, "price": price, "date": date}
    json.dump(state, open(sp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    rep = [f"# 高配当ウォッチ {date}", "", "## 通知"] + ([f"- {a}" for a in alerts] or ["- なし"]) + [
        "", "## 一覧", "| コード | 銘柄 | 株価 | 予想配当 | 利回り | 4%になる株価 | 基準株価比 | 判定 |", "|---|---|---|---|---|---|---|---|"] + rows + [
        "", "判定：強い買い＝利回り4.5%以上／買い目安＝4%以上／接近＝4%になる株価の+3%以内。投資助言ではありません。"]
    os.makedirs(os.path.join(HERE, "reports"), exist_ok=True)
    open(os.path.join(HERE, "reports", f"{date}.md"), "w", encoding="utf-8").write("\n".join(rep) + "\n")
    print("ALERTS:" if alerts else "ALERTS: なし")
    for a in alerts: print(a)

if __name__ == "__main__":
    main(sys.argv[1])
