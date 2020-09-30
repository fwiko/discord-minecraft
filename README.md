# discord-minecraft
A discord.py extension allowing you to easily communicate with your Minecraft server's console through discord with no server-side dependencies. 


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

`Config.json`

```
{
    # put the IP to your server here
    "server_ip": "0.0.0.0",

    # put the RCON port for your server here (this can be found/set in your server.properties file)
    "rcon_port": 8000,

    # put the RCON password for your server here (this can be found/set in your server.properties file)
    "rcon_password": "supersecretpassword123",

    # put the ID of the channel you wish to send commands in here
    "commands_channel_id": 1234567890123456789,

    # put the names of all roles you wish to be able to execute commands here
    "allowed_roles": ['ExampleRole', 'Example Role', 'example role', 708133151653888112]
}
```
Fill in all necessary information if the self.config dict within the extension. (These values are now found in the Config.json file)

### General use

Once setup in your guild you will be able to communicate with your servers console by doing the following:
```
[p]console <command> [arguments] | (e.g. !console kick <player>)
```

### Other Commands

- Change the server IP in the config `[p]dmc serverip <server_ip>`
- Change the RCON Port in the config `[p]dmc rconport <rcon_port>`
- Change the RCON Password in the config `[p]dmc rconpassword <rcon_password>`
- Change the Commands Channel ID in the config `[p]dmc commandchannel <channel_id>`

- Return Cog info `[p]dmc info`

## Preview/Examples

# Successfully Executed Commands

![github-small](https://raffsimms.com/files/Discord-0889.png)

# Command Execution Failed

![github-small](https://raffsimms.com/files/Discord-0888.png)

## RedBot Version

Coming Soon

