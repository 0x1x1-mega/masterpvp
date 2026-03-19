from discord.ext import commands
import discord
import aiohttp
import random
from urllib.parse import quote
import datetime
import os
from keep_alive import keep_alive

keep_alive()

TOKEN = os.getenv("DISCORD_TOKEN")
LOGS_CHANNELID = 1483592614555942952
WELCOME_CHANNELID = 1483592839546933268

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("Hazır!")

@bot.event
async def on_message_delete(msg: discord.Message):
    if msg.author == bot.user:
        return
    channel = bot.get_channel(LOGS_CHANNELID)
    await channel.send(f"Silinen mesaj: {msg.content} Mesajı yazan: {msg.author}")

@bot.event
async def on_message_edit(before: discord.Message, after: discord.Message):
    if before.author == bot.user:
        return
    channel = bot.get_channel(LOGS_CHANNELID)
    await channel.send(f"Düzenlenen mesaj: {before.content} → {after.content}\nYazan: {before.author}")

@bot.event
async def on_member_join(member: discord.Member):
    channel = bot.get_channel(WELCOME_CHANNELID)
    embed = discord.Embed(
        title="Yeni biri katıldı!",
        description=f"Hoşgeldin, {member.mention}!\nKurallara bakmayı unutma!",
        color=discord.Color.blurple()
    )
    embed.set_author(name="- Merlasy | Master PVP -")
    await channel.send(member.mention, embed=embed)

kufurler = ["sik", "fuck", "nig", "anan", "amın", "oros"]

@bot.event
async def on_message(msg: discord.Message):
    if msg.author == bot.user:
        return

    if msg.content.lower().startswith("sa"):
        await msg.channel.send(f"Aleyküm selam, {msg.author.mention}!")

    if any(k in msg.content.lower() for k in kufurler):
        await msg.delete()
        await msg.author.timeout(datetime.timedelta(minutes=10), reason="küfretme")
        await msg.channel.send(f"{msg.author.mention} küfretme sebebiyle 10 dk timeout yedi.")

    await bot.process_commands(msg)

@bot.command()
async def cmds(ctx):
    embed = discord.Embed(title="Komutlar", description="!cmds - Standart komutlar", color=discord.Color.blue())
    embed.add_field(name="!kick", value="@user -> Bir üyeyi atar.")
    embed.add_field(name="!ban", value="@user -> Bir üyeyi yasaklar.")
    embed.add_field(name="!help", value="Komutları gösterir")
    embed.add_field(name="!cmds", value="Komutları ve işlevlerini gösterir")
    embed.add_field(name="!rng", value="<min> <max> -> En az ve en çok sayı arasında bir sayı seçer")
    embed.add_field(name="!truthtr", value="Doğru olman gereken bir soru sorar")
    embed.add_field(name="!translate", value="<tr> <en> -> Türkçe'den İngilizce'ye çeviri")
    embed.set_author(name="MasterPVP - official.")
    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    if reason is None:
        reason = "Belirtilmedi"
    await ctx.guild.kick(member)
    await ctx.send(f"Kullanıcı {member.name} atıldı. Sebep: {reason}")

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    if reason is None:
        reason = "Belirtilmedi"
    await ctx.guild.ban(member)
    await ctx.send(f"Kullanıcı {member.name} yasaklandı. Sebep: {reason}")

sorular = [
    "En sevdiğin kişi kim?",
    "Hiç sevgilin oldu mu?",
    "Tekrar yaşamak istediğin bir anı var mı?",
    "Hiç tekrar görmek istediğin bir kişi oldu mu?",
    "Anan mı baban mı?",
    "Hiç sınıftayken osurdun mu?",
    "En utanç verici anın neydi?",
]

@bot.command()
async def truth(ctx):
    ch = random.choice(sorular)
    embed = discord.Embed(title="🎲 Rastgele Soru", description=ch, colour=discord.Color.blurple())
    embed.set_footer(text=f"İsteyen: {ctx.author.name}")
    await ctx.send(embed=embed)

@bot.command()
async def rng(ctx, min: int = 1, max: int = 100):
    if min >= max:
        await ctx.send("Az sayı çok sayıdan fazla olamaz!")
        return
    result = random.randint(min, max)
    await ctx.send(f"Sonuç: {result}")

@bot.command()
async def translate(ctx, *, text: str):
    try:
        async with aiohttp.ClientSession() as session:
            url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=tr&tl=en&dt=t&q={quote(text)}"
            async with session.get(url) as r:
                res = await r.json()
                result = res[0][0][0]
                embed = discord.Embed(title="🌍 Çeviri", color=discord.Color.green())
                embed.add_field(name="🇹🇷 Türkçe", value=text, inline=False)
                embed.add_field(name="🇬🇧 İngilizce", value=result, inline=False)
                embed.set_footer(text=f"İsteyen: {ctx.author.name}")
                await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Hata: {e}")

bot.run(TOKEN)