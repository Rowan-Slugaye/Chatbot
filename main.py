import os
import random  # for AI choice

import discord
from discord.ext import commands
from discord.ui import Button

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix='!', intents=intents)


class RPSView(discord.ui.View):

  def __init__(self, options, initiator, opponent):
    super().__init__(timeout=60)  # Set a timeout of 60 seconds
    self.options = options
    self.choices = {}  # Dictionary to store choices made by players
    self.initiator = initiator
    self.opponent = opponent
    self.ai_choice = None

    for option in options:
      button = Button(label=option, custom_id=option)
      button.callback = self.on_button_click  # Assign callback here
      self.add_item(button)

  async def on_button_click(self, interaction: discord.Interaction):
    # Check if the responder is one of the allowed users
    if interaction.user.id not in [self.initiator.id, self.opponent.id]:
      await interaction.response.send_message(
          "You are not allowed to respond to this message.", ephemeral=True)
      return

    # Get the custom ID of the clicked button
    custom_id = interaction.data['custom_id']
    user_id = interaction.user.id

    # Store the choice made by the user
    self.choices[user_id] = custom_id

    # If only one player has made their choice and the opponent is AI, proceed to determine the winner
    if len(self.choices) == 1 and self.opponent == client.user:
      await interaction.response.send_message(
          f"{self.initiator.mention}, please make your choice and mention {self.opponent.mention} to play against!",
          ephemeral=True)
    # If only one player has made their choice and the initiator is AI, ask the opponent to make a choice
    elif len(self.choices) == 1 and self.initiator == client.user:
      await interaction.response.send_message(
          f"{self.opponent.mention}, please make your choice and mention {self.initiator.mention} to play against!",
          ephemeral=True)
    # If both players have made their choices or if the AI has made its choice, determine the winner
    elif len(self.choices) == 2 or (len(self.choices) == 1 and self.ai_choice):
      await self.determine_winner(interaction)

  async def determine_winner(self, interaction):
    # If AI hasn't made its choice yet and opponent is AI, make it now
    if not self.ai_choice and self.opponent == client.user:
      self.ai_choice = random.choice(self.options)

    # Get user IDs of both players
    player1_id = next(iter(self.choices.keys()))

    # Get choices made by both players
    player1_choice = self.choices[player1_id]
    player2_choice = self.choices.get(self.opponent.id, self.ai_choice)

    # Determine the winner
    winner = None
    if player1_choice == player2_choice:
      pass
    elif (player1_choice == 'rock' and player2_choice == 'scissors') or \
            (player1_choice == 'paper' and player2_choice == 'rock') or \
            (player1_choice == 'scissors' and player2_choice == 'paper'):
      winner = player1_id
    else:
      winner = self.opponent.id

    # Construct the result message
    if winner:
      # Mention both players in the initial message
      initial_message = f"{self.initiator.mention} and {self.opponent.mention}, {player1_choice} vs {player2_choice}:"

      # Edit the original message to mention the winner
      await interaction.message.edit(
          content=f"{initial_message}\n<@{winner}> wins!")

      loser_id = player1_id if winner == self.opponent.id else self.opponent.id
      loser_message = f"<@{loser_id}> lost! {self.choices[player1_id]} vs {player2_choice}"

      # Send a single message stating who won and who lost
      final_message = f"<@{winner}> wins! {self.choices[player1_id]} vs {player2_choice}\n{loser_message}"
      await interaction.channel.send(final_message)

      # Delete the original message
      await interaction.message.delete()
    else:
      result_message = "It's a tie!"
      await interaction.message.edit(content=result_message)


