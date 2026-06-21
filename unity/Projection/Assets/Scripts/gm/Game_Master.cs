using UnityEngine;
using System.Collections;
using System.IO;
using UnityEngine.SceneManagement;
using JetBrains.Annotations;
using Unity.Collections;
using UnityEditor.Tilemaps;
using System;
using UnityEngine.Rendering.Universal;
using Unity.VisualScripting;
public class Game_Master : MonoBehaviour
{
    public bool cardget = true;
    public animation_card anicard;
    public Background bg;
    public Animator lcanimtor;
    public dialouge dl;
    public left_char lc;
    public playsound ps;
    public string Eventnamer;
    public Fadesystem fs;
    public Transitionmanager tm;
    public S_Camera cm;
    public bool gameactive = false;
    public leftb lb;
    public S_Camera scam;
    public buttonright rb;
    public hidebuttons hb;
    private PixelPerfectCamera ppc;
    public RainbowText_V1 rain;
    public Mainmenu mm;
    public int chapternum;
    //      INITAL GAME START MAIN MENU AND OTHER STUFF      //
    void Start()
    {
        Startgamemenu();
    }
    void Startgamemenu()
    {
        // this starts the game call this first always :D
        dl.gameObject.SetActive(true);
        chapternum = 0;
        mm.Enablemenu();
        hb.gameObject.SetActive(false);
        dl.gameObject.SetActive(false);
        bg.Changebg(6);
        rain.gameObject.SetActive(false);
        rain.Changetext("Projection");
        ps.Soundmanager(1); // the_last_horn
    }
    public void Rightnextchapter()
    {
        if (chapternum < 5 && gameactive == false)
        {
            chapternum++;
            lb.gameObject.SetActive(true);
            rain.Changetext("Chapter" + " " + chapternum);
            Chapterbgchanger();
            if (chapternum == 4)
            {
                rb.gameObject.SetActive(false);
            }
        }
        else
        {
            try { bg.svbg += 1; }
            catch (Exception)
            {
                print("You failed to change BG");
            }
            dl.Setline(bg.svbg);
        }


    }
    private void Chapterbgchanger()
    {
        // index maybe should have an effect here
        if (chapternum == 0)
        {
            dl.Setline(0);
            bg.Changebg(0);
        }
        if (chapternum == 1)
        {
            bg.Changebg(1);
            dl.Setline(1);
        }
        if (chapternum == 2)
        {
            bg.Changebg(2);
            dl.Setline(2);
        }
        if (chapternum == 3)
        {
            bg.Changebg(2);
            dl.Setline(3);
        }
        if (chapternum == 4)
        {
            bg.Changebg(2);
            dl.Setline(4);
        }
    }
    public void Leftnextchapter()
    {
        Chapterbgchanger();
        if (chapternum > 0 && gameactive == false)
        {
            chapternum--;
            rb.gameObject.SetActive(true);
            rain.Changetext("Chapter" + " " + chapternum);
            Chapterbgchanger();
            if (chapternum == 0)
            {
                lb.gameObject.SetActive(false);
            }
        }
        else
        {
            bg.svbg -= 1;
            dl.Setline(bg.svbg);
        }        
    }
    public void Startchapterselect()
    {
        rain.Changetext("Chapter" + " " + chapternum);
        hb.gameObject.SetActive(true);
        rb.gameObject.SetActive(true);
        hb.gameObject.SetActive(true);
        Gaincard();
        dl.enabledl = true;
        dl.gameObject.SetActive(true);
        dl.Dlsetup();
    }
    void Gaincard() // card goes up from bottom of screen
    {
        anicard.Startcardget();
        rain.Begincolor();
        ps.Soundmanager(0);
        bg.Changebg(0);
    }
    // save and load systems//

    public void Savegame()
    {
        using (StreamWriter sw = new StreamWriter(Application.dataPath + "/save.dat", false))
        {
            //You want to edit the file yourself go ahead! this is a csv file first is bg 2nd is line number
            sw.WriteLine(bg.svbg + "," + dl.index);
        }
    }
    int Numbg;
    int Numline;
    public void Loadgame()
    {
        StreamReader strReader = new StreamReader(Application.dataPath + "/save.dat");
        bool eof = false;
        while (!eof)
        {
            string data_string = strReader.ReadLine();
            if (data_string == null)
            {
                eof = true;
                break;
            }
            var datavalues = data_string.Split(',');
            Numbg = int.Parse(datavalues[0]);
            Numline = int.Parse(datavalues[1]);
            bg.Changebg(Numbg);
            dl.Setline(Numline);
        }

    }
    /// CH01 START FUN
    public void Chp0()
    {
        dl.gameObject.SetActive(true);
        ppc = scam.GetComponent<PixelPerfectCamera>();
        ppc.assetsPPU = 101;
        ps.Fadeoutvool();
        fs.gameObject.SetActive(false);
        mm.gameObject.SetActive(false);
        rain.gameObject.SetActive(false);
        tm.Fadein();
        ps.Stopallsounds();
        ps.Fadeinvoolume();
        dl.Setline(4);
        dl.NextLinePhaser();
        dl.enabledl = true;
        bg.Changebg(5); //scene one begin!
        hb.gameObject.SetActive(false);
        gameactive = true;
    }
    public void Handleevents(string Eventnamer)
    {
        if (Eventnamer == "explosiveentrance")
        {
            Debug.Log("explosiveentrance");
            lc.Playanim("explosiveentrance");
            ps.Soundmanager(4);
            StopAllCoroutines();
           }
        if (Eventnamer == "Benleaveleft")
        {
            Debug.Log("Benleaveleft");
            lc.Playanim("Benleaveleft");
            StopAllCoroutines();
           }           
    }

}
