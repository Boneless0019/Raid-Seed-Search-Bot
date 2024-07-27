import discord
from discord.ext import commands
import json
import os
import random
from asyncio import TimeoutError
from discord.enums import StickerFormatType
from math import ceil

# Get the directory of the bot script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(BASE_DIR, 'images')
SHINY_IMAGES_DIR = os.path.join(IMAGES_DIR, 'shiny')
REGULAR_IMAGES_DIR = os.path.join(IMAGES_DIR, 'regular')

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

# Custom emojis for Tera Types (replace with actual emoji IDs from your server)
tera_emojis = {
    'Poison': '<:poison:id>',
    'Flying': '<:flying:id>',
    'Electric': '<:electric:id>',
    'Fire': '<:fire:id>',
    'Water': '<:water:id>',
    'Grass': '<:grass:id>',
    'Ice': '<:ice:id>',
    'Fighting': '<:fighting:id>',
    'Psychic': '<:psychic:id>',
    'Dark': '<:dark:id>',
    'Rock': '<:rock:id>',
    'Ghost': '<:ghost:id>',
    'Dragon': '<:dragon:id>',
    'Steel': '<:steel:id>',
    'Bug': '<:bug:id>',
    'Ground': '<:ground:id>',
    'Normal': '<:normal:id>',
    'Fairy': '<:fairy:id>'
}

tera_colors = {
    'Poison': 0xa040a0, 'Flying': 0xa890f0, 'Electric': 0xf8d030, 'Fire': 0xf08030, 'Water': 0x6890f0,
    'Grass': 0x78c850, 'Ice': 0x98d8d8, 'Fighting': 0xc03028, 'Psychic': 0xf85888, 'Dark': 0x705848,
    'Rock': 0xb8a038, 'Ghost': 0x705898, 'Dragon': 0x7038f8, 'Steel': 0xb8b8d0, 'Fairy': 0xee99ac
}

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

async def notify_user(ctx, command_name):
    try:
        notification_embed = discord.Embed(title="Check Your DMs", description=f"The results for the `{command_name}` command have been sent to your DMs.", color=discord.Color.blue())
        await ctx.send(embed=notification_embed)
    except discord.Forbidden:
        await ctx.send(f"{ctx.author.mention}, I couldn't send you a DM. Please enable DMs from server members.")

@bot.command()
async def help(ctx):
    help_embed = discord.Embed(title="Bot Commands", description="Here are the available commands:", color=discord.Color.blue())
    help_embed.add_field(name="!search", value="Starts the Pokémon search process. You will be guided through selecting a game, file, and specifying search criteria.", inline=False)
    help_embed.add_field(name="!rewards", value="Lists all available rewards in the selected game and file, and shows raids with the selected reward.", inline=False)
    help_embed.add_field(name="!randomshiny", value="Selects a random shiny raid from the selected game and file.", inline=False)
    help_embed.add_field(name="!invite", value="Provides an invite link to add the bot to another server.", inline=False)
    await ctx.send(embed=help_embed)

@bot.command()
async def info(ctx):
    info_embed = discord.Embed(title="Welcome to Rotom's Seed Search!", description="## How-To\n- There are multiple commands you can use to search for seeds:", color=discord.Color.blue())
    info_embed.add_field(name="!rewards", value="- The Bot will DM you asking for the game, Map, and 'Reward' type then display a browsable embed for you to look through the matching seeds.", inline=False)
    info_embed.add_field(name="!search", value="- The Bot will DM you asking for the game, Map, and 'Pokémon' name then display a browsable embed for you to look through the matching seeds.", inline=False)
    info_embed.add_field(name="!randomshiny", value="- The Bot will DM you asking for the game and Map, then display a random shiny Pokémon seed.", inline=False)
    info_embed.add_field(name="GitHub Repository", value="[Source Code](https://github.com/your-repo-url)", inline=False)
    await ctx.send(embed=info_embed)

@bot.command()
async def invite(ctx):
    permissions = discord.Permissions(permissions=322624)
    invite_link = discord.utils.oauth_url(bot.user.id, permissions=permissions)
    invite_embed = discord.Embed(title="Invite Me!", description=f"Click [here]({invite_link}) to invite me to your server!", color=discord.Color.green())
    await ctx.send(embed=invite_embed)

