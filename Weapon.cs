using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Linq;
using UnityEngine.Windows.Speech;

public class Weapon : MonoBehaviour
{

    public Transform firePoint;
    public GameObject bulletPrefab;
    public float offset;
    
    //attempt at adding ammo
    public int maxAmmo = 3;
    private int currentAmmo;
    //public float reloadTIme = 1f;

    // Attempting to add voice recognition to fire the arrow
    private KeywordRecognizer keywordRecognizer;
    private Dictionary<string, Action> actions = new Dictionary<string, Action>();

    void Start()
    {
        actions.Add("fire", Shoot);
        actions.Add("reload", Reload);

        keywordRecognizer = new KeywordRecognizer(actions.Keys.ToArray());
        keywordRecognizer.OnPhraseRecognized += RecognizedSpeech;
        keywordRecognizer.Start(); // Use this to start listening, Might be useful so it is not listening always.

        currentAmmo = maxAmmo; // Set's starting ammo to max when launching the game

    }

    // Update is called once per frame
    void Update()
    {
        //This allows us to fire a bulletPrefab from a firePoint that we allocated on the scene
        //This will also allow there to be rotation with respect ot the mouse position on screen. 
        //I believe later we will have to import the constant change in vertical angle with respect
        //to a point on screen for the arrow when integrated. 
        Vector3 difference = Camera.main.ScreenToWorldPoint(Input.mousePosition) - transform.position;
        float rotZ = Mathf.Atan2(difference.y, difference.x) * Mathf.Rad2Deg;
        transform.rotation = Quaternion.Euler(0f, 0f, rotZ + offset);


        if (Input.GetButtonDown("Fire1"))
        {
            Shoot();
        }
    }

    private void RecognizedSpeech(PhraseRecognizedEventArgs speech)
    {
        Debug.Log(speech.text);
        actions[speech.text].Invoke();
    }

    void Shoot()
    {
        // Shooting Logic
        if(currentAmmo > 0)
        {
        GameObject newArrow = Instantiate(bulletPrefab, firePoint.position, firePoint.rotation);
        }
        if(currentAmmo <= 0)
        {
            Debug.Log("You need to say reload");
        }
        currentAmmo--; // This subtracts from our current ammo each time we shoot

    }

    void Reload() 
    {
        Debug.Log("Reloading");

        //yield return new WaitForSeconds(reloadTime);

        currentAmmo = maxAmmo;
        
    }
}
