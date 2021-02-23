# ProctorPhil

ProctorPhil is a bot for my discord server that brings together many of my small Python projects.

The bot can search Wikipedia, Twitter, Urban Dictionary, and multiple dictionary APIs.

`uphilities.py` is where several projects are boiled down into nice discord-bot-friendly functions,
and soon there will be fewer `.py` files as the consolidation continues.

The bot runs on my Raspberry Pi: cron executes a C program that spawns and kills the bot on a regular
schedule so it can pull updates from this repository. In the future, I would like to skip the C
step and just have cron run a shell script to restart and update the bot.
