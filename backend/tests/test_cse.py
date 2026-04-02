from cse_lk import CSEClient

client = CSEClient()
summary = client.get_market_summary()


summary_dict = summary.__dict__
print(summary_dict)
