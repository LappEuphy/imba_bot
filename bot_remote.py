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

@bot.tree.command(name="toggle_permissions", description="Toggle permissions for a channel")
async def toggle_permissions(interaction: discord.Interaction, channel: discord.TextChannel, view: bool, manage_permissions: bool, manage_channel: bool):
    if channel is None:
        await interaction.response.send_message("Канал не найден.", ephemeral=True)
        return

    # Получаем текущие права доступа
    overwrites = channel.overwrites_for(interaction.guild.default_role)
    
    # Меняем право просмотра канала
    if view:
        overwrites.view_channel = not overwrites.view_channel
    
    # Меняем право на изменение прав в канале
    if manage_permissions:
        overwrites.manage_permissions = not overwrites.manage_permissions
    
    # Меняем право управления каналом
    if manage_channel:
        overwrites.manage_channel = not overwrites.manage_channel

    await channel.set_permissions(interaction.guild.default_role, overwrite=overwrites)
    await interaction.response.send_message(
        f"Просмотр канала {'включён' if overwrites.view_channel else 'выключен'}, "
        f"изменение прав {'включено' if overwrites.manage_permissions else 'выключено'}, "
        f"управление каналом {'включено' if overwrites.manage_channel else 'выключено'}."
    )

# Запуск бота
bot.run(config['token'])
