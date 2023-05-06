import os
import sqlite3
import asyncio
from datetime import datetime
from discord.ext import commands

# Set up the SQLite database
conn = sqlite3.connect("reminders.db")
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS reminders (
                    id INTEGER PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    reminder_text TEXT NOT NULL,
                    reminder_time INTEGER NOT NULL
                  );''')
conn.commit()

# Initialize the Discord bot
bot = commands.Bot(command_prefix="!")

async def create_reminder(user_id, reminder_text, reminder_time):
    cursor.execute("INSERT INTO reminders (user_id, reminder_text, reminder_time) VALUES (?, ?, ?)",
                   (user_id, reminder_text, reminder_time))
    conn.commit()

async def send_reminder(user_id, reminder_text):
    user = await bot.fetch_user(user_id)
    await user.send(f"Reminder: {reminder_text}")

@bot.command()
async def remindme(ctx, unix_time: int, *, reminder_text: str):
    user_id = ctx.author.id
    reminder_time = unix_time
    current_time = int(datetime.utcnow().timestamp())

    if reminder_time < current_time:
        await ctx.send("The specified time is in the past. Please provide a valid Unix timestamp.")
        return

    await create_reminder(user_id, reminder_text, reminder_time)
    await ctx.send(f"Reminder set for {reminder_text} at Unix timestamp {reminder_time}")

    delay = reminder_time - current_time
    await asyncio.sleep(delay)
    await send_reminder(user_id, reminder_text)

@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")

# Run the bot
if __name__ == "__main__":
    bot.run(os.environ["DISCORD_TOKEN"])
