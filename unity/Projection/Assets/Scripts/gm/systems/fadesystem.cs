using System.Collections;
using Microsoft.Unity.VisualStudio.Editor;
using UnityEngine;

public class Fadesystem : MonoBehaviour
{
    public void Awake()
    {
        gameObject.SetActive(false);
    }
    public void Lightfade()
    {
        gameObject.SetActive(true);
        StartCoroutine(Lightbackgroundfade());
    }
    public IEnumerator Lightbackgroundfade()
    {
        CanvasGroup Fdi = GetComponent<CanvasGroup>();
        Fdi.alpha = 0;
        while (Fdi.alpha < 1)
        {
            Fdi.alpha += 0.001f;
            yield return null;
        }
    }
}
