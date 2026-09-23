using System;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

/// <summary>
/// Builds and drives the visual-novel style text box at the bottom of the
/// screen, matching the reference mock-up:
///
///   +------------------+  +----------------------------------------+
///   | NAME   (plate)   |  |                                        |
///   |                  |  |   dialogue text                        |
///   |   portrait on    |  |                                        |
///   |   emotion glow   |  |                                        |
///   +------------------+  +----------------------------------------+
///                (anchored to the bottom of the screen)
///
/// Everything is variable-driven:
///  * SetSpeaker(...) swaps the nameplate text/color and the portrait
///    based on the CharacterVisual entries below.
///  * SetEmotion(...) re-tints the portrait background gradient. The real
///    gameplay emotion system is not in the game yet, so this component
///    only talks to DialogueEmotion / DialogueEmotionPalette — plug the
///    future system into SetEmotion and the UI follows.
///
/// The layout itself is generated in Awake() from the serialized values
/// below; the existing name/body TextMeshPro objects are re-parented into
/// the new layout so old scene wiring keeps working. The legacy Save /
/// Load / History buttons are restyled into small chips above the panel.
/// </summary>
[RequireComponent(typeof(RectTransform))]
public class DialogueBoxUI : MonoBehaviour
{
    [Serializable]
    public class CharacterVisual
    {
        [Tooltip("Speaker key, matched case-insensitively against the line's name field.")]
        public string key;
        [Tooltip("Text shown on the nameplate.")]
        public string displayName;
        [Tooltip("Color of the nameplate text while this character speaks.")]
        public Color nameColor = Color.white;
        [Tooltip("Portraits per DialogueEmotion (array index = emotion value). Missing entries fall back to index 0; an empty array keeps the previous portrait.")]
        public Sprite[] emotionPortraits = new Sprite[0];
    }

    [Header("Existing text (re-styled & re-parented into the new layout)")]
    public TextMeshProUGUI nameText;
    public TextMeshProUGUI bodyText;

    [Header("Speakers (change nameplate / portrait from these variables)")]
    public CharacterVisual[] characters = new CharacterVisual[0];

    [Header("Layout")]
    [SerializeField] float panelHeight = 252f;
    [SerializeField] float sideMargin = 28f;
    [SerializeField] float bottomMargin = 26f;
    [SerializeField] float leftPanelWidth = 288f;
    [SerializeField] float panelGap = 16f;
    [SerializeField] float nameplateHeight = 52f;
    [SerializeField] float accentHeight = 4f;
    [SerializeField] float portraitSidePadding = 18f;
    [SerializeField] float portraitTopPadding = 6f;
    [SerializeField] float nameFontSize = 34f;
    [SerializeField] float bodyFontSize = 32f;

    [Header("Colors (sampled from the reference mock-up)")]
    [SerializeField] Color32 leftPanelColor = new Color32(0x0B, 0x0C, 0x12, 0xFF);
    [SerializeField] Color32 textPanelColor = new Color32(0x26, 0x26, 0x2C, 0xFF);
    [SerializeField] Color32 nameplateColor = new Color32(0x07, 0x08, 0x0C, 0xFF);
    [SerializeField] Color32 accentColor = new Color32(0x83, 0xC8, 0xDE, 0xFF);
    [SerializeField] Color32 bodyTextColor = new Color32(0xF0, 0xF0, 0xF0, 0xFF);
    [SerializeField] Color32 shadeOverlayColor = new Color32(0x12, 0x16, 0x20, 0xFA);
    [SerializeField] Color32 chipColor = new Color32(0x0C, 0x0D, 0x12, 0xF2);
    [SerializeField] Color32 chipTextColor = new Color32(0xC9, 0xD1, 0xD9, 0xFF);

    [Header("Motion")]
    [Tooltip("How fast the emotion background color blends toward its target.")]
    public float colorFadeSpeed = 6f;

    // generated runtime pieces
    RectTransform root;
    Image glowImage;      // emotion-tinted glow at the bottom of the portrait area
    Image shadeImage;     // dark fade on top of the glow
    RectTransform portraitRT;
    Image portraitImage;
    CharacterVisual activeCharacter;
    DialogueEmotion activeEmotion = DialogueEmotion.Neutral;
    Color targetGlow;
    Sprite fadeSprite;
    Texture2D fadeTexture;

