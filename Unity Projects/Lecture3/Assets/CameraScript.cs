using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CameraScript : MonoBehaviour
{
	// Start is called before the first frame update
	public Transform car;
	[Range(0f,2f)]
	public float speed = 0.05f;
	// var cameradistance;
	Vector3 hood;
	Vector3 offset;
	Vector3[] cameradistance;
	int index;

	void Start()
	{
		hood = new Vector3(0f,5.11f*0.3f,2.7f);
		cameradistance = new Vector3[4];
		cameradistance[0]=transform.position-car.position;
		cameradistance[1]=transform.position+Vector3.back*5+Vector3.up*3-car.position;
		cameradistance[2]=transform.position+Vector3.back*7+Vector3.up*5-car.position;
		cameradistance[3]=hood;
		offset=transform.position-car.position;
	}

	// Update is called once per frame
	void Update()
	{
		if(Input.GetKeyDown(KeyCode.C)) {
			if (index == 3)
				index = -1;
			offset = cameradistance[++index];
		}
		offset = Quaternion.AngleAxis (Input.GetAxis("PadHorizontal") *speed , Vector3.up) * offset;
		offset.y+=Input.GetAxis("PadVertical")*0.05f*speed;
		if (offset.y<0.5f)
			offset.y = 0.5f;
		if (offset.y>15)
			offset.y = 15;
		transform.position = car.position + offset;
		if(index == 3)
			transform.LookAt(car.position+hood);
		else transform.LookAt(car.position);
	}
}
