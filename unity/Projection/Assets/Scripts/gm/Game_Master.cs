using UnityEngine;

public class Game_Master : MonoBehaviour
{
    public bool cardget = true;
    public animation_card anicard;
    public background bg;
    public RainbowText_V1 rain;
    public mainmenu mm;
    void Start()
    {
       //  gaincard();
        startgame();
    }
    void startgame()
    {
        // this starts the game call this first always :D
        bg.changebg(1);
        rain.gameObject.SetActive(true);
        rain.changetext("Projection");
        mm.gameObject.SetActive(true);
    }
    void gaincard(){ // no idea when this will be used 
        anicard.startcardget();
        rain.begincolor();
        bg.changebg(0);
    }
    void Update()
    {
        
    }
}
