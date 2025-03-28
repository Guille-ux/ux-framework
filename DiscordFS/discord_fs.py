import json
import time
import math
import random
import discord

def faker(bot, channel_id):
    channel = bot.get_channel(channel_id)
    return FakeContext(bot, channel)

class FakeContext:
    def __init__(self, bot, channel):
        self.bot = bot
        self.guild = channel.guild
        self.channel = channel
        self.author = bot.user

class DiscordFS:
    def __init__(self, maxes, bot):
        self.bot = bot
        self.max = maxes
        self.users = {}
        self.current = 0
        self.users_list = []
    
    def init_fs(self, user, channel):
        self.users[user] = channel
        self.users_list.append(user)
        self.current += 1
        if self.current == self.max:
            self.current -= 1
            del self.users[self.users_list[0]]
            self.users_list.pop(0)

    async def list(self, user, limit=10):
        try:
            channel_id = self.users[user]
            channel = self.bot.get_channel(channel_id)
            if not channel:
                return "Wtf, no existe"
            messages = [msg async for msg in channel.history(limit=limit)]
            return "\n - ".join(f"{msg.author.name}: {msg.content}" for msg in messages)
        except Exception as e:
            return f"Error {e}"

    def dir(self, user):
        try:
            channel = self.users[user]
            ctx = faker(self.bot, channel)
            channels = ctx.guild.channels
            channel_names = [ch.name for ch in channels]
            return "\n - ".join(channel_names)
        except Exception as e:
            return f"Hubo un error: {e}"

    def pwd(self, user):
        try:
            ctx = faker(self.bot, self.users[user])
            channel = ctx.channel.name
            return "Estás en: " + channel
        except Exception:
            return "No existes, eres un fantasma"

    def cd(self, user, channel):
        try:
            ctx = faker(self.bot, self.users[user])
            guild = ctx.guild
            new_channel = discord.utils.get(guild.channels, name=channel)
            if new_channel is None:
                return "Error, el canal no existe"
            self.users[user] = new_channel.id
            return f"Directorio actual: '{new_channel.name}'"
        except Exception as e:
            return f"Error: {e}"

    # Nuevo método para enviar mensajes
    async def send_message(self, user, content):
        try:
            channel_id = self.users[user]
            channel = self.bot.get_channel(channel_id)
            if not channel:
                return "Wtf, no existe"
            await channel.send(content)  # Enviar el mensaje al canal
            return f"Mensaje enviado a {channel.name}"
        except Exception as e:
            return f"Error al enviar el mensaje: {e}"
