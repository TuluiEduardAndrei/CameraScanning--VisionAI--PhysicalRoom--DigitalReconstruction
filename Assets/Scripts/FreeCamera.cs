
using UnityEngine;
using UnityEngine.InputSystem;

public class FreeCamera : MonoBehaviour
{
    public float speed = 5f;
    public float mouseSensitivity = 0.15f;
    public float sprintMultiplier = 3f;

    private float yaw;      // horizontal rotation
    private float pitch;    // vertical rotation

    private void Start()
    {
        yaw = transform.eulerAngles.y;
        pitch = transform.eulerAngles.x;

        if (pitch > 180f)
            pitch -= 360f;
    }

    private void Update()
    {
        var keyboard = Keyboard.current;
        var mouse = Mouse.current;

        if (keyboard == null || mouse == null)
            return;

        // Mouse look
        if (mouse.rightButton.isPressed)
        {
            Cursor.lockState = CursorLockMode.Locked;

            Vector2 delta = mouse.delta.ReadValue();

            yaw += delta.x * mouseSensitivity;
            pitch -= delta.y * mouseSensitivity;
            pitch = Mathf.Clamp(pitch, -89f, 89f);

            transform.rotation = Quaternion.Euler(pitch, yaw, 0f);
        }
        else
        {
            Cursor.lockState = CursorLockMode.None;
        }

        // Movement
        Vector3 direction = Vector3.zero;

        if (keyboard.wKey.isPressed) direction += transform.forward;
        if (keyboard.sKey.isPressed) direction -= transform.forward;
        if (keyboard.dKey.isPressed) direction += transform.right;
        if (keyboard.aKey.isPressed) direction -= transform.right;

        if (keyboard.eKey.isPressed) direction += Vector3.up;
        if (keyboard.qKey.isPressed) direction -= Vector3.up;

        float currentSpeed = speed;

        if (keyboard.leftShiftKey.isPressed)
            currentSpeed *= sprintMultiplier;

        transform.position +=
            direction.normalized * currentSpeed * Time.deltaTime;
    }

    private void OnDisable()
    {
        Cursor.lockState = CursorLockMode.None;
    }
}
