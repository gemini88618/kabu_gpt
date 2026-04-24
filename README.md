# Stock Scanner

iPhone Safariからホーム画面に追加して使える、日本株・米国株対応の株スクリーニングPWAです。

## 構成

- `index.html`: GitHub Pages用の静的PWA
- `manifest.json`: GitHub Pages用PWA manifest
- `service-worker.js`: GitHub Pages用Service Worker
- `icon.png`: iPhoneホーム画面用アイコン
- `frontend/`: Next.js PWA
- `backend/`: Python FastAPI
- `docs/`: API設計とデプロイ手順

## 主な機能

- 日本株 / 米国株の切り替え
- 週 / 月 / 半年の期間切り替え
- 4パターンの期間表示
- トップ10銘柄ランキング
- 係数スライダーによるアルゴリズム調整
- yfinanceによる株価・財務データ取得
- バックテストAPIによる過去検証

## ローカル起動

### Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

フロントエンドは `http://localhost:3000`、APIは `http://localhost:8000/docs` で確認できます。

## 本番デプロイ

詳しくは [DEPLOYMENT.md](docs/DEPLOYMENT.md) を参照してください。

GitHub Pagesで使う場合は、リポジトリ直下の `index.html` を公開します。株価データ取得はGitHub Pagesでは実行できないため、`backend/` をRenderへデプロイし、画面内の `API接続` にRender URLを入力してください。

## 注意

このアプリは投資判断を補助するためのスクリーニングツールです。売買判断は自己責任で行ってください。
