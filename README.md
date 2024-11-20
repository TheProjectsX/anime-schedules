# Anime Schedule API!

Get Anime Schedule Information's via this simple python module!

## Installation:

```bash
pip install git+https://github.com/TheProjectsX/anime-schedules.git
```

#### Upgrade:

```bash
pip uninstall anime-schedules && pip install git+https://github.com/TheProjectsX/anime-schedules.git
```

## Methods Available:

-   validateSeasonInfo
-   getCurrentSeason
-   getNextSeason
-   getSeasonOfDate
-   getCurrentSeasonAnimeScheduled
-   getAnimeScheduleOfSeason
-   getAnimeScheduleOfToday
-   getAnimeScheduleOfNextHours

## Usages:

```python
import anime_schedules as ani

season, year = ani.getCurrentSeason()

schedule_data = ani.getCurrentSeasonAnimeScheduled()

```

Here's a documentation in markdown format that you can use in your GitHub `README.md`:

## Function Documentation

### `validateSeasonInfo(season="", year: Union[str, int] = "")`

Validate a Season info (Season name and Season Year).

#### Arguments:

-   `season`: A season name (e.g., "winter", "spring", "summer", "fall").
-   `year`: A year (string or integer).

#### Returns:

```python
{
    "valid": [True || False],
    "message": Validation Message
}
```

---

### `getCurrentSeason() -> tuple[str, int]`

Get the current season information.

#### Returns:

```python
(season_name, season_year)
```

---

### `getNextSeason() -> tuple[str, int]`

Get the next season information.

#### Returns:

```python
(season_name, season_year)
```

---

### `getSeasonOfDate(date: Union[str, int])`

Get the season information based on a given date.

#### Arguments:

-   `date`: A datetime string or timestamp.

#### Returns:

```python
(season_name, season_year)
```

---

### `getCurrentSeasonAnimeScheduled(type="tv", sortby="popularity", language="english")`

Get anime scheduled to release this current season.

#### Arguments:

-   `type`: Type of Anime [tv || movies || ovas || all] (Default: "tv").
-   `sortby`: Sort the anime by [popularity || countdown || title || airdate || anime.avg_rating] (Default: "popularity").
-   `language`: Anime title language [english || romaji] (Default: "english").

#### Returns:

Anime scheduled data for the current season.

---

### `getAnimeScheduleOfSeason(season="", year="", type="tv", sortby="popularity", language="english")`

Get anime scheduled to release in the given season and year.

#### Arguments:

-   `season`: Season name (e.g., "winter", "spring", "summer", "fall").
-   `year`: Year of the season.
-   `type`: Type of Anime [tv || movies || ovas || all] (Default: "tv").
-   `sortby`: Sort the anime by [popularity || countdown || title || airdate || anime.avg_rating] (Default: "popularity").
-   `language`: Anime title language [english || romaji] (Default: "english").

#### Returns:

Anime scheduled data for the given season.

---

### `getAnimeScheduleOfToday(type="tv", language="english")`

Get anime scheduled to release today or within the next 24 hours.

#### Arguments:

-   `type`: Type of Anime [tv || movies || ovas || all] (Default: "tv").
-   `language`: Anime title language [english || romaji] (Default: "english").

#### Returns:

Anime scheduled data for today.

---

### `getAnimeScheduleOfNextHours(hours=24, type="tv", language="english")`

Get anime scheduled to release from now until the next specified number of hours.

#### Arguments:

-   `hours`: Number of hours from now (Default: 24).
-   `type`: Type of Anime [tv || movies || ovas || all] (Default: "tv").
-   `language`: Anime title language [english || romaji] (Default: "english").

#### Returns:

Anime scheduled data for the next specified hours.
