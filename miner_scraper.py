import discord
from discord.client import Client
import requests  # http request
from bs4 import BeautifulSoup  # web scraping

# Discord bot token. You will need your own.
TOKEN = 'YOUR_TOKEN_HERE'

client = discord.Client()


g = []


def listToString(g):

    # initialize an empty string
    string = ""

    # return string
    return (string.join(g))


def discord_bot():
    # site used for scraping
    url = "https://2cryptocalc.com/"
    result = requests.get(url).text
    soup = BeautifulSoup(result, 'html.parser')

    tbody = soup.tbody
    trs = tbody.contents
    # loop for scraping
    for coin in trs[:6]:
        coin_names = coin.find('span', class_="crypto-coin__name")
        if coin_names is not None:
            atr = coin_names.descendants
            name = list(atr)[0]
        coin_pools = coin.find('span', class_="crypto-coin__pool")
        if coin_pools is not None:
            pool = coin_pools.text

        coin_prices = coin.find('span', class_="text-val")
        if coin_prices is not None:
            price = coin_prices.text

        coin_rate = coin.find('span', class_="exchange-rate p-up")
        if coin_rate is not None:
            rate = coin_rate.text

        coin_nethash = coin.find(class_="column_desktop text-right")
        if coin_nethash is not None:
            nethash_atr = coin_nethash.descendants
            nethash = list(nethash_atr)[1].text
            nethash_atr = coin_nethash.descendants
            nethash_rate = list(nethash_atr)[5].text

        coin_profit = coin.find('span', class_='crypto-val-no-pad')
        if coin_profit is not None:
            atr = coin_profit.descendants
            profit = list(atr)[0].text
            atr = coin_profit.descendants
            amount = list(atr)[5].text

            g.append("Name: " + name + "\n" + pool + "\n" + "Current price: " + price + "\n" + "Current rate: " + rate + "\n" +
                     "Nethash: " + nethash + " " + nethash_rate + "\n" + "Profit 24h: " + profit+"\n" + "Amount: " + amount + '\n' + '\n')

    return listToString(g)


print(discord_bot())

# login discord bot


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

# the even handler for when the bot is made a request in Discord.


@client.event
async def on_message(message):
    username = str(message.author.name)
    user_message = str(message.content)
    channel = str(message.channel.name)
    print(f'{username}: {user_message} ({channel})')

    if message.author == client.user:
        return
    if message.channel.name == "general":
        if user_message.lower() == '!miner':

            await message.channel.send(discord_bot())

g.clear()
client.run(TOKEN)
