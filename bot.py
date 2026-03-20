import discord
from discord import app_commands
from discord.ext import commands
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

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree  # Slash command tree

# ──────────────────────────────────────────────
# BOT HAZIR
# ──────────────────────────────────────────────
@bot.event
async def on_ready():
    await tree.sync()  # Slash komutları Discord'a gönder
    print(f"Hazır! {bot.user} olarak giriş yapıldı.")

# ──────────────────────────────────────────────
# LOG: SİLİNEN MESAJ
# ──────────────────────────────────────────────
@bot.event
async def on_message_delete(msg: discord.Message):
    if msg.author == bot.user:
        return
    channel = bot.get_channel(LOGS_CHANNELID)
    if channel:
        await channel.send(f"🗑️ **Silinen mesaj:** {msg.content}\n**Yazan:** {msg.author}")

# ──────────────────────────────────────────────
# LOG: DÜZENLENENs MESAJ
# ──────────────────────────────────────────────
@bot.event
async def on_message_edit(before: discord.Message, after: discord.Message):
    if before.author == bot.user:
        return
    channel = bot.get_channel(LOGS_CHANNELID)
    if channel:
        await channel.send(
            f"✏️ **Düzenlenen mesaj:**\n"
            f"**Önce:** {before.content}\n"
            f"**Sonra:** {after.content}\n"
            f"**Yazan:** {before.author}"
        )

# ──────────────────────────────────────────────
# HOŞGELDİN
# ──────────────────────────────────────────────
@bot.event
async def on_member_join(member: discord.Member):
    channel = bot.get_channel(WELCOME_CHANNELID)
    if channel:
        embed = discord.Embed(
            title="Yeni biri katıldı! 🎉",
            description=f"Hoşgeldin, {member.mention}!\nKurallara bakmayı unutma!",
            color=discord.Color.blurple()
        )
        embed.set_author(name="- Merlasy | Master PVP -")
        await channel.send(member.mention, embed=embed)

# ──────────────────────────────────────────────
# KÜFÜR FİLTRESİ
# ──────────────────────────────────────────────
kufurler = ["sik", "fuck", "nig", "anan", "amın", "oros"]

@bot.event
async def on_message(msg: discord.Message):
    if msg.author == bot.user:
        return

    if msg.content.lower().startswith("sa"):
        await msg.channel.send(f"Aleyküm selam, {msg.author.mention}!")

    if any(k in msg.content.lower() for k in kufurler):
        await msg.delete()
        await msg.author.timeout(datetime.timedelta(minutes=10), reason="Küfür")
        await msg.channel.send(f"{msg.author.mention} küfretme sebebiyle 10 dk timeout yedi.")

    await bot.process_commands(msg)

# ──────────────────────────────────────────────
# /cmds
# ──────────────────────────────────────────────
@tree.command(name="cmds", description="Tüm komutları ve işlevlerini gösterir.")
async def cmds(interaction: discord.Interaction):
    embed = discord.Embed(
        title="📋 Komutlar",
        description="Slash komutların listesi:",
        color=discord.Color.blue()
    )
    embed.add_field(name="/kick", value="@kullanıcı → Bir üyeyi atar.", inline=False)
    embed.add_field(name="/ban", value="@kullanıcı → Bir üyeyi yasaklar.", inline=False)
    embed.add_field(name="/timeout", value="@kullanıcı <dakika> → Bir üyeye timeout verir.", inline=False)
    embed.add_field(name="/untimeout", value="@kullanıcı → Bir üyenin timeoutunu kaldırır.", inline=False)
    embed.add_field(name="/rng", value="<min> <max> → Rastgele sayı seçer.", inline=False)
    embed.add_field(name="/truth", value="Sana doğruluk sorusu sorar.", inline=False)
    embed.add_field(name="/translate", value="<metin> → Türkçe'den İngilizce'ye çevirir.", inline=False)
    embed.add_field(name="/cmds", value="Bu listeyi gösterir.", inline=False)
    embed.add_field(name="/hesapla", value="<sayı1> <işlem> <sayı2> → Matematik işlemi yapar.", inline=False)
    embed.set_author(name="MasterPVP - official.")
    await interaction.response.send_message(embed=embed)

# ──────────────────────────────────────────────
# /kick
# ──────────────────────────────────────────────
@tree.command(name="kick", description="Bir üyeyi sunucudan atar.")
@app_commands.describe(member="Atılacak kullanıcı", reason="Atılma sebebi")
@app_commands.checks.has_permissions(kick_members=True)
async def kick(interaction: discord.Interaction, member: discord.Member, reason: str = "Belirtilmedi"):
    await interaction.guild.kick(member, reason=reason)
    await interaction.response.send_message(f"✅ **{member.name}** atıldı. Sebep: {reason}")

