from dis import disco
from tkinter import E
from turtle import position
from unicodedata import category
import discord
import datetime
import pytz
import dateutil.parser
import requests
import config
import discord.utils

# relating team id to shortened version of names for formatting reasons
team_ids = {
    "1": "devils",
    "2": "isles",
    "3": "rangers",
    "4": "flyers",
    "5": "penguins",
    "6": "bruins",
    "7": "sabres",
    "8": "habs",
    "9": "sens",
    "10": "leafs",
    "12": "canes",
    "13": "panthers",
    "14": "bolts",
    "15": "caps",
    "16": "hawks",
    "17": "wings",
    "18": "preds",
    "19": "blues",
    "20": "flames",
    "21": "avs",
    "22": "oilers",
    "23": "canucks",
    "24": "ducks",
    "25": "stars",
    "26": "kings",
    "28": "sharks",
    "29": "jackets",
    "30": "wild",
    "52": "jets",
    "53": "yotes",
    "54": "knights",
    "55": "kraken"
}
# function to be called daily to receive each day's NHL games in JSON format


def get_daily_games():
    # get today's date, to be used in URL for API request
    today = datetime.date.today()
    today_string = today.strftime("%Y-%m-%d")

    # make a request to NHL API, using today's date, save it into response (should be an XML file)
    response = requests.get(
        "https://statsapi.web.nhl.com/api/v1/schedule?date="+today_string)
    # pull out json from response for easier interaction
    response_json = response.json().get("dates")[0].get("games")
    # pull just the games from the json to a list for easier traversal
    games = response.json().get("dates")[0].get("games")
    return games

# convert each gameTime to EST using dateutil, then return it


def convert_timezone(time):
    utctime = dateutil.parser.parse(time)
    est = utctime.astimezone(pytz.timezone(
        "Canada/Eastern")).strftime("%I%M%p")
    if(est[2] == "0"):
        est = est[0: 2] + est[4:]
    if(est[0] == "0"):
        est = est[1:]
    return est


# deletes channels from the Game Day category (besides game-day-muted)
async def delete_gameday_channel(channel):
    if channel.name != "game-day-muted" and (type(channel) != discord.VoiceChannel):
        await channel.delete()

# adds a gameday channel for an individual game, in a server, in a specific position in a category


async def add_gameday_channel(game, guild, position):
    away = team_ids.get(str(game.get("teams").get(
        "away").get("team").get("id")))
    home = team_ids.get(str(game.get("teams").get(
        "home").get("team").get("id")))
    category = discord.utils.get(
        guild.categories, name="Game Day")
    channel = await guild.create_text_channel(away + "-vs-" + home + "-" + convert_timezone(game.get("gameDate")), category=category, position=position)


def main():
    client = discord.Client()

    # gets list of games from NHL API, to be used to create the GDC's
    games = get_daily_games()

    # Once the bot is ready, execute the code below
    @client.event
    async def on_ready():
        guild = discord.utils.get(client.guilds, name="bottest")

        # create list of channels in "Game Day" category to make removal of old Game Day channels easier
        game_day_channels = guild.channels
        filtered = filter(lambda chan: (chan.category is not None) and chan.category.name ==
                          "Game Day", game_day_channels)
        for item in filtered:
            await delete_gameday_channel(item)

        # creates channels for each game of the day, at the very beginning of the "Game Day" category
        position = 0  # position used here to store each channel properly withing "Game Day" category

        for game in games:
            await add_gameday_channel(game=game, guild=guild, position=position)
            position += 1
    # Runs the bot
    client.run(config.token)


if __name__ == "__main__":
    main()
