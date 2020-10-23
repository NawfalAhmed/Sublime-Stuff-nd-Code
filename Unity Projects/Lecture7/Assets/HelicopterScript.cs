using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;
public class HelicopterScript : MonoBehaviour
{
	[Range(0.4f,1f)]
	public float firerate = 0.6f;

	GameObject newmissile;
	GameObject missile;
	float nextFire = 0.2f;
	float fireTime = 0f;
	// Vector3 customPos;
	// Vector3 customRot;
	float InputVertical;
	float InputVertical2;
	float InputHorizontal;
	float InputHorizontal2;
	void Start() {
		missile = Resources.Load("Missile") as GameObject;

		// customPos = new Vector3(0f,0f,0f);
		// customRot = new Vector3(0f,0f,0f);
	}
	// Update is called once per frame
	void Update()
	{
		InputVertical = Input.GetAxis("Vertical");
		InputVertical2 = Input.GetAxis("Vertical2");
		InputHorizontal = Input.GetAxis("Horizontal");
		InputHorizontal2 = Input.GetAxis("Horizontal2");
		if (Input.GetKey(KeyCode.LeftControl)){
			transform.Rotate(0.25f,0, 0);
		}
		if (Input.GetKey(KeyCode.LeftShift)){
			transform.Rotate(-0.25f,0, 0);
		}
		transform.Translate(0, 0, InputVertical*0.5f);
		if(transform.position.y<=150)
			transform.Translate(0, InputVertical2*0.25f, 0);
		transform.Translate(InputHorizontal*0.18f, 0, 0);
		transform.Rotate(0, InputHorizontal2*0.5f, 0);
		fireTime = fireTime + Time.deltaTime;
		if (Input.GetButton("Fire1") && fireTime > nextFire)
		{
			nextFire = fireTime + firerate;
			Vector3 customPos = transform.position;
			// Vector3 customRot = transform.rotation;
			customPos.y -= 0.045f;
			customPos.z += 2;
			newmissile = Instantiate(missile, customPos, transform.rotation) as GameObject;
			nextFire -= fireTime;
			fireTime = 0.0f;
		}
	}

	private void OnCollisionEnter(Collision other)
	{
		if (other.gameObject.tag != "Player" ) {
			SceneManager.LoadScene("EndGame");
		}
	}

	private void OnTriggerEnter(Collider other)
	{
		// print("Trigggerrr!!!!");
	}
}
