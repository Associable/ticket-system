# Ticket System 🎫

A sophisticated Discord bot for managing support tickets in your server. Designed to provide a clean and efficient ticketing system for server members, with features like dynamic ticket creation, priority selection, archiving, transcript generation, and advanced logging.

## Features ✨

- **Custom Ticket Categories**: Allow users to create tickets for different purposes such as "Purchase", "Replacements", or "Questions".
- **Priority System**: Users can set priorities like "Low", "Medium", "High", and "Urgent" for their tickets, ensuring that issues are attended to efficiently.
- **Enhanced Logging**: Comprehensive logging to keep track of all ticket activities.
- **Archive & Transcript System**: Close tickets and automatically archive them, with both `.txt` and `.html` transcripts available.
- **HTML Transcripts with Dark Mode**: Beautiful HTML transcripts with a dark mode and animations for modern, sleek ticket documentation.
- **Ticket Management**: Includes options to delete or archive tickets with buttons for easy ticket lifecycle management.
- **Bot Owner Commands**: Bot administrators can bulk purge tickets and manage the setup with ease.

## Installation & Setup 🛠️

### Prerequisites

- Python 3.8 or higher
- A Discord bot token ([Learn how to get one here](https://discordpy.readthedocs.io/en/stable/discord.html))
- Required Python packages listed in `requirements.txt`:
  - discord.py
  - aiofiles
  - json
  - logging

### Getting Started

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/lunars-cave-ticket-bot.git
   cd lunars-cave-ticket-bot
   ```

2. **Install the Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the Bot**

   The bot requires a `config.json` file for setup. If one does not exist, a default configuration file will be generated.

   Edit the `config.json` to include the required details:

   ```json
   {
     "BOT_TOKEN": "YOUR_DISCORD_BOT_TOKEN_HERE",
     "SERVER_NAME": "lunar's cave",
     "TICKET_CATEGORY_NAME": "Tickets",
     "ARCHIVE_CATEGORY_NAME": "Archived Tickets",
     "TRANSCRIPTS_CATEGORY_NAME": "Transcripts",
     "LOG_CHANNEL_NAME": "logs",
     "DEFAULT_TICKET_MESSAGE": "🎫 Welcome to the lunar's cave support system! Please select a category to proceed.",
     "PEARL_WHITE": 15329770,
     "TICKET_PRIORITY_LEVELS": ["Low", "Medium", "High", "Urgent"],
     "MAX_TICKETS_PER_USER": 1
   }
   ```

4. **Run the Bot**

   ```bash
   python bot.py
   ```

## Commands 🚀

### Ticket System Commands

- **Setup Ticket Panel**: `/setup`
  - Allows server administrators to set up the ticket system panel.

- **Purge Tickets**: `/purge_tickets`
  - Purges all tickets in the active and archived categories.
  - Requires the **Owner** role. (CAN CHANGE IN CODE TO SPECIFIC ROLE)

### Ticket User Workflow

1. **Ticket Creation**: Users select from available ticket categories to create tickets (e.g., "Purchase", "Questions").
2. **Priority Selection**: Users are prompted to set a priority for their ticket.
3. **Staff Support**: Staff members assist the user in the created ticket channel.
4. **Ticket Closure**: Users can close tickets with a button, prompting transcript creation.
5. **Archive & Transcript Generation**: Closed tickets are archived, and a transcript (both `.txt` and `.html`) is sent to the log channel.

## Usage Instructions ⚡

1. Add the bot to your Discord server.
2. Run the `/setup` command to create a ticket system in your server.
3. Users will see a selection panel and can choose their type of ticket.
4. Admins and staff will assist users through the created channels.

## Configuration Details ⚙️

The configuration file (`config.json`) can be customized to meet your needs:

- **`BOT_TOKEN`**: Your Discord bot token.
- **`SERVER_NAME`**: The name displayed in the bot's activity status.
- **`TICKET_CATEGORY_NAME`**: The category where active tickets are created.
- **`ARCHIVE_CATEGORY_NAME`**: Category where closed tickets are moved.
- **`TRANSCRIPTS_CATEGORY_NAME`**: Name of the transcripts category.
- **`LOG_CHANNEL_NAME`**: Name of the log channel for ticket actions.
- **`DEFAULT_TICKET_MESSAGE`**: Default message displayed when setting up the ticket panel.
- **`TICKET_PRIORITY_LEVELS`**: Priority options available to users.
- **`MAX_TICKETS_PER_USER`**: Maximum number of tickets a user can open at one time.

## Built With 🛠️

- [discord.py](https://github.com/Rapptz/discord.py) - Discord API wrapper for Python.
- Python 3 - Programming language for the bot's logic.

## Roadmap 🗺️

- Add advanced features like automated reminders for unanswered tickets.
- Integrate AI-based message classification for more efficient ticket routing.
- Support for multiple languages and custom translations.

## Contributing 🤝

Contributions, issues, and feature requests are welcome!

1. Fork the repository.
2. Create a new feature branch.
3. Commit your changes.
4. Open a pull request.

## Acknowledgements 🙏

- Thanks to the [discord.py](https://discordpy.readthedocs.io/en/stable/) community for their invaluable library and support.
- Big thanks to my mental sanity for making this bot more awesome!

---

### Contact 📬

If you have questions, please reach out at:
- **Discord**: lunarings
- **Email**: lunaringsgg@gmail.com

### Stargazers ⭐

If you like this project, please give it a star to show your support!

---

Enjoy using the ticket system to enhance your server's support experience! 🚀