@bot.command()
async def search(ctx):
    await notify_user(ctx, 'search')
    await game_and_map_selection(ctx, search_command)

@bot.command()
async def rewards(ctx):
    await notify_user(ctx, 'rewards')
    await game_and_map_selection(ctx, rewards_command)

@bot.command()
async def randomshiny(ctx):
    await notify_user(ctx, 'randomshiny')
    await game_and_map_selection(ctx, random_shiny_command)

async def game_and_map_selection(ctx, callback):
    # Initial game selection
    games = ['Scarlet', 'Violet']
    game_emojis = ['🔴', '🟣']
    game_embed = discord.Embed(title="**Choose the Game**", description="🔴 - Scarlet\n🟣 - Violet", color=discord.Color.blue())
    game_message = await ctx.author.send(embed=game_embed)
    for emoji in game_emojis:
        await game_message.add_reaction(emoji)
    
    def check_game(reaction, user):
        return user == ctx.author and reaction.message.id == game_message.id and str(reaction.emoji) in game_emojis
    
    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check_game)
    except TimeoutError:
        await ctx.author.send("Timed out waiting for a reaction.")
        return

    game = games[game_emojis.index(str(reaction.emoji))]
    game_path = os.path.join(BASE_DIR, game)

    # Map selection
    maps = {
        "Paldea": "paldea.json",
        "Kitakami": "kitakami.json",
        "Blueberry": "blueberry.json"
    }
    map_emojis = ['🗺️', '🏞️', '🏫']
    map_embed = discord.Embed(title="**Choose the Map**", description="🗺️ - Paldea\n🏞️ - Kitakami\n🏫 - Blueberry", color=discord.Color.green())
    map_message = await ctx.author.send(embed=map_embed)
    for emoji in map_emojis:
        await map_message.add_reaction(emoji)

    def check_map(reaction, user):
        return user == ctx.author and reaction.message.id == map_message.id and str(reaction.emoji) in map_emojis

    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check_map)
    except TimeoutError:
        await ctx.author.send("Timed out waiting for a reaction.")
        return

    map_choice = ["Paldea", "Kitakami", "Blueberry"][map_emojis.index(str(reaction.emoji))]
    file_name = maps[map_choice]
    with open(os.path.join(game_path, file_name), 'r') as file:
        pokemons = json.load(file)
    
    await callback(ctx, pokemons)

async def search_command(ctx, pokemons):
    # Query for Pokémon name
    query_embed = discord.Embed(title="**Enter Pokémon Name**", description="Type the name of the Pokémon you're searching for:", color=discord.Color.orange())
    await ctx.author.send(embed=query_embed)
    msg = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
    query = msg.content.lower()

    # Filter Pokémon by name
    matched_pokemon = [pokemon for pokemon in pokemons if query in pokemon['Pokemon'].lower()]
    if not matched_pokemon:
        no_pokemon_embed = discord.Embed(title="No Pokémon Found", description="No Pokémon found with that name.", color=discord.Color.red())
        await ctx.author.send(embed=no_pokemon_embed)
        return

    # Choose Tera Type
    tera_types = sorted(set(pokemon['Tera'] for pokemon in matched_pokemon))
    tera_embed = discord.Embed(title="**Choose Tera Type**", description="Available Tera Types:\n" + "\n".join(f"{tera_emojis.get(t, '')} {t}" for t in tera_types), color=discord.Color.gold())
    await ctx.author.send(embed=tera_embed)
    tera_msg = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
    tera_type = tera_msg.content.lower()

    # Choose Shiny status with emojis
    shiny_embed = discord.Embed(title="**Is it Shiny?**", description="React with ✅ for Shiny, ❌ for not Shiny, or ⏺️ for no preference:", color=discord.Color.gold())
    shiny_message = await ctx.author.send(embed=shiny_embed)
    shiny_emojis = ['✅', '❌', '⏺️']
    for emoji in shiny_emojis:
        await shiny_message.add_reaction(emoji)
    
    def check_shiny(reaction, user):
        return user == ctx.author and reaction.message.id == shiny_message.id and str(reaction.emoji) in shiny_emojis
    
    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check_shiny)
    except TimeoutError:
        await ctx.author.send("Timed out waiting for a reaction.")
        return

    shiny_preference = 'any'
    if str(reaction.emoji) == '✅':
        shiny_preference = 'yes'
    elif str(reaction.emoji) == '❌':
        shiny_preference = 'no'

    # Final filtering
    final_results = [p for p in matched_pokemon if (tera_type == 'any' or p['Tera'].lower() == tera_type) and (shiny_preference == 'any' or p['IsShiny'].lower() == shiny_preference)]
    if not final_results:
        no_match_embed = discord.Embed(title="No Matches Found", description="No Pokémon match the specified criteria.", color=discord.Color.red())
        await ctx.author.send(embed=no_match_embed)
        return
    
    await display_results(ctx, final_results)

