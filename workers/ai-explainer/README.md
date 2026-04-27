# Stock AI Explainer Worker

Cloudflare Workers AIを使って、Stock Scannerの銘柄スコアを日本語で解説するAPIです。

## 使うもの

- Cloudflare Workers
- Cloudflare Workers AI binding
- Model: `@cf/meta/llama-3.1-8b-instruct`

## デプロイ

```powershell
cd workers/ai-explainer
npx wrangler login
npx wrangler deploy
```

デプロイ後に表示されるURLを、アプリ画面の `AI解説API（Cloudflare Workers）を設定する` に保存してください。

例:

```text
https://stock-ai-explainer.your-name.workers.dev
```

## API

```http
POST /explain
Content-Type: application/json
```

PWAから銘柄名、指標、合議モデルスコアを送ると、LLMが日本語の解説を返します。

## 無料枠について

Cloudflare Workers AIはFree/Paid Workers plansで利用できます。Cloudflare公式ドキュメントでは、無料枠として1日10,000 Neuronsが案内されています。
