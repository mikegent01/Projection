using UnityEngine;
using System.Collections;

public class Musicvolcontrol : MonoBehaviour
{
 public IEnumerator Fadeoutvol2()
    {
        AudioSource ais = GetComponent<AudioSource>();
        while (ais.volume > 0)
        {
            
            ais.volume -= Time.deltaTime / 2;
            yield return null;
        }
    }
    public IEnumerator Fadeinvol2()
    {
        AudioSource ais = GetComponent<AudioSource>();
        while (ais.volume < 1)
        {
            ais.volume += Time.deltaTime / 2;
            yield return null;
        }
    }   
}
