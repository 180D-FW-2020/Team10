using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

//[ExecuteInEditMode()]
public class ProgressBar : MonoBehaviour
{
    Speed speedX;

    public int maximum;
    public float current;
    public Image mask;

    // Start is called before the first frame update
    void Start()
    {
        speedX = FindObjectOfType<Speed>();
    }

    // Update is called once per frame
    void Update()
    {
        current = speedX.speed;
        GetCurrentFill();
    }

    void GetCurrentFill()
    {
        float fillAmount = (float)current / (float)maximum;
        mask.fillAmount = fillAmount;
    }
}