@kick.error
async def kick_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.MissingPermissions):
        await interaction.response.send_message("❌ Bu komutu kullanmak için **Üye At** iznine ihtiyacın var.", ephemeral=True)

# ──────────────────────────────────────────────
# /ban
# ──────────────────────────────────────────────
@tree.command(name="ban", description="Bir üyeyi sunucudan yasaklar.")
@app_commands.describe(member="Yasaklanacak kullanıcı", reason="Yasaklanma sebebi")
@app_commands.checks.has_permissions(ban_members=True)
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = "Belirtilmedi"):
    await interaction.guild.ban(member, reason=reason)
    await interaction.response.send_message(f"🔨 **{member.name}** yasaklandı. Sebep: {reason}")

@ban.error
async def ban_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.MissingPermissions):
        await interaction.response.send_message("❌ Bu komutu kullanmak için **Üye Yasakla** iznine ihtiyacın var.", ephemeral=True)

# ──────────────────────────────────────────────
# /timeout
# ──────────────────────────────────────────────
@tree.command(name="timeout", description="Bir üyeye timeout verir.")
@app_commands.describe(
    member="Timeout verilecek kullanıcı",
    sure="Timeout süresi (dakika cinsinden)",
    reason="Timeout sebebi"
)
@app_commands.checks.has_permissions(moderate_members=True)
async def timeout(interaction: discord.Interaction, member: discord.Member, sure: int = 10, reason: str = "Belirtilmedi"):
    if member.top_role >= interaction.user.top_role:
        await interaction.response.send_message("❌ Kendinle aynı veya daha yüksek roldeki birine timeout veremezsin!", ephemeral=True)
        return
    await member.timeout(datetime.timedelta(minutes=sure), reason=reason)
    embed = discord.Embed(
        title="⏳ Timeout Verildi",
        color=discord.Color.orange()
    )
    embed.add_field(name="Kullanıcı", value=member.mention, inline=True)
    embed.add_field(name="Süre", value=f"{sure} dakika", inline=True)
    embed.add_field(name="Sebep", value=reason, inline=False)
    embed.add_field(name="Veren", value=interaction.user.mention, inline=True)
    await interaction.response.send_message(embed=embed)

@timeout.error
async def timeout_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.MissingPermissions):
        await interaction.response.send_message("❌ Bu komutu kullanmak için **Üyeleri Sustur** iznine ihtiyacın var.", ephemeral=True)

# ──────────────────────────────────────────────
# /untimeout
# ──────────────────────────────────────────────
@tree.command(name="untimeout", description="Bir üyenin timeoutunu kaldırır.")
@app_commands.describe(member="Timeoutu kaldırılacak kullanıcı")
@app_commands.checks.has_permissions(moderate_members=True)
async def untimeout(interaction: discord.Interaction, member: discord.Member):
    await member.timeout(None)
    embed = discord.Embed(
        title="✅ Timeout Kaldırıldı",
        description=f"{member.mention} kullanıcısının timeoutu kaldırıldı.",
        color=discord.Color.green()
    )
    embed.add_field(name="Kaldıran", value=interaction.user.mention, inline=True)
    await interaction.response.send_message(embed=embed)

@untimeout.error
async def untimeout_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.MissingPermissions):
        await interaction.response.send_message("❌ Bu komutu kullanmak için **Üyeleri Sustur** iznine ihtiyacın var.", ephemeral=True)

# ──────────────────────────────────────────────
# /truth
# ──────────────────────────────────────────────
sorular = [
    "En sevdiğin kişi kim?",
    "Hiç sevgilin oldu mu?",
    "Tekrar yaşamak istediğin bir anı var mı?",
    "Hiç tekrar görmek istediğin bir kişi oldu mu?",
    "Anan mı baban mı?",
    "Hiç sınıftayken osurdun mu?",
    "En utanç verici anın neydi?",
]

@tree.command(name="truth", description="Sana rastgele bir doğruluk sorusu sorar.")
async def truth(interaction: discord.Interaction):
    soru = random.choice(sorular)
    embed = discord.Embed(
        title="🎲 Rastgele Soru",
        description=soru,
        colour=discord.Color.blurple()
    )
    embed.set_footer(text=f"İsteyen: {interaction.user.name}")
    await interaction.response.send_message(embed=embed)

