using UnityEngine;

public class playsound : MonoBehaviour
{
    public InputHandler inputhan;
    public animation_card anicar;
    [Header("Audio")]

    [SerializeField] AudioSource soundSource;
    [Header ("Music")]

    [SerializeField] AudioSource musicSource;
    [Header ("Var")]

    public AudioClip liftoff;
    public AudioClip click;
    public AudioClip get;



    // probably should be a directory but its just 4 things lol
    public void soundmanager(string name)
    {
        if (name == "intro")
        {
            musicSource.clip = liftoff;
            musicSource.Play();
        }
        else if (name == "click")
        {
            musicSource.clip = click;
            musicSource.Play();
        }      
        else if (name == "get")
        {
            musicSource.clip = get;
            musicSource.Play();
        }                  
        else
        {
            Debug.Log("Tried to play sound but failed :O");

        }
    }
}
