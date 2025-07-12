import discord
from discord.ext import commands
from discord.ui import View, Button
from rapidfuzz import process
import re
from datetime import datetime, timezone, timedelta
import pytz
import string
from discord import PartialEmoji
import asyncio

TOKEN = "x"

# Canal de log - substitua pelo ID do canal onde quer receber os logs
CANAL_LOG_ID = "x"  # Substitua pelo ID real do canal

intents = discord.Intents.all()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='*', intents=intents)

fruits = {
    "rocket": ("<:Rocket:1366602548642844734>", "Rocket", "5,000"),
    "spin": ("<:spin:1353905786711183461>", "Spin", "7,500"),
    "blade": ("<:blade:1353908156207730760>", "Blade", "30,000"),
    "spring": ("<:Spring:1366602998196736110>", "Spring", "60,000"),
    "bomb": ("<:bomb:1366603308936204358>", "Bomb", "80,000"),
    "smoke": ("<:smoke:1366603571361218700>", "Smoke", "100,000"),
    "spike": ("<:spike:1353905805392478260>", "Spike", "180,000"),
    "flame": ("<:flame:1366604323261251715>", "Flame", "250,000"),
    "ice": ("<:ice:1353906141926654083>", "Ice", "350,000"),
    "sand": ("<:sand:1353905898149384274>", "Sand", "420,000"),
    "dark": ("<:dark:1353906366435295327>", "Dark", "500,000"),
    "eagle": ("<:Eagle:1366600287590023198>", "Eagle", "550,000"),
    "diamond": ("<:diamond:1353906345992126494>", "Diamond", "600,000"),
    "light": ("<:light:1353906091309928581>", "Light", "650,000"),
    "rubber": ("<:rubber:1353905933838844006>", "Rubber", "750,000"),
    "ghost": ("<:ghost:1353906184389660683>", "Ghost", "940,000"),
    "magma": ("<:magma:1353906057000259645>", "Magma", "960,000"),
    "quake": ("<:quake:1353905970232692820>", "Quake", "1,000,000"),
    "buddha": ("<:buddha:1353906406742556702>", "Buddha", "1,200,000"),
    "love": ("<:love:1353906072464916551>", "Love", "1,300,000"),
    "creation": ("<:Creation:1366600390656921671>", "Creation", "1,400,000"),
    "spider": ("<:spider:1353905823209885726>", "Spider", "1,500,000"),
    "sound": ("<:sound:1353905840528035931>", "Sound", "1,700,000"),
    "phoenix": ("<:phoenix:1353906004366069852>", "Phoenix", "1,800,000"),
    "portal": ("<:portal:1353905986577895556>", "Portal", "1,900,000"),
    "rumble": ("<:rumble:1353905916470104116>", "Rumble", "2,100,000"),
    "pain": ("<:pain:1353906021797593233>", "Pain", "2,300,000"),
    "blizzard": ("<:blizzard:1353906455513923656>", "Blizzard", "2,400,000"),
    "gravity": ("<:Gravity:1366601369108090890>", "Gravity", "2,500,000"),
    "mammoth": ("<:mammoth:1353906041196253276>", "Mammoth", "2,700,000"),
    "trex": ("<:trex:1353905722374488094>", "Trex", "2,700,000"),
    "dough": ("<:dough:1353906309421863096>", "Dough", "2,800,000"),
    "shadow": ("<:shadow:1353905880692822066>", "Shadow", "2,900,000"),
    "venom": ("<:venom:1353905702808064000>", "Venom", "3,000,000"),
    "control": ("<:control:1353906385800138814>", "Control", "3,200,000"),
    "gas": ("<:gas:1353906203784122419>", "Gas", "3,200,000"),
    "spirit": ("<:spirit:1353905765605310474>", "Spirit", "3,400,000"),
    "leopard": ("<:leopard:1353906106996621414>", "Leopard", "5,000,000"),
    "yeti": ("<:yeti:1353905683438764122>", "Yeti", "5,000,000"),
    "kitsune": ("<:kitsune:1353906123815653376>", "Kitsune", "8,000,000"),
    "dragon": ("<:stockdragonfruit:1368609591075803279>", "Dragon", "15,000,000"),
}

