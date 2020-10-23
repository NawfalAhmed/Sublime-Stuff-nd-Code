using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CameraControllerScript : MonoBehaviour {
	public Camera[] cameras;
	private int currentIndex;
	// Start is called before the first frame update
	void Start()
	{
		cameras[0].enabled = true;
		currentIndex = 0;
		for (int i = 1; i<cameras.Length; i++)
			cameras[i].enabled= false;

	}
	// Update is called once per frame
	void Update()
	{
		if (Input.GetKeyDown(KeyCode.C)) {
			cameras[currentIndex].enabled= false;
			cameras[currentIndex].GetComponent<AudioListener>().enabled = false;
			currentIndex++;
			if (currentIndex >= cameras.Length)
				currentIndex = 0;
			cameras[currentIndex].enabled= true;
			cameras[currentIndex].GetComponent<AudioListener>().enabled = true;
		}
	}
}