    void Awake()
    {
        BuildLayout();
        // snap to neutral so the first frame has no color pop
        targetGlow = DialogueEmotionPalette.Glow(DialogueEmotion.Neutral);
        if (glowImage != null) glowImage.color = targetGlow;
        RefreshPortrait();
    }

    void Update()
    {
        if (glowImage != null && colorFadeSpeed > 0f)
        {
            glowImage.color = Color.Lerp(glowImage.color, targetGlow, Time.deltaTime * colorFadeSpeed);
        }
    }

    void OnDestroy()
    {
        if (fadeSprite != null) Destroy(fadeSprite);
        if (fadeTexture != null) Destroy(fadeTexture);
    }

    // ---------------------------------------------------------------- API

    /// <summary>Swap nameplate + portrait for the given speaker key.</summary>
    public void SetSpeaker(string key)
    {
        activeCharacter = FindCharacter(key);

        if (nameText != null)
        {
            nameText.text = activeCharacter != null ? activeCharacter.displayName : (key ?? string.Empty);
            if (activeCharacter != null) nameText.color = activeCharacter.nameColor;
        }
        RefreshPortrait();
    }

    /// <summary>Re-tint the portrait background from a per-line emotion index.</summary>
    public void SetEmotion(int emotionIndex)
    {
        SetEmotion(DialogueEmotionPalette.FromIndex(emotionIndex));
    }

    /// <summary>Re-tint the portrait background (entry point for the future emotion system).</summary>
    public void SetEmotion(DialogueEmotion emotion)
    {
        activeEmotion = emotion;
        targetGlow = DialogueEmotionPalette.Glow(emotion);
        RefreshPortrait();
    }

    /// <summary>Convenience: set speaker + emotion in one call.</summary>
    public void Apply(string speaker, int emotionIndex)
    {
        SetSpeaker(speaker);
        SetEmotion(emotionIndex);
    }

    // ------------------------------------------------------------- lookup

    CharacterVisual FindCharacter(string key)
    {
        if (string.IsNullOrEmpty(key)) return null;
        string cleaned = key.Trim();
        foreach (CharacterVisual c in characters)
        {
            if (c != null && string.Equals(c.key, cleaned, StringComparison.OrdinalIgnoreCase))
                return c;
        }
        return null;
    }

    void RefreshPortrait()
    {
        if (portraitImage == null) return;

        Sprite sprite = null;
        if (activeCharacter != null && activeCharacter.emotionPortraits != null && activeCharacter.emotionPortraits.Length > 0)
        {
            int i = Mathf.Clamp((int)activeEmotion, 0, activeCharacter.emotionPortraits.Length - 1);
            sprite = activeCharacter.emotionPortraits[i];
            if (sprite == null) sprite = activeCharacter.emotionPortraits[0];
        }

        portraitImage.gameObject.SetActive(sprite != null);
        portraitImage.sprite = sprite;

        if (sprite != null && portraitRT != null)
        {
            // Bust framing like the mock-up: fill the panel width and anchor
            // to the top so the head/shoulders show; the mask crops the body.
            float w = Mathf.Max(1f, leftPanelWidth - portraitSidePadding * 2f);
            Rect srect = sprite.rect;
            float aspect = srect.width > 0f ? srect.height / srect.width : 1f;
            portraitRT.sizeDelta = new Vector2(w, w * aspect);
            portraitRT.anchoredPosition = new Vector2(0f, -portraitTopPadding);
        }
    }

    // ------------------------------------------------------------- layout

