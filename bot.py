from dis import disco
import discord
import datetime
import pytz
import dateutil.parser
import requests
import config

client = discord.Client()
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
# BOT_URL = https://discord.com/api/oauth2/authorize?client_id=947937415862059108&permissions=2064&scope=bot
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
    if(est[0] == "0"):
        est = est[1:]
    return est


def main():
    games = get_daily_games()

    @client.event
    async def on_ready():
        guild = discord.utils.get(client.guilds, name="bottest")

        # deletes channels from the Game Day category (besides game-day-muted)
        # TODO figure out how to delete specific channels, i.e. gameday category channels BESIDES game-day-muted
        game_day_channels = guild.
        # creates channels for each game of the day
        for game in games:
            away = team_ids.get(str(game.get("teams").get(
                "away").get("team").get("id")))
            home = team_ids.get(str(game.get("teams").get(
                "home").get("team").get("id")))
            channel = await guild.create_text_channel(away + "-vs-" + home + "-" + convert_timezone(game.get("gameDate")))
    client.run(config.token)


if __name__ == "__main__":
    main()
