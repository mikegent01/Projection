using UnityEngine;

public class Game_Master : MonoBehaviour
{
    public bool cardget = true;
    public animation_card anicard;
    public background bg;
    public RainbowText_V1 rain;
    void Start()
    {
        gaincard();
    }
    void gaincard(){
        anicard.startcardget();
        rain.begincolor();
        bg.changebg(0);
    }
    void Update()
    {
        
    }
}