    void BuildLayout()
    {
        root = (RectTransform)transform;

        // Anchor the box to the bottom of the (real) canvas rect. The legacy
        // parent ("Essential") is a plain Transform, so reparent to the root
        // canvas for predictable anchoring — visibility is toggled on this
        // GameObject itself, so this does not change menu behavior.
        Canvas canvas = GetComponentInParent<Canvas>();
        if (canvas != null && transform.parent != canvas.transform)
        {
            Transform fx = canvas.transform.Find("FX");
            transform.SetParent(canvas.transform, false);
            if (fx != null) transform.SetSiblingIndex(fx.GetSiblingIndex()); // keep fade/FX on top
            else transform.SetAsLastSibling();
        }

        root.anchorMin = new Vector2(0f, 0f);
        root.anchorMax = new Vector2(1f, 0f);
        root.pivot = new Vector2(0.5f, 0f);
        root.anchoredPosition = new Vector2(0f, bottomMargin);
        root.sizeDelta = new Vector2(-sideMargin * 2f, panelHeight);

        // The legacy background image becomes invisible (the two dark panels
        // replace it) but keeps its raycast behavior so click handling is
        // unchanged.
        Image legacyBg = GetComponent<Image>();
        if (legacyBg != null)
        {
            Color c = legacyBg.color;
            legacyBg.color = new Color(c.r, c.g, c.b, 0f);
        }

        // Left panel: nameplate on top, portrait on emotion gradient below.
        RectTransform leftPanel = MakePanel("Character Panel", root, leftPanelColor);
        Stretch(leftPanel, 0f, 0f, 0f, 1f);
        leftPanel.pivot = new Vector2(0f, 0.5f);
        leftPanel.anchoredPosition = Vector2.zero;
        leftPanel.sizeDelta = new Vector2(leftPanelWidth, 0f);

        MakeAccent(leftPanel, "Top Accent");

        RectTransform nameplate = MakePanel("Nameplate", leftPanel, nameplateColor);
        nameplate.anchorMin = new Vector2(0f, 1f);
        nameplate.anchorMax = new Vector2(1f, 1f);
        nameplate.pivot = new Vector2(0.5f, 1f);
        nameplate.offsetMin = new Vector2(0f, -(accentHeight + nameplateHeight));
        nameplate.offsetMax = new Vector2(0f, -accentHeight);

        RectTransform portraitArea = MakeRect("Portrait Area", leftPanel);
        portraitArea.anchorMin = new Vector2(0f, 0f);
        portraitArea.anchorMax = new Vector2(1f, 1f);
        portraitArea.pivot = new Vector2(0.5f, 0.5f);
        portraitArea.offsetMin = Vector2.zero;
        portraitArea.offsetMax = new Vector2(0f, -(accentHeight + nameplateHeight));
        portraitArea.gameObject.AddComponent<RectMask2D>();

        glowImage = MakeImage("Emotion Glow", portraitArea, DialogueEmotionPalette.Glow(DialogueEmotion.Neutral));
        Stretch((RectTransform)glowImage.transform, 0f, 0f, 1f, 1f);

        shadeImage = MakeImage("Top Shade", portraitArea, shadeOverlayColor);
        Stretch((RectTransform)shadeImage.transform, 0f, 0f, 1f, 1f);
        shadeImage.sprite = GetFadeSprite();

        portraitRT = MakeRect("Portrait", portraitArea);
        portraitRT.anchorMin = new Vector2(0.5f, 1f);
        portraitRT.anchorMax = new Vector2(0.5f, 1f);
        portraitRT.pivot = new Vector2(0.5f, 1f);
        portraitImage = portraitRT.gameObject.AddComponent<Image>();
        portraitImage.raycastTarget = false;

        // Right panel: the dialogue text itself.
        RectTransform textPanel = MakePanel("Text Panel", root, textPanelColor);
        textPanel.anchorMin = new Vector2(0f, 0f);
        textPanel.anchorMax = new Vector2(1f, 1f);
        textPanel.pivot = new Vector2(0.5f, 0.5f);
        textPanel.offsetMin = new Vector2(leftPanelWidth + panelGap, 0f);
        textPanel.offsetMax = Vector2.zero;

        MakeAccent(textPanel, "Top Accent");

        // Re-parent + restyle the existing text objects so old scene wiring
        // (dialouge.text / dialouge.nametext / DLname) keeps working.
        if (nameText != null)
        {
            RectTransform rt = (RectTransform)nameText.transform;
            rt.SetParent(nameplate, false);
            Stretch(rt, 0f, 0f, 1f, 1f);
            rt.offsetMin = new Vector2(16f, 4f);
            rt.offsetMax = new Vector2(-8f, -6f);
            nameText.alignment = TextAlignmentOptions.Left;
            nameText.fontSize = nameFontSize;
            nameText.fontStyle = FontStyles.Bold;
            nameText.raycastTarget = false;
            nameText.margin = Vector4.zero;
        }

        if (bodyText != null)
        {
            RectTransform rt = (RectTransform)bodyText.transform;
            rt.SetParent(textPanel, false);
            Stretch(rt, 0f, 0f, 1f, 1f);
            rt.offsetMin = new Vector2(24f, 16f);
            rt.offsetMax = new Vector2(-24f, -16f);
            bodyText.alignment = TextAlignmentOptions.TopLeft;
            bodyText.fontSize = bodyFontSize;
            bodyText.color = bodyTextColor;
            bodyText.raycastTarget = false;
            bodyText.margin = Vector4.zero;
        }

        RestyleLegacyButton("History", 0);
        RestyleLegacyButton("Load", 1);
        RestyleLegacyButton("Save", 2);
    }

