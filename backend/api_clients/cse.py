from cse_lk import CSEClient

_client = CSEClient()


def get_cse_market_summary() -> dict:
    summary = _client.get_market_summary()
    return summary.__dict__


def get_cse_company_info(symbol: str) -> dict:
    company = _client.get_company_info(symbol)
    return company.__dict__


def get_cse_share_price(symbol: str) -> dict:

    shares = _client.get_today_share_prices()

    if not shares:
        raise Exception("CSE returned empty share price list")

    symbol = symbol.upper()

    for share in shares:
        share_symbol = share.symbol.upper()

       
        base_symbol = share_symbol.split(".")[0]

        if base_symbol == symbol:
            return {
                "symbol": base_symbol,
                "last_trade_price": share.last_trade_price,
                "change": share.change,
                "percent_change": share.percent_change,
                "volume": share.volume
            }

    raise Exception(f"Symbol {symbol} not found in CSE list")

