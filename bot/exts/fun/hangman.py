from pathlib import Path
import json
from random import choice

from discord import Embed, Message
from discord.ext import commands

from bot.bot import Bot
from bot.constants import Colours, NEGATIVE_REPLIES

# Load word presets from JSON file
with open(Path("bot/exts/fun/hangman_presets.json")) as f:
    WORD_PRESETS = json.load(f)["DIFFICULTY_PRESETS"]

# Defining a dictionary of images that will be used for the game to represent the hangman person
IMAGES = {
    6: "https://cdn.discordapp.com/attachments/859123972884922418/888133201497837598/hangman0.png",
    5: "https://cdn.discordapp.com/attachments/859123972884922418/888133595259084800/hangman1.png",
    4: "https://cdn.discordapp.com/attachments/859123972884922418/888134194474139688/hangman2.png",
    3: "https://cdn.discordapp.com/attachments/859123972884922418/888133758069395466/hangman3.png",
    2: "https://cdn.discordapp.com/attachments/859123972884922418/888133786724859924/hangman4.png",
    1: "https://cdn.discordapp.com/attachments/859123972884922418/888133828831477791/hangman5.png",
    0: "https://cdn.discordapp.com/attachments/859123972884922418/888133845449338910/hangman6.png",
}


class Hangman(commands.Cog):
    """
    Cog for the Hangman game.

    Hangman is a classic game where the user tries to guess a word, with a limited amount of tries.
    """

    def __init__(self, bot: Bot):
        self.bot = bot

    @staticmethod
    def create_embed(tries: int, user_guess: str, difficulty: str = None) -> Embed:
        """
        Helper method that creates the embed where the game information is shown.

        This includes how many letters the user has guessed so far, and the hangman photo itself.
        """
        hangman_embed = Embed(
            title="Hangman",
            color=Colours.python_blue,
        )
        hangman_embed.set_image(url=IMAGES[tries])
        hangman_embed.add_field(
            name=f"You've guessed `{user_guess}` so far.",
            value="Guess the word by sending a message with a letter!"
        )
        footer_text = f"Tries remaining: {tries}"
        if difficulty:
            footer_text += f" | Difficulty: {difficulty.capitalize()}"
        hangman_embed.set_footer(text=footer_text)
        return hangman_embed

    @commands.command()
    async def hangman(
            self,
            ctx: commands.Context,
            difficulty: str = "medium"
    ) -> None:
        """
        Play hangman against the bot, where you have to guess the word it has provided!

        The difficulty parameter can be one of:
        - easy: Shorter words with fewer unique letters
        - medium: Medium length words with moderate unique letters
        - hard: Longer words with more unique letters
        """
        difficulty = difficulty.lower()
        if difficulty not in WORD_PRESETS:
            invalid_difficulty_embed = Embed(
                title=choice(NEGATIVE_REPLIES),
                description="Invalid difficulty! Please choose from `easy`, `medium`, or `hard`.",
                color=Colours.soft_red,
            )
            await ctx.send(embed=invalid_difficulty_embed)
            return

        word = choice(WORD_PRESETS[difficulty])
        # `pretty_word` is used for comparing the indices where the guess of the user is similar to the word
        # The `user_guess` variable is prettified by adding spaces between every dash, and so is the `pretty_word`
        pretty_word = "".join([f"{letter} " for letter in word])[:-1]
        user_guess = ("_ " * len(word))[:-1]
        tries = 6
        guessed_letters = set()

        def check(msg: Message) -> bool:
            return msg.author == ctx.author and msg.channel == ctx.channel

        original_message = await ctx.send(embed=Embed(
            title="Hangman",
            description="Loading game...",
            color=Colours.soft_green
        ))

        # Game loop
        while user_guess.replace(" ", "") != word:
            # Edit the message to the current state of the game
            await original_message.edit(embed=self.create_embed(tries, user_guess, difficulty))

            try:
                message = await self.bot.wait_for(
                    "message",
                    timeout=60.0,
                    check=check
                )
            except TimeoutError:
                timeout_embed = Embed(
                    title="You lost",
                    description=f"Time's up! The correct word was `{word}`.",
                    color=Colours.soft_red,
                )
                await ctx.send(embed=timeout_embed)
                return

            # If the user enters a capital letter as their guess, it is automatically converted to a lowercase letter
            normalized_content = message.content.lower()
            # The user should only guess one letter per message
            if len(normalized_content) > 1:
                letter_embed = Embed(
                    title=choice(NEGATIVE_REPLIES),
                    description="You can only send one letter at a time, try again!",
                    color=Colours.dark_green,
                )
                await ctx.send(embed=letter_embed, delete_after=4)
                continue

            # Checks for repeated guesses
            if normalized_content in guessed_letters:
                already_guessed_embed = Embed(
                    title=choice(NEGATIVE_REPLIES),
                    description=f"You have already guessed `{normalized_content}`, try again!",
                    color=Colours.dark_green,
                )
                await ctx.send(embed=already_guessed_embed, delete_after=4)
                continue

            # Checks for correct guesses from the user
            if normalized_content in word:
                positions = {idx for idx, letter in enumerate(pretty_word) if letter == normalized_content}
                user_guess = "".join(
                    [normalized_content if index in positions else dash for index, dash in enumerate(user_guess)]
                )
            else:
                tries -= 1

                if tries <= 0:
                    losing_embed = Embed(
                        title="You lost.",
                        description=f"The word was `{word}`.",
                        color=Colours.soft_red,
                    )
                    await original_message.edit(embed=self.create_embed(tries, user_guess, difficulty))
                    await ctx.send(embed=losing_embed)
                    return

            guessed_letters.add(normalized_content)

        # The loop exited meaning that the user has guessed the word
        await original_message.edit(embed=self.create_embed(tries, user_guess, difficulty))
        win_embed = Embed(
            title="You won!",
            description=f"The word was `{word}`.",
            color=Colours.grass_green
        )
        await ctx.send(embed=win_embed)


async def setup(bot: Bot) -> None:
    """Load the Hangman cog."""
    await bot.add_cog(Hangman(bot))
