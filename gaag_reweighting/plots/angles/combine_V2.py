import sys 
from PIL import Image

residues = ["C5","G6","A7","A8","G9","G10"]
angles = ["alpha_C4p-P",
          "beta_C4Pb_1H5P_2H5P",
          "chi_C1-CC",
          "delta_C1-C2_C3-C4",
          "delta_H1H2_H2H3_H3H4",
          "epsilon_C4Pe_H3P",
          "gamma_1H5H4_2H5H4",
          "zeta_C3p-P-plus_C4p-P-plus"
          ]

for angle in angles:
    input_paths = []
    for res in residues:
        input_paths.append(f"plots/angles/{res}_{angle}.png")

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
    output_path = f"{angle}_overview.png"
    grid.save(output_path)
    print(f"Ausgabe gespeichert: {output_path}")