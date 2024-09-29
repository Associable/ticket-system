import os
import json
import discord
from discord import app_commands
from discord.ext import commands
import io
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime

CONFIG_FILE = 'config.json'
DEFAULT_CONFIG = {
    "BOT_TOKEN": "",
    "SERVER_NAME": "lunar's cave",
    "TICKET_CATEGORY_NAME": "Tickets",
    "ARCHIVE_CATEGORY_NAME": "Archived Tickets",
    "TRANSCRIPTS_CATEGORY_NAME": "Transcripts",
    "LOG_CHANNEL_NAME": "logs",
    "DEFAULT_TICKET_MESSAGE": "🎫 Welcome to the lunar's cave support system! Please select a category to proceed.",
    "PEARL_WHITE": 0xEAEAEA,
    "TICKET_PRIORITY_LEVELS": ["Low", "Medium", "High", "Urgent"],
    "MAX_TICKETS_PER_USER": 1
}

logger = logging.getLogger("VouchBotLogger")
logger.setLevel(logging.DEBUG)
handler = RotatingFileHandler("vouchbot.log", maxBytes=5000000, backupCount=5)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def load_config():
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'w') as f:
            json.dump(DEFAULT_CONFIG, f, indent=4)
        logger.warning(f"No configuration file found. Creating default '{CONFIG_FILE}'. Please fill in the required details.")
        print(f"No configuration file found. Created default '{CONFIG_FILE}'. Please fill in the required details and re-run the bot.")
        exit(1)
    else:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)

try:
    config = load_config()
except json.JSONDecodeError:
    logger.error("The configuration file is corrupted or improperly formatted. Please fix or delete it to regenerate.")
    print("The configuration file is corrupted or improperly formatted. Please fix or delete it to regenerate.")
    exit(1)

BOT_TOKEN = config["BOT_TOKEN"]
SERVER_NAME = config["SERVER_NAME"]
TICKET_CATEGORY_NAME = config["TICKET_CATEGORY_NAME"]
ARCHIVE_CATEGORY_NAME = config["ARCHIVE_CATEGORY_NAME"]
TRANSCRIPTS_CATEGORY_NAME = config["TRANSCRIPTS_CATEGORY_NAME"]
LOG_CHANNEL_NAME = config["LOG_CHANNEL_NAME"]
DEFAULT_TICKET_MESSAGE = config["DEFAULT_TICKET_MESSAGE"]
PEARL_WHITE = config["PEARL_WHITE"]
TICKET_PRIORITY_LEVELS = config["TICKET_PRIORITY_LEVELS"]
MAX_TICKETS_PER_USER = config["MAX_TICKETS_PER_USER"]

if not BOT_TOKEN:
    logger.error("BOT_TOKEN is missing in config.json. Please add the bot token and restart the bot.")
    print("BOT_TOKEN is missing in config.json. Please add the bot token and restart the bot.")
    exit(1)

def clear_console():
    os.system("cls" if os.name == "nt" else "clear")

class nuhuh(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        intents.members = True
        intents.messages = True
        super().__init__(command_prefix='!', intents=intents)
        self.synced = False

    async def setup_hook(self):
        if not self.synced:
            await self.tree.sync()
            self.synced = True
            logger.info("Command tree synced.")

    async def on_ready(self):
        await self.change_presence(status=discord.Status.dnd, activity=discord.Game(SERVER_NAME))
        logger.info(f'{self.user} has connected to Discord!')
        print(f'{self.user} has connected to Discord!')
        clear_console()

bot = nuhuh()

class TicketTypeSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Purchase", description="Click this option to purchase a product!", emoji="🛒"),
            discord.SelectOption(label="Replacements", description="Click this option if you require replacements!", emoji="🔄"),
            discord.SelectOption(label="Questions", description="Click this option if you have questions!", emoji="❓")
        ]
        super().__init__(placeholder="Select a category...", options=options)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        try:
            ticket_type = self.values[0].lower()
            category_name = f"{ticket_type.capitalize()} {TICKET_CATEGORY_NAME}"
            category = discord.utils.get(interaction.guild.categories, name=category_name) or await interaction.guild.create_category(category_name)

            existing_tickets = [channel for channel in category.channels if channel.name.startswith(f"{ticket_type}-{interaction.user.name}")]
            if len(existing_tickets) >= MAX_TICKETS_PER_USER:
                error_embed = discord.Embed(
                    title="🚫 Ticket Limit Reached",
                    description=f"You already have {MAX_TICKETS_PER_USER} open ticket(s) in this category. Please close your existing ticket(s) before opening a new one.",
                    color=PEARL_WHITE
                )
                await interaction.followup.send(embed=error_embed, ephemeral=True)
                return

            channel_name = f"{ticket_type}-{interaction.user.name}-{interaction.user.discriminator}"
            overwrites = {
                interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True, attach_files=True, embed_links=True),
                interaction.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_channels=True, manage_messages=True)
            }

            ticket_channel = await category.create_text_channel(channel_name, overwrites=overwrites)

            ticket_embed = discord.Embed(
                title=f"🎟️ Ticket Created: {channel_name}",
                description=f"Please wait for staff to respond, {interaction.user.mention}. Our team will assist you shortly. Please select a priority for this ticket below.",
                color=PEARL_WHITE
            )

            priority_view = discord.ui.View()
            priority_view.add_item(TicketPrioritySelect(ticket_channel, interaction.user))
            await ticket_channel.send(embed=ticket_embed, view=priority_view)

            success_embed = discord.Embed(
                title="✅ Ticket Created",
                description=f"Your ticket has been successfully created: {ticket_channel.mention}.",
                color=PEARL_WHITE
            )
            await interaction.followup.send(embed=success_embed, ephemeral=True)
            logger.info(f"Ticket created by {interaction.user} in {ticket_channel.name}")

        except Exception as e:
            logger.error(f"Error creating ticket: {e}")
            await interaction.followup.send("An error occurred while creating the ticket. Please try again later.", ephemeral=True)

