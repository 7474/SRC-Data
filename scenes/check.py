#!/usr/bin/env python3
"""場面のカタログ（scenes/index.json）を確かめる（.github/workflows/validate-scenes.yml）。

- make.py で作り直しても変わらない（カタログとマップは make.py から作る）
- マップの大きさと行の数が合い、地形は SRC# の最小の汎用データ（basic-data）にあるもの。置く位置はマップの中
- titles は index.json の作品の path。units のユニット・パイロットはその作品（と同じデータパックの System）のデータにある。
- units の rank は 0〜20、bossRank は -1〜5（どちらも任意）。
  セリフの話す人は置いたユニットのパイロットかナレーション（空）
- 出来事（7474/SRC#1689。goal・loss・events）: 条件と、きっかけ・援軍・会話の名前が置いたユニット（援軍も含む）のもの
使い方: python3 scenes/check.py   （リポジトリのルートで）
"""
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 7474/SRC の SRC.Sharp/Content/basic-data/Data/System/terrain.txt の番号（宇宙・月面を含む）
BASIC_TERRAINS = {0, 2, 10, 11, 15, 17, 19, 21, 22, 25, 29, 31, 32, 33, 42, 47, 48, 49, 83,
                  5, 12, 13, 28, 35, 36, 6, 7, 8, 14, 24, 62}
errors = []


def names(path):
    """データのファイルの、各データの名前（空行で区切った塊の最初の行）"""
    out, block = set(), []
    try:
        text = open(path, encoding='utf-8-sig').read()
    except FileNotFoundError:
        return out
    for line in text.split('\n') + ['']:
        s = line.strip()
        if s.startswith('#') or s.startswith("'") or s.startswith('//'):
            continue
        if not s:
            if block:
                out.add(block[0])
            block = []
        else:
            block.append(s)
    return out


before = subprocess.run(['git', 'status', '--porcelain', 'scenes'], cwd=ROOT, capture_output=True, text=True).stdout
subprocess.run([sys.executable, os.path.join(ROOT, 'scenes', 'make.py')], check=True)
after = subprocess.run(['git', 'status', '--porcelain', 'scenes'], cwd=ROOT, capture_output=True, text=True).stdout
if before != after:
    errors.append('make.py で作り直すと scenes/ が変わります（make.py を直して作り直してください）\n' + after)

index = {t['path']: t for t in json.load(open(os.path.join(ROOT, 'index.json'), encoding='utf-8'))['titles']}
for scene in json.load(open(os.path.join(ROOT, 'scenes', 'index.json'), encoding='utf-8'))['scenes']:
    sid = scene['id']
    lines = open(os.path.join(ROOT, 'scenes', scene['map']), encoding='utf-8', newline='').read().split('\r\n')
    w, h = map(int, lines[2].split(','))
    tiles = [l for l in lines[3:] if l]
    # SRC は幅か高さが 15 マス未満のマップをドラッグでスクロールしない（Main.frm の picMain_MouseMove）
    if w < 15 or h < 15:
        errors.append(f'{sid}: マップが {w}×{h} です。遊ぶときにドラッグでスクロールできるよう、幅・高さとも 15 マス以上にしてください')
    if len(tiles) != w * h:
        errors.append(f'{sid}: マップのマスの数が {w}×{h} と合いません')
    for t in tiles:
        if int(t.split(',')[0]) not in BASIC_TERRAINS:
            errors.append(f'{sid}: 最小の汎用データに無い地形 {t}')
            break
    units = scene.get('units', {})
    for side in ('allies', 'enemies'):
        for p in scene.get(side, []) + units.get(side, []):
            if not (1 <= p['x'] <= w and 1 <= p['y'] <= h):
                errors.append(f'{sid}: {side} の位置 ({p["x"]},{p["y"]}) がマップの外です')
    unit_names, pilot_names = set(), set()
    for path in scene.get('titles', []):
        title = index.get(path)
        if not title:
            errors.append(f'{sid}: 作品 {path} が index.json にありません')
            continue
        folders = [path]
        system = next((t for t in index.values() if t['base'] == title['base'] and t['title'] == 'System'), None)
        if system:
            folders.append(system['path'])
        for folder in folders:
            for f in index[folder]['files']:
                full = os.path.join(ROOT, folder, f)
                if f.lower() in ('robot.txt', 'unit.txt'):
                    unit_names |= names(full)
                elif f.lower() in ('pilot.txt', 'non_pilot.txt'):
                    pilot_names |= names(full)
    placed = set()
    events = scene.get('events', [])
    enemy_pilots = {u['pilot'] for u in units.get('enemies', [])} | {u['pilot'] for e in events for u in e.get('enemies', [])}
    ally_pilots = {u['pilot'] for u in units.get('allies', [])} | {u['pilot'] for e in events for u in e.get('allies', [])}
    for side in ('allies', 'enemies'):
        for u in units.get(side, []) + [x for e in events for x in e.get(side, [])]:
            if u['unit'] not in unit_names:
                errors.append(f'{sid}: ユニット「{u["unit"]}」が作品のデータにありません')
            if u['pilot'] not in pilot_names:
                errors.append(f'{sid}: パイロット「{u["pilot"]}」が作品のデータにありません')
            placed.add(u['pilot'])
            # ランクは 0〜20（既定 0）、ボスランクは -1（ボスにしない。既定）か 0〜5（SRC の BossRank）
            if not (isinstance(u.get('rank', 0), int) and 0 <= u.get('rank', 0) <= 20):
                errors.append(f'{sid}: 「{u["unit"]}」のランク {u.get("rank")} は 0〜20 にしてください')
            if not (isinstance(u.get('bossRank', -1), int) and -1 <= u.get('bossRank', -1) <= 5):
                errors.append(f'{sid}: 「{u["unit"]}」のボスランク {u.get("bossRank")} は -1〜5 にしてください')
    talks = list(scene.get('talk', {}).items()) + [(f'出来事 {i + 1}', e.get('talk', [])) for i, e in enumerate(events)]
    for key, talk in talks:
        for line in talk:
            if line['speaker'] and line['speaker'] not in placed:
                errors.append(f'{sid}: {key} の話す人「{line["speaker"]}」は置いたユニットのパイロットではありません')
    goal = scene.get('goal', {'kind': 'annihilate'})
    if goal['kind'] not in ('annihilate', 'boss', 'survive', 'reach'):
        errors.append(f'{sid}: 勝利の条件「{goal["kind"]}」は分かりません')
    if goal['kind'] == 'boss' and goal.get('target') not in enemy_pilots:
        errors.append(f'{sid}: 勝利の条件で倒す相手「{goal.get("target")}」は置いた敵のパイロットではありません')
    loss = scene.get('loss', {'kind': 'annihilate'})
    if loss['kind'] not in ('annihilate', 'unit', 'turns'):
        errors.append(f'{sid}: 敗北の条件「{loss["kind"]}」は分かりません')
    if loss['kind'] == 'unit' and loss.get('target') not in ally_pilots:
        errors.append(f'{sid}: 敗北の条件の「{loss.get("target")}」は置いた味方のパイロットではありません')
    for i, e in enumerate(events):
        if e.get('trigger') not in ('turn', 'attack', 'damaged', 'destroyed'):
            errors.append(f'{sid}: 出来事 {i + 1} のきっかけ「{e.get("trigger")}」は分かりません')
        for key in ('unit', 'target'):
            if key in e and e[key] not in placed:
                errors.append(f'{sid}: 出来事 {i + 1} の「{e[key]}」は置いたユニットのパイロットではありません')

for e in errors:
    print(f'::error::{e}')
print(f'{len(errors)} 件の問題')
sys.exit(1 if errors else 0)
