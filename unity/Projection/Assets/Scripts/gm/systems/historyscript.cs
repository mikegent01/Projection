using System.Collections;
using TMPro;
using Unity.Collections;
using UnityEngine;

public class historyscript : MonoBehaviour
{
    public dialouge dl;
    public TMP_Text Mtext;
    // Start is called once before the first execution of Update after the MonoBehaviour is created
    void Start()
    {
        gameObject.SetActive(false);
    }

    // Update is called once per frame
    void Enable()
    {
        gameObject.SetActive(true);
    }
    public void Populate(int cdln)
    {
        cdln =+ cdln+1;
        StartCoroutine(Populatehistory(cdln));

    }

    IEnumerator Populatehistory(int cdln)
    {
    string aggregateText = "";
    for (int index = 5; index < cdln; index++) {
        aggregateText += "\n"+ dl.lines[index].name  +" | "+ dl.lines[index].lineofd+"\n"; // Extra addition to put a space between elements
    }
    Mtext.text = aggregateText;
        yield return null;
    }
}
