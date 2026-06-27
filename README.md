# Backlog Tracker Template Store

Public JSON template store for Backlog Tracker.

Templates in this repository are used by the Backlog Tracker template browser. Each template is a plain `.json` file inside the `data/` folder. 

## Folder Structure

```text
data/
  gaming-backlog.json
  work-projects.json
  study-plan.json
```

Only JSON files inside `data/` are shown in the template browser.

## Template Format

Use the universal `items` format for new templates:

```json
{
  "schemaVersion": 1,
  "title": "Gaming Backlog",
  "description": "Games to finish or continue later",
  "items": {
    "Elden Ring": {
      "emoji": "🎮",
      "color": "#6750a4",
      "perday": 1,
      "perday_type": "quest"
    },
    "Hollow Knight": {
      "emoji": "🗡️",
      "color": "#006a6a",
      "repeat_days": ["wed"]
    },
    "Cyberpunk 2077": {
      "emoji": "🌃",
      "color": "#f5b400",
      "repeat_days": ["sun", "wed"]
    }
  }
}
```

Study/course templates can use the same format:

```json
{
  "schemaVersion": 1,
  "title": "Class 12 Science",
  "description": "Study backlog template for core subjects",
  "items": {
    "Physics": {
      "emoji": "⚛️",
      "color": "#ff8a65",
      "perday": 1,
      "perday_type": "lecture"
    },
    "Maths": {
      "emoji": "🧮",
      "color": "#4fc3f7"
    },
    "Chemistry": {
      "emoji": "🧪",
      "color": "#ba68c8"
    }
  }
}
```

## Required Fields

- `schemaVersion`: use `1`.
- `title`: display name for the template.
- `items`: object containing the things to track.
- Each item should include:
  - `emoji`: short visual marker.
  - `color`: hex color like `#6750a4`.

## Optional Schedule Fields

Schedule fields are allowed but not required.

- `perday`: number of units expected per day. Example: `"perday": 1`.
- `perday_type`: the unit label for `perday`. Examples: `lecture`, `task`, `episode`, `quest`, `page`, `work item`.
- `repeat_days`: weekly repeat days. Use lowercase three-letter day names:
  - `mon`
  - `tue`
  - `wed`
  - `thu`
  - `fri`
  - `sat`
  - `sun`

Examples:

```json
{
  "items": {
    "Gym": {
      "emoji": "🏋️",
      "color": "#006a6a",
      "repeat_days": ["mon", "wed", "fri"]
    },
    "Weekly Review": {
      "emoji": "📝",
      "color": "#6750a4",
      "repeat_days": ["sun"]
    },
    "Practice Problems": {
      "emoji": "🧮",
      "color": "#4fc3f7",
      "perday": 10,
      "perday_type": "problem"
    },
    "Support Tickets": {
      "emoji": "🎫",
      "color": "#f5b400",
      "perday": 5,
      "perday_type": "ticket"
    }
  }
}
```

Do not add `perday`, `perday_type`, or `repeat_days` if the item does not need a schedule. If `perday` is present and `perday_type` is omitted, the app may show a generic unit.

## Naming Files

Use short lowercase filenames with hyphens:

```text
gaming-backlog.json
work-sprint.json
class-12-science.json
anime-watchlist.json
```

Avoid spaces and special characters in filenames.

## Add a New Template by Pull Request

1. Fork this repository.
2. Create a new branch:

```bash
git checkout -b add-my-template
```

3. Add your JSON file inside the `data/` folder.
4. Make sure the file is valid JSON. You can check it with:

```bash
node -e "JSON.parse(require('fs').readFileSync('data/YOUR_FILE.json', 'utf8')); console.log('valid json')"
```

5. Commit your file:

```bash
git add data/YOUR_FILE.json
git commit -m "Add YOUR TEMPLATE NAME template"
```

6. Push your branch:

```bash
git push origin add-my-template
```

7. Open a pull request to the `main` branch.

