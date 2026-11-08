# Antopik

A desktop widget that helps me learn Korean, with the goal of taking the TOPIK exam within the next two to three years.

It shows a random Korean word or writing rule on my screen. Clicking it opens a full lesson card that I wrote myself, with an explanation, examples and a memory tip. Cards I struggle with come back more often.

![Antopik screenshot](ScreenShots/Antopik%20-%20Desk.png)

A right click on the card shows more details about a word.

![Antopik screenshot](ScreenShots/Antopik%20-%20Desk%20-%20RightClickOnCard.png)
## Features 

- **Always-on-top widget:** showing a random word, its romanization and its meaning
- **Automatic updating:** Every hours, the card changes on it's own. 
- **Lesson card on click:** explanation, examples and an optional memory tip
- **Color-coded categories:** Vocabulary, Key expressions, Grammar, Culture...
- **Known / To review tracking:** with weighted random draw (review > new > known)
- **Right-click menu:** next word, quit
- **Lessons stored as plain JSON files:** one file per category

## Getting started

**Requirements:** Python 3.9+ with Tkinter. Tested on MACOS.

```bash
git clone https://github.com/bizienmaximepro-dev/Antopik.git
cd Antopik
python3 antopik.py
```

## Usage

| Action | Result |
|---|---|
| Left click | Open the lesson card |
| Right click (or Ctrl + click) | Open the menu (next word, quit) |
| `Esc` in a lesson | Close the card |
| ✓ Known / ↻ To review | Save the status of the card |

## Adding your own lessons

Each file in `lessons/` is one category. The filename becomes the category name (`key_expressions.json` → "Key expressions"). A file is a list of cards:

```json
[
  {
    "korean": "물",
    "romanization": "mul",
    "meaning": "water",
    "explanation": "Very common word.",
    "examples": [
      { "korean": "물 주세요", "english": "Water, please" }
    ],
    "tip": "Optional memory tip."
  }
]
```

Required fields: `korean`, `romanization`, `meaning`. Everything else is optional. To add a category, just drop a new `.json` file in `lessons/`.

## Project structure

```
Antopik/
├── antopik.py        
├── lessons/  
    └──  grammar.json
    └── key_expressions.json
    └── vocabulary.json       
├── progress.json               #personal progress
├──  assets/                    #Screenshots 
```

