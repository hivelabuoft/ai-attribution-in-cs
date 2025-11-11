import OpenAI from 'openai';
import dotenv from 'dotenv';
import fs from 'fs';
import path from 'path';

dotenv.config();

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY
});

const SYSTEM_PROMPT = `You are an expert at creating educational vignettes for research studies on AI attribution in computer science education. Your task is to take course information and assignment descriptions and generate structured data that will be used to create HTML slides.

You will output ONLY valid JSON in the following format (no markdown, no code blocks, just the JSON):

{
  "scenario_brief": "Brief 1-2 sentence description",
  "slide1": {
    "course_name": "Full course name",
    "course_icon": "emoji",
    "learning_objectives": [
      "Objective 1 (8-12 words)",
      "Objective 2 (8-12 words)",
      "Objective 3 (8-12 words)"
    ]
  },
  "slide2": {
    "task": "One sentence task description (10-15 words)",
    "requirements": [
      "Requirement 1 (8-15 words)",
      "Requirement 2 (8-15 words)",
      "Requirement 3 (8-15 words)",
      "Requirement 4 (8-15 words)"
    ],
    "deliverable": "One sentence deliverable (6-12 words)"
  },
  "slide3": {
    "starting_state": "One sentence starting state (8-15 words)",
    "info_cards": [
      {
        "emoji": "emoji",
        "title": "Title (2-4 words)",
        "description": "Description (12-20 words)"
      },
      {
        "emoji": "emoji",
        "title": "Title (2-4 words)",
        "description": "Description (12-20 words)"
      },
      {
        "emoji": "emoji",
        "title": "Title (2-4 words)",
        "description": "Description (12-20 words)"
      }
    ],
    "summary": "2-3 sentences, max 40 words total"
  },
  "slide4": {
    "student_actions": [
      {
        "emoji": "emoji",
        "action": "Action description (8-15 words)"
      },
      {
        "emoji": "emoji",
        "action": "Action description (8-15 words)"
      },
      {
        "emoji": "emoji",
        "action": "Action description (8-15 words)"
      },
      {
        "emoji": "emoji",
        "action": "Action description (8-15 words)"
      }
    ]
  },
  "slide5": {
    "ai_level": "NO_AI or AI_GENERATED",
    "indicator_text": "NO AI ASSISTANCE or AI [VERB PHRASE]",
    "indicator_color": "#7a7a7a or #5a9fd4",
    "role_text": "AI contributed nothing to [domain] or AI [produced/generated] [output]",
    "ai_actions": [
      {
        "emoji": "⛔ or meaningful emoji",
        "action": "Action description"
      },
      {
        "emoji": "⛔ or meaningful emoji",
        "action": "Action description"
      },
      {
        "emoji": "⛔ or meaningful emoji",
        "action": "Action description"
      }
    ],
    "outcome": "Final outcome description",
    "badges": ["Badge 1", "Badge 2"]
  }
}

CRITICAL: Output ONLY the JSON. No explanation, no markdown formatting, no code blocks.`;

