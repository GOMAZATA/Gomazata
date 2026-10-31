# だい2わ「どんぐりから むしが でてきた！」— 台本（案）

形式：前回（だい1わ「かめむしが ついちゃった！」）と同じ絵本スタイル
- クリーム色の背景、まんなかに正方形のイラスト、下にひらがなのセリフ（必要なら小さい補足文字）、右下に「いち／はち」
- 左上にタイトル「どんぐりから むしが でてきた！」
- 1280×720・24fps ／ 全8ページ・約1分

声：ElevenLabs「Hina – cute and friendly」（前回と同じ：speed 1.15 / stability 100 / similarity 99 / v4）
→ 1ページ1ファイル、ファイル名に 01〜08 を入れて書き出し

主人公：前回と同じ女の子（黒髪ボブ・青い目・白いもこもこセーター・緑のスカート・深緑のブーツ、フェルト人形風3D）
季節：晩秋。落ち葉と、どんぐりの木（コナラ・クヌギ）のある公園

---

| p | ナレーション（読み上げ） | 小さい補足文字 | 絵 |
|---|---|---|---|
| いち | おさんぽ、おさんぽ。どんぐり、いっぱい おちてるね。 | | 落ち葉の小道を歩く女の子。足もとにどんぐりがころころ |
| に | ぴかぴかの どんぐり。おうちに もってかえろう！ | | しゃがんで、どんぐりを小さなかごに入れてにっこり |
| さん | つぎの ひ……わっ！ しろい むしが でてきた！ | | 家のテーブル。どんぐりの横に小さな白いイモムシ。女の子はびっくりして一歩引く |
| よん | だいじょうぶ。どんぐりの なかで そだった、ぞうむしの あかちゃんだよ。 | かんだり しないよ。 | 女の子がそっと顔を近づけて見る（さわってはいない） |
| ご | なつに、おかあさん ぞうむしが どんぐりに たまごを うんだの。どんぐりは、むしの おうちでも あるんだね。 | | 絵本風の説明カット：長い口のゾウムシが、緑のどんぐりに口で穴をあけている／どんぐりの断面の中に白い幼虫 |
| ろく | この こは、つちの なかで ふゆを こすんだって。こうえんに かえして あげよう。 | てで さわらずに、はっぱに のせてね。 | 女の子がおかあさんと一緒に、葉っぱにのせた幼虫とどんぐりを公園へ運ぶ |
| なな | つちの うえに、そーっと。もぐもぐ、もぐっていったよ。 | | 木の根もとの土の上に葉っぱごと置く。幼虫が土にもぐっていく。女の子はしゃがんで見守る |
| はち | どんぐりを ひろったら、ちいさな まるい あなが ないか、みてみてね。またね！ | | 女の子が、小さな丸い穴のあいたどんぐりを見せて、笑顔で手をふる |

### 内容のもと（事実）
- どんぐりから出てくる白い幼虫は、主に **シギゾウムシ類**（コナラシギゾウムシなど）の幼虫。
- 夏〜初秋、母ゾウムシが長い口でまだ緑のどんぐりに穴をあけ、卵を産む。幼虫は中身を食べて育つ。
- どんぐりが落ちたあと、幼虫は丸い穴（直径2〜3mmほど）をあけて外に出て、土にもぐって冬をこす。
- かんだり、毒があったりはしない。
- 丸い穴があいているどんぐり ＝ 幼虫がもう出ていったあと。

### 概要欄用「おうちの方へ」（案）
> ひろってきたどんぐりは、なべで数分ゆでるか、袋に入れて冷凍庫で1週間ほど冷やすと、中から虫が出てこなくなります。工作に使う前の下ごしらえにどうぞ。

---

## 絵の生成プロンプト（前回と同じツールで作る場合）
共通：`Same girl as reference: felt / wool doll style 3D chibi girl, black bob hair, big blue eyes, rosy cheeks, cream fluffy sweater, green skirt, dark green boots. Late autumn park with fallen leaves and oak trees, warm soft sunlight, shallow depth of field, picture-book feel. Square 1:1. No text.`

- p1: `the girl walks happily along a path covered with fallen leaves; many shiny brown acorns on the ground`
- p2: `the girl crouches and puts shiny acorns into a small woven basket, smiling`
- p3: `indoors on a wooden table next morning: a few acorns and a tiny plump white grub crawling out of one acorn through a small round hole; the girl leans back, surprised`
- p4: `the girl leans in gently to look at the tiny white grub on the table, curious and calm, hands on her knees (not touching it)`
- p5: `picture-book explanation scene: a cute acorn weevil with a very long thin snout drilling into a green acorn on an oak branch; inset cutaway of an acorn with a small white grub inside`
- p6: `the girl and her mother (only hand and legs visible) walk back to the park; the girl carefully carries a big leaf with the grub and acorn on it`
- p7: `at the foot of an oak tree, the leaf is placed on soft soil; the small white grub is burrowing into the soil; the girl crouches and watches kindly`
- p8: `the girl holds up an acorn with a small round hole toward the viewer and waves goodbye with the other hand, smiling`
