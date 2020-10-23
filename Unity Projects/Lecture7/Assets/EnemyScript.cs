using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class EnemyScript : MonoBehaviour
{
	 GameObject player;
	 // Start is called before the first frame update
	 void Start()
	 {
		player = GameObject.Find("Missile-Heli");
	 }

	 // Update is called once per frame
	 void Update()
	 {
		  transform.Translate(0,0,0.2f);
		  transform.LookAt(player.transform);
	 }
}
