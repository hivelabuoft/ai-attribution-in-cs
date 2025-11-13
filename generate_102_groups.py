#!/usr/bin/env python3
"""
Script to generate 102 groups (S1-S102) in the Qualtrics QSF file.
Each group will have an iframe pointing to pages/1 through pages/102.
"""

import json
import sys

def generate_groups(input_file, output_file):
    """Generate 102 groups with iframes for each page number."""
    
    # Read the QSF file
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Find the existing QID53 and QID54 questions (the iframe questions)
    survey_elements = data.get('SurveyElements', [])
    
    # We'll use QID53 as the template (it has pages/1)
    template_question = None
    for element in survey_elements:
        if element.get('Element') == 'SQ' and element.get('PrimaryAttribute') == 'QID53':
            template_question = element
            break
    
    if not template_question:
        print("Error: Could not find template question QID53")
        return False
    
    # Store the base QID number - we'll start from QID53 + 2 = QID55
    # (since QID54 is already used for pages/2)
    base_qid = 55
    
    # Generate questions for pages 3 through 102
    new_questions = []
    
    for page_num in range(3, 103):
        qid = f"QID{base_qid}"
        base_qid += 1
        
        # Create new question based on template
        new_question = {
            "SurveyID": template_question["SurveyID"],
            "Element": "SQ",
            "PrimaryAttribute": qid,
            "SecondaryAttribute": "Click to write the question text",
            "TertiaryAttribute": None,
            "Payload": {
                "QuestionText": f'<iframe src="https://hivelabuoft.github.io/ai-attribution-in-cs/pages/{page_num}" \n        width="100%" \n        height="1000px" \n        frameborder="0"\n        scrolling="auto">\n</iframe>',
                "DefaultChoices": False,
                "DataExportTag": "slide",
                "QuestionType": "DB",
                "Selector": "TB",
                "DataVisibility": {
                    "Private": False,
                    "Hidden": False
                },
                "Configuration": {
                    "QuestionDescriptionOption": "UseText"
                },
                "QuestionDescription": "Click to write the question text",
                "ChoiceOrder": [],
                "Validation": {
                    "Settings": {
                        "Type": "None"
                    }
                },
                "GradingData": [],
                "Language": [],
                "NextChoiceId": 4,
                "NextAnswerId": 1,
                "QuestionID": qid
            }
        }
        
        new_questions.append(new_question)
    
    # Find where to insert the new questions (after QID54)
    insert_index = None
    for i, element in enumerate(survey_elements):
        if element.get('Element') == 'SQ' and element.get('PrimaryAttribute') == 'QID54':
            insert_index = i + 1
            break
    
    if insert_index is None:
        print("Error: Could not find insertion point after QID54")
        return False
    
    # Insert all new questions
    for i, new_q in enumerate(new_questions):
        survey_elements.insert(insert_index + i, new_q)
    
    print(f"✓ Generated {len(new_questions)} new iframe questions (QID55-QID{base_qid-1})")
    
    # Now we need to create 102 groups in the Survey Flow
    # Find the Survey Flow element
    flow_element = None
    for element in data.get('SurveyElements', []):
        if element.get('Element') == 'FL':
            flow_element = element
            break
    
    if not flow_element:
        print("Error: Could not find Survey Flow element")
        return False
    
    # Find the existing S1 and S2 groups in the flow to use as templates
    flow_payload = flow_element.get('Payload', {})
    flow_items = flow_payload.get('Flow', [])
    
    # We need to find the BlockRandomizer that contains the S1/S2 groups
    def find_randomizer_with_groups(flow_items):
        """Recursively find the BlockRandomizer containing S1/S2 groups."""
        for item in flow_items:
            if item.get('Type') == 'BlockRandomizer':
                # Check if this randomizer has groups
                inner_flow = item.get('Flow', [])
                for inner_item in inner_flow:
                    if inner_item.get('Type') == 'Group':
                        desc = inner_item.get('Description', '')
                        if desc == 'S1' or desc == 'S2':
                            return item  # Return the randomizer itself
            # Recursively search in nested flows
            if 'Flow' in item:
                result = find_randomizer_with_groups(item['Flow'])
                if result:
                    return result
        return None
    
    randomizer = find_randomizer_with_groups(flow_items)
    
    if not randomizer:
        print("Error: Could not find BlockRandomizer with S1/S2 groups")
        return False
    
    randomizer_flow = randomizer.get('Flow', [])
    
    # Find the existing groups within the randomizer
    existing_groups = []
    group_insert_index = None
    
    for i, item in enumerate(randomizer_flow):
        if item.get('Type') == 'Group' and item.get('Description', '').startswith('S'):
            existing_groups.append(item)
            if group_insert_index is None:
                group_insert_index = i
    
    if len(existing_groups) < 2:
        print(f"Warning: Found only {len(existing_groups)} existing groups (S1, S2), expected 2")
        if len(existing_groups) == 0:
            print("Error: No template groups found")
            return False
    
    # Use S1 as template
    s1_template = existing_groups[0]
    
    print(f"✓ Found template group: {s1_template.get('Description')}")
    
    # Generate groups S3 through S102
    new_groups = []
    next_flow_id = 1000  # Start with a high number to avoid conflicts
    
    for group_num in range(3, 103):
        # Create new group based on S1 template
        new_group = json.loads(json.dumps(s1_template))  # Deep copy
        
        # Update the description and FlowID
        new_group['Description'] = f'S{group_num}'
        new_group['FlowID'] = f'FL_{next_flow_id}'
        next_flow_id += 1
        
        # Update all nested FlowIDs within the group
        if 'Flow' in new_group:
            for i, flow_item in enumerate(new_group['Flow']):
                flow_item['FlowID'] = f'FL_{next_flow_id}'
                next_flow_id += 1
        
        new_groups.append(new_group)
    
    # Insert new groups after S2 in the randomizer
    if group_insert_index is not None:
        # Find position after S2
        s2_index = group_insert_index + 1 if len(existing_groups) > 1 else group_insert_index
        
        for i, new_group in enumerate(new_groups):
            randomizer_flow.insert(s2_index + 1 + i, new_group)
    
    print(f"✓ Generated {len(new_groups)} new groups (S3-S102) in BlockRandomizer")
    
    # Update the randomizer to select 5 of 102 instead of 1 of 2
    randomizer['SubSet'] = '5'  # Select 5 groups
    print(f"✓ Updated BlockRandomizer to select 5 of {len(randomizer_flow)} groups")
    
    # Now handle the Teaching branch - find and add groups there too
    teaching_groups_added = False
    for item in flow_items:
        if item.get('Type') == 'Branch':
            branch_logic = item.get('BranchLogic', {})
            # Check if this is the Teaching branch
            is_teaching = False
            for key in branch_logic:
                if isinstance(branch_logic[key], dict):
                    for subkey in branch_logic[key]:
                        if isinstance(branch_logic[key][subkey], dict):
                            desc = branch_logic[key][subkey].get('Description', '')
                            if 'Teaching' in desc:
                                is_teaching = True
                                break
            
            if is_teaching:
                teaching_flow = item.get('Flow', [])
                # Find existing S1 group in teaching branch
                teaching_s1_group = None
                teaching_s1_index = None
                
                for i, sub_item in enumerate(teaching_flow):
                    if sub_item.get('Type') == 'Group' and sub_item.get('Description') == 'S1':
                        teaching_s1_group = sub_item
                        teaching_s1_index = i
                        break
                
                if teaching_s1_group:
                    # Generate all groups S1-S102 for teaching branch
                    teaching_all_groups = []
                    teaching_flow_id = 2000  # Different starting point for teaching branch
                    
                    # First, update S1 with unique FlowIDs
                    s1_group_copy = json.loads(json.dumps(teaching_s1_group))
                    s1_group_copy['FlowID'] = f'FL_{teaching_flow_id}'
                    teaching_flow_id += 1
                    if 'Flow' in s1_group_copy:
                        for flow_item in s1_group_copy['Flow']:
                            flow_item['FlowID'] = f'FL_{teaching_flow_id}'
                            teaching_flow_id += 1
                    teaching_all_groups.append(s1_group_copy)
                    
                    # Generate S2-S102
                    for group_num in range(2, 103):
                        new_group = json.loads(json.dumps(teaching_s1_group))  # Deep copy
                        new_group['Description'] = f'S{group_num}'
                        new_group['FlowID'] = f'FL_{teaching_flow_id}'
                        teaching_flow_id += 1
                        
                        # Update nested FlowIDs and block references
                        if 'Flow' in new_group:
                            for i, flow_item in enumerate(new_group['Flow']):
                                flow_item['FlowID'] = f'FL_{teaching_flow_id}'
                                teaching_flow_id += 1
                                
                                # Update block IDs to reference unique blocks for each scenario
                                # Teaching branch doesn't have iframe blocks, just per-vig and post-vig
                                if i == 0:  # per-vignette block
                                    flow_item['ID'] = f'BL_PerVig_T{group_num}'
                                elif i == 1:  # post-vig-reflect block
                                    flow_item['ID'] = f'BL_PostVig_T{group_num}'
                        
                        teaching_all_groups.append(new_group)
                    
                    # Also update S1 group to reference unique teaching blocks
                    if 'Flow' in s1_group_copy:
                        for i, flow_item in enumerate(s1_group_copy['Flow']):
                            if i == 0:  # per-vignette block
                                flow_item['ID'] = 'BL_PerVig_T1'
                            elif i == 1:  # post-vig-reflect block
                                flow_item['ID'] = 'BL_PostVig_T1'
                    
                    # Remove the old S1 group
                    teaching_flow.pop(teaching_s1_index)
                    
                    # Create a BlockRandomizer for teaching branch
                    teaching_randomizer = {
                        'Type': 'BlockRandomizer',
                        'FlowID': f'FL_{teaching_flow_id}',
                        'SubSet': '5',
                        'EvenPresentation': True,
                        'Flow': teaching_all_groups
                    }
                    teaching_flow_id += 1
                    
                    # Insert the randomizer where S1 was
                    teaching_flow.insert(teaching_s1_index, teaching_randomizer)
                    
                    teaching_groups_added = True
                    print(f"✓ Created BlockRandomizer for Teaching branch with 102 groups (S1-S102)")
                    print(f"✓ Teaching branch set to select 5 of 102 groups evenly")
    
    # Now create the corresponding blocks for S3-S102
    # Find the blocks section
    blocks = None
    for element in survey_elements:
        if element.get('Element') == 'BL':
            blocks = element
            break
    
    if not blocks:
        print("Warning: Could not find blocks element")
    else:
        # Find S1 and S2 blocks, per-vignette block, and post-vig-reflect block as templates
        blocks_payload = blocks.get('Payload', [])
        s1_block = None
        s2_block = None
        per_vig_block = None
        post_vig_block = None
        
        for block in blocks_payload:
            desc = block.get('Description', '')
            if desc == 'S1':
                s1_block = block
            elif desc == 'S2':
                s2_block = block
            elif 'per-vignette' in desc.lower() or desc == 'per-vig':
                per_vig_block = block
            elif 'post-vig' in desc.lower():
                post_vig_block = block
        
        if s1_block:
            # First, create unique per-vignette and post-vig blocks for S1 and S2
            if per_vig_block and post_vig_block:
                # Create per-vignette-S1
                per_vig_s1 = json.loads(json.dumps(per_vig_block))
                per_vig_s1['Description'] = 'per-vignette-S1'
                per_vig_s1['ID'] = 'BL_PerVig_S1'
                
                # Create per-vignette-S2
                per_vig_s2 = json.loads(json.dumps(per_vig_block))
                per_vig_s2['Description'] = 'per-vignette-S2'
                per_vig_s2['ID'] = 'BL_PerVig_S2'
                
                # Create post-vig-reflect-S1
                post_vig_s1 = json.loads(json.dumps(post_vig_block))
                post_vig_s1['Description'] = 'post-vig-reflect-S1'
                post_vig_s1['ID'] = 'BL_PostVig_S1'
                
                # Create post-vig-reflect-S2
                post_vig_s2 = json.loads(json.dumps(post_vig_block))
                post_vig_s2['Description'] = 'post-vig-reflect-S2'
                post_vig_s2['ID'] = 'BL_PostVig_S2'
                
                # Add these to blocks
                blocks_payload.extend([per_vig_s1, per_vig_s2, post_vig_s1, post_vig_s2])
                
                # Update S1 and S2 groups to reference their unique blocks
                for group in existing_groups:
                    if group['Description'] == 'S1' and 'Flow' in group and len(group['Flow']) >= 3:
                        group['Flow'][1]['ID'] = 'BL_PerVig_S1'
                        group['Flow'][2]['ID'] = 'BL_PostVig_S1'
                    elif group['Description'] == 'S2' and 'Flow' in group and len(group['Flow']) >= 3:
                        group['Flow'][1]['ID'] = 'BL_PerVig_S2'
                        group['Flow'][2]['ID'] = 'BL_PostVig_S2'
                
                print(f"✓ Created unique per-vignette and post-vig blocks for S1 and S2")
            
            # Create new blocks for S3-S102
            new_s_blocks = []
            new_per_vig_blocks = []
            new_post_vig_blocks = []
            
            for block_num in range(3, 103):
                # Create Sn block (iframe)
                new_s_block = json.loads(json.dumps(s1_block))  # Deep copy
                new_s_block['Description'] = f'S{block_num}'
                new_s_block['ID'] = f'BL_S{block_num}Generated'  # Unique block ID
                
                # Update the question ID in BlockElements
                qid_for_block = f'QID{52 + block_num}'
                new_s_block['BlockElements'] = [{"Type": "Question", "QuestionID": qid_for_block}]
                
                new_s_blocks.append(new_s_block)
                
                # Create unique per-vignette block for this scenario
                if per_vig_block:
                    new_per_vig = json.loads(json.dumps(per_vig_block))  # Deep copy
                    new_per_vig['Description'] = f'per-vignette-S{block_num}'
                    new_per_vig['ID'] = f'BL_PerVig_S{block_num}'
                    # Keep all the same questions - just copy the BlockElements as-is
                    new_per_vig_blocks.append(new_per_vig)
                
                # Create unique post-vig-reflect block for this scenario
                if post_vig_block:
                    new_post_vig = json.loads(json.dumps(post_vig_block))  # Deep copy
                    new_post_vig['Description'] = f'post-vig-reflect-S{block_num}'
                    new_post_vig['ID'] = f'BL_PostVig_S{block_num}'
                    # Keep all the same questions - just copy the BlockElements as-is
                    new_post_vig_blocks.append(new_post_vig)
                
                # Update the Flow references in the group to use these new blocks
                for group in new_groups:
                    if group['Description'] == f'S{block_num}':
                        if 'Flow' in group and len(group['Flow']) >= 3:
                            # Update block IDs for all three blocks in the group
                            group['Flow'][0]['ID'] = new_s_block['ID']  # Sn block
                            if per_vig_block:
                                group['Flow'][1]['ID'] = f'BL_PerVig_S{block_num}'  # per-vignette
                            if post_vig_block:
                                group['Flow'][2]['ID'] = f'BL_PostVig_S{block_num}'  # post-vig-reflect
            
            # Add new blocks to the blocks payload
            blocks_payload.extend(new_s_blocks)
            blocks_payload.extend(new_per_vig_blocks)
            blocks_payload.extend(new_post_vig_blocks)
            print(f"✓ Created {len(new_s_blocks)} new S blocks (S3-S102) with iframe questions")
            print(f"✓ Created {len(new_per_vig_blocks)} new per-vignette blocks (unique for each scenario)")
            print(f"✓ Created {len(new_post_vig_blocks)} new post-vig-reflect blocks (unique for each scenario)")
            
            # Now create Teaching branch blocks (T1-T102)
            # Teaching branch doesn't have iframe blocks, only per-vignette and post-vig-reflect
            teaching_per_vig_blocks = []
            teaching_post_vig_blocks = []
            
            if per_vig_block and post_vig_block:
                for block_num in range(1, 103):
                    # Create unique per-vignette block for Teaching scenario
                    new_teaching_per_vig = json.loads(json.dumps(per_vig_block))
                    new_teaching_per_vig['Description'] = f'per-vignette-T{block_num}'
                    new_teaching_per_vig['ID'] = f'BL_PerVig_T{block_num}'
                    teaching_per_vig_blocks.append(new_teaching_per_vig)
                    
                    # Create unique post-vig-reflect block for Teaching scenario
                    new_teaching_post_vig = json.loads(json.dumps(post_vig_block))
                    new_teaching_post_vig['Description'] = f'post-vig-reflect-T{block_num}'
                    new_teaching_post_vig['ID'] = f'BL_PostVig_T{block_num}'
                    teaching_post_vig_blocks.append(new_teaching_post_vig)
                
                # Add Teaching branch blocks
                blocks_payload.extend(teaching_per_vig_blocks)
                blocks_payload.extend(teaching_post_vig_blocks)
                print(f"✓ Created {len(teaching_per_vig_blocks)} Teaching per-vignette blocks (T1-T102)")
                print(f"✓ Created {len(teaching_post_vig_blocks)} Teaching post-vig-reflect blocks (T1-T102)")
    
    # Write the modified QSF file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Successfully created {output_file}")
    print(f"   - Added {len(new_questions)} iframe questions (pages 3-102)")
    print(f"   - Added {len(new_groups)} groups to Student branch BlockRandomizer")
    print(f"   - Student BlockRandomizer: select 5 of 102 groups evenly")
    if teaching_groups_added:
        print(f"   - Added 102 groups to Teaching branch BlockRandomizer")
        print(f"   - Teaching BlockRandomizer: select 5 of 102 groups evenly")
    
    return True


if __name__ == '__main__':
    input_file = 'ai-attribution-in-cs-ed-master (1).qsf'
    output_file = 'ai-attribution-in-cs-ed-master-102groups.qsf'
    
    print(f"Generating 102 groups from {input_file}...\n")
    
    success = generate_groups(input_file, output_file)
    
    if success:
        print("\n🎉 Done! You can now import the new QSF file into Qualtrics.")
    else:
        print("\n❌ Failed to generate groups. Please check the error messages above.")
        sys.exit(1)
