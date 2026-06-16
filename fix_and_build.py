import os
import http.server
import socketserver
import webbrowser
import json

# ================= CONFIGURATION =================
PORT = 8000
script_location = os.path.dirname(os.path.abspath(__file__))
SOUNDS_DIR = os.path.join(script_location, "sounds")
OUTPUT_FILE = os.path.join(script_location, "index.html")

# ================= DESIGN UPGRADE =================
html_part_1 = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ultimate Soundboard</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;800&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-color: #0f0c29;
            --card-bg: #24243e;
            --accent: #00f260;
            --accent-grad: linear-gradient(to right, #0575E6, #021B79);
        }

        body {
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            color: white;
            text-align: center;
            min-height: 100vh;
            margin: 0;
            padding: 40px 20px;
        }

        h1 {
            font-weight: 800;
            font-size: 3rem;
            margin-bottom: 10px;
            background: -webkit-linear-gradient(#00f260, #0575E6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0px 0px 20px rgba(0, 242, 96, 0.3);
        }

        /* SEARCH BAR */
        #search-box {
            padding: 15px;
            width: 100%;
            max-width: 400px;
            border-radius: 50px;
            border: none;
            background: rgba(255, 255, 255, 0.1);
            color: white;
            font-size: 1.1rem;
            text-align: center;
            margin-bottom: 30px;
            backdrop-filter: blur(10px);
            outline: none;
            transition: 0.3s;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }
        #search-box:focus {
            background: rgba(255, 255, 255, 0.2);
            box-shadow: 0 0 15px #0575E6;
        }

        /* RANDOM BUTTON */
        #random-btn {
            background: linear-gradient(45deg, #ff416c, #ff4b2b);
            color: white;
            border: none;
            padding: 15px 50px;
            border-radius: 50px;
            font-size: 1.2rem;
            font-weight: 700;
            cursor: pointer;
            margin-bottom: 40px;
            box-shadow: 0 10px 20px rgba(255, 75, 43, 0.3);
            transition: transform 0.2s, box-shadow 0.2s;
        }
        #random-btn:hover { transform: translateY(-3px) scale(1.05); box-shadow: 0 15px 30px rgba(255, 75, 43, 0.5); }
        #random-btn:active { transform: scale(0.95); }

        /* GRID */
        #board {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
            gap: 20px;
            max-width: 1200px;
            margin: 0 auto;
        }

        /* CARDS */
        .buzzer {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            color: #e0e0e0;
            padding: 20px;
            border-radius: 20px;
            cursor: pointer;
            font-size: 0.95rem;
            font-weight: 600;
            transition: all 0.2s ease;
            backdrop-filter: blur(5px);
            word-wrap: break-word;
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 100px;
            position: relative;
            overflow: hidden;
        }

        /* Hover Effect */
        .buzzer:hover {
            background: rgba(255, 255, 255, 0.15);
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.3);
            border-color: #00f260;
            color: white;
        }

        /* Click Effect */
        .buzzer:active {
            transform: scale(0.95);
            background: #00f260;
            color: black;
            box-shadow: 0 0 20px #00f260;
            border-color: #00f260;
        }

        /* Playing State (Added by JS) */
        .playing {
            background: linear-gradient(45deg, #0575E6, #021B79) !important;
            border: 1px solid #0575E6 !important;
            color: white !important;
            box-shadow: 0 0 15px #0575E6 !important;
            animation: pulse 1s infinite;
        }

        @keyframes pulse {
            0% { box-shadow: 0 0 0 0 rgba(5, 117, 230, 0.7); }
            70% { box-shadow: 0 0 0 10px rgba(5, 117, 230, 0); }
            100% { box-shadow: 0 0 0 0 rgba(5, 117, 230, 0); }
        }

    </style>
</head>
<body>
    <h1>⚡ SONIC BOARD</h1>
    
    <input type="text" id="search-box" placeholder="🔍 Search sounds..." onkeyup="filterSounds()">
    <br>
    <button id="random-btn" onclick="playRandom()">🎲 SURPRISE ME</button>

    <div id="board">
"""

def setup_and_run():
    if not os.path.exists(SOUNDS_DIR):
        print("❌ Error: 'sounds' folder is missing!")
        return

    files = sorted(os.listdir(SOUNDS_DIR))
    buttons_html = ""
    safe_filenames_list = []
    counter = 1
    
    print(f"🎨 Designing {len(files)} buttons...")

    for original_name in files:
        if original_name.startswith('.') or not original_name.endswith('.mp3'): 
            continue

        # Keep existing track names if possible
        if original_name.startswith("track_"):
            safe_filename = original_name
            # If the user manually named it track_1, we default to "Sound 1"
            display_label = original_name.replace("track_", "Sound ").replace(".mp3", "")
        else:
            safe_filename = f"track_{counter}.mp3"
            src = os.path.join(SOUNDS_DIR, original_name)
            dst = os.path.join(SOUNDS_DIR, safe_filename)
            try:
                os.rename(src, dst)
            except:
                pass 
            # Make the label look nice (Capitalize, remove dashes)
            display_label = original_name.replace(".mp3", "").replace("_", " ").replace("-", " ")

        safe_filenames_list.append(safe_filename)

        # ADD THE ID so we can highlight it later
        buttons_html += f"""
        <div class="buzzer" id="btn-{safe_filename}" onclick="play('{safe_filename}')">
            {display_label}
        </div>
        """
        counter += 1

    js_array = json.dumps(safe_filenames_list)

    # === JAVASCRIPT ===
    html_script = f"""
    </div>
    <script>
        const allSounds = {js_array};
        let currentAudio = null;
        let currentBtn = null;

        function play(filename) {{
            // 1. Reset old button style
            if (currentBtn) {{
                currentBtn.classList.remove('playing');
            }}

            // 2. Stop old audio
            if (currentAudio) {{
                currentAudio.pause();
                currentAudio.currentTime = 0;
            }}

            // 3. Find new button
            const btnId = "btn-" + filename;
            const newBtn = document.getElementById(btnId);
            
            // 4. Play and Style
            if (newBtn) {{
                newBtn.classList.add('playing');
                currentBtn = newBtn;
            }}

            currentAudio = new Audio('sounds/' + filename);
            currentAudio.play();

            // When sound finishes, remove style
            currentAudio.onended = function() {{
                if (newBtn) newBtn.classList.remove('playing');
            }};
        }}

        function playRandom() {{
            const randomIndex = Math.floor(Math.random() * allSounds.length);
            play(allSounds[randomIndex]);
        }}

        function filterSounds() {{
            const input = document.getElementById('search-box');
            const filter = input.value.toLowerCase();
            const buttons = document.getElementsByClassName('buzzer');

            for (let i = 0; i < buttons.length; i++) {{
                const txtValue = buttons[i].innerText;
                if (txtValue.toLowerCase().indexOf(filter) > -1) {{
                    buttons[i].style.display = "flex";
                }} else {{
                    buttons[i].style.display = "none";
                }}
            }}
        }}
    </script>
</body>
</html>
    """

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html_part_1 + buttons_html + html_script)
    
    print(f"✅ Design Upgrade Complete! Opening now...")

    os.chdir(script_location)
    Handler = http.server.SimpleHTTPRequestHandler
    socketserver.TCPServer.allow_reuse_address = True
    
    try:
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print(f"\n🚀 SERVER STARTED at http://localhost:{PORT}")
            webbrowser.open(f"http://localhost:{PORT}")
            httpd.serve_forever()
    except:
        print("⚠️ Port 8000 is busy. Please close other Python windows.")

if __name__ == "__main__":
    setup_and_run()