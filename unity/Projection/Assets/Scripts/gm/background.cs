using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using JetBrains.Annotations;
using UnityEngine;
public class Background : MonoBehaviour
{
    [SerializeField] Sprite[] backgrounds;
    public Animator Animetor;
    public int svbg = 0;
    public void Changebg(int num)
    {
        if (backgrounds == null || num < 0 || num >= backgrounds.Length)
        {
            Debug.LogError("Background.Changebg: index " + num + " is out of range!");
            return;
        }
        if (backgrounds[num] == null)
        {
            // keep the current sprite instead of going blank — the slot
            // still needs art assigned in the inspector!
            Debug.LogWarning("Background.Changebg: slot " + num + " has no sprite assigned, keeping current background.");
        }
        else
        {
            gameObject.GetComponent<SpriteRenderer>().sprite = backgrounds[num];
        }
        svbg = num;
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