async def rewards_command(ctx, pokemons):
    # List rewards
    rewards = sorted(set(pokemon['Rewards'] for pokemon in pokemons))
    rewards_embed = discord.Embed(title="**Choose the Reward**", description="Available Rewards:\n" + "\n".join(rewards), color=discord.Color.gold())
    await ctx.author.send(embed=rewards_embed)
    rewards_msg = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
    chosen_reward = rewards_msg.content

    # Filter Pokémon by reward
    reward_pokemon = [pokemon for pokemon in pokemons if chosen_reward.lower() in pokemon['Rewards'].lower()]
    if not reward_pokemon:
        no_reward_embed = discord.Embed(title="No Pokémon Found", description="No Pokémon found with that reward.", color=discord.Color.red())
        await ctx.author.send(embed=no_reward_embed)
        return
    
    await display_results(ctx, reward_pokemon)

async def random_shiny_command(ctx, pokemons):
    async def send_random_shiny():
        # Select a random shiny Pokémon
        selected_pokemon = random.choice([pokemon for pokemon in pokemons if pokemon['IsShiny'].lower() == 'yes'])
        
        color = tera_colors.get(selected_pokemon['Tera'], 0x78c850)
        detail_embed = discord.Embed(
            title=f"**{selected_pokemon['Pokemon']} Details**",
            description=f"Seed: `{selected_pokemon['Seed']}`\nRewards: `{selected_pokemon['Rewards']}`",
            color=color
        )
        
        # Determine the correct image directory based on "Shiny" status
        image_path = os.path.join(
            SHINY_IMAGES_DIR if selected_pokemon['IsShiny'].lower() == 'yes' else REGULAR_IMAGES_DIR,
            f"{sanitize_pokemon_name(selected_pokemon['Pokemon'])}.png"
        )
        
        if os.path.exists(image_path):
            detail_embed.set_thumbnail(url=f"attachment://{os.path.basename(image_path)}")
        
        detail_embed.set_footer(text="React with ✅ to generate a raid request command. React with 🔄 to reroll.")
        return detail_embed, image_path

    embed, image_path = await send_random_shiny()
    message = await ctx.author.send(embed=embed, file=discord.File(image_path) if os.path.exists(image_path) else None)
    await message.add_reaction('✅')
    await message.add_reaction('🔄')

    def check_reaction(reaction, user):
        return user == ctx.author and reaction.message.id == message.id and str(reaction.emoji) in ['✅', '🔄']

    while True:
        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check_reaction)
            if str(reaction.emoji) == '✅':
                raid_command = f".ra {embed.description.split('`')[1]} {5}"  # Adjust the command string if needed
                await ctx.author.send(f"Raid request command: `{raid_command}`")
                reminder_embed = discord.Embed(
                    title="Reminder",
                    description="Please add the correct bot prefix before the `ra` command.",
                    color=discord.Color.orange()
                )
                await ctx.author.send(embed=reminder_embed)
            elif str(reaction.emoji) == '🔄':
                embed, image_path = await send_random_shiny()
                await message.edit(embed=embed, attachments=[discord.File(image_path)] if os.path.exists(image_path) else [])
        except TimeoutError:
            break

def sanitize_pokemon_name(pokemon_name):
    return pokemon_name.lower().replace(' ', '_').replace('(', '').replace(')', '').replace('.', '').replace('♀', 'f').replace('♂', 'm')

