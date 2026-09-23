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

    [Header("Game flow (wired for the chapter select nav chips)")]
    public Game_Master gm;

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

    [Header("Military theme (see MilitaryGUI)")]
    [SerializeField] Color32 leftPanelColor = new Color32(0x1B, 0x1E, 0x16, 0xFF);   // near-black olive
    [SerializeField] Color32 textPanelColor = new Color32(0x2A, 0x2D, 0x24, 0xFF);   // olive drab, dark
    [SerializeField] Color32 nameplateColor = new Color32(0x12, 0x14, 0x0E, 0xFF);   // recessed plate
    [SerializeField] Color32 accentColor = new Color32(0xE0, 0xB3, 0x51, 0xFF);      // stencil amber
    [SerializeField] Color32 bodyTextColor = new Color32(0xEA, 0xE8, 0xDA, 0xFF);    // warm off-white
    [SerializeField] Color32 shadeOverlayColor = new Color32(0x0C, 0x0E, 0x08, 0xFA);
    [SerializeField] Color32 chipColor = new Color32(0x12, 0x14, 0x0E, 0xF2);
    [SerializeField] Color32 chipTextColor = new Color32(0xE0, 0xB3, 0x51, 0xFF);    // amber
    [SerializeField] Color32 chipDisabledColor = new Color32(0x5A, 0x5E, 0x4C, 0xFF);

    [Header("Motion")]
    [Tooltip("How fast the emotion background color blends toward its target.")]
    public float colorFadeSpeed = 6f;

    [Header("Chapter Select restyle")]
    [SerializeField] float chapterFontSize = 46f;
    [SerializeField] Color32 chapterAccentColor = new Color32(0x7C, 0x8A, 0x4F, 0xFF); // olive marking
    [SerializeField] Color32 chapterTextPanelColor = new Color32(0x1B, 0x1E, 0x16, 0xFF);

    public enum BoxMode
    {
        Dialogue,      // mock-up layout: nameplate + portrait left, text right
        ChapterSelect  // full-width, centered announcement panel, no portrait/nameplate
    }

    // generated runtime pieces
    RectTransform root;
    RectTransform leftPanelRT;
    Image textPanelImg;
    Image leftAccentImg;
    Image rightAccentImg;
    Image glowImage;      // emotion-tinted glow at the bottom of the portrait area
    Image shadeImage;     // dark fade on top of the glow
    RectTransform portraitRT;
    Image portraitImage;
    RectTransform chapterNav;
    Button prevChip;
    Button nextChip;
    CharacterVisual activeCharacter;
    DialogueEmotion activeEmotion = DialogueEmotion.Neutral;
    BoxMode activeMode = BoxMode.Dialogue;
    Color targetGlow;
    Sprite fadeSprite;
    Texture2D fadeTexture;

    void Awake()
    {
        if (gm == null) gm = FindFirstObjectByType<Game_Master>();
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
            string display = activeCharacter != null ? activeCharacter.displayName : (key ?? string.Empty);
            nameText.text = display.ToUpperInvariant(); // stencil-style military plate
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

    /// <summary>Switch between the dialogue layout and the chapter-select layout.</summary>
    public void SetChapterSelectMode(bool chapterSelect)
    {
        SetMode(chapterSelect ? BoxMode.ChapterSelect : BoxMode.Dialogue);
    }

    /// <summary>Switch the whole text box between <see cref="BoxMode"/> layouts.</summary>
    public void SetMode(BoxMode mode)
    {
        if (mode == activeMode) return;
        activeMode = mode;
        ApplyMode();
    }

    /// <summary>Current layout mode of the text box.</summary>
    public BoxMode Mode => activeMode;

    /// <summary>Enable/dim the chapter select nav chips (PREV / NEXT).</summary>
    public void SetChapterNavState(bool canPrev, bool canNext)
    {
        SetChipState(prevChip, canPrev);
        SetChipState(nextChip, canNext);
    }

    void SetChipState(Button chip, bool enabled)
    {
        if (chip == null) return;
        chip.interactable = enabled;
        TextMeshProUGUI label = chip.GetComponentInChildren<TextMeshProUGUI>(true);
        if (label != null) label.color = enabled ? (Color)chipTextColor : (Color)chipDisabledColor;
    }

    void ApplyMode()
    {
        bool chapter = activeMode == BoxMode.ChapterSelect;

        // Chapter select: drop the character column entirely and let the
        // text panel take the full width with big centered text.
        if (leftPanelRT != null) leftPanelRT.gameObject.SetActive(!chapter);

        if (textPanelImg != null)
        {
            textPanelImg.color = chapter ? (Color)chapterTextPanelColor : (Color)textPanelColor;
            RectTransform rt = (RectTransform)textPanelImg.transform;
            rt.offsetMin = new Vector2(chapter ? 0f : leftPanelWidth + panelGap, 0f);
        }

        Color32 accent = chapter ? chapterAccentColor : accentColor;
        MilitaryGUI.StyleHazard(leftAccentImg, accent);
        MilitaryGUI.StyleHazard(rightAccentImg, accent);

        if (chapterNav != null) chapterNav.gameObject.SetActive(chapter);

        if (bodyText != null)
        {
            bodyText.fontSize = chapter ? chapterFontSize : bodyFontSize;
            bodyText.alignment = chapter ? TextAlignmentOptions.Center : TextAlignmentOptions.TopLeft;
            bodyText.characterSpacing = chapter ? 6f : 0f; // stencil-ish spread for announcements
        }
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
        leftPanelRT = leftPanel;
        Stretch(leftPanel, 0f, 0f, 0f, 1f);
        leftPanel.pivot = new Vector2(0f, 0.5f);
        leftPanel.anchoredPosition = Vector2.zero;
        leftPanel.sizeDelta = new Vector2(leftPanelWidth, 0f);

        leftAccentImg = MakeAccent(leftPanel, "Top Accent");

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
        textPanelImg = textPanel.GetComponent<Image>();
        textPanel.anchorMin = new Vector2(0f, 0f);
        textPanel.anchorMax = new Vector2(1f, 1f);
        textPanel.pivot = new Vector2(0.5f, 0.5f);
        textPanel.offsetMin = new Vector2(leftPanelWidth + panelGap, 0f);
        textPanel.offsetMax = Vector2.zero;

        rightAccentImg = MakeAccent(textPanel, "Top Accent");

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
            nameText.characterSpacing = 8f; // stencil markings spread
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

        BuildChapterNav();

        ApplyMode();
    }

    void RestyleLegacyButton(string childName, int slot)
    {
        Transform button = transform.Find(childName);
        if (button == null) return;

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
            // History opens the field log now
            label.text = childName == "History" ? "LOG" : childName.ToUpperInvariant();
            label.color = chipTextColor;
            label.fontSize = 20f;
            label.fontStyle = FontStyles.Bold;
            label.characterSpacing = 6f;
            label.alignment = TextAlignmentOptions.Center;
            RectTransform lrt = (RectTransform)label.transform;
            Stretch(lrt, 0f, 0f, 1f, 1f);
            lrt.offsetMin = Vector2.zero;
            lrt.offsetMax = Vector2.zero;
        }

        button.SetAsLastSibling(); // keep chips clickable above the panels
    }

    const float chipWidth = 96f;
    const float chipHeight = 30f;
    const float chipGap = 10f;
    const float navChipWidth = 196f;

    void BuildChapterNav()
    {
        chapterNav = MakeRect("Chapter Nav", root);
        chapterNav.anchorMin = new Vector2(0f, 1f);
        chapterNav.anchorMax = new Vector2(0f, 1f);
        chapterNav.pivot = new Vector2(0f, 0f);
        chapterNav.anchoredPosition = new Vector2(0f, 12f);
        chapterNav.sizeDelta = new Vector2(navChipWidth * 2f + chipGap, chipHeight);

        prevChip = MakeNavChip(chapterNav, "<< PREV CHAPTER", 0f);
        nextChip = MakeNavChip(chapterNav, "NEXT CHAPTER >>", navChipWidth + chipGap);

        if (prevChip != null && gm != null)
            prevChip.onClick.AddListener(() => gm.Leftnextchapter());
        if (nextChip != null && gm != null)
            nextChip.onClick.AddListener(() => gm.Rightnextchapter());

        chapterNav.gameObject.SetActive(false); // chapter-select mode only
        chapterNav.SetAsLastSibling();
    }

    Button MakeNavChip(RectTransform parent, string label, float x)
    {
        RectTransform rt = MakeRect(label, parent);
        rt.anchorMin = new Vector2(0f, 0f);
        rt.anchorMax = new Vector2(0f, 0f);
        rt.pivot = new Vector2(0f, 0f);
        rt.anchoredPosition = new Vector2(x, 0f);
        rt.sizeDelta = new Vector2(navChipWidth, chipHeight);

        Image bg = rt.gameObject.AddComponent<Image>();
        bg.color = chipColor;

        Button button = rt.gameObject.AddComponent<Button>();
        button.targetGraphic = bg;

        TextMeshProUGUI tmp = MakeLabel(rt, label, 20f, chipTextColor);
        tmp.fontStyle = FontStyles.Bold;
        tmp.characterSpacing = 5f;
        tmp.alignment = TextAlignmentOptions.Center;
        return button;
    }

    TextMeshProUGUI MakeLabel(RectTransform parent, string text, float size, Color32 color)
    {
        RectTransform rt = MakeRect("Label", parent);
        Stretch(rt, 0f, 0f, 1f, 1f);
        var tmp = rt.gameObject.AddComponent<TextMeshProUGUI>();
        tmp.text = text;
        tmp.fontSize = size;
        tmp.color = color;
        tmp.raycastTarget = false;
        tmp.margin = Vector4.zero;
        // inherit the project font from the existing dialogue text objects
        if (nameText != null && nameText.font != null) tmp.font = nameText.font;
        else if (bodyText != null && bodyText.font != null) tmp.font = bodyText.font;
        return tmp;
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
        MilitaryGUI.StyleHazard(accent, accentColor); // hazard-stripe accent strip
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
