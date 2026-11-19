# Digital reconstruction of a room in Unity

Unity reconstructs a room by placing 3D objects at positions reported by a detector. A Python WebSocket server forwards the detections to Unity as JSON.

## What’s in this repository?

- `UnityProject/` contains the `DigitalRoom` scene, furniture prefabs, scripts, packages and project settings for **Unity 6000.3.8f1**.
- `Server/server.py` connects the detector to Unity at `ws://localhost:8765`.
- `Detection/detector.py` is a demo for testing the server and checking that Unity renders the detected objects correctly. It uses YOLO with two included images and their depth maps, so you can run it without a camera.

The live detector uses a **ZED camera** and lives in [ComputerVision-Project](https://github.com/OuterSpace989/ComputerVision-Project).

## Run the demo on your laptop

Install Git, [uv](https://docs.astral.sh/uv/getting-started/installation/) and Unity Hub. In Unity Hub, install Editor **6000.3.8f1**.

### 1. Clone the project and start the server

```sh
git clone https://github.com/TuluiEduardAndrei/CameraScanning--VisionAI--PhysicalRoom--DigitalReconstruction.git
cd CameraScanning--VisionAI--PhysicalRoom--DigitalReconstruction
uv sync --locked --python 3.14
uv run python Server/server.py
```

Leave this terminal running. It should print `Server running!`.

### 2. Open the scene in Unity

In Unity Hub, choose **Add project from disk** and select the cloned repository’s **UnityProject** folder. On first open, Unity imports the assets and rebuilds its local cache. Open `Assets/Scenes/DigitalRoom.unity` and press **Play**. Wait for the server terminal to print `Unity connected!`.

### 3. Send the demo scenes

The demo defaults to Apple’s Metal backend (`device="mps"`). On a laptop without MPS support, change this argument to `device="cpu"` in `Detection/detector.py` before running it.

Open a second terminal in the cloned repository and run the demo from the folder containing the images and model weights.

```sh
cd Detection
uv run python detector.py
```

After processing both images, the demo alternates between their detections once per second for 60 updates. The server prints `Scene sent to Unity!` as it forwards each update. In Unity’s **Game** view, you should see furniture appear in the room.
