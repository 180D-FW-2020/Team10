using UnityEngine;
using UnityEngine.UI;

public class Score : MonoBehaviour
{
    Player player;
    public Text scoreText;
    void Start()
    {
        player = FindObjectOfType<Player>();
    }

    // Update is called once per frame
    void Update()
    {
        scoreText.text = player.points.ToString();
    }
}
