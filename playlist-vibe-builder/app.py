import gradio as gr
import math


# default songs shown in the table
DEFAULT_ROWS = [
    ["From Time", "Drake", 88, 322],
    ["Music and Me", "fakemink", 90, 126],
    ["Boys Don't Cry", "The Cure", 81, 157],
    ["Club Paradise", "Drake", 78, 288],
]


def format_titles(songs):
    return "[" + ", ".join(song["title"] for song in songs) + "]"


# merge sort function
def merge_sort_with_trace(songs, key, trace, depth=0):
    indent = "  " * depth
    trace.append(f"{indent}merge_sort({format_titles(songs)}) by '{key}'") #adds to trace

    # base case if only 1 song its already sorted
    if len(songs) <= 1:
        trace.append(f"{indent}Base case reached -> {format_titles(songs)}") #adds to trace
        return songs

    # split list into two halves
    mid = len(songs) // 2
    left_half = songs[:mid]
    right_half = songs[mid:]
    trace.append(
        f"{indent}Split at index {mid}: left={format_titles(left_half)}, right={format_titles(right_half)}"
    ) #adds to trace

    # recursive calls
    left_sorted = merge_sort_with_trace(left_half, key, trace, depth + 1)
    right_sorted = merge_sort_with_trace(right_half, key, trace, depth + 1)

    merged = []
    i = 0
    j = 0
    trace.append(f"{indent}Merging left/right halves") #adds to trace

    # compare left and right values
    while i < len(left_sorted) and j < len(right_sorted):
        left_val = left_sorted[i][key]
        right_val = right_sorted[j][key]
        trace.append(
            f"{indent}Compare {left_sorted[i]['title']}({left_val}) vs {right_sorted[j]['title']}({right_val})"
        ) #adds to trace
        if left_val <= right_val:
            merged.append(left_sorted[i])
            trace.append(f"{indent}Take left -> {left_sorted[i]['title']}") #adds to trace
            i += 1
        else:
            merged.append(right_sorted[j])
            trace.append(f"{indent}Take right -> {right_sorted[j]['title']}") #adds to trace
            j += 1

    # add leftovers from left side
    while i < len(left_sorted):
        merged.append(left_sorted[i])
        trace.append(f"{indent}Append leftover left -> {left_sorted[i]['title']}") #adds to trace
        i += 1

    # add leftovers from right side
    while j < len(right_sorted):
        merged.append(right_sorted[j])
        trace.append(f"{indent}Append leftover right -> {right_sorted[j]['title']}") #adds to trace
        j += 1

    trace.append(f"{indent}Merged result -> {format_titles(merged)}") #adds to trace
    return merged


def validate_and_normalize(rows):
    songs = []
    errors = []

    # parse energy and duration as integers
    def parse_int_cell(value, field_name, row_idx):
        if value is None:
            errors.append(f"Row {row_idx}: {field_name} is required.")
            return None

        if isinstance(value, str):
            stripped = value.strip()
            if stripped == "":
                errors.append(f"Row {row_idx}: {field_name} is required.")
                return None
            try:
                as_float = float(stripped)
            except ValueError:
                errors.append(
                    f"Row {row_idx}: {field_name} must be an integer."
                )
                return None
        elif isinstance(value, (int, float)):
            as_float = float(value)
        else:
            errors.append(f"Row {row_idx}: {field_name} must be an integer.")
            return None

        if not math.isfinite(as_float) or not as_float.is_integer():
            errors.append(f"Row {row_idx}: {field_name} must be an integer.")
            return None

        return int(as_float)

    if hasattr(rows, "values") and hasattr(rows, "columns"):
        normalized_rows = rows.values.tolist()
    else:
        normalized_rows = rows

    # validate each row
    for idx, row in enumerate(normalized_rows, start=1):
        if row is None:
            continue
        row_values = list(row)
        if len(row_values) < 4:
            row_values += [""] * (4 - len(row_values))
        title_raw, artist_raw, energy_raw, duration_raw = row_values[:4]

        # skip empty rows
        if all(str(value).strip() == "" for value in row_values):
            continue

        title = str(title_raw).strip()
        artist = str(artist_raw).strip()

        if not title:
            errors.append(f"Row {idx}: title is required.")
        if not artist:
            errors.append(f"Row {idx}: artist is required.")

        energy = parse_int_cell(energy_raw, "energy", idx)
        duration = parse_int_cell(duration_raw, "duration", idx)

        # check ranges
        if energy is not None and not (0 <= energy <= 100):
            errors.append(f"Row {idx}: energy must be in range 0-100.")
        if duration is not None and duration <= 0:
            errors.append(f"Row {idx}: duration must be greater than 0.")

        # save valid song
        if (
            title
            and artist
            and energy is not None
            and duration is not None
            and 0 <= energy <= 100
            and duration > 0
        ):
            songs.append(
                {
                    "title": title,
                    "artist": artist,
                    "energy": energy,
                    "duration": duration,
                }
            )

    if len(songs) < 2:
        errors.append("At least 2 valid songs are required.")

    return songs, errors


def run_sort(input_rows, sort_key):
    # run validation
    songs, errors = validate_and_normalize(input_rows)
    if errors:
        return [], "Validation failed:\n" + "\n".join(f"- {error}" for error in errors)

    # run merge sort
    trace = [f"Starting merge sort with {len(songs)} songs, key='{sort_key}'"]
    sorted_songs = merge_sort_with_trace(songs, sort_key, trace)

    # format output table
    output_rows = [
        [song["title"], song["artist"], song["energy"], song["duration"]]
        for song in sorted_songs
    ]
    return output_rows, "\n".join(trace)


with gr.Blocks(
    title="Playlist Vibe Builder",
    css="""
    #sort-by-select label span {
        color: #1d4ed8 !important;
    }
    #sort-by-select input:checked + span {
        color: #1d4ed8 !important;
        font-weight: 600;
    }
    """,
) as demo:
    gr.Markdown(
        """
        # Playlist Vibe Builder
        Enter songs in the table, choose a sort method, and run Merge Sort.
        """
    )

    # gradio input table
    songs_table = gr.Dataframe(
        headers=["title", "artist", "energy", "duration"],
        value=DEFAULT_ROWS,
        row_count=(6, "dynamic"),
        column_count=(4, "fixed"),
        datatype=["str", "str", "number", "number"],
        interactive=True,
        label="Input Playlist",
    )

    # sort selector
    sort_choice = gr.Radio(
        choices=["energy", "duration"],
        value="energy",
        label="Sort By",
        elem_id="sort-by-select",
    )

    sort_btn = gr.Button("Sort Playlist")

    # sorted output and trace
    sorted_table = gr.Dataframe(
        headers=["title", "artist", "energy", "duration"],
        column_count=(4, "fixed"),
        interactive=False,
        label="Sorted Playlist",
    )

    trace_box = gr.Textbox(
        label="Merge Sort Trace",
        lines=18,
        max_lines=30,
        interactive=False,
    )

    sort_btn.click(
        fn=run_sort,
        inputs=[songs_table, sort_choice],
        outputs=[sorted_table, trace_box],
    )


if __name__ == "__main__":
    demo.launch()
