using System;
using System.Collections.Generic;
using UnityEngine;

/// <summary>
/// Loads dialogue from JSON files under Assets/Resources/Dialogue.
///
/// A file is one object with a "lines" array — human readable and machine
/// readable, editable in any text editor:
///
/// {
///   "lines": [
///     { "id": "", "speaker": "Ben", "emotion": "keep", "eventName": "", "text": "When the giant wakes..." },
///     { "id": "", "speaker": "Ben", "emotion": "keep", "eventName": "explosiveentrance", "text": "..." }
///   ]
/// }
///
/// Fields:
///   id        : optional stable id, usable for jumps (SetlineById)
///   speaker   : key matched against DialogueBoxUI CharacterVisuals ("" = none)
///   emotion   : "keep" leaves the current mood alone (emotions persist
///               until changed); neutral, embarrassed, happy, sad, stoic,
///               angry (or the raw "0".."5" index) set an explicit one
///   eventName : gameplay event fired when the line shows ("" = none)
///   text      : the spoken line ("" = empty)
///
/// Files are concatenated in the order their paths are passed to Load(),
/// so entry indices are simply: all lines of file 1, then file 2, ...
/// </summary>
public static class DialogueScript
{
    [Serializable]
    public class EntryData
    {
        public string id = "";
        public string speaker = "";
        public string emotion = "keep";
        public string eventName = "";
        public string text = "";
    }

    [Serializable]
    public class FileData
    {
        public EntryData[] lines = new EntryData[0];
    }

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

            FileData data = null;
            try
            {
                data = JsonUtility.FromJson<FileData>(asset.text);
            }
            catch (Exception e)
            {
                Debug.LogError("DialogueScript: " + path + " is not valid JSON: " + e.Message);
                continue;
            }
            if (data == null || data.lines == null)
            {
                Debug.LogError("DialogueScript: " + path + " must contain an object with a \"lines\" array.");
                continue;
            }

            for (int i = 0; i < data.lines.Length; i++)
            {
                EntryData e = data.lines[i];
                if (e == null) continue;
                lines.Add(new DialogueLine(
                    e.speaker,
                    e.text,
                    e.eventName,
                    ParseEmotion(e.emotion, path, i + 1),
                    e.id));
            }
            Debug.Log("DialogueScript: loaded " + data.lines.Length + " lines from " + path);
        }

        if (lines.Count == 0)
        {
            Debug.LogError("DialogueScript: no dialogue was loaded at all!");
        }
        return lines.ToArray();
    }

    static int ParseEmotion(string raw, string source, int entryNo)
    {
        if (string.IsNullOrEmpty(raw) || raw == "-") raw = "keep";
        string key = raw.Trim().ToLowerInvariant();

        int index;
        switch (key)
        {
            case "keep": return -1; // persist current emotion
            case "neutral": index = (int)DialogueEmotion.Neutral; break;
            case "embarrassed":
            case "embaresed": index = (int)DialogueEmotion.Embarrassed; break;
            case "happy": index = (int)DialogueEmotion.Happy; break;
            case "sad": index = (int)DialogueEmotion.Sad; break;
            case "stoic": index = (int)DialogueEmotion.Stoic; break;
            case "angry": index = (int)DialogueEmotion.Angry; break;
            default:
                if (int.TryParse(key, out index))
                {
                    break;
                }
                Debug.LogWarning("DialogueScript: " + source + " entry " + entryNo +
                    " has unknown emotion '" + raw + "', keeping current.");
                return -1;
        }

        if (index < 0 || index > (int)DialogueEmotion.Angry)
        {
            Debug.LogWarning("DialogueScript: " + source + " entry " + entryNo +
                " emotion index " + index + " out of range, keeping current.");
            return -1;
        }
        return index;
    }
}
