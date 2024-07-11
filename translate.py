# Instelling voor nederlands!
USE_DUTCH = False

sentences = {
    "dutch": {
        "bot_status":
        "brood bakken",
        "baked":
        "{}, je brood is gebakken!",
        "baking":
        "Je bent al brood aan het bakken, kijk even later op je DM's!",
        "error_negative_time":
        "je kan niet in de min gaan met de tijd!",
        "started":
        "{} heeft gestart met brood bakken voor {} minuten!",
        "burned":
        "{} je brood is verbrand! Maar je hebt wat ervaring gekregen.",
        "leaderboard_message":
        "Scorebord:\n",
        "leaderboard_single":
        "{} brood, {} XP\n",
        "leaderboard_multiple":
        "{} broden, {} XP\n",
        "status_baking":
        "{} je brood is klaar in {} minuten.",
        "status_idle":
        "{} je bent momenteel geen brood aan het bakken.",
        "count_single":
        "{} heeft {} brood.",
        "count_multiple":
        "{} heeft {} broden.",
        "help_title":
        "Brood Bot-opdrachten:",
        "help_description":
        "!bak <tijd> - Begin met het bakken van brood gedurende de opgegeven tijd (in minuten).\n"
        "!brood - Controleer hoeveel broden je hebt.\n"
        "!status - Controleer de resterende baktijd van uw brood.\n"
        "!scorebord - Toon het scorebord van gebruikers met het meeste brood.\n"
        "!help - Dit helpbericht weergeven.\n\n"
        "You can translate the commands and messages to english by changing the USE_DUTCH variable to False in the 'translate.py' file."
    },
    "english": {
        "bot_status":
        "baking bread",
        "baked":
        "{}, your bread is done!",
        "baking":
        "You're already baking bread, check your DMs later!",
        "error_negative_time":
        "you can't go back in time with the time!",
        "started":
        "{} has started baking bread for {} minutes!",
        "burned":
        "{} your bread has burned! But you gained some experience.",
        "leaderboard_message":
        "Leaderboard:\n",
        "leaderboard_single":
        "{} bread, {} XP\n",
        "leaderboard_multiple":
        "{} breads, {} XP\n",
        "status_baking":
        "{} your bread will be done in {} minutes.",
        "status_idle":
        "{} you are not currently baking any bread.",
        "count_single":
        "{} has {} bread.",
        "count_multiple":
        "{} has {} breads.",
        "help_title":
        "Bread Bot commands:",
        "help_description":
        "!bake <time> - Start baking bread for the specified time (in minutes).\n"
        "!bread - Check how many breads you have.\n"
        "!status - Check the remaining bake time for your bread.\n"
        "!leaderboard - Show the leaderboard of users with the most bread.\n"
        "!help - Show this help message.\n\n"
        "Je kunt de commandos en de berichten naar het Nederlands vertalen door de variabele USE_DUTCH in het 'translate.py' bestand te wijzigen naar True."
    }
}

commands = {
    "dutch": {
        "bake": "bak",
        "leaderboard": "scorebord",
        "bread": "brood",
        "status": "status"
    },
    "english": {
        "bake": "bake",
        "leaderboard": "leaderboard",
        "bread": "bread",
        "status": "status"
    }
}


def get_sentence(index: str, *format: object) -> str:
    found_sentence = sentences["dutch" if USE_DUTCH else "english"][index]
    if found_sentence is None:
        raise Exception(f"Invalid sentence index! found at: {index}")
    return found_sentence.format(*format)


def get_command(index: str):
    found_command = commands["dutch" if USE_DUTCH else "english"][index]
    if found_command is None:
        raise Exception(f"Invalid command index! found at: {index}")
    return found_command
