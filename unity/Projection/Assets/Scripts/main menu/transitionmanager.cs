using System.Collections;
using Microsoft.Unity.VisualStudio.Editor;
using UnityEngine;
using UnityEngine.SceneManagement;

public class Transitionmanager : MonoBehaviour
{
    public void Fade()
    {
        StartCoroutine(Fadeoutsystem());
    }
    public void Fadein()
    {
        StartCoroutine(Fadeinsystem());
    }    
    IEnumerator Fadeoutsystem()
    {
        CanvasGroup canvas = GetComponent<CanvasGroup>();
        while (canvas.alpha > 0)
        {
            canvas.alpha -= Time.deltaTime / 6;
            yield return null;
        }
        canvas.interactable = false;
        yield return null;
    }
     IEnumerator Fadeinsystem()
    {
        CanvasGroup canvas = GetComponent<CanvasGroup>();
        while (canvas.alpha < 1)
        {
            canvas.alpha += Time.deltaTime * 6;
            yield return null;
        }
        canvas.interactable = true;
        yield return null;
    }   
}