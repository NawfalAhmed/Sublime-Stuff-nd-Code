using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class EnemyAI : MonoBehaviour
{
	 // Start is called before the first frame update
	public GameObject Enemy;
	void Start()
	{
		  for(int i =0; i<2;i++) {
			Vector3 pos = new Vector3(Random.Range(-100,1100),Random.Range(15,40),Random.Range(-100,1200));
			Instantiate(Enemy, pos, Quaternion.identity);
		  }
	}

	 // Update is called once per frame
	 void Update()
	 {

	 }
}
