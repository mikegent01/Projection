using System;
using Unity.VisualScripting;
using UnityEngine;

public class animation_card : MonoBehaviour
{
    [SerializeField] private Animator cardani;
    [SerializeField] private string cardliftoff = "Card_Outtro";
    public bool Introended = false;
    public InputHandler inputhan;
    public playsound ps;



    public void Startcardget()
    {
        cardani.gameObject.SetActive(true);
        cardani.gameObject.GetComponent<Animator>().enabled = true;           
    }
    public void Introend()
    {
        Introended = true;
        Debug.Log("Animation Finished You May Click");
    }
    public void Playliftoff()
    {
        if (inputhan.animation_card_liftoff == true)
        {
            inputhan.animation_card_liftoff = false;
            cardani.Play(cardliftoff, 0, 0.0f);
        }     
    }

}
