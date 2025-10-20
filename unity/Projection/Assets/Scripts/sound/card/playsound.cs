using System;
using JetBrains.Annotations;
 using System.Collections.Generic; 
using UnityEngine;
using System.Linq;
public class playsound : MonoBehaviour
{
    public List<AudioClip> musiclist = new List<AudioClip>();

    public int[] songsthatloop = new int[5]; // update this when adding looping songs

    public animation_card anicar;
    [Header("Audio")]

    [SerializeField] AudioSource soundSource;
    [Header ("Music")]
    public AudioClip the_last_horn;

    [SerializeField] AudioSource musicSource;
    [Header ("Var")]

    public AudioClip liftoff;
    public AudioClip click;
    public AudioClip get;
    // probably should be a directory but its just 4 things lol
    void Awake()
    {

        songsthatloop[0] = 1; // also a nice thing to be a list of music
        musiclist.Add(liftoff); // 0 sfx card up
        musiclist.Add(the_last_horn); // 1 music titlescreen
        musiclist.Add(click); // 2 click generic
        musiclist.Add(get); //3 click on card get sound
    }

    public void Soundmanager(int num)
    {
        musicSource.loop = false;
        if (musiclist.Count > num)
        {
            musicSource.PlayOneShot(musiclist[num]);
            if (songsthatloop.Contains(num))
            {
                musicSource.loop = true;
            }
        }
        else
        {
            Debug.Log("Tried to play sound but failed :O");

        }
    }
}
