import sys
import aiohttp
import asyncio
from datetime import datetime, timedelta

class PrivatBankAPI:
    API_URL = 'https://api.privatbank.ua/p24api/exchange_rates?json&date='

    async def fetch_data(self, date):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.API_URL}{date}") as response:
                return await response.json()

    async def get_exchange_rates(self, days):
        results = []
        today = datetime.now().date()
        for i in range(days):
            date = (today - timedelta(days=i)).strftime('%d.%m.%Y')
            data = await self.fetch_data(date)
            exchange_rate = {
                date: {
                    'EUR': {
                        'sale': data['exchangeRate'][0]['saleRateNB'],
                        'purchase': data['exchangeRate'][0]['purchaseRateNB']
                    },
                    'USD': {
                        'sale': data['exchangeRate'][1]['saleRateNB'],
                        'purchase': data['exchangeRate'][1]['purchaseRateNB']
                    }
                }
            }
            results.append(exchange_rate)
        return results

async def main(days):
    pb_api = PrivatBankAPI()
    exchange_rates = await pb_api.get_exchange_rates(days)
    print(exchange_rates)

if __name__ == "__main__":
    try:
        days = int(sys.argv[1])
    except IndexError:
        exit("Enter the number of days")
    if days > 10:
        print("Error: Maximum number of days allowed is 10")
    else:
        asyncio.run(main(days))