reset_horarios = {
    "normal": ["9:00", "13:00", "17:00", "21:00", "1:00", "5:00"],
    "mirage": ["9:00", "11:00", "13:00", "15:00", "17:00", "19:00", "21:00", "23:00", "1:00", "3:00", "5:00", "7:00"]
}

emoji_normal = "<:1286146698120531980:1367880072433766440>"
emoji_mirage = "🏝️"

def extrair_frutas(texto):
    frutas_validas = {f.lower() for f in fruits.keys()}
    stopwords = {"e", "ou", "de", "a", "o", "um", "uma", "do", "da"}
    texto = texto.lower()
    texto = re.sub(r'<a?:\w+:\d+>', '', texto)
    texto = texto.replace('-', ' ')
    texto = texto.translate(str.maketrans('', '', string.punctuation))
    palavras = [p for p in texto.split() if p not in stopwords and len(p) > 2]

    frutas_encontradas = set()
    frutas_invalidas = []

    for palavra in palavras:
        resultado = process.extractOne(palavra, frutas_validas, score_cutoff=83)
        if resultado:
            frutas_encontradas.add(resultado[0])
        else:
            frutas_invalidas.append(palavra)

    frutas_encontradas.update(["spin", "rocket"])
    return sorted(frutas_encontradas), frutas_invalidas

def checar_permissao(ctx):
    cargos = {1353364912742858776, 1353390217645789224, 1366932437157937276, 1250635875289923606}
    return any(role.id in cargos for role in ctx.author.roles)

def calcular_proximo_reset(tipo):
    fuso = pytz.timezone('America/Sao_Paulo')
    agora = datetime.now(timezone.utc).astimezone(fuso)
    horarios = reset_horarios[tipo]
    proximo = None

    for hms in horarios:
        h, m = map(int, hms.split(":"))
        reset = agora.replace(hour=h, minute=m, second=0, microsecond=0)
        if reset <= agora:
            reset += timedelta(days=1)
        if proximo is None or reset < proximo:
            proximo = reset
    return proximo

async def enviar_log_stock(ctx, tipo, frutas_lista):
    """Envia log do stock para o canal específico"""
    try:
        canal_log = bot.get_channel(CANAL_LOG_ID)
        if not canal_log or not isinstance(canal_log, discord.TextChannel):
            print(f"❌ Canal de log não encontrado ou não é um canal de texto: {CANAL_LOG_ID}")
            return
        
        # Formata a lista de frutas
        frutas_formatadas = []
        for fruta in frutas_lista:
            emoji, nome, preco = fruits[fruta]
            frutas_formatadas.append(f"{emoji} {nome}")
        
        # Data e hora atual
        fuso = pytz.timezone('America/Sao_Paulo')
        agora = datetime.now(timezone.utc).astimezone(fuso)
        data_hora = agora.strftime("%d/%m/%Y às %H:%M:%S")
        
        # Emoji e cor baseado no tipo
        emoji_tipo = "📦" if tipo == "normal" else "🏝️"
        cor_tipo = 0x00ff00 if tipo == "normal" else 0xff8800
        
        # Cria o embed de log
        embed = discord.Embed(
            title=f"{emoji_tipo} Log de Stock - {tipo.upper()}",
            description=f"**👤 Usuário:** {ctx.author.mention} (`{ctx.author.name}`)\n"
                       f"**📋 Tipo de Stock:** {emoji_tipo} **{tipo.upper()}**\n"
                       f"**🕐 Data/Hora:** {data_hora}\n"
                       f"**📍 Canal:** {ctx.channel.mention}",
            color=cor_tipo
        )
        
        embed.add_field(
            name=f"🍇 Frutas do Stock ({len(frutas_lista)} frutas)",
            value="\n".join(frutas_formatadas) if frutas_formatadas else "Nenhuma fruta válida",
            inline=False
        )
        
        embed.set_footer(text=f"ID do usuário: {ctx.author.id}")
        embed.set_thumbnail(url=ctx.author.display_avatar.url)
        
        await canal_log.send(embed=embed)
        
    except Exception as e:
        print(f"❌ Erro ao enviar log: {e}")

