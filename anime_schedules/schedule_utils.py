from datetime import datetime, timedelta
import re
from typing import Union
from requests_html import HTMLSession
from dateutil import parser as dateparser

### GLOBALs ###
SEASONS_INFO = {
    "winter": (1, 3),
    "spring": (4, 6),
    "summer": (7, 9),
    "fall": (10, 12),
}


# Validate a Season Info
def __validate_season_info(season="", year=""):
    if not season.lower() in SEASONS_INFO.keys():
        return (
            False,
            "Invalid season. Must be one of 'winter', 'spring', 'summer', 'fall'.",
        )

    try:
        year = int(year)
    except Exception as e:
        return False, "Invalid year. Year must be a number."

    current_year = datetime.now().year
    if year < 1907 or year > current_year + 2:  # Allowing a 2-year future margin
        return False, f"Invalid year. Year must be between 1907 and {current_year + 2}."

    return True, f"Valid season-year: {season} {year}"


# Get Season form Date (Inner Function)
def __season_from_date(date) -> tuple[str, int]:
    currentMonth = date.month

    currentSeason = None

    for season, (startMonth, endMonth) in SEASONS_INFO.items():
        if startMonth <= currentMonth <= endMonth:
            currentSeason = season
            break

    return (currentSeason, date.year)


# Get next Season Info
def __get_next_season() -> tuple[str, int]:
    current_season, current_year = __season_from_date(datetime.mow())

    seasons = list(SEASONS_INFO.keys())
    next_season_index = (seasons.index(current_season) + 1) % len(seasons)

    # If we are in fall, the next season is winter and the year will change
    if current_season == "fall":
        next_year = current_year + 1
    else:
        next_year = current_year

    next_season = seasons[next_season_index]

    return (next_season, next_year)


# Live Chart (HTML Scrapper)
def __live_chart_base(path="", cookies={}):
    path = f"https://www.livechart.me/{path}"

    try:
        response = HTMLSession().get(path, cookies=cookies)
    except Exception as e:
        return {"success": False, "error": str(e)}

    response = {"success": True, "obj": response}

    return response


