using UnityEngine;
using System.IO;

public class SceneJsonSpawner : MonoBehaviour
{
    [Header("Prefabs")]
    public GameObject chairPrefab;
    public GameObject tablePrefab;
    public GameObject couchPrefab;

    // Start is called once before the first execution of Update after the MonoBehaviour is created
    void Start()
    {
        string path = Path.Combine(Application.streamingAssetsPath, "scene.json");

        string json = File.ReadAllText(path);

        SceneData scene = JsonUtility.FromJson<SceneData>(json);

        if (scene == null || scene.objects == null)
        {
            Debug.LogError("Invalid Scene JSON!");
            return;
        }

        foreach (ObjectData item in scene.objects)
        {
            GameObject prefab = GetPrefab(item.className);

            if (prefab == null)
            {
                Debug.LogWarning("Unknown prefab" + item.className);
                continue;
            }

            GameObject obj = Instantiate(prefab, item.position, Quaternion.Euler(item.rotation));

            obj.name = item.id;

            obj.transform.localScale = Vector3.Scale(prefab.transform.localScale, item.scale);
        }
    }

    GameObject GetPrefab(string className)
    {
        switch(className)
        {
            case "chair":
                return chairPrefab;

            case "table":
                return tablePrefab;

            case "couch":
                return couchPrefab;

            default:
                return null;
        }
    }
}
