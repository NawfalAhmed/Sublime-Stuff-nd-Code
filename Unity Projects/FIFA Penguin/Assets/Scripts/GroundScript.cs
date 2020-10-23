using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GroundScript : MonoBehaviour
{
    // Start is called before the first frame update
    void Start()
    {

    }

    // Update is called once per frame
    void Update()
    {
        if(Input.GetKey(KeyCode.LeftArrow)) {
        	transform.Rotate(0, 0, 0.1f);
        }
        if(Input.GetKey(KeyCode.RightArrow)) {
        	transform.Rotate(0, 0, -0.1f);
        }
        // if(Input.GetKey(KeyCode.UpArrow)) {
        // 	transform.Rotate(0.1f, 0, 0);
        // }
        // if(Input.GetKey(KeyCode.DownArrow)) {
        // 	transform.Rotate(-0.1f, 0 , 0);
        // }
    }
}
