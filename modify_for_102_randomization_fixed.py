#!/usr/bin/env python3
"""
CORRECT approach for 102-scenario randomization.

Instead of having each scenario set all 5 positions to the same value,
we need each scenario to set a UNIQUE field (Selected1, Selected2, ... Selected102).

Then after the randomizer, we use JavaScript to:
1. Check which of the 102 fields were set
2. Collect those 5 scenario numbers
3. Store them in Pos1-Pos5 for display
"""

import json
import sys

def modify_qsf_correct(input_file, output_file):
    """Modify the QSF file for 102-scenario randomization - CORRECT VERSION."""
    
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
    # Each one sets its OWN unique field (Selected1, Selected2, etc.)
    flow_elements = []
    flow_id_start = 5000
    
    for i in range(1, 103):  # 1 to 102
        flow_element = {
            "Type": "EmbeddedData",
            "FlowID": f"FL_{flow_id_start + i}",
            "EmbeddedData": [
                {
                    "Description": f"Selected{i}",
                    "Type": "Custom",
                    "Field": f"Selected{i}",
                    "VariableType": "String",
                    "DataVisibility": [],
                    "AnalyzeText": False,
                    "Value": str(i)  # The value is the scenario number
                }
            ]
        }
        flow_elements.append(flow_element)
    
    # Replace the randomizer's Flow with our 102 elements
    randomizer['Flow'] = flow_elements
    print(f"✓ Generated 102 embedded data elements (Selected1-Selected102)")
    
    # Step 3: Add a JavaScript block AFTER the randomizer to collect results
    # This will check which Selected1-Selected102 fields are set
    # and populate Pos1-Pos5 with those values
    
    # First, add embedded data fields to initialize Pos1-Pos5
    collector_flow_id = 6200
    
    collector_embedded_data = {
        "Type": "EmbeddedData",
        "FlowID": f"FL_{collector_flow_id}",
        "EmbeddedData": [
            {
                "Description": "Pos1",
                "Type": "Custom",
                "Field": "Pos1",
                "VariableType": "String",
                "DataVisibility": [],
                "AnalyzeText": False,
                "Value": ""
            },
            {
                "Description": "Pos2",
                "Type": "Custom",
                "Field": "Pos2",
                "VariableType": "String",
                "DataVisibility": [],
                "AnalyzeText": False,
                "Value": ""
            },
            {
                "Description": "Pos3",
                "Type": "Custom",
                "Field": "Pos3",
                "VariableType": "String",
                "DataVisibility": [],
                "AnalyzeText": False,
                "Value": ""
            },
            {
                "Description": "Pos4",
                "Type": "Custom",
                "Field": "Pos4",
                "VariableType": "String",
                "DataVisibility": [],
                "AnalyzeText": False,
                "Value": ""
            },
            {
                "Description": "Pos5",
                "Type": "Custom",
                "Field": "Pos5",
                "VariableType": "String",
                "DataVisibility": [],
                "AnalyzeText": False,
                "Value": ""
            }
        ]
    }
    
    # Insert this AFTER the randomizer in the student flow
    student_flow.insert(randomizer_index + 1, collector_embedded_data)
    print("✓ Added Pos1-Pos5 embedded data fields after randomizer")
    
    # Step 4: Find QID371 and add JavaScript to it
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
            
            # Add JavaScript to collect the selected scenarios
            javascript_code = """
Qualtrics.SurveyEngine.addOnload(function() {
    // Find which Selected1-Selected102 fields were set by checking their values
    var selected = [];
    
    for (var i = 1; i <= 102; i++) {
        var fieldValue = "${e://Field/Selected" + i + "}";
        // Check if the piped text was actually replaced (not empty and not the literal string)
        if (fieldValue && fieldValue !== "" && fieldValue !== "${e://Field/Selected" + i + "}") {
            selected.push(fieldValue);
        }
    }
    
    // Set Pos1-Pos5 with the selected scenario numbers
    for (var j = 0; j < 5 && j < selected.length; j++) {
        Qualtrics.SurveyEngine.setEmbeddedData("Pos" + (j+1), selected[j]);
    }
    
    // Force the question to re-render with the updated values
    setTimeout(function() {
        jQuery("#QID371").closest(".QuestionOuter").find(".QuestionText").html(
            'You have been assigned the following scenario IDs: ' +
            selected.join(', ') +
            '<br><br>Please write down each scenario ID individually in the text boxes below. ' +
            'You will be asked to complete tasks for each of these scenarios later in the survey.'
        );
    }, 100);
});
"""
            
            payload['QuestionJS'] = javascript_code
            
            # Also update the description
            payload['QuestionDescription'] = 'You have been assigned the following scenario IDs: ${e://Field/Pos1}, ${e://Field/Pos2}, ${e://Field/Pos3}, ${e://Field/Pos4}, ${e://Field/Pos5} Please write do...'
            element['SecondaryAttribute'] = 'You have been assigned the following scenario IDs: ${e://Field/Pos1}, ${e://Field/Pos2}, ${e://Field/Pos3}, ${e://Field/Pos4}, ${e://Field/Pos5} Please write do...'
            
            question_updated = True
            print("✓ Updated QID371 with JavaScript to collect selected scenarios")
            break
    
    if not question_updated:
        print("Warning: Could not find QID371 to update")
    
    # Write the modified QSF file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Successfully created {output_file}")
    print(f"\nHow it works:")
    print(f"   1. BlockRandomizer selects 5 of 102 embedded data elements")
    print(f"   2. Each selected element sets Selected1-Selected102 to its scenario number")
    print(f"   3. JavaScript on QID371 checks which Selected# fields are set")
    print(f"   4. JavaScript populates Pos1-Pos5 with the 5 selected scenario numbers")
    print(f"   5. Question displays the 5 randomly selected scenario IDs")
    
    return True


if __name__ == '__main__':
    input_file = 'ai-attribution-in-cs-ed-master (7).qsf'
    output_file = 'ai-attribution-in-cs-ed-master-102random-fixed.qsf'
    
    print("=" * 60)
    print("Modifying QSF for 102-scenario randomization (CORRECT)")
    print("=" * 60)
    print()
    
    success = modify_qsf_correct(input_file, output_file)
    
    if success:
        print("\n🎉 Done! Import the new QSF file into Qualtrics.")
    else:
        print("\n❌ Failed. Please check the error messages above.")
        sys.exit(1)
