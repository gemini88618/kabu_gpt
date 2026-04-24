# Deployment

## Backend: Render

GitHub Pagesは静的ファイルだけを配信するため、`yfinance` を使った株価取得は別のPython APIで動かします。

1. Renderで `New Web Service` を作成します。
2. GitHubリポジトリを接続します。
3. `Root Directory` に `backend` を指定します。
4. Runtimeは `Docker` を選択します。
5. `Health Check Path` に `/api/health` を指定します。
6. デプロイ後のURLを控えます。

例:

```text
https://stock-scanner-api.onrender.com
```

## Frontend: GitHub Pages

リポジトリ直下の以下をGitHub Pagesで公開します。

```text
index.html
manifest.json
service-worker.js
icon.png
```

GitHubで `Settings` → `Pages` を開き、`Deploy from a branch` で `main` / `/root` を選択してください。

## API URL設定

GitHub Pagesでアプリを開いたら、画面内の `API接続` にRenderのURLを入力します。

```text
https://stock-scanner-api.onrender.com
```

`API URLを保存して接続確認` を押すと、ブラウザの `localStorage` に保存されます。

## Local Development

Backend:

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Frontend:

```bash
start index.html
```

ローカルで開いた場合、API URLの初期値は `http://localhost:8000` になります。
