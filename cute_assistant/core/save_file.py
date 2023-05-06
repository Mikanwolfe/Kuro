import os
import json
from discord.ext import commands

# Initialize the Discord bot
bot = commands.Bot(command_prefix="!")

# Function to save question-prompts to a JSON file
def save_to_json(question_prompts, filename="question_prompts.json"):
    with open(filename, "w") as f:
        json.dump(question_prompts, f, indent=2)

# Discord bot command to save question-prompts
@bot.command()
async def save_questions(ctx, *questions):
    question_prompts = {"questions": list(questions)}

    save_to_json(question_prompts)
    await ctx.send(f"Questions saved to JSON file: {', '.join(questions)}")

@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")

# Run the bot
if __name__ == "__main__":
    bot.run(os.environ["DISCORD_TOKEN"])
