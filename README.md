# discord-minecraft
A discord.py extension allowing you to easily communicate with your Minecraft server's console through discord. 


## Getting Started

Once you have the discord-minecraft.py file in the correct place these instructions will help you when setting everything up

### Prerequisites

[discord.py](https://pypi.org/project/discord.py/) is required

```
pip install discord.py
```

[mcrcon](https://pypi.org/project/mcrcon/) is required

```
pip install mcrcon
```


## Setup

Once up an running and the above requirements are met. Follow these steps to get the cog/extension fully set up in your guild.

### Setting up to work with your server

```
self.config = {
            # put the IP to your server here
            "server_ip": "",

            # put the RCON port for your server here (this can be found/set in your server.properties file)
            "rcon_port": 0,

            # put the RCON password for your server here (this can be found/set in your server.properties file)
            "rcon_password": "",

            # put the ID of the channel you wish to send commands in here
            "commands_channel_id": 0,

            # put the names of all roles you wish to be able to execute commands here (capitalisation matters)
            "allowed_roles": ['ExampleRole', 'Example Role', 'example role']
        }
```
Fill in all necessary information if the self.config dict within the extension.

### General use

Once setup in your guild you will be able to communicate with your servers console by doing the following:
```
[p]console <command> [arguments] | (e.g. !console kick <player>)
```

## Preview/Examples

# Successfully Executed Commands

![github-small](https://raffsimms.com/files/Discord-0889.png)
![github-small](https://raffsimms.com/files/Discord-0890.png)

# Command Execution Failed

![github-small](https://raffsimms.com/files/Discord-0888.png)

