using System;
using UnityEngine;

public class animation_card : MonoBehaviour
{
    [SerializeField] private Animator cardani;
    [SerializeField] private string cardliftoff = "Card_Outtro";
    public bool introended = false;
    public InputHandler inputhan;
    public playsound ps;

    public void soundevent()
    {
        ps.soundmanager("intro");        
    }


    public void introend()
    {
        introended = true;
        Debug.Log("Animation Finished You May Click");
    }
    public void playliftoff()
    {
        if (inputhan.animation_card_liftoff == true)
        {
            inputhan.animation_card_liftoff = false;
            cardani.Play(cardliftoff, 0, 0.0f);
        }     
    }

}