const FEW_SHOT_EXAMPLES = [
  {
    role: 'user',
    content: `Course: A second-year course on Human-Computer Interaction (HCI).
Assigned task: Students were asked to develop a plan for a new mobile application, including defining the primary user flow.
Vignette: In a second-year HCI course, the assignment was to design the core user flow for a new mobile application concept. Starting entirely from scratch, the student had only a vague idea for a language-learning app. Without using any generative AI, they spent the initial phase brainstorming on paper, sketching out different screen sequences and decision points for the user registration and first-lesson experience. This conceptual work focused on planning the app's structure and enumerating the necessary features. The student's primary deliverable was a set of these hand-drawn diagrams and notes that outlined the application's logic before any digital wireframing would begin.`
  },
  {
    role: 'assistant',
    content: `{
  "scenario_brief": "Second-year HCI student designs mobile app user flow from scratch without AI assistance",
  "slide1": {
    "course_name": "Second-year Human-Computer Interaction (HCI)",
    "course_icon": "📱",
    "learning_objectives": [
      "Design user flows for interactive applications",
      "Translate abstract ideas into structured interaction sequences",
      "Apply design thinking methodologies"
    ]
  },
  "slide2": {
    "task": "Design core user flow for a mobile language-learning app",
    "requirements": [
      "Start from scratch with a vague concept",
      "Design two flows: user registration + first lesson",
      "Plan app structure and decision points",
      "Document features and logic"
    ],
    "deliverable": "Hand-drawn diagrams and notes (pre-digital phase)"
  },
  "slide3": {
    "starting_state": "Only a vague idea: a language-learning app",
    "info_cards": [
      {
        "emoji": "💭",
        "title": "Concept",
        "description": "General idea with no specific features or structure"
      },
      {
        "emoji": "📋",
        "title": "Planning",
        "description": "No sketches, wireframes, or flows. Started from blank slate"
      },
      {
        "emoji": "🎯",
        "title": "Approach",
        "description": "Had to develop entire UX structure through brainstorming"
      }
    ],
    "summary": "General awareness of language-learning apps, but no concrete plan or structured design. All work developed from scratch."
  },
  "slide4": {
    "student_actions": [
      {
        "emoji": "💡",
        "action": "Brainstormed on paper — explored possibilities for core functionality"
      },
      {
        "emoji": "✏️",
        "action": "Sketched screen sequences and navigation paths by hand"
      },
      {
        "emoji": "🗺️",
        "action": "Mapped decision points where users make choices"
      },
      {
        "emoji": "📝",
        "action": "Documented app logic and features (pre-digital work)"
      }
    ]
  },
  "slide5": {
    "ai_level": "NO_AI",
    "indicator_text": "NO AI ASSISTANCE",
    "indicator_color": "#7a7a7a",
    "role_text": "AI contributed nothing to the design work",
    "ai_actions": [
      {
        "emoji": "⛔",
        "action": "No ideation or brainstorming"
      },
      {
        "emoji": "⛔",
        "action": "No sketch or flow generation"
      },
      {
        "emoji": "⛔",
        "action": "No documentation or refinement"
      }
    ],
    "outcome": "All work (ideation → sketching → documentation) completed by student using traditional manual methods. Hand-drawn diagrams and notes represent 100% student work.",
    "badges": ["100% Student Work", "Manual Methods"]
  }
}`
  },
  {
    role: 'user',
    content: `Course: A senior-level software architecture course.
Task: Students needed to propose and justify an architecture for a large-scale data processing system.
Vignette: For a senior software architecture class, a student had already completed a detailed and valid design document proposing a microservices-based system. Seeking to improve their justification, the student engaged in further conceptual planning without using AI. They manually researched alternative patterns, such as a monolithic architecture with a modular design, and created a private document outlining the pros and cons of this alternative compared to their original choice. This exploration was purely for conceptual comparison to strengthen their final report's discussion section, and did not involve changing the already-working design.`
  },
  {
    role: 'assistant',
    content: `{
  "scenario_brief": "Senior architecture student researches alternative patterns to strengthen design justification",
  "slide1": {
    "course_name": "Senior-level Software Architecture",
    "course_icon": "🏗️",
    "learning_objectives": [
      "Design architectures for large-scale distributed systems",
      "Evaluate and justify architectural decisions with evidence",
      "Compare alternative patterns to strengthen design rationale"
    ]
  },
  "slide2": {
    "task": "Propose and justify architecture for large-scale data processing system",
    "requirements": [
      "Design complete system architecture with justification",
      "Consider scalability, maintainability, and performance requirements",
      "Evaluate alternative architectural patterns",
      "Provide evidence-based rationale for design decisions"
    ],
    "deliverable": "Architecture proposal with justified design decisions"
  },
  "slide3": {
    "starting_state": "Complete and valid microservices-based design document already created",
    "info_cards": [
      {
        "emoji": "✅",
        "title": "Design Status",
        "description": "Detailed microservices architecture proposal completed and validated"
      },
      {
        "emoji": "📊",
        "title": "Design Quality",
        "description": "Working design with proper service decomposition and patterns"
      },
      {
        "emoji": "🎯",
        "title": "Next Step",
        "description": "Needed to strengthen justification by exploring alternatives"
      }
    ],
    "summary": "Student had finished the architecture design. Goal was to improve the justification by researching and comparing alternative patterns."
  },
  "slide4": {
    "student_actions": [
      {
        "emoji": "🔍",
        "action": "Manually researched alternative architectural patterns (monolithic modular)"
      },
      {
        "emoji": "📝",
        "action": "Created comparison document outlining pros and cons"
      },
      {
        "emoji": "⚖️",
        "action": "Analyzed trade-offs between microservices and monolithic approaches"
      },
      {
        "emoji": "📄",
        "action": "Strengthened final report's discussion section with findings"
      }
    ]
  },
  "slide5": {
    "ai_level": "NO_AI",
    "indicator_text": "NO AI ASSISTANCE",
    "indicator_color": "#7a7a7a",
    "role_text": "AI contributed nothing to the research or analysis",
    "ai_actions": [
      {
        "emoji": "⛔",
        "action": "No pattern research or comparison"
      },
      {
        "emoji": "⛔",
        "action": "No pros/cons analysis"
      },
      {
        "emoji": "⛔",
        "action": "No justification writing"
      }
    ],
    "outcome": "All research and conceptual exploration completed by student using manual methods. Comparison document represents 100% student work.",
    "badges": ["100% Student Work", "Manual Research"]
  }
}`
  }
];

async function generateVignetteData(courseInfo, task, vignette) {
  const userPrompt = `Course: ${courseInfo}
Assigned task: ${task}
Vignette: ${vignette}`;

  const completion = await openai.chat.completions.create({
    model: "gpt-4o",
    messages: [
      { role: 'system', content: SYSTEM_PROMPT },
      ...FEW_SHOT_EXAMPLES,
      { role: 'user', content: userPrompt }
    ],
    temperature: 0.7,
  });

  const response = completion.choices[0].message.content.trim();
  
  // Remove markdown code blocks if present
  const jsonMatch = response.match(/```json\s*([\s\S]*?)\s*```/) || response.match(/```\s*([\s\S]*?)\s*```/);
  const jsonText = jsonMatch ? jsonMatch[1] : response;
  
  return JSON.parse(jsonText);
}

function generateHTML(data) {
  return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${data.slide1.course_name} Assignment Vignette</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f5f5f5;
            overflow: hidden;
        }

        .slide-container {
            width: 100vw;
            height: 100vh;
            display: flex;
            transition: transform 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        }

        .slide {
            min-width: 100vw;
            height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            padding: 60px;
            color: #2c3e50;
            text-align: center;
        }

        h1 {
            font-size: 3.5rem;
            margin-bottom: 20px;
            text-shadow: none;
            animation: fadeInDown 0.8s ease-out;
            color: #2c3e50;
        }

        h2 {
            font-size: 2.8rem;
            margin-bottom: 30px;
            text-shadow: none;
            color: #2c3e50;
        }

        .content-box {
            background: white;
            backdrop-filter: none;
            border-radius: 12px;
            padding: 40px;
            margin: 20px;
            max-width: 900px;
            border: 1px solid #e0e0e0;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        }

        .info-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }

        .info-card {
            background: #fafafa;
            padding: 25px;
            border-radius: 8px;
            border: 1px solid #e0e0e0;
            transition: transform 0.3s, box-shadow 0.3s;
        }

        .info-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        }

        .info-card h3 {
            font-size: 1.3rem;
            margin-bottom: 10px;
            color: #2c3e50;
        }

        .info-card p {
            font-size: 1.15rem;
            line-height: 1.7;
            color: #5a5a5a;
        }

        .process-steps {
            display: flex;
            flex-direction: column;
            gap: 25px;
            text-align: left;
            max-width: 800px;
        }

        .step {
            background: #fafafa;
            padding: 25px 30px;
            border-radius: 8px;
            border-left: 4px solid #2c3e50;
            animation: slideInLeft 0.6s ease-out;
            transition: all 0.3s;
        }

        .step:hover {
            transform: translateX(8px);
            background: #f0f0f0;
        }

        .step-content {
            display: inline-block;
            vertical-align: top;
            width: calc(100% - 50px);
            font-size: 1.25rem;
            line-height: 1.8;
            color: #5a5a5a;
        }

        .highlight-box {
            background: #f9f9f9;
            border: 1px solid #d0d0d0;
            border-radius: 8px;
            padding: 30px;
            margin: 30px 0;
            font-size: 1.3rem;
            line-height: 1.8;
            color: #5a5a5a;
        }

        .badge {
            display: inline-block;
            background: #e8e8e8;
            padding: 10px 25px;
            border-radius: 20px;
            margin: 10px;
            font-size: 1.1rem;
            border: 1px solid #d0d0d0;
            color: #2c3e50;
        }

        .ai-indicator {
            background: #2c3e50;
            display: inline-block;
            padding: 15px 35px;
            border-radius: 8px;
            font-size: 1.5rem;
            font-weight: bold;
            margin: 20px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            color: white;
        }

        .navigation {
            position: fixed;
            bottom: 80px;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            gap: 15px;
            z-index: 1000;
        }

        .nav-btn {
            background: white;
            border: 1px solid #d0d0d0;
            color: #2c3e50;
            padding: 15px 30px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1.1rem;
            transition: all 0.3s;
            backdrop-filter: none;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        }

        .nav-btn:hover {
            background: #f5f5f5;
            transform: scale(1.02);
            box-shadow: 0 3px 8px rgba(0, 0, 0, 0.1);
        }

        .nav-btn:disabled {
            opacity: 0.4;
            cursor: not-allowed;
        }

        .progress-dots {
            position: fixed;
            bottom: 30px;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            gap: 12px;
            z-index: 1000;
        }

        .dot {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: #d0d0d0;
            transition: all 0.3s;
            cursor: pointer;
        }

        .dot.active {
            background: #2c3e50;
            transform: scale(1.3);
        }

        @keyframes fadeInDown {
            from {
                opacity: 0;
                transform: translateY(-30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        @keyframes slideInLeft {
            from {
                opacity: 0;
                transform: translateX(-50px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }

        @media (max-width: 768px) {
            h1 { font-size: 2.5rem; }
            h2 { font-size: 2rem; }
            .slide { padding: 30px; }
        }
    </style>
</head>
<body>
    <div class="slide-container" id="slideContainer">
        <!-- Slide 1: Course Level & Objective -->
        <div class="slide">
            <h1>${data.slide1.course_icon} Assignment Scenario</h1>
            
            <div class="content-box" style="max-width: 900px;">
                <h3 style="font-size: 2rem; margin-bottom: 25px; color: #2c3e50;">Course Level & Objective</h3>
                
                <div style="text-align: left; font-size: 1.4rem; line-height: 2; color: #5a5a5a;">
                    <p style="margin-bottom: 35px; color: #2c3e50;">
                        <strong>Course:</strong> ${data.slide1.course_name}
                    </p>
                    
                    <p style="margin-bottom: 15px; color: #2c3e50;">
                        <strong>Learning Objective:</strong>
                    </p>
                    <ul style="margin-left: 25px; font-size: 1.3rem;">
                        ${data.slide1.learning_objectives.map(obj => `<li style="margin-bottom: 15px;">${obj}</li>`).join('\n                        ')}
                    </ul>
                </div>
            </div>
        </div>

        <!-- Slide 2: What Instructor Assigned -->
        <div class="slide">
            <h2>📋 What the Instructor Assigned</h2>
            
            <div class="content-box" style="max-width: 900px;">
                <div style="text-align: left; font-size: 1.4rem; line-height: 2; color: #5a5a5a;">
                    <p style="margin-bottom: 30px; color: #2c3e50;">
                        <strong>Task:</strong> ${data.slide2.task}
                    </p>
                    
                    <p style="margin-bottom: 15px; color: #2c3e50;"><strong>Requirements:</strong></p>
                    <ul style="margin-left: 25px; margin-bottom: 35px; font-size: 1.3rem;">
                        ${data.slide2.requirements.map(req => `<li style="margin-bottom: 12px;">${req}</li>`).join('\n                        ')}
                    </ul>
                    
                    <p style="margin-bottom: 15px; color: #2c3e50;"><strong>Deliverable:</strong></p>
                    <p style="font-size: 1.3rem;">
                        ${data.slide2.deliverable}
                    </p>
                </div>
            </div>
        </div>

        <!-- Slide 3: Prior Knowledge -->
        <div class="slide">
            <h2>📚 Prior Knowledge & Starting Point</h2>
            
            <div class="content-box" style="max-width: 900px;">
                <h3 style="font-size: 1.8rem; margin-bottom: 25px; color: #2c3e50;">What the Student Knew Before Starting</h3>
                <p style="font-size: 1.4rem; line-height: 2; text-align: left; margin-bottom: 30px; color: #5a5a5a;">
                    ${data.slide3.starting_state}
                </p>
                
                <div class="info-grid" style="text-align: left;">
                    ${data.slide3.info_cards.map(card => `
                    <div class="info-card">
                        <h3>${card.emoji} ${card.title}</h3>
                        <p>${card.description}</p>
                    </div>`).join('\n                    ')}
                </div>

                <div class="highlight-box" style="text-align: left; font-size: 1.25rem;">
                    <strong style="color: #2c3e50;">Summary:</strong> ${data.slide3.summary}
                </div>
            </div>
        </div>

        <!-- Slide 4: Student Work -->
        <div class="slide">
            <h2>✏️ What the Student Did</h2>
            
            <div class="content-box" style="max-width: 950px;">
                <h3 style="font-size: 1.8rem; margin-bottom: 30px; color: #2c3e50;">Student's Work Process</h3>

                <div class="process-steps" style="text-align: left;">
                    ${data.slide4.student_actions.map(action => `
                    <div class="step">
                        <span style="font-size: 1.8rem; margin-right: 15px;">${action.emoji}</span>
                        <span class="step-content">
                            ${action.action}
                        </span>
                    </div>`).join('\n                    ')}
                </div>
            </div>
        </div>

        <!-- Slide 5: AI Contribution -->
        <div class="slide">
            <h2>🤖 What the AI Did</h2>
            
            <div class="content-box" style="max-width: 900px;">
                <div class="ai-indicator" style="background: ${data.slide5.indicator_color};">
                    ${data.slide5.ai_level === 'NO_AI' ? '✋' : '🤖'} ${data.slide5.indicator_text}
                </div>

                <h3 style="font-size: 1.8rem; margin-top: 35px; margin-bottom: 20px; color: #2c3e50;">AI's Role in This Assignment</h3>
                <p style="font-size: 1.4rem; line-height: 2; text-align: left; margin-bottom: 30px; color: #5a5a5a;">
                    ${data.slide5.role_text}
                </p>

                <div class="process-steps" style="text-align: left; max-width: 700px; margin: 0 auto;">
                    ${data.slide5.ai_actions.map(action => `
                    <div class="step">
                        <span style="font-size: 1.8rem; margin-right: 15px;">${action.emoji}</span>
                        <span class="step-content">
                            ${action.action}
                        </span>
                    </div>`).join('\n                    ')}
                </div>

                <div class="highlight-box" style="text-align: left; font-size: 1.25rem; margin-top: 40px;">
                    <strong style="color: #2c3e50;">Final Outcome:</strong> ${data.slide5.outcome}
                </div>

                <div style="margin-top: 25px;">
                    ${data.slide5.badges.map(badge => `<div class="badge">${badge}</div>`).join('\n                    ')}
                </div>
            </div>
        </div>
    </div>

    <!-- Navigation -->
    <div class="navigation">
        <button class="nav-btn" id="prevBtn" onclick="changeSlide(-1)">← Previous</button>
        <button class="nav-btn" id="nextBtn" onclick="changeSlide(1)">Next →</button>
    </div>

    <!-- Progress Dots -->
    <div class="progress-dots" id="progressDots"></div>

    <script>
        let currentSlide = 0;
        const slides = document.querySelectorAll('.slide');
        const totalSlides = slides.length;
        const container = document.getElementById('slideContainer');
        const prevBtn = document.getElementById('prevBtn');
        const nextBtn = document.getElementById('nextBtn');
        const progressDots = document.getElementById('progressDots');

        // Create progress dots
        for (let i = 0; i < totalSlides; i++) {
            const dot = document.createElement('div');
            dot.className = 'dot';
            if (i === 0) dot.classList.add('active');
            dot.onclick = () => goToSlide(i);
            progressDots.appendChild(dot);
        }

        function updateSlide() {
            container.style.transform = \`translateX(-\${currentSlide * 100}vw)\`;
            
            // Update progress dots
            document.querySelectorAll('.dot').forEach((dot, index) => {
                dot.classList.toggle('active', index === currentSlide);
            });
            
            // Update button states
            prevBtn.disabled = currentSlide === 0;
            nextBtn.disabled = currentSlide === totalSlides - 1;
        }

        function changeSlide(direction) {
            currentSlide += direction;
            if (currentSlide < 0) currentSlide = 0;
            if (currentSlide >= totalSlides) currentSlide = totalSlides - 1;
            updateSlide();
        }

        function goToSlide(index) {
            currentSlide = index;
            updateSlide();
        }

        // Keyboard navigation
        document.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowLeft') changeSlide(-1);
            if (e.key === 'ArrowRight') changeSlide(1);
        });

        // Initialize
        updateSlide();
    </script>
</body>
</html>`;
}

async function processBatch(jsonFilePath) {
  console.log('Reading vignettes from:', jsonFilePath);
  
  const jsonContent = fs.readFileSync(jsonFilePath, 'utf-8');
  const vignettes = JSON.parse(jsonContent);
  
  console.log(`Found ${vignettes.length} vignettes to process\n`);
  
  const pagesDir = path.join(process.cwd(), 'pages');
  if (!fs.existsSync(pagesDir)) {
    fs.mkdirSync(pagesDir, { recursive: true });
  }
  
  const results = {
    success: [],
    failed: []
  };
  
  for (let i = 0; i < vignettes.length; i++) {
    const vignette = vignettes[i];
    const { id, course, assignedTask, vignette: vignetteText } = vignette;
    
    console.log(`[${i + 1}/${vignettes.length}] Processing vignette ${id}...`);
    
    try {
      // Generate vignette data from OpenAI
      const data = await generateVignetteData(course, assignedTask, vignetteText);
      
      // Generate HTML
      const html = generateHTML(data);
      
      // Save HTML file
      const htmlPath = path.join(pagesDir, `${id}.html`);
      fs.writeFileSync(htmlPath, html);
      
      // Save JSON data for reference
      const jsonPath = path.join(pagesDir, `${id}.json`);
      fs.writeFileSync(jsonPath, JSON.stringify(data, null, 2));
      
      console.log(`  ✓ Generated pages/${id}.html and pages/${id}.json`);
      console.log(`  Scenario: ${data.scenario_brief.substring(0, 60)}...`);
      console.log(`  AI Level: ${data.slide5.ai_level}\n`);
      
      results.success.push(id);
      
      // Add a small delay to avoid rate limiting
      if (i < vignettes.length - 1) {
        await new Promise(resolve => setTimeout(resolve, 1000));
      }
      
    } catch (error) {
      console.error(`  ✗ Failed to process vignette ${id}:`, error.message);
      results.failed.push({ id, error: error.message });
    }
  }
  
  // Summary
  console.log('\n' + '='.repeat(60));
  console.log('BATCH PROCESSING COMPLETE');
  console.log('='.repeat(60));
  console.log(`✓ Successfully generated: ${results.success.length} files`);
  console.log(`✗ Failed: ${results.failed.length} files`);
  
  if (results.failed.length > 0) {
    console.log('\nFailed IDs:');
    results.failed.forEach(f => console.log(`  - ID ${f.id}: ${f.error}`));
  }
  
  console.log(`\nAll generated files saved to: ${pagesDir}`);
}

// Main execution
const args = process.argv.slice(2);
const jsonFilePath = args[0] || 'vignettes.json';

processBatch(jsonFilePath).catch(error => {
  console.error('Fatal error:', error);
  process.exit(1);
});
