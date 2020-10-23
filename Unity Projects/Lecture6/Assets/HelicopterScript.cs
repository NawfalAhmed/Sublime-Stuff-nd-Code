using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class HelicopterScript : MonoBehaviour
{
	Rigidbody body;
	Vector3 inputDirection;
	bool isInAir;
	bool space;
	float inputvertical;
	float inputvertical2;
	float inputhorizontal;
	float inputhorizontal2;
	float timer;

	[Range(5f,100f)]
	public float speedmultiplier = 8f;

	void Start() {
		isInAir = true;
		space = false;
		timer = 0f;
		body  = GetComponent<Rigidbody>();
		inputDirection.x= 0;
		inputDirection.z= 0;
	}

	void Update() {
		inputvertical = Input.GetAxis("Vertical");
		inputvertical2 = Input.GetAxis("Vertical2");
		inputhorizontal = Input.GetAxis("Horizontal");
		inputhorizontal2 = Input.GetAxis("Horizontal2");
	}

	void FixedUpdate() {
		if (isInAir) {
			inputDirection.y = inputvertical*speedmultiplier;
			print(body.velocity);
			if (body.velocity.y < 60 && body.velocity.y > -30)
				body.AddRelativeForce(inputDirection,ForceMode.Acceleration);
			transform.Rotate(inputvertical2,0,0);
			transform.Rotate(0,inputhorizontal*0.4f,0);
			transform.Rotate(0,0,inputhorizontal2);
		}
	}
}
