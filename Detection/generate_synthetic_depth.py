"""Hand-authored depth fixture for room2.jpeg, NOT camera measurements.

Distances and coarse polygons are chosen only for pipeline testing.
Output: space-separated forward Z depths in metres, indexed [row, column].
No detector/server execution or changes are needed to generate this fixture.
"""
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw


def main():
    folder = Path(__file__).resolve().parent
    with Image.open(folder / "room2.jpeg") as image:
        width, height = image.size
    if (width, height) != (2000, 1500):
        raise ValueError("Polygons were authored for the 2000 x 1500 room2.jpeg")

    yy, xx = np.indices((height, width), dtype=np.float32)
    # Back wall at 5 m; a deliberately simple floor depth ramp toward camera.
    depth = np.broadcast_to(
        np.interp(np.arange(height), [0, 440, 650, 1000, 1499],
                  [5.0, 5.0, 3.5, 2.1, 0.9])[:, None],
        (height, width),
    ).astype(np.float32).copy()

    def surface(points, far, near=None):
        # Coarse synthetic surfaces, not segmentation or learned depth.
        mask_image = Image.new("L", (width, height))
        ImageDraw.Draw(mask_image).polygon(points, fill=255)
        mask = np.asarray(mask_image) > 0
        top, bottom = min(y for _, y in points), max(y for _, y in points)
        t = np.clip((yy - top) / max(1, bottom - top), 0, 1)
        values = far + t * ((far if near is None else near) - far)
        depth[mask] = np.minimum(depth[mask], values[mask])

    # Cabinet, rear desks, monitors and standing person.
    surface([(1390,180),(1675,155),(1615,630),(1330,635)], 4.2)
    surface([(0,440),(1220,440),(1220,510),(0,670)], 4.3, 3.4)
    surface([(500,366),(607,366),(607,455),(500,455)], 4.0)
    surface([(788,366),(912,367),(914,438),(790,438)], 4.0)
    surface([(983,214),(1040,210),(1085,310),(1086,475),
             (1058,651),(973,650),(949,408),(950,316)], 3.7, 3.5)
    # Rear chairs and seated person on the left.
    surface([(590,435),(718,435),(733,607),(686,683),(563,677)], 3.5, 3.2)
    surface([(800,429),(966,430),(947,610),(877,681),(780,648)], 3.4, 3.1)
    surface([(1105,425),(1211,427),(1200,566),(1155,640),(1082,607)], 3.5, 3.2)
    surface([(1000,518),(1125,508),(1175,530),(1175,650),(991,653)], 2.9)
    surface([(200,350),(283,344),(365,439),(371,539),(227,560),(157,496)], 3.3)
    surface([(243,480),(388,460),(448,659),(393,779),(201,704)], 2.9, 2.5)
    surface([(115,552),(211,541),(202,701),(257,808),(151,928),(36,814)], 2.6, 2.0)
    surface([(0,575),(63,563),(70,775),(110,904),(0,1030)], 2.3, 1.6)
    # Foreground table and its base.
    surface([(819,651),(1470,623),(1999,808),(1830,955),(920,975)], 2.8, 1.7)
    surface([(1014,940),(1220,934),(1243,1192),(1020,1206)], 1.7)
    # Box and laptop above the table.
    surface([(862,636),(937,699),(1157,680),(1229,647),(1281,687),
             (1215,738),(1231,880),(951,907),(923,766)], 2.35, 1.9)
    surface([(1394,634),(1583,620),(1601,770),(1480,830),(1384,757)], 2.15, 1.9)
    # Central chair, foreground seated person and right chair.
    surface([(622,602),(729,575),(765,601),(810,775),(774,833),
             (867,842),(928,966),(726,997),(670,936),(658,793)], 2.25, 1.65)
    surface([(1669,501),(1762,488),(1839,527),(1827,652),(1914,698),
             (1970,813),(1801,1020),(1517,1052),(1409,924),(1400,821),
             (1470,754),(1585,728),(1668,654),(1640,573)], 1.9, 1.45)
    surface([(1617,862),(1999,812),(1999,1097),(1896,1239),
             (1679,1284),(1490,1198),(1427,1085),(1460,1008)], 1.5, 1.0)
    surface([(0,944),(88,1042),(68,1152),(366,1159),(370,1208),
             (110,1270),(0,1241)], 0.85)
    surface([(0,1477),(227,1426),(443,1436),(459,1499),(0,1499)], 0.65)

    target = folder / "depth_matrix_room2_synthetic.txt"
    np.savetxt(target, depth, fmt="%.3f", header=(
        f"SYNTHETIC Depth Matrix (forward Z in meters; NOT measured) - "
        f"Shape: {height} rows x {width} cols"))
    loaded = np.loadtxt(target, dtype=np.float32)
    assert loaded.shape == (height, width)
    assert np.isfinite(loaded).all() and (loaded > 0).all()
    print(f"Saved {target}")
    print(f"Verified: {loaded.shape}, range {loaded.min():.3f}–{loaded.max():.3f} m")


if __name__ == "__main__":
    main()
