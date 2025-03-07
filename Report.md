# Report for assignment 4

This is a template for your report. You are free to modify it as needed.
It is not required to use markdown for your report either, but the report
has to be delivered in a standard, cross-platform format.

## Project

Name: sir-lancebot

URL: https://github.com/e-basaran/sir-lancebot-hangman-update.git

A Discord bot for many stuff, like playing games. We focused on hangman game.

## Onboarding experience

We chose a new project, because we didn't have much experience with deep learning.

It was a bit easier. For some of us, there were some version conflicts with the packages, but overall it was straightforward.
Another thing that slowed us was the tokens, but we managed to build the project successfully.

## Effort spent

For each team member, how much time was spent in

Eyüp: I mostly dealt with argumnt parsing logic, setting up the project, and connecting the components.

1. plenary discussions/meetings: 5-6 hours (0.5h every day online meeting to divide works and fix bugs)

2. discussions within parts of the group: 2 hours

3. reading documentation: 1 hour

4. configuration and setup: 2 hours. I didn't have package conflicts, but understanding the tokens, and setting them slowed me a bit.

5. analyzing code/output: 3 hours

6. writing documentation: 2 hour

7. writing code: 4 hours

8. running code: 2 hour

Bingjie:

1. plenary discussions/meetings: 5-6 hours (0.5h every day online meeting to divide works and fix bugs)

2. discussions within parts of the group: 3 hours

3. reading documentation: 1 hour

4. configuration and setup: 4 hours.

5. analyzing code/output: 4 hours

6. writing code: 4 hours

7. running code: 2 hour

Melissa:

1. plenary discussions/meetings: 5-6 hours (0.5h every day online meeting to divide works and fix bugs)

2. discussions within parts of the group: 2hour

3. reading documentation: 1 hour

4. configuration and setup: 3 hours. I needed to redo the setup because of the tokens were wrong. Also at the start it took time to understand how to export the tokens in an .env or with export in terminal.

5. writing code for defficulty presets/understanding how to define: 2 hours

6. Writing/understanding test cases: 3 hours

7. writing documentation: 1 hour

8. running code: 1 hour

Ismail:

1. plenary discussions/meetings: 5-6 hours (0.5h every day online meeting to divide work and fix bugs)

2. discussions within parts of the group: 2 hours

3. reading documentation: 1 hour

4. configuration and setup: 6 hours. Initially, I tried setting up on Linux Ubuntu, but I ran into multiple errors, including package version conflicts and an issue where Poetry wouldn't install due to an unknown reason. After spending a lot of time troubleshooting, I switched to Windows, where the setup went smoothly. From there, I only had to fix minor issues like understanding tokens and figuring out how to set up and run the bot properly.

5. analyzing code/output: 3 hours

6. writing documentation: 1 hour

7. writing code: 3 hours

8. running code: 2 hours


## Overview of issue(s) and work done.

Title: Update the Hangman game

URL: https://github.com/python-discord/sir-lancebot/issues/1085

Adding difficulty presets and arguments to run the game (like .hangman easy) instead of the existing running arguments (.hangman 4 4 2 5)

It mainly affected hangman.py (all the functions inside of that file), and the utility file hangman-words.txt. We ended up creating a json file for the words.

## Requirements for the new feature or requirements affected by functionality being refactored

Requirements stayed the same. The users can still run the game with the previous arguments, but now they have other arguments like easy, medium, hard, and help.

## Code changes

### Patch

git diff upstream/main origin/main

Optional (point 4): the patch is clean.

Optional (point 5): considered for acceptance (passes all automated checks).

## Test results

Overall results with link to a copy or excerpt of the logs (before/after
refactoring).

## UML class diagram and its description

### Key changes/classes affected

Optional (point 1): Architectural overview.

### Before Implementation

```
+------------------------------------------+
|                 Hangman                  |
+------------------------------------------+
| - bot: Bot                               |
+------------------------------------------+
| + create_embed(tries, user_guess)        |
| + hangman(ctx, min_length,               |
|          max_length,                     |
|          min_unique_letters,             |
|          max_unique_letters)             |
+------------------------------------------+
```

### After Implementation

```
+------------------------------------------+
|                 Hangman                  |
+------------------------------------------+
| - bot: Bot                               |
+------------------------------------------+
| + create_embed(tries, user_guess,        |
|              difficulty)                 |
| + get_help_embed()                       |
| + hangman(ctx, difficulty_or_min_length, |
|          max_length,                     |
|          min_unique_letters,             |
|          max_unique_letters)             |
+------------------------------------------+
```

Optional (point 2): relation to design pattern(s).

## Overall experience

What are your main take-aways from this project? What did you learn?

We mainly learned debugging, and refactoring, or at least we strengthen ourselves in these areas. We also learned much about tokens, and environmntal variables. Other than that, we learned what an UML diagram is.

How did you grow as a team, using the Essence standard to evaluate yourself?

We approached this project with a more mature and systematic methodology compared to our previous experiences. Our initial phase began with a thorough analysis of the Sir Lancebot codebase and Discord bot architecture. We demonstrated significant growth by immediately establishing a clear division of responsibilities and adopting the project's existing practices. We effectively divided the implementation into distinct components We transitioned from "In Use" to "Working Well" because everything was notably smoother this time. 

Optional (point 6): How would you put your work in context with best software engineering practice?

Optional (point 7): Is there something special you want to mention here?
