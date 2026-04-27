const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type",
  "Access-Control-Max-Age": "86400"
};

function jsonResponse(body, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: {
      ...corsHeaders,
      "Content-Type": "application/json; charset=utf-8"
    }
  });
}

function clampText(value, maxLength = 1200) {
  return String(value ?? "").slice(0, maxLength);
}

function buildPrompt(stock) {
  const modelScores = Object.entries(stock.modelScores || {})
    .map(([key, value]) => `${key}: ${value}点`)
    .join(", ");
  const reasons = (stock.reasons || [])
    .map((reason) => `${reason.label}: ${reason.value}`)
    .join(", ");
  const warnings = (stock.riskWarnings || []).join(", ") || "特になし";

  return `
あなたは日本語で説明する株式分析アシスタントです。
以下の銘柄について、投資助言ではなく、アプリのスコアを読み解く中立的な解説をしてください。
断定を避け、「上昇しそう」ではなく「上昇期待が評価されている理由」として説明してください。

出力形式:
1. 期待が高い理由
2. 強い材料
3. 注意点
4. 期間別の見方
5. 最後に一言

銘柄:
- コード: ${clampText(stock.symbol, 40)}
- 会社名: ${clampText(stock.name, 120)}
- セクター: ${clampText(stock.sector, 80)}
- 期間: ${clampText(stock.periodType, 40)}
- 目標上昇率: +${stock.targetReturn}%
- 期待上昇率: ${stock.expectedReturn}%
- 総合評価: ${clampText(stock.grade, 20)}
- リスク: ${clampText(stock.riskLevel, 20)}
- リスク警告: ${clampText(warnings, 240)}

指標:
- PER: ${stock.factors?.per ?? "-"}
- PBR: ${stock.factors?.pbr ?? "-"}
- ROE: ${stock.factors?.roe ?? "-"}
- 売上成長率: ${stock.factors?.salesGrowth ?? "-"}
- 市場相対リターン: ${stock.factors?.relativeReturn ?? "-"}
- セクター相対リターン: ${stock.factors?.sectorRelativeReturn ?? "-"}
- 過去再現性: ${stock.factors?.reliability ?? "-"}

アプリ内スコア:
- 主要理由: ${clampText(reasons, 500)}
- 合議モデル: ${clampText(modelScores, 500)}

注意:
- 買い推奨・売り推奨とは書かない
- 不確実性とリスクを必ず含める
- 初心者にもわかる言葉で、400〜700字程度
`;
}

export default {
  async fetch(request, env) {
    if (request.method === "OPTIONS") {
      return new Response(null, { headers: corsHeaders });
    }

    const url = new URL(request.url);
    if (url.pathname === "/" && request.method === "GET") {
      return jsonResponse({
        ok: true,
        service: "Stock AI Explainer",
        endpoint: "/explain"
      });
    }

    if (url.pathname !== "/explain" || request.method !== "POST") {
      return jsonResponse({ error: "Not found" }, 404);
    }

    try {
      const stock = await request.json();
      if (!stock?.symbol || !stock?.name) {
        return jsonResponse({ error: "symbol and name are required" }, 400);
      }

      const prompt = buildPrompt(stock);
      const result = await env.AI.run("@cf/meta/llama-3.1-8b-instruct", {
        prompt,
        max_tokens: 900
      });

      const explanation = result?.response || result?.text || JSON.stringify(result);
      return jsonResponse({
        symbol: stock.symbol,
        explanation
      });
    } catch (error) {
      return jsonResponse({
        error: "AI explanation failed",
        detail: String(error?.message || error)
      }, 500);
    }
  }
};
