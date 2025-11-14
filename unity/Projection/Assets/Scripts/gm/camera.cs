using System.Runtime.CompilerServices;
using UnityEngine;
using UnityEngine.Rendering.Universal;
using System.Collections;
using Unity.VisualScripting;
public class S_Camera : MonoBehaviour
{
    public Game_Master gm;

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

        while (Pixel.assetsPPU < 2000)
        {
            Pixel.assetsPPU += 1;
            yield return null;
        }
        StartCoroutine(Correctzoomin());

    }
    IEnumerator Correctzoomin()
    {
        PixelPerfectCamera Pixel = GetComponent<PixelPerfectCamera>();
        if (gm.chapternum == 0)
        {
            Pixel.assetsPPU = 4000;
            StopAllCoroutines();
            gm.Chp0();
            yield return null;
        }       
             
    }
    IEnumerator Zoomout()
    {
        PixelPerfectCamera Pixel = GetComponent<PixelPerfectCamera>();

        while (Pixel.assetsPPU < 101)
        {
            Debug.Log("Zooming time");
            Pixel.assetsPPU -= 1;
            yield return null;
        }

    }
    IEnumerator Correctzoomout()
    {
        PixelPerfectCamera Pixel = GetComponent<PixelPerfectCamera>();
        while (Pixel.assetsPPU > 101)
        {
            Pixel.assetsPPU = 101;
            yield return null;
        }           
    }

}
