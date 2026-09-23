using System;
using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.EventSystems;

/// <summary>
/// Visual-novel style text box matching the reference GUI:
///
///   +------------------+  +----------------------------------------+
///   | BENJAMIN (orange)|  |                                        |
///   |------------------|  |   White dialogue text...               |
///   |   Portrait with  |  |                                        |
///   |   emotion glow   |  |                                        |
///   |  [CLICK TO OPEN] |  |                                        |
///   +------------------+  +----------------------------------------+
///     Back   History   Skip   Auto   Save   Q.Save   Q.Load   Prefs
///
/// Features:
///  * Left Box: Solid black 5px border, dark nameplate banner with orange
///    title-case character name, emotion-tinted glow behind character portrait.
///  * Interactive Portrait: Clicking the character's face opens up the
///    detailed Character Dossier / Profile popup with full art and stats.
///  * Right Box: Solid black 5px border, solid dark-gray fill, clean white text.
///  * Quick Action Menu: Bottom row with Back, History (Field Log), Skip, Auto,
///    Save, Q.Save, Q.Load, and Prefs.
///  * Chapter Select: Full-width centered announcement box with PREV/NEXT chips.
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
        public Color nameColor = new Color(0.91f, 0.57f, 0.10f, 1f); // amber/orange
        [Tooltip("Role / assignment displayed in the dossier modal.")]
        public string role = "INFANTRY // RECONNAISSANCE";
        [Tooltip("Bio / tactical notes displayed in the dossier modal.")]
        public string bio = "Cadet operative currently stationed in the Endless Tower facility. Monitored for emotional fluctuations under high-stress deployment.";
        [Tooltip("Full body / expanded art used in the dossier popup (falls back to emotion portrait).")]
        public Sprite fullBodyArt;
        [Tooltip("Portraits per DialogueEmotion (array index = emotion value). Missing entries fall back to index 0; an empty array keeps the previous portrait.")]
        public Sprite[] emotionPortraits = new Sprite[0];
    }

    [Header("Existing text (re-styled & re-parented into the new layout)")]
    public TextMeshProUGUI nameText;
    public TextMeshProUGUI bodyText;

    [Header("Game flow")]
    public Game_Master gm;
    public dialouge dl;

    [Header("Speakers (change nameplate / portrait / dossier from these variables)")]
    public CharacterVisual[] characters = new CharacterVisual[0];

    [Header("Layout")]
    [SerializeField] float panelHeight = 240f;
    [SerializeField] float sideMargin = 32f;
    [SerializeField] float bottomMargin = 34f;
    [SerializeField] float leftPanelWidth = 280f;
    [SerializeField] float panelGap = 14f;
    [SerializeField] float nameplateHeight = 44f;
    [SerializeField] float borderWidth = 5f;
    [SerializeField] float nameFontSize = 28f;
    [SerializeField] float bodyFontSize = 28f;

    [Header("Visual Colors")]
    [SerializeField] Color32 borderColor = new Color32(0x00, 0x00, 0x00, 0xFF);          // solid black frame
    [SerializeField] Color32 leftBgColor = new Color32(0x11, 0x13, 0x15, 0xFF);          // dark charcoal
    [SerializeField] Color32 textPanelColor = new Color32(0x44, 0x44, 0x44, 0xFF);       // medium-dark gray
    [SerializeField] Color32 nameplateColor = new Color32(0x0A, 0x0A, 0x0A, 0xFF);       // solid black plate
    [SerializeField] Color32 bodyTextColor = new Color32(0xFF, 0xFF, 0xFF, 0xFF);        // pure white text
    [SerializeField] Color32 defaultNameColor = new Color32(0xE8, 0x6A, 0x00, 0xFF);     // orange
    [SerializeField] Color32 quickMenuColor = new Color32(0x8E, 0x9E, 0xAB, 0xFF);       // subtle silver/slate
    [SerializeField] Color32 quickMenuHover = new Color32(0xFF, 0xFF, 0xFF, 0xFF);       // white hover
    [SerializeField] Color32 shadeOverlayColor = new Color32(0x0A, 0x0C, 0x0E, 0xF5);

    [Header("Motion")]
    [Tooltip("How fast the emotion background color blends toward its target.")]
    public float colorFadeSpeed = 6f;

    [Header("Chapter Select restyle")]
    [SerializeField] float chapterFontSize = 40f;
    [SerializeField] Color32 chapterAccentColor = new Color32(0x7C, 0x8A, 0x4F, 0xFF); // olive marking

    public enum BoxMode
    {
        Dialogue,      // two-panel layout: nameplate + portrait left, dialogue text right
        ChapterSelect  // full-width centered announcement panel
    }

    // generated runtime pieces
    RectTransform root;
    RectTransform leftOuterRT;
    RectTransform rightOuterRT;
    Image rightInnerImg;
    Image glowImage;
    Image shadeImage;
    RectTransform portraitRT;
    Image portraitImage;
    Button portraitButton;
    Image portraitHoverHighlight;
    RectTransform quickMenuBar;
    RectTransform chapterNav;
    Button prevChip;
    Button nextChip;
    CharacterVisual activeCharacter;
    DialogueEmotion activeEmotion = DialogueEmotion.Neutral;
    BoxMode activeMode = BoxMode.Dialogue;
    Color targetGlow;
    Sprite fadeSprite;
    Texture2D fadeTexture;

    // Dossier modal popup
    GameObject dossierRoot;
    Image dossierDimmer;
    TMP_Text dossierTitleText;
    Image dossierArtImage;
    TMP_Text dossierNameText;
    TMP_Text dossierRoleText;
    TMP_Text dossierStatusText;
    TMP_Text dossierPsychText;
    TMP_Text dossierStatsText;
    TMP_Text dossierBioText;

    void Awake()
    {
        if (gm == null) gm = FindFirstObjectByType<Game_Master>();
        if (dl == null) dl = GetComponent<dialouge>();
        if (dl == null) dl = FindFirstObjectByType<dialouge>();

        BuildLayout();
        BuildDossierModal();

        // snap to neutral emotion glow
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

        // Close dossier with Escape or Space
        if (dossierRoot != null && dossierRoot.activeSelf)
        {
            if (Input.GetKeyDown(KeyCode.Escape) || Input.GetKeyDown(KeyCode.Space))
            {
                CloseCharacterDossier();
            }
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
            nameText.text = display; // Title Case / clean display
            nameText.color = activeCharacter != null ? activeCharacter.nameColor : (Color)defaultNameColor;
            nameText.characterSpacing = 0f;
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
        if (dossierRoot != null && dossierRoot.activeSelf)
        {
            UpdateDossierContent();
        }
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
        if (label != null) label.color = enabled ? (Color)defaultNameColor : new Color(0.4f, 0.4f, 0.4f, 1f);
    }

    void ApplyMode()
    {
        bool chapter = activeMode == BoxMode.ChapterSelect;

        if (leftOuterRT != null) leftOuterRT.gameObject.SetActive(!chapter);

        if (rightOuterRT != null)
        {
            rightOuterRT.offsetMin = new Vector2(chapter ? 0f : leftPanelWidth + panelGap, 0f);
        }

        if (quickMenuBar != null) quickMenuBar.gameObject.SetActive(!chapter);
        if (chapterNav != null) chapterNav.gameObject.SetActive(chapter);

        if (bodyText != null)
        {
            bodyText.fontSize = chapter ? chapterFontSize : bodyFontSize;
            bodyText.alignment = chapter ? TextAlignmentOptions.Center : TextAlignmentOptions.TopLeft;
            bodyText.characterSpacing = 0f;
        }
    }

    // --------------------------------------------------- Character Dossier

    /// <summary>Opens the full character inspect / dossier modal when clicking the character's face.</summary>
    public void OpenCharacterDossier()
    {
        if (dossierRoot == null) return;
        UpdateDossierContent();
        dossierRoot.SetActive(true);
        dossierRoot.transform.SetAsLastSibling();

        if (gm != null && gm.ps != null)
        {
            gm.ps.Soundmanager(2); // UI click sound
        }
    }

    /// <summary>Closes the character dossier modal.</summary>
    public void CloseCharacterDossier()
    {
        if (dossierRoot != null)
        {
            dossierRoot.SetActive(false);
            if (gm != null && gm.ps != null)
            {
                gm.ps.Soundmanager(2);
            }
        }
    }

    void UpdateDossierContent()
    {
        string charName = activeCharacter != null && !string.IsNullOrEmpty(activeCharacter.displayName)
            ? activeCharacter.displayName
            : "BENJAMIN";

        string role = activeCharacter != null && !string.IsNullOrEmpty(activeCharacter.role)
            ? activeCharacter.role
            : "INFANTRY // RECONNAISSANCE";

        string bio = activeCharacter != null && !string.IsNullOrEmpty(activeCharacter.bio)
            ? activeCharacter.bio
            : "Cadet operative currently stationed in the Endless Tower facility. Monitored for emotional fluctuations under high-stress deployment.";

        if (dossierTitleText != null)
            dossierTitleText.text = "PERSONNEL DOSSIER // " + charName.ToUpperInvariant();

        if (dossierNameText != null)
            dossierNameText.text = "<b>SUBJECT:</b> <color=#E86A00>" + charName.ToUpperInvariant() + "</color>";

        if (dossierRoleText != null)
            dossierRoleText.text = "<b>ASSIGNMENT:</b> <color=#EAE8DA>" + role + "</color>";

        if (dossierStatusText != null)
            dossierStatusText.text = "<b>STATUS:</b> <color=#7C8A4F>ACTIVE // DEPLOYED</color>";

        if (dossierPsychText != null)
        {
            string moodStr;
            string moodColor;
            switch (activeEmotion)
            {
                case DialogueEmotion.Neutral:
                    moodStr = "NEUTRAL // BASELINE";
                    moodColor = "#4B7055";
                    break;
                case DialogueEmotion.Embarrassed:
                    moodStr = "AGITATED // ELEVATED STRESS";
                    moodColor = "#C84B31";
                    break;
                case DialogueEmotion.Happy:
                    moodStr = "CONFIDENT // HIGH MORALE";
                    moodColor = "#2D8C6F";
                    break;
                case DialogueEmotion.Sad:
                    moodStr = "DESPONDENT // FATIGUE DETECTED";
                    moodColor = "#3D5A80";
                    break;
                case DialogueEmotion.Stoic:
                    moodStr = "RESOLUTE // COMBAT READY";
                    moodColor = "#6B7280";
                    break;
                case DialogueEmotion.Angry:
                    moodStr = "HOSTILE // HIGH VIGILANCE";
                    moodColor = "#9E2A2B";
                    break;
                default:
                    moodStr = "OPERATIONAL";
                    moodColor = "#E0B351";
                    break;
            }
            dossierPsychText.text = "<b>PSYCH EVAL:</b> <color=" + moodColor + ">" + moodStr + "</color>";
        }

        if (dossierStatsText != null)
        {
            dossierStatsText.text = "<b>PHYSICAL EVALUATION:</b>\n" +
                                   "<color=#9CA088>STRENGTH:</color> 74%    " +
                                   "<color=#9CA088>SPEED:</color> 88%    " +
                                   "<color=#9CA088>RESILIENCE:</color> NOMINAL";
        }

        if (dossierBioText != null)
            dossierBioText.text = "<b>TACTICAL NOTES:</b>\n" + bio;

        if (dossierArtImage != null)
        {
            Sprite art = null;
            if (activeCharacter != null && activeCharacter.fullBodyArt != null)
                art = activeCharacter.fullBodyArt;
            else if (portraitImage != null && portraitImage.sprite != null)
                art = portraitImage.sprite;

            dossierArtImage.sprite = art;
            dossierArtImage.gameObject.SetActive(art != null);
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

        portraitImage.sprite = sprite;
        portraitImage.gameObject.SetActive(sprite != null);

        if (sprite != null && portraitRT != null)
        {
            // Center the bust inside the portrait box cleanly
            portraitRT.sizeDelta = new Vector2(170f, 170f);
        }
    }

    // -------------------------------------------------------------- build

    void BuildLayout()
    {
        root = (RectTransform)transform;

        // Hide old gray box background Image component if present
        Image oldImg = GetComponent<Image>();
        if (oldImg != null) oldImg.enabled = false;

        // Dock to the bottom of the screen
        root.anchorMin = new Vector2(0f, 0f);
        root.anchorMax = new Vector2(1f, 0f);
        root.pivot = new Vector2(0.5f, 0f);
        root.anchoredPosition = new Vector2(0f, bottomMargin);
        root.sizeDelta = new Vector2(-sideMargin * 2f, panelHeight);

        // 1. LEFT PANEL: Nameplate + Character Portrait Box
        leftOuterRT = MakeBorderedFrame("Left Frame", root, leftBgColor, borderColor, borderWidth);
        leftOuterRT.anchorMin = new Vector2(0f, 0f);
        leftOuterRT.anchorMax = new Vector2(0f, 1f);
        leftOuterRT.pivot = new Vector2(0f, 0.5f);
        leftOuterRT.anchoredPosition = Vector2.zero;
        leftOuterRT.sizeDelta = new Vector2(leftPanelWidth, 0f);

        Transform leftInner = leftOuterRT.Find("Fill");

        // Top Nameplate inside Left Panel
        RectTransform nameplate = MakePanel("Nameplate", leftInner, nameplateColor);
        nameplate.anchorMin = new Vector2(0f, 1f);
        nameplate.anchorMax = new Vector2(1f, 1f);
        nameplate.pivot = new Vector2(0.5f, 1f);
        nameplate.offsetMin = new Vector2(0f, -nameplateHeight);
        nameplate.offsetMax = Vector2.zero;

        // Divider strip below nameplate
        Image divider = MakeImage("Divider", leftInner, borderColor);
        RectTransform divRT = (RectTransform)divider.transform;
        divRT.anchorMin = new Vector2(0f, 1f);
        divRT.anchorMax = new Vector2(1f, 1f);
        divRT.pivot = new Vector2(0.5f, 1f);
        divRT.offsetMin = new Vector2(0f, -(nameplateHeight + 2f));
        divRT.offsetMax = new Vector2(0f, -nameplateHeight);

        // Portrait Area below nameplate
        RectTransform portraitArea = MakeRect("Portrait Area", leftInner);
        portraitArea.anchorMin = new Vector2(0f, 0f);
        portraitArea.anchorMax = new Vector2(1f, 1f);
        portraitArea.pivot = new Vector2(0.5f, 0.5f);
        portraitArea.offsetMin = Vector2.zero;
        portraitArea.offsetMax = new Vector2(0f, -(nameplateHeight + 2f));
        portraitArea.gameObject.AddComponent<RectMask2D>();

        // Emotion glow gradient
        glowImage = MakeImage("Emotion Glow", portraitArea, DialogueEmotionPalette.Glow(DialogueEmotion.Neutral));
        Stretch((RectTransform)glowImage.transform, 0f, 0f, 1f, 1f);

        // Dark top fade overlay
        shadeImage = MakeImage("Top Shade", portraitArea, shadeOverlayColor);
        Stretch((RectTransform)shadeImage.transform, 0f, 0f, 1f, 1f);
        shadeImage.sprite = GetFadeSprite();

        // Character bust portrait
        portraitRT = MakeRect("Portrait", portraitArea);
        portraitRT.anchorMin = new Vector2(0.5f, 0f);
        portraitRT.anchorMax = new Vector2(0.5f, 0f);
        portraitRT.pivot = new Vector2(0.5f, 0f);
        portraitRT.anchoredPosition = new Vector2(0f, 0f);
        portraitRT.sizeDelta = new Vector2(170f, 170f);
        portraitImage = portraitRT.gameObject.AddComponent<Image>();
        portraitImage.preserveAspect = true;
        portraitImage.raycastTarget = false;

        // Interactive Click Trigger on Portrait Area ("when you click on character's face it opens it up")
        portraitButton = portraitArea.gameObject.AddComponent<Button>();
        portraitButton.onClick.AddListener(OpenCharacterDossier);
        Image clickRaycaster = portraitArea.gameObject.AddComponent<Image>();
        clickRaycaster.color = new Color(1f, 1f, 1f, 0f); // invisible raycast target
        portraitButton.targetGraphic = clickRaycaster;

        // 2. RIGHT PANEL: Dialogue Text Box
        rightOuterRT = MakeBorderedFrame("Right Frame", root, textPanelColor, borderColor, borderWidth);
        rightOuterRT.anchorMin = new Vector2(0f, 0f);
        rightOuterRT.anchorMax = new Vector2(1f, 1f);
        rightOuterRT.pivot = new Vector2(0.5f, 0.5f);
        rightOuterRT.offsetMin = new Vector2(leftPanelWidth + panelGap, 0f);
        rightOuterRT.offsetMax = Vector2.zero;

        Transform rightInner = rightOuterRT.Find("Fill");

        // Re-parent & restyle existing TextMeshPro components
        if (nameText != null)
        {
            RectTransform rt = (RectTransform)nameText.transform;
            rt.SetParent(nameplate, false);
            Stretch(rt, 0f, 0f, 1f, 1f);
            rt.offsetMin = new Vector2(14f, 2f);
            rt.offsetMax = new Vector2(-10f, -2f);
            nameText.alignment = TextAlignmentOptions.Left;
            nameText.fontSize = nameFontSize;
            nameText.fontStyle = FontStyles.Bold;
            nameText.color = defaultNameColor;
            nameText.characterSpacing = 0f;
            nameText.raycastTarget = false;
            nameText.margin = Vector4.zero;
        }

        if (bodyText != null)
        {
            RectTransform rt = (RectTransform)bodyText.transform;
            rt.SetParent(rightInner, false);
            Stretch(rt, 0f, 0f, 1f, 1f);
            rt.offsetMin = new Vector2(24f, 18f);
            rt.offsetMax = new Vector2(-24f, -18f);
            bodyText.alignment = TextAlignmentOptions.TopLeft;
            bodyText.fontSize = bodyFontSize;
            bodyText.color = bodyTextColor;
            bodyText.characterSpacing = 0f;
            bodyText.raycastTarget = false;
            bodyText.margin = Vector4.zero;
        }

        // Hide legacy button chips in favor of the clean quick menu
        HideLegacyButton("History");
        HideLegacyButton("Load");
        HideLegacyButton("Save");

        // 3. Build VN Quick Action Menu Bar along the bottom
        BuildQuickMenuBar();

        // 4. Build Chapter Select Navigation Chips
        BuildChapterNav();

        ApplyMode();
    }

    void HideLegacyButton(string childName)
    {
        Transform button = transform.Find(childName);
        if (button != null) button.gameObject.SetActive(false);
    }

    void BuildQuickMenuBar()
    {
        quickMenuBar = MakeRect("Quick Menu Bar", root);
        quickMenuBar.anchorMin = new Vector2(0f, 0f);
        quickMenuBar.anchorMax = new Vector2(1f, 0f);
        quickMenuBar.pivot = new Vector2(0.5f, 1f);
        quickMenuBar.anchoredPosition = new Vector2(0f, -6f);
        quickMenuBar.sizeDelta = new Vector2(0f, 24f);

        HorizontalLayoutGroup hlg = quickMenuBar.gameObject.AddComponent<HorizontalLayoutGroup>();
        hlg.childAlignment = TextAnchor.MiddleCenter;
        hlg.spacing = 20f;
        hlg.childForceExpandWidth = false;
        hlg.childForceExpandHeight = false;

        MakeQuickAction("Back", () => { if (dl != null) dl.Previousline(); });
        MakeQuickAction("History", () => { if (dl != null) dl.Populatehistory(); });
        MakeQuickAction("Skip", () => { if (dl != null) dl.SkipLine(); });
        MakeQuickAction("Auto", () => { if (dl != null) dl.ToggleAuto(); });
        MakeQuickAction("Save", () => { if (gm != null) gm.Savegame(); });
        MakeQuickAction("Q.Save", () => { if (gm != null) gm.Savegame(); });
        MakeQuickAction("Q.Load", () => { if (gm != null) gm.Loadgame(); });
        MakeQuickAction("Prefs", () => { if (gm != null) gm.Loadgame(); });
    }

    Button MakeQuickAction(string labelText, UnityEngine.Events.UnityAction action)
    {
        RectTransform rt = MakeRect(labelText, quickMenuBar);
        rt.sizeDelta = new Vector2(80f, 22f);

        Image bg = rt.gameObject.AddComponent<Image>();
        bg.color = new Color(0f, 0f, 0f, 0f); // invisible hit area

        Button btn = rt.gameObject.AddComponent<Button>();
        btn.targetGraphic = bg;
        if (action != null) btn.onClick.AddListener(action);

        TextMeshProUGUI tmp = MakeLabel(rt, labelText, 17f, quickMenuColor);
        tmp.fontStyle = FontStyles.Bold;
        tmp.alignment = TextAlignmentOptions.Center;

        // Hover effect helper
        var trigger = rt.gameObject.AddComponent<EventTrigger>();
        var entryEnter = new EventTrigger.Entry { eventID = EventTriggerType.PointerEnter };
        entryEnter.callback.AddListener((data) => { tmp.color = quickMenuHover; });
        trigger.triggers.Add(entryEnter);

        var entryExit = new EventTrigger.Entry { eventID = EventTriggerType.PointerExit };
        entryExit.callback.AddListener((data) => { tmp.color = quickMenuColor; });
        trigger.triggers.Add(entryExit);

        return btn;
    }

    void BuildChapterNav()
    {
        chapterNav = MakeRect("Chapter Nav", root);
        chapterNav.anchorMin = new Vector2(0f, 1f);
        chapterNav.anchorMax = new Vector2(0f, 1f);
        chapterNav.pivot = new Vector2(0f, 0f);
        chapterNav.anchoredPosition = new Vector2(0f, 12f);
        chapterNav.sizeDelta = new Vector2(196f * 2f + 10f, 32f);

        prevChip = MakeNavChip(chapterNav, "<< PREV CHAPTER", 0f);
        nextChip = MakeNavChip(chapterNav, "NEXT CHAPTER >>", 196f + 10f);

        if (prevChip != null && gm != null)
            prevChip.onClick.AddListener(() => gm.Leftnextchapter());
        if (nextChip != null && gm != null)
            nextChip.onClick.AddListener(() => gm.Rightnextchapter());

        chapterNav.gameObject.SetActive(false);
        chapterNav.SetAsLastSibling();
    }

    Button MakeNavChip(RectTransform parent, string label, float x)
    {
        RectTransform rt = MakeRect(label, parent);
        rt.anchorMin = new Vector2(0f, 0f);
        rt.anchorMax = new Vector2(0f, 0f);
        rt.pivot = new Vector2(0f, 0f);
        rt.anchoredPosition = new Vector2(x, 0f);
        rt.sizeDelta = new Vector2(196f, 32f);

        Image bg = rt.gameObject.AddComponent<Image>();
        bg.color = new Color32(0x10, 0x12, 0x0E, 0xF5);

        Button button = rt.gameObject.AddComponent<Button>();
        button.targetGraphic = bg;

        TextMeshProUGUI tmp = MakeLabel(rt, label, 18f, defaultNameColor);
        tmp.fontStyle = FontStyles.Bold;
        tmp.characterSpacing = 4f;
        tmp.alignment = TextAlignmentOptions.Center;
        return button;
    }

    // ------------------------------------------------- Dossier Modal Build

    void BuildDossierModal()
    {
        Canvas canvas = GetComponentInParent<Canvas>();
        Transform parentTransform = canvas != null ? canvas.transform : transform.root;

        dossierRoot = new GameObject("Character Dossier Modal", typeof(RectTransform));
        RectTransform rootRT = (RectTransform)dossierRoot.transform;
        rootRT.SetParent(parentTransform, false);
        Stretch(rootRT, 0f, 0f, 1f, 1f);

        // Dimmed backdrop (click to dismiss)
        Image dim = MakeImage("Dim Backdrop", rootRT, new Color32(0x00, 0x00, 0x00, 0xD4));
        dim.raycastTarget = true;
        Stretch((RectTransform)dim.transform, 0f, 0f, 1f, 1f);
        Button dimBtn = dim.gameObject.AddComponent<Button>();
        dimBtn.onClick.AddListener(CloseCharacterDossier);

        // Centered Dossier Card Window
        RectTransform cardRT = MakeBorderedFrame("Dossier Window", rootRT, new Color32(0x18, 0x1B, 0x20, 0xFF), borderColor, borderWidth);
        cardRT.anchorMin = new Vector2(0.5f, 0.5f);
        cardRT.anchorMax = new Vector2(0.5f, 0.5f);
        cardRT.pivot = new Vector2(0.5f, 0.5f);
        cardRT.sizeDelta = new Vector2(760f, 460f);

        Transform cardInner = cardRT.Find("Fill");

        // Header Title Bar
        RectTransform header = MakePanel("Header", cardInner, new Color32(0x0B, 0x0D, 0x10, 0xFF));
        header.anchorMin = new Vector2(0f, 1f);
        header.anchorMax = new Vector2(1f, 1f);
        header.pivot = new Vector2(0.5f, 1f);
        header.offsetMin = new Vector2(0f, -48f);
        header.offsetMax = Vector2.zero;

        dossierTitleText = MakeLabel(header, "PERSONNEL DOSSIER // BENJAMIN", 22f, defaultNameColor);
        dossierTitleText.fontStyle = FontStyles.Bold;
        dossierTitleText.characterSpacing = 4f;
        dossierTitleText.alignment = TextAlignmentOptions.Left;
        RectTransform dtRT = (RectTransform)dossierTitleText.transform;
        dtRT.offsetMin = new Vector2(18f, 0f);
        dtRT.offsetMax = new Vector2(-60f, 0f);

        // Close [X] Button in Header
        RectTransform closeHeaderRT = MakeRect("Close X", header);
        closeHeaderRT.anchorMin = new Vector2(1f, 0.5f);
        closeHeaderRT.anchorMax = new Vector2(1f, 0.5f);
        closeHeaderRT.pivot = new Vector2(1f, 0.5f);
        closeHeaderRT.anchoredPosition = new Vector2(-12f, 0f);
        closeHeaderRT.sizeDelta = new Vector2(36f, 32f);
        Image closeXBg = closeHeaderRT.gameObject.AddComponent<Image>();
        closeXBg.color = new Color32(0x22, 0x26, 0x2E, 0xFF);
        Button closeXBtn = closeHeaderRT.gameObject.AddComponent<Button>();
        closeXBtn.targetGraphic = closeXBg;
        closeXBtn.onClick.AddListener(CloseCharacterDossier);
        TMP_Text closeXLabel = MakeLabel(closeHeaderRT, "X", 18f, Color.white);
        closeXLabel.fontStyle = FontStyles.Bold;
        closeXLabel.alignment = TextAlignmentOptions.Center;

        // Content Area (Two Columns)
        RectTransform contentArea = MakeRect("Content", cardInner);
        contentArea.anchorMin = new Vector2(0f, 0f);
        contentArea.anchorMax = new Vector2(1f, 1f);
        contentArea.pivot = new Vector2(0.5f, 0.5f);
        contentArea.offsetMin = new Vector2(18f, 18f);
        contentArea.offsetMax = new Vector2(-18f, -54f);

        // Left Column: Large Character Visual Card
        RectTransform artCard = MakeBorderedFrame("Art Card", contentArea, new Color32(0x0E, 0x11, 0x14, 0xFF), borderColor, 4f);
        artCard.anchorMin = new Vector2(0f, 0f);
        artCard.anchorMax = new Vector2(0f, 1f);
        artCard.pivot = new Vector2(0f, 0.5f);
        artCard.sizeDelta = new Vector2(240f, 0f);

        Transform artInner = artCard.Find("Fill");
        RectTransform artRT = MakeRect("Art", artInner);
        Stretch(artRT, 0f, 0f, 1f, 1f);
        artRT.offsetMin = new Vector2(10f, 10f);
        artRT.offsetMax = new Vector2(-10f, -10f);
        dossierArtImage = artRT.gameObject.AddComponent<Image>();
        dossierArtImage.preserveAspect = true;
        dossierArtImage.raycastTarget = false;

        // Right Column: Details & Vitals
        RectTransform detailsPanel = MakeRect("Details", contentArea);
        detailsPanel.anchorMin = new Vector2(0f, 0f);
        detailsPanel.anchorMax = new Vector2(1f, 1f);
        detailsPanel.pivot = new Vector2(0.5f, 0.5f);
        detailsPanel.offsetMin = new Vector2(256f, 0f);
        detailsPanel.offsetMax = Vector2.zero;

        dossierNameText = MakeLabel(detailsPanel, "SUBJECT: BENJAMIN", 22f, Color.white);
        dossierNameText.alignment = TextAlignmentOptions.TopLeft;
        RectTransform nRT = (RectTransform)dossierNameText.transform;
        nRT.anchorMin = new Vector2(0f, 1f); nRT.anchorMax = new Vector2(1f, 1f);
        nRT.offsetMin = new Vector2(0f, -28f); nRT.offsetMax = Vector2.zero;

        dossierRoleText = MakeLabel(detailsPanel, "ASSIGNMENT: INFANTRY", 18f, new Color32(0xEA, 0xE8, 0xDA, 0xFF));
        dossierRoleText.alignment = TextAlignmentOptions.TopLeft;
        RectTransform rRT = (RectTransform)dossierRoleText.transform;
        rRT.anchorMin = new Vector2(0f, 1f); rRT.anchorMax = new Vector2(1f, 1f);
        rRT.offsetMin = new Vector2(0f, -54f); rRT.offsetMax = new Vector2(0f, -28f);

        dossierStatusText = MakeLabel(detailsPanel, "STATUS: ACTIVE", 18f, new Color32(0x7C, 0x8A, 0x4F, 0xFF));
        dossierStatusText.alignment = TextAlignmentOptions.TopLeft;
        RectTransform sRT = (RectTransform)dossierStatusText.transform;
        sRT.anchorMin = new Vector2(0f, 1f); sRT.anchorMax = new Vector2(1f, 1f);
        sRT.offsetMin = new Vector2(0f, -80f); sRT.offsetMax = new Vector2(0f, -54f);

        dossierPsychText = MakeLabel(detailsPanel, "PSYCH EVAL: NEUTRAL", 18f, defaultNameColor);
        dossierPsychText.alignment = TextAlignmentOptions.TopLeft;
        RectTransform pRT = (RectTransform)dossierPsychText.transform;
        pRT.anchorMin = new Vector2(0f, 1f); pRT.anchorMax = new Vector2(1f, 1f);
        pRT.offsetMin = new Vector2(0f, -106f); pRT.offsetMax = new Vector2(0f, -80f);

        // Divider
        Image colDiv = MakeImage("Detail Divider", detailsPanel, new Color32(0x30, 0x34, 0x3C, 0xFF));
        RectTransform cdRT = (RectTransform)colDiv.transform;
        cdRT.anchorMin = new Vector2(0f, 1f); cdRT.anchorMax = new Vector2(1f, 1f);
        cdRT.offsetMin = new Vector2(0f, -116f); cdRT.offsetMax = new Vector2(0f, -114f);

        dossierStatsText = MakeLabel(detailsPanel, "PHYSICAL EVALUATION:", 17f, new Color32(0xEA, 0xE8, 0xDA, 0xFF));
        dossierStatsText.alignment = TextAlignmentOptions.TopLeft;
        RectTransform stRT = (RectTransform)dossierStatsText.transform;
        stRT.anchorMin = new Vector2(0f, 1f); stRT.anchorMax = new Vector2(1f, 1f);
        stRT.offsetMin = new Vector2(0f, -170f); stRT.offsetMax = new Vector2(0f, -122f);

        dossierBioText = MakeLabel(detailsPanel, "TACTICAL NOTES:", 16f, new Color32(0x9C, 0xA0, 0x88, 0xFF));
        dossierBioText.alignment = TextAlignmentOptions.TopLeft;
        RectTransform bRT = (RectTransform)dossierBioText.transform;
        bRT.anchorMin = new Vector2(0f, 0f); bRT.anchorMax = new Vector2(1f, 1f);
        bRT.offsetMin = new Vector2(0f, 44f); bRT.offsetMax = new Vector2(0f, -174f);

        // Bottom Return Button
        RectTransform returnBtnRT = MakeRect("Return Button", detailsPanel);
        returnBtnRT.anchorMin = new Vector2(0f, 0f);
        returnBtnRT.anchorMax = new Vector2(1f, 0f);
        returnBtnRT.pivot = new Vector2(0.5f, 0f);
        returnBtnRT.offsetMin = Vector2.zero;
        returnBtnRT.offsetMax = new Vector2(0f, 36f);
        Image retBg = returnBtnRT.gameObject.AddComponent<Image>();
        retBg.color = new Color32(0x0C, 0x0E, 0x10, 0xFF);
        Button retBtn = returnBtnRT.gameObject.AddComponent<Button>();
        retBtn.targetGraphic = retBg;
        retBtn.onClick.AddListener(CloseCharacterDossier);

        TMP_Text retLabel = MakeLabel(returnBtnRT, "[ RETURN TO MISSION ]", 18f, defaultNameColor);
        retLabel.fontStyle = FontStyles.Bold;
        retLabel.characterSpacing = 3f;
        retLabel.alignment = TextAlignmentOptions.Center;

        dossierRoot.SetActive(false);
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

    RectTransform MakeBorderedFrame(string name, Transform parent, Color32 fillColor, Color32 borderColor, float borderWidth = 5f)
    {
        var outer = MakeImage(name, parent, borderColor);
        RectTransform outerRT = (RectTransform)outer.transform;

        var inner = MakeImage("Fill", outerRT, fillColor);
        RectTransform innerRT = (RectTransform)inner.transform;
        innerRT.anchorMin = Vector2.zero;
        innerRT.anchorMax = Vector2.one;
        innerRT.offsetMin = new Vector2(borderWidth, borderWidth);
        innerRT.offsetMax = new Vector2(-borderWidth, -borderWidth);

        return outerRT;
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
        if (nameText != null && nameText.font != null) tmp.font = nameText.font;
        else if (bodyText != null && bodyText.font != null) tmp.font = bodyText.font;
        return tmp;
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

        const int h = 64;
        fadeTexture = new Texture2D(1, h, TextureFormat.RGBA32, false);
        fadeTexture.wrapMode = TextureWrapMode.Clamp;
        fadeTexture.filterMode = FilterMode.Bilinear;
        for (int y = 0; y < h; y++)
        {
            float t = y / (float)(h - 1);
            fadeTexture.SetPixel(0, y, new Color(1f, 1f, 1f, t));
        }
        fadeTexture.Apply();
        fadeSprite = Sprite.Create(fadeTexture, new Rect(0, 0, 1, h), new Vector2(0.5f, 0.5f), 100f);
        return fadeSprite;
    }
}
