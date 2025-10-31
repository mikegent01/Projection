using UnityEngine;
using System.Collections;
using System.IO;
using UnityEngine.SceneManagement;
using JetBrains.Annotations;
public class Game_Master : MonoBehaviour
{
    public bool cardget = true;
    public animation_card anicard;
    public Background bg;
    public dialouge dl;
    public playsound ps;
    public Transitionmanager tm;
    public S_Camera cm;
    public leftb lb;
    public buttonright rb;
    public hidebuttons hb;

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
        chapternum = 0;
        mm.Enablemenu();
        hb.gameObject.SetActive(false);
        bg.Changebg(1);
        rain.Changetext("Projection");
        ps.Soundmanager(1); // the_last_horn
    }
    public void Rightnextchapter()
    {
        if (chapternum < 5)
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
        if (chapternum > 0)
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
}
