# New World Server Status
Discord bot to know the status of the New World game server status

This bot is intented to only know the status of the servers of the various regions. I don't own any of the data provided by the bot, it is all obtained by scraping the support page of the official game here: https://www.newworld.com/en-us/support/server-status

The bot returns the status of each server according to the support page:

`Up ✅`: The server is on.

`Down ❌`: The server is down.

`Full ⛔`: The server is full and doesn't accept new player for now.

`Maintenance ⚠️`: The server is down for maintenance.

You can invite this bot with the following link:

[New World Server Status](https://discord.com/api/oauth2/authorize?client_id=898268933801525319&permissions=377957125120&scope=bot)

# Setup

This bot is written in python, and uses the following libraries:

[BeautifulSoap4](https://pypi.org/project/beautifulsoup4/)

[Discord.py](https://pypi.org/project/discord.py/)

[requests](https://pypi.org/project/requests/)

# Functions

The bot can filter by Zone and by Server, so you can get all the servers in a zone and a specific server. Remember that this bot is case unsensitive for the commands arguments, so you can write "US WEST" and "us west", it will be the same for it.

# Usage

`$zone [zone]` - gets all servers of the provided zone.

`$server [server]` - gets the provided server.

`$zones` - gets all the available zones.

`$all` - gets all servers divided by zone.

For full game info go to https://www.newworld.com/

Examples:

```
$zone US West

Aarnivalkea: Up ✅
Adlivun: Up ✅
Aeaea: Up✅
...
```
```
$server Atvatabar

Atvatabar: Full⛔
```
```
$zones

US West
AP Southeast
...
```
```
$all

Us East
    Aarnivalkea: Up ✅
    Adlivun: Up ✅
    Aeaea: Up ✅
...
```
