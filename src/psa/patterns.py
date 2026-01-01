from __future__ import annotations

def max_consecutive_repeats(s: str) -> int:
    """
    Returns the maximum number of consecutive identical characters in s.
    Examples:
      "" -> 0
      "a" -> 1
      "aaab" -> 3
      "abcccdd" -> 3
    """
    if not s:
        return 0

    best = 1
    run = 1

    for i in range(1, len(s)):
        if s[i] == s[i - 1]:
            run += 1
            if run > best:
                best = run
        else:
            run = 1

    return best

def sequential_runs(s: str, min_len: int = 3) -> list[dict]:
    """
    Detects case-insensitive sequential runs (abc, cba, 123, 321).
    Returns factual evidence with positions and sequence.
    """
    if len(s) < min_len:
        return []

    runs: list[dict] = []

    # normalize for comparison, but keep original string for slicing
    norm = s.lower()

    run_start = 0
    run_dir = 0  # +1 or -1
    run_type = None  # "alpha" or "digit"

    def char_type(c: str) -> str | None:
        if c.isalpha():
            return "alpha"
        if c.isdigit():
            return "digit"
        return None

    for i in range(1, len(norm)):
        prev = norm[i - 1]
        curr = norm[i]

        prev_type = char_type(prev)
        curr_type = char_type(curr)

        diff = ord(curr) - ord(prev)

        # valid continuation?
        if (
            prev_type == curr_type
            and prev_type is not None
            and diff in (1, -1)
            and (run_dir == 0 or diff == run_dir)
        ):
            if run_dir == 0:
                run_start = i - 1
                run_dir = diff
                run_type = prev_type
        else:
            # finalize previous run
            if run_dir != 0:
                run_len = i - run_start
                if run_len >= min_len:
                    runs.append({
                        "type": run_type,
                        "direction": "ascending" if run_dir == 1 else "descending",
                        "start": run_start,
                        "end": i,
                        "sequence": s[run_start:i],
                    })

            run_dir = 0
            run_type = None

    # handle run at end
    if run_dir != 0:
        run_len = len(norm) - run_start
        if run_len >= min_len:
            runs.append({
                "type": run_type,
                "direction": "ascending" if run_dir == 1 else "descending",
                "start": run_start,
                "end": len(norm),
                "sequence": s[run_start:],
            })

    return runs

def keyboard_runs_qwerty(s: str, min_len: int = 3) -> list[dict]:
    """
    Detect case-insensitive adjacency runs on QWERTY letter rows.

    Example matches:
      "qwerty"   -> forward
      "asdf"     -> forward
      "lkj"      -> backward

    Only letters are considered.
    Digits are NOT included (handled by sequential runs).
    """

    # If the string is too short, no runs are possible
    if len(s) < min_len:
        return []

    # Define QWERTY keyboard rows (letters only)
    rows = [
        "qwertyuiop",
        "asdfghjkl",
        "zxcvbnm",
    ]

    # Build a lookup table:
    # letter -> (row_index, column_index)
    position = {}
    for row_index, row in enumerate(rows):
        for col_index, char in enumerate(row):
            position[char] = (row_index, col_index)

    # Helper function:
    # checks whether b is adjacent to a on the keyboard
    def adjacency_direction(a: str, b: str) -> int:
        """
        Returns:
          +1  if b is immediately to the RIGHT of a
          -1  if b is immediately to the LEFT of a
           0  if not adjacent or not on same row
        """
        if a not in position or b not in position:
            return 0

        row_a, col_a = position[a]
        row_b, col_b = position[b]

        # Must be on the same keyboard row
        if row_a != row_b:
            return 0

        if col_b == col_a + 1:
            return 1
        if col_b == col_a - 1:
            return -1

        return 0

    # Normalize to lowercase for comparisons,
    # but keep the original string for slicing later
    normalized = s.lower()

    runs: list[dict] = []

    # Track the current run
    run_start = 0      # index where the run begins
    run_direction = 0  # +1 = forward, -1 = backward, 0 = no run

    # Walk through the string character by character
    for i in range(1, len(normalized)):
        prev_char = normalized[i - 1]
        curr_char = normalized[i]

        # Check keyboard adjacency
        direction = adjacency_direction(prev_char, curr_char)

        # Case 1: valid continuation of a run
        if direction != 0 and (run_direction == 0 or direction == run_direction):

            # If this is the start of a new run, mark where it began
            if run_direction == 0:
                run_start = i - 1
                run_direction = direction

        # Case 2: run breaks
        else:
            if run_direction != 0:
                run_length = i - run_start

                # Only record runs long enough to matter
                if run_length >= min_len:
                    runs.append({
                        "type": "keyboard_qwerty",
                        "direction": "forward" if run_direction == 1 else "backward",
                        "start": run_start,
                        "end": i,
                        "sequence": s[run_start:i],
                    })

            # Reset run tracking
            run_direction = 0

    # Handle a run that reaches the end of the string
    if run_direction != 0:
        run_length = len(normalized) - run_start
        if run_length >= min_len:
            runs.append({
                "type": "keyboard_qwerty",
                "direction": "forward" if run_direction == 1 else "backward",
                "start": run_start,
                "end": len(normalized),
                "sequence": s[run_start:],
            })

    return runs