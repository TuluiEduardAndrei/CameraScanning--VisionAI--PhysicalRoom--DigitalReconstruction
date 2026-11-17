using UnityEngine;
using System.Collections.Generic;

public class SceneJsonSpawner : MonoBehaviour
{
    public GameObject floor;

    [Header("Prefabs")]
    public GameObject chairPrefab;
    public GameObject tablePrefab;
    public GameObject couchPrefab;
    public GameObject tvPrefab;
    public GameObject laptopPrefab;

    public List<GameObject> spawnedObjects = new List<GameObject>();
    public List<TrackedObject> objectsData = new List<TrackedObject>();

    public void SpawnFromJson(string json)
    {
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

            TrackedObject newObject = new TrackedObject(item);
            newObject.observationTime = Time.time;

            bool ok = true;
            foreach (TrackedObject existingObject in objectsData)
            {
                float distance = Vector3.Distance(newObject.extractedPosition, existingObject.extractedPosition);

                if (distance < 0.15f && newObject.className == existingObject.className && existingObject.rendered == true)
                {
                    newObject.rendered = false;
                    newObject.similarRenderedObjectId = existingObject.id;
                    ok = false;
                    break;
                }
            }

            if (ok == true)
            {
                newObject.rendered = true;
                newObject.similarRenderedObjectId = newObject.id;

                GameObject obj = Instantiate(prefab, newObject.renderedPosition, Quaternion.Euler(newObject.renderedRotation));
                newObject.renderedTime = Time.time;
                obj.name = newObject.id;
                obj.transform.localScale = Vector3.Scale(prefab.transform.localScale, newObject.scale);

                // Align the chairs, couches, tables with the floor. Do not think that we will meet flying chairs or tables.
                if (newObject.className == "chair" || newObject.className == "couch" || newObject.className == "table")
                {
                    Renderer objectRenderer = obj.GetComponentInChildren<Renderer>();

                    if (objectRenderer != null)
                    {
                        float floorY = floor.transform.position.y;
                        float offset = floorY - objectRenderer.bounds.min.y;
                        obj.transform.position += Vector3.up * offset;
                    }

                    newObject.renderedPosition = obj.transform.position;
                    newObject.renderedRotation = obj.transform.eulerAngles;
                }

                spawnedObjects.Add(obj);
            }

            objectsData.Add(newObject);
        }

        AlignObjectsWithTables();
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
            case "tv":
                return tvPrefab;
            case "laptop":
                return laptopPrefab;
            default:
                return null;
        }
    }

    public void AlignObjectsWithTables()
    {
        foreach (TrackedObject objectData in objectsData)
        {
            if (!objectData.rendered || (objectData.className != "laptop" && objectData.className != "tv")) continue;

            GameObject obj = spawnedObjects.Find(candidate => candidate != null && candidate.name == objectData.id);

            if (obj == null) continue;

            Renderer objectRenderer = obj.GetComponentInChildren<Renderer>();

            if (objectRenderer == null) continue;

            foreach (TrackedObject tableData in objectsData)
            {
                if (tableData.className != "table" || !tableData.rendered) continue;

                GameObject tableObj = spawnedObjects.Find(candidate => candidate != null && candidate.name == tableData.id);

                if (tableObj == null) continue;

                Renderer tableRenderer = tableObj.GetComponentInChildren<Renderer>();

                if (tableRenderer == null) continue;

                Bounds tableBounds = tableRenderer.bounds;
                Vector3 objectCenter = objectRenderer.bounds.center;

                bool insideX = objectCenter.x >= tableBounds.min.x && objectCenter.x <= tableBounds.max.x;

                bool insideZ = objectCenter.z >= tableBounds.min.z && objectCenter.z <= tableBounds.max.z;

                if (insideX && insideZ)
                {
                    float offset = tableBounds.max.y - objectRenderer.bounds.min.y;

                    obj.transform.position += Vector3.up * offset;
                    objectData.renderedPosition = obj.transform.position;

                    break;
                }
            }
        }
    }
}
