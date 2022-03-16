import os
import discord_slash.utils.manage_commands
import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
import json

client_discord = commands.Bot(command_prefix='=')
slash = SlashCommand(client_discord, sync_commands=True)
guild = discord.Guild

if not 'Config.txt' in os.listdir():
    open('Config.txt', 'w', encoding='utf-8').write('{"Delete_Time":1, "Delete_Time_Shop_Cooldown":15, "guild_id":, "token":"", "owner_token":[""]}')
if not 'database' in os.listdir():
    os.mkdir('database')

print('loading Config')
try:
    config = json.loads(open('Config.txt', 'r').read())
    delete_time = int(config['Delete_Time'])
    delete_time_cooldown = int(config['Delete_Time_Shop_Cooldown'])
    guild_id = int(config['guild_id'])
    token = config['token']
except:
    print('Please add correct value in config')
    input()
    exit()
print(f'done.Bot running')

@slash.slash(
    name='everyone',
    description='Only for shop slot',
    guild_ids=[guild_id]
)
async def _everyone(ctx=SlashContext):
    await ctx.send('Give a Moment To Check Cooldown :)', delete_after=delete_time)
    allowed_mentions = discord.AllowedMentions(everyone = True)
    channel_id = ctx.channel.id
    if not f'{channel_id}.txt' in os.listdir('database'):
        await ctx.channel.send('this shop not in database')
    else:
        info_raw = open(f'database/{channel_id}.txt', 'r', encoding='utf-8').readlines()
        deadline = str(info_raw[0].strip('\n'))
        cooldown = str(info_raw[1].strip('\n'))
        today = date.today()
        timenow = datetime.now()
        current_time = str(today) + " " + str(timenow.strftime("%H:%M:%S"))
        start = datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S')
        ends = datetime.strptime(deadline, '%Y/%m/%d/%H/%M/%S')
        diff = relativedelta(ends, start)
        time_left = (str(diff.days) + " days "
                     + str(diff.hours) + " hours "
                     + str(diff.minutes) + " minutes "
                     + str(diff.seconds) + " seconds "
                     )
        if '-' in time_left:
            new_time = datetime.now() + timedelta(hours=int(cooldown))
            open(f'database/{channel_id}.txt', 'w', encoding='utf-8').write(
                f'{str(new_time.strftime("%Y/%m/%d/%H/%M/%S"))}\n{cooldown}')
            await ctx.channel.send(content = "@everyone", allowed_mentions = allowed_mentions, delete_after=delete_time)
        else:
            embed = discord.Embed(title='Mention Cooldown', description='', color=discord.Colour.red())
            embed.add_field(name='Time Left', value=(f'{time_left}'), inline=False)
            await ctx.channel.send(embed=embed, delete_after=delete_time_cooldown)

@slash.slash(
    name='makeshop',
    description='make shop',
    guild_ids=[guild_id],
    options=[
        discord_slash.utils.manage_commands.create_option(
            name='channel_id',
            description='channel id',
            required=True,
            option_type=3
        ),
        discord_slash.utils.manage_commands.create_option(
            name='cooldown',
            description='cooldown in hour',
            required=True,
            option_type=3
        ),
    ]
)
async def _makeshop(ctx=SlashContext, channel_id=str, cooldown=str):
    if not str(ctx.author.id) in json.loads(open('Configs.txt', 'r').read())['owner_token']:
        await ctx.send('Only Founder Allowed To Make A shop')
    else:
        open(f'database/{channel_id}.txt', 'w', encoding='utf-8').write(f'{str(datetime.now().strftime("%Y/%m/%d/%H/%M/%S"))}\n{cooldown}')
        await ctx.send('Created a record for the shop.Done')

@slash.slash(
    name='shopinfo',
    description='make shop',
    guild_ids=[guild_id],
    options=[
        discord_slash.utils.manage_commands.create_option(
            name='channel_id',
            description='channel id',
            required=True,
            option_type=3
        )
    ]
)
async def _shopinfo(ctx=SlashContext, channel_id=str):
    if f'{str(channel_id)}.txt' in os.listdir('database'):
        info_raw = open(f'database/{channel_id}.txt', 'r', encoding='utf-8').readlines()
        deadline = str(info_raw[0].strip('\n'))
        cooldown = str(info_raw[1].strip('\n'))
        today = date.today()
        timenow = datetime.now()
        current_time = str(today) + " " + str(timenow.strftime("%H:%M:%S"))
        start = datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S')
        ends = datetime.strptime(deadline, '%Y/%m/%d/%H/%M/%S')
        diff = relativedelta(ends, start)
        time_left = (str(diff.days) + " days "
                     + str(diff.hours) + " hours "
                     + str(diff.minutes) + " minutes "
                     + str(diff.seconds) + " seconds "
                     )
        
        embed = discord.Embed(title='Shop Info', description='', color=discord.Colour.green())
        embed.add_field(name='Channel Id', value=(channel_id), inline=False)
        embed.add_field(name='Next Mention', value=(f'{time_left}'), inline=False)
        await ctx.send(embed=embed)
    else:
        await ctx.send('cant find the shop in database')
    
    


client_discord.run(
    token
)
