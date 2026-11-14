from ultralytics import YOLO
from pathlib import Path
from websockets.asyncio.client import connect

import numpy as np
import json
import asyncio

def detect_and_process(image, depth_file):
    # Class name and BBOX estimation
    model = YOLO("yolo26n.pt")

    output_dir = Path(__file__).resolve().parent / "runs" / "detect"

    results = model(image, device="mps", save=True, project=str(output_dir))

    output = []

    for result in results:
        for box in result.boxes:
            class_id = int(box.cls[0])
            class_name = result.names[class_id]
            confidence = float(box.conf[0])
            bbox = box.xyxy[0].tolist()

            output.append([class_name, bbox])

    file_path = Path(__file__).resolve().parent / depth_file

    # 3D Coordinates estimation using the depth map
    depth = np.loadtxt(file_path, dtype=np.float32)

    objects = []

    height, width = depth.shape

    # Some processing is made to estimate coordinates, but with a coordinate map
    # this won t be necessary
    for index, (class_name, coordinates) in enumerate(output):
        x1, y1, x2, y2 = coordinates

        u = int((x1 + x2) / 2)
        v = int((y1 + y2) / 2)

        Z = float(depth[v, u])

        if not np.isfinite(Z) or Z <= 0:
            continue

        cx = (width - 1) / 2
        cy = (height - 1) / 2

        f = width / 2

        X = (u - cx) * Z / f
        Y = (cy - v) * Z / f    # Unity Y goes up not down

        if class_name == "dining table":
            class_name = "table"

        objects.append({
            "id": f"{class_name}_{index}",
            "className": class_name,
            "position": {"x": X, "y": Y, "z": Z},
            "rotation": {"x": 0, "y": 0, "z": 0},
            "scale": {"x": 1, "y": 1, "z": 1}
        })

    scene = {
        "sceneName": "ScannedRoom",
        "objects": objects
    }

    return scene

scene_a = detect_and_process("test.jpeg", "depth_matrix_test.txt")

async def send_scene(package):
    async with connect("ws://localhost:8765") as connection:
        await connection.send(json.dumps({"role": "detector"}))
        await connection.send(json.dumps(package))


# asyncio.run(send_scene(scene_a))




### Demo using 2 different images mimicking a video

scene_b = detect_and_process("room2.jpeg", "depth_matrix_room2_synthetic.txt")

async def send_scenes(scene_first, scene_second):
    async with connect("ws://localhost:8765") as connection:
        await connection.send(json.dumps({"role": "detector"}))

        for i in range(60):
            scene = scene_first if i % 2 == 0 else scene_second

            await connection.send(json.dumps(scene))
            await asyncio.sleep(1)

asyncio.run(send_scenes(scene_a, scene_b))