async def enviar_estoque(ctx, tipo, frutas_lista):
    if not frutas_lista:
        erro_msg = await ctx.send(embed=discord.Embed(description=f"❌ Nenhuma fruta válida detectada para `{tipo}`.", color=0xff0000))
        await asyncio.sleep(5)
        await erro_msg.delete()
        return

    frutas_lista.sort(key=lambda f: list(fruits.keys()).index(f))
    proximo = calcular_proximo_reset(tipo)
    
    # Verifica se proximo não é None
    if proximo is None:
        erro_msg = await ctx.send(embed=discord.Embed(description="❌ Erro ao calcular próximo reset.", color=0xff0000))
        await asyncio.sleep(5)
        await erro_msg.delete()
        return
    
    emoji_tipo = emoji_normal if tipo == "normal" else emoji_mirage
    header = f"# __{tipo.capitalize()} Stock__ {emoji_tipo}"
    corpo = '\n'.join(f"{fruits[f][0]} | {fruits[f][1]} - <:cifrao:1367879504558686209> {fruits[f][2]}" for f in frutas_lista)

    # Mensagem inicial com tempo atual
    delta = proximo - datetime.now(timezone.utc).astimezone(pytz.timezone('America/Sao_Paulo'))
    horas, minutos = divmod(int(delta.total_seconds() // 60), 60)
    horario_msg = f"# Reseta às {proximo.strftime('%H:%M')} (em {horas}h {minutos}min) {emoji_tipo}"

    msg_final = await ctx.send(f"{header}\n{corpo}\n{horario_msg}")

    # Envia log do stock
    await enviar_log_stock(ctx, tipo, frutas_lista)

    # Tarefa que atualiza o tempo restante em tempo real
    async def atualizar_tempo():
        while True:
            agora = datetime.now(timezone.utc).astimezone(pytz.timezone('America/Sao_Paulo'))
            delta = proximo - agora
            if delta.total_seconds() <= 0:
                break
            horas, minutos = divmod(int(delta.total_seconds() // 60), 60)
            horario_msg = f"# Reseta às {proximo.strftime('%H:%M')} (em {horas}h {minutos}min) {emoji_tipo}"
            try:
                await msg_final.edit(content=f"{header}\n{corpo}\n{horario_msg}")
            except:
                break
            await asyncio.sleep(60)

    bot.loop.create_task(atualizar_tempo())

    # Reações
    try:
        await msg_final.add_reaction(PartialEmoji.from_str(fruits[frutas_lista[-1]][0]))
    except:
        pass

    for emj in ["<:w_:1368681825953644708>", "<:l_:1368681852050870353>", "<:punido2:1368682308022042684>"]:
        try:
            await msg_final.add_reaction(PartialEmoji.from_str(emj))
        except:
            pass

class EscolherTipoView(discord.ui.View):
    def __init__(self, autor):
        super().__init__(timeout=20)
        self.autor = autor
        self.valor = None
        self.message = None

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user != self.autor:
            await interaction.response.send_message("❌ Apenas quem usou o comando pode clicar aqui.", ephemeral=True)
            return False
        return True

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        try:
            if self.message:
                await self.message.edit(view=self)
                await asyncio.sleep(3)
                await self.message.delete()
        except:
            pass

    @discord.ui.button(label="Normal", style=discord.ButtonStyle.primary, emoji="📦")
    async def normal(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.valor = "normal"
        await interaction.response.defer()
        self.stop()

    @discord.ui.button(label="Mirage", style=discord.ButtonStyle.success, emoji="🏝️")
    async def mirage(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.valor = "mirage"
        await interaction.response.defer()
        self.stop()

async def esperar_resposta(ctx, check, timeout=20):
    """Espera mensagem do usuário com timeout.
    Em timeout envia aviso fixo (não apagado)."""
    try:
        resposta = await bot.wait_for("message", check=check, timeout=timeout)
        return resposta
    except asyncio.TimeoutError:
        # Mensagem fixa de timeout, NÃO será apagada
        await ctx.send(embed=discord.Embed(description="❌ Tempo esgotado.", color=0xff0000))
        return None

@bot.command()
async def s(ctx):
    await ctx.message.delete()
    mensagens_temp = []

    try:
        if not checar_permissao(ctx):
            erro_perm = await ctx.send(embed=discord.Embed(description="❌ Você não tem permissão para usar este comando.", color=0xff0000))
            # Apaga erro de permissão depois de 5 segundos
            await asyncio.sleep(5)
            await erro_perm.delete()
            return

        embed = discord.Embed(
            title="📦 Escolha o tipo de estoque",
            description="Clique em um dos botões abaixo para selecionar:",
            color=0x00ffcc
        )
        view = EscolherTipoView(ctx.author)
        msg_tipo = await ctx.send(embed=embed, view=view)
        view.message = msg_tipo
        mensagens_temp.append(msg_tipo)

        await view.wait()
        tipo = view.valor

        if not tipo:
            erro_timeout = await ctx.send(embed=discord.Embed(description="❌ Tempo esgotado.", color=0xff0000))
            # Apaga erro timeout depois de 5s? NÃO! Quer manter fixo, então não apaga.
            # Só retorna
            return

        embed2 = discord.Embed(title="🍇 Frutas", description="Mande a lista de frutas.", color=0xffcc00)
        msg_frutas = await ctx.send(embed=embed2)
        mensagens_temp.append(msg_frutas)

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        resposta = await esperar_resposta(ctx, check, timeout=20)
        if resposta is None:
            return
        mensagens_temp.append(resposta)

        frutas, ignoradas = extrair_frutas(resposta.content)
        frutas_validas = [f for f in frutas if f in fruits]

        if ignoradas:
            aviso = await ctx.send(f"⚠️ Frutas ignoradas: `{', '.join(ignoradas)}`")
            mensagens_temp.append(aviso)

        await enviar_estoque(ctx, tipo, frutas_validas)

    except Exception as e:
        erro = await ctx.send(embed=discord.Embed(description=str(e), color=0xff0000))
        # Apaga erro geral depois de 5 segundos
        await asyncio.sleep(5)
        await erro.delete()
    finally:
        for msg in mensagens_temp:
            try:
                await msg.delete()
            except: pass

@bot.command()
async def ss(ctx):
    await ctx.message.delete()
    mensagens_temp = []

    try:
        if not checar_permissao(ctx):
            erro_perm = await ctx.send(embed=discord.Embed(description="❌ Você não tem permissão para usar este comando.", color=0xff0000))
            await asyncio.sleep(5)
            await erro_perm.delete()
            return

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        msg1 = await ctx.send(embed=discord.Embed(title="🍇 Estoque Normal", description="Mande a lista de frutas para o estoque normal.", color=0x00ffcc))
        mensagens_temp.append(msg1)
        resposta_normal = await esperar_resposta(ctx, check, timeout=20)
        if resposta_normal is None:
            return
        mensagens_temp.append(resposta_normal)

        msg2 = await ctx.send(embed=discord.Embed(title="🍇 Estoque Mirage", description="Mande a lista de frutas para o estoque mirage.", color=0x00ffcc))
        mensagens_temp.append(msg2)
        resposta_mirage = await esperar_resposta(ctx, check, timeout=20)
        if resposta_mirage is None:
            return
        mensagens_temp.append(resposta_mirage)

        frutas_normal, ignoradas_normal = extrair_frutas(resposta_normal.content)
        frutas_mirage, ignoradas_mirage = extrair_frutas(resposta_mirage.content)

        ignoradas_total = set(ignoradas_normal + ignoradas_mirage)
        if ignoradas_total:
            aviso = await ctx.send(f"⚠️ Frutas ignoradas: `{', '.join(ignoradas_total)}`")
            mensagens_temp.append(aviso)

        await enviar_estoque(ctx, "normal", [f for f in frutas_normal if f in fruits])
        await enviar_estoque(ctx, "mirage", [f for f in frutas_mirage if f in fruits])

    except Exception as e:
        erro = await ctx.send(embed=discord.Embed(description=str(e), color=0xff0000))
        await asyncio.sleep(5)
        await erro.delete()
    finally:
        for msg in mensagens_temp:
            try:
                await msg.delete()
            except: pass

@bot.command()
async def ping(ctx):
    await ctx.message.delete()
    if not checar_permissao(ctx):
        erro_perm = await ctx.send(embed=discord.Embed(description="❌ Você não tem permissão para usar este comando.", color=0xff0000))
        await asyncio.sleep(5)
        await erro_perm.delete()
        return
    latencia = round(bot.latency * 1000)
    if latencia < 100:
        status = "✅ Rápido"
    elif latencia < 200:
        status = "🟡 OK"
    else:
        status = "🔴 Lento"

    embed = discord.Embed(title="�� Ping", description=f"Latência: {latencia}ms\nStatus: {status}", color=0x00ff00)
    await ctx.send(embed=embed)

@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user}")

bot.run(TOKEN)
