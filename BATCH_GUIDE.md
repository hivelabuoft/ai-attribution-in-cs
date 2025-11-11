# Batch Vignette Generator - Quick Guide

## How to Use

### 1. Prepare Your JSON File

Create or edit `vignettes.json` with your vignettes in this format:

```json
[
  {
    "id": 3,
    "course": "Course description",
    "assignedTask": "Task description",
    "vignette": "Full vignette text describing what happened"
  },
  {
    "id": 4,
    "course": "Another course",
    "assignedTask": "Another task",
    "vignette": "Another vignette..."
  }
]
```

**Important:** 
- `id` should be unique numbers (3-102 for your use case)
- Each vignette will generate `pages/<id>.html`

### 2. Add Your OpenAI API Key

Edit `.env` file:
```
OPENAI_API_KEY=sk-your-actual-key-here
```

### 3. Run the Batch Generator

```bash
node batch-generate.js
```

Or specify a custom JSON file:
```bash
node batch-generate.js my-custom-vignettes.json
```

## What Happens

1. Reads all vignettes from the JSON file
2. For each vignette:
   - Sends to OpenAI GPT-4 with few-shot examples
   - Generates structured data
   - Creates HTML file with embedded CSS and JavaScript
   - Saves both `.html` and `.json` files
3. Shows progress for each vignette
4. Displays final summary

## Output

For each vignette with `id: 3`, you'll get:
- `pages/3.html` - Complete standalone HTML page
- `pages/3.json` - Structured data (for reference)

## Example JSON Template for 100 Vignettes

```json
[
  {
    "id": 3,
    "course": "A third-year database systems course",
    "assignedTask": "Design a normalized relational database schema",
    "vignette": "Student used AI to generate initial schema then manually refined it..."
  },
  {
    "id": 4,
    "course": "A second-year data structures course",
    "assignedTask": "Implement an AVL tree",
    "vignette": "Student coded everything manually without AI assistance..."
  },
  {
    "id": 5,
    "course": "...",
    "assignedTask": "...",
    "vignette": "..."
  }
  // ... continue for id 6-102
]
```

## Progress Output Example

```
Reading vignettes from: vignettes.json
Found 100 vignettes to process

[1/100] Processing vignette 3...
  ✓ Generated pages/3.html and pages/3.json
  Scenario: Third-year database student uses AI to generate initial...
  AI Level: AI_GENERATED

[2/100] Processing vignette 4...
  ✓ Generated pages/4.html and pages/4.json
  Scenario: Second-year student implements AVL tree manually without...
  AI Level: NO_AI

...

============================================================
BATCH PROCESSING COMPLETE
============================================================
✓ Successfully generated: 100 files
✗ Failed: 0 files

All generated files saved to: /path/to/pages
```

## Rate Limiting

The script includes a 1-second delay between requests to avoid OpenAI rate limits. For 100 vignettes, expect:
- Processing time: ~100-120 seconds (about 2 minutes)
- Cost: ~100 API calls to GPT-4

## Tips

1. **Test First**: Start with 2-3 vignettes to verify everything works
2. **Check Progress**: The script shows real-time progress for each vignette
3. **Review Output**: Check the generated HTML files in your browser
4. **Backup**: Save your `vignettes.json` file before running

## Troubleshooting

**"Error: Cannot find module 'openai'"**
- Run: `npm install`

**"API key not set"**
- Add your key to `.env` file

**"Rate limit exceeded"**
- Wait a few minutes and try again
- Or increase the delay in `batch-generate.js` (line with `setTimeout`)

**Some vignettes failed**
- Check the error messages at the end
- Failed vignettes can be re-run individually
- Common causes: API timeout, invalid JSON response

## Re-running Failed Vignettes

If some vignettes fail, you can create a new JSON file with just those:

```json
[
  {
    "id": 15,
    "course": "...",
    "assignedTask": "...",
    "vignette": "..."
  }
]
```

Then run: `node batch-generate.js failed-vignettes.json`
