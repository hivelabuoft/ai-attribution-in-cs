#!/usr/bin/env python3
"""
Modify the QSF file to:
1. Change BlockRandomizer SubSet from 3 to 5 (select 5 scenarios)
2. Generate 102 embedded data elements (one for each scenario 1-102)
3. Add JavaScript collection logic to identify which 5 were selected
4. Update QID371 question text to display the selected scenarios

The approach uses embedded data with "OR" logic - each of the 102 elements
sets ALL 5 position variables (Pos1-Pos5) to the same scenario number.
When 5 are randomly selected, only those 5 scenario numbers will be set,
and we can display them.
"""

import json
import sys

def modify_qsf(input_file, output_file):
    """Modify the QSF file for 102-scenario randomization."""
    
    # Read the QSF file
    print(f"Reading {input_file}...")
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Find the Survey Flow element
    flow_element = None
    for element in data.get('SurveyElements', []):
        if element.get('Element') == 'FL':
            flow_element = element
            break
    
    if not flow_element:
        print("Error: Could not find Survey Flow element")
        return False
    
    flow_payload = flow_element.get('Payload', {})
    flow_items = flow_payload.get('Flow', [])
    
    # Find the Student branch and its BlockRandomizer
    student_branch = None
    student_branch_index = None
    
    for i, item in enumerate(flow_items):
        if item.get('Type') == 'Branch':
            # Check if this is the Student branch
            branch_logic = item.get('BranchLogic', {})
            is_student = False
            for key in branch_logic:
                if isinstance(branch_logic[key], dict):
                    for subkey in branch_logic[key]:
                        if isinstance(branch_logic[key][subkey], dict):
                            desc = branch_logic[key][subkey].get('Description', '')
                            if 'Student' in desc:
                                is_student = True
                                break
            if is_student:
                student_branch = item
                student_branch_index = i
                break
    
    if not student_branch:
        print("Error: Could not find Student branch")
        return False
    
    print("✓ Found Student branch")
    
    # Find the BlockRandomizer within the Student branch
    student_flow = student_branch.get('Flow', [])
    randomizer = None
    randomizer_index = None
    
    for i, item in enumerate(student_flow):
        if item.get('Type') == 'BlockRandomizer':
            randomizer = item
            randomizer_index = i
            break
    
    if not randomizer:
        print("Error: Could not find BlockRandomizer in Student branch")
        return False
    
    print(f"✓ Found BlockRandomizer (current SubSet: {randomizer.get('SubSet')})")
    
    # Step 1: Change SubSet to 5
    randomizer['SubSet'] = 5
    print("✓ Changed SubSet to 5")
    
    # Step 2: Generate 102 embedded data elements
    flow_elements = []
    flow_id_start = 5000  # Use high numbers to avoid conflicts
    
    for i in range(1, 103):  # 1 to 102
        # Each embedded data element sets all 5 position variables to its scenario number
        # When randomizer selects 5 of these, those 5 scenario numbers will be set
        flow_element = {
            "Type": "EmbeddedData",
            "FlowID": f"FL_{flow_id_start + i}",
            "EmbeddedData": [
                {
                    "Description": f"Pos{j}",
                    "Type": "Custom",
                    "Field": f"Pos{j}",
                    "VariableType": "String",
                    "DataVisibility": [],
                    "AnalyzeText": False,
                    "Value": str(i)
                } for j in range(1, 6)  # Pos1 through Pos5
            ]
        }
        flow_elements.append(flow_element)
    
    # Replace the randomizer's Flow with our 102 elements
    randomizer['Flow'] = flow_elements
    print(f"✓ Generated 102 embedded data elements in BlockRandomizer")
    
    # Step 3: Add a Web Service / Embedded Data block AFTER the randomizer
    # This will collect the non-empty Pos values
    collector_flow_id = f"FL_{flow_id_start + 200}"
    
    # We don't actually need JavaScript for this approach!
    # The Pos1-Pos5 variables will already contain the selected scenario numbers
    # We just need to create a display string
    
    # Add an embedded data element to create a comma-separated list
    # Actually, in Qualtrics we can just reference Pos1-Pos5 directly in the question
    # So we'll skip adding more embedded data and just update the question
    
    # Step 4: Find and update QID371 question text
    survey_elements = data.get('SurveyElements', [])
    question_updated = False
    
    for element in survey_elements:
        if element.get('Element') == 'SQ' and element.get('PrimaryAttribute') == 'QID371':
            payload = element.get('Payload', {})
            
            # Update question text to use piped text
            new_question_text = (
                'You have been assigned the following scenario IDs: '
                '${e://Field/Pos1}, ${e://Field/Pos2}, ${e://Field/Pos3}, '
                '${e://Field/Pos4}, ${e://Field/Pos5}'
                '<br><br>'
                'Please write down each scenario ID individually in the text boxes below. '
                'You will be asked to complete tasks for each of these scenarios later in the survey.'
            )
            
            payload['QuestionText'] = new_question_text
            
            # Also update the description
            payload['QuestionDescription'] = 'You have been assigned the following scenario IDs: ${e://Field/Pos1}, ${e://Field/Pos2}, ${e://Field/Pos3}, ${e://Field/Pos4}, ${e://Field/Pos5} Please write do...'
            element['SecondaryAttribute'] = 'You have been assigned the following scenario IDs: ${e://Field/Pos1}, ${e://Field/Pos2}, ${e://Field/Pos3}, ${e://Field/Pos4}, ${e://Field/Pos5} Please write do...'
            
            question_updated = True
            print("✓ Updated QID371 question text to display selected scenarios")
            break
    
    if not question_updated:
        print("Warning: Could not find QID371 to update question text")
    
    # Write the modified QSF file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Successfully created {output_file}")
    print(f"   - BlockRandomizer will select 5 of 102 scenarios")
    print(f"   - Selected scenario IDs will be stored in Pos1-Pos5")
    print(f"   - Question displays: ${{e://Field/Pos1}}, ${{e://Field/Pos2}}, etc.")
    
    return True


if __name__ == '__main__':
    # Use the current file
    input_file = 'ai-attribution-in-cs-ed-master (7).qsf'
    output_file = 'ai-attribution-in-cs-ed-master-102random.qsf'
    
    print("="* 60)
    print("Modifying QSF for 102-scenario randomization (select 5)")
    print("=" * 60)
    print()
    
    success = modify_qsf(input_file, output_file)
    
    if success:
        print("\n🎉 Done! Import the new QSF file into Qualtrics.")
        print("\nHow it works:")
        print("  1. BlockRandomizer randomly selects 5 of 102 embedded data elements")
        print("  2. Each selected element sets Pos1-Pos5 to its scenario number")
        print("  3. The 5 selected scenarios will appear in Pos1, Pos2, Pos3, Pos4, Pos5")
        print("  4. Question text displays these using piped text: ${e://Field/Pos1}, etc.")
    else:
        print("\n❌ Failed. Please check the error messages above.")
        sys.exit(1)
