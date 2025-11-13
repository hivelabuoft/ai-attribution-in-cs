#!/usr/bin/env python3
"""
Create a clean version starting directly from (2).qsf,
only modifying what's necessary and preserving all original structure.
"""

import json

def main():
    input_file = 'ai-attribution-in-cs-ed-master (2).qsf'
    output_file = 'ai-attribution-in-cs-ed-master-clean.qsf'
    
    print(f"Loading {input_file}...")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Keep original SurveyEntry unchanged
    print(f"✓ Preserving SurveyEntry")
    
    # Find blocks element
    blocks_element = None
    blocks_index = None
    for i, elem in enumerate(data.get('SurveyElements', [])):
        if elem.get('Element') == 'BL':
            blocks_element = elem
            blocks_index = i
            break
    
    blocks_payload = blocks_element.get('Payload', [])
    
    # Find per-vignette block
    per_vig_block = None
    for block in blocks_payload:
        if block.get('ID') == 'BL_8xeykGPs5f8ULQy':
            per_vig_block = block
            break
    
    print(f"✓ Found per-vignette block")
    
    # Create 5 copies of per-vignette block
    for i in range(1, 6):
        new_block = json.loads(json.dumps(per_vig_block))
        new_block['Description'] = f'per-vignette-S{i}'
        new_block['ID'] = f'BL_PerVig_S{i}'
        blocks_payload.append(new_block)
    
    print(f"✓ Created 5 per-vignette blocks")
    
    # Create 5 dynamic S blocks
    for i in range(1, 6):
        blocks_payload.append({
            "Type": "Default",
            "Description": f"S{i}_Dynamic",
            "ID": f"BL_S{i}_Dynamic",
            "BlockElements": [{"Type": "Question", "QuestionID": f"QID_S{i}_Dynamic"}],
            "Options": {
                "BlockLocking": "false",
                "RandomizeQuestions": "false",
                "BlockVisibility": "Expanded"
            }
        })
    
    print(f"✓ Created 5 dynamic S blocks")
    
    # Create display and input blocks
    blocks_payload.append({
        "Type": "Default",
        "Description": "Display Assigned Scenarios",
        "ID": "BL_DisplayScenarios",
        "BlockElements": [{"Type": "Question", "QuestionID": "QID_DisplayScenarios"}],
        "Options": {
            "BlockLocking": "false",
            "RandomizeQuestions": "false",
            "BlockVisibility": "Expanded"
        }
    })
    
    blocks_payload.append({
        "Type": "Default",
        "Description": "Input Scenario Numbers",
        "ID": "BL_InputScenarios",
        "BlockElements": [{"Type": "Question", "QuestionID": "QID_InputScenarios"}],
        "Options": {
            "BlockLocking": "false",
            "RandomizeQuestions": "false",
            "BlockVisibility": "Expanded"
        }
    })
    
    print(f"✓ Created display and input blocks")
    
    # Get a sample SurveyID from existing questions
    sample_survey_id = None
    for elem in data['SurveyElements']:
        if elem.get('Element') == 'SQ':
            sample_survey_id = elem.get('SurveyID')
            break
    
    # Create questions
    questions_to_add = []
    
    # Display question
    questions_to_add.append({
        "SurveyID": sample_survey_id,
        "Element": "SQ",
        "PrimaryAttribute": "QID_DisplayScenarios",
        "SecondaryAttribute": "Your assigned scenarios are:",
        "TertiaryAttribute": None,
        "Payload": {
            "QuestionText": "<strong>Your assigned scenarios are:</strong><br><br>\\nScenario 1: <strong>\${e://Field/scenario1}</strong><br>\\nScenario 2: <strong>\${e://Field/scenario2}</strong><br>\\nScenario 3: <strong>\${e://Field/scenario3}</strong><br>\\nScenario 4: <strong>\${e://Field/scenario4}</strong><br>\\nScenario 5: <strong>\${e://Field/scenario5}</strong><br><br>\\nPlease write down these numbers before proceeding.",
            "DataExportTag": "display_scenarios",
            "QuestionType": "DB",
            "Selector": "TB",
            "DataVisibility": {"Private": False, "Hidden": False},
            "Configuration": {"QuestionDescriptionOption": "UseText"},
            "QuestionDescription": "Display assigned scenarios",
            "ChoiceOrder": [],
            "Validation": {"Settings": {"Type": "None"}},
            "Language": [],
            "QuestionID": "QID_DisplayScenarios"
        }
    })
    
    # Input question
    questions_to_add.append({
        "SurveyID": sample_survey_id,
        "Element": "SQ",
        "PrimaryAttribute": "QID_InputScenarios",
        "SecondaryAttribute": "Please enter your assigned scenario numbers",
        "TertiaryAttribute": None,
        "Payload": {
            "QuestionText": "<strong>Please enter the 5 scenario numbers shown on the previous page:</strong>",
            "DataExportTag": "input_scenarios",
            "QuestionType": "TE",
            "Selector": "FORM",
            "DataVisibility": {"Private": False, "Hidden": False},
            "Configuration": {"QuestionDescriptionOption": "UseText"},
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
    })
    
    # Dynamic iframe questions
    for i in range(1, 6):
        questions_to_add.append({
            "SurveyID": sample_survey_id,
            "Element": "SQ",
            "PrimaryAttribute": f"QID_S{i}_Dynamic",
            "SecondaryAttribute": f"Scenario {i}",
            "TertiaryAttribute": None,
            "Payload": {
                "QuestionText": f'<iframe src="https://hivelabuoft.github.io/ai-attribution-in-cs/pages/\${{q://QID_InputScenarios/ChoiceTextEntryValue/{i}}}" \\n        width="100%" \\n        height="1000px" \\n        frameborder="0"\\n        scrolling="auto">\\n</iframe>',
                "DefaultChoices": False,
                "DataExportTag": f"s{i}_dynamic",
                "QuestionType": "DB",
                "Selector": "TB",
                "DataVisibility": {"Private": False, "Hidden": False},
                "Configuration": {"QuestionDescriptionOption": "UseText"},
                "QuestionDescription": f"Scenario {i} iframe",
                "ChoiceOrder": [],
                "Validation": {"Settings": {"Type": "None"}},
                "GradingData": [],
                "Language": [],
                "NextChoiceId": 4,
                "NextAnswerId": 1,
                "QuestionID": f"QID_S{i}_Dynamic"
            }
        })
    
    # Insert questions before blocks element
    for i, q in enumerate(questions_to_add):
        data['SurveyElements'].insert(blocks_index + i, q)
    
    print(f"✓ Created {len(questions_to_add)} questions")
    
    # Modify Survey Flow
    flow_element = None
    for elem in data.get('SurveyElements', []):
        if elem.get('Element') == 'FL':
            flow_element = elem
            break
    
    flow_payload = flow_element.get('Payload', {})
    original_flow = flow_payload.get('Flow', [])
    
    # Create new flow
    new_flow = []
    
    # 1. Embedded Data
    new_flow.append({
        "Type": "EmbeddedData",
        "FlowID": "FL_EmbeddedData",
        "EmbeddedData": [
            {"Description": f"scenario{i}", "Type": "Custom", "Field": f"scenario{i}", 
             "VariableType": "String", "DataVisibility": [], "AnalyzeText": False, "Value": ""}
            for i in range(1, 6)
        ]
    })
    
    # 2. BlockRandomizer with Groups
    randomizer = {
        "Type": "BlockRandomizer",
        "FlowID": "FL_ScenarioRandomizer",
        "SubSet": "1",
        "EvenPresentation": True,
        "Flow": []
    }
    
    # Create 102 groups with different scenario combinations
    for i in range(1, 103):
        scenarios = []
        for j in range(5):
            idx = (i - 1 + j * 20) % 102
            scenarios.append(idx + 1)
        
        randomizer["Flow"].append({
            "Type": "Group",
            "FlowID": f"FL_Group{i}",
            "Description": f"Scenario Combo {i}",
            "Flow": [{
                "Type": "EmbeddedData",
                "FlowID": f"FL_SetScenarios{i}",
                "EmbeddedData": [
                    {"Description": f"scenario{j+1}", "Type": "Custom", "Field": f"scenario{j+1}",
                     "VariableType": "String", "DataVisibility": [], "AnalyzeText": False, "Value": str(scenarios[j])}
                    for j in range(5)
                ]
            }]
        })
    
    new_flow.append(randomizer)
    
    # 3-4. Display and Input blocks
    new_flow.extend([
        {"Type": "Standard", "ID": "BL_DisplayScenarios", "FlowID": "FL_DisplayScenarios"},
        {"Type": "Standard", "ID": "BL_InputScenarios", "FlowID": "FL_InputScenarios"}
    ])
    
    # 5-14. Dynamic S blocks + per-vignette blocks
    flow_id = 100
    for i in range(1, 6):
        new_flow.append({"Type": "Standard", "ID": f"BL_S{i}_Dynamic", "FlowID": f"FL_{flow_id}"})
        flow_id += 1
        new_flow.append({"Type": "Standard", "ID": f"BL_PerVig_S{i}", "FlowID": f"FL_{flow_id}"})
        flow_id += 1
    
    # Replace flow
    flow_payload['Flow'] = new_flow
    flow_payload['Properties'] = {"Count": len(new_flow)}
    
    print(f"✓ Created new flow with {len(new_flow)} items")
    
    # Write output
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\\n✅ Successfully created {output_file}")
    print(f"   - Based directly on original (2).qsf")
    print(f"   - Preserves all original metadata")
    print(f"   - 5 dynamic iframe blocks with piped text")
    print(f"   - 5 per-vignette blocks")
    print(f"   - 102 scenario combinations evenly distributed")
    
    return True

if __name__ == '__main__':
    main()
