from finlab.market_info import TWMarketInfo


market = TWMarketInfo()

def set_market(new_market):
    global market
    market = new_market

def reset_market():
    global market
    market = TWMarketInfo()