    void RestyleLegacyButton(string childName, int slot)
    {
        Transform button = transform.Find(childName);
        if (button == null) return;

        const float chipWidth = 96f;
        const float chipHeight = 30f;
        const float chipGap = 10f;
        const float chipRise = 12f;

        RectTransform rt = (RectTransform)button;
        rt.anchorMin = new Vector2(1f, 1f);
        rt.anchorMax = new Vector2(1f, 1f);
        rt.pivot = new Vector2(1f, 0f);
        rt.sizeDelta = new Vector2(chipWidth, chipHeight);
        // anchored to the root's top-right corner -> chips float just above the panel
        rt.anchoredPosition = new Vector2(-(chipGap + (chipWidth + chipGap) * slot), chipRise);

        Image bg = button.GetComponent<Image>();
        if (bg != null) bg.color = chipColor;

        TextMeshProUGUI label = button.GetComponentInChildren<TextMeshProUGUI>(true);
        if (label != null)
        {
            label.color = chipTextColor;
            label.fontSize = 20f;
            label.alignment = TextAlignmentOptions.Center;
            RectTransform lrt = (RectTransform)label.transform;
            Stretch(lrt, 0f, 0f, 1f, 1f);
            lrt.offsetMin = Vector2.zero;
            lrt.offsetMax = Vector2.zero;
        }

        button.SetAsLastSibling(); // keep chips clickable above the panels
    }

    // ----------------------------------------------------------- helpers

    RectTransform MakeRect(string name, Transform parent)
    {
        var go = new GameObject(name, typeof(RectTransform));
        RectTransform rt = (RectTransform)go.transform;
        rt.SetParent(parent, false);
        return rt;
    }

    Image MakeImage(string name, Transform parent, Color32 color)
    {
        RectTransform rt = MakeRect(name, parent);
        Image img = rt.gameObject.AddComponent<Image>();
        img.color = color;
        img.raycastTarget = false;
        return img;
    }

    RectTransform MakePanel(string name, Transform parent, Color32 color)
    {
        return (RectTransform)MakeImage(name, parent, color).transform;
    }

    Image MakeAccent(RectTransform panel, string name)
    {
        Image accent = MakeImage(name, panel, accentColor);
        RectTransform rt = (RectTransform)accent.transform;
        rt.anchorMin = new Vector2(0f, 1f);
        rt.anchorMax = new Vector2(1f, 1f);
        rt.pivot = new Vector2(0.5f, 1f);
        rt.offsetMin = new Vector2(0f, -accentHeight);
        rt.offsetMax = Vector2.zero;
        return accent;
    }

    static void Stretch(RectTransform rt, float minX, float minY, float maxX, float maxY)
    {
        rt.anchorMin = new Vector2(minX, minY);
        rt.anchorMax = new Vector2(maxX, maxY);
        rt.offsetMin = Vector2.zero;
        rt.offsetMax = Vector2.zero;
    }

    Sprite GetFadeSprite()
    {
        if (fadeSprite != null) return fadeSprite;

        // Vertical alpha falloff (opaque top -> transparent bottom). Tinted
        // by shadeImage.color, giving the emotion glow a dark upper fade.
        const int h = 64;
        fadeTexture = new Texture2D(1, h, TextureFormat.RGBA32, false);
        fadeTexture.wrapMode = TextureWrapMode.Clamp;
        fadeTexture.filterMode = FilterMode.Bilinear;
        for (int y = 0; y < h; y++)
        {
            float t = y / (float)(h - 1); // 0 at bottom -> 1 at top
            fadeTexture.SetPixel(0, y, new Color(1f, 1f, 1f, t));
        }
        fadeTexture.Apply();
        fadeSprite = Sprite.Create(fadeTexture, new Rect(0, 0, 1, h), new Vector2(0.5f, 0.5f), 100f);
        return fadeSprite;
    }
}
