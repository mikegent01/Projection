using System.Collections.Generic;
using UnityEngine;

/// <summary>
/// Loads dialogue from plain-text files under Assets/Resources/Dialogue.
///
/// Format — one entry per line:
///
///     NAME | EMOTION | EVENT | TEXT
///
///   NAME    : speaker key, matched against DialogueBoxUI CharacterVisuals
///             ('-' or blank = no speaker)
///   EMOTION : '-' / 'keep' keeps the current emotion; neutral, embarrassed,
///             happy, sad, stoic, angry (or the raw 0..5 index) sets one
///   EVENT   : gameplay event fired when the line shows ('-' = none)
///   TEXT    : the spoken line ('-' = empty). May contain '|' — only the
///             first three separators count.
///
/// Lines starting with '#' are comments. A line starting with '@' gives the
/// NEXT entry a stable id (for events/jumps/saves). Files are concatenated
/// in the order their paths are passed to Load(), so entry indices are
/// simply: all lines of file 1, then all lines of file 2, ...
/// </summary>
public static class DialogueScript
{
    /// <summary>Load and concatenate the given Resources paths into one script.</summary>
    public static DialogueLine[] Load(IEnumerable<string> resourcePaths)
    {
        List<DialogueLine> lines = new List<DialogueLine>();

        foreach (string path in resourcePaths)
        {
            TextAsset asset = Resources.Load<TextAsset>(path);
            if (asset == null)
            {
                Debug.LogError("DialogueScript: could not find dialogue file '" + path + "' in Resources.");
                continue;
            }

            int before = lines.Count;
            Parse(asset.text, path, lines);
            Debug.Log("DialogueScript: loaded " + (lines.Count - before) + " lines from " + path);
        }

        if (lines.Count == 0)
        {
            Debug.LogError("DialogueScript: no dialogue was loaded at all!");
        }
        return lines.ToArray();
    }

    static void Parse(string content, string source, List<DialogueLine> lines)
    {
        string pendingId = string.Empty;
        string[] rawLines = content.Replace("\r\n", "\n").Split('\n');

        for (int i = 0; i < rawLines.Length; i++)
        {
            string raw = rawLines[i].Trim();

            if (raw.Length == 0 || raw.StartsWith("#")) continue;      // blank / comment
            if (raw.StartsWith("@"))                                   // @id for the next entry
            {
                pendingId = raw.Substring(1).Trim();
                continue;
            }

            // only the first three '|' separate columns — text may contain more
            string[] parts = raw.Split(new char[] { '|' }, 4);
            if (parts.Length < 4)
            {
                Debug.LogError("DialogueScript: " + source + ":" + (i + 1) +
                    " needs 4 columns (NAME | EMOTION | EVENT | TEXT), got: " + raw);
                continue;
            }

            string speaker = Clean(parts[0]);
            string emotion = Clean(parts[1]);
            string evt = Clean(parts[2]);
            string text = parts[3].Trim();
            if (text == "-") text = string.Empty;

            lines.Add(new DialogueLine(speaker, text, evt, ParseEmotion(emotion, source, i + 1), pendingId));
            pendingId = string.Empty;
        }
    }

    static string Clean(string column)
    {
        string value = column.Trim();
        return value == "-" ? string.Empty : value;
    }

    static int ParseEmotion(string raw, string source, int lineNo)
    {
        if (string.IsNullOrEmpty(raw) || raw == "keep") return -1; // persist current emotion

        int index;
        switch (raw.ToLowerInvariant())
        {
            case "neutral": index = (int)DialogueEmotion.Neutral; break;
            case "embarrassed":
            case "embaresed": index = (int)DialogueEmotion.Embarrassed; break;
            case "happy": index = (int)DialogueEmotion.Happy; break;
            case "sad": index = (int)DialogueEmotion.Sad; break;
            case "stoic": index = (int)DialogueEmotion.Stoic; break;
            case "angry": index = (int)DialogueEmotion.Angry; break;
            default:
                if (int.TryParse(raw, out index))
                {
                    break;
                }
                Debug.LogWarning("DialogueScript: " + source + ":" + lineNo +
                    " unknown emotion '" + raw + "', keeping current.");
                return -1;
        }

        if (index < 0 || index > (int)DialogueEmotion.Angry)
        {
            Debug.LogWarning("DialogueScript: " + source + ":" + lineNo +
                " emotion index " + index + " out of range, keeping current.");
            return -1;
        }
        return index;
    }
}
