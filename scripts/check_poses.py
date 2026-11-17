import re

with open(r'C:\Users\laksh\.gemini\antigravity\scratch\rag-speech-to-isl\frontend\public\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the COMPUTED_POSES block
start = content.find('const COMPUTED_POSES = {')
# Find the closing }; of the block
# It should be the next line that has just '    };' after the start
end = content.find('\n    };\n', start + 100) + 7
block = content[start:end]

print(f'COMPUTED_POSES block length: {len(block)} chars')
print(f'Block starts at char: {start}')

# Print just the top level structure (lines starting with 6+ spaces and a quote)
lines = block.splitlines()
for i, line in enumerate(lines[:5]):
    print(f'{i}: {line}')

# Show all immediate sign keys 
top_keys = []
for line in lines:
    stripped = line.strip()
    if stripped.startswith('"') and '": {' in stripped:
        key = stripped.split('"')[1]
        top_keys.append(key)
        print(f'  KEY: {key}')
