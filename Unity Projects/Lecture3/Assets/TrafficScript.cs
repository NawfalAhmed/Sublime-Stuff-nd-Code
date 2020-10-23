using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TrafficScript : MonoBehaviour
{
	Rigidbody body;
	Vector3 inputDirection;
	bool notbackward = true;
	void Start() {
		if (transform.rotation.eulerAngles.y == 180) {
			inputDirection = new Vector3(0,0,-8);
			notbackward = false;
		}
		else
			inputDirection = new Vector3(0,0,8);
		body = GetComponent<Rigidbody>();
	}
	void Update() {
		Vector3 pos = transform.position;
		if(pos.z >= -181 && pos.z <= -179 && notbackward) {
			pos.z -=700;
			transform.position = pos;
		}
		if(pos.z >= -891 && pos.z <= -889) {
			pos.z =800;
			transform.position = pos;
		}
	}
	void FixedUpdate() {
		if (body.velocity.z > -20 && body.velocity.z < 20)
			body.AddForce(inputDirection,ForceMode.Acceleration);
	}
}
