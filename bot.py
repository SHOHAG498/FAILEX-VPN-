import os
import discord
from discord.ext import commands
import requests

# Discord Bot Token & Configuration
TOKEN = os.getenv("DISCORD_TOKEN")  # Render-এর Environment Variable থেকে নেবে
FALIX_API_KEY = "flx_live_N41x35HDALAJohiMSUw8M4dHvD7RGSHpjX7AJ2xh"
SERVER_ID = "3517994"  # তোমার FalixNodes সার্ভার আইডি

# Panel API Base URL
BASE_URL = f"https://client.falixnodes.net/api/client/servers/{SERVER_ID}"

headers = {
    "Authorization": f"Bearer {FALIX_API_KEY}",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Bot logged in as {bot.user}')

@bot.command(name="VPN")
async def start_server(ctx):
    await ctx.send("⌛ সার্ভার অন করার রিকোয়েস্ট পাঠানো হচ্ছে...")
    
    url = f"{BASE_URL}/power"
    payload = {"signal": "start"}
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 204:
            await ctx.send("✅ **মাইনক্রাফট সার্ভার অন হচ্ছে!** ১-২ মিনিটের মধ্যে ঢুকতে পারবে।")
        elif response.status_code == 412:
            await ctx.send("⚠️ সার্ভারটি ইতোমধ্যে চালু আছে বা অন হচ্ছে!")
        else:
            await ctx.send(f"❌ সার্ভার অন করা যায়নি। Error Code: {response.status_code}")
    except Exception as e:
        await ctx.send(f"❌ কোনো একটি সমস্যা হয়েছে: {e}")

@bot.command(name="status")
async def check_status(ctx):
    try:
        response = requests.get(BASE_URL, headers=headers)
        if response.status_code == 200:
            data = response.json()
            state = data['attributes']['current_state']
            await ctx.send(f"📊 **সার্ভার স্ট্যাটাস:** `{state.upper()}`")
        else:
            await ctx.send("❌ স্ট্যাটাস চেক করা যায়নি।")
    except Exception as e:
        await ctx.send("❌ সমস্যা হয়েছে স্ট্যাটাস আনতে।")

bot.run(TOKEN)
