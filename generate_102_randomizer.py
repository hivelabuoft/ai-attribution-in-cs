#!/usr/bin/env python3
"""
Generate 102 embedded data elements for the BlockRandomizer.
Each element in the randomizer will set ALL 5 position variables (Pos1-Pos5) to its scenario number.
When BlockRandomizer selects 5 elements, they'll sequentially fill positions 1-5.
"""

import json

# Generate 102 embedded data flow elements
flow_elements = []
flow_id_start = 4000  # Start with a high number to avoid conflicts

for i in range(1, 103):  # 1 to 102
    # Each element sets all 5 position variables to its own number
    # The BlockRandomizer will select 5 of these and present them in order
    # So the first selected will set Pos1=i, second selected sets Pos2=i, etc.
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

# Print the JSON structure
output = {
    "Type": "BlockRandomizer",
    "FlowID": "FL_3039",
    "SubSet": 5,
    "EvenPresentation": True,
    "Flow": flow_elements
}

print(json.dumps(output, indent=2))
print(f"\n\nTotal elements generated: {len(flow_elements)}")
