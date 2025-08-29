#\\\\\\LIBARY\\\\\\
import os
import datetime
import discord
from discord.ext import commands
import requests
from myserver import server_on

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix="!", intents=intents)
client.remove_command("help")


#\\\\\\\\\Token\\\\\\\\\\\\\


#\\\Command\\\\
@client.command()
async def help(ctx):
    embed = discord.Embed(title=" Help Center", color=discord.Color.random())
    commands_info = {
        "!hi": "Say hello to the bot",
        "!sy": "Spam '!sybau!' 5 times",
        "!now": "Show current time in Bangkok/Thailand",
        "!bye": "Close the bot",
        "!members": "Show member count in this server",
        "!shownews": "Show news categories available",
        "!news": "Get latest news. Usage: !news <country> <category>",
        "!ip": "Show ip info",
        "!set_status": "Set Bot status"
    }

    for name, desc in commands_info.items():
        embed.add_field(name=name, value=desc, inline=False)

    await ctx.send(embed=embed)
@client.command()
async def hi(ctx):
    await ctx.send("hello!")
@client.command()
async def sy(ctx):
    for i in range(5):
        await ctx.send("!sybau!")
@client.command()
async def now(ctx):
    now = datetime.datetime.now()
    formatted_time = now.strftime("%H:%M:%S")


    embed_text = discord.Embed(
        title = f"Now is {formatted_time}",
        description= "🌏 Timezone: 🇹🇭 Bangkok/Thailand",
        color=discord.Color.blue())
    await ctx.send(embed=embed_text)
@client.command()
async def bye(ctx):
    await ctx.send("bye.")
    await client.close()
@client.command()
async def members(ctx):
    count = ctx.guild.member_count
    await ctx.send(f"member: {count}")
@client.command()
async def shownews(ctx):
        await ctx.send(
        "📢 Please choose a category by typing the letter:\n"
        "b = business\n"
        "e = entertainment\n"
        "g = general\n"
        "h = health\n"
        "s = science\n"
        "sp = sports\n"
        "t = technology"
    )
@client.command()
async def news(ctx, country: str, category: str):
    api_key = "193c27cc5e4f41209601bd8c4ebf4ce6"

    # แปลงตัวอักษรย่อเป็นชื่อ category
    choice = category.lower()
    mapping = {
        "b": "business",
        "e": "entertainment",
        "g": "general",
        "h": "health",
        "s": "science",
        "sp": "sports",
        "t": "technology"
    }

    if choice in mapping:
        category = mapping[choice]
    else:
        await ctx.send("❌ Invalid category! Use b/e/g/h/s/sp/t")
        return

    # ดึงข่าว
    url = f"https://newsapi.org/v2/top-headlines?country={country}&category={category}&apiKey={api_key}"
    res = requests.get(url).json()

    if res['status'] == 'ok' and len(res['articles']) > 0:
        article = res['articles'][0]

        # สร้าง embed สวย ๆ
        embed = discord.Embed(
            title=article['title'],
            description=article['description'] or "No description available.",
            url=article['url'],  # กดที่ title ไปยังข่าว
            color=discord.Color.random()  # สุ่มสี embed
        )
        embed.set_author(name=f"News from {article['source']['name']}")
        embed.set_footer(text=f"Category: {category.capitalize()} | Country: {country.upper()}")
        if article['urlToImage']:
            embed.set_image(url=article['urlToImage'])  # ใส่ภาพประกอบข่าว

        await ctx.send(embed=embed)
    else:
        await ctx.send("❌ No news found. Try another country or category.")
@client.command()
async def set_status(ctx, *, status: str):
    """เปลี่ยนสถานะของบอท"""
    await client.change_presence(activity=discord.Game(name=status))
    await ctx.send(f"บอทเปลี่ยนสถานะเป็น: {status}")
@client.command()
async def ip(ctx, ip_address: str):
    try:

        response = requests.get(f'https://ipinfo.io/{ip_address}/json')
        data = response.json()

        if 'error' in data:
            await ctx.send(f"ไม่สามารถค้นหาข้อมูลสำหรับ IP: {ip_address}")
            return

   
        location_info = (
            f"ข้อมูลสำหรับ IP: {ip_address}\n"
            f"ประเทศ: {data.get('country', 'ไม่ระบุ')}\n"
            f"จังหวัด: {data.get('region', 'ไม่ระบุ')}\n"
            f"เมือง: {data.get('city', 'ไม่ระบุ')}\n"
            f"ISP: {data.get('org', 'ไม่ระบุ')}\n"
            f"รายละเอียดเพิ่มเติม: {data.get('loc', 'ไม่ระบุ')}\n"
            f"ชื่อโฮสต์: {data.get('hostname', 'ไม่ระบุ')}\n"
            "**หมายเหตุ:** กรุณาใส่เป็น **Public IP** ไม่ใช่ **Private IP**\n"
            " เช่น `192.168.4.1` ❌"
        )

    
        await ctx.send(location_info)

    except Exception as e:
        await ctx.send(f"เกิดข้อผิดพลาด: {str(e)}")
#\\\\\EVENT\\\\\
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    print(f"{message.author}:{message.content}")

    await client.process_commands(message)
@client.event
async def on_reaction_add(reaction, user):
    print(f"{user} reaction {reaction.emoji} in {reaction.message.content}")
@client.event
async def on_ready():
    print(f"บอท {client.user} ออนไลน์แล้ว!")
    await client.change_presence(
    activity=discord.Activity(
        type=discord.ActivityType.watching,
        name="เอาชีวิตรอด 24 ชั่วโมงบนเกาะส่วนตัวทางภาคใต้ของประเทศไทย!"
    )
)
    ascii_art = r"""

██████╗  ██████╗ ████████╗     ██████╗ ███╗   ██╗
██╔══██╗██╔═══██╗╚══██╔══╝    ██╔═══██╗████╗  ██║
██████╔╝██║   ██║   ██║       ██║   ██║██╔██╗ ██║
█████═╝ ██║   ██║   ██║       ██║   ██║██║╚██╗██║
██║  ██╗╚██████╔╝   ██║       ╚██████╔╝██║ ╚████║
██████╔╝╚═════╝    ╚═╝        ╚═════╝ ╚═╝  ╚═══╝

"""
    print(ascii_art)




server_on()


#\\\RUN\\\\
client.run(os.getenv('Token'))
