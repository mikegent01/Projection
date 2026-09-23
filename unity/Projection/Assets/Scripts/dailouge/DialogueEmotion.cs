using UnityEngine;

/// <summary>
/// Emotions a speaker can be in while a dialogue line is shown.
///
/// The numeric values are locked to the sprite slot order already used by
/// Emotionhandler and by the emotion column in the dialogue data files
/// (see DialogueScript), so existing data keeps working:
/// 0 Neutral, 1 Embarrassed, 2 Happy, 3 Sad, 4 Stoic, 5 Angry.
/// </summary>
public enum DialogueEmotion
{
    Neutral = 0,
    Embarrassed = 1,
    Happy = 2,
    Sad = 3,
    Stoic = 4,
    Angry = 5,
}

/// <summary>
/// Central palette for the emotion-driven text box UI.
///
/// The real emotion system is not in the game yet, so for now this is a
/// small static lookup that <see cref="DialogueBoxUI"/> reads from. When
/// the gameplay emotion system lands it only has to feed an emotion into
/// DialogueBoxUI.SetEmotion(...) — or swap these defaults — and the whole
/// UI follows automatically.
///
/// The portrait panel reads as a CRT-style glow: a dark overlay sits at
/// the top of the panel and fades down into <see cref="Glow"/> at the
/// bottom (greenish glow for excitement/happiness in the reference
/// mock-up, pink for embarrassment, etc.).
/// </summary>
public static class DialogueEmotionPalette
{
    /// <summary>Emotion glow color at the bottom of the portrait panel.</summary>
    public static Color32 Glow(DialogueEmotion emotion)
    {
        switch (emotion)
        {
            case DialogueEmotion.Embarrassed: return new Color32(0xD9, 0x8A, 0xB4, 0xFF); // warm pink
            case DialogueEmotion.Happy: return new Color32(0x59, 0xC1, 0x6B, 0xFF); // bright green (excitement in the mock-up)
            case DialogueEmotion.Sad: return new Color32(0x4E, 0x6E, 0xC8, 0xFF); // cold blue
            case DialogueEmotion.Stoic: return new Color32(0x3D, 0x8E, 0x7C, 0xFF); // deep teal
            case DialogueEmotion.Angry: return new Color32(0xC2, 0x3A, 0x2E, 0xFF); // hot red
            case DialogueEmotion.Neutral:
            default: return new Color32(0x55, 0x66, 0x7A, 0xFF); // neutral slate
        }
    }

    /// <summary>Safe int -> enum conversion used by the per-line int field.</summary>
    public static DialogueEmotion FromIndex(int emotionIndex)
    {
        if (emotionIndex < 0 || emotionIndex > (int)DialogueEmotion.Angry)
        {
            Debug.LogWarning("DialogueEmotionPalette: unknown emotion index " + emotionIndex + ", falling back to Neutral.");
            return DialogueEmotion.Neutral;
        }
        return (DialogueEmotion)emotionIndex;
    }
}
