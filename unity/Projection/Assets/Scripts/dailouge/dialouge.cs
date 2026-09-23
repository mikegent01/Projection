using UnityEngine;
using TMPro;
using System.Collections;

/// <summary>
/// Dialogue runner: plays back a loaded DialogueScript.
///
/// Content lives in plain-text/JSON files under Assets/Resources/Dialogue
/// (see DialogueScript for the format) — this class only runs it:
/// typewriter, speaker/nameplate sync (DialogueBoxUI), emotion bridging,
/// event dispatch, history recording, auto-forward, and skip actions.
/// Public surface kept stable for Game_Master / InputHandler / buttons:
/// Dlsetup, NextLinePhaser, Setline, Previousline, SkipLine, ToggleAuto,
/// Populatehistory, RestoreEmotion, index, enabledl.
/// </summary>
public class dialouge : MonoBehaviour
{
    [Header("Wiring")]
    public TextMeshProUGUI text;
    public TextMeshProUGUI nametext;
    public historyscript his;
    public Game_Master gm;
    public objhist objhist;
    public Emotionhandler emohan;
    public DLname dl;
    public DialogueBoxUI box;

    [Header("Script (Resources paths, loaded in order -> stable line indices)")]
    [SerializeField] string[] scriptFiles = { "Dialogue/chapter_select", "Dialogue/ch0" };

    [Header("Playback")]
    public float textspeed;
    public bool enabledl;
    public int index;

    /// <summary>
    /// The emotion the dialogue is currently sitting in. Persists across
    /// lines until a line with an explicit (>= 0) emotion changes it.
    /// </summary>
    public int currentEmotion = 0;

    DialogueLine[] lines = new DialogueLine[0];

    /// <summary>The loaded script (chapter select previews first, then chapters in order).</summary>
    public DialogueLine[] Lines => lines;

    /// <summary>Number of loaded lines (0 before Start / when no files were found).</summary>
    public int LineCount => lines.Length;

    /// <summary>Auto-forward playback state.</summary>
    public bool isAuto = false;
    Coroutine autoRoutine = null;

    void Start()
    {
        if (textspeed <= 0f) textspeed = 0.1f; // safety default (scene normally sets 0.1)
        lines = DialogueScript.Load(scriptFiles);
        SyncBox(index);
    }

    // ------------------------------------------------------------- playback

    /// <summary>Reset to the first line and start typing (chapter select entry point).</summary>
    public void Dlsetup()
    {
        text.text = string.Empty;
        Startdialouge();
        enabledl = false;
    }

    /// <summary>Advance entry point used by InputHandler: emotion hook, then event/advance.</summary>
    public void NextLinePhaser()
    {
        Checknextlineemotion();
        Checknextlineevent();
    }

    void Startdialouge()
    {
        index = 0;
        SyncBox(index);
        StartCoroutine(Typeline());
    }

    /// <summary>Skip / complete the current line (legacy low-level advance helper).</summary>
    public void Nextline()
    {
        if (index < 0 || index >= lines.Length) return;
        StopAllCoroutines();
        text.text = lines[index].Text;
    }

    /// <summary>
    /// Skip action: if the typewriter is still animating, completes the text immediately;
    /// if the text is already finished typing, advances to the next line.
    /// </summary>
    public void SkipLine()
    {
        if (index < 0 || index >= lines.Length) return;
        if (text != null && text.text != lines[index].Text)
        {
            StopAllCoroutines();
            text.text = lines[index].Text;
        }
        else
        {
            NextLinePhaser();
        }
    }

    /// <summary>Toggles auto-forward dialogue playback mode.</summary>
    public void ToggleAuto()
    {
        isAuto = !isAuto;
        if (isAuto)
        {
            if (autoRoutine != null) StopCoroutine(autoRoutine);
            autoRoutine = StartCoroutine(AutoPlayRoutine());
        }
        else
        {
            if (autoRoutine != null) StopCoroutine(autoRoutine);
            autoRoutine = null;
        }
    }

    IEnumerator AutoPlayRoutine()
    {
        while (isAuto)
        {
            if (index >= 0 && index < lines.Length)
            {
                // Wait until current line finishes typing
                while (text != null && text.text != lines[index].Text)
                {
                    yield return new WaitForSeconds(0.1f);
                }
                // Pause to let player read
                yield return new WaitForSeconds(1.8f);
                if (isAuto && enabledl)
                {
                    NextLinePhaser();
                }
            }
            else
            {
                yield break;
            }
        }
    }

