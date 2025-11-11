# Vignette Generator

Generate HTML vignette pages using OpenAI GPT-4 based on course descriptions and assignment scenarios.

## Setup

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Add your OpenAI API key:**
   Open `.env` and replace `your_api_key_here` with your actual OpenAI API key:
   ```
   OPENAI_API_KEY=sk-your-actual-api-key-here
   ```

## Usage

### Basic Command

```bash
node generate-vignette.js "<course>" "<task>" "<vignette>" <page_number>
```

### Parameters

- `<course>`: Brief description of the course (e.g., "A third-year database systems course")
- `<task>`: The assignment task given to students
- `<vignette>`: Full scenario description of what the student did
- `<page_number>`: Output file number (e.g., 3 creates `pages/3.html`)

### Examples

#### Example 1: Database Course (AI-Generated)
```bash
node generate-vignette.js \
  "A third-year database systems course" \
  "Students were asked to design a normalized relational database schema for an e-commerce platform" \
  "In a third-year database course, a student was assigned to design a normalized database schema for an e-commerce system. The student used ChatGPT to generate an initial set of tables and relationships based on their requirements document. The AI produced a complete ER diagram with entities for Users, Products, Orders, and Reviews, including primary keys, foreign keys, and cardinality. The student then manually reviewed the schema, identified normalization issues, and refined the design to reach 3NF. The final deliverable included both the AI-generated initial schema and the student's refined version with annotations explaining the improvements." \
  3
```

#### Example 2: No AI Assistance
```bash
node generate-vignette.js \
  "A second-year data structures course" \
  "Implement a balanced binary search tree from scratch" \
  "For a data structures assignment, students were required to implement a self-balancing AVL tree in Java. The student started with an empty file and manually coded all the insertion, deletion, and rotation methods. They drew diagrams on paper to understand the rotation cases, then translated their understanding into working code. Through trial and error and manual debugging, they created a fully functional AVL tree implementation. All code, comments, and test cases were written entirely by the student without any AI assistance." \
  4
```

#### Example 3: Security Course
```bash
node generate-vignette.js \
  "A senior-level cybersecurity course" \
  "Perform a security audit of a web application and write a penetration testing report" \
  "In a cybersecurity course, students conducted security audits on provided web applications. One student manually tested for common vulnerabilities including SQL injection, XSS, and CSRF. After identifying several security flaws through manual testing and code review, they used ChatGPT to help structure their penetration testing report. The AI generated a professional report template with standard sections (Executive Summary, Methodology, Findings, Recommendations). The student filled in all technical details, vulnerability descriptions, and proof-of-concept code themselves, but the AI provided the organizational framework and professional language for the report structure." \
  5
```

## Output

The generator creates two files:
- `pages/<N>.html` - The complete HTML vignette page
- `pages/<N>.json` - The structured data used to generate the page (for reference)

## How It Works

1. **Few-shot Learning**: The script includes two complete examples (from pages/1.html and pages/2.html) to guide the AI
2. **Structured Output**: AI generates JSON with all slide content
3. **HTML Generation**: The JSON is transformed into a complete HTML page using the exact styling from your templates
4. **Automatic Detection**: The AI determines whether the scenario involves AI assistance (AI_GENERATED) or not (NO_AI)

## Customization

To modify the output format, edit:
- **System prompt**: Change `SYSTEM_PROMPT` in `generate-vignette.js`
- **HTML template**: Modify the `generateHTML()` function
- **Styling**: Update the CSS within the `generateHTML()` function

## Troubleshooting

**"Error: OPENAI_API_KEY is not set"**
- Make sure you've added your API key to `.env`

**"API Response: 401"**
- Your API key is invalid or expired

**"JSON parsing error"**
- The AI occasionally returns malformed JSON. Try running again.

**Rate limiting**
- If generating many vignettes, add delays between requests

## Tips for Best Results

1. **Be specific** in your vignette description
2. **Include details** about what the student did vs. what AI did
3. **Mention deliverables** explicitly (e.g., "report", "code", "diagrams")
4. **Specify the AI tool** if applicable (e.g., "ChatGPT", "GitHub Copilot")
5. **Describe the work process** step-by-step
