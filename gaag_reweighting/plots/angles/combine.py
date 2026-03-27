import sys 
from PIL import Image

input_paths = [ "plots/angles/C5_alpha_C4p-P.png",
                "plots/angles/G6_alpha_C4p-P.png",
                "plots/angles/A7_alpha_C4p-P.png",
                "plots/angles/A8_alpha_C4p-P.png",
                "plots/angles/G9_alpha_C4p-P.png",
                "plots/angles/G10_alpha_C4p-P.png"]

if len(input_paths) != 6:
    print("Fehler: 6 Bildpfade müssen angegeben werden.")
    sys.exit(1)

# Alle Bilder öffnen
images = [Image.open(p) for p in input_paths]

# Optional: sicherstellen, dass alle die gleiche Größe haben
w, h = images[0].size
for img in images[1:]:
    if img.size != (w, h):
        # Falls nicht gleich groß, auf die Größe des ersten Bildes skalieren
        img = img.resize((w, h))
images = [img for img in images]

# Erzeuge leeres Zielbild: 3 Spalten x 2 Reihen
cols, rows = 2, 3
grid_w, grid_h = w * cols, h * rows
grid = Image.new("RGBA", (grid_w, grid_h))

# Positioniere die Bilder: Zeilenweise von links nach rechts, oben nach unten
for idx, img in enumerate(images):
    col = idx % cols
    row = idx // cols
    x = col * w
    y = row * h
    grid.paste(img, (x, y))

# Ergebnis speichern
output_path = "ausgebaute_galerie.png"
grid.save(output_path)
print(f"Ausgabe gespeichert: {output_path}")