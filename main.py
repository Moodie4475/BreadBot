import os
import random

from discord import Embed, Game, Intents, Member, Message, Status, User
from discord.ext import commands, tasks
from replit import db as Database

from translate import get_command, get_sentence

intents = Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


# Deze calculatie was hell
def burn_chance(time: int):
    return min(0.1 + (time - 30) * 0.01, 0.9) if time > 30 else 0.1


async def check_bake_time(author: User | Member,
                          message: Message | None = None):

    user_id = str(author.id)

    # database check
    if user_id not in Database or Database[user_id]['bake_time'] is None:
        return

    new_bake_time = Database[user_id]['bake_time'] - 1
    if new_bake_time <= 0:
        if random.random() < burn_chance(
                Database[user_id]['bake_time_initial']):

            if message is not None:
                await message.reply(get_sentence("burned", author.mention))

            Database[user_id][
                'xp'] += Database[user_id]['bake_time_initial'] // 2
        else:
            if message is not None:
                await message.reply(get_sentence("baked", author.mention))

            Database[user_id]['bread_count'] += 1
            Database[user_id]['xp'] += Database[user_id]['bake_time_initial']

        Database[user_id]['bake_time'] = None
        Database[user_id]['bake_time_initial'] = None
    else:
        Database[user_id]['bake_time'] = new_bake_time


@bot.event
async def on_ready():
    print(f'Logged in als {bot.user}')
    check_bake_times.start()
    await bot.change_presence(status=Status.online,
                              activity=Game(get_sentence('bot_status')))


@bot.event
async def on_message(message):
    if message.author.bot:
        return

    await check_bake_time(message.author, message)

    await bot.process_commands(message)


@bot.command(name=get_command('bake'))
async def bake(ctx: commands.Context, time: int):
    if time <= 0:
        await ctx.reply(get_sentence('error_negative_time'))
        return

    user_id = str(ctx.author.id)
    if user_id not in Database:
        Database[user_id] = {'bread_count': 0, 'bake_time': time}
    else:
        Database[user_id]['bake_time'] = time

    await ctx.reply(get_sentence('started', ctx.author.mention, time))


@bot.command(name=get_command('leaderboard'))
async def leaderboard(ctx):
    leaderboard = sorted(
        ((user_id, data['bread_count'], data.get('xp', 0))
         for user_id, data in Database.items() if 'bread_count' in data),
        key=lambda x: (x[1], x[2]),
        reverse=True)

    newEmbed = Embed(title=get_sentence('leaderboard_message'))
    for user_id, bread_count, xp in leaderboard[:10]:
        user = await bot.fetch_user(int(user_id))
        if bread_count > 1:
            newEmbed.add_field(name=f"{user.name}: ",
                               value=get_sentence('leaderboard_multiple',
                                                  bread_count, xp),
                               inline=False)
        else:
            newEmbed.add_field(name=f"{user.name}: ",
                               value=get_sentence('leaderboard_single',
                                                  bread_count, xp),
                               inline=False)
    await ctx.reply(embed=newEmbed)


@bot.command(name=get_command('bread'))
async def bread(ctx):
    user_id = str(ctx.author.id)
    bread_count = Database[user_id].get('bread_count',
                                        0) if user_id in Database else 0
    if bread_count > 1:
        await ctx.reply(
            get_sentence('count_multiple', ctx.author.mention, bread_count))
    else:
        await ctx.reply(
            get_sentence('count_single', ctx.author.mention, bread_count))


@bot.command(name=get_command('status'))
async def status(ctx):
    user_id = str(ctx.author.id)
    if user_id in Database and 'bake_time' in Database[user_id] and Database[
            user_id]['bake_time'] is not None:
        await ctx.reply(
            get_sentence('status_baking', ctx.author.mention,
                         Database[user_id]['bake_time']))
    else:
        await ctx.reply(get_sentence('status_idle', ctx.author.mention))


@tasks.loop(minutes=1)
async def check_bake_times():
    for user_id in Database:
        if Database[user_id]['bake_time'] is None:
            continue

        new_bake_time = Database[user_id]['bake_time'] - 1
        if new_bake_time <= 0:
            author = await bot.fetch_user(int(user_id))
            channel = author.dm_channel or await author.create_dm()
            if random.random() < burn_chance(
                    Database[user_id]['bake_time_initial']):

                await channel.send(get_sentence("burned", author.mention))
                Database[user_id][
                    'xp'] += Database[user_id]['bake_time_initial'] // 2
            else:
                await channel.send(get_sentence("baked", author.mention))
                Database[user_id]['bread_count'] += 1
                Database[user_id]['xp'] += Database[user_id][
                    'bake_time_initial']

            Database[user_id]['bake_time'] = None
            Database[user_id]['bake_time_initial'] = None
        else:
            Database[user_id]['bake_time'] = new_bake_time


if os.environ.get('TOKEN') is None:
    raise Exception(
        "You need to set the TOKEN secret that you got from your discord bot!")

bot.run(os.environ['TOKEN'])
