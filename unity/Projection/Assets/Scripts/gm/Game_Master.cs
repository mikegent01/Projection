using UnityEngine;
using System.Collections;
using System.IO;
using UnityEngine.SceneManagement;
using JetBrains.Annotations;
using Unity.Collections;
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
    // Highest chapter the select screen can browse (chapters actually have
    // preview text/backgrounds defined). Only chapter 0 is playable so far,
    // but its siblings are defined and browsable.
    const int LastSelectableChapter = 4;

    public void Rightnextchapter()
    {
        if (gameactive) return;
        if (chapternum < LastSelectableChapter)
        {
            chapternum++;
            rain.Changetext("Chapter" + " " + chapternum);
            Chapterbgchanger();
            UpdateChapterNav();
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
        if (gameactive) return;
        if (chapternum > 0)
        {
            chapternum--;
            rain.Changetext("Chapter" + " " + chapternum);
            Chapterbgchanger();
            UpdateChapterNav();
        }
    }

    /// <summary>Enable/dim the PREV / NEXT chips at the ends of the chapter list.</summary>
    void UpdateChapterNav()
    {
        if (dl != null && dl.box != null)
        {
            dl.box.SetChapterNavState(chapternum > 0, chapternum < LastSelectableChapter);
        }
    }

    public void Startchapterselect()
    {
        rain.Changetext("Chapter" + " " + chapternum);
        Gaincard();
        if (dl.his != null) dl.his.ClearLog(); // fresh run -> fresh field log
        dl.enabledl = true;
        dl.gameObject.SetActive(true);
        dl.Dlsetup();
        UpdateChapterNav();
    }
    void Gaincard() // card goes up from bottom of screen
    {
        anicard.Startcardget();
        rain.Begincolor();
        ps.Soundmanager(0);
        bg.Changebg(0);
    }
    // save and load systems//

    // persistentDataPath is the only location that is reliably writable in
    // both the editor and standalone builds (dataPath points into the
    // install/Assets folder).
    static string SavePath => Path.Combine(Application.persistentDataPath, "save.dat");

    public void Savegame()
    {
        if (bg == null || dl == null)
        {
            Debug.LogError("Savegame: missing Background or dialouge reference!");
            return;
        }
        try
        {
            // csv line: background, dialogue line, current emotion.
            // (old 2-field saves still load — extra fields are optional)
            File.WriteAllText(SavePath, bg.svbg + "," + dl.index + "," + dl.currentEmotion);
            Debug.Log("Game saved to " + SavePath);
        }
        catch (Exception e)
        {
            Debug.LogError("Savegame failed: " + e.Message);
        }
    }
    int Numbg;
    int Numline;
    public void Loadgame()
    {
        if (!File.Exists(SavePath))
        {
            Debug.LogWarning("Loadgame: no save file found at " + SavePath);
            return;
        }
        try
        {
            string[] datavalues = File.ReadAllText(SavePath).Trim().Split(',');
            if (datavalues.Length < 2)
            {
                Debug.LogError("Loadgame: save file is corrupted (expected at least bg,line).");
                return;
            }

            Numbg = int.Parse(datavalues[0]);
            Numline = int.Parse(datavalues[1]);

            bg.Changebg(Numbg);

            dl.gameObject.SetActive(true);
            dl.enabledl = true;
            dl.Setline(Numline); // Setline -> SyncBox restores speaker + mode

            // restore the persisted emotion (saved as optional 3rd field)
            if (datavalues.Length > 2)
            {
                dl.currentEmotion = int.Parse(datavalues[2]);
                dl.RestoreEmotion();
            }

            // refill the field log so the loaded run shows its full history
            if (dl.his != null) dl.his.RebuildFromLines(Numline);

            Debug.Log("Game loaded: bg " + Numbg + ", line " + Numline);
        }
        catch (Exception e)
        {
            Debug.LogError("Loadgame failed: " + e.Message);
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
