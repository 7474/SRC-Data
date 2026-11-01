#!/usr/bin/env bash
# GitHub Pages のページを作る。
# 使い方: site/build.sh <SRC-Data のフォルダ> <SRC のフォルダ> <出力フォルダ>
# SRC の tools/pack-stats・tools/pack-analysis を使う（.NET 10 が要る）。
set -euo pipefail
DATA=$(cd "$1" && pwd)
SRC=$(cd "$2" && pwd)
OUT=$3
mkdir -p "$OUT/evaluation"
OUT=$(cd "$OUT" && pwd)

dotnet build "$SRC/tools/pack-stats" -c Release -v q
dotnet build "$SRC/tools/pack-analysis" -c Release -v q
PS="$SRC/tools/pack-stats/bin/Release/net10.0/PackStats.dll"
PA="$SRC/tools/pack-analysis/bin/Release/net10.0/PackAnalysis.dll"
G="$DATA/GSCデータパック"

# Jekyll のページにする（front matter を付け、Liquid の記法に見える文字列をそのまま出す）
page() {
  local title=$1 src=$2 dst=$3
  {
    printf -- '---\ntitle: "%s"\n---\n\n[トップ](%s)\n\n{%% raw %%}\n' "$title" "$4"
    sed 's/{% endraw %}/{ % endraw % }/g' "$src"
    printf '\n{%% endraw %%}\n'
  } > "$dst"
}

# 組の評価（レーダーチャートと総評つき）。Sharp/Data の作品は拡張のパックに足して評価する
WORK=$(mktemp -d)
ls "$DATA/Sharp/Data" > "$WORK/works-sharp.txt"
mkdir -p "$WORK/combined"
cp -r "$G/拡張/." "$WORK/combined/"
cp -r "$DATA/Sharp/Data/." "$WORK/combined/"
dotnet "$PA" "$G/拡張" 拡張 "$SRC/tools/pack-analysis/roles-ext.csv" "$SRC/tools/pack-analysis/works-ext.txt" --tiers "$SRC/tools/pack-stats/tiers-ext.tsv" --cards 1 > "$WORK/拡張.md" 2> "$WORK/拡張.err" &
dotnet "$PA" "$G/ロボ" ロボ "$SRC/tools/pack-analysis/roles-robo.csv" "$SRC/tools/pack-analysis/works-robo.txt" --tiers "$SRC/tools/pack-stats/tiers-robo.tsv" --cards 1 > "$WORK/ロボ.md" 2> "$WORK/ロボ.err" &
dotnet "$PA" "$WORK/combined" 拡張 "$SRC/tools/pack-analysis/roles-ext.csv" "$WORK/works-sharp.txt" --cards 1 > "$WORK/Sharp.md" 2> "$WORK/Sharp.err" &
wait
for n in 拡張 ロボ Sharp; do
  page "組の評価: $n" "$WORK/$n.md" "$OUT/evaluation/$n.md" "../"
  tail -n 3 "$WORK/$n.err" >&2 || true
done

# データ作成ガイドライン
page "データ作成ガイドライン" "$DATA/docs/データ作成ガイドライン.md" "$OUT/guideline.md" "./"

# 作品ごとのデータと評価、トップページ
dotnet "$PS" site "$OUT" "$G" "$DATA/Sharp/Data" 2> >(grep -v '^読み込めない' >&2)

# Jekyll の設定
cp -r "$DATA/site/_config.yml" "$DATA/site/_includes" "$OUT/"
rm -rf "$WORK"