async def display_results(ctx, results):
    # Prepare embeds and image paths
    embeds = []
    image_paths = []
    for i, pokemon in enumerate(results):
        color = tera_colors.get(pokemon['Tera'], 0x78c850)
        detail_embed = discord.Embed(
            title=f"**{pokemon['Pokemon']} Details**",
            description=f"Page {i + 1} of {len(results)}",
            color=color
        )
        
        # Determine the correct image directory based on "Shiny" status
        image_path = os.path.join(
            SHINY_IMAGES_DIR if pokemon['IsShiny'].lower() == 'yes' else REGULAR_IMAGES_DIR,
            f"{sanitize_pokemon_name(pokemon['Pokemon'])}.png"
        )
        image_paths.append(image_path)

        if os.path.exists(image_path):
            detail_embed.set_thumbnail(url=f"attachment://{os.path.basename(image_path)}")

        # Add fields to the embed
        detail_embed.add_field(name="Stats", value="\n".join(f"{stat}: `{pokemon[stat]}`" for stat in ['HP', 'Atk', 'Def', 'SpA', 'SpD', 'Spe']), inline=False)
        detail_embed.add_field(name="General Info", value="\n".join(f"{info}: `{pokemon[info]}`" for info in ['Ability', 'Nature', 'Gender', 'Tera']), inline=False)
        detail_embed.add_field(name="Physical Attributes", value="\n".join(f"{attr}: `{pokemon[attr]}`" for attr in ['Height', 'Weight', 'Scale']), inline=False)
        detail_embed.add_field(name="Pokemon", value=f"`{pokemon['Pokemon']}`", inline=True)
        detail_embed.add_field(name="Is Shiny?", value=f"`{pokemon['IsShiny']}`", inline=True)
        detail_embed.add_field(name="Seed", value=f"`{pokemon['Seed']}`", inline=False)
        detail_embed.add_field(name="Rewards", value=f"`{pokemon['Rewards']}`", inline=False)
        detail_embed.add_field(name="Difficulty", value=f"`{pokemon['Difficulty']}`", inline=True)
        detail_embed.set_footer(text="React with ✅ to generate a raid request command.")
        embeds.append(detail_embed)

    # Send the initial embed and manage pagination
    current_page = 0
    message = await ctx.author.send(embed=embeds[current_page], file=discord.File(image_paths[current_page]) if os.path.exists(image_paths[current_page]) else None)
    await message.add_reaction('◀️')
    await message.add_reaction('▶️')
    await message.add_reaction('⏩')
    await message.add_reaction('✅')

    # Handle pagination
    def check_reaction(reaction, user):
        return user == ctx.author and reaction.message.id == message.id and str(reaction.emoji) in ['◀️', '▶️', '⏩', '✅']

    while True:
        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check_reaction)
            if str(reaction.emoji) in ['◀️', '▶️', '⏩']:
                if str(reaction.emoji) == '▶️' and current_page < len(embeds) - 1:
                    current_page += 1
                elif str(reaction.emoji) == '◀️' and current_page > 0:
                    current_page -= 1
                elif str(reaction.emoji) == '⏩':
                    current_page = min(current_page + ceil(len(embeds) * 0.2), len(embeds) - 1)

                if os.path.exists(image_paths[current_page]):
                    file = discord.File(image_paths[current_page])
                    await message.edit(embed=embeds[current_page], attachments=[file])
                else:
                    await message.edit(embed=embeds[current_page])
                    
            elif str(reaction.emoji) == '✅':
                pokemon = results[current_page]
                story_progress = 3 if pokemon['Rewards'] in ['1 Star Shiny', '2 Star Shiny', '3 Star Shiny'] else 5
                raid_command = f"$ra {pokemon['Seed']} {pokemon['Difficulty']} {story_progress}"
                await ctx.author.send(f"Raid request command: `{raid_command}`")
                reminder_embed = discord.Embed(
                    title="Reminder",
                    description="Please add the correct bot prefix before the `ra` command.",
                    color=discord.Color.orange()
                )
                await ctx.author.send(embed=reminder_embed)

        except TimeoutError:
            break
# Replace 'your_token_here' with your bot's token
bot.run('your_token_here')