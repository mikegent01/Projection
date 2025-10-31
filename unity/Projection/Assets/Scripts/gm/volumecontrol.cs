using UnityEngine;
using System.Collections;

public class Volumecontrol : MonoBehaviour
{
    public IEnumerator Fadeoutvol()
    {
        AudioSource ais = GetComponent<AudioSource>();
        while (ais.volume > 0)
        {
            ais.volume -= 2;
            yield return null;
        }
    }
    public IEnumerator Fadeinvol()
    {
        AudioSource ais = GetComponent<AudioSource>();
        while (ais.volume < 1)
        {
            ais.volume += 2;
            yield return null;
        }
    }   
}
