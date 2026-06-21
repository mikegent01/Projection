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
    public int emotion;
}
public class dialouge : MonoBehaviour
{
    public TextMeshProUGUI text;
    public TextMeshProUGUI nametext;
    public Dialougesystem[] lines;
    public historyscript his;
    public Game_Master gm;
    public objhist objhist;
    public Emotionhandler emohan;
    public float textspeed;
    public DLname dl; 
    public bool enabledl;
    public int index;
    bool Histenabled = false;

    // Start is called once before the first execution of Update after the MonoBehaviour is created
    void Start() // WALL OF TEXT 
    {
        textspeed = 0.01f;
       // gameObject.SetActive(false);
        //chapter select lines
        int x = 0;
        while (x != 4)
        {
            lines[x].name = "Chapter Select";
            x++;
        }
        while (x != 12)
        {
            lines[x].name = "Ben";
            x++;
        }        
      lines[0].lineofd = "The dampness of the hallway I stand in causes.";
        lines[1].lineofd = "My bones ache in pain but my will has not withered.";
        lines[2].lineofd = "The past will not dictate my future.";
        lines[3].lineofd = "As I climb this endless tower the truth unveils itself.";
        lines[4].lineofd = "When the giant wakes...";
        // begin DL CH0
        lines[5].lineofd = "The door creeks open as the handle falls off its hinges I quickly pick it up as a rotted wooden piece falls down a splash being heard below me.";
        lines[6].lineofd = "I look up from the door into the room I used to call home.The smell of moldy mildew hits my nose. My nose scrunches up and I recoil.";
        
        lines[6].lineofd = "I recognize the smell, I could never really get used to it. I take one step forward another splash is heard I look down to the source of the noise.";
        lines[7].lineofd = "The broken door handle in my hand stares back at me. I remembered what this room meant to me how the people here used to be not just friends but family.";
        lines[8].lineofd = "How all of them slowly failed training or moved away. Now its just me its not my home anymore only strangers remain my hand lossens its grip. A thunk is heard on the ground as the door handle lays there in a puddle of its own sorrow. I begin to walk forward trying to forget the past another splash is heard and...";
        lines[9].eventname = "explosiveentrance";
        lines[9].lineofd = "My feet skid across the wet floor, I catch myself before I fall. Could I have been pranked or did the janitors just not do there job. It could have been both for all I knew.";
        lines[10].emotion = 1; //embaresed 
        lines[11].lineofd = "My pants are soaking wet. My face is burning hot, My own self doubt consuming me like the moldy walls of this room. I begin to consider my options.";
        lines[12].lineofd = "I can run away leave this all behind right now or I can look up and walk straight ahead with a smile. ";
        lines[13].lineofd = "I freeze up looking around the room, most seats were empty only the best of the best remained. Do I really deserve to be here?";
        lines[14].lineofd = "I ball my fists up and look up. Everyone else in the room seems to distracted. The faint smell of mildew and the state of th eothers uniforms tells me it will be okay. ";
        lines[15].lineofd = "I begin to walk forward trying to ignore my soaked pants as they brush against my rough skin. It is a privilege to shower and my lack of confidence left me without it.";
        lines[16].lineofd = "I begin to hyperfocus on my walking one step forward and than another... I walk past empty seats slowly. methodology making sure to not trip ever again...";
        lines[9].eventname = "Benleaveleft";
        //new scene logic here
        lines[17].lineofd = "";
        
        
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
