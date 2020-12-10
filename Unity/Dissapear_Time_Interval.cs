using UnityEngine;
using UnityEngine.UI;

public class Dissapear_Time_Interval : MonoBehaviour
{
    void Start()
    {
        Destroy(gameObject, 1.0f);
        // Attempt at making the text fade in then fad out. Might be better to just have
        // a fade out, will see If I can get this to work. 
        // gO.CrossFadeAlpha(1, 2.0f, false);
        // WaitForSeconds(5.0f);
        // dmarcher.CrossFadeAlpha(0,2.0f,false);
    }
}
