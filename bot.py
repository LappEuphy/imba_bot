import discord
from discord.ext import commands

# Конфигурация бота
config = {
    'token': '...',
    'prefix': '!',
}

# Создание объекта intents
intents = discord.Intents.default()
intents.message_content = True  # Включаем доступ к содержимому сообщений

# Создание экземпляра бота
bot = commands.Bot(command_prefix=config['prefix'], intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command()
async def toggle_view(ctx, channel_id: int):
    channel = bot.get_channel(channel_id)
    if channel is None:
        await ctx.send("Канал не найден.")
        return

    # Получаем текущие права доступа
    overwrites = channel.overwrites_for(ctx.guild.default_role)
    # Меняем право просмотра канала
    overwrites.view_channel = not overwrites.view_channel
    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrites)
    await ctx.send(f"Право просмотра канала {'включено' if overwrites.view_channel else 'выключено'}.")

# Запуск бота
bot.run(config['token'])
