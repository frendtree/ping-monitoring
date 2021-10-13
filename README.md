# ping-monitoring

Pingによる死活チェックを行い、応答が無い場合はメールを送信します。

## 動作環境
- docker-compose
  - python 3.10

## 設定方法
設定ファイルを適宜修正して利用してください。
```shell
cp settings.env.example settings.env
vi settings.env
```

## 実行方法
```shell
docker-compose build
docker-compose up
```
Ping成功時は「Success!」と出力されます。
失敗時は、「Failed！」と出力され、メールが送信されます。
