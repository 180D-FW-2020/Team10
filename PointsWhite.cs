using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PointsWhite : MonoBehaviour
{
    Player player;
    public int points;
    // Start is called before the first frame update
    void Start()
    {
        player = FindObjectOfType<Player>();
    }

    // Update is called once per frame
    void OnTriggerEnter2D(Collider2D hit)
    {
        /*
        if (hit.CompareTag("Projectile Arrow"))
        {
        player.points += points;
        }
        Debug.Log(hit.tag);
        */
        player.points += points;
    }
}
