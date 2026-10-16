def hit_rate_percent(hits, misses):
    """
    Percentage of correct answers as a whole number.

    The value is rounded to the nearest integer, and halves round up
    (62.5% is shown as 63%). Returns 0 when nothing has been played yet.
    """
    attempts = hits + misses

    if attempts == 0:
        return 0

    return round(hits / attempts * 100)


def average_points(total_points, finished_runs):
    """Average points per finished run, with two decimals (0 if none)."""
    if finished_runs == 0:
        return 0.0

    return round(total_points / finished_runs, 2)
