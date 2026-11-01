# SRC Data

SRC向けのデータを眺めたり弄ってみたりするためのリポジトリ。

https://7474.github.io/SRC/ で参照しています。

## GSCデータパック

[GSCデータパック](./GSCデータパック) 配下のデータは[ＳＲＣ総合支援センター](http://www.gsc.ne.jp/)の[データパック](http://www.gsc.ne.jp/materials_data.php)の文字コードを閲覧の便宜上UTF-8に変換したものです。

## Sharp

このリポジトリ管理のデータ・画像。

## tools

リポジトリ内のデータを処理するツール。

## site

GitHub Pages で、データを作品ごとに閲覧し、評価を見るためのページを作る（[`.github/workflows/pages.yml`](.github/workflows/pages.yml)）。

- 作品ごとのページ: パイロット・SP・ユニット・武器・マップ兵器・メッセージの数と、GSC データパックの同じ層の中での位置、ガイドラインの目安から外れているもの（SRC の [`tools/pack-stats`](https://github.com/7474/SRC/tree/master/tools/pack-stats) の `check`・`site`）
- 組の評価: 使いどころごとの評価と指数（実効性能・単純数字）、組ごとのレーダーチャートと総評（SRC の [`tools/pack-analysis`](https://github.com/7474/SRC/tree/master/tools/pack-analysis)）。`Sharp/Data` の作品は GSC データパックの拡張に足して評価する
- [データ作成ガイドライン](docs/データ作成ガイドライン.md)

データ・ガイドライン・`site` が変わったとき、手動、毎週（SRC の評価の更新を取り込む）に作り直す。手元では次で作れる（.NET 10 と、SRC のリポジトリが要る）。

```bash
site/build.sh . ../SRC out
```

