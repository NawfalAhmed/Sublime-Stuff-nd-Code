public class GameEvents : MonoBehaviour {
	public static GameEvents manager;
	void Awake() {
		manager =  this;
	}
	public event System.Action onPlayerFired;
	public void TriggerPlayerFired() {
		if (onPlayerFired!= null)
			onPlayerFired();
	}
}

public class Enemy : MonoBehaviour {
	spotted = false;
	void Start () {
		GameEvents.manager.onPlayerFired += PlayerFired;
		//ur code here
	}
	void Update() {
		//ur code here
		if (spotted) {
			//what to do if spotted
		}
	}
	void PlayerFired() {
		spotted = true;
	}
	private void OnDestroy() {
		GameEvents.manager.onPlayerFired -= PlayerFired;
	}
}


// call this in some object to invoke the event
GameEvents.manager.TriggerPlayerFired();
