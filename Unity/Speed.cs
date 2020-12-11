using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Speed : MonoBehaviour
{
    public float speed;
}
//This file needs to be attactched somewhere in the scene, so that when an arrow is generated it can access this speed variable
//that changes as data is brought through from the M2MqttUnityClientFire script that connects to our broker at broker.hivemq.com
//with the topic MRDMarcher/fire

//The reason this is necessary is because the arrow does not generate until it is called upon, so you can't modify it's data in a constant
//stream. But you can modify some data dump variable that is always generated and then call upon that variable upon generation of the arrow
