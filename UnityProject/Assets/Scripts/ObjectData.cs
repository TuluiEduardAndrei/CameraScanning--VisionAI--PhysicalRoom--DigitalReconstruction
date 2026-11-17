using System;
using UnityEngine;

[Serializable]
public class ObjectData
{
    public string id;
    public string className;

    public Vector3 extractedPosition;
    public Vector3 extractedRotation;

    public Vector3 scale;
}

[Serializable]
public class SceneData
{
    public string sceneName;
    public ObjectData[] objects;
}

[System.Serializable]
public class TrackedObject : ObjectData
{
    public bool rendered;
    public string similarRenderedObjectId;

    public float renderedTime;
    public float deletedTime;
    public float observationTime;

    public Vector3 renderedPosition;
    public Vector3 renderedRotation;

    public TrackedObject(ObjectData data)
    {
        id = data.id;
        className = data.className;
        if (data.scale == Vector3.zero)
        {
            scale = Vector3.one;
        }
        else
        {
            scale = data.scale;
        }

        extractedPosition = data.extractedPosition;
        extractedRotation = data.extractedRotation;

        renderedPosition = data.extractedPosition;
        renderedRotation = data.extractedRotation;

        rendered = false;
        similarRenderedObjectId = null;

        renderedTime = -1f;
        observationTime = -1f;
    }
}
