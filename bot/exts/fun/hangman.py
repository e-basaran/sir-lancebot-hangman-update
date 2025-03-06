from pathlib import Path
import json
from random import choice
from typing import Dict, Optional, Tuple, Union

from discord import Embed, Message
from discord.ext import commands

from bot.bot import Bot
from bot.constants import Colours, NEGATIVE_REPLIES

# Load word presets from JSON file
with open(Path("bot/exts/fun/hangman_presets.json")) as f:
    WORD_PRESETS = json.load(f)["DIFFICULTY_PRESETS"]

# Default parameter ranges for custom games
DEFAULT_PARAMS = {
    "min_length": 0,
    "max_length": 25,
    "min_unique_letters": 0,
    "max_unique_letters": 25
}

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
    def parse_arguments(args: Tuple[str, ...]) -> Tuple[Optional[str], Optional[Dict[str, int]], Optional[str]]:
        """
        Parse and validate command arguments.

        Returns:
            A tuple containing:
            - difficulty preset name if using a preset, None if using custom params
            - dictionary of custom parameters if provided, None if using a preset
            - error message if validation fails, None if validation succeeds
        """
        # No arguments provided - use default difficulty
        if not args:
            return "medium", None, None

        # Check for help command
        if args[0].lower() == "help":
            return None, None, "help"

        # Check if using a difficulty preset
        if len(args) == 1:
            difficulty = args[0].lower()
            if difficulty in WORD_PRESETS:
                return difficulty, None, None
            return None, None, f"Invalid difficulty! Please choose from `easy`, `medium`, or `hard`.\nType `.hangman help` for more information."

        # Parse custom parameters
        try:
            params = DEFAULT_PARAMS.copy()
            if len(args) > 0:
                params["min_length"] = int(args[0])
            if len(args) > 1:
                params["max_length"] = int(args[1])
            if len(args) > 2:
                params["min_unique_letters"] = int(args[2])
            if len(args) > 3:
                params["max_unique_letters"] = int(args[3])

            # Validate parameter ranges
            if params["min_length"] < 0 or params["max_length"] < 0:
                return None, None, "Word length parameters cannot be negative."
            if params["min_unique_letters"] < 0 or params["max_unique_letters"] < 0:
                return None, None, "Unique letter parameters cannot be negative."
            if params["min_length"] > params["max_length"]:
                return None, None, "Minimum word length cannot be greater than maximum word length."
            if params["min_unique_letters"] > params["max_unique_letters"]:
                return None, None, "Minimum unique letters cannot be greater than maximum unique letters."
            if params["min_unique_letters"] > params["max_length"]:
                return None, None, "Number of unique letters cannot be greater than word length."

            return None, params, None

        except ValueError:
            return None, None, "Invalid parameters! Please provide valid numbers or use a difficulty preset.\nType `.hangman help` for more information."

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
            *args: str
    ) -> None:
        """
        Play hangman against the bot, where you have to guess the word it has provided!

        You can play in two ways:
        1. Using difficulty presets:
           - easy: Shorter words with fewer unique letters
           - medium: Medium length words with moderate unique letters
           - hard: Longer words with more unique letters

        2. Using custom parameters:
           - min_length: Minimum word length
           - max_length: Maximum word length
           - min_unique_letters: Minimum unique letters
           - max_unique_letters: Maximum unique letters

        Examples:
        - `.hangman easy` - Play with easy difficulty
        - `.hangman 5 8` - Words with 5-8 letters
        - `.hangman 5 8 3 6` - Words with 5-8 letters and 3-6 unique letters
        - `.hangman help` - Show detailed help

        Type `.hangman help` for more detailed information.
        """
        # Parse and validate arguments
        difficulty, custom_params, error = self.parse_arguments(args)

        # Handle help command
        if error == "help":
            await self.hangman_help(ctx)
            return

        # Handle validation errors
        if error:
            error_embed = Embed(
                title=choice(NEGATIVE_REPLIES),
                description=error,
                color=Colours.soft_red,
            )
            await ctx.send(embed=error_embed)
            return

        # Get word based on difficulty preset or custom parameters
        if difficulty:
            word = choice(WORD_PRESETS[difficulty])
        else:
            # Filter words based on custom parameters
            filtered_words = [
                word for word in sum(WORD_PRESETS.values(), [])  # Combine all word lists
                if custom_params["min_length"] <= len(word) <= custom_params["max_length"]
                and custom_params["min_unique_letters"] <= len(set(word)) <= custom_params["max_unique_letters"]
            ]

            if not filtered_words:
                no_words_embed = Embed(
                    title=choice(NEGATIVE_REPLIES),
                    description="No words found matching your criteria. Try widening your parameters.",
                    color=Colours.soft_red,
                )
                await ctx.send(embed=no_words_embed)
                return

            word = choice(filtered_words)

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

    async def hangman_help(self, ctx):
        """Displays the help message for Hangman, including difficulty options and custom parameters."""
        help_embed = Embed(
            title="Hangman Help",
            description="Here's how to play Hangman!",
            color=Colours.dark_green
        )

        help_embed.add_field(
            name="Basic Commands",
            value="`hangman`: Start a new game with medium difficulty.\n"
                "`hangman help`: Show this help message.",
            inline=False
        )

        help_embed.add_field(
            name="Difficulty Presets",
            value="Choose your difficulty level by typing:\n"
                "`.hangman easy`: Common words (3-5 letters)\n"
                "`.hangman medium`: Moderate words (4-8 letters)\n"
                "`.hangman hard`: Challenging words (8+ letters)",
            inline=False
        )

        help_embed.add_field(
            name="Custom Parameters",
            value="You can customize word selection with these parameters:\n"
                "`.hangman min_length max_length [min_unique max_unique]`\n"
                "Examples:\n"
                "- `.hangman 5 8` - Words with 5-8 letters\n"
                "- `.hangman 5 8 3 6` - Words with 5-8 letters and 3-6 unique letters",
            inline=False
        )

        help_embed.add_field(
            name="How to Play",
            value="1. The bot will choose a word based on your settings\n"
                "2. Guess one letter at a time\n"
                "3. You have 6 tries to guess the word\n"
                "4. The game shows your progress and remaining tries",
            inline=False
        )

        help_embed.add_field(
            name="Tips",
            value="- Start with common vowels (a, e, i, o, u)\n"
                "- Look for common consonants (r, s, t, n)\n"
                "- Pay attention to word length and difficulty level\n"
                "- If no words match your custom parameters, try widening the ranges",
            inline=False
        )

        await ctx.send(embed=help_embed)


async def setup(bot: Bot) -> None:
    """Load the Hangman cog."""
    await bot.add_cog(Hangman(bot))
