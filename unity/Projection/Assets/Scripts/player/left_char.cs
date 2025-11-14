using JetBrains.Annotations;
using UnityEngine;

public class left_char : MonoBehaviour
{
    // Start is called once before the first execution of Update after the MonoBehaviour is created
    void Start()
    {

    }
    public Animator anime;
    public void Playanim(string Eventnamer)
    {
        if (Eventnamer == "explosiveentrance"){
        anime = GetComponent<Animator>();
        anime.Play("Slamin");        
        }
    }
    // Update is called once per frame
    void Update()
    {
        
    }
}
