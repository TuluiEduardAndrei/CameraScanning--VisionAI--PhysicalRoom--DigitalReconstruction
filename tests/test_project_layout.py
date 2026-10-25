import ast
import asyncio
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest


def repository_root():
    return Path(__file__).resolve().parents[1]


def original_directory(variable):
    value = os.environ.get(variable)
    if not value:
        raise unittest.SkipTest(f"Set {variable} to verify the original copy")
    directory = Path(value).resolve(strict=True)
    if not directory.is_dir():
        raise ValueError(f"{variable} must identify a directory")
    return directory


class ProjectLayoutTests(unittest.TestCase):
    def test_unity_project_can_be_identified(self):
        unity = repository_root() / "UnityProject"
        for name in ("Assets", "Packages", "ProjectSettings"):
            self.assertTrue((unity / name).is_dir(), name)
        self.assertIn("6000.3.8f1", (unity / "ProjectSettings/ProjectVersion.txt").read_text())
        manifest = json.loads((unity / "Packages/manifest.json").read_text())
        self.assertIsInstance(manifest["dependencies"], dict)
        self.assertTrue((unity / "Assets/Scenes/DigitalRoom.unity").is_file())

    def test_one_repository_contains_both_projects(self):
        root = repository_root()
        for folder in (root / "UnityProject", root / "Server"):
            top = subprocess.check_output(["git", "-C", str(folder), "rev-parse", "--show-toplevel"], text=True)
            self.assertEqual(Path(top.strip()).resolve(), root)

    def test_ignore_rules_exclude_caches_but_keep_source(self):
        ignored = ["UnityProject/Library/cache", "UnityProject/Temp/cache", "UnityProject/Logs/log", "UnityProject/UserSettings/settings", "Server/.venv/bin/python", "Server/__pycache__/server.pyc", "Server/.env", "verification/log.txt"]
        visible = ["UnityProject/Assets/Scenes/DigitalRoom.unity", "UnityProject/Assets/Scenes/DigitalRoom.unity.meta", "Server/server.py", "Server/scene.json", "Server/uv.lock"]
        for path in ignored + visible:
            result = subprocess.run(["git", "check-ignore", "--no-index", "--quiet", path], cwd=repository_root())
            self.assertEqual(result.returncode, 0 if path in ignored else 1, path)

    def test_python_sources_parse(self):
        for path in (repository_root() / "Server").glob("*.py"):
            ast.parse(path.read_text(), filename=str(path))

    def test_scene_matches_unity_data_shape(self):
        scene = json.loads((repository_root() / "Server/scene.json").read_text())
        self.assertIsInstance(scene["sceneName"], str)
        self.assertIsInstance(scene["objects"], list)
        identifiers = set()
        for item in scene["objects"]:
            self.assertIsInstance(item["id"], str)
            self.assertNotIn(item["id"], identifiers)
            identifiers.add(item["id"])
            self.assertIn(item["className"], ("chair", "table", "couch"))
            for vector in ("position", "rotation", "scale"):
                self.assertEqual(set(item[vector]), {"x", "y", "z"})
                for value in item[vector].values():
                    self.assertIn(type(value), (int, float))

    def test_unity_source_and_metadata_match_original(self):
        source = original_directory("ORIGINAL_UNITY_PROJECT")
        target = repository_root() / "UnityProject"
        for folder in ("Assets", "Packages", "ProjectSettings"):
            originals = {p.relative_to(source) for p in (source / folder).rglob("*") if p.is_file() and p.name != ".DS_Store"}
            copies = {p.relative_to(target) for p in (target / folder).rglob("*") if p.is_file() and p.name != ".DS_Store"}
            self.assertEqual(originals, copies, folder)
            for relative in sorted(originals):
                self.assertEqual((source / relative).read_bytes(), (target / relative).read_bytes(), str(relative))
        self.assertEqual((source / ".gitignore").read_bytes(), (target / ".gitignore").read_bytes())

    def test_server_files_match_original(self):
        source = original_directory("ORIGINAL_SERVER_PROJECT")
        for name in ("server.py", "test_client.py", "scene.json", "pyproject.toml", "uv.lock"):
            self.assertEqual((source / name).read_bytes(), (repository_root() / "Server" / name).read_bytes(), name)

    def test_git_history_and_remote_match_original(self):
        source = original_directory("ORIGINAL_UNITY_PROJECT")
        for arguments in (["rev-parse", "HEAD"], ["remote", "get-url", "origin"]):
            original = subprocess.check_output(["git", "-C", str(source), *arguments])
            copied = subprocess.check_output(["git", "-C", str(repository_root()), *arguments])
            self.assertEqual(original, copied)


class ServerCommunicationTests(unittest.IsolatedAsyncioTestCase):
    async def test_scene_delivery_over_websocket(self):
        if importlib.util.find_spec("websockets") is None:
            self.skipTest("Run with Server/.venv/bin/python after uv sync --locked")
        from websockets.asyncio.client import connect

        # An ephemeral port keeps verification separate from the user's Unity session.
        bootstrap = """
import server
from contextlib import asynccontextmanager
actual_serve = server.serve
@asynccontextmanager
async def isolated_serve(handler, host, port):
    async with actual_serve(handler, '127.0.0.1', 0) as listener:
        print('PORT=' + str(listener.sockets[0].getsockname()[1]), flush=True)
        yield listener
server.serve = isolated_serve
server.asyncio.run(server.main())
"""
        process = await asyncio.create_subprocess_exec(sys.executable, "-u", "-c", bootstrap, cwd=repository_root() / "Server", stdin=asyncio.subprocess.PIPE, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        try:
            line = await asyncio.wait_for(process.stdout.readline(), 10)
            self.assertTrue(line.startswith(b"PORT="), line)
            port = int(line.split(b"=", 1)[1])
            async with connect(f"ws://127.0.0.1:{port}", open_timeout=5, close_timeout=2) as client:
                for _ in range(3):
                    ready = await asyncio.wait_for(process.stdout.readline(), 5)
                    if b"Unity connected!" in ready:
                        break
                self.assertIn(b"Unity connected!", ready)
                process.stdin.write(b"\n")
                await process.stdin.drain()
                received = json.loads(await asyncio.wait_for(client.recv(), 5))
                expected = json.loads((repository_root() / "Server/scene.json").read_text())
                self.assertEqual(received, expected)
        finally:
            if process.returncode is None:
                process.terminate()
            try:
                await asyncio.wait_for(process.communicate(), 5)
            except asyncio.TimeoutError:
                process.kill()
                await process.communicate()


if __name__ == "__main__":
    unittest.main()
