def longest_hit_streak(results):
    """
    Longest run of correct answers in a row.

    `results` is a list of booleans in the order the movies were answered
    (True = hit, False = miss). Returns 0 for an empty list.
    """
    longest = 0
    current = 0

    for hit in results:
        if hit:
            current += 1
        else:
            longest = max(longest, current)
            current = 0

    return longest
