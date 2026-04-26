# Aviator Game - Setup Instructions

## Current Status
The website is now configured to display the Aviator game via an iframe on the `/game` page.

## Required Steps to Complete Setup

### 1. Export the Godot Project to HTML5

To make the game playable on the web, you need to export your Godot project to HTML5:

1. **Open your Godot project** from the `aviator/` folder
2. **Go to Project → Export** (or Ctrl+Shift+E)
3. **Create a new export preset** if you don't have one:
   - Click "Add Preset" 
   - Select "HTML5"
4. **Configure the export settings:**
   - Set the Export Path to: `static/game/aviator.html5`
   - Make sure "HTML5" is selected
   - Optionally adjust rendering and physics settings as needed
5. **Export the project:**
   - Click "Export" or "Export Project" button
   - Choose the export folder as `static/game/`

### 2. Required Export Files

After exporting, the following files should be present in the `static/game/` directory:

- `index.html` ← Already created for you
- `aviator.html5` ← Godot main export file (generated after export)
- `aviator.html5.js` ← Game logic
- `aviator.html5.wasm` ← WebAssembly binary
- `aviator.html5.pck` ← Game resources/pack file
- Any additional `.js` files needed by Godot

### 3. Test the Game

1. Run your Flask server: `python main.py`
2. Navigate to `http://localhost:5000/game`
3. You should see the Aviator game loaded in the iframe

## If the Game Doesn't Load

**Check the following:**
- ✓ All exported files are in the `static/game/` directory
- ✓ The `index.html` file exists and isn't corrupted
- ✓ Browser console (F12) for any error messages
- ✓ Ensure the export was done in HTML5 format
- ✓ Check that the Godot export files match the names referenced in `index.html`

## File Structure

```
static/
└── game/
    ├── index.html              (Entry point)
    ├── aviator.html5           (Godot export main file)
    ├── aviator.html5.js        (Godot JavaScript)
    ├── aviator.html5.wasm      (WebAssembly binary)
    ├── aviator.html5.pck       (Game resources)
    └── [other Godot files]
```

## Additional Notes

- The game is embedded in an iframe on `http://localhost:5000/game`
- The iframe is responsive and will adjust to different screen sizes
- On mobile devices, the game height is set to 400px for better usability
- The `main.py` Flask app already has a route for `/game` that renders `game.html`

For more information about Godot HTML5 exports, visit: https://docs.godotengine.org/en/stable/tutorials/export/exporting_for_web.html
