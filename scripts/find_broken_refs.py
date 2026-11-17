"""
Find all broken references in getPoseForSign that access non-existent keys
"""
with open(r'C:\Users\laksh\.gemini\antigravity\scratch\rag-speech-to-isl\frontend\public\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.splitlines()

# Find getPoseForSign function range
start_line = None
end_line = None
for i, line in enumerate(lines):
    if 'function getPoseForSign' in line:
        start_line = i
    if start_line and i > start_line and line.strip() == '}' and end_line is None:
        # Check if it's the end of the function
        if i - start_line > 10:
            end_line = i
            break

print(f'getPoseForSign: lines {start_line+1} to {end_line+1 if end_line else "?"}')

# Find broken references
for i, line in enumerate(lines):
    if 'COMPUTED_POSES.' in line:
        # Extract the access pattern
        import re
        matches = re.findall(r'COMPUTED_POSES\.(\w+)\.(\w+)', line)
        for m in matches:
            sign_key = m[0]
            sub_key = m[1]
            if sub_key not in ('leftArm', 'rightArm', 'desc'):
                print(f'  Line {i+1}: COMPUTED_POSES.{sign_key}.{sub_key} -- POSSIBLY BROKEN')
            else:
                pass  # These are valid
