#!/usr/bin/env python3
"""かんたん作成（7474/SRC の SRC#Studio。docs/tools/quick-create.md）の場面のカタログ（index.json）とマップ（maps/*.map）を作る。

マップは SRC# の最小の汎用データ（basic-data）の地形だけを使い、どのサイトの SRC#Web でも出せるようにする。
作品の場面のユニット・パイロットの名前は GSC データパック（このリポジトリの index.json の作品）のもの。セリフはこのカタログのために書いた。
使い方: python3 scenes/make.py   （scenes/index.json と scenes/maps/ を書き直す）
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))

# basic-data の地形の番号（SRC.Sharp/Content/basic-data/Data/System/terrain.txt）
PLAIN, ROAD, WASTE, WOODS, MOUNTAIN, SEA, RIVER, TOWN, BUILDING, BRIDGE = 0, 2, 10, 11, 15, 17, 19, 21, 22, 25
ROCK, HILL, BUSH, BASE, RUINS, CASTLE, POWER, REMAINS = 29, 31, 32, 33, 42, 47, 48, 49


class Map:
    def __init__(self, w, h, fill=PLAIN):
        self.w, self.h = w, h
        self.t = [[fill] * w for _ in range(h)]

    def set(self, x, y, terrain):
        if 1 <= x <= self.w and 1 <= y <= self.h:
            self.t[y - 1][x - 1] = terrain

    def rect(self, x1, y1, x2, y2, terrain):
        for y in range(y1, y2 + 1):
            for x in range(x1, x2 + 1):
                self.set(x, y, terrain)

    def cells(self, cells, terrain):
        for x, y in cells:
            self.set(x, y, terrain)

    def path(self, points, terrain, bridge_over=None):
        """点を順に縦・横に結ぶ（道・川）。bridge_over の地形の上は橋にする"""
        for (x1, y1), (x2, y2) in zip(points, points[1:]):
            x, y = x1, y1
            while True:
                if bridge_over is not None and self.t[y - 1][x - 1] in bridge_over:
                    self.set(x, y, BRIDGE)
                else:
                    self.set(x, y, terrain)
                if (x, y) == (x2, y2):
                    break
                if x != x2:
                    x += 1 if x2 > x else -1
                else:
                    y += 1 if y2 > y else -1

    def text(self):
        # SRCAuthoring の MapDocument と同じ書き方: 1 行目 MapData、空行、幅,高さ、列（x）ごとに上から地形,画像
        lines = ['MapData', '', f'{self.w},{self.h}']
        for x in range(self.w):
            for y in range(self.h):
                lines.append(f'{self.t[y][x]},0')
        return '\r\n'.join(lines) + '\r\n'


def scene_jaburo():
    m = Map(22, 16, WOODS)
    m.path([(6, 1), (6, 5), (3, 5), (3, 10), (1, 10)], RIVER)
    m.path([(15, 1), (15, 4), (19, 4), (19, 8), (22, 8)], RIVER)
    m.rect(9, 12, 14, 16, BASE)
    m.cells([(8, 13), (15, 13), (8, 14), (15, 14)], BASE)
    m.path([(11, 12), (11, 7), (6, 7)], ROAD, bridge_over={RIVER})
    m.cells([(1, 1), (2, 1), (1, 2), (22, 1), (21, 1), (22, 2), (1, 16), (2, 16), (22, 16), (21, 16), (17, 12), (18, 12), (17, 13)], ROCK)
    m.rect(8, 9, 9, 10, BUSH)
    return m, {
        'id': 'gundam-jaburo',
        'title': 'ジャブロー攻防戦',
        'description': '密林の地下基地に、川から水陸両用のモビルスーツが迫る（機動戦士ガンダム）',
        'tags': ['機動戦士ガンダム', '密林', '基地防衛'],
        'allies': [{'x': 11, 'y': 11}, {'x': 10, 'y': 12}, {'x': 13, 'y': 12}, {'x': 12, 'y': 13}],
        'enemies': [{'x': 6, 'y': 3}, {'x': 15, 'y': 2}, {'x': 3, 'y': 7}, {'x': 19, 'y': 6}, {'x': 6, 'y': 1}],
        'titles': ['GSCデータパック/ロボ/機動戦士ガンダム'],
        'units': {
            'allies': [
                {'unit': 'ガンダム', 'pilot': 'アムロ＝レイ(0079)', 'level': 22, 'x': 11, 'y': 11},
                {'unit': 'ガンキャノン', 'pilot': 'カイ＝シデン', 'level': 18, 'x': 10, 'y': 12},
                {'unit': 'ジム', 'pilot': '連邦軍兵士(ザコ)', 'level': 12, 'x': 13, 'y': 12},
            ],
            'enemies': [
                {'unit': 'ズゴック(シャア専用)', 'pilot': 'シャア＝アズナブル', 'level': 20, 'x': 6, 'y': 3},
                {'unit': 'ゴッグ', 'pilot': 'ジオン兵(ザコ)', 'level': 10, 'x': 15, 'y': 2},
                {'unit': 'アッガイ', 'pilot': 'ジオン兵(ザコ)', 'level': 10, 'x': 3, 'y': 7},
                {'unit': 'ズゴック', 'pilot': 'ジオンベテラン兵(ザコ)', 'level': 12, 'x': 19, 'y': 6},
            ],
        },
        'talk': {
            'opening': [
                {'speaker': '', 'text': '南米、密林の奥。地下に築かれた連邦軍の本部に、川をさかのぼってジオンの部隊が忍び寄る。'},
                {'speaker': 'シャア＝アズナブル', 'text': '入口さえ見つければこちらのものだ。各機、散開して探せ。'},
                {'speaker': 'アムロ＝レイ(0079)', 'text': '赤い機体……やっぱりあの人か。ここは通さない！'},
            ],
            'victory': [
                {'speaker': 'アムロ＝レイ(0079)', 'text': '基地は守りきった。……でも、あの人はまた来る。'},
            ],
            'defeat': [
                {'speaker': 'シャア＝アズナブル', 'text': '連邦の本部、いただいたぞ。'},
            ],
        },
    }


def scene_photon():
    m = Map(20, 16, PLAIN)
    m.rect(17, 1, 20, 16, SEA)
    m.cells([(16, 1), (16, 2), (16, 7), (16, 8), (16, 9), (16, 14), (16, 15), (16, 16)], SEA)
    m.rect(1, 1, 9, 3, MOUNTAIN)
    m.cells([(10, 1), (11, 1), (10, 2), (1, 4), (2, 4), (1, 5)], MOUNTAIN)
    m.rect(4, 6, 9, 10, HILL)
    m.rect(5, 7, 8, 9, BASE)
    m.cells([(6, 8), (7, 8)], POWER)
    m.rect(1, 12, 5, 16, TOWN)
    m.path([(8, 10), (8, 13), (14, 13), (14, 16)], ROAD)
    m.path([(6, 13), (6, 16)], ROAD)
    m.rect(12, 5, 14, 7, WOODS)
    m.cells([(15, 3), (15, 4), (15, 11), (15, 12)], WASTE)
    return m, {
        'id': 'mazinger-photon-lab',
        'title': '光子力研究所防衛戦',
        'description': '山あいの研究所に、海から機械獣が上陸してくる（マジンガーＺ）',
        'tags': ['マジンガーＺ', '海岸', '基地防衛'],
        'allies': [{'x': 9, 'y': 8}, {'x': 9, 'y': 9}, {'x': 8, 'y': 11}, {'x': 10, 'y': 10}],
        'enemies': [{'x': 17, 'y': 6}, {'x': 18, 'y': 9}, {'x': 17, 'y': 12}, {'x': 19, 'y': 4}, {'x': 19, 'y': 14}],
        'titles': ['GSCデータパック/ロボ/マジンガーＺ'],
        'units': {
            'allies': [
                {'unit': 'マジンガーＺ', 'pilot': '兜甲児', 'level': 20, 'x': 9, 'y': 8},
                {'unit': 'アフロダイＡ', 'pilot': '弓さやか', 'level': 16, 'x': 9, 'y': 9},
                {'unit': 'ボスボロット', 'pilot': 'ボス(マジンガーＺ)', 'level': 14, 'x': 8, 'y': 11},
            ],
            'enemies': [
                {'unit': '機械獣ガラダＫ７', 'pilot': '機械獣用ＡＩ(ザコ)', 'level': 10, 'x': 17, 'y': 6},
                {'unit': '機械獣ダブラスＭ２', 'pilot': '機械獣用ＡＩ(ザコ)', 'level': 10, 'x': 18, 'y': 9},
                {'unit': '機械獣グロマセンＲ９', 'pilot': '機械獣用ＡＩ(ザコ)', 'level': 10, 'x': 17, 'y': 12},
            ],
        },
        'talk': {
            'opening': [
                {'speaker': '', 'text': '富士の山すそに立つ光子力研究所。その沖合から、巨大な影が姿を現した。'},
                {'speaker': '弓さやか', 'text': '甲児くん、機械獣よ！ 三体も上がってくるわ！'},
                {'speaker': '兜甲児', 'text': '何体来ようが同じだ。マジンガーＺの力、見せてやるぜ！'},
            ],
            'victory': [
                {'speaker': '兜甲児', 'text': 'へへっ、研究所には指一本触れさせないぜ！'},
            ],
            'defeat': [
                {'speaker': '弓さやか', 'text': 'このままじゃ研究所が……！'},
            ],
        },
    }


def scene_tokyo3():
    m = Map(22, 16, PLAIN)
    for y in range(1, 17):
        for x in range(1, 23):
            if x <= 2 or y <= 1 or x >= 21:
                m.set(x, y, MOUNTAIN)
    m.rect(1, 5, 4, 12, SEA)
    m.rect(7, 4, 16, 11, BUILDING)
    for x in (9, 12, 15):
        m.path([(x, 3), (x, 12)], ROAD)
    for y in (6, 9):
        m.path([(5, y), (18, y)], ROAD)
    m.rect(7, 12, 16, 13, TOWN)
    m.rect(16, 13, 20, 16, HILL)
    m.cells([(18, 14), (19, 15)], MOUNTAIN)
    m.rect(5, 14, 12, 16, WOODS)
    return m, {
        'id': 'eva-tokyo3',
        'title': '第３新東京市迎撃戦',
        'description': '山に囲まれた要塞都市に、最初の使徒が現れる（新世紀エヴァンゲリオン）',
        'tags': ['新世紀エヴァンゲリオン', '市街地', '迎撃'],
        'allies': [{'x': 18, 'y': 14}, {'x': 17, 'y': 13}, {'x': 16, 'y': 14}],
        'enemies': [{'x': 11, 'y': 7}, {'x': 8, 'y': 5}, {'x': 14, 'y': 10}],
        'titles': ['GSCデータパック/ロボ/新世紀エヴァンゲリオン'],
        'units': {
            'allies': [
                {'unit': 'エヴァ初号機', 'pilot': '碇シンジ', 'level': 24, 'x': 17, 'y': 14},
                {'unit': 'エヴァ零号機', 'pilot': '綾波レイ', 'level': 24, 'x': 16, 'y': 13},
            ],
            'enemies': [
                {'unit': '第３使徒サキエル', 'pilot': '第３使徒サキエル', 'level': 10, 'x': 11, 'y': 7},
            ],
        },
        'talk': {
            'opening': [
                {'speaker': '', 'text': '山に囲まれた要塞都市、第３新東京市。ビルの谷間を、巨大な影がゆっくりと歩いてくる。'},
                {'speaker': '綾波レイ', 'text': '使徒、確認。……碇くん、行ける？'},
                {'speaker': '碇シンジ', 'text': '逃げちゃだめだ……。わかった、やってみるよ。'},
            ],
            'victory': [
                {'speaker': '碇シンジ', 'text': '……終わった、のかな。'},
            ],
            'defeat': [
                {'speaker': '碇シンジ', 'text': 'だめだ……届かない……！'},
            ],
        },
    }


def scene_saotome():
    m = Map(20, 15, WOODS)
    m.rect(1, 1, 20, 3, MOUNTAIN)
    m.rect(1, 1, 3, 15, MOUNTAIN)
    m.cells([(4, 4), (5, 4), (4, 5), (19, 4), (20, 4), (20, 5)], MOUNTAIN)
    m.rect(7, 8, 12, 12, BASE)
    m.rect(6, 7, 13, 7, PLAIN)
    m.rect(6, 13, 13, 13, PLAIN)
    m.path([(10, 13), (10, 15)], ROAD)
    m.path([(16, 4), (16, 15)], RIVER)
    m.cells([(17, 10), (18, 11), (14, 5), (14, 14)], ROCK)
    return m, {
        'id': 'getter-saotome-lab',
        'title': '早乙女研究所',
        'description': '山奥の研究所に、地底から恐竜帝国のメカザウルスが襲いかかる（ゲッターロボ）',
        'tags': ['ゲッターロボ', '山岳', '基地防衛'],
        'allies': [{'x': 9, 'y': 9}, {'x': 11, 'y': 10}, {'x': 10, 'y': 12}],
        'enemies': [{'x': 18, 'y': 7}, {'x': 18, 'y': 13}, {'x': 13, 'y': 4}, {'x': 6, 'y': 14}],
        'titles': ['GSCデータパック/ロボ/ゲッターロボ'],
        'units': {
            'allies': [
                {'unit': 'ゲッター１', 'pilot': '流竜馬', 'level': 22, 'x': 9, 'y': 9},
            ],
            'enemies': [
                {'unit': 'メカザウルス・サキ', 'pilot': '恐竜兵(ザコ)', 'level': 8, 'x': 18, 'y': 7},
                {'unit': 'メカザウルス・バド', 'pilot': '恐竜兵(ザコ)', 'level': 8, 'x': 18, 'y': 13},
            ],
        },
        'talk': {
            'opening': [
                {'speaker': '', 'text': '山奥の早乙女研究所。地鳴りとともに、地の底から鋼の恐竜が這い出してきた。'},
                {'speaker': '流竜馬', 'text': '恐竜帝国め、性懲りもなく来やがったな。ゲッターの力で叩き返してやる！'},
            ],
            'victory': [
                {'speaker': '流竜馬', 'text': '研究所は無事か。……まだ終わりじゃなさそうだな。'},
            ],
            'defeat': [
                {'speaker': '流竜馬', 'text': 'くそっ、研究所が……！'},
            ],
        },
    }


def scene_udo():
    m = Map(20, 15, WASTE)
    m.rect(5, 4, 15, 11, REMAINS)
    m.rect(7, 6, 13, 9, TOWN)
    m.path([(1, 8), (20, 8)], ROAD)
    m.path([(10, 1), (10, 15)], ROAD)
    m.cells([(3, 3), (4, 12), (17, 3), (18, 12), (16, 13), (2, 14)], ROCK)
    m.rect(16, 5, 18, 7, RUINS)
    return m, {
        'id': 'votoms-udo',
        'title': 'ウドの街',
        'description': '戦争の残骸が集まる荒んだ街で、ＡＴ同士がぶつかる（装甲騎兵ボトムズ）',
        'tags': ['装甲騎兵ボトムズ', '廃墟', '小規模'],
        'allies': [{'x': 3, 'y': 8}, {'x': 2, 'y': 7}],
        'enemies': [{'x': 12, 'y': 7}, {'x': 15, 'y': 9}, {'x': 10, 'y': 4}, {'x': 17, 'y': 6}],
        'titles': ['GSCデータパック/ロボ/装甲騎兵ボトムズ'],
        'units': {
            'allies': [
                {'unit': 'スコープドッグ', 'pilot': 'キリコ＝キュービィー', 'level': 22, 'x': 3, 'y': 8},
            ],
            'enemies': [
                {'unit': 'スコープドッグ', 'pilot': 'ボトムズ乗り(ザコ)', 'level': 8, 'x': 12, 'y': 7},
                {'unit': 'スコープドッグ', 'pilot': 'ボトムズ乗り(ザコ)', 'level': 8, 'x': 15, 'y': 9},
                {'unit': 'スコープドッグ', 'pilot': 'ベテランボトムズ乗り(ザコ)', 'level': 10, 'x': 10, 'y': 4},
            ],
        },
        'talk': {
            'opening': [
                {'speaker': '', 'text': '戦争の吐き出したものが流れ着く街、ウド。油と鉄の匂いの中で、ＡＴのローラーが砂を噛む。'},
                {'speaker': 'キリコ＝キュービィー', 'text': '……囲まれたか。やるしかない。'},
            ],
            'victory': [
                {'speaker': 'キリコ＝キュービィー', 'text': '……。'},
            ],
            'defeat': [],
        },
    }


def scene_ataria():
    m = Map(22, 16, SEA)
    m.rect(5, 4, 17, 13, PLAIN)
    m.cells([(4, 6), (4, 7), (4, 8), (18, 7), (18, 8), (18, 9), (8, 3), (9, 3), (13, 14), (14, 14)], PLAIN)
    m.rect(6, 5, 9, 7, TOWN)
    m.rect(12, 5, 15, 7, BASE)
    m.path([(6, 10), (16, 10)], ROAD)
    m.rect(6, 11, 9, 12, WOODS)
    m.cells([(16, 12), (17, 12), (17, 11)], WOODS)
    m.cells([(11, 8), (11, 9)], HILL)
    return m, {
        'id': 'macross-south-ataria',
        'title': '南アタリア島',
        'description': '巨大な艦の眠る南の島に、海からゼントラーディのリガードが上陸してくる（超時空要塞マクロス）',
        'tags': ['超時空要塞マクロス', '島', '海岸'],
        'allies': [{'x': 12, 'y': 8}, {'x': 13, 'y': 9}, {'x': 10, 'y': 9}],
        'enemies': [{'x': 19, 'y': 5}, {'x': 20, 'y': 9}, {'x': 19, 'y': 13}, {'x': 3, 'y': 11}],
        'titles': ['GSCデータパック/ロボ/超時空要塞マクロス'],
        'units': {
            'allies': [
                {'unit': 'ＶＦ－１Ｓバトロイド(ＲＦＳ)', 'pilot': 'ロイ＝フォッカー', 'level': 22, 'x': 12, 'y': 8},
                {'unit': 'ＶＦ－１Ｊバトロイド(輝)', 'pilot': '一条輝', 'level': 14, 'x': 13, 'y': 9},
            ],
            'enemies': [
                {'unit': 'リガード', 'pilot': 'ゼントラーディ兵(ザコ)', 'level': 8, 'x': 19, 'y': 5},
                {'unit': 'リガード', 'pilot': 'ゼントラーディ兵(ザコ)', 'level': 8, 'x': 20, 'y': 9},
                {'unit': 'リガード', 'pilot': 'ゼントラーディ兵(ザコ)', 'level': 8, 'x': 19, 'y': 13},
            ],
        },
        'talk': {
            'opening': [
                {'speaker': '', 'text': '南太平洋の島。進宙式の祝いの日に、空と海から異星の兵が降りてきた。'},
                {'speaker': 'ロイ＝フォッカー', 'text': '輝、ぼさっとするな！ 変形の仕方は体で覚えろ！'},
                {'speaker': '一条輝', 'text': 'わ、わかってますよ、先輩！'},
            ],
            'victory': [
                {'speaker': 'ロイ＝フォッカー', 'text': 'なかなかやるじゃないか、輝。'},
            ],
            'defeat': [],
        },
    }


def generic_wasteland():
    m = Map(20, 15, WASTE)
    m.cells([(4, 3), (5, 3), (4, 4), (9, 7), (10, 7), (15, 4), (16, 11), (6, 12), (13, 13)], ROCK)
    m.rect(8, 10, 11, 11, HILL)
    m.cells([(2, 9), (3, 9), (18, 2), (17, 6)], BUSH)
    return m, {
        'id': 'generic-wasteland', 'title': '荒野', 'description': '岩の点在する荒れ地（20×15。どの作品でも）',
        'tags': ['汎用', '荒野'],
        'allies': [{'x': 3, 'y': 7}, {'x': 3, 'y': 8}, {'x': 2, 'y': 6}, {'x': 2, 'y': 9}],
        'enemies': [{'x': 17, 'y': 7}, {'x': 18, 'y': 8}, {'x': 18, 'y': 6}, {'x': 19, 'y': 9}],
    }


def generic_coast():
    m = Map(20, 15, PLAIN)
    m.rect(14, 1, 20, 15, SEA)
    m.cells([(13, 1), (13, 2), (13, 8), (13, 9), (13, 15)], SEA)
    m.rect(3, 3, 6, 6, WOODS)
    m.rect(2, 11, 5, 14, TOWN)
    m.path([(1, 8), (12, 8)], ROAD)
    m.cells([(12, 4), (12, 12)], ROCK)
    return m, {
        'id': 'generic-coast', 'title': '海岸', 'description': '海から敵が上陸してくる海岸線（20×15。どの作品でも）',
        'tags': ['汎用', '海岸'],
        'allies': [{'x': 7, 'y': 8}, {'x': 6, 'y': 9}, {'x': 6, 'y': 7}, {'x': 5, 'y': 8}],
        'enemies': [{'x': 16, 'y': 5}, {'x': 17, 'y': 8}, {'x': 16, 'y': 11}, {'x': 18, 'y': 3}],
    }


def generic_city():
    m = Map(20, 15, TOWN)
    m.rect(7, 4, 13, 10, BUILDING)
    for x in (4, 10, 16):
        m.path([(x, 1), (x, 15)], ROAD)
    for y in (3, 8, 13):
        m.path([(1, y), (20, y)], ROAD)
    m.rect(1, 14, 3, 15, WOODS)
    return m, {
        'id': 'generic-city', 'title': '市街地', 'description': 'ビル街を挟んで向かい合う（20×15。どの作品でも）',
        'tags': ['汎用', '市街地'],
        'allies': [{'x': 2, 'y': 8}, {'x': 3, 'y': 7}, {'x': 3, 'y': 9}, {'x': 1, 'y': 8}],
        'enemies': [{'x': 19, 'y': 8}, {'x': 18, 'y': 7}, {'x': 18, 'y': 9}, {'x': 20, 'y': 8}],
    }


def generic_mountain():
    m = Map(20, 15, PLAIN)
    m.rect(8, 1, 12, 5, MOUNTAIN)
    m.rect(8, 10, 12, 15, MOUNTAIN)
    m.rect(9, 6, 11, 9, HILL)
    m.path([(1, 7), (20, 7)], ROAD)
    m.rect(2, 2, 5, 4, WOODS)
    m.rect(15, 11, 18, 13, WOODS)
    m.path([(5, 9), (5, 15)], RIVER)
    return m, {
        'id': 'generic-mountain-pass', 'title': '山あいの峠', 'description': '山にはさまれた峠道を奪い合う（20×15。どの作品でも）',
        'tags': ['汎用', '山岳'],
        'allies': [{'x': 3, 'y': 7}, {'x': 2, 'y': 8}, {'x': 2, 'y': 6}, {'x': 4, 'y': 8}],
        'enemies': [{'x': 18, 'y': 7}, {'x': 19, 'y': 6}, {'x': 19, 'y': 8}, {'x': 17, 'y': 8}],
    }


SCENES = [scene_jaburo, scene_photon, scene_tokyo3, scene_saotome, scene_udo, scene_ataria,
          generic_wasteland, generic_coast, generic_city, generic_mountain]


def main():
    os.makedirs(os.path.join(HERE, 'maps'), exist_ok=True)
    scenes = []
    for make in SCENES:
        m, scene = make()
        name = f"maps/{scene['id']}.map"
        with open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='') as f:
            f.write(m.text())
        scene['map'] = name
        scenes.append(scene)
    with open(os.path.join(HERE, 'index.json'), 'w', encoding='utf-8', newline='\n') as f:
        json.dump({'scenes': scenes}, f, ensure_ascii=False, indent=2)
        f.write('\n')


if __name__ == '__main__':
    main()
