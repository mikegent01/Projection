using UnityEngine;

public class Game_Master : MonoBehaviour
{
    public bool cardget = true;
    public animation_card anicard;
    public background bg;
    public dialouge dl;
    public playsound ps;
    public leftb lb;
    public buttonright rb;
    public hidebuttons hb;

    public RainbowText_V1 rain;
    public Mainmenu mm;
    public int chapternum;
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
    void Gaincard(){ // no idea when this will be used 
        anicard.Startcardget();
        rain.begincolor();
        ps.Soundmanager(0);         
        bg.Changebg(0);
    }

}
