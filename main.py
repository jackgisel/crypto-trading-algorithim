import schedule
import time

from trading import check_products
from coinbase import get_holdings
from slack import send_message

def job(t):
    balances = get_holdings()
    buys = check_products()
    print(balances, buys)
    return

schedule.every(5).minutes.do(job, '\t---JOB RUNNING---\n')

while True:
    schedule.run_pending()
    time.sleep(1)