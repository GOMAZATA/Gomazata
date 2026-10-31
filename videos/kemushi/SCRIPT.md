# だい2わ「けむしが いた！」— 台本（案）

形式：前回（だい1わ「かめむしが ついちゃった！」）と同じ絵本スタイル
- クリーム色の背景、まんなかに正方形のイラスト、下にひらがなのセリフ、右下に「いち／はち」のページ番号
- 左上にタイトル「けむしが いた！」
- 1280×720・24fps ／ 全8ページ・約1分

声：ElevenLabs「Hina – cute and friendly」（前回と同じ設定：speed 1.15 / stability 100 / similarity 99 / v4）
→ 1ページ1ファイルで書き出してください（ファイル名に番号 01〜08 を入れてもらえると助かります）

主人公：前回と同じ女の子（黒髪ボブ・青い目・白いもこもこセーター・緑のスカート・深緑のブーツ、フェルト人形風3D）

---

| p | ナレーション（読み上げ） | 小さい補足文字 | 絵 |
|---|---|---|---|
| いち | おさんぽ、おさんぽ。きょうは なにが いるかな？ | | 女の子が公園の小道を歩く（前回の1ページ目と同じ構図） |
| に | あれ？ はっぱに なにか いるよ。 | | 女の子が立ち止まり、ツバキの生け垣をのぞきこむ（距離はまだ少し遠め） |
| さん | けむしだ！ もじゃもじゃの けが、いっぱい。 | | ツバキの葉のうらに、黄色っぽい毛虫が何匹も並んでいる（女の子は少しはなれて目をまるくしている） |
| よん | けむしの けはね、かぜで ふわっと とんでくるの。 | ちかくに いるだけで、かゆく なることが あるよ。 | 風が吹き、小さな毛がキラキラふわっと舞う（女の子は手で口をおさえる） |
| ご | だから、ちかづかない。さわらない。 | ぼうで つつくのも だめだよ。 | 女の子が一歩うしろにさがり、両手を背中にまわしている |
| ろく | 「おかあさーん！ けむしが いたよ！」 | みつけたら、おとなに おしえてね。 | 女の子がふりかえって、おかあさん（手と足元だけ映る大人でもOK）に指さして知らせる |
| なな | もし さわっちゃったら？ こすらないで、すぐ おとなに いってね。 | | 女の子が腕を見て「あっ」→ おかあさんのところへ走っていく |
| はち | けむしを みつけたら、ちかづかない、さわらない、おとなに いう。またね。 | | 女の子が笑顔で手をふる（前回の最後のページと同じ雰囲気） |

### 内容のチェック用メモ
- チャドクガ：ツバキ・サザンカにつく。毛（毒針毛）は風で飛び、近くにいるだけでかぶれることがある。ぬけがらにも毒が残る。
- 子どもには毛虫の見分けはさせない → 「毛虫は全部、ちかづかない・さわらない・おとなに言う」で統一。
- さわった後の手当て（テープで毛をとる・水で流す・着がえる・皮膚科）は大人の仕事。必要なら概要欄に「おうちの方へ」として書く。

---

## 絵の生成プロンプト（前回と同じツールで作る場合）
共通：`Same girl as reference: felt / wool doll style 3D chibi girl, black bob hair, big blue eyes, rosy cheeks, cream fluffy sweater, green skirt, dark green boots. Soft sunny garden park, shallow depth of field, warm picture-book lighting. Square 1:1. No text.`

- p2: `the girl stops on a garden path and peeks curiously at a camellia hedge from a little distance`
- p3: `close-up of the underside of a glossy camellia leaf with a row of small pale-yellow hairy caterpillars; the girl in the background, a safe distance away, eyes wide`
- p4: `a gentle breeze blows; tiny glittering hairs float in the air from the caterpillars toward the viewer; the girl covers her mouth with both hands, surprised`
- p5: `the girl takes one step back from the hedge, both hands held behind her back, serious but cute face`
- p6: `the girl turns around and points toward the hedge, calling out happily to her mother; only the mother's hand and legs visible`
- p7: `the girl looks at her forearm with a worried face, then runs toward her mother`
- p8: `the girl smiles and waves goodbye on the garden path, sunny`
