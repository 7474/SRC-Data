#!/usr/bin/env bash
# GitHub Pages のページを作る。
# 使い方: site/build.sh <SRC-Data のフォルダ> <SRC のフォルダ> <出力フォルダ>
# SRC の tools/pack-stats・tools/pack-analysis を使う（.NET 10 が要る）。
# 役割表・格の一覧は analysis/ のものを使う（無ければ SRC の tools/ のもの）。
# 組の評価は、作品の頁のほかに analysis/pairs-<区分>.json にも出す（データビューアの「比べる」が読む）。
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
# 役割表・格の一覧（SRC-Data の analysis/ を優先する）
input() {
  if [ -f "$DATA/analysis/$1" ]; then echo "$DATA/analysis/$1"; else echo "$TOOLS/$2/$1"; fi
}
ROLES_EXT=$(input roles-ext.csv pack-analysis)
ROLES_ROBO=$(input roles-robo.csv pack-analysis)
TIERS_EXT=$(input tiers-ext.tsv pack-stats)
TIERS_ROBO=$(input tiers-robo.tsv pack-stats)
mkdir -p "$OUT/analysis"

# 組の評価（全ての作品。レーダーチャートと総評つき）。作品ごとのページに載せる。
# Sharp/Data の作品は拡張のパックに足して評価する。ファイル名（拡張・ロボ・Sharp）は site の区分の名前に合わせる
WORK=$(mktemp -d)
ls "$G/拡張" > "$WORK/works-ext.txt"
ls "$G/ロボ" > "$WORK/works-robo.txt"
ls "$DATA/Sharp/Data" > "$WORK/works-sharp.txt"
mkdir -p "$WORK/combined"
cp -r "$G/拡張/." "$WORK/combined/"
cp -r "$DATA/Sharp/Data/." "$WORK/combined/"
dotnet "$PA" "$G/拡張" 拡張 "$ROLES_EXT" "$WORK/works-ext.txt" --tiers "$TIERS_EXT" --cards 1 --json "$OUT/analysis/pairs-拡張.json" > "$WORK/拡張.md" 2> "$WORK/拡張.err" &
dotnet "$PA" "$G/ロボ" ロボ "$ROLES_ROBO" "$WORK/works-robo.txt" --tiers "$TIERS_ROBO" --cards 1 --json "$OUT/analysis/pairs-ロボ.json" > "$WORK/ロボ.md" 2> "$WORK/ロボ.err" &
dotnet "$PA" "$WORK/combined" 拡張 "$ROLES_EXT" "$WORK/works-sharp.txt" --cards 1 --json "$OUT/analysis/pairs-Sharp.json" > "$WORK/Sharp.md" 2> "$WORK/Sharp.err" &
wait
# 組の評価の JSON の一覧（データビューアの「比べる」が最初に読む）。区分の名前とファイル
{
  printf '{"format":1,"generatedAt":"%s","files":[' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  sep=""
  for n in ロボ 拡張 Sharp; do
    if [ -s "$OUT/analysis/pairs-$n.json" ]; then
      printf '%s{"section":"%s","file":"pairs-%s.json"}' "$sep" "$n" "$n"
      sep=","
    fi
  done
  printf ']}\n'
} > "$OUT/analysis/index.json"
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
