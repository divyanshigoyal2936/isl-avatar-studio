text = open(r'C:\Users\laksh\.gemini\antigravity\scratch\rag-speech-to-isl\frontend\public\index.html', encoding='utf-8').read()
signs = ['HELLO', 'THANK-YOU', 'WELCOME', 'PLEASE', 'NAME', 'WHAT', 'WHERE', 'HOW', 'YOU', 'ME', 'HELP', 'WATER', 'FOOD', 'HOSPITAL', 'DOCTOR', 'TIME', 'TODAY', 'GOOD', 'MORNING', 'YES', 'NO', 'INDIA', 'NICE', 'MEET']

results = {}
for s in signs:
    key = f'norm === "{s}"'
    results[s] = key in text

print("Verification of 24 signs in index.html:")
for s, ok in results.items():
    print(f"  {s}: {'OK' if ok else 'MISSING'}")

all_present = all(results.values())
print(f"\nALL 24 SIGNS PRESENT: {all_present}")
