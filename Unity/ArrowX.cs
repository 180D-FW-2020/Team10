using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ArrowX : MonoBehaviour
{
    public float speed = 20f; //This sets the float speed for the object in game
    public Rigidbody2D rb;  //Need Rigidbody2D for collision
    public bool hasHit; //This allows us to use the object to see if it has hit another object on collider


    void Start ()
    {
        rb.velocity = transform.right * speed;
        rb = GetComponent<Rigidbody2D>();
    }

    void Update()
    {
        if (hasHit == false)
        {
        float angle = Mathf.Atan2(rb.velocity.y, rb.velocity.x) * Mathf.Rad2Deg;
        transform.rotation = Quaternion.AngleAxis(angle, Vector3.forward);
        }
    }

    // happens when the object collides with another object with a collider attatched to it
    void OnTriggerEnter2D (Collider2D hitInfo)
    {
        hasHit = true;
        rb.velocity = Vector2.zero;
        rb.isKinematic = true;
        Destroy(gameObject, 2.0f); 
    }

    /*// IGNORE THIS CODE BELOW
    void OnCollisionEnter2D(Collision2D collision)
    {
        hasHit = true;
        rb.velocity = Vector2.zero;
        rb.isKinematic = true;
    }
    
    //This function should output the name of the object that it hits. 
    /*void OnTriggerEnter2D (Collider2D hitInfo)
    {
        Debug.Log(hitInfo.name);
        Destroy(gameObject);
    }    
    */
    
}
