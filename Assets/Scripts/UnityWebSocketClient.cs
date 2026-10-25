using UnityEngine;
using NativeWebSocket;
using System.Text;

public class UnityWebSocketClient : MonoBehaviour
{
    private WebSocket connection;

    public SceneJsonSpawner spawner;

    // Uses events that trigger at a specific time after the connection has been established.
    // Python uses " async for message in connection " to receive the message, but Unity uses " connection.OnMessage ".
    async void Start()
    {
        Application.runInBackground = true;

        connection = new WebSocket("ws://localhost:8765");

        connection.OnOpen += () =>
        {
            Debug.Log("Connected to Python!");
        };

        connection.OnMessage += (bytes) =>
        {
            string json = Encoding.UTF8.GetString(bytes);
            Debug.Log("Received JSON: " + json);
            spawner.SpawnFromJson(json);
        };

        connection.OnClose += (code) =>
        {
            Debug.Log("Disconnected: " + code);
        };

        await connection.Connect();
    }

    private async void OnApplicationQuit()
    {
        if (connection != null)
        {
            await connection.Close();
        }
    }
}
