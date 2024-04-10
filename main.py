import discord
from discord.ext import commands
import os

# Define a list of toxic words (you can add more words to this list)
toxic_words = ['kdor', 'kduy', 'jui', 'fuck', 'bitch', 'nigga', 'nigger', 'ass', 'juii']

# Define intents
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True

# Initialize the bot with the defined intents
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    # Set the bot's status to invisible (offline)
    await bot.change_presence(status=discord.Status.invisible)

@bot.event
async def on_message(message):
    # Ignore messages sent by the bot
    if message.author == bot.user:
        return

    # Check if the message contains any toxic word
    for toxic_word in toxic_words:
        if toxic_word in message.content.lower():
            # Delete the toxic message
            await message.delete()
            # Create an embed for the warning message
            warn_embed = discord.Embed(
                title="Warning",
                description=f"{message.author.mention}, please refrain from using toxic language!",
                color=discord.Color.red()
            )
            # Send the embed to the channel
            await message.channel.send(embed=warn_embed)
            # Create an embed for the notification message
            notify_embed = discord.Embed(
                title="Toxic Message Alert",
                description=f"A toxic message containing the word '{toxic_word}' was sent by {message.author.display_name} in {message.channel.name}.",
                color=discord.Color.gold()
            )
            # Send a notification to the server owner
            owner = message.guild.owner
            if owner:
                await owner.send(embed=notify_embed)
            break  # Stop checking after the first match

    # Process commands
    await bot.process_commands(message)

bot_token = os.getenv('TOKEN')

# Run the bot with the token
bot.run('TOKEN')
