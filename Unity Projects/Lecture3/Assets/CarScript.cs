using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CarScript : MonoBehaviour
{
	Rigidbody body;
	Vector3 inputDirection;
	bool isInAir;
	bool space;
	float inputvertical;
	float timer;

	[Range(5f,11f)]
	public float speedmultiplier = 8f;

	void Start() {
		isInAir = false;
		space = false;
		timer = 0f;
		body  = GetComponent<Rigidbody>();
		inputDirection.y = 0;
	}

	void Update() {
		inputDirection.x= Input.GetAxis("Horizontal")*2	*speedmultiplier;
		inputvertical = Input.GetAxis("Vertical");
		Vector3 pos = transform.position;
		if(pos.z >= -181 && pos.z <= -179) {
			pos.z -=700;
			transform.position = pos;
		}
		if(Input.GetKeyDown(KeyCode.Space))
			space = true;
	}

	void FixedUpdate() {
		print(body.velocity);
		if (body.velocity.y == 0)
			isInAir = false;
		else
			isInAir = true;
		if (!isInAir) {
			if (inputvertical <-0.5) {
				if (timer<1)
					timer+=Time.deltaTime;
				else
					inputDirection.z = inputvertical*speedmultiplier;
					if (body.velocity.z > -10)
						body.AddForce(inputDirection,ForceMode.Acceleration);
			}
			else {
				timer = 0;
				inputDirection.z = inputvertical*speedmultiplier;
				if (body.velocity.z < 60)
					body.AddForce(inputDirection,ForceMode.Acceleration);
				if(space) {
					space = false;
					body.AddForce(Vector3.up*8.8f,ForceMode.VelocityChange);
				}
			}
		}
	}
}
