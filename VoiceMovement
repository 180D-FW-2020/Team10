using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Linq;
using UnityEngine.Windows.Speech;

public class VoiceMovement : MonoBehaviour
{
    private KeywordRecognizer keywordRecognizer;
    private Dictionary<string, Action> actions = new Dictionary<string, Action>();

    void Start() 
    {
        actions.Add("forward", Forward);
        //actions.Add("jump", Up);
        actions.Add("back", Back);

        keywordRecognizer = new KeywordRecognizer(actions.Keys.ToArray());
        keywordRecognizer.OnPhraseRecognized += RecognizedSpeech;
        keywordRecognizer.Start(); // Use this to start listening, Might be useful so it is not listening always. 

    }

    private void RecognizedSpeech(PhraseRecognizedEventArgs speech)
    {
        Debug.Log(speech.text);
        actions[speech.text].Invoke();
    }

    private void Forward()
    {
        transform.Translate(1,0,0);
    }

    private void Back()
    {
        transform.Translate(-1,0,0);
    }

/*
    private void Up()
    {
        //_rigidbody.AddForce(new Vector2(0, JumpForce), ForceMode2D.Impulse);
        transform.Translate(0,10,0);
    }
*/
}
