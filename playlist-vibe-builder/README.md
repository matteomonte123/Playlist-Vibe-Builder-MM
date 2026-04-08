# Playlist Vibe Builder using Merge Sort

A gradio app that uses merge sort to sort an inputed playlist by either energy or duration.

## Chosen Problem

**Playlist Vibe Builder**

The app works with an inputed list of songs. Each song needs a:
- title
- artist
- energy (0 to 100)
- duration (seconds)
There is are default songs in the list. These are meant to be edited so the user can input their own songs. Also I included the ability to add rows and columns.

## Chosen Algorithm

Merge sort is the algorithm I used.
- O(n log n) performance
- It is stable (<= branch keeps original order for equal keys)
- Its split/merge structure is pretty easy to explain espcieally with the trace logs i added.

Preconditions and assumptions:
- Each row must include non-empty title and artist.
- energy must be numeric and between 0-100.
- duration must be numeric and greater than 0

## Demo 

- Screenshot in folder


## Problem Breakdown and Computational Thinking

### Flowchart

- Screenshot in folder


### Decomposition

- Make a app where the user can input a playlist into like an excel style sheet. Use merge sort to sort rows containing songs, artists, energy, and duration. Sorting should be done by duration or by energy. Must return the specified sorted playlist.

### Pattern Recognition

- Repeatedly split the playlist in two, recursively sort the two, and merge by repeatedly comparying elements in the two.

### Abstraction

- Ignore displaying the state and positions of the pointers in the logs or trace. 


### Algorithm Design (Input -> Process -> Output)

- Input: songs in rows, including their energy and length. Process: make sure the rows contain integers, and run merge sort, log each step so we have a trace of what the algorithm is doing during the process. Output: Fully sorted table and a trace of the process.

## Steps to Run (Local)
1. Open a terminal in the project folder.
2. (Optional) Create a virtual environment:
   `py -3 -m venv .venv`
3. Activate the virtual environment:
   `.\.venv\Scripts\Activate.ps1`
4. Install dependencies:
   `py -3 -m pip install -r requirements.txt`
5. Start the app:
   `py -3 app.py`
6. Open the local Gradio URL shown in terminal.

What to do in the app:
- Edit/add songs in the input table (title, artist, energy, duration).
- Choose sort key (energy or duration).
- Click Sort Playlist.
- View sorted output table and full merge sort trace log.

## Testing:

  I tested:
   - Valid songs with energy sorting
   - valid songs with duration sorting
   - empty rows/columns
   - energy outside the range of 0-100
   - duration <=0
   - non integer inputs

  Expected:
   - Validation messages
   - Rows sort correctly if valid

  Actual:
   - Errors with validity display in the trace box
   - Playlist apears sorted 


## Hugging Face & Github Link
https://huggingface.co/spaces/mxtteo/Playlist-Vibe-Builder-MM
https://github.com/matteomonte123/Playlist-Vibe-Builder-MM/tree/main/playlist-vibe-builder

## File Structure
Playlist-vibe-builder
        app.py
        README.md
        requirements.txt
        playlist-vibe-builder-screenshots

## Author and Acknowledgment

Author:
- Matteo Montemarano, CISC 121 001, 20392850

# AI Disclosure:
- I included all the screenshots of my AI use in the screenshot folder. I Also included my original code in a .txt file. Quick breakdown of my use: I wrote a shell of what I wanted, had a code that asked user to input songs, with title, artist, duration, energy, and when typed 'done' it would prompt for sorting method, either energy or duration. The code would then run merge sort and output the sorted playlist. I had no Idea how to use gradio and I just wanted my idea to be complete, I then told codex to help me implement the gradio ui, and it ended up changing ALOT. This is level 4 AI usage. I wrote comments not super specific but they describe the core steps of the merge sort and I was able to write a few comments on the gradio code. Everything is included in the screenshots.
