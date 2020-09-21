import discord

from discord.ext import commands
from discord.utils import get
from mcrcon import MCRcon, MCRconException


def channel_check():
    async def checker(ctx):
        if ctx.message.channel.id == ctx.cog.config['commands_channel_id']:
            return True
    return commands.check(checker)

def config_check():
    async def checker(ctx):
        async def roles_check(ctx):
            for role in ctx.cog.config['allowed_roles']:
                check_role = get(ctx.guild.roles, name=role)
                if check_role in ctx.author.roles:
                    return True
                else:
                    continue
        role_check = (await roles_check(ctx))
        if (role_check == True)\
            and ctx.cog.config["server_ip"] != None\
                and ctx.cog.config["rcon_port"] != None\
                    and ctx.cog.config["rcon_password"] != None:
            return True
    return commands.check(checker)

def parseReturned(returned):
  for k, v in enumerate(returned):
    if v == "§":
      returned = returned.replace(returned[k+1], "")
  return returned.replace("§", "")

class discordMinecraft(commands.Cog):

    '''
    Simple extension allowing you to access your Minecraft server's console through a discord channel using the command [p]console
    '''

    __author__ = "Raff"
    __version__ = "1.0"


    def __init__(self, bot):
        self.bot = bot
        self.config = {
            # put the IP to your server here
            "server_ip": "play.bd-craft.com",

            # put the RCON port for your server here (this can be found/set in your server.properties file)
            "rcon_port": 8084,

            # put the RCON password for your server here (this can be found/set in your server.properties file)
            "rcon_password": "secret123",

            # put the ID of the channel you wish to send commands in here
            "commands_channel_id": 686707809835941902,

            # put the names of all roles you wish to be able to execute commands here (capitalisation matters)
            "allowed_roles": ['ExampleRole', 'Example Role', 'example role']
        }

        
    @commands.command(
        name='console',
        description='Send commands to your minecraft console',
        aliases=['c'],
        usage='!console <command> [values]')
    @channel_check()
    @config_check()
    async def minecraft_console(self, ctx, command: str, *, values=None):
        await ctx.message.channel.trigger_typing()
        try:
            with MCRcon(str(self.config['server_ip']),str(self.config['rcon_password']),int(self.config['rcon_port'])) as mcr:
                if values != None:
                    returned = mcr.command(f"{command} {values}")
                    returnembed = discord.Embed(
                        title=f"Executed Command: `/{command} {values}`",
                        color=0x35fc03
                    )
                    if returned != "":
                        returnembed.add_field(
                            name="Returned",
                            value=f"```{returned}```"
                        )
                    else:
                        returnembed.add_field(
                            name="Returned",
                            value=f"```nothing```"
                        )
                    returnembed.set_footer(
                        text="Discord -> Minecraft (https://github.com/fwiko)"
                    )
                    await ctx.send(embed=returnembed)
                else:
                    returned = mcr.command(f"{command}")
                    returnembed = discord.Embed(
                        title=f"Executed Command: `/{command}`",
                        color=0x35fc03
                    )
                    if returned != "":
                        returnembed.add_field(
                            name="Returned",
                            value=f"```{returned}```"
                        )
                    else:
                        returnembed.add_field(
                            name="Returned",
                            value=f"```nothing```"
                        )
                    returnembed.set_footer(
                        text="Discord -> Minecraft (https://github.com/fwiko)"
                    )
                    await ctx.send(embed=returnembed)
        except (ConnectionRefusedError, TimeoutError, MCRconException) as error:
            embed = discord.Embed(
                title="Execution failed",
                description="The connection to the server failed. This may be due to:\n\n**• incorrect rcon password in config**\n**• incorrect rcon port in config**\n**• incorrect server IP in config**\n**• the server is down/restarting**",
                color=0xfc3503
            )
            embed.add_field(
                name="Error",
                value=f"```{error}```"
            )
            await ctx.send(embed=embed)
        finally:
            pass

def setup(bot):
    bot.add_cog(discordMinecraft(bot))
