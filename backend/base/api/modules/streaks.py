from datetime import timedelta


def compute_streaks(played_days, today):
    """
    Work out a player's daily play streaks.

    `played_days` is an iterable of `date` objects, one for each run the
    player started (a day on which the player played at least once counts
    as one day of the streak, no matter how many runs were played).

    Returns a dict with:
      current_streak: consecutive days played, ending today or yesterday
                      (0 if the player did not play today or yesterday)
      longest_streak: the longest run of consecutive days ever played
      last_played:    the most recent day played, or None
    """
    days = sorted(played_days)

    if not days:
        return {"current_streak": 0, "longest_streak": 0, "last_played": None}

    longest = streak = 1

    for previous, current in zip(days, days[1:]):
        if (current - previous).days == 1:
            streak += 1
        else:
            streak = 1

        longest = max(longest, streak)

    last_played = days[-1]
    is_alive = last_played >= today - timedelta(days=1)

    return {
        "current_streak": streak if is_alive else 0,
        "longest_streak": longest,
        "last_played": last_played,
    }
