# Snipet

## データのインデックスを作る

```sh
dotnet run --project ./tools
```

- 要 .NET5 環境

## データを検証する

```sh
docker run -it -v ${PWD}:/data koudenpa/srcdatalinter:latest /data/Sharp
```

- 要 Docker 環境
- `${PWD}` の部分は環境に合わせて適当に変更してください

