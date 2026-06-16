import os

# ==========================================
# 🔧 AUTO-FIX: Get the folder where THIS script is located
# ==========================================
script_location = os.path.dirname(os.path.abspath(__file__))
SOUNDS_DIR = os.path.join(script_location, "sounds")
OUTPUT_FILE = os.path.join(script_location, "index.html")
# ==========================================

# HTML Template
html_start = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Soundboard</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background-color: #2c3e50; color: white; text-align: center; padding: 20px; }
        h1 { margin-bottom: 30px; }
        #board { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 20px; max-width: 1000px; margin: 0 auto; }
        .buzzer {
            background-color: #e74c3c; border: none; border-radius: 15px; padding: 30px 10px;
            font-size: 1.2rem; font-weight: bold; color: white; cursor: pointer;
            box-shadow: 0 8px 0 #c0392b; transition: all 0.1s; text-transform: capitalize;
            overflow: hidden; text-overflow: ellipsis;
        }
        .buzzer:active { box-shadow: 0 0 0 #c0392b; transform: translateY(8px); }
        .buzzer:nth-child(even) { background-color: #3498db; box-shadow: 0 8px 0 #2980b9; }
        .buzzer:nth-child(even):active { box-shadow: 0 0 0 #2980b9; }
    </style>
</head>
<body>
    <h1>🔊 Auto-Generated Soundboard</h1>
    <div id="board">
"""

html_end = """
    </div>
    <script>
        function playSound(filename) {
            // Encode the filename to handle spaces and special characters
            const path = 'sounds/' + encodeURIComponent(filename);
            new Audio(path).play();
        }
    </script>
</body>
</html>
"""

def generate():
    print(f"📍 Script is running in: {script_location}")
    print(f"🔎 Looking for sounds in: {SOUNDS_DIR}")

    # 1. Check if sounds folder exists
    if not os.path.exists(SOUNDS_DIR):
        print("\n❌ CRITICAL ERROR: Folder not found!")
        print(f"   I expected to find a folder here:\n   {SOUNDS_DIR}")
        print("   👉 Make sure the folder is named exactly 'sounds' (lowercase).")
        return

    # 2. Get all audio files
    files = [f for f in os.listdir(SOUNDS_DIR) if f.lower().endswith(('.mp3', '.wav', '.ogg', '.m4a'))]
    
    if not files:
        print("\n❌ Folder found, but it is EMPTY (or has no mp3/wav files).")
        print(f"   Files currently in that folder: {os.listdir(SOUNDS_DIR)}")
        return

    print(f"✅ Found {len(files)} sounds. Building website...")

    # 3. Generate HTML Buttons
    buttons_html = ""
    for sound in files:
        display_name = sound.rsplit('.', 1)[0].replace('-', ' ').replace('_', ' ')
        # We pass the raw filename to JS, but display the clean name
        buttons_html += f"""        <button class="buzzer" onclick="playSound('{sound}')">{display_name}</button>\n"""

    # 4. Write the final file
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html_start + buttons_html + html_end)

    print(f"🎉 Success! Created: {OUTPUT_FILE}")

if __name__ == "__main__":
    generate()