import requests

BASE_URL = "https://glama.ai/mcp/servers/@Shaveen12/cse-mcp/api/stocks"


def get_mcp_stock_price(symbol: str) -> dict:
    """
    Fetch stock price from CSE MCP HTTP endpoint
    """

    try:
        url = f"{BASE_URL}/{symbol.upper()}"
        response = requests.get(url, timeout=5)

        if response.status_code != 200:
            raise Exception(f"MCP returned {response.status_code}")

        data = response.json()

        return {
            "symbol": data.get("symbol"),
            "last_trade_price": float(data.get("last_price", 0)),
            "change": float(data.get("change", 0)),
            "percent_change": float(data.get("percent_change", 0)),
            "volume": int(data.get("volume", 0))
        }

    except Exception as e:
        print("MCP fetch error:", e)
        return None
