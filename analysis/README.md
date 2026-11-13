# 組の評価の入力（役割表・格の一覧）

GitHub Pages の組の評価（SRC の `tools/pack-analysis`）と、データビューアの「比べる」が使う。データを見ながら、ここで直す。

| ファイル | 内容 |
|---|---|
| `roles-robo.csv`・`roles-ext.csv` | 役割表。誰がどのユニットに乗るか、役割・格。書いた組は、名前の一致などで自動で組んだ組より優先される |
| `tiers-robo.tsv`・`tiers-ext.tsv` | 格の一覧。格の目安のはっきりしたキャラ（主人公格・準主役格・サブキャラ格など）と、乗るユニット |

書式は SRC の [tools/pack-analysis の README](https://github.com/7474/SRC/blob/master/tools/pack-analysis/README.md) の「役割表」と、[tools/pack-stats の README](https://github.com/7474/SRC/blob/master/tools/pack-stats/README.md) の「格の一覧」にある。

## 役割表を足す

1. 作品の、自動で組んだ組を役割表の形で出す（SRC のリポジトリが要る）。

   ```bash
   dotnet ../SRC/tools/pack-analysis/bin/Release/net10.0/PackAnalysis.dll GSCデータパック/ロボ ロボ analysis/roles-robo.csv - --roles-template 機動戦士ガンダム
   ```

2. 出た行のうち要るものを `roles-robo.csv`（拡張は `roles-ext.csv`）に足し、格（主人公格・準主役格・サブキャラ格・端役格・名前なし）を埋める。乗るユニットが違えば直す。
3. push すると、名前（パイロット・ユニット）がデータにあるかを CI（`Validate Analysis`）が確かめ、Pages が作り直される。

どの作品に役割表が無いかは、データビューアの「比べる」の「作品」で分かる（`declared` が 0 の作品）。
