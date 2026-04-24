using System;
using JetBrains.Annotations;
using NUnit.Framework.Constraints;
using UnityEngine;

public class Emotionhandler : MonoBehaviour
{


 [SerializeField] Sprite[] Emotion;

    public void ChangeSprite(int spritename)
    {
        gameObject.GetComponent<SpriteRenderer>().sprite = Emotion[spritename];
    }
}
