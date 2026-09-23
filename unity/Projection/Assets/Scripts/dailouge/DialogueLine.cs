using UnityEngine;

/// <summary>
/// One line of dialogue, loaded from a data file (see DialogueScript).
/// Runtime container — not a Unity asset, not serialized in scenes.
/// Replaces the old hardcoded Dialougesystem entries.
/// </summary>
public class DialogueLine
{
    /// <summary>Speaker key (may be empty). Matched against DialogueBoxUI CharacterVisuals.</summary>
    public string SpeakerName;

    /// <summary>The spoken text (may be empty).</summary>
    public string Text;

    /// <summary>Optional gameplay event fired when this line shows (may be empty).</summary>
    public string EventName;

    /// <summary>
    /// -1 = keep the current emotion (they persist until changed);
    /// 0..5 = DialogueEmotion values that explicitly set the mood.
    /// </summary>
    public int Emotion;

    /// <summary>Optional stable id from an @tag in the data file (for jumps/saves).</summary>
    public string Id;

    public DialogueLine(string speakerName, string text, string eventName, int emotion, string id)
    {
        SpeakerName = speakerName ?? string.Empty;
        Text = text ?? string.Empty;
        EventName = eventName ?? string.Empty;
        Emotion = emotion;
        Id = id ?? string.Empty;
    }

    public override string ToString()
    {
        return "[" + (string.IsNullOrEmpty(SpeakerName) ? "?" : SpeakerName) + "] " + Text;
    }
}
