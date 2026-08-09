# Contributing to Backlog Tracker Templates

Thanks for contributing a template! Please follow these guidelines so your submission gets merged quickly.

The easiest way to make a template is to set it up in the app, then use **Settings → Backup & Restore → Export Backlog Data → Template Only → Download**. This exports a file the app can re-import directly.

## Template Format

```json
{
  "schemaVersion": 1,
  "title": "Backlog",
  "description": "Shared Backlog Tracker template",
  "items": {
    "Elden Ring": {
      "emoji": "🎮",
      "color": "#6750a4",
      "growth_mode": "none",
      "completion_mode": "todo"
    },
    "Physics": {
      "emoji": "📚",
      "color": "#4fc3f7",
      "growth_mode": "none",
      "completion_mode": "backlog"
    },
    "Math": {
      "emoji": "📚",
      "color": "#ba68c8",
      "growth_mode": "perday",
      "completion_mode": "backlog",
      "perday": 1,
      "perday_type": "tasks"
    },
    "Code": {
      "emoji": "📚",
      "color": "#81c784",
      "growth_mode": "repeat",
      "completion_mode": "backlog",
      "perday": 1,
      "repeat_days": ["thu", "sun", "tue"]
    }
  },
  "theme": "dark"
}
```



## Field Reference

This is validated exactly as the app validates it on import, so a file that fails these rules will be rejected there too.

### `schemaVersion` (optional)

Must be a number. If present, must be `1` or lower.

### `title` (optional)

Display name for the template. Falls back to `"Imported Course"` if missing.

### `description` (optional)

Short summary shown in the template browser.

### `items` (required)

An object keyed by entry name. Each key must be a non-empty (after trimming) string. At least one item is required.

> The older key name `subjects` is also still accepted for backward compatibility, but new templates should use `items`.

Each item may include:

| Field | Type | Default | Notes |
|---|---|---|---|
| `emoji` | string | `📚` | Trimmed, truncated to 15 characters. |
| `color` | string | `#ba68c8` | Must be a 6-digit hex color, e.g. `#6750a4`. |
| `growth_mode` | `"none"` \| `"perday"` \| `"repeat"` | inferred | If omitted, inferred from other fields: `perday`/`daily_increase` present → `perday`; `repeat_days` present → `repeat`; otherwise `none`. |
| `completion_mode` | `"todo"` \| `"backlog"` | `"backlog"` | `todo` = one-off task. `backlog` = ongoing accumulating count. |
| `perday` | number ≥ 0 | — | Amount added per day. Also accepted as `daily_increase`. Required for meaningful `perday` or `repeat` growth. |
| `perday_type` | string | — | Unit label for `perday`, e.g. `lecture`, `task`, `tasks`. Trimmed, truncated to 32 characters. |
| `repeat_days` | array of strings | — | Lowercase three-letter day names only: `mon`, `tue`, `wed`, `thu`, `fri`, `sat`, `sun`. Duplicates are removed automatically. |

Do not set both `perday`/`daily_increase` and `repeat_days` without an explicit `growth_mode` — the importer will still accept it but flags it internally as a schedule conflict, so the behavior is ambiguous. Set `growth_mode` explicitly if an item genuinely needs both.

### `theme` (optional)

`"dark"` or `"light"`. Defaults to `"dark"` if omitted or invalid.

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
