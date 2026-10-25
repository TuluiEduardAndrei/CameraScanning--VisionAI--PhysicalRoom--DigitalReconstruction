# Digital Reconstruction of a Scanned Room using Zed Camera and Yolo Vision

This repository contains the Unity digital room and the Python WebSocket server together. It preserves the history and remote of the existing PI-DIGITAL-TWIN repository.

## Project folders

- `UnityProject/`: the existing Unity project, including its assets, metadata, packages, and settings.
- `Server/`: the Python server, example scene, dependency declaration, lockfile, and manual test client.
- `tests/`: automated structure, migration, and server communication checks.

## Open in Unity

In Unity Hub, choose **Add project from disk** and select the **UnityProject** folder inside this repository. Open it with **Unity 6000.3.8f1**. The first opening imports assets and rebuilds the local cache.

Open `Assets/Scenes/DigitalRoom.unity`. Keep each asset together with its `.meta` file: those files preserve Unity's references to scenes, scripts, and prefabs.

## Run the Python server

Open `Server/` as the Python project in your editor. With uv installed, run these commands from that folder:

```sh
uv sync --locked
uv run --locked python server.py
```

The project requires Python 3.14 or newer. Its `.venv` is local and excluded from Git. Run the server from `Server/`, because the existing code reads `scene.json` relative to the current directory.

Start the server, enter Play mode in Unity, wait for the connection, then press Enter in the server terminal to send the example scene. The current connection is `ws://localhost:8765`. To try another scene, update `Server/scene.json` and press Enter again. The supplied example contains one table, two chairs, and one couch.

`test_client.py` is an alternative manual client for testing the server without Unity. The server currently supports one client, so run that client separately from Unity.

## GitHub Desktop

Choose **File > Add Local Repository** and select this repository's outer folder (the folder containing this README), rather than `UnityProject/`. Review the reorganization and new server files there. The remote remains `TuluiEduardAndrei/PI-DIGITAL-TWIN`.

The original Desktop project folders are retained as backups. Once you switch to this combined repository, make future edits here to avoid keeping divergent copies. The folder reorganization is local until committed and pushed.

## Verification

From the repository root:

```sh
Server/.venv/bin/python -B -m unittest discover -s tests -v
git fsck --full
git diff --check
```

The communication test launches a temporary server on an available local port, sends the bundled scene, checks that the JSON arrives unchanged, and shuts down the process. It does not use the normal Unity port.

To additionally compare the migration with the originals, set `ORIGINAL_UNITY_PROJECT` and `ORIGINAL_SERVER_PROJECT` to their original absolute directory paths before running the tests. These comparisons skip when those variables are unset, so the repository also works on another computer.

Local verification reports are stored under `verification/` and excluded from Git.
