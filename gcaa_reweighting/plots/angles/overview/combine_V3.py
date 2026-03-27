import sys
from PIL import Image, ImageDraw, ImageFont

residues = ["C5", "G6", "C7", "A8", "A9", "G10"]
angles = [
    "alpha_C4p-P",
    "beta_C4Pb_1H5P_2H5P",
    "chi_C1-CC",
    "delta_C1-C2_C3-C4",
    "delta_H1H2_H2H3_H3H4",
    "epsilon_C4Pe_H3P",
    "gamma_1H5H4_2H5H4",
    "zeta_C3p-P-plus_C4p-P-plus"
]

# Buchstaben A bis F
labels = ['A', 'B', 'C', 'D', 'E', 'F']

# Schriftart laden (Fallback auf Standard falls kein TrueType verfügbar)
try:
    font = ImageFont.truetype("arial.ttf", size=24)
except IOError:
    font = ImageFont.load_default()

for angle in angles:
    input_paths = [f"plots/angles/{res}_{angle}.png" for res in residues]

    if len(input_paths) != 6:
        print("Fehler: 6 Bildpfade müssen angegeben werden.")
        sys.exit(1)

    # Bilder öffnen
    images = [Image.open(p) for p in input_paths]

    # Größe normalisieren
    w, h = images[0].size
    normalized_images = []
    for img in images:
        if img.size != (w, h):
            img = img.resize((w, h))
        
        # Bild beschriften
        idx = len(normalized_images)
        draw = ImageDraw.Draw(img)

        # Dynamische Schriftgröße basierend auf Bildhöhe
        fontsize = int(h * 0.05)
        try:
            font = ImageFont.truetype("arial.ttf", fontsize)
        except IOError:
            font = ImageFont.load_default()

        text = labels[idx]
        text_position = (10, 10)  # oben links mit kleinem Abstand

        # Weißer Schatten für bessere Lesbarkeit
        shadow_offset = 1
        draw.text((text_position[0] + shadow_offset, text_position[1] + shadow_offset), text, font=font, fill="white")
        draw.text(text_position, text, font=font, fill="black")

        normalized_images.append(img)

    # Grid erstellen (2 Spalten x 3 Zeilen)
    cols, rows = 2, 3
    grid_w, grid_h = w * cols, h * rows
    grid = Image.new("RGBA", (grid_w, grid_h))

    # Bilder platzieren
    for idx, img in enumerate(normalized_images):
        col = idx % cols
        row = idx // cols
        x = col * w
        y = row * h
        grid.paste(img, (x, y))

    # Ergebnis speichern
    output_path = f"plots/angles/overview/{angle}_overview_V3.png"
    grid.save(output_path)
    print(f"Ausgabe gespeichert: {output_path}")