    void NextLine()
    {
        StopAllCoroutines();
        if (index < lines.Length - 2)
        {
            index++;
            text.text = string.Empty;
            SyncBox(index);
            StartCoroutine(Typeline());
        }
        else
        {
            Debug.Log("End of script!");
            gameObject.SetActive(false);
        }
    }

    public void Setline(int line)
    {
        if (lines.Length == 0) return;
        index = Mathf.Clamp(line, 0, lines.Length - 1);
        dl.Changetext(lines[index].SpeakerName);
        StopAllCoroutines();
        text.text = string.Empty;
        SyncBox(index);
        StartCoroutine(Typeline());
    }

    /// <summary>Jump to the line tagged with an @id in the data files.</summary>
    public void SetlineById(string id)
    {
        for (int i = 0; i < lines.Length; i++)
        {
            if (lines[i].Id == id)
            {
                Setline(i);
                return;
            }
        }
        Debug.LogWarning("SetlineById: no line tagged '@" + id + "'.");
    }

    public void Previousline()
    {
        if (index > 0)
        {
            index--;
            StopAllCoroutines();
            text.text = string.Empty;
            SyncBox(index);
            StartCoroutine(Typeline());
        }
        else
        {
            gameObject.SetActive(false);
        }
    }

    IEnumerator Typeline()
    {
        if (index < 0 || index >= lines.Length) yield break;
        foreach (char c in lines[index].Text.ToCharArray())
        {
            text.text += c;
            yield return new WaitForSeconds(textspeed);
        }
    }

    // --------------------------------------------------------- line effects

    void Checknextlineemotion()
    {
        if (index < 0 || index >= lines.Length) return;
        if (lines[index].Emotion < 0)
        {
            Debug.Log(index + " Next Line dosen't have an emotion!");
        }
        else
        {
            Debug.Log(index + " has an emotion!");
            StopAllCoroutines();
            emohan.ChangeSprite(lines[index].Emotion);
        }
    }

    void Checknextlineevent()
    {
        if (index < 0 || index >= lines.Length)
        {
            Debug.Log("Dialogue finished / no script loaded.");
            gameObject.SetActive(false);
            return;
        }

        if (string.IsNullOrEmpty(lines[index].EventName))
        {
            Debug.Log(index + " Next Line dosen't have an event!");
            StopAllCoroutines();
            if (index + 1 < lines.Length)
            {
                dl.Changetext(lines[index + 1].SpeakerName);
            }
            NextLine();
        }
        else
        {
            Debug.Log(index + " has an event!");
            StopAllCoroutines();
            gm.Handleevents(lines[index].EventName);
            NextLine();
        }
    }

    // ------------------------------------------------------------ UI / sync

    /// <summary>
    /// Pushes the current line's speaker + mode into the text box UI and
    /// records the line into the field log. The emotion only updates when
    /// the line carries an explicit one (>= 0) — otherwise it persists
    /// instead of snapping back to neutral. Safe with no DialogueBoxUI.
    /// </summary>
    void SyncBox(int i)
    {
        if (box == null) box = GetComponent<DialogueBoxUI>();
        if (lines == null || i < 0 || i >= lines.Length) return;

        string speaker = lines[i].SpeakerName;

        // Layout follows the game state, not the speaker name: everything
        // while browsing the chapter select screen is an announcement
        // (some previews are spoken lines and must NOT flip the layout).
        bool chapterSelect = gm != null && !gm.gameactive;

        if (box != null)
        {
            box.SetChapterSelectMode(chapterSelect);
            box.SetSpeaker(speaker);
        }

        // only real dialogue is logged (chapter select previews are not)
        if (!chapterSelect && his != null && !string.IsNullOrEmpty(lines[i].Text))
            his.Record(speaker, lines[i].Text, i);

        if (lines[i].Emotion >= 0)
        {
            currentEmotion = lines[i].Emotion;
            if (box != null) box.SetEmotion(currentEmotion);
        }
    }

    /// <summary>Re-applies currentEmotion to the portrait + background (used by save/load).</summary>
    public void RestoreEmotion()
    {
        if (box == null) box = GetComponent<DialogueBoxUI>();
        if (box != null && currentEmotion >= 0) box.SetEmotion(currentEmotion);
        if (emohan != null && currentEmotion >= 0) emohan.ChangeSprite(currentEmotion);
    }

    /// <summary>Opens/closes the FIELD LOG overlay (wired to the LOG chip).</summary>
    public void Populatehistory()
    {
        if (his != null)
        {
            his.Toggle();
        }
    }
}
