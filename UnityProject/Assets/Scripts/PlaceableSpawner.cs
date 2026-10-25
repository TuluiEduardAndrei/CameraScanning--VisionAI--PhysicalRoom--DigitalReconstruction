using UnityEngine;
using UnityEngine.InputSystem;
using System.IO;

public class PlaceableSpawner : MonoBehaviour
{
    [Header("Prefab to Spawn")]
    public GameObject prefabToSpawn;

    [Header("Spawn Settings")]
    public Vector3 position = new Vector3(0f, 0f, 0f);
    public Quaternion rotation = Quaternion.identity;

    public void Spawn()
    {
        if (prefabToSpawn == null)
        {
            Debug.LogWarning("No prefab assigned to spawn!");
            return;
        }

        string path = Path.Combine(Application.streamingAssetsPath, "scene.json");

        if (!File.Exists(path))
        {
            Debug.LogError("JSON file not found: " + path);
            return;
        }

        string json = File.ReadAllText(path);

        ObjectData data = JsonUtility.FromJson<ObjectData>(json);

        if (data == null)
        {
            Debug.LogError("Invalid JSON");
            return;
        }

        GameObject spawnedObject = Instantiate(prefabToSpawn, data.position, Quaternion.Euler(data.rotation));
    }
    private void Update()
    {
        if (Keyboard.current != null &&
            Keyboard.current.tKey.wasPressedThisFrame)
        {
            Spawn();
        }
    }
}
