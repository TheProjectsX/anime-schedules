from datetime import datetime
from dateutil import parser as dateparser
from typing import Union
import schedule_utils

### Internal Function(s) Processed ###


# Validate a Season Info
def validateSeasonInfo(season="", year: Union[str, int] = ""):
    """
    Validate a Season info (Season name and Season Year)

    ### Arguments:
    - season: A season name
    - year: A year

    ### Returns a Dict:
    ```
    {
        "valid": [True || False],
        "message": Validation Message
    }
    ```
    """

    validSeason, msg = schedule_utils.__validate_season_info(season=season, year=year)

    return {"valid": validSeason, "message": msg}


# Get current Anime Season
def getCurrentSeason() -> tuple[str, int]:
    """
    Get the Current Season info: Season name and Season Year.

    #### Returns a Tuple of:
    ```
    (season_name, season_year)
    ```
    """
    return schedule_utils.__season_from_date(datetime.now())


# Get current Anime Season
def getNextSeason() -> tuple[str, int]:
    """
    Get the Next Season info: Season name and Season Year.

    #### Returns a Tuple of:
    ```
    (season_name, season_year)
    ```
    """
    return schedule_utils.__get_next_season()


# Get Season based on Date
def getSeasonOfDate(date: Union[str, int]):
    """
    Get the Season info Based on Given Date: Season name and Season Year.
    #### Argument:
    - date: A Datetime string or Timestamp

    #### Returns a Tuple of:
    ```
    (season_name, season_year)
    ```
    """

    try:
        parsedDate = dateparser.parse(date)
    except Exception as e:
        return (None, None)

    return schedule_utils.__season_from_date(parsedDate)


### External APIs in Use ###


# Get Schedules anime data of current Season
def getCurrentSeasonAnimeScheduled(type="tv", sortby="popularity", language="english"):
    """
    Get anime scheduled to release this Season

    #### Arguments:
    - type: Type of Anime [tv || movies || ovas || all]
    - sortby: Sort the Anime by [popularity || countdown || title || airdate || anime.avg_rating]
    - language: Anime title Language [english || romaji]
    """

    season, year = schedule_utils.__season_from_date(datetime.now())

    animeScheduledData = schedule_utils.__get_anime_schedule_data(
        season=season, year=year, type=type, sortby=sortby, language=language
    )
    return animeScheduledData


# Get Scheduled anime of given Season
def getAnimeScheduleOfSeason(
    season="", year="", type="tv", sortby="popularity", language="english"
):
    """
    Get anime scheduled to release this Season

    #### Arguments:
    - type: Type of Anime [tv || movies || ovas || all]
    - sortby: Sort the Anime by [popularity || countdown || title || airdate || anime.avg_rating]
    - language: Anime title Language [english || romaji]
    """

    validSeason, msg = schedule_utils.__validate_season_info(season=season, year=year)
    if not validSeason:
        return {"success": False, "message": msg}

    animeScheduledData = schedule_utils.__get_anime_schedule_data(
        season=season, year=year, type=type, sortby=sortby, language=language
    )
    return animeScheduledData


# Get Anime Scheduled to Release Today
def getAnimeScheduleOfToday(type="tv", language="english"):
    """
    Get anime scheduled to release Today or more precisely in next 24 hours

    #### Arguments:
    - type: Type of Anime [tv || movies || ovas || all]
    - language: Anime title Language [english || romaji]
    """

    animeScheduledData = schedule_utils.__get_anime_scheduled_by_time(
        hours=24, type=type, language=language
    )
    return animeScheduledData


# Get Anime Scheduled to Release by next n Hours
def getAnimeScheduleOfNextHours(hours=24, type="tv", language="english"):
    """
    Get anime scheduled to release from now to next n Hours

    #### Arguments:
    - hours: Next n Hours
    - type: Type of Anime [tv || movies || ovas || all]
    - language: Anime title Language [english || romaji]
    """
    try:
        hours = int(hours)
    except Exception as e:
        return {"success": False, "message": "Invalid hours Given"}

    animeScheduledData = schedule_utils.__get_anime_scheduled_by_time(
        hours=hours, type=type, language=language
    )
    return animeScheduledData
