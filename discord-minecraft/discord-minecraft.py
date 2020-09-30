import discord, json, datetime

from discord.ext import commands
from discord.utils import get
from mcrcon import MCRcon, MCRconException

def load_config():
    f = open('config.json', )
    return json.load(f)

def write_config(config):
    with ('config.json', 'w') as file:
        json.dump(config, file, indent=4)


def channel_check():
    async def checker(ctx):
        config = load_config()
        if ctx.message.channel.id == config['commands_channel_id']:
            return True
    return commands.check(checker)

def config_check():
    config = load_config()
    async def checker(ctx):
        async def roles_check(ctx):
            for role in config['allowed_roles']:
                if type(role) == str:
                    try:
                        check_role = get(ctx.guild.roles, name=role)
                    except Exception:
                        print(f"Discord-Minecraft > Role {role} does not exist.")
                    else:
                        if check_role in ctx.author.roles:
                            return True
                        else:
                            continue
                elif type(role) == int:
                    try:
                        check_role = get(ctx.guild.roles, id=role)
                    except Exception:
                        print(f"Discord-Minecraft > Role {role} does not exist.")
                    else:
                        if check_role in ctx.author.roles:
                            return True
                        else:
                            continue
                else:
                    pass
        role_check = (await roles_check(ctx))
        if (role_check == True)\
            and config["server_ip"] != None\
                and config["rcon_port"] != None\
                    and config["rcon_password"] != None:
            return True
    return commands.check(checker)

def parseReturned(returned):
  for k, v in enumerate(returned):
    if v == "§":
      returned = returned.replace(returned[k+1], "")
  return returned.replace("§", "")

class discordMinecraft(commands.Cog):

    '''
    Simple discord.py extension allowing you to access your Minecraft server's console through a discord channel using the command [p]console
    '''

    def __init__(self, bot):
        self.bot = bot
        self.author = "Raff Simms"
        self.version = "1.2.0"
        self.github = "https://github.com/fwiko/discord-minecraft"
        
    @commands.group()
    async def dmc(self, ctx):
        if ctx.invoked_subcommand is None:
            await bot.say(f'{ctx.invoked_subcommand} is not a valid subcommand')

    @dmc.command(name="serverip")
    @config_check()
    async def change_server_ip(self, ctx, serverip):
        config = load_config()
        config["server_ip"] = serverip
        try:
            write_config(config)
        except Exception as e:
            await ctx.send(f"Failed to change **Server IP**. ```{e}```")
        else:
            await ctx.send(f"Server IP changed to `{serverip}`")


    @dmc.command(name="rconport")
    @config_check()
    async def change_rcon_port(self, ctx, rcon_port):
        config = load_config()
        config["rcon_port"] = rcon_port
        try:
            write_config(config)
        except Exception as e:
            await ctx.send(f"Failed to change **RCON port**. ```{e}```")
        else:
            await ctx.send(f"RCON port changed to `{rcon_port}`")

    @dmc.command(name="rconpassword")
    @config_check()
    async def change_rcon_password(self, ctx, rcon_password):
        config = load_config()
        config["rcon_password"] = rcon_password
        try:
            write_config(config)
        except Exception as e:
            await ctx.send(f"Failed to change **RCON password**. ```{e}```")
        else:
            await ctx.send(f"RCON password changed to ||{rcon_password}||")

    @dmc.command(name="commandchannel")
    @config_check()
    async def change_commands_channel(self, ctx, channel: discord.TextChannel):
        config = load_config()
        config["commands_channel_id"] = channel.id
        try:
            write_config(config)
        except Exception as e:
            await ctx.send(f"Failed to change **Command channel ID**. ```{e}```")
        else:
            await ctx.send(f"Commands channel ID changed to `{commands_channel_id}`")

    @dmc.command(name="info")
    async def discord_minecraft_info(self, ctx):
        embed = discord.embed(
            color=0xb5feff,
            timestamp=datetime.datetime.utcnow()
        )
        embed.set_author(
            name=f"Discord > Minecraft (v{self.version})",
            icon_url="https://avatars0.githubusercontent.com/u/71665152?s=200&v=4"
        )
        embed.add_field(name="Author", value=self.author, inline=False)
        embed.add_field(name="Version", value=self.version, inline=False)
        embed.add_field(name="Github", value=f"[click here]({self.github})", inline=False)
        await ctx.send(embed=embed)

    @commands.command(name='console',description='Send commands to your minecraft console',aliases=['c'],usage='!console <command> [values]')
    @channel_check()
    @config_check()
    async def minecraft_console(self, ctx, command: str, *, values=None):
        await ctx.message.channel.trigger_typing()
        config = load_config()
        try:
            with MCRcon(str(config['server_ip']),str(config['rcon_password']),int(config['rcon_port'])) as mcr:
                if values != None:
                    returned = mcr.command(f"{command} {values}")
                    returnembed = discord.Embed(
                        title=f"Executed Command: `/{command} {values}`",
                        color=0x35fc03
                    )
                    if returned != "":
                        returnembed.add_field(
                            name="Returned",
                            value=f"```{parseReturned(returned)}```"
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
                            value=f"```{parseReturned(returned)}```"
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
