import random
import discord
from discord.ext import commands

client = discord.Client()
client = commands.Bot(command_prefix = '!')

@client.event
async def on_ready():
  print('Ready')

@client.command()
async def clearChat(ctx):
  await ctx.channel.purge(limit = 1000)

@client.command()
async def play(ctx):
  guessedWord = False
  lives = 6
  word = ''
  lettersGuessed = []
  correctGuessed = list('_____')

  with open("words.txt", "r") as file:
    data = file.read()
    words = data.split()
    word_pos = random.randint(0, len(words) - 1)
    word = words[word_pos]

  while lives > 0 and '_' in correctGuessed:
    await ctx.send('```' + str(ctx.author)[:-5] + ' guess a letter or the word:```')
    msg = await client.wait_for('message', check=lambda message: message.author == ctx.author)

    if len(msg.content) == 5:
      if msg.content.lower().__eq__(word):
        for i in range(0, len(word)):
          correctGuessed[i] = word[i]
      else:
        lives = lives - 1
    elif not msg.content.lower() in lettersGuessed and len(msg.content) == 1:
      if msg.content.lower() in word:
        for i in [i for i, letter in enumerate(word) if letter == msg.content.lower()]:
          correctGuessed[i] = msg.content.lower()
      else:
        lives = lives - 1
        
      lettersGuessed.append(msg.content.lower())

    await ctx.send('```' + ''.join(correctGuessed) + '```')
    await ctx.send('```' + str(lettersGuessed) + '```')
    if lives == 6:
      await ctx.send(file=discord.File('images/lives6.png'))
    elif lives == 5:
      await ctx.send(file=discord.File('images/lives5.png'))
    elif lives == 4:
      await ctx.send(file=discord.File('images/lives4.png'))
    elif lives == 3:
      await ctx.send(file=discord.File('images/lives3.png'))
    elif lives == 2:
      await ctx.send(file=discord.File('images/lives2.png'))
    elif lives == 1:
      await ctx.send(file=discord.File('images/lives1.png'))

  if lives == 0:
    await ctx.send('```You lost!```')
    await ctx.send('```The word was ' + word + '```')
    await ctx.send(file=discord.File('images/DEAD.png'))
  else:
    await ctx.send('```You win!```')
  
client.run('')