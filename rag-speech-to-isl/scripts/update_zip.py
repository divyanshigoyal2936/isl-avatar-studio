import os
import zipfile

src_dir = r"C:\Users\laksh\.gemini\antigravity\scratch\rag-speech-to-isl"
zip_path = r"C:\Users\laksh\.gemini\antigravity\brain\e3a3317a-4f97-4c99-9d00-9bf8c45c5245\rag-speech-to-isl.zip"

print(f"Creating zip from {src_dir} to {zip_path}...")
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
    for root, dirs, files in os.walk(src_dir):
        # Exclude __pycache__, .pytest_cache, .git
        dirs[:] = [d for d in dirs if d not in ('__pycache__', '.pytest_cache', '.git')]
        for file in files:
            if file.endswith(('.pyc', '.log')) or file == 'isl_avatar.db':
                continue
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, src_dir)
            zf.write(full_path, rel_path)

print(f"Successfully created zip file of size {os.path.getsize(zip_path) / 1024:.1f} KB")
