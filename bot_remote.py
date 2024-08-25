import discord
from discord import app_commands
from discord.ext import commands
import os

# Конфигурация бота
config = {
    'token': os.getenv("DISCORD_TOKEN"),
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
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} command(s)')
    except Exception as e:
        print(f'Failed to sync commands: {e}')

@bot.tree.command(name="toggle_view", description="Toggle the view permission of a channel")
async def toggle_view(interaction: discord.Interaction, channel: discord.TextChannel):
    if channel is None:
        await interaction.response.send_message("Канал не найден.", ephemeral=True)
        return

    # Получаем текущие права доступа
    overwrites = channel.overwrites_for(interaction.guild.default_role)
    # Меняем право просмотра канала
    overwrites.view_channel = not overwrites.view_channel
    await channel.set_permissions(interaction.guild.default_role, overwrite=overwrites)
    await interaction.response.send_message(f"Просмотр канала {'включён' if overwrites.view_channel else 'выключен'}.")

# Запуск бота
bot.run(config['token'])
