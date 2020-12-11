using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ArrowX : MonoBehaviour
{
    public float speed = 20f;
    public Rigidbody2D rb;
    private bool hasHit;
    public Vector3 Enemyposition;
    //public Collider2D tx;
    Speed speedX;

    void Start ()
    {
        speedX = FindObjectOfType<Speed>();
        speed = (speedX.speed * 10f);
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


    void OnTriggerEnter2D (Collider2D hitInfo)
    {
        hasHit = true;
        rb.velocity = Vector2.zero;
        rb.isKinematic = true;

        Destroy(gameObject, 2.0f);
        //Debug.Log(hitInfo.name);


        /* //This worked at relaying coordinates but for somereason output the same
        //coordinates for all objects of the board the same. So changing it up
        // and just creating more than one object on the board to hit
        // going to implement a massive if statement for the point system. 
        GameObject gHit = hitInfo.gameObject;
        Transform tHit = gHit.transform;
        Enemyposition = new Vector3(tHit.position.x, 
                                    tHit.position.y, 
                                    tHit.position.z);
        Debug.Log(Enemyposition);
        */
    }

    /*
    void OnCollisionEnter2D(Collision2D collision)
    {
        hasHit = true;
        rb.velocity = Vector2.zero;
        rb.isKinematic = true;
    }
    
    void OnTriggerEnter2D (Collider2D hitInfo)
    {
        Debug.Log(hitInfo.name);
        Destroy(gameObject);
    }    
    */
    
}
