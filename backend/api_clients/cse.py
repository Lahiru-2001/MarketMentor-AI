from cse_lk import CSEClient

# Initialize the CSE client once
_client = CSEClient()


def get_cse_market_summary() -> dict:
    """
    Get the current Colombo Stock Exchange market summary
    Returns as a dictionary suitable for JSON responses.
    """
    summary = _client.get_market_summary()
    return summary.__dict__


def get_cse_company_info(symbol: str) -> dict:
    """
    Get detailed info for a specific company by symbol
    """
    company = _client.get_company_info(symbol)
    return company.__dict__


def get_cse_share_price(symbol: str) -> dict:
    """
    Get latest share price info for a specific company
    """
    share_price = _client.get_share_price(symbol)
    return share_price.__dict__


def get_cse_top_gainers() -> list:
    """
    Get list of top gaining shares
    """
    gainers = _client.get_top_gainers()
    # Convert each object to dict
    return [g.__dict__ for g in gainers]


def get_cse_top_losers() -> list:
    """
    Get list of top losing shares
    """
    losers = _client.get_top_losers()
    return [l.__dict__ for l in losers]


def get_cse_listed_companies() -> list:
    """
    Get all listed companies on the CSE
    """
    companies = _client.get_listed_companies()
    return [c.__dict__ for c in companies]
