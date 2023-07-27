import ccxt
import settings



target_percent = settings.TARGET_PERCENT
api_key = settings.API_KEY
api_secret = settings.API_SECRET
exchange = ccxt.binance({
        "apiKey": api_key,
        "secret": api_secret,

        'options': {
            
            'defaultType': 'future'
        },
        'enableRateLimit': True
    }) 


def close_all_position():
    positions = exchange.fetch_balance()['info']['positions']
    positions = [p for p in positions if float(p['positionAmt']) != 0]

    for position in positions:
        symbol= position['symbol']
        amount = float(position['positionAmt'])
        print(symbol)
        print(amount)
        exchange.cancel_all_orders(symbol)
        if amount > 0:
            # We need a Short to close
            print("long kapat")
            print(symbol)
            exchange.create_order(symbol=symbol,
                                      type='market',
                                      side='sell',
                                      amount=abs(amount))
        else:
            # We need a LONG to close
            print("short kapat")
            exchange.create_order(symbol=symbol,
                                      type='market',
                                      side='buy',
                                      amount=abs(amount))
import time
while True:
    balance = exchange.fetch_balance()
    total_balance = float(balance["info"]["totalWalletBalance"])
    total_profit = float(balance["info"]["totalUnrealizedProfit"])
    profit_percent = (total_profit / total_balance) * 100
    print(total_profit)
    print(profit_percent)

    if profit_percent >= target_percent:
        close_all_position()
        # print("ee")