class DiceView(discord.ui.View):

  def __init__(self, options, initiator, opponent):
    super().__init__(timeout=60)  # Set a timeout of 60 seconds
    self.options = options
    self.choices = {}  # Dictionary to store choices made by players
    self.initiator = initiator
    self.opponent = opponent
    self.ai_choice = None

    for option in options:
      button = Button(label=option, custom_id=option)
      button.callback = self.on_button_click  # Assign callback here
      self.add_item(button)

  async def on_button_click(self, interaction: discord.Interaction):
    # Check if the responder is one of the allowed users
    if interaction.user.id not in [self.initiator.id, self.opponent.id]:
      await interaction.response.send_message(
          "You are not allowed to respond to this message.", ephemeral=True)
      return

    # Get the custom ID of the clicked button
    custom_id = interaction.data['custom_id']
    user_id = interaction.user.id

    # Store the choice made by the user
    self.choices[user_id] = random.randint(1, 6)

    # If only one player has made their choice and the opponent is AI, proceed to determine the winner
    if len(self.choices) == 1 and self.opponent == client.user:
      await interaction.response.send_message(
          f"{self.initiator.mention}, please make your choice and mention {self.opponent.mention} to play against!",
          ephemeral=True)
    # If only one player has made their choice and the initiator is AI, ask the opponent to make a choice
    elif len(self.choices) == 1 and self.initiator == client.user:
      await interaction.response.send_message(
          f"{self.opponent.mention}, please make your choice and mention {self.initiator.mention} to play against!",
          ephemeral=True)
    # If both players have made their choices or if the AI has made its choice, determine the winner
    elif len(self.choices) == 2 or (len(self.choices) == 1 and self.ai_choice):
      await self.determine_winner(interaction)

  async def determine_winner(self, interaction):
    # If AI hasn't made its choice yet and opponent is AI, make it now
    if not self.ai_choice and self.opponent == client.user:
      self.ai_choice = random.choice(self.options)

    # Get user IDs of both players
    player1_id = next(iter(self.choices.keys()))

    # Get choices made by both players
    player1_choice = self.choices[player1_id]
    player2_choice = self.choices.get(self.opponent.id, self.ai_choice)

    # Determine the winner
    winner = None
    if player1_choice == player2_choice:
      pass
    elif (player1_choice > player2_choice):
      winner = self.initiator.id
    else:
      winner = self.opponent.id

    # Construct the result message
    if winner:
      # Mention both players in the initial message
      initial_message = f"{self.initiator.mention} and {self.opponent.mention}, {player1_choice} vs {player2_choice}:"

      # Edit the original message to mention the winner
      await interaction.message.edit(
          content=f"{initial_message}\n<@{winner}> wins!")

      loser_id = player1_id if winner == self.opponent.id else self.opponent.id
      loser_message = f"<@{loser_id}> lost! {self.choices[player1_id]} vs {player2_choice}"

      # Send a single message stating who won and who lost
      final_message = f"<@{winner}> wins! {self.choices[player1_id]} vs {player2_choice}\n{loser_message}"
      await interaction.channel.send(final_message)

      # Delete the original message
      await interaction.message.delete()
    else:
      result_message = "It's a tie!"
      await interaction.message.edit(content=result_message)


@client.event
async def on_ready():
  await client.change_presence(activity=discord.Game(
      name="V: 0.2.2 and Created by Rowan"))
  print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('!ping'):
    await message.channel.send('pong!')
  if message.content.startswith('!help'):
    help_message = """**Available Commands:**\n- `!ping`: Responds with "pong!"\n- `!help`: Displays this help message\n- `!Version`: Displays the current version\n- `!rps`: Starts a game of Rock, Paper, Scissors with a mentioned user"""
    await message.channel.send(help_message)
  if message.content.startswith('!Version'):
    await message.channel.send('0.2.2')
  if message.content.startswith('!rps'):
    options = ["Rock", "Paper", "Scissors"]

    # Determine opponent
    if len(message.mentions) == 0:
      await message.channel.send("Please mention someone to play against!")
      return
    opponent = message.mentions[0]

    # Print the players in console
    print(f"{message.author} is playing against {opponent}")

    # Mention both players
    view = RPSView(options, message.author, opponent)
    await message.channel.send(
        f"{message.author.mention} and {opponent.mention} make your move:",
        view=view)
  if message.content.startswith('!dice'):
    options = ["roll"]

    # Determine opponent
    if len(message.mentions) == 0:
      await message.channel.send("Please mention someone to play against!")
      return
    opponent = message.mentions[0]

    # Print the players in console
    print(f"{message.author} is playing against {opponent}")

    # Mention both players
    view = DiceView(options, message.author, opponent)
    await message.channel.send(
        f"{message.author.mention} and {opponent.mention} make your move:",
        view=view)


try:
  token = os.getenv("TOKEN") or ""
  if token == "":
    raise Exception("Please add your token to the Secrets pane.")
  client.run(token)
except discord.HTTPException as e:
  if e.status == 429:
    print(
        "The Discord servers denied the connection for making too many requests"
    )
    print(
        "Get help from https://stackoverflow.com/questions/66724687/in-discord-py-how-to-solve-the-error-for-toomanyrequests"
    )
  else:
    raise e
