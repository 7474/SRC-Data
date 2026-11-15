#!/usr/bin/env python3
"""場面のカタログ（scenes/index.json）を確かめる（.github/workflows/validate-scenes.yml）。

- make.py で作り直しても変わらない（カタログとマップは make.py から作る）
- マップの大きさと行の数が合い、地形は SRC# の最小の汎用データ（basic-data）にあるもの。置く位置はマップの中
- titles は index.json の作品の path。units のユニット・パイロットはその作品（と同じデータパックの System）のデータにある。
  セリフの話す人は置いたユニットのパイロットかナレーション（空）
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
    for side in ('allies', 'enemies'):
        for u in units.get(side, []):
            if u['unit'] not in unit_names:
                errors.append(f'{sid}: ユニット「{u["unit"]}」が作品のデータにありません')
            if u['pilot'] not in pilot_names:
                errors.append(f'{sid}: パイロット「{u["pilot"]}」が作品のデータにありません')
            placed.add(u['pilot'])
    for key, talk in scene.get('talk', {}).items():
        for line in talk:
            if line['speaker'] and line['speaker'] not in placed:
                errors.append(f'{sid}: {key} の話す人「{line["speaker"]}」は置いたユニットのパイロットではありません')

for e in errors:
    print(f'::error::{e}')
print(f'{len(errors)} 件の問題')
sys.exit(1 if errors else 0)
