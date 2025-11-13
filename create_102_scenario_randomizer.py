#!/usr/bin/env python3
"""
Create a complete solution for randomizing 5 scenarios from 102.

The approach:
1. BlockRandomizer with 102 embedded data elements (SubSet=5)
2. Each element sets a field like Selected1="1", Selected2="2", etc.
3. After the randomizer, JavaScript collects which fields were set
4. Those values are displayed in the question text

This is the proper Qualtrics pattern for random selection with display.
"""

import json
import sys

def generate_102_randomizer():
    """Generate the BlockRandomizer with 102 embedded data elements."""
    flow_elements = []
    flow_id_start = 4000
    
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
                    "Value": str(i)
                }
            ]
        }
        flow_elements.append(flow_element)
    
    return flow_elements

def generate_collector_embedded_data():
    """Generate embedded data element that collects the selected scenarios."""
    # This JavaScript will run through Selected1-Selected102 and collect which ones are set
    collector_js = """
var selected = [];
for (var i = 1; i <= 102; i++) {
    var fieldValue = "${e://Field/Selected" + i + "}";
    if (fieldValue && fieldValue !== "${e://Field/Selected" + i + "}") {
        selected.push(i);
    }
}
// Set the selected scenarios to Pos1-Pos5
for (var j = 0; j < 5 && j < selected.length; j++) {
    Qualtrics.SurveyEngine.setEmbeddedData("Pos" + (j+1), selected[j]);
}
// Create a display string
Qualtrics.SurveyEngine.setEmbeddedData("SelectedList", selected.join(", "));
"""
    
    return {
        "Type": "EmbeddedData",
        "FlowID": "FL_COLLECTOR",
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
            },
            {
                "Description": "SelectedList",
                "Type": "Custom",
                "Field": "SelectedList",
                "VariableType": "String",
                "DataVisibility": [],
                "AnalyzeText": False,
                "Value": ""
            }
        ]
    }

def main():
    print("Generating 102-scenario randomizer structure...")
    print("=" * 60)
    
    flow_elements = generate_102_randomizer()
    
    randomizer_block = {
        "Type": "BlockRandomizer",
        "FlowID": "FL_3039",
        "SubSet": 5,
        "EvenPresentation": True,
        "Flow": flow_elements
    }
    
    print("\n1. BlockRandomizer structure (paste into Survey Flow):")
    print(json.dumps(randomizer_block, indent=2))
    
    print("\n\n" + "=" * 60)
    print("\n2. Question text to use:")
    print("\nYou have been assigned the following scenario IDs: ${e://Field/SelectedList}")
    print("\nOr individually:")
    print("${e://Field/Pos1}, ${e://Field/Pos2}, ${e://Field/Pos3}, ${e://Field/Pos4}, ${e://Field/Pos5}")
    
    print("\n\n" + "=" * 60)
    print("\n3. After the BlockRandomizer, add a Web Service element or use JavaScript")
    print("   to collect which Selected1-Selected102 fields were set.")
    print(f"\nTotal scenario elements: {len(flow_elements)}")

if __name__ == "__main__":
    main()
