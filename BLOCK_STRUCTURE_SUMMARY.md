# Qualtrics Survey Block Structure Summary

## Overview
Successfully created a Qualtrics survey with 102 unique scenarios (S1-S102) across two branches:
- **Student Branch**: 102 groups with iframe vignettes + per-vignette questions + post-vignette reflection
- **Teaching Branch**: 102 groups with per-vignette questions + post-vignette reflection (no iframes)

## Block Counts

### Total Blocks: 519

#### Student Branch Blocks:
- **100 iframe blocks** (BL_S3Generated - BL_S102Generated): Display vignette pages
- **102 per-vignette blocks** (BL_PerVig_S1 - BL_PerVig_S102): Questions about the vignette
- **102 post-vignette blocks** (BL_PostVig_S1 - BL_PostVig_S102): Reflection questions

#### Teaching Branch Blocks:
- **102 per-vignette blocks** (BL_PerVig_T1 - BL_PerVig_T102): Questions about the scenario
- **102 post-vignette blocks** (BL_PostVig_T1 - BL_PostVig_T102): Reflection questions

## Block Uniqueness

### Why Each Scenario Needs Unique Blocks

Even though the questions are **identical** across all per-vignette and post-vignette blocks, each scenario requires its own **unique block ID** because:

1. **Data Separation**: Qualtrics uses block IDs to organize responses. If all groups shared the same block, responses would be indistinguishable.

2. **Scenario Tracking**: Unique block IDs ensure that when a participant sees S5, their responses are tagged with BL_PerVig_S5, making it clear which scenario they experienced.

3. **Analysis**: This allows filtering responses by scenario during data analysis (e.g., "show me all responses to scenario 42").

## Group Structure

### Student Branch Groups (S1-S102)

Each Student group contains 3 blocks:

```
S1:
  1. BL_9za7vBZGWQqAZts (existing S1 iframe)
  2. BL_PerVig_S1 (per-vignette questions)
  3. BL_PostVig_S1 (post-vignette reflection)

S3 (example):
  1. BL_S3Generated (iframe: pages/3)
  2. BL_PerVig_S3 (per-vignette questions)
  3. BL_PostVig_S3 (post-vignette reflection)

S102:
  1. BL_S102Generated (iframe: pages/102)
  2. BL_PerVig_S102 (per-vignette questions)
  3. BL_PostVig_S102 (post-vignette reflection)
```

### Teaching Branch Groups (T1-T102)

Each Teaching group contains 2 blocks:

```
S1:
  1. BL_PerVig_T1 (per-vignette questions)
  2. BL_PostVig_T1 (post-vignette reflection)

S102:
  1. BL_PerVig_T102 (per-vignette questions)
  2. BL_PostVig_T102 (post-vignette reflection)
```

## Randomization Settings

### Student Branch BlockRandomizer
- **SubSet**: 5 (selects 5 of 102 groups)
- **EvenPresentation**: True (balanced distribution across participants)

### Teaching Branch BlockRandomizer
- **SubSet**: 5 (selects 5 of 102 groups)
- **EvenPresentation**: True (balanced distribution across participants)

## FlowID Structure

### Student Branch
- FlowIDs start at **1000** for the Student BlockRandomizer
- Each group and nested block reference has a unique FlowID (FL_1000, FL_1001, ...)

### Teaching Branch
- FlowIDs start at **2000** for the Teaching BlockRandomizer
- Each group and nested block reference has a unique FlowID (FL_2000, FL_2001, ...)

This ensures no FlowID conflicts between branches.

## Question Structure

### Per-Vignette Blocks (17 questions)
All per-vignette blocks contain the same questions:
- QID31, QID32, QID33, None, QID34, QID35, QID36, None, QID38, QID39, QID40, None, QID41, QID42, QID47, QID48, QID159

The questions are **identical** in content, but each scenario has its own copy of the block with a unique ID.

### Post-Vignette Blocks
All post-vignette blocks contain identical reflection questions, with each scenario having its own unique block ID.

## Import Instructions

1. Import `ai-attribution-in-cs-ed-master-102groups.qsf` into Qualtrics
2. Verify the BlockRandomizers show "5 of 102" in both branches
3. Preview the survey to confirm:
   - Student branch shows iframe vignettes
   - Teaching branch shows per-vignette questions directly
   - Each scenario uses its unique blocks

## Data Collection

When participants complete the survey:
- Responses are tagged with scenario-specific block IDs (e.g., BL_PerVig_S42)
- You can filter responses by scenario during analysis
- Each of the 102 scenarios has independent response tracking
- Randomization ensures balanced distribution of scenarios across participants
