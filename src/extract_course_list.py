import json
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Any

def find_uc_key(course_entry):
    # Return the key in course_entry that looks like the UC side:
    # any key that starts with "UC" (case-insensitive) or contains "University of California"
    for k in course_entry:
        if not isinstance(k, str):
            continue
        low = k.lower()
        if low.startswith('uc') or 'university of california' in low:
            return k
    return None

def map_uc_dvc(obj: Dict[str, Any], campus_key: str = "Berkeley"):
    """
    Returns:
      { uc_course_code: {
            'uc_title': str,
            'uc_units': number,
            'category': str,
            'dvc': [ { 'code':..., 'title':..., 'units':... }, ... ]
        }, ... }
    """
    out = {} #empty dict to return, Keys: UC course codes
    items = obj.get(campus_key, []) # retrieves top level key with Year metadata
    # items is a list
    for block in items:
        # Skip entries that are metadata (like Year) Only check "category" blocks
        if not isinstance(block, dict) or 'Category' not in block:
            continue
        cat = block.get('Category') #Read category string
        #Iterate through the courses
        for course_entry in block.get('Courses', []):
            uc_key = find_uc_key(course_entry)
            uc = course_entry.get(uc_key) if uc_key else None
            dvc = course_entry.get('DVC')
            if not uc:
                continue
            uc_code = uc.get('Course_Code')

            #Remove whitespace
            if uc_code:
                uc_code = uc_code.strip()

            record = out.setdefault(uc_code, {
                'uc_title': uc.get('Title'),
                'uc_units': uc.get('Units'),
                'category': cat,
                'dvc': []
            })
            # DVC may be a dict or a list
            if isinstance(dvc, dict):
                record['dvc'].append({
                    'code': dvc.get('Course_Code'),
                    'title': dvc.get('Title'),
                    'units': dvc.get('Units')
                })
            elif isinstance(dvc, list):
                for d in dvc:
                    record['dvc'].append({
                        'code': d.get('Course_Code'),
                        'title': d.get('Title'),
                        'units': d.get('Units')
                    })
    return out


#-----------Initialize all course data-----------
#UCSD
ucsd = Path("agreements_25-26/ucsd_25-26_cs.json")
if not ucsd.exists():
    raise FileNotFoundError(f"{ucsd} not found")

with ucsd.open('r', encoding='utf-8') as f:
    ucsd_data = json.load(f)

ucsd_map = map_uc_dvc(ucsd_data, campus_key="San_Diego")
#UCB
ucb = Path("agreements_25-26/ucb_25-26_cs.json")
if not ucb.exists():
    raise FileNotFoundError(f"{ucb} not found")

with ucb.open('r', encoding='utf-8') as f:
    ucb_data = json.load(f)

ucb_map = map_uc_dvc(ucb_data, campus_key="Berkeley")
#UCI
uci = Path("agreements_25-26/uci_25-26_cs.json")
if not uci.exists():
    raise FileNotFoundError(f"{uci} not found")

with uci.open('r', encoding='utf-8') as f:
    uci_data = json.load(f)

uci_map= map_uc_dvc(uci_data, campus_key="Irvine")
#UCLA
ucla = Path("agreements_25-26/ucla_24-25_cs.json")
if not ucla.exists():
    raise FileNotFoundError(f"{ucla} not found")

with ucla.open('r', encoding='utf-8') as f:
    ucla_data = json.load(f)

ucla_map= map_uc_dvc(ucla_data, campus_key="Los Angeles")
#UCD
ucd = Path("agreements_25-26/ucd_24-25_cs.json")
if not ucd.exists():
    raise FileNotFoundError(f"{ucd} not found")

with ucd.open('r', encoding='utf-8') as f:
    ucd_data = json.load(f)

ucd_map= map_uc_dvc(ucd_data, campus_key="Davis")

"""
#Test UCSD
print("***Suggest the minimum courses I must complete this semester to be eligible for transfer next year to UC San Diego.***")
print("Found UCSD courses:", len(ucsd_map))
for i, (uc_code, info) in enumerate(sorted(ucsd_map.items())):
    print(f"{uc_code} -> DVC: {[d['code'] for d in info['dvc']]}")
#print(list(ucsd_map.items())[:2])  # show first 2 items in detail
print()

#UCSD and UCB
print("***I want to apply to both UC San Diego and UC Berkeley to transfer, what courses do I need to satisfy the requirements for both schools?***")
print("Found UCB and UCSD courses:", len(ucb_map)+len(ucsd_map))
print("-----UCB-----")
for i, (uc_code, info) in enumerate(sorted(ucb_map.items())):
    print(f"{uc_code} -> DVC: {[d['code'] for d in info['dvc']]}")
print("-----UCSD-----")
for i, (uc_code, info) in enumerate(sorted(ucsd_map.items())):
    print(f"{uc_code} -> DVC: {[d['code'] for d in info['dvc']]}")

print()
#UCI Test
print("***What DVC courses should I take to transfer into the Computer Science major at UC Irvine?***")
print("Found UCI courses:", len(uci_map))
for i, (uc_code, info) in enumerate(sorted(uci_map.items())):
    print(f"{uc_code} -> DVC: {[d['code'] for d in info['dvc']]}")

print()
#UCB and UCLA
print("***Is there one course list that works for both UC Berkeley and UCLA?***")
print("Found UCB and UCLA courses:", len(ucb_map)+len(ucla_map))
print("-----UCB-----")
for i, (uc_code, info) in enumerate(sorted(ucb_map.items())):
    print(f"{uc_code} -> DVC: {[d['code'] for d in info['dvc']]}")
print("-----UCLA-----")
for i, (uc_code, info) in enumerate(sorted(ucla_map.items())):
    print(f"{uc_code} -> DVC: {[d['code'] for d in info['dvc']]}")

print()
#UCD Test
print("***I want to see the DVC course equivalents for UC Davis courses.***")
print("Found UCD courses:", len(ucd_map))
for i, (uc_code, info) in enumerate(sorted(ucd_map.items())):
    print(f"{uc_code} -> DVC: {[d['code'] for d in info['dvc']]}")

print()
#UCD Math
print("***What math classes does UC Davis require for computer science transfers?***")
print("Found UCD Mathematics courses:", len([1 for info in ucd_map.values() if 'Mathematics' in (info.get('category'))]))
for uc_code, info in sorted(ucd_map.items()):
    # info stores the category under the lower-case 'category' key in map_uc_dvc
    if 'Mathematics' in (info.get('category') or ''):
        print(f"{uc_code} -> DVC: {[d['code'] for d in info['dvc']]}")

print()
#UCLA Test
print("***I’m currently registered for COMSC-110 at DVC. Does UCLA accept this course for a UC computer science transfer?***")
print("Found UCLA courses:", len(ucla_map))
for i, (uc_code, info) in enumerate(sorted(ucla_map.items())):
    print(f"{uc_code} -> DVC: {[d['code'] for d in info['dvc']]}")
"""