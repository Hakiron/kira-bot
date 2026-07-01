import random
import os  # <-- ТЕПЕРЬ МОДУЛЬ НА МЕСТЕ!
import disnake
from disnake.ext import commands, tasks

# 1. НАСТРОЙКА ПРАВ БОТА
intents = disnake.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

LOG_CHANNEL_ID = int(os.environ.get("LOG_CHANNEL_ID", 0))

# --- СПИСОК СТАТУСОВ НА КАЖДЫЙ ДЕНЬ ---
BOT_STATUSES = [
    "(＃＞＜) Админы добрые, честно",
    "(≧◡≦) Я рада, что Вы тут",
    "(* ^ ω ^) Не обижай Друзяшек ",
    "(^ヮ^) Еще катку!!!",
    "(„• ᴗ •„) Хорошо Вам отдохнуть",
    "(￢‿￢ ) Не шали тут",
    "(ﾉ◕ヮ◕)ﾉ я все вижу",
    "(￣︿￣) Админ, где ЗП?"
]


# --- БЛОК 1: СИСТЕМНЫЕ СОБЫТИЯ И ФОНОВЫЙ ТАЙМЕР ---

@bot.event
async def on_ready():
    print("=========================================")
    print(f"Бот {bot.user.name} успешно запущен!")
    print("Фоновое обновление статусов активировано.")
    print("=========================================")

    # Запускаем фоновый цикл смены статуса, как только бот включился
    change_status_daily.start()


@tasks.loop(hours=24.0)
async def change_status_daily():
    """Фоновая задача, которая срабатывает раз в 24 часа"""
    new_status = random.choice(BOT_STATUSES)
    await bot.change_presence(activity=disnake.Game(name=new_status))
    print(f"[Статус] Бот обновил статус на: {new_status}")


# --- БЛОК 2: КОМАНДА !ROLL (РАНДОМАЙЗЕР) ---

@bot.command(name="roll", aliases=["Roll", "ROLL", "ролл", "Ролл"])
async def roll(ctx, *, args: str = None):
    if args is None:
        number = random.randint(1, 100)
        await ctx.send(f"🎲 {ctx.author.mention} выбросил число: **{number}** (из 100)")
        return

    if args.isdigit():
        max_value = int(args)
        if max_value <= 1:
            await ctx.send("⚠️ Число должно быть больше 1!")
            return
        number = random.randint(1, max_value)
        await ctx.send(f"🎲 {ctx.author.mention} выбросил число: **{number}** (из {max_value})")
        return

    choices = args.split()
    if len(choices) > 1:
        winner = random.choice(choices)
        await ctx.send(f"🔮 Мой выбор для {ctx.author.mention}: **{winner}**")
    else:
        await ctx.send("⚠️ Напиши число (например, `!roll 50`) или варианты через пробел (например, `!roll кс дота`)!")


# --- БЛОК 3: ОТПРАВКА ТЕКСТА ОТ ИМЕНИ БОТА ---

@bot.command()
@commands.has_permissions(manage_messages=True)
async def say(ctx, *, text: str):
    await ctx.message.delete()
    await ctx.send(text)


# --- БЛОК 4: КОМАНДЫ МОДЕРАЦИИ И СТАТИСТИКИ ---

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"✅ Удалено **{amount}** сообщений.", delete_after=5)


@bot.command()
async def ping(ctx):
    latency = round(bot.latency * 1000)
    await ctx.send(f"🏓 **Понг!** Задержка: {latency} мс")


@bot.command()
async def server(ctx):
    guild = ctx.guild
    await ctx.send(
        f"🎮 **Информация о сервере:**\n"
        f"• Название: **{guild.name}**\n"
        f"• Создатель: {guild.owner.mention}\n"
        f"• Участников: **{guild.member_count}**"
    )


# --- БЛОК 5: СИСТЕМА ЛОГИРОВАНИЯ ---

@bot.event
async def on_message_delete(message: disnake.Message):
    if message.author.bot: return
    log_channel = bot.get_channel(LOG_CHANNEL_ID)
    if log_channel:
        content = message.content if message.content else "*Нет текста*"
        embed = disnake.Embed(title="🗑️ Сообщение удалено", color=disnake.Color.red(), timestamp=message.created_at)
        embed.add_field(name="Автор:", value=f"{message.author.mention}", inline=False)
        embed.add_field(name="Текст:", value=f"```{content}```", inline=False)
        await log_channel.send(embed=embed)


@bot.event
async def on_message_edit(before: disnake.Message, after: disnake.Message):
    if before.author.bot or before.content == after.content: return
    log_channel = bot.get_channel(LOG_CHANNEL_ID)
    if log_channel:
        embed = disnake.Embed(title="✏️ Сообщение изменено", color=disnake.Color.orange())
        embed.add_field(name="Автор:", value=f"{before.author.mention}", inline=False)
        embed.add_field(name="Было:", value=f"```{before.content}```", inline=False)
        embed.add_field(name="Стало:", value=f"```{after.content}```", inline=False)
        await log_channel.send(embed=embed)


# --- БЕЗОПАСНЫЙ ЗАПУСК ---
bot.run(os.environ.get("DISCORD_TOKEN"))

















































































































































































