# Digital Reconstruction of a Scanned Room using Zed Camera and Yolo Vision

This repository contains the Unity digital room and the Python WebSocket server together. It preserves the history and remote of the existing PI-DIGITAL-TWIN repository.

## Project folders

- `UnityProject/`: the existing Unity project, including its assets, metadata, packages, and settings.
- `Server/`: the Python server, example scene, dependency declaration, lockfile, and manual test client.

## Open in Unity

In Unity Hub, choose **Add project from disk** and select the **UnityProject** folder inside this repository. Open it with **Unity 6000.3.8f1**. The first opening imports assets and rebuilds the local cache.

Open `Assets/Scenes/DigitalRoom.unity`. Keep each asset together with its `.meta` file: those files preserve Unity's references to scenes, scripts, and prefabs.

## Run the Python server

Open `Server/` as the Python project in your editor. With uv installed, run these command from that folder:

```sh
uv run python server.py
```

The project requires Python 3.14 or newer. Its `.venv` is local and excluded from Git.

Start the server, enter Play mode in Unity, then run the script detector.py to send synthetic data to test if the Unity rendering works.
