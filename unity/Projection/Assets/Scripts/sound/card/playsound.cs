using System;
using JetBrains.Annotations;
 using System.Collections.Generic; 
using UnityEngine;
using System.Linq;
using System.Collections;
public class playsound : MonoBehaviour
{
    public List<AudioClip> musiclist = new List<AudioClip>();

    public int[] songsthatloop = new int[5]; // update this when adding looping songs

    public animation_card anicar;
    public Volumecontrol vc;
    public Musicvolcontrol mvc;
    [Header("Audio")]
    [SerializeField] AudioSource soundSource;
    [Header ("Music")]
    public AudioClip the_last_horn;

    [SerializeField] AudioSource musicSource;
    [Header ("Var")]

    public AudioClip liftoff;
    public AudioClip dooropen;
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
        musiclist.Add(dooropen); //4 click on card get sound
    }
    public void Stopallsounds()
    {
        musicSource.Stop();
    }
    public void Soundmanager(int num)
    {
        musicSource.loop = false;
        if (musiclist.Count > num)
        {
            Debug.Log("Played song #" + num);
            musicSource.PlayOneShot(musiclist[num]);
            if (songsthatloop.Contains(num))
            {
                musicSource.loop = true;
                Debug.Log("Looping song #" + num);
            }
        }
        else
        {
            Debug.Log("Tried to play sound but failed :O");

        }
    }
    public void Fadeoutvool()
    {
        StartCoroutine(vc.Fadeoutvol());
        StartCoroutine(mvc.Fadeoutvol2());
    }
    public void Fadeinvoolume()
    {
        StartCoroutine(vc.Fadeinvol());
        StartCoroutine(mvc.Fadeinvol2());
    }
 
}
