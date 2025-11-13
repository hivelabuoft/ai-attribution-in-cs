#!/usr/bin/env python3
"""
Fix per-vignette blocks in (2).qsf to create unique blocks for each scenario.
Only modifies the per-vignette block references, keeping everything else the same.
"""

import json

def main():
    input_file = 'ai-attribution-in-cs-ed-master (2).qsf'
    output_file = 'ai-attribution-in-cs-ed-master-102groups.qsf'
    
    print(f"Loading {input_file}...")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Find the blocks element
    blocks_element = None
    for elem in data.get('SurveyElements', []):
        if elem.get('Element') == 'BL':
            blocks_element = elem
            break
    
    if not blocks_element:
        print("Error: Could not find blocks element")
        return False
    
    blocks_payload = blocks_element.get('Payload', [])
    
    # Find the original per-vignette block
    per_vig_block = None
    for block in blocks_payload:
        desc = block.get('Description', '')
        if 'per-vignette' in desc.lower() or block.get('ID') == 'BL_8xeykGPs5f8ULQy':
            per_vig_block = block
            print(f"✓ Found per-vignette block: {block.get('ID')} - {desc}")
            break
    
    if not per_vig_block:
        print("Error: Could not find per-vignette block")
        return False
    
    # Create 102 unique copies of the per-vignette block
    new_per_vig_blocks = []
    for i in range(1, 103):
        new_block = json.loads(json.dumps(per_vig_block))  # Deep copy
        new_block['Description'] = f'per-vignette-S{i}'
        new_block['ID'] = f'BL_PerVig_S{i}'
        new_per_vig_blocks.append(new_block)
    
    # Add all new blocks to the payload
    blocks_payload.extend(new_per_vig_blocks)
    print(f"✓ Created {len(new_per_vig_blocks)} unique per-vignette blocks (BL_PerVig_S1 - BL_PerVig_S102)")
    
    # Now update all groups to reference their unique per-vignette blocks
    # Find Survey Flow
    flow_element = None
    for elem in data.get('SurveyElements', []):
        if elem.get('Element') == 'FL':
            flow_element = elem
            break
    
    if not flow_element:
        print("Error: Could not find Survey Flow element")
        return False
    
    flow_payload = flow_element.get('Payload', {})
    flow_items = flow_payload.get('Flow', [])
    
    # Find and update Student branch BlockRandomizer
    def find_and_update_student_randomizer(items):
        for item in items:
            if item.get('Type') == 'BlockRandomizer':
                inner_flow = item.get('Flow', [])
                for sub in inner_flow:
                    if sub.get('Type') == 'Group' and sub.get('Description', '').startswith('S'):
                        # Found it, update all groups
                        groups = [g for g in inner_flow if g.get('Type') == 'Group']
                        for group in groups:
                            desc = group.get('Description', '')
                            if desc.startswith('S') and desc[1:].isdigit():
                                scenario_num = int(desc[1:])
                                # Update the per-vignette block reference (Flow[1])
                                if 'Flow' in group and len(group['Flow']) >= 2:
                                    group['Flow'][1]['ID'] = f'BL_PerVig_S{scenario_num}'
                        print(f"✓ Updated {len(groups)} Student groups to use unique per-vignette blocks")
                        return True
            if 'Flow' in item:
                if find_and_update_student_randomizer(item['Flow']):
                    return True
        return False
    
    find_and_update_student_randomizer(flow_items)
    
    # Find and update Teaching branch BlockRandomizer
    def find_teaching_branch(items):
        for item in items:
            if item.get('Type') == 'Branch':
                logic = item.get('BranchLogic', {})
                str_logic = str(logic)
                if 'Teaching' in str_logic:
                    return item
            if 'Flow' in item:
                result = find_teaching_branch(item['Flow'])
                if result:
                    return result
        return None
    
    teaching_branch = find_teaching_branch(flow_items)
    if teaching_branch:
        teaching_flow = teaching_branch.get('Flow', [])
        
        # Find BlockRandomizer in teaching branch
        for item in teaching_flow:
            if item.get('Type') == 'BlockRandomizer':
                groups = [g for g in item['Flow'] if g.get('Type') == 'Group']
                for group in groups:
                    desc = group.get('Description', '')
                    if desc.startswith('S') and desc[1:].isdigit():
                        scenario_num = int(desc[1:])
                        # Update the per-vignette block reference (Flow[1])
                        if 'Flow' in group and len(group['Flow']) >= 2:
                            group['Flow'][1]['ID'] = f'BL_PerVig_S{scenario_num}'
                print(f"✓ Updated {len(groups)} Teaching groups to use unique per-vignette blocks")
                break
    
    # Write the modified QSF file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Successfully created {output_file}")
    print(f"   - Created 102 unique per-vignette blocks")
    print(f"   - Updated Student branch groups to reference unique blocks")
    print(f"   - Updated Teaching branch groups to reference unique blocks")
    print(f"\n🎉 Ready to import into Qualtrics!")
    
    return True

if __name__ == '__main__':
    main()
