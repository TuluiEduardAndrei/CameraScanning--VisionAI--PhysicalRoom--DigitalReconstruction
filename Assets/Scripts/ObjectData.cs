
using System;
using UnityEngine;

[Serializable]
public class ObjectData
{
    public string id;
    public string className;
    public Vector3 position;
    public Vector3 rotation;
    public Vector3 scale;
}

[Serializable]
public class SceneData
{
    public string sceneName;
    public ObjectData[] objects;
}
