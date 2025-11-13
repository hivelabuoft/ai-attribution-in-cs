#!/usr/bin/env python3
"""
Simplified restructure:
1. Randomly assign 5 scenario numbers (1-102) with even presentation
2. Display the assigned numbers
3. Ask users to input those numbers (5 text boxes)
4. Show 5 pairs of blocks: S1-S5 with dynamic iframe URLs using piped text from user input
"""

import json

def create_display_block():
    """Create a block that displays the assigned scenario numbers."""
    return {
        "Type": "Default",
        "Description": "Display Assigned Scenarios",
        "ID": "BL_DisplayScenarios",
        "BlockElements": [
            {
                "Type": "Question",
                "QuestionID": "QID_DisplayScenarios"
            }
        ],
        "Options": {
            "BlockLocking": "false",
            "RandomizeQuestions": "false",
            "BlockVisibility": "Expanded"
        }
    }

def create_input_validation_block():
    """Create a block for users to input the 5 scenario numbers."""
    return {
        "Type": "Default",
        "Description": "Input Scenario Numbers",
        "ID": "BL_InputScenarios",
        "BlockElements": [
            {
                "Type": "Question",
                "QuestionID": "QID_InputScenarios"
            }
        ],
        "Options": {
            "BlockLocking": "false",
            "RandomizeQuestions": "false",
            "BlockVisibility": "Expanded"
        }
    }

def create_dynamic_s_block(num):
    """Create an S block with dynamic iframe URL based on user input."""
    return {
        "Type": "Default",
        "Description": f"S{num}",
        "ID": f"BL_S{num}_Dynamic",
        "BlockElements": [
            {
                "Type": "Question",
                "QuestionID": f"QID_S{num}_Dynamic"
            }
        ],
        "Options": {
            "BlockLocking": "false",
            "RandomizeQuestions": "false",
            "BlockVisibility": "Expanded"
        }
    }

def create_display_question():
    """Create question showing assigned scenario numbers."""
    return {
        "SurveyID": "SV_placeholder",
        "Element": "SQ",
        "PrimaryAttribute": "QID_DisplayScenarios",
        "SecondaryAttribute": "Your assigned scenarios are:",
        "TertiaryAttribute": None,
        "Payload": {
            "QuestionText": "<strong>Your assigned scenarios are:</strong><br><br>\nScenario 1: <strong>${e://Field/scenario1}</strong><br>\nScenario 2: <strong>${e://Field/scenario2}</strong><br>\nScenario 3: <strong>${e://Field/scenario3}</strong><br>\nScenario 4: <strong>${e://Field/scenario4}</strong><br>\nScenario 5: <strong>${e://Field/scenario5}</strong><br><br>\nPlease write down these numbers before proceeding.",
            "DataExportTag": "display_scenarios",
            "QuestionType": "DB",
            "Selector": "TB",
            "DataVisibility": {
                "Private": False,
                "Hidden": False
            },
            "Configuration": {
                "QuestionDescriptionOption": "UseText"
            },
            "QuestionDescription": "Display assigned scenarios",
            "ChoiceOrder": [],
            "Validation": {
                "Settings": {
                    "Type": "None"
                }
            },
            "Language": [],
            "QuestionID": "QID_DisplayScenarios"
        }
    }

def create_input_question():
    """Create question for users to input the scenario numbers."""
    return {
        "SurveyID": "SV_placeholder",
        "Element": "SQ",
        "PrimaryAttribute": "QID_InputScenarios",
        "SecondaryAttribute": "Please enter your assigned scenario numbers",
        "TertiaryAttribute": None,
        "Payload": {
            "QuestionText": "<strong>Please enter the 5 scenario numbers shown on the previous page:</strong>",
            "DataExportTag": "input_scenarios",
            "QuestionType": "TE",
            "Selector": "FORM",
            "DataVisibility": {
                "Private": False,
                "Hidden": False
            },
            "Configuration": {
                "QuestionDescriptionOption": "UseText"
            },
            "QuestionDescription": "Input scenario numbers",
            "Validation": {
                "Settings": {
                    "ForceResponse": "ON",
                    "Type": "ContentType",
                    "ContentType": "ValidNumber"
                }
            },
            "Language": [],
            "QuestionID": "QID_InputScenarios",
            "Choices": {
                "1": {"Display": "Scenario 1"},
                "2": {"Display": "Scenario 2"},
                "3": {"Display": "Scenario 3"},
                "4": {"Display": "Scenario 4"},
                "5": {"Display": "Scenario 5"}
            },
            "ChoiceOrder": ["1", "2", "3", "4", "5"]
        }
    }

