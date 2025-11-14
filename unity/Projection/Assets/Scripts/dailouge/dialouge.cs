using UnityEngine;
using TMPro;
using System.Collections;
using UnityEditor;
using Unity.VisualScripting;
using System;
[System.Serializable]
public class Dialougesystem
{
    public string lineofd;
    public string name;
    public Color color;
    public string eventname;
    public string emotion;
}
public class dialouge : MonoBehaviour
{
    public TextMeshProUGUI text;
    public TextMeshProUGUI nametext;
    public Dialougesystem[] lines;
    public historyscript his;
    public Game_Master gm;
    public objhist objhist;
    public float textspeed;
    public DLname dl; 
    public bool enabledl;
    public int index;
    bool Histenabled = false;

    // Start is called once before the first execution of Update after the MonoBehaviour is created
    void Start() // WALL OF TEXT 
    {
        gameObject.SetActive(false);
        //chapter select lines
        int x = 0;
        while (x != 4)
        {
            lines[x].name = "Chapter Select";
            x++;
        }
        lines[0].lineofd = "My heart feels heavy and my head feels light.";
        lines[1].lineofd = "My bones ache in pain but my will has not withered.";
        lines[2].lineofd = "The past will not dictate my future.";
        lines[3].lineofd = "As I climb this endless tower the truth unveils itself.";
        lines[4].lineofd = "When the giant wakes...";
        // begin DL CH0
        lines[5].lineofd = "20XX 10/12";
        lines[5].eventname = "explosiveentrance";
        lines[6].lineofd = "Cool";
        lines[7].name = "Ben";
        lines[7].lineofd = "Whoops!";
    }
    public void Populatehistory()
    {
        if (Histenabled == false)
        {
            Histenabled = true;
            objhist.gameObject.SetActive(true);
            his.gameObject.SetActive(true);
            his.Populate(index);
        }
        else
        {
            objhist.gameObject.SetActive(false);
            his.gameObject.SetActive(false);
            Histenabled = false;
        }
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
            dl.Changetext(lines[index].name);
        }
        else
        {
            StopAllCoroutines();
            text.text = lines[index].lineofd;
        }
    }
    public void NextLinePhaser()
    {
        if (lines[index].eventname ==null || lines[index].eventname =="")
        {
            Debug.Log(index + " Next Line dosen't have an event!");
            StopAllCoroutines();
            dl.Changetext(lines[index+1].name);
            
           NextLine();
        }
        else
        {
            
            Debug.Log(index + " has an event!");
            StopAllCoroutines();
            gm.Handleevents(lines[index].eventname);
            NextLine();         
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
        if (index < lines.Length - 2)
        {
            index++;
            text.text = string.Empty;
            Setcolor();
            StartCoroutine(Typeline());
        }
        else
        {
            Debug.Log("End of script!");
            gameObject.SetActive(false);
        }
    }
    void Setcolor()
    {
        if (lines[index].color != null)
        {
            if (lines[index].name != null )
            {
                Debug.Log(index + "name color!");
                Characolor(lines[index].name);
                
            }
            else
            {
            Debug.Log(index + "null color!");

            nametext.color = lines[index].color;
                
            }            
        }
        else
        {

                if (lines[index].color != new Color32(0, 0, 0, 255))
                {
                    lines[index].color = new Color32(0, 0, 0, 255);
                    nametext.color = new Color32(0, 0, 0, 255);
                    Debug.Log(index + "No Chara Color found, or cutom color set setting to black!");
                }
                else
            {
                    Debug.Log(index + "Custom Color set!");
            }
            }
    }

    void Characolor(String name)
    {
        name = name.ToLower();
        if (name == "ben" || name == "benjamin"|| name == "allec")
        {
            lines[index].color = new Color32(158, 255, 0, 255);
            nametext.color = new Color32(158, 255, 0, 255);
        }
    }
    public void Setline(int line)
    {
        dl.Changetext(lines[index].name);
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
