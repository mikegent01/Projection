using UnityEngine;

public class Mainmenu : MonoBehaviour
{
    public Game_Master gm;
    public void Enablemenu()
    {
        gameObject.SetActive(true);
    }
    public void Begingame()
    {
        Debug.Log("Lets Play!");
        gameObject.SetActive(false);
        gm.Startchapterselect();
    }
    public void Quitgame()
    {
        Application.Quit();
    }
}
