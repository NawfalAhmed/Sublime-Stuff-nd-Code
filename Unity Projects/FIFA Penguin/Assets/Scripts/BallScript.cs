using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BallScript : MonoBehaviour
{
	Camera main;
	Rigidbody body;
	Vector3 Velocity;
	Vector3 inputDirection;
	Vector3 actualDirection;
	bool isPlane = false;
	[Range(0f,8f)]
	public float speed = 1f;
	void Start() {
		main = Camera.main;
		body  = GetComponent<Rigidbody>();
		inputDirection.y = 0;
	}
	void Update() {
		if (isPlane) {
			inputDirection.x = Input.GetAxis("Horizontal")*speed;
			inputDirection.z = Input.GetAxis("Vertical")*speed;
			actualDirection = main.transform.TransformDirection(inputDirection);
			body.AddForce(actualDirection*2,ForceMode.Acceleration);
			if(Input.GetKeyDown(KeyCode.Space)) {
				isPlane = false;
				body.AddForce(Vector3.up*5,ForceMode.VelocityChange);
			}
		}
	}

	public void OnCollisionEnter(Collision other) {
		if(other.gameObject.tag != "Boundary")
			isPlane = true;
	}
	public void OnCollisionExit(Collision other) {
		isPlane = false;
	}
}






