import os
import discord
from discord.ext import commands
import requests
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

# --- Render Port Binding Fix (যাতে Render-এ কোনো পোর্ট ওয়ার্নিং না আসে) ---
class DummyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running successfully!")

def run_dummy_server():
    port = int(os.getenv("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), DummyHandler)
    server.serve_forever()

threading.Thread(target=run_dummy_server, daemon=True).start()

# --- Discord Bot Setup ---
TOKEN = os.getenv("DISCORD_TOKEN")
SERVER_IP = "SRSHOHAG9834.aternos.me"  # তোমার Aternos সার্ভার আইপি

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Bot logged in successfully as {bot.user}')

@bot.command(name="status")
async def check_status(ctx):
    # মাইনক্রাফট সার্ভার স্ট্যাটাস চেক করার পাবলিক এপিআই
    url = f"https://api.mcsrvstat.us/2/{SERVER_IP}"
    try:
        response = requests.get(url)
        data = response.json()
        if data.get("online"):
            players = data["players"]["online"]
            max_players = data["players"]["max"]
            await ctx.send(f"✅ সার্ভার বর্তমানে **ONLINE** আছে! \n👥 প্লেয়ার খেলছে: {players}/{max_players}")
        else:
            await ctx.send(f"❌ সার্ভার বর্তমানে **OFFLINE** আছে! আগে Aternos ওয়েবসাইট বা অ্যাপ থেকে স্টার্ট করে নাও।")
    except Exception as e:
        await ctx.send("⚠️ সার্ভার স্ট্যাটাস চেক করতে সমস্যা হয়েছে।")

@bot.command(name="ping")
async def ping(ctx):
    await ctx.send(f"🏓 Pong! Latency: {round(bot.latency * 1000)}ms")

bot.run(TOKEN)
