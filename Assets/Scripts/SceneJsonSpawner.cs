using UnityEngine;
using System.Collections.Generic;

public class SceneJsonSpawner : MonoBehaviour
{
    [Header("Prefabs")]
    public GameObject chairPrefab;
    public GameObject tablePrefab;
    public GameObject couchPrefab;

    private List<GameObject> spawnedObjects = new List<GameObject>();

    public void SpawnFromJson(string json)
    {
        foreach (GameObject obj in spawnedObjects)
        {
            Destroy(obj);
        }
        spawnedObjects.Clear();

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

            spawnedObjects.Add(obj);
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
