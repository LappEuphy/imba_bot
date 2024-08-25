import discord
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

@bot.command()
async def set_permission(ctx, channel: discord.TextChannel, permission: str, value: bool):
    channel = bot.get_channel(channel.id)
    if channel is None:
        await ctx.send("Канал не найден.")
        return

    # Получаем текущие права доступа
    overwrites = channel.overwrites_for(ctx.guild.default_role)

    # Словарь для сопоставления строковых значений с атрибутами
    permissions_map = {
        'create_instant_invite': 'create_instant_invite',
        'kick_members': 'kick_members',
        'ban_members': 'ban_members',
        'administrator': 'administrator',
        'manage_channels': 'manage_channels',
        'manage_guild': 'manage_guild',
        'add_reactions': 'add_reactions',
        'view_audit_log': 'view_audit_log',
        'view_channel': 'view_channel',
        'send_messages': 'send_messages',
        'send_tts_messages': 'send_tts_messages',
        'manage_messages': 'manage_messages',
        'embed_links': 'embed_links',
        'attach_files': 'attach_files',
        'read_message_history': 'read_message_history',
        'mention_everyone': 'mention_everyone',
        'use_external_emojis': 'use_external_emojis',
        'view_guild_insights': 'view_guild_insights',
        'change_nickname': 'change_nickname',
        'manage_nicknames': 'manage_nicknames',
        'manage_roles': 'manage_roles',
        'manage_webhooks': 'manage_webhooks',
        'manage_emojis': 'manage_emojis',
        'use_slash_commands': 'use_slash_commands',
        'request_to_speak': 'request_to_speak',
        'manage_events': 'manage_events',
        'manage_threads': 'manage_threads',
        'create_public_threads': 'create_public_threads',
        'create_private_threads': 'create_private_threads',
        'use_external_stickers': 'use_external_stickers',
        'send_messages_in_threads': 'send_messages_in_threads',
        'moderate_members': 'moderate_members',
        'view_creator_monetization_analytics': 'view_creator_monetization_analytics',
        'use_soundboard': 'use_soundboard',
        'create_guild_expressions': 'create_guild_expressions',
        'create_events': 'create_events',
        'use_external_sounds': 'use_external_sounds',
        'send_voice_messages': 'send_voice_messages',
        'priority_speaker': 'priority_speaker',
        'stream': 'stream',
        'connect': 'connect',
        'speak': 'speak',
        'mute_members': 'mute_members',
        'deafen_members': 'deafen_members',
        'move_members': 'move_members',
        'use_voice_activation': 'use_voice_activation',
        'use_embedded_activities': 'use_embedded_activities',
        'set_voice_channel_status': 'set_voice_channel_status',
        'send_polls': 'send_polls',
        'use_external_apps': 'use_external_apps'
    }

    # Проверяем, существует ли указанное право
    if permission not in permissions_map:
        await ctx.send("Указанное право не найдено.")
        return

    # Устанавливаем новое значение права
    setattr(overwrites, permissions_map[permission], value)
    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrites)
    await ctx.send(f"Право {permission} {'включено' if value else 'выключено'}.")

# Запуск бота
bot.run(config['token'])
