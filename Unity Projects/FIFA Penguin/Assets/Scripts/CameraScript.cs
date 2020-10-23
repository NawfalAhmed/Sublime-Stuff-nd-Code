using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CameraScript : MonoBehaviour
{
	// Start is called before the first frame update
	public Transform ball;
	Vector3 offset;
	Vector3 trueoffset;
	[Range(0f,2f)]
	public float speed = 0.05f;
	void Start()
	{
		trueoffset=transform.position-ball.position;
		offset=transform.position-ball.position;
	}

	// Update is called once per frame
	void Update()
	{
		if(Input.GetKeyDown(KeyCode.LeftControl))
			offset = trueoffset;
		offset = Quaternion.AngleAxis (Input.GetAxis("PadHorizontal") *speed , Vector3.up) * offset;
		offset.y+=Input.GetAxis("PadVertical")*0.01f;
		if (offset.y<0)
			offset.y = 0;
		if (offset.y>5)
			offset.y = 5;
		print(offset.y);
		transform.position = ball.position + offset;
		transform.LookAt(ball.position);
	}
}
