# 102 Groups Generation - Summary

## What Was Done

Successfully generated a new Qualtrics survey file (`ai-attribution-in-cs-ed-master-102groups.qsf`) with 102 scenario groups (S1-S102).

## Changes Made

### 1. Questions Created
- **100 new iframe questions** added (QID55-QID154)
- Each question displays an iframe pointing to `https://hivelabuoft.github.io/ai-attribution-in-cs/pages/[N]` where N ranges from 3 to 102
- Questions QID53 (pages/1) and QID54 (pages/2) already existed

### 2. Blocks Created
- **100 new blocks** created (S3-S102)
- Each block contains one iframe question corresponding to its scenario number
- S1 block → QID53 (pages/1)
- S2 block → QID54 (pages/2)
- S3 block → QID55 (pages/3)
- ...
- S102 block → QID154 (pages/102)

### 3. Groups in Survey Flow
- **100 new groups** added to the BlockRandomizer (S3-S102)
- Each group contains:
  - The scenario-specific block (iframe)
  - The per-vignette questions block (BL_8xeykGPs5f8ULQy)
  - The post-reflection block (BL_7UJh1skuAhde79c)

### 4. BlockRandomizer Configuration
- **SubSet**: Set to `5` (randomly select 5 groups per participant)
- **EvenPresentation**: `true` (ensures scenarios are distributed evenly across participants)
- **Total Groups**: 102 (S1 through S102)

## How It Works

When a student takes the survey:
1. They will be randomly assigned **5 out of 102 scenarios**
2. Each scenario shows a different iframe (pages/1 through pages/102)
3. For each scenario, they answer the per-vignette questions and post-reflection questions
4. The `EvenPresentation` setting ensures all 102 scenarios are presented evenly across all participants

## Files

- **Input**: `ai-attribution-in-cs-ed-master (1).qsf` (original survey with S1 and S2)
- **Output**: `ai-attribution-in-cs-ed-master-102groups.qsf` (new survey with S1-S102)
- **Script**: `generate_102_groups.py` (the Python script that generated the changes)

## Next Steps

1. Import `ai-attribution-in-cs-ed-master-102groups.qsf` into Qualtrics
2. Review the survey flow to ensure it looks correct
3. Create the corresponding HTML pages (pages/3.html through pages/102.html) following the same pattern as pages/1.html and pages/2.html
4. Test the survey with a few participants to ensure randomization works as expected

## File Size

- Original: ~94 KB
- New file: ~361 KB (increased due to 100 additional questions, blocks, and groups)
