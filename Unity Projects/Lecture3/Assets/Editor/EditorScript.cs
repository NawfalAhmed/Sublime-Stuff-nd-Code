// using System.Collections;
// using System.Collections.Generic;
// using UnityEngine;
// using UnityEditor;

// public class EditorScript : EditorWindow
// {
// 	void OnSceneGUI(SceneView sceneView)
// 	{
// 		Vector3 mousePosition = Event.current.mousePosition;
// 		mousePosition.y = sceneView.camera.pixelHeight - mousePosition.y;
// 		mousePosition = sceneView.camera.ScreenToWorldPoint(mousePosition);
// 		mousePosition.y = -mousePosition.y;
// 		print(mousePosition);
// 	}
// }
