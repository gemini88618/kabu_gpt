# API Specification

## GET `/health`

ヘルスチェック。

## GET `/api/stocks/{market}`

対象市場の銘柄一覧を返します。

- `market`: `jp` or `us`

## POST `/api/screen`

株スクリーニングを実行します。

```json
{
  "market": "jp",
  "period_type": "weekly",
  "period_slot": "current_to_next",
  "coefficients": {
    "per": 0.08,
    "pbr": 0.07,
    "roe": 0.15,
    "sales_growth": 0.16,
    "moving_average": 0.18,
    "volume": 0.16,
    "momentum": 0.2
  }
}
```

## POST `/api/backtest`

同じ係数・市場・期間で過去検証を実行します。

期間タイプ:

- `weekly`: 1週間、目標 `+10%`
- `monthly`: 1か月、目標 `+50%`
- `half_year`: 半年、目標 `+300%`

期間スロット:

- `p3_to_p2`
- `p2_to_p1`
- `p1_to_now`
- `current_to_next`
