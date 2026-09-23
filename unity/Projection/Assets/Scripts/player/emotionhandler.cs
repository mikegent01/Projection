using System;
using JetBrains.Annotations;
using NUnit.Framework.Constraints;
using UnityEngine;

public class Emotionhandler : MonoBehaviour
{


 [SerializeField] Sprite[] Emotion;

    public void ChangeSprite(int spritename)
    {
        if (Emotion == null || Emotion.Length == 0)
        {
            Debug.LogWarning("Emotionhandler on " + gameObject.name + ": no emotion sprites assigned!");
            return;
        }
        if (spritename < 0 || spritename >= Emotion.Length || Emotion[spritename] == null)
        {
            Debug.LogWarning("Emotionhandler on " + gameObject.name + ": emotion index " + spritename + " not available, keeping current sprite.");
            return;
        }
        gameObject.GetComponent<SpriteRenderer>().sprite = Emotion[spritename];
    }
}