def create_dynamic_iframe_question(num):
    """Create iframe question that uses piped text from user input."""
    return {
        "SurveyID": "SV_placeholder",
        "Element": "SQ",
        "PrimaryAttribute": f"QID_S{num}_Dynamic",
        "SecondaryAttribute": f"Scenario {num}",
        "TertiaryAttribute": None,
        "Payload": {
            "QuestionText": f'<iframe src="https://hivelabuoft.github.io/ai-attribution-in-cs/pages/${{q://QID_InputScenarios/ChoiceTextEntryValue/{num}}}" \n        width="100%" \n        height="1000px" \n        frameborder="0"\n        scrolling="auto">\n</iframe>',
            "DefaultChoices": False,
            "DataExportTag": f"s{num}_dynamic",
            "QuestionType": "DB",
            "Selector": "TB",
            "DataVisibility": {
                "Private": False,
                "Hidden": False
            },
            "Configuration": {
                "QuestionDescriptionOption": "UseText"
            },
            "QuestionDescription": f"Scenario {num} iframe",
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
            "QuestionID": f"QID_S{num}_Dynamic"
        }
    }

def main():
    input_file = 'ai-attribution-in-cs-ed-master (2).qsf'
    output_file = 'ai-attribution-in-cs-ed-master-simplified.qsf'
    
    print(f"Loading {input_file}...")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Find blocks element
    blocks_element = None
    blocks_index = None
    for i, elem in enumerate(data.get('SurveyElements', [])):
        if elem.get('Element') == 'BL':
            blocks_element = elem
            blocks_index = i
            break
    
    if not blocks_element:
        print("Error: Could not find blocks element")
        return False
    
    blocks_payload = blocks_element.get('Payload', [])
    
    # Find per-vignette block
    per_vig_block = None
    for block in blocks_payload:
        if block.get('ID') == 'BL_8xeykGPs5f8ULQy':
            per_vig_block = block
            break
    
    print(f"✓ Found per-vignette block: {per_vig_block.get('ID') if per_vig_block else 'NOT FOUND'}")
    
    # Create 5 copies of per-vignette block
    new_per_vig_blocks = []
    for i in range(1, 6):
        new_block = json.loads(json.dumps(per_vig_block))
        new_block['Description'] = f'per-vignette-S{i}'
        new_block['ID'] = f'BL_PerVig_S{i}'
        new_per_vig_blocks.append(new_block)
    
    blocks_payload.extend(new_per_vig_blocks)
    print(f"✓ Created 5 per-vignette blocks (BL_PerVig_S1 - BL_PerVig_S5)")
    
    # Create 5 dynamic S blocks
    dynamic_s_blocks = []
    for i in range(1, 6):
        dynamic_s_blocks.append(create_dynamic_s_block(i))
    
    blocks_payload.extend(dynamic_s_blocks)
    print(f"✓ Created 5 dynamic S blocks (BL_S1_Dynamic - BL_S5_Dynamic)")
    
    # Add display and input blocks
    display_block = create_display_block()
    input_block = create_input_validation_block()
    blocks_payload.extend([display_block, input_block])
    print(f"✓ Created display and input blocks")
    
    # Add questions
    display_question = create_display_question()
    input_question = create_input_question()
    
    # Create 5 dynamic iframe questions
    dynamic_iframe_questions = []
    for i in range(1, 6):
        dynamic_iframe_questions.append(create_dynamic_iframe_question(i))
    
    # Insert all questions before blocks element
    questions_to_insert = [display_question, input_question] + dynamic_iframe_questions
    for i, q in enumerate(questions_to_insert):
        data['SurveyElements'].insert(blocks_index + i, q)
    
    print(f"✓ Created display, input, and 5 dynamic iframe questions")
    
    # Now restructure the Survey Flow
    flow_element = None
    for elem in data.get('SurveyElements', []):
        if elem.get('Element') == 'FL':
            flow_element = elem
            break
    
    if not flow_element:
        print("Error: Could not find Survey Flow element")
        return False
    
    flow_payload = flow_element.get('Payload', {})
    
    # Create new flow structure
    new_flow = []
    
    # 1. Embedded Data block - initialize scenario variables
    embedded_data = {
        "Type": "EmbeddedData",
        "FlowID": "FL_EmbeddedData",
        "EmbeddedData": [
            {
                "Description": "scenario1",
                "Type": "Custom",
                "Field": "scenario1",
                "VariableType": "String",
                "DataVisibility": [],
                "AnalyzeText": False,
                "Value": ""
            },
            {
                "Description": "scenario2",
                "Type": "Custom",
                "Field": "scenario2",
                "VariableType": "String",
                "DataVisibility": [],
                "AnalyzeText": False,
                "Value": ""
            },
            {
                "Description": "scenario3",
                "Type": "Custom",
                "Field": "scenario3",
                "VariableType": "String",
                "DataVisibility": [],
                "AnalyzeText": False,
                "Value": ""
            },
            {
                "Description": "scenario4",
                "Type": "Custom",
                "Field": "scenario4",
                "VariableType": "String",
                "DataVisibility": [],
                "AnalyzeText": False,
                "Value": ""
            },
            {
                "Description": "scenario5",
                "Type": "Custom",
                "Field": "scenario5",
                "VariableType": "String",
                "DataVisibility": [],
                "AnalyzeText": False,
                "Value": ""
            }
        ]
    }
    new_flow.append(embedded_data)
    
    # 2. Randomizer to assign scenario numbers evenly
    randomizer = {
        "Type": "BlockRandomizer",
        "FlowID": "FL_ScenarioRandomizer",
        "SubSet": "5",
        "EvenPresentation": True,
        "Flow": []
    }
    
    # Add all 102 scenarios to the randomizer
    for i in range(1, 103):
        randomizer["Flow"].append({
            "Type": "EmbeddedData",
            "FlowID": f"FL_Scenario{i}",
            "EmbeddedData": [
                {"Description": "scenario1", "Type": "Custom", "Field": "scenario1", "VariableType": "String", "DataVisibility": [], "AnalyzeText": False, "Value": str(i)},
                {"Description": "scenario2", "Type": "Custom", "Field": "scenario2", "VariableType": "String", "DataVisibility": [], "AnalyzeText": False, "Value": str(i)},
                {"Description": "scenario3", "Type": "Custom", "Field": "scenario3", "VariableType": "String", "DataVisibility": [], "AnalyzeText": False, "Value": str(i)},
                {"Description": "scenario4", "Type": "Custom", "Field": "scenario4", "VariableType": "String", "DataVisibility": [], "AnalyzeText": False, "Value": str(i)},
                {"Description": "scenario5", "Type": "Custom", "Field": "scenario5", "VariableType": "String", "DataVisibility": [], "AnalyzeText": False, "Value": str(i)}
            ]
        })
    
    new_flow.append(randomizer)
    
    # 3. Display block
    new_flow.append({
        "Type": "Standard",
        "ID": "BL_DisplayScenarios",
        "FlowID": "FL_DisplayScenarios"
    })
    
    # 4. Input validation block
    new_flow.append({
        "Type": "Standard",
        "ID": "BL_InputScenarios",
        "FlowID": "FL_InputScenarios"
    })
    
    # 5-14. Add 5 pairs of S blocks + per-vignette blocks
    flow_id_counter = 100
    for i in range(1, 6):
        # Dynamic S block with iframe
        new_flow.append({
            "Type": "Standard",
            "ID": f"BL_S{i}_Dynamic",
            "FlowID": f"FL_{flow_id_counter}"
        })
        flow_id_counter += 1
        
        # Per-vignette block
        new_flow.append({
            "Type": "Standard",
            "ID": f"BL_PerVig_S{i}",
            "FlowID": f"FL_{flow_id_counter}"
        })
        flow_id_counter += 1
    
    # Replace the flow
    flow_payload['Flow'] = new_flow
    flow_payload['Properties'] = {
        "Count": len(new_flow)
    }
    
    print(f"✓ Created simplified flow structure (no branches needed)")
    
    # Write output
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Successfully created {output_file}")
    print(f"   - Randomly assigns 5 scenario numbers (1-102) with even presentation")
    print(f"   - Displays assigned numbers to participants")
    print(f"   - Asks participants to input the numbers")
    print(f"   - Shows 5 S blocks with dynamic iframe URLs based on user input")
    print(f"   - Shows 5 per-vignette blocks")
    print(f"\n🎉 Ready to import into Qualtrics!")
    
    return True

if __name__ == '__main__':
    main()
