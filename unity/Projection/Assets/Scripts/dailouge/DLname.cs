using JetBrains.Annotations;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

public class DLname : MonoBehaviour
{
    // Start is called once before the first execution of Update after the MonoBehaviour is created
    public TextMeshProUGUI text;

    public void Changetext(string textreal)
{
    text.text = textreal;
}

}
