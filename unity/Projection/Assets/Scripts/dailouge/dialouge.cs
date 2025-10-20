using UnityEngine;
using TMPro;
using System.Collections;
using UnityEditor;
[System.Serializable]
public class Dialougesystem
{
    public string lineofd;
    public string eventname;
}

public class dialouge : MonoBehaviour
{
    public TextMeshProUGUI text;
    public Dialougesystem[] lines;
    public float textspeed;
    public bool enabledl;
    private int index;
    
    // Start is called once before the first execution of Update after the MonoBehaviour is created
    void Start() // WALL OF TEXT 
    {
        gameObject.SetActive(false);
        //chapter select lines
        lines[0].lineofd = "My heart feels heavy and my head feels light.";
        lines[1].lineofd = "My bones ache in pain but my will has not withered.";
        lines[2].lineofd = "The past will not dictate my future.";
        lines[3].lineofd = "As I climb this endless tower the truth unveils itself.";
        lines[4].lineofd = "When the giant wakes...";
    }
    public void Dlsetup()
    {
        text.text = string.Empty;
        Startdialouge();
        enabledl = false;        
    }
    public void Nextline()
    {
        if (text.text == lines[index].lineofd)
        {
            NextLine();
        }
        else
        {
            StopAllCoroutines();
            text.text = lines[index].lineofd;
        }
    }
    // Update is called once per frame

    void Startdialouge()
    {
        index = 0;
        StartCoroutine(Typeline());
    }
    void NextLine()
    {
        if (index < lines.Length - 1)
        {
            index++;
            text.text = string.Empty;
            StartCoroutine(Typeline());
        }
        else
        {
            gameObject.SetActive(false);
        }
    }
    public void Setline(int line)
    {
        StopAllCoroutines();
        text.text = string.Empty;
        index = line; //index actual line number
        StartCoroutine(Typeline());
    }        
    public void Previousline()
    {
        if (index > 0)
        {
            StopAllCoroutines();
           text.text = string.Empty;
           index = index--;
           index = index--;
           StartCoroutine(Typeline());

        }
        else
        {
            gameObject.SetActive(false);
        }
    }    
    IEnumerator Typeline()
    {
        foreach (char c in lines[index].lineofd.ToCharArray())
        {
            text.text += c;
            yield return new WaitForSeconds(textspeed);
        }
    }
}
