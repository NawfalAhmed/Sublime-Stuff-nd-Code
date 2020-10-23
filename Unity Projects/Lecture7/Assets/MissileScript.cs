using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MissileScript : MonoBehaviour
{
	Rigidbody body;
	GameObject explosion;
	GameObject Gexplosion;
	GameObject Mexplosion;
	// Start is called before the first frame update
	void Start()
	{
		transform.Rotate(100,0,0);
		body  = GetComponent<Rigidbody>();
		body.AddRelativeForce(Vector3.up*2f);
		explosion = Resources.Load("Explosion") as GameObject;
		Gexplosion = Resources.Load("GreatExplosion") as GameObject;
		Mexplosion = Resources.Load("MiniExplosion") as GameObject;
	}

	// Update is called once per frame
	void FixedUpdate()
	{
		body.AddRelativeForce(Vector3.up*1.2f);
	}

	private void OnCollisionEnter(Collision other)
	{
		if (other.gameObject.tag == "Player") {
			return;
		}
		if (other.gameObject.tag == "Enemy" ) {
			Vector3 enemypos = other.gameObject.transform.position;
			enemypos.x = Random.Range(0, 1000);
			enemypos.z = Random.Range(0, 1000);
			other.gameObject.transform.position = enemypos;
			Destroy(transform.gameObject);
			return;
		}
		Vector3 position = transform.position;
		if (other.gameObject.tag == "GreatOne") {
			position.y+=3;
			Instantiate(Gexplosion, position, transform.rotation);
			position.z+=3;
			Instantiate(Gexplosion, position, transform.rotation);
			Destroy(other.gameObject);
		}
		else if(!other.gameObject.name.StartsWith("Terrain"))
		{
			Instantiate(explosion, transform.position, transform.rotation);
			Destroy(other.gameObject);
		}
		else {
			position.y-=2;
			Instantiate(Mexplosion, position, transform.rotation);
		}
		Destroy(transform.gameObject);
	}
}
