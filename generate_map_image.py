"""
CampusFlow - Chandigarh University Map Generator
=================================================
Generates high-resolution editorial blueprint image assets/campus_map.png
with True-North corrected orientation:
- NH-05 Highway on North (Top)
- Gate 1 facing NH-05 on North
- Central Passage in central concourse
- Block B1 on West (Left)
- Academic Block D1 & C on East (Right)
- Maka Trophy Sports Arena in South-West
- Hostel Complex on South C3 side
"""

import os
import json
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def generate_campus_map():
    json_path = os.path.join(BASE_DIR, "campus_data.json")
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    width, height = 1200, 860
    img = Image.new("RGBA", (width, height), (19, 20, 23, 255))  # Charcoal #131417
    draw = ImageDraw.Draw(img)

    # 1. Architectural grid
    grid_spacing = 40
    for x in range(0, width, grid_spacing):
        draw.line([(x, 0), (x, height)], fill=(30, 32, 38, 140), width=1)
    for y in range(0, height, grid_spacing):
        draw.line([(0, y), (width, y)], fill=(30, 32, 38, 140), width=1)

    margin = 35
    font_small = ImageFont.load_default()

    # 2. External NH-05 Highway Zone (NORTH FRONTAGE AT TOP)
    draw.rounded_rectangle(
        [(margin, 20), (width - margin, 70)],
        radius=6,
        fill=(26, 28, 32, 255),
        outline=(43, 46, 54, 255),
        width=1
    )
    draw.line([(margin + 10, 45), (width - margin - 10, 45)], fill=(88, 94, 109, 200), width=2)
    draw.text((60, 38), "NH-05 CHANDIGARH - LUDHIANA HIGHWAY (NORTH HIGHWAY FRONTAGE - EXTERNAL ROAD)", fill=(140, 147, 160), font=font_small)

    # 3. Campus boundary outline
    draw.rounded_rectangle(
        [(margin, 80), (width - margin, height - 35)],
        radius=14,
        outline=(45, 49, 58, 220),
        width=2
    )

    # 4. Campus Zones (Accurate OpenStreetMap Alignment)
    # Zone 1: Gate 1 (North-East facing NH-05)
    draw.rounded_rectangle([(700, 95), (1130, 240)], radius=10, fill=(36, 32, 27, 120), outline=(58, 52, 44, 160), width=1)
    draw.text((715, 105), "GATE 1 ENTRANCE & ARRIVAL (NH-05)", fill=(185, 165, 140), font=font_small)

    # Zone 2: Fountain Park & Central Core
    draw.rounded_rectangle([(520, 230), (880, 520)], radius=10, fill=(28, 32, 40, 120), outline=(48, 54, 68, 160), width=1)
    draw.text((535, 240), "CENTRAL ACADEMIC CORE (FOUNTAIN PARK & B1)", fill=(130, 150, 180), font=font_small)

    # Zone 3: Block A Complex (East)
    draw.rounded_rectangle([(900, 230), (1150, 520)], radius=10, fill=(29, 30, 40, 120), outline=(50, 52, 68, 160), width=1)
    draw.text((915, 240), "EAST ACADEMIC (A1–A3 COMPLEX)", fill=(140, 145, 175), font=font_small)

    # Zone 4: South Campus (D-Blocks & Star Library)
    draw.rounded_rectangle([(60, 140), (480, 470)], radius=10, fill=(24, 29, 38, 120), outline=(42, 50, 64, 160), width=1)
    draw.text((75, 150), "SOUTH CAMPUS (D-BLOCKS D1–D7 & STAR LIBRARY)", fill=(120, 140, 170), font=font_small)

    # Zone 5: Sports Complex Maka Trophy (South-West)
    draw.rounded_rectangle([(60, 490), (460, 780)], radius=10, fill=(24, 34, 29, 120), outline=(40, 56, 48, 160), width=1)
    draw.text((75, 500), "SPORTS COMPLEX (MAKA TROPHY ARENA)", fill=(110, 150, 128), font=font_small)

    # Zone 6: C-Blocks & Hostels Enclave (South)
    draw.rounded_rectangle([(490, 530), (1150, 810)], radius=10, fill=(32, 30, 38, 120), outline=(52, 48, 62, 160), width=1)
    draw.text((505, 540), "C-BLOCKS & HOSTELS (NC1–NC6 & ZAKIR)", fill=(148, 140, 168), font=font_small)

    # 5. Nodes Lookup
    loc_coords = {}
    loc_meta = {}
    for loc in data["locations"]:
        raw_x = loc["schematic"]["x"]
        raw_y = loc["schematic"]["y"]
        cx = int(40 + raw_x * 1.15)
        cy = int(25 + raw_y * 1.14)
        loc_coords[loc["id"]] = (cx, cy)
        loc_meta[loc["id"]] = loc

    # 6. Draw Internal Paths
    for path in data["paths"]:
        u, v = path["source"], path["target"]
        if u in loc_coords and v in loc_coords:
            p1 = loc_coords[u]
            p2 = loc_coords[v]
            dist = path["distance"]

            draw.line([p1, p2], fill=(52, 56, 68, 255), width=3)

            mx = (p1[0] + p2[0]) // 2
            my = (p1[1] + p2[1]) // 2
            badge_text = f"{dist}m"

            tw = len(badge_text) * 7 + 8
            th = 16
            draw.rounded_rectangle(
                [(mx - tw//2, my - th//2), (mx + tw//2, my + th//2)],
                radius=4,
                fill=(28, 30, 36, 240),
                outline=(50, 54, 64, 255),
                width=1
            )
            draw.text((mx - tw//2 + 5, my - th//2 + 2), badge_text, fill=(180, 185, 195), font=font_small)

    # 7. Draw Nodes
    for loc_id, (cx, cy) in loc_coords.items():
        meta = loc_meta[loc_id]
        code = meta.get("code", "")
        name = meta.get("name", "")
        is_junc = (meta.get("node_type") == "junction")

        if is_junc:
            draw.ellipse([(cx - 3, cy - 3), (cx + 3, cy + 3)], fill=(65, 70, 85, 200), outline=(40, 44, 52, 255), width=1)
            continue

        r_inner = 13
        draw.ellipse([(cx - r_inner, cy - r_inner), (cx + r_inner, cy + r_inner)], fill=(30, 32, 38, 255), outline=(229, 138, 69, 255), width=2)
        draw.ellipse([(cx - 4, cy - 4), (cx + 4, cy + 4)], fill=(255, 255, 255, 255))

        label_text = f"{code}: {name}"
        lw = len(label_text) * 7 + 12
        lh = 18
        ly = cy + 16
        draw.rounded_rectangle(
            [(cx - lw//2, ly), (cx + lw//2, ly + lh)],
            radius=4,
            fill=(24, 26, 32, 240),
            outline=(46, 50, 58, 255),
            width=1
        )
        draw.text((cx - lw//2 + 6, ly + 3), label_text, fill=(230, 235, 245), font=font_small)

    # Compass Rose on North
    draw.text((width - 90, 95), "N ^", fill=(229, 138, 69), font=font_small)

    out_path = os.path.join(BASE_DIR, "assets", "campus_map.png")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    img.save(out_path)
    print(f"{out_path} regenerated with True-North orientation!")

if __name__ == "__main__":
    generate_campus_map()
