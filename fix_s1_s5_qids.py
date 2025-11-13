#!/usr/bin/env python3
"""
Fix duplicate Question IDs in per-vignette-S1 to S5 blocks.
Each block should have unique QIDs for its 14 questions.
"""

import json
import sys
import copy

def fix_qids_for_s1_to_s5(qsf_file):
    """
    Fix QIDs for per-vignette-S1 to S5 blocks.
    Each block gets unique QIDs.
    """
    with open(qsf_file, 'r', encoding='utf-8') as f:
        survey = json.load(f)
    
    # The original QIDs used in all blocks
    original_qids = [
        "QID31", "QID32", "QID33",  # First group (3 questions)
        "QID34", "QID35", "QID36",  # Second group (3 questions)
        "QID38", "QID39", "QID40",  # Third group (3 questions)
        "QID41", "QID42", "QID47", "QID48", "QID159"  # Fourth group (5 questions)
    ]
    
    # Find blocks S1-S5
    target_blocks = ["per-vignette-S1", "per-vignette-S2", "per-vignette-S3", 
                     "per-vignette-S4", "per-vignette-S5"]
    
    # Starting QID number for new unique IDs
    # Using 1000+ range to avoid conflicts
    next_qid_num = 1000
    
    # Map to store old QID -> new QID mappings for each block
    block_qid_mappings = {}
    
    # Find the BL (Blocks) element
    blocks_element = [e for e in survey['SurveyElements'] if e.get('Element') == 'BL'][0]
    all_blocks = blocks_element['Payload']
    
    # Process each target block
    for block_idx, target_block_desc in enumerate(target_blocks, start=1):
        print(f"\nProcessing {target_block_desc}...")
        
        # Find the block
        block = None
        for block_data in all_blocks:
            if isinstance(block_data, dict) and block_data.get('Description') == target_block_desc:
                block = block_data
                break
        
        if not block:
            print(f"Warning: Block {target_block_desc} not found")
            continue
        
        # Create mapping for this block
        block_qid_mappings[target_block_desc] = {}
        
        # Get BlockElements
        block_elements = block.get('BlockElements', [])
        question_qids = [elem['QuestionID'] for elem in block_elements if elem.get('Type') == 'Question']
        
        if len(question_qids) != 14:
            print(f"Warning: Expected 14 questions in {target_block_desc}, found {len(question_qids)}")
        
        # Assign new QIDs
        for old_qid in question_qids:
            new_qid = f"QID{next_qid_num}"
            block_qid_mappings[target_block_desc][old_qid] = new_qid
            print(f"  {old_qid} -> {new_qid}")
            next_qid_num += 1
        
        # Update BlockElements with new QIDs
        for elem in block_elements:
            if elem.get('Type') == 'Question':
                old_qid = elem['QuestionID']
                new_qid = block_qid_mappings[target_block_desc][old_qid]
                elem['QuestionID'] = new_qid
    
    # Now create new SQ elements for each new QID
    # Find original question definitions
    original_questions = {}
    for element in survey['SurveyElements']:
        if element.get('Element') == 'SQ':
            qid = element.get('PrimaryAttribute')
            if qid in original_qids:
                original_questions[qid] = element
    
    print(f"\nFound {len(original_questions)} original question definitions")
    
    # Create new question elements for each block
    new_elements = []
    for block_desc, qid_mapping in block_qid_mappings.items():
        for old_qid, new_qid in qid_mapping.items():
            if old_qid in original_questions:
                # Deep copy the original question element
                new_question_element = copy.deepcopy(original_questions[old_qid])
                # Update the PrimaryAttribute (which is the QID)
                new_question_element['PrimaryAttribute'] = new_qid
                # Update the QuestionID in the Payload
                new_question_element['Payload']['QuestionID'] = new_qid
                # Add to the list of new elements
                new_elements.append(new_question_element)
                print(f"Created question element for {new_qid} (from {old_qid})")
    
    # Add new elements to SurveyElements
    # Find the position to insert (after the last SQ element)
    last_sq_index = -1
    for i, element in enumerate(survey['SurveyElements']):
        if element.get('Element') == 'SQ':
            last_sq_index = i
    
    # Insert new elements after the last SQ element
    if last_sq_index >= 0:
        survey['SurveyElements'][last_sq_index+1:last_sq_index+1] = new_elements
        print(f"\nInserted {len(new_elements)} new question elements")
    
    # Save the modified survey
    output_file = qsf_file.replace('.qsf', '-fixed-s1-s5.qsf')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(survey, f, indent=2)
    
    print(f"\n✅ Fixed survey saved to: {output_file}")
    print(f"Created {next_qid_num - 1000} new unique question IDs")
    
    return output_file

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python fix_s1_s5_qids.py <qsf_file>")
        sys.exit(1)
    
    qsf_file = sys.argv[1]
    fix_qids_for_s1_to_s5(qsf_file)
