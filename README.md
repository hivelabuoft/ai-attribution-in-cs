# AI Attribution Study - Individual Page System

This system displays different study scenarios as separate HTML files. Each page contains its own CSS and JavaScript for complete independence.

## How it works

### URL Structure
- Home page: `your-domain.com/ai-attribution-in-cs/`
- Page 1: `your-domain.com/ai-attribution-in-cs/pages/1.html`
- Page 2: `your-domain.com/ai-attribution-in-cs/pages/2.html`
- Page N: `your-domain.com/ai-attribution-in-cs/pages/N.html`

### Files Structure
```
ai-attribution-in-cs/
├── index.html       # Home page with navigation to all scenarios
├── pages/           # Individual page files
│   ├── 1.html      # Security course scenario
│   ├── 2.html      # Statistics course scenario
│   └── ...         # Additional scenarios
└── README.md        # This file
```

## Adding New Pages

To add a new page (e.g., page 3):

1. Create `pages/3.html` with the complete HTML structure including CSS and JavaScript
2. Update `index.html` to add a link to the new page in the page grid

### Template for New Page
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Your Scenario Title</title>
    <style>
        /* Include all CSS styles here */
    </style>
</head>
<body>
    <a href="../index.html" class="home-btn">← Home</a>
    
    <div class="slide-container" id="slideContainer">
        <!-- Your slides here -->
    </div>

    <!-- Navigation -->
    <div class="navigation">
        <button class="nav-btn" id="prevBtn" onclick="changeSlide(-1)">← Previous</button>
        <button class="nav-btn" id="nextBtn" onclick="changeSlide(1)">Next →</button>
    </div>

    <div class="progress-dots" id="progressDots"></div>

    <script>
        /* Include all JavaScript here */
    </script>
</body>
</html>
```

## Features

1. **Independent Pages**: Each scenario is a complete, standalone HTML file
2. **Self-Contained**: All CSS and JavaScript included in each page
3. **Slide Navigation**: Each page supports multiple slides with navigation
4. **Responsive Design**: Works on desktop and mobile devices
5. **Home Navigation**: Easy return to home page from any scenario
6. **Backward Compatibility**: Old URL format (?id=1) automatically redirects

## Deployment

### GitHub Pages
1. Push this folder to a GitHub repository
2. Enable GitHub Pages in repository settings
3. Your site will be available at `username.github.io/repository-name/ai-attribution-in-cs/`

### Local Testing
Open any HTML file directly in a web browser:
- `index.html` - Home page
- `pages/1.html` - Security scenario
- `pages/2.html` - Statistics scenario

## Available Scenarios

### Page 1: Security Course (pages/1.html)
- **Course**: Security Course
- **Assignment**: Penetration test plan for online banking portal
- **AI Role**: Generated complete test plan including SQL injection, XSS, and authentication tests

### Page 2: Statistics Course (pages/2.html)
- **Course**: Statistics Course  
- **Assignment**: Customer satisfaction data analysis
- **AI Role**: Performed statistical analysis, created visualizations, provided interpretations

## Customization

### Adding a New Scenario
1. Copy an existing page file (e.g., `1.html`)
2. Rename it with the next number (e.g., `3.html`)
3. Update the content, title, and styling as needed
4. Add a card for the new page in `index.html`

### Styling
Each page contains its own complete CSS. You can:
- Modify colors by changing the CSS color values
- Adjust typography by updating font-family and sizes
- Change animations by modifying the @keyframes rules