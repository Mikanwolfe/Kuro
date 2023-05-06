import os
import requests
from pydub import AudioSegment
from pydub.playback import play
from discord.ext import commands
from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import types

# Set up the Google Cloud Speech-to-Text client
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/your/google-credentials.json"
speech_client = speech.SpeechClient()

# Initialize the Discord bot
bot = commands.Bot(command_prefix="!")

@bot.command()
async def play_wav(ctx):
    # Query the Elevenlabs API and save the WAV file
    url = "https://api.elevenlabs.com/path/to/your/endpoint"
    response = requests.get(url)
    with open("audio.wav", "wb") as f:
        f.write(response.content)

    # Play the WAV file in the voice channel
    channel = ctx.author.voice.channel
    if channel:
        voice_client = await channel.connect()
        source = discord.FFmpegPCMAudio("audio.wav")
        voice_client.play(source, after=lambda e: print("Finished playing"))
        while voice_client.is_playing():
            pass
        await voice_client.disconnect()

    # Record the microphone input for speech-to-text
    # The following code should be executed on the user's side and not within the bot's script
    # Please refer to the note below for more details
    """
    with open("microphone_input.wav", "rb") as f:
        content = f.read()
    audio = types.RecognitionAudio(content=content)

    config = types.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )

    response = speech_client.recognize(config=config, audio=audio)
    for result in response.results:
        print("Transcript: {}".format(result.alternatives[0].transcript))
    """

@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")

# Run the bot
if __name__ == "__main__":
    bot.run(os.environ["DISCORD_TOKEN"])
