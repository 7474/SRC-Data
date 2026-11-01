アーマード・コアⅥ（ARMORED CORE VI FIRES OF RUBICON）

フロム・ソフトウェア、2023年8月25日発売（PS5・PS4・Xbox Series X|S・Xbox One・PC）。
惑星ルビコン３を舞台に、強化人間 C4-621（独立傭兵「レイヴン」）が企業・解放戦線・傭兵たちの争いに関わる。

■ ファイル
- pilot.txt          パイロット 42 人（名前付き 32 人（ボスとしての姿 2 人を含む）、サポート 2 人、ザコ 5 人、汎用 3 人）
- robot.txt          ユニット 48 機（AC 32 機、ボス 10 機、MT・LC・HC 6 機）
- pilot_message.txt  メッセージ
- alias.txt          アサルトブースト(ＡＣ６)

■ 作り方
docs/データ作成ガイドライン.md に沿い、GSC データパックのロボを基準にした。
- 主人公の Ｃ４－６２１ は作中で喋らないため、メッセージは「……」だけにしている
  （アーマード・コアラストレイヴンのレイヴン(ＬＲ)と同じ）。
- ハンドラー＝ウォルター・エア(ＡＣ６) は 621 のサポートパイロット。
  終盤のボスとしての姿は ハンドラー＝ウォルター(ＨＡＬ８２６)・エア(ＳＯＬ６４４) として別に用意した。
- 原作の仕組みは次のように表した。
  - アサルトブースト: アビリティで１ターンの間、運動性+15・移動力+1（アーマード・コアフォーアンサーのオーバードブーストと同じ作り）
  - アサルトアーマー: 射程１の全方位のマップ兵器（Ｍ全）
  - パルスアーマー・パルスプロテクション: １回だけ使えるバリアを付加するアビリティ
  - ターミナルアーマー: ペイターの SP「ド根性」
  - ACS 負荷とスタッガー: スタン系の武器の「痺」、621 の SP「直撃」
  - リペアキット: 621 の機体だけに付けた回復のアビリティ（３回）
  - 強化人間: 特殊能力「サイボーグ=強化人間」
- 名前が GSC データパックの既存のデータと重なるもの（ラスティ・ナイル・レッド・キング・エア）は「(ＡＣ６)」を付けた。
  機体は「ＡＣ<機体名>」とした。
- 画像は「AMC6_」で始まる名前にした（画像そのものは含まない）。

■ 出典
- 公式サイト https://www.armoredcore.net/
- 公式オンラインマニュアル https://www.fromsoftware.jp/manual/armoredcore6/ps5/action.html
- Wikipedia https://ja.wikipedia.org/wiki/ARMORED_CORE_VI_FIRES_OF_RUBICON
- 神ゲー攻略 https://kamigame.jp/armoredcore6/
- Game8 https://game8.jp/armoredcore6/
- Fextralife Wiki https://armoredcore6.wiki.fextralife.com/
- 台詞: GameSpark https://www.gamespark.jp/article/2023/09/18/134158.html 、AUTOMATON https://automaton-media.com/articles/newsjp/20230829-261960/

原作の台詞は短いものだけを使い、ほかのメッセージは人物の口調に合わせて書いた。
