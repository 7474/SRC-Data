#!/usr/bin/env bash
# GitHub Pages のページを作る。
# 使い方: site/build.sh <SRC-Data のフォルダ> <SRC のフォルダ> <出力フォルダ>
# SRC の tools/pack-stats・tools/pack-analysis を使う（.NET 10 が要る）。
set -euo pipefail
DATA=$(cd "$1" && pwd)
SRC=$(cd "$2" && pwd)
OUT=$3
mkdir -p "$OUT"
OUT=$(cd "$OUT" && pwd)

dotnet build "$SRC/tools/pack-stats" -c Release -v q
dotnet build "$SRC/tools/pack-analysis" -c Release -v q
PS="$SRC/tools/pack-stats/bin/Release/net10.0/PackStats.dll"
PA="$SRC/tools/pack-analysis/bin/Release/net10.0/PackAnalysis.dll"
G="$DATA/GSCデータパック"
TOOLS="$SRC/tools"

# 組の評価（全ての作品。レーダーチャートと総評つき）。作品ごとのページに載せる。
# Sharp/Data の作品は拡張のパックに足して評価する。ファイル名（拡張・ロボ・Sharp）は site の区分の名前に合わせる
WORK=$(mktemp -d)
ls "$G/拡張" > "$WORK/works-ext.txt"
ls "$G/ロボ" > "$WORK/works-robo.txt"
ls "$DATA/Sharp/Data" > "$WORK/works-sharp.txt"
mkdir -p "$WORK/combined"
cp -r "$G/拡張/." "$WORK/combined/"
cp -r "$DATA/Sharp/Data/." "$WORK/combined/"
dotnet "$PA" "$G/拡張" 拡張 "$TOOLS/pack-analysis/roles-ext.csv" "$WORK/works-ext.txt" --tiers "$TOOLS/pack-stats/tiers-ext.tsv" --cards 1 > "$WORK/拡張.md" 2> "$WORK/拡張.err" &
dotnet "$PA" "$G/ロボ" ロボ "$TOOLS/pack-analysis/roles-robo.csv" "$WORK/works-robo.txt" --tiers "$TOOLS/pack-stats/tiers-robo.tsv" --cards 1 > "$WORK/ロボ.md" 2> "$WORK/ロボ.err" &
dotnet "$PA" "$WORK/combined" 拡張 "$TOOLS/pack-analysis/roles-ext.csv" "$WORK/works-sharp.txt" --cards 1 > "$WORK/Sharp.md" 2> "$WORK/Sharp.err" &
wait
for n in 拡張 ロボ Sharp; do
  grep -c '^評価できない' "$WORK/$n.err" | sed "s/^/$n: 評価できない組 /" >&2 || true
done

# データ作成ガイドライン
{
  printf -- '---\ntitle: "データ作成ガイドライン"\nnav_order: 2\nsearch_terms: "データ作成ガイドライン ガイドライン"\n---\n\n{%% raw %%}\n'
  sed 's/{% endraw %}/{ % endraw % }/g' "$DATA/docs/データ作成ガイドライン.md" | sed '1{/^# /d}'
  printf '\n{%% endraw %%}\n'
} > "$OUT/guideline.md"

# 作品ごとのデータと評価（組の評価を含む）、組の評価の前提と格ごとの指数、トップページ
dotnet "$PS" site "$OUT" "$G" "$DATA/Sharp/Data" --analysis "$WORK/拡張.md" "$WORK/ロボ.md" "$WORK/Sharp.md" 2> >(grep -v '^読み込めない' >&2)

# Jekyll の設定・テーマの上書き
cp -r "$DATA/site/_config.yml" "$DATA/site/_includes" "$DATA/site/_sass" "$DATA/site/assets" "$OUT/"
rm -rf "$WORK"
