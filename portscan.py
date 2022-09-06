import discord
import aiohttp
import datetime
import typing

from discord import commands, app_commands, Interaction, Embed
from typing import Optional

#a portscan command made by xTridentSecurityx | discord: La Kitty#1280
class portscan(commands.GroupCog, name = 'portscan',  description = 'scan for command ports or scan a custom port of an IP Address or URL'):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="portscan", description = "Portscan an IP Address or Website!")
    @app_commands.describe(host = 'IP Address or Website', port = 'The port to scan')
    #makes sure the bot has the permission to send messages.
    @app_commands.checks.bot_has_permissions(send_messages = True)
    #30 second cooldown.
    @app_commands.checks.cooldown(1, 30, key=lambda i: (i.guild_id, i.user.id))
    async def portscan(self, interaction: Interaction, host: str, port: Optional[int] = None):
        if port == None:
            #waits until its ready.
            await interaction.response.defer()
            async with aiohttp.ClientSession() as session:
                #replace [YOUR-FREE-API-KEY-HERE] with your webresolver api key.
                async with session.get(f'https://webresolver.nl/api.php?key=YOUR-FREE-API-KEY-HERE&action=portscan&string={host}') as r:
                    res = await r.read()
            embed = Embed(color = discord.Color.blurple(), timestamp = datetime.now())
            embed.add_field(
                name = f"Open Ports For {host}",
                value = f"{res}".replace("<br>", "\n", 13).replace("closed", "***CLOSED***", 13).replace("open", "**__OPEN__**", 13).replace("Port 3306 (unknown)", "Port 3306 (mysql)", 13).replace("Port 5900 (unknown)", "Port 5900 (vnc)", 13).replace("Port", " ", 13).replace("8080 (unknown)", "8080 (localhost)", 13).replace("b'", "", 13).replace("'", "", 13)
            )
            embed.set_author(name = f"{interaction.user}", icon_url=f"{interaction.user.avatar}")
            await interaction.followup.send(embed = embed)
            #closes the session after its been sent.
            await session.close()
        else:
            #waits until its ready.
            await interaction.response.defer()
            async with aiohttp.ClientSession() as custom:
                #replace [YOUR-FREE-API-KEY-HERE] with your webresolver api key.
                async with custom.get(f'https://webresolver.nl/api.php?key=YOUR-FREE-API-KEY-HERE&action=portscan&string={host}&port={port}') as r:
                    res = await r.read()
            embed = Embed(color = discord.Color.blurple(), timestamp = datetime.now())
            embed.add_field(
                name=f"Open Ports For {host}",
                value=f"{res}".replace("b'", "", 2).replace("<br>'", "", 2)
            )
            embed.set_author(name = f"{interaction.user}", icon_url = f"{interaction.user.avatar}")
            await interaction.followup.send(embed = embed)
            #closes the session after its been sent.
            await custom.close()

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(portscan(bot))
