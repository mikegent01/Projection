using System;
using System.Collections.Generic;
using System.Linq;
using JetBrains.Annotations;
using UnityEngine;
public class background : MonoBehaviour
{
    [SerializeField] Sprite[] backgrounds;
    public Animator Animetor;
    
    public void Changebg(int num)
    {
        gameObject.GetComponent<SpriteRenderer>().sprite = backgrounds[num];
        if (num == 2)
        {
            GetComponent<Animator>().enabled = true;
            Animetor.SetInteger("aninum", num);
        }
        else
        {
            GetComponent<Animator>().enabled = false;
            Animetor.SetInteger("aninum", num);
        }
    }

}
