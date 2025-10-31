using System.Runtime.CompilerServices;
using UnityEngine;
using UnityEngine.Rendering.Universal;
using System.Collections;
using Unity.VisualScripting;

public class S_Camera : MonoBehaviour
{

    public void Zooomout()
    {
        StopAllCoroutines();
        StartCoroutine(Zoomout());
    }
    public void Zooomin()
    {
        StopAllCoroutines();
        StartCoroutine(Zoomin());
    }
    IEnumerator Zoomin()
    {
        PixelPerfectCamera Pixel = GetComponent<PixelPerfectCamera>();

        while (Pixel.assetsPPU != 4000){
            Pixel.assetsPPU += 1;
            yield return null;
        }
    }
    IEnumerator Zoomout()
    {
        PixelPerfectCamera Pixel = GetComponent<PixelPerfectCamera>();

        while (Pixel.assetsPPU > 100)
        {
            Debug.Log("Zooming time");
            Pixel.assetsPPU -= 1;
            yield return null;
        }
        while (Pixel.assetsPPU > 100)
        {
            Pixel.assetsPPU = 100;
            yield return null;
        }        
    }

}
