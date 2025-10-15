using System;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;
public class background : MonoBehaviour
{
    [SerializeField] Sprite[] backgrounds;
    public void changebg(int num)
    {
        gameObject.GetComponent<SpriteRenderer>().sprite = backgrounds[num];
    }

}
