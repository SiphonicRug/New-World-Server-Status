import config
import requests
from bs4 import BeautifulSoup

import discord
from discord.ext import commands

from datetime import datetime

zones_array = ['US EAST', 'SA EAST', 'EU CENTRAL', 'AP SOUTHEAST', 'US WEST']

zones_arr = {}
ts = 0

bot = commands.Bot(command_prefix='$')

async def multiprint(ctx, text):
        i = 0
        tText = []
        pText = ""
        tOffset = 0
        for c in text:
                pText += c
                i+=1
                lastPos = text.find('\n',i)
                if i == 2000 or (c=='\n' and lastPos > 2000):
                        tText.append(pText)
                        i = 0
                        tOffset += 2000
                        pText = ""
        if pText != "":
                tText.append(pText)

        for t in tText:
                await ctx.send(t)

#gets all the zones
@bot.command()
async def zones(ctx):
        text = ""
        for x in zones_array:
                text += x.title() + '\r\n'
        await multiprint(ctx, text)

#gets all the servers
@bot.command()
async def all(ctx):
        arr = server_scrape()
        text = ""
        for x in arr.keys():
                text += x.title() + "\r\n"
                for server in arr[x]:
                        text += '\t' + server["name"] + ": " + server["status"] + " " + config.emoji_status[server["status"]] + "\r\n"

        await multiprint(ctx, text)
	
#gets specific server
@bot.command()
async def server(ctx, *,arg):
        temp_arr = server_scrape()
        temp_arr = [[x for x in v if x['name'].upper() == arg.upper()] for v in temp_arr.values()]
        temp_arr = [x for x in temp_arr if x]
        if temp_arr:
                temp_arr = temp_arr[0][0]
                text = temp_arr["name"] + ': ' + temp_arr["status"] + " " + config.emoji_status[temp_arr["status"]]
        else:
                text = "No server found!"

        await multiprint(ctx,text)

#gets specific zone servers
@bot.command()
async def zone(ctx, *,arg):
        arr = server_scrape()
        text = ""
        print("Requested zone: " + arg)
        arg = arg.upper()
        if arg in arr.keys():
                for server in arr[arg]:
                        text += server["name"] + ": " + server["status"] + " " + config.emoji_status[server["status"]] + "\r\n"
        else:
                text = "No zone found!"

        await multiprint(ctx,text)

def server_scrape():
        global zones_arr
        global ts

        if datetime.timestamp(datetime.now()) - ts < (5 * 60 * 1000):
                return zones_arr

        zone_class = "ags-ServerStatus-content-responses-response"
        server_class = zone_class + "-server"
        server_name_class = server_class + "-name"
        server_status_class = server_class + "-status"

        URL = "https://www.newworld.com/it-it/support/server-status"
        page = requests.get(URL)

        soup = BeautifulSoup(page.content, "html.parser")
        zones = soup.find_all("div", class_=zone_class)
        zones_arr = {}

        for zone in zones:
                servers = zone.find_all("div", class_=server_class)
                servers_arr = []
                for server in servers:
                        name = server.find("div", class_=server_name_class)
                        status = server.find("div", class_=server_status_class)
                        server_status = ""
                        server_obj = {}
                        if ((server_status_class + "--up") in status.attrs.get("class")):
                                server_status = "Up"
                        if ((server_status_class + "--down") in status.attrs.get("class")):
                                server_status = "Down"
                        if ((server_status_class + "--full") in status.attrs.get("class")):
                                server_status = "Full"
                        if ((server_status_class + "--maintenance") in status.attrs.get("class")):
                                server_status = "Maintenance"
                        server_obj['name'] = name.text.replace("\n","").replace("\r","").replace(" ","")
                        server_obj['status'] = server_status
                        servers_arr.append(server_obj)
                zones_arr[(zones_array[int(zone.attrs.get('data-index'))])] = servers_arr

        ts = datetime.timestamp(datetime.now())
        return zones_arr

bot.run(config.key)
