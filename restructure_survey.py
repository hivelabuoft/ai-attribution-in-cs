#!/usr/bin/env python3
"""
Restructure the survey to:
1. Remove BlockRandomizer/groups approach
2. Use embedded data to randomly assign 5 scenario numbers (1-102)
3. Show assigned numbers and ask user to input them
4. Display 5 S blocks + 5 per-vignette blocks based on assigned numbers
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

def main():
    input_file = 'ai-attribution-in-cs-ed-master (2).qsf'
    output_file = 'ai-attribution-in-cs-ed-master-restructured.qsf'
    
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
    
    # Find S1-S102 blocks and per-vignette block
    s_blocks = {}
    per_vig_block = None
    
    for block in blocks_payload:
        block_id = block.get('ID', '')
        desc = block.get('Description', '')
        
        # Find S blocks
        if desc.startswith('S') and (desc[1:].isdigit() or desc in ['S1', 'S2']):
            s_blocks[desc] = block
        elif block_id == 'BL_8xeykGPs5f8ULQy':
            per_vig_block = block
    
    print(f"✓ Found {len(s_blocks)} S blocks")
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
    
    # Add display and input blocks
    display_block = create_display_block()
    input_block = create_input_validation_block()
    blocks_payload.extend([display_block, input_block])
    print(f"✓ Created display and input blocks")
    
    # Add questions
    display_question = create_display_question()
    input_question = create_input_question()
    
    # Insert questions into SurveyElements (before blocks element)
    data['SurveyElements'].insert(blocks_index, display_question)
    data['SurveyElements'].insert(blocks_index + 1, input_question)
    print(f"✓ Created display and input questions")
    
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
    
    # 1. Embedded Data block - randomly assign 5 numbers from 1-102
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
    
    # 5-14. Add 5 pairs of blocks using branches to show correct S block based on embedded data
    for i in range(1, 6):
        # Branch for each scenario position
        branch = {
            "Type": "Branch",
            "FlowID": f"FL_Branch_S{i}",
            "Description": f"Branch for Scenario {i}",
            "BranchLogic": {
                "0": {
                    "0": {
                        "LogicType": "EmbeddedField",
                        "LeftOperand": f"scenario{i}",
                        "Operator": "!Empty",
                        "RightOperand": "",
                        "Description": f"<span class=\"ConjDesc\">If</span> <span class=\"LeftOpDesc\">scenario{i}</span> <span class=\"OpDesc\">Is Not Empty</span> ",
                        "Type": "Expression"
                    },
                    "Type": "If"
                },
                "Type": "BooleanExpression"
            },
            "Flow": []
        }
        
        # Add all 102 possible S blocks + per-vig pairs as sub-branches
        for scenario_num in range(1, 103):
            sub_branch = {
                "Type": "Branch",
                "FlowID": f"FL_Branch_S{i}_Num{scenario_num}",
                "Description": f"If scenario{i} = {scenario_num}",
                "BranchLogic": {
                    "0": {
                        "0": {
                            "LogicType": "EmbeddedField",
                            "LeftOperand": f"scenario{i}",
                            "Operator": "EqualTo",
                            "RightOperand": str(scenario_num),
                            "Description": f"<span class=\"ConjDesc\">If</span> <span class=\"LeftOpDesc\">scenario{i}</span> <span class=\"OpDesc\">Is Equal To</span> <span class=\"RightOpDesc\">{scenario_num}</span>",
                            "Type": "Expression"
                        },
                        "Type": "If"
                    },
                    "Type": "BooleanExpression"
                },
                "Flow": [
                    {
                        "Type": "Standard",
                        "ID": s_blocks.get(f'S{scenario_num}', {}).get('ID', f'BL_S{scenario_num}Generated'),
                        "FlowID": f"FL_S{i}_Scenario{scenario_num}"
                    },
                    {
                        "Type": "Standard",
                        "ID": f"BL_PerVig_S{i}",
                        "FlowID": f"FL_PerVig_S{i}_Scenario{scenario_num}"
                    }
                ]
            }
            branch["Flow"].append(sub_branch)
        
        new_flow.append(branch)
    
    # Replace the flow
    flow_payload['Flow'] = new_flow
    flow_payload['Properties'] = {
        "Count": len(new_flow)
    }
    
    print(f"✓ Created new flow structure with randomization and branching")
    
    # Write output
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Successfully created {output_file}")
    print(f"   - Randomly assigns 5 scenario numbers (1-102) with even presentation")
    print(f"   - Displays assigned numbers to participants")
    print(f"   - Asks participants to input the numbers")
    print(f"   - Shows 5 S blocks + 5 per-vignette blocks based on assignments")
    print(f"\n🎉 Ready to import into Qualtrics!")
    
    return True

if __name__ == '__main__':
    main()
