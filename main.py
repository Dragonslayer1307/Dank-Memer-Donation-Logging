import discord
from discord.ext import commands
import json

bot = commands.Bot(command_prefix=("!"))

@bot.command()
async def myd(ctx, member : discord.Member=None):
    member = member or ctx.author
    await open_account(member)
    users = await get_dono_data()
    g_amt = users[str(member.id)]["gd"]
    h_amt = users[str(member.id)]["hd"]
    embed = discord.Embed(title = f"{member}'s Donation Logs",colour=discord.Colour.green())
    embed.add_field(name='Giveaway Donations', value= g_amt, inline=False)
    embed.add_field(name='Heist Donations', value= h_amt, inline=False)
    await ctx.channel.send(embed=embed)
    
@bot.command()
@commands.guild_only()
@commands.has_permissions(manage_guild=True)
async def gadd(ctx, member : discord.Member, amt:int):
    """Adds giveaway donations for a particular user."""
    await open_account(member)
    user = member
    users = await get_dono_data()
    amt1 = amt
    users[str(user.id)]["gd"] += amt1
    with open("dono.json",'w') as f:
        json.dump(users,f)
    await ctx.send(f"Added {amt} to {member}'s giveaway donations")
    
@bot.command()
@commands.guild_only()
@commands.has_permissions(manage_guild=True)
async def hadd(ctx, member : discord.Member, amt:int):
    """Adds heist donations for a particular user."""
    await open_account(member)
    user = member
    users = await get_dono_data()
    amt1 = amt
    users[str(user.id)]["hd"] += amt1
    with open("dono.json",'w') as f:
        json.dump(users,f)
    await ctx.send(f"Added {amt} to {member}'s heist donations")


async def open_account(user):
    users = await get_dono_data()
    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["gd"] = 0
        users[str(user.id)]["hd"] = 0
    with open('dono.json','w') as f:
        json.dump(users,f)
    return True

async def get_dono_data():
    with open('dono.json','r') as f:
        users = json.load(f)
    return users

async def update_bank(user,change=0,mode = 'gd'):
    users = await get_dono_data()
    users[str(user.id)][mode] += change
    with open('dono.json','w') as f:
        json.dump(users,f)
    bal = users[str(user.id)]['gd'],users[str(user.id)]['hd']
    return bal     
  
bot.run("token") 
