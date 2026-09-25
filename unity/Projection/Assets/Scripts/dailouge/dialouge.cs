using UnityEngine;
using TMPro;
using System.Collections;
using UnityEditor;
using Unity.VisualScripting;
using System;
using System.Collections.Generic;
[System.Serializable]
public class Dialougesystem
{
    List<string> dialouge = new List<string>();
    public string lineofd;
    public string name;
    public Color color;
    public string eventname;
    public int emotion;
}
public class dialouge : MonoBehaviour
{
    public TextMeshProUGUI text;
    public TextMeshProUGUI nametext;
    public List<Dialougesystem> lines;
    public historyscript his;
    public Game_Master gm;
    public objhist objhist;
    public Emotionhandler emohan;
    public float textspeed;
    public DLname dl; 
    public bool enabledl;
    public int index;
    bool Histenabled = false;




    void C0A0()
    {
        lines.Add(new Dialougesystem { lineofd = "Rot. Mold. Decay.", name = "Ben" });
        lines.Add(new Dialougesystem { lineofd = "These words are important to me they mean home.", name = "Ben" });
        lines.Add(new Dialougesystem { lineofd = "I slowly open the door...", name = "Ben" });
        lines.Add(new Dialougesystem { lineofd = "...", name = "Ben" });
        lines.Add(new Dialougesystem { lineofd = "What am I even doing.", name = "Ben" });
        lines.Add(new Dialougesystem { lineofd = "I have been talking to myself outloud like some kind of philosopher.", name = "Ben" });
        lines.Add(new Dialougesystem { lineofd = "Finally", name = "Ben" });
        lines.Add(new Dialougesystem { lineofd = "This place sucks.", name = "Ben" });
        lines.Add(new Dialougesystem { name = "Ben" });
    }
    void Start()
    {
        textspeed = 0.1f;
        lines.Clear();
        lines.Add(new Dialougesystem { lineofd = "The dampness of the hallway I stand in causes.", name = "Chapter Select" });
        lines.Add(new Dialougesystem { lineofd = "My bones ache in pain but my will has not withered.", name = "Chapter Select" });
        lines.Add(new Dialougesystem { lineofd = "The past will not dictate my future.", name = "Chapter Select" });
        lines.Add(new Dialougesystem { lineofd = "As I climb this endless tower the truth unveils itself.", name = "Chapter Select" });
        lines.Add(new Dialougesystem { lineofd = "When the giant wakes...", name = "Ben" });
        C0A0();
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
        Checknextlineemotion();
        Checknextlineevent();
    }
    void Checknextlineemotion()
    {
        if (lines[index].emotion < 0)
        {
            Debug.Log(index + " Next Line dosen't have an emotion!");
        }        
        else
        {
            Debug.Log(index + " has an emotion!");
            StopAllCoroutines();
            emohan.ChangeSprite(lines[index].emotion);
        }                       
    }
    void Checknextlineevent()
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
        if (index < lines.Count - 2)
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
        index = line; //index actual line number
        dl.Changetext(lines[index].name);
        StopAllCoroutines();
        text.text = string.Empty;
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
