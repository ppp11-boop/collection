# Finish and submit this collection

Most of the structure is complete. Your job is to add your own media and replace the bracketed details in `records.json`.

## 1. Rename the folder and statement

Replace `studentID` and `studentName` with your real details in both names:

- Folder: `studentID-studentName-collection`
- Statement: `studentID-studentName-collection-concept.md`

Example: `21012345-ChanTaiMan-collection`

## 2. Add your media

Put your files inside `media/` using the exact filenames listed in `MEDIA-CHECKLIST.md`. If your phone records audio as `.mp3` or `.wav` rather than `.m4a`, rename the matching `file` value in `records.json` too.

Do not invent or copy encounters you did not make. You may adjust titles, descriptions, `not_captured` and certainty so they honestly match what you recorded.

## 3. Complete `records.json`

Replace every bracketed placeholder:

- `[ENTER DATE AND TIME]` - for example, `2026-09-14 08:35`
- `[ENTER PLACE]` - for example, `Bathroom, home, Kowloon`
- `[ENTER YOUR NAME]` - use the same recorder name throughout if you made every record

Keep exactly 20 records. Valid types are `image`, `sound` and `text`. Valid certainty values are `high`, `medium` and `low`.

Tip: use Find and Replace to change all 20 recorder and place placeholders at once.

## 4. Personalize the statement

Open `studentID-studentName-collection-concept.md`. The draft is already under 500 words and answers the three required points. Edit it into your own voice and replace the GitHub placeholder with your real repository link.

## 5. Preview the app

Do not double-click `collection.html`, because browsers may block it from reading `records.json`. Run a local server from inside the collection folder.

If Python is installed:

```bash
python3 -m http.server 8000
```

Then open <http://localhost:8000>.

Alternatively, open the folder in Visual Studio Code and use the Live Server extension.

After saving changes to `records.json`, refresh the browser to see the updated date, time and `not_captured` text.

To enter a record's date and time, replace the text after `"date":` while keeping the quotation marks. Example:

```json
"date": "2026-09-15 04:30"
```

To change what was not captured, replace the sentence after `"not_captured":` while keeping the quotation marks and comma. Example:

```json
"not_captured": "The feeling of the paper and what happened after the photograph.",
```

## 6. Validate and submit

If Python is installed, run:

```bash
python3 validate.py
```

Fix every reported error. Then compress the renamed folder into exactly:

`studentID-studentName-collection.zip`

Upload that ZIP to Moodle before the deadline.