class TicketPrioritySelect(discord.ui.Select):
    def __init__(self, ticket_channel, ticket_user):
        self.ticket_channel = ticket_channel
        self.ticket_user = ticket_user
        options = [
            discord.SelectOption(label="Low", description="Low priority.", emoji="🟢"),
            discord.SelectOption(label="Medium", description="Medium priority.", emoji="🟡"),
            discord.SelectOption(label="High", description="High priority.", emoji="🟠"),
            discord.SelectOption(label="Urgent", description="Urgent priority.", emoji="🔴")
        ]
        super().__init__(placeholder="Select ticket priority...", options=options)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        try:
            priority = self.values[0]
            await self.ticket_channel.edit(topic=f"Priority: {priority} | User: {self.ticket_user.display_name}")

            priority_embed = discord.Embed(
                title=f"🎟️ Ticket Priority: {priority}",
                description=f"Priority has been set to **{priority}**. A staff member will respond shortly.",
                color=PEARL_WHITE
            )

            priority_view = discord.ui.View()
            priority_view.add_item(TicketCloseButton(self.ticket_channel))
            await self.ticket_channel.send(embed=priority_embed, view=priority_view)

            await interaction.followup.send(f"Priority set to **{priority}**.", ephemeral=True)
            logger.info(f"Ticket priority set to {priority} by {interaction.user} in {self.ticket_channel.name}")

        except Exception as e:
            logger.error(f"Error setting priority: {e}")
            await interaction.followup.send("An error occurred while setting the priority. Please try again later.", ephemeral=True)

class TicketCloseButton(discord.ui.Button):
    def __init__(self, ticket_channel):
        super().__init__(label="Close Ticket", style=discord.ButtonStyle.danger)
        self.ticket_channel = ticket_channel

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        try:
            messages = []
            async for message in self.ticket_channel.history(limit=None, oldest_first=True):
                timestamp = message.created_at.strftime("%Y-%m-%d %H:%M:%S")
                messages.append({
                    "timestamp": timestamp,
                    "author": message.author.display_name,
                    "author_avatar": message.author.avatar.url if message.author.avatar else None,
                    "content": message.content
                })

            transcript_content = "\n".join([f"{msg['timestamp']} - {msg['author']} ({msg['content']})" for msg in messages])
            transcript_file = discord.File(fp=io.BytesIO(transcript_content.encode()), filename=f"transcript-{self.ticket_channel.name}.txt")

            html_content = f"""
            <html>
            <head>
                <title>Transcript for {self.ticket_channel.name}</title>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        background-color: #121212;
                        color: #e0e0e0;
                        padding: 20px;
                    }}
                    .message {{
                        border-bottom: 1px solid #333;
                        padding: 10px 0;
                    }}
                    .timestamp {{
                        color: #999;
                        font-size: 0.85em;
                    }}
                    .author {{
                        font-weight: bold;
                        color: #ffa726;
                    }}
                </style>
            </head>
            <body>
                <h1>Transcript for {self.ticket_channel.name}</h1>
            """
            for message in messages:
                html_content += f"""
                <div class="message">
                    <div class="author">{message['author']}</div>
                    <div class="timestamp">{message['timestamp']}</div>
                    <div>{message['content']}</div>
                </div>
                """
            html_content += "</body></html>"

            html_file = discord.File(fp=io.BytesIO(html_content.encode()), filename=f"transcript-{self.ticket_channel.name}.html")

            embed = discord.Embed(
                title=f"Transcript for {self.ticket_channel.name}",
                description="Transcript is attached as a .txt file and an HTML file.",
                color=discord.Color.blurple()
            )

            logs_channel = discord.utils.get(interaction.guild.text_channels, name=LOG_CHANNEL_NAME) or await interaction.guild.create_text_channel(LOG_CHANNEL_NAME)
            await logs_channel.send(f"Transcript for {self.ticket_channel.name} closed by {interaction.user.mention}:", embed=embed, files=[transcript_file, html_file])

            archive_category = discord.utils.get(interaction.guild.categories, name=ARCHIVE_CATEGORY_NAME) or await interaction.guild.create_category(ARCHIVE_CATEGORY_NAME)
            await self.ticket_channel.edit(category=archive_category)
            await self.ticket_channel.send("Ticket has been archived.")
            logger.info(f"Ticket {self.ticket_channel.name} closed and archived by {interaction.user}")

            delete_view = discord.ui.View()
            delete_view.add_item(TicketDeleteButton(self.ticket_channel))
            await self.ticket_channel.send("Would you like to delete this ticket now?", view=delete_view)

        except Exception as e:
            logger.error(f"Error closing ticket: {e}")
            await interaction.followup.send("An error occurred while closing the ticket. Please try again later.", ephemeral=True)

class TicketDeleteButton(discord.ui.Button):
    def __init__(self, ticket_channel):
        super().__init__(label="Delete Ticket", style=discord.ButtonStyle.danger)
        self.ticket_channel = ticket_channel

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        try:
            await self.ticket_channel.delete(reason=f"Ticket deleted by {interaction.user.display_name}")
            await interaction.followup.send("The ticket has been successfully deleted.", ephemeral=True)
            logger.info(f"Ticket {self.ticket_channel.name} deleted by {interaction.user}")

        except Exception as e:
            logger.error(f"Error deleting ticket: {e}")
            await interaction.followup.send("An error occurred while deleting the ticket. Please try again later.", ephemeral=True)

@bot.tree.command(name='purge_tickets', description='Purge all ticket channels including archived tickets')
@app_commands.checks.has_any_role("Owner")
async def purge_tickets(interaction: discord.Interaction):
    await interaction.response.defer()
    try:
        categories_to_purge = [TICKET_CATEGORY_NAME, ARCHIVE_CATEGORY_NAME]
        channels_deleted = 0

        for category_name in categories_to_purge:
            category = discord.utils.get(interaction.guild.categories, name=category_name)
            if category:
                for channel in category.channels:
                    await channel.delete(reason=f"Bulk purge requested by {interaction.user.display_name}")
                    channels_deleted += 1

        await interaction.followup.send(f"Successfully purged {channels_deleted} ticket channel(s).", ephemeral=True)
        logger.info(f"{channels_deleted} ticket channels purged by {interaction.user}")

    except Exception as e:
        logger.error(f"Error purging tickets: {e}")
        await interaction.followup.send("An error occurred while purging tickets. Please try again later.", ephemeral=True)

@bot.tree.command(name='setup', description=f'Setup the {TICKET_CATEGORY_NAME} system')
@app_commands.checks.has_any_role("Owner")
async def setup(interaction: discord.Interaction):
    try:
        await interaction.response.defer()
        embed = discord.Embed(
            title=f"🎫 {TICKET_CATEGORY_NAME} Panel | {SERVER_NAME}",
            description=DEFAULT_TICKET_MESSAGE,
            color=PEARL_WHITE
        )

        embed.add_field(name="💳 Payment Methods", value="**💰 Cryptocurrencies**\n**💵 Cashapp**\n**💸 PayPal**", inline=False)
        embed.add_field(name="💼 Select a Category:", value="Select an option below to proceed.", inline=False)
        embed.set_footer(text=f"Powered by {SERVER_NAME} | All rights reserved.")

        view = discord.ui.View()
        view.add_item(TicketTypeSelect())

        await interaction.followup.send(embed=embed, view=view)
        logger.info(f"Ticket setup panel sent by {interaction.user}")

    except Exception as e:
        logger.error(f"Error during setup command: {e}")
        await interaction.followup.send("An error occurred during the setup process. Please try again later.", ephemeral=True)

bot.run(BOT_TOKEN)