# ──────────────────────────────────────────────
# /rng
# ──────────────────────────────────────────────
@tree.command(name="rng", description="Belirtilen aralıkta rastgele bir sayı seçer.")
@app_commands.describe(min="En küçük sayı (varsayılan: 1)", max="En büyük sayı (varsayılan: 100)")
async def rng(interaction: discord.Interaction, min: int = 1, max: int = 100):
    if min >= max:
        await interaction.response.send_message("❌ Az sayı çok sayıdan fazla olamaz!", ephemeral=True)
        return
    result = random.randint(min, max)
    await interaction.response.send_message(f"🎰 **Sonuç:** {result}")

# ──────────────────────────────────────────────
# /translate
# ──────────────────────────────────────────────
@tree.command(name="translate", description="Türkçe metni İngilizce'ye çevirir.")
@app_commands.describe(text="Çevrilecek Türkçe metin")
async def translate(interaction: discord.Interaction, text: str):
    await interaction.response.defer()  # API çağrısı uzun sürebilir
    try:
        async with aiohttp.ClientSession() as session:
            url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=tr&tl=en&dt=t&q={quote(text)}"
            async with session.get(url) as r:
                res = await r.json()
                result = res[0][0][0]
                embed = discord.Embed(title="🌍 Çeviri", color=discord.Color.green())
                embed.add_field(name="🇹🇷 Türkçe", value=text, inline=False)
                embed.add_field(name="🇬🇧 İngilizce", value=result, inline=False)
                embed.set_footer(text=f"İsteyen: {interaction.user.name}")
                await interaction.followup.send(embed=embed)
    except Exception as e:
        await interaction.followup.send(f"❌ Hata: {e}")

# ──────────────────────────────────────────────
# /hesapla
# ──────────────────────────────────────────────
@tree.command(name="hesapla", description="İki sayı ile matematik işlemi yapar.")
@app_commands.describe(
    sayi1="Birinci sayı",
    islem="Yapılacak işlem",
    sayi2="İkinci sayı"
)
@app_commands.choices(islem=[
    app_commands.Choice(name="➕ Toplama",    value="toplama"),
    app_commands.Choice(name="➖ Çıkarma",   value="cikarma"),
    app_commands.Choice(name="✖️ Çarpma",    value="carpma"),
    app_commands.Choice(name="➗ Bölme",     value="bolme"),
    app_commands.Choice(name="🔢 Üs Alma",   value="us"),
])
async def hesapla(
    interaction: discord.Interaction,
    sayi1: float,
    islem: app_commands.Choice[str],
    sayi2: float
):
    semboller = {
        "toplama": "+",
        "cikarma": "−",
        "carpma":  "×",
        "bolme":   "÷",
        "us":      "^",
    }

    if islem.value == "toplama":
        sonuc = sayi1 + sayi2
    elif islem.value == "cikarma":
        sonuc = sayi1 - sayi2
    elif islem.value == "carpma":
        sonuc = sayi1 * sayi2
    elif islem.value == "bolme":
        if sayi2 == 0:
            await interaction.response.send_message(
                "❌ Sıfıra bölme yapılamaz!", ephemeral=True
            )
            return
        sonuc = sayi1 / sayi2
    elif islem.value == "us":
        if sayi1 == 0 and sayi2 < 0:
            await interaction.response.send_message(
                "❌ 0'ın negatif üssü hesaplanamaz!", ephemeral=True
            )
            return
        sonuc = sayi1 ** sayi2

    # Tam sayıysa .0 gösterme
    sayi1_str = int(sayi1) if sayi1 == int(sayi1) else sayi1
    sayi2_str = int(sayi2) if sayi2 == int(sayi2) else sayi2
    sonuc_str = int(sonuc) if isinstance(sonuc, float) and sonuc == int(sonuc) else sonuc

    sembol = semboller[islem.value]

    embed = discord.Embed(
        title="🧮 Hesap Makinesi",
        color=discord.Color.blurple()
    )
    embed.add_field(
        name="İşlem",
        value=f"`{sayi1_str} {sembol} {sayi2_str}`",
        inline=False
    )
    embed.add_field(
        name="Sonuç",
        value=f"**`{sonuc_str}`**",
        inline=False
    )
    embed.set_footer(text=f"İsteyen: {interaction.user.name}")
    await interaction.response.send_message(embed=embed)

# Basic discord.py
@tree.command(name="print", description="İstediğin bişeyi yazdırır!")
@app_commands.describe(text="Enter your text")
async def print(interaction:discord.Interaction, text: str):
    await interaction.response.send_message(text)

# ──────────────────────────────────────────────
# ÇALIŞTIR
# ──────────────────────────────────────────────
bot.run(TOKEN)
