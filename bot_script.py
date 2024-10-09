import discord
from discord.ext import commands


#  ==================================================
# Required Intents for bot 
#  ==================================================
#
intents = discord.Intents.default()
intents.members = True
intents.reactions = True  
intents.guilds = True
intents.messages = True
intents.message_content = True 
intents.guild_messages = True

bot = commands.Bot(command_prefix='!', intents=intents)


#  ==================================================
#  LOGGING MESSAGE FUNCTION 
#  ==================================================
#
LOGGING_CHANNEL_ID = 1234 # Channel ID for logging messages
REPLYING_CHANNEL_ID = 1234 # Channel ID for replying to commands
COMMANDS_CHANNEL_ID = 1234 # Channel ID for bot commands

async def send_logs(buffer, channel_id):
    # Get the channel object by its ID
    logging_channel = bot.get_channel(channel_id)
    
    if logging_channel is None:
        print(f"Channel with ID {channel_id} not found.")
        return

    # Decode the buffer and send it as a message
    if isinstance(buffer, bytes):
        text_content = buffer.decode('utf-8') # Decode the byte buffer to string (assuming UTF-8)
    else:
        text_content = buffer  
    
    # Send the message to the channel
    await logging_channel.send(content=text_content)




#   ==================================================
#   FORM MEMBER CHECKING FUNCTION
#   ==================================================
#

FORM_CHANNEL = 1234 # Channel ID for the form submission

@bot.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return

    # Check if the message is from the specific channel
    elif message.channel.id == FORM_CHANNEL:
        log_buffer = "Bot Log\nCategory: Forms\nReason: Member Form Received"
        
        # Logging the message received
        try:
            send_logs(log_buffer, LOGGING_CHANNEL_ID)
        except Exception as e:
            print(f"Category: Error\nReason: Failed to log message reception.\nError: {str(e)}\nLine: 66")
            
        
        # React to the message with a ✅ emoji
        try:
            await message.add_reaction('✅')
        except Exception as e:
            error_log = f"Log\nCategory: Error\nReason: Failed to add reaction to the message.\nError: {str(e)}\nLine: 75"
            send_logs(error_log, LOGGING_CHANNEL_ID)
    
    elif message.channel.id == COMMANDS_CHANNEL_ID:
        await message.delete()

    # Allow other commands to work
    await bot.process_commands(message)




#   ==================================================
#   ROLE MANAGEMENT SECTION
#   ==================================================
#


MEMBER_MESSAGE_ID = 1234  
VOLUNTEER_MESSAGE_ID = 1234 # Maybe Depricated
SCIENTIFIC_MESSAGE_ID = 1234

@bot.event
async def on_raw_reaction_add(payload):
    # ---------------------------------------------------
    # Code to execute when a user want to become a member
    if payload.message_id == MEMBER_MESSAGE_ID:
        
        role_name = "Members"

        # Get the guild object
        guild = bot.get_guild(payload.guild_id)

        # Check if guild is found
        if guild is None:
            log_buffer = "Log\nCategory: Role Management\nReason: Guild not found\nLine: 109"
            await send_logs(log_buffer, LOGGING_CHANNEL_ID)
            return
        

        # Check if role_name is found
        if role_name is None:
            log_buffer = "Log\nCategory: Role Management\nReason: Role Name not found\nLine: 116"
            await send_logs(log_buffer, LOGGING_CHANNEL_ID)
            return

        # Get the role object
        role = discord.utils.get(guild.roles, name=role_name)

        # Check if role is found
        if role is None:
            log_buffer = "Log\nCategory: Role Management\nReason: Role not found\nLine: 125"
            await send_logs(log_buffer, LOGGING_CHANNEL_ID)
            return

        member = guild.get_member(payload.user_id)
        #member = discord.utils.get(guild.members, id=payload.user_id)
        
        # Check if member is found
        if member is None:
            log_buffer = "Log\nCategory: Role Management\nReason: Member not found\Line: 134"
            await send_logs(log_buffer, LOGGING_CHANNEL_ID)
            return
        
        # Check if correct emoji
        if str(payload.emoji) == "✅":
            await member.add_roles(role)
            log_buffer = f"Log\nCategory: Role Management\nReason: Assigned {role.name} to {member.display_name}"
            await send_logs(log_buffer, LOGGING_CHANNEL_ID)



#  ==================================================
#  Default functions
#  ==================================================
#

@bot.event
async def on_ready():
    await send_logs('Log\nCategory: Bot\nReason: Bot is ready', LOGGING_CHANNEL_ID)
    print(f'Logged in as {bot.user}')

#  ==================================================
#  COMMANDS SECTION
#  ==================================================
#

bot.remove_command('ping')
bot.remove_command('help')

@bot.command(name='onlyusedbytransistors_itshided')
async def help_command(ctx):
    help_message = """
🔸**Welcome to the ByteMeACM channel**🔸
This is the channel to use bot commands.
A reply message will be sent to you when you use a command in channel <#1293521046326214656>.

🔸**Bot Commands:**🔸
🔹!join {group} - Join a scientific group.

🔸**Available Scientific Groups:**🔸
• `!join AI` - Join Artificial Intelligence Group.
• `!join Hardweras` - Join Hardware Group.
• `!join Cybersecurity` - Join Cybersecurity Group.

❗️Please do not spam commands.❗️
"""
    await ctx.send(help_message)

@bot.command(name='join')
async def join_group(ctx, group: str):
    # Find the role based on the group name
    role = discord.utils.get(ctx.guild.roles, name=group)

    if role is None:
        error_message = f"{ctx.author.mention}, the '{group}' role does not exist."
        await send_logs(error_message, REPLYING_CHANNEL_ID)
        return

    # Check if the user already has the role
    if role in ctx.author.roles:
        log_message = f"{ctx.author.mention}, you already have the '{group}' role."
        await send_logs(log_message, REPLYING_CHANNEL_ID)
    else:
        try:
            # Add the role to the user
            await ctx.author.add_roles(role)
            log_message = f"{ctx.author.mention}, you have been added to the '{group}' group."
            await send_logs(log_message, REPLYING_CHANNEL_ID)
        except discord.Forbidden:
            error_message = f"{ctx.author.mention}, I do not have permission to add roles."
            await send_logs(error_message, LOGGING_CHANNEL_ID)
        except discord.HTTPException as e:
            error_message = f"{ctx.author.mention}, an error occurred while adding the role. Line: 225"
            await send_logs(error_message, LOGGING_CHANNEL_ID)
            print(e)

    log_buffer = f"Log\nCategory: Role Management\nReason: Assigned {role.name} to {ctx.author.display_name}"
    await send_logs(log_buffer, LOGGING_CHANNEL_ID)




bot.run('ByteMeACM_TOKEN')




