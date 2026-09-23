using System.Collections;
using System.Text;
using TMPro;
using Unity.Collections;
using UnityEngine;

public class historyscript : MonoBehaviour
{
    public dialouge dl;
    public TMP_Text Mtext;

    // Lines before this index belong to the chapter select intro and are
    // not shown in the dialogue history.
    [SerializeField] int firstHistoryLine = 5;

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

    public void Populate(int currentLine)
    {
        StopAllCoroutines();
        StartCoroutine(Populatehistory(currentLine));
    }

    IEnumerator Populatehistory(int currentLine)
    {
        if (dl == null || Mtext == null || dl.lines == null)
        {
            Debug.LogWarning("historyscript: missing references, cannot populate history.");
            yield break;
        }

        // include the line currently on screen, clamped into the array
        int lastLine = Mathf.Clamp(currentLine + 1, firstHistoryLine, dl.lines.Length);

        StringBuilder aggregateText = new StringBuilder();
        for (int index = firstHistoryLine; index < lastLine; index++)
        {
            // skip empty filler lines so the log stays readable
            if (string.IsNullOrEmpty(dl.lines[index].lineofd)) continue;

            string speaker = string.IsNullOrEmpty(dl.lines[index].name) ? "???" : dl.lines[index].name;
            aggregateText.Append("\n").Append(speaker).Append(" | ").Append(dl.lines[index].lineofd).Append("\n");
        }
        Mtext.text = aggregateText.ToString();
        yield return null;
    }
}
