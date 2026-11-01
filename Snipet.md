# Snipet

## データのインデックスを作る

```sh
dotnet run --project ./tools
```

- 要 .NET5 環境

## データを検証する

```sh
docker run -it --rm -v ${PWD}:/data koudenpa/srcdatalinter:dev /data/Sharp
```

- 要 Docker 環境
- `dev` は 7474/SRC の開発版（master にマージされるたびに入れ替わる）。正式版は `latest`
- `srcsharp` で検査するときは `docker run --rm -v ${PWD}:/s koudenpa/srcdatalinter:dev lint /s/Sharp/Data`
- `${PWD}` の部分は環境に合わせて適当に変更してください

