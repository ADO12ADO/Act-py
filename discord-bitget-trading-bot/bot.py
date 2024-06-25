import discord
import os
from dotenv import load_dotenv
from parser import parse_message
from bitget import place_order

load_dotenv()

TOKEN = os.getenv('DISCORD_BOT_TOKEN')
CHANNEL_ID = int(os.getenv('DISCORD_CHANNEL_ID'))

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.event
async def on_message(message):
    if message.channel.id == CHANNEL_ID and not message.author.bot:
        print('Message received:', message.content)
        order_details = parse_message(message.content)
        place_order(
            order_details['token'],
            order_details['entry_price'],
            order_details['invalidation_level'],
            order_details['target_prices'],
            balance=10000
        )
        await message.channel.send(f"Order placed for {order_details['token']}")

if __name__ == "__main__":
    print("Token from .env:", TOKEN)
    bot.run(TOKEN)
