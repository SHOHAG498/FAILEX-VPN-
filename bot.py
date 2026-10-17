import os
import discord
from discord.ext import commands
import requests
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

# --- Render Port Binding Fix ---
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

# --- Discord Bot Configuration ---
TOKEN = os.getenv("DISCORD_TOKEN")
FALIX_API_KEY = "flx_live_3gPqUoiWErbgFjYemiThfOCRcQrvv9VIZ4gDPHrX"
SERVER_ID = "3517994"

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
    
    # FalixNodes API Endpoint
    urls = [
        f"https://client.falixnodes.net/api/client/servers/{SERVER_ID}/power",
        f"https://panel.falixnodes.net/api/client/servers/{SERVER_ID}/power"
    ]
    
    payload = {"signal": "start"}
    success = False

    for url in urls:
        try:
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code in [204, 200]:
                await ctx.send("✅ **মাইনক্রাফট সার্ভার অন হচ্ছে!** ১-২ মিনিটের মধ্যে ঢুকতে পারবে।")
                success = True
                break
            elif response.status_code == 412:
                await ctx.send("⚠️ সার্ভারটি ইতোমধ্যে চালু আছে বা অন হচ্ছে!")
                success = True
                break
        except Exception as e:
            pass

    if not success:
        await ctx.send(f"❌ সার্ভার অন করা যায়নি। (Error Code: 403 - API Key/Permissions issue)")

@bot.command(name="status")
async def check_status(ctx):
    url = f"https://client.falixnodes.net/api/client/servers/{SERVER_ID}"
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            state = data['attributes']['current_state']
            await ctx.send(f"📊 **সার্ভার স্ট্যাটাস:** `{state.upper()}`")
        else:
            await ctx.send(f"❌ স্ট্যাটাস আনা যায়নি। Error: {response.status_code}")
    except Exception as e:
        await ctx.send("❌ স্ট্যাটাস চেক করতে সমস্যা হয়েছে।")

bot.run(TOKEN)
