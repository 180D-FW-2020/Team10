using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Weapon_Rotate : MonoBehaviour
{
    // Start is called before the first frame update
    // public Transform firePoint;
    // public GameObject bulletPrefab;
    public float offset;

    // Update is called once per frame
    void Update()
    {
        Vector3 difference = Camera.main.ScreenToWorldPoint(Input.mousePosition) - transform.position;
        float rotZ = Mathf.Atan2(difference.y, difference.x) * Mathf.Rad2Deg;
        transform.rotation = Quaternion.Euler(0f, 0f, rotZ + offset);


        // if (Input.GetButtonDown("Fire1"))
        // {
        //     Shoot();
        // }
    }

}