# Get HTML data of Schedule and convert!
def __get_anime_schedule_data(
    season="",
    year: Union[str, int] = "",
    type="tv",
    sortby="popularity",
    language="english",
):
    animeType = {
        "tv": "TV Series",
        "movies": "Movie",
        "ovas": "OVA",
        "onas": "ONA",
    }
    if language.lower() not in ["english", "romaji"]:
        language = "english"

    # Cookies are used to get the Anime Data based on the preferences
    cookies = {
        "preferences": f"""{{"titles":"{language.lower()}","sortby":"{sortby}","ongoing":"all","use_24h_clock":false,"night_mode":true,"reveal_spoilers":true}}"""
    }

    # Create path if Year, Season and Type is Declared
    if year != "" and season != "" and type != "":
        path = f"{season.lower()}-{year}/{type}"

    # Get the Server Data
    server_response = __live_chart_base(path, cookies=cookies)
    if not server_response["success"]:
        return server_response

    response = server_response.get("obj")
    anime_card = response.html.find("div.anime-card")

    return_response = {
        "success": True,
        "data": [],
    }

    for card in anime_card:

        try:
            malId = re.search(
                r"/anime/(\d+)",
                card.find(".related-links", first=True)
                .find("a.mal-icon", first=True)
                .attrs.get("href"),
                re.IGNORECASE,
            )
            malId = int(malId.group(1)) if malId else None
        except Exception as e:
            malId = None

        try:
            images = [
                url.strip().split(" ")[0]
                for url in card.find("img", first=True).attrs.get("srcset").split(",")
            ]
        except Exception as e:
            images = []

        try:
            episode = re.search(
                r"EP(\d+)",
                card.find("div.release-schedule-info", first=True).text.strip(),
                re.IGNORECASE,
            )
            episode = int(episode.group(1)) if episode else None
        except Exception as e:
            episode = None

        try:
            match = re.search(
                r"^(\d+|\?)\s+eps\s+×\s+(\d+|\?)m$",
                card.find("div.anime-episodes", first=True).text.strip(),
                re.IGNORECASE,
            )
            if match:
                episodeCount = int(match.group(1)) if match.group(1) != "?" else None
                duration = int(match.group(2)) if match.group(2) != "?" else None
            else:
                episodeCount, duration = None, None
        except Exception as e:
            episodeCount, duration = None, None

        try:
            match = re.search(
                r"(\d+\.\d+)\s+out\s+of\s+10\s+based\s+on\s+(\d+)\s+user\s+ratings",
                card.find("div.anime-avg-user-rating", first=True)
                .attrs.get("title")
                .strip(),
                re.IGNORECASE,
            )
            if match:
                rating = float(match.group(1)) if match.group(1) != "?" else None
                members = int(match.group(2)) if match.group(2) != "?" else None
            else:
                rating, members = None, None
        except Exception as e:
            rating, members = None, None

        try:
            startDateTimestamp = int(
                dateparser.parse(
                    card.find(".anime-date", first=True).text.strip()
                ).timestamp()
            )
        except ValueError as e:
            startDateTimestamp = None

        try:
            episodeCountdown = card.find("time.text-bold", first=True)
            if episodeCountdown:
                nextEpisode = int(episodeCountdown.attrs.get("data-timestamp"))
                if nextEpisode is None:
                    nextEpisode = episodeCountdown.attrs.get("data-intl-time-datetime")
            else:
                nextEpisode = card.find(
                    "a.episode-countdown span.text-bold", first=True
                ).text.strip()
        except Exception as e:
            nextEpisode = None

        try:
            genres = [
                {"id": None, "name": li.text.strip()}
                for li in card.find("ol.anime-tags", first=True).find("li")
            ]
        except Exception as e:
            genres = []

        try:
            studios = [
                {"id": None, "name": li.text.strip()}
                for li in card.find("ul.anime-studios", first=True).find("li")
            ]
        except Exception as e:
            studios = []

        data = {
            "mal_id": malId,
            "title": card.find("h3.main-title", first=True).text.strip(),
            "image": next((url for url in images if url.endswith("small.jpg")), None),
            "image_large": next(
                (url for url in images if url.endswith("large.jpg")), None
            ),
            "synopsis": card.find("div.anime-synopsis", first=True).text.strip(),
            "aired": {
                "from": startDateTimestamp,
                "to": None,
                "string": f"{datetime.fromtimestamp(startDateTimestamp).strftime("%b %d, %Y") if startDateTimestamp else "?"} to ?",
            },
            "next": {
                "timestamp": nextEpisode,
                "episode": episode,
            },
            "status": (
                "Currently Airing"
                if isinstance(nextEpisode, int)
                else "Aired" if nextEpisode == "Released" else "Not yet Aired"
            ),
            "type": animeType.get(type),
            "year": year,
            "season": season,
            "score": rating,
            "scored_by": members,
            "episodes": episodeCount,
            "duration": duration,
            "studios": studios,
            "genres": genres,
            "source": card.find(".anime-source", first=True).text.strip(),
        }

        return_response["data"].append(data)

    return return_response


# Get anime scheduled to release Today!
def __get_anime_scheduled_by_time(hours=24, type="tv", language="english"):
    try:
        hours = int(hours)
    except Exception as e:
        return {"success": False, "message": "Invalid hours Given"}

    season, year = __season_from_date(datetime.now())

    anime_schedule_data = __get_anime_schedule_data(
        season=season, year=year, type=type, sortby="countdown", language=language
    )

    if not anime_schedule_data.get("success"):
        return {
            "success": False,
            "message": anime_schedule_data.get("message", "Server Busy"),
        }

    return_response = {
        "success": True,
        "data": [],
    }

    now = datetime.now()
    next24Hours = now + timedelta(hours=hours)

    for item in anime_schedule_data.get("data", []):
        if not item.get("next", {}).get("timestamp"):
            continue

        episode_date_time = datetime.fromtimestamp(
            item.get("next", {}).get("timestamp")
        )
        if now <= episode_date_time < next24Hours:
            return_response["data"].append(item)
        else:
            break

    return return_response
