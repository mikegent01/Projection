using System.Collections.Generic;
using System.Text;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

/// <summary>
/// FIELD LOG — the redesigned dialogue history overlay.
///
/// Lines are recorded as they are actually spoken (dialouge feeds Record),
/// so the log shows what the player has seen — nothing more, nothing less.
/// After a load, RebuildFromLines refills the log from the script so it
/// looks like the player played straight through.
///
/// The whole overlay builds itself at runtime as a sibling under the root
/// canvas (military theme, see MilitaryGUI): dim backdrop, titled panel,
/// scrollable log, close chip. The old ScrollRect "Content" setup in the
/// scene is retired — this script no longer depends on it.
/// </summary>
public class historyscript : MonoBehaviour
{
    public dialouge dl;

    [Header("Log content")]
    [Tooltip("Lines before this index belong to chapter select / intro and are not logged.")]
    [SerializeField] int firstHistoryLine = 5;
    [SerializeField] int maxEntries = 300;
    [SerializeField] float entryFontSize = 26f;

    [Header("Panel sizing")]
    [SerializeField] Vector2 panelSize = new Vector2(1120f, 580f);
    [SerializeField] Vector2 panelMaxRatio = new Vector2(0.86f, 0.72f); // of screen

    class Entry
    {
        public string speaker;
        public string text;
    }

    readonly List<Entry> entries = new List<Entry>();
    int lastRecordedLine = -1;

    // generated UI
    TMP_Text logText;
    ScrollRect scroll;
    TMP_FontAsset uiFont;

    void Awake()
    {
        BuildOverlay();
        gameObject.SetActive(false);
    }

    // ---------------------------------------------------------------- API

    /// <summary>Flip the log open/closed (wired to the LOG chip via dialouge).</summary>
    public void Toggle()
    {
        if (gameObject.activeSelf) Hide();
        else Show();
    }

    public void Show()
    {
        RebuildText();
        gameObject.SetActive(true);
        // jump to the bottom so the newest entry is visible
        if (scroll != null) scroll.verticalNormalizedPosition = 0f;
    }

    public void Hide()
    {
        gameObject.SetActive(false);
    }

    /// <summary>Append a spoken line (dedupes re-runs of the same line index).</summary>
    public void Record(string speaker, string text, int lineIndex)
    {
        if (string.IsNullOrEmpty(text)) return;
        if (lineIndex < firstHistoryLine) return;   // chapter select / intro is not logged
        if (lineIndex <= lastRecordedLine) return;  // already logged this line

        lastRecordedLine = lineIndex;
        entries.Add(new Entry { speaker = speaker, text = text });
        if (entries.Count > maxEntries) entries.RemoveAt(0);

        if (gameObject.activeSelf) RebuildText();
    }

    /// <summary>Empty the log (new game / chapter select).</summary>
    public void ClearLog()
    {
        entries.Clear();
        lastRecordedLine = -1;
        if (gameObject.activeSelf) RebuildText();
    }

    /// <summary>
    /// Refill the log from the script up to (and including) the given line —
    /// used after Loadgame so restoring a save shows the full history.
    /// </summary>
    public void RebuildFromLines(int currentLineInclusive)
    {
        entries.Clear();
        lastRecordedLine = -1;

        if (dl != null && dl.Lines != null)
        {
            int last = Mathf.Min(currentLineInclusive, dl.Lines.Length - 1);
            for (int i = firstHistoryLine; i <= last; i++)
            {
                if (string.IsNullOrEmpty(dl.Lines[i].Text)) continue;
                entries.Add(new Entry { speaker = dl.Lines[i].SpeakerName, text = dl.Lines[i].Text });
            }
            lastRecordedLine = currentLineInclusive;
        }

        if (gameObject.activeSelf) RebuildText();
    }

    // --------------------------------------------------------------- build

    void RebuildText()
    {
        if (logText == null) return;

        if (entries.Count == 0)
        {
            logText.text = "-- NO ENTRIES LOGGED --";
            return;
        }

        StringBuilder sb = new StringBuilder();
        foreach (Entry e in entries)
        {
            // amber stencil speaker tag, then the line in warm white
            sb.Append("<color=#E0B351><b>")
              .Append(string.IsNullOrEmpty(e.speaker) ? "???" : e.speaker.ToUpperInvariant())
              .Append("</b></color>")
              .Append("  //  ")
              .Append(e.text)
              .Append("\n\n");
        }
        logText.text = sb.ToString();
    }

    void BuildOverlay()
    {
        RectTransform root = (RectTransform)transform;

        // sit on top of everything else on the root canvas
        Canvas canvas = GetComponentInParent<Canvas>();
        if (canvas != null && transform.parent != canvas.transform)
        {
            transform.SetParent(canvas.transform, false);
            transform.SetAsLastSibling();
        }
        Stretch(root, 0f, 0f, 1f, 1f);

        // dim backdrop (also eats clicks so the game below can't advance)
        Image dim = MakeImage("Dim", root, MilitaryGUI.DimShade);
        dim.raycastTarget = true;
        Stretch((RectTransform)dim.transform, 0f, 0f, 1f, 1f);

        // centered panel, sized down on small screens
        RectTransform panel = MakeRect("Field Log Panel", root);
        panel.anchorMin = new Vector2(0.5f, 0.5f);
        panel.anchorMax = new Vector2(0.5f, 0.5f);
        panel.pivot = new Vector2(0.5f, 0.5f);
        Image panelImg = panel.gameObject.AddComponent<Image>();
        panelImg.color = MilitaryGUI.PanelMid;

        float w = panelSize.x;
        float h = panelSize.y;
        if (canvas != null)
        {
            RectTransform crt = (RectTransform)canvas.transform;
            w = Mathf.Min(w, crt.rect.width * panelMaxRatio.x);
            h = Mathf.Min(h, crt.rect.height * panelMaxRatio.y);
        }
        panel.sizeDelta = new Vector2(Mathf.Max(320f, w), Mathf.Max(240f, h));

        // hazard strips: amber on top, subdued olive on the bottom
        Image top = MakeImage("Top Hazard", panel, MilitaryGUI.Amber);
        MilitaryGUI.StyleHazard(top, MilitaryGUI.Amber);
        RectTransform topRT = (RectTransform)top.transform;
        topRT.anchorMin = new Vector2(0f, 1f);
        topRT.anchorMax = new Vector2(1f, 1f);
        topRT.pivot = new Vector2(0.5f, 1f);
        topRT.offsetMin = new Vector2(0f, -6f);
        topRT.offsetMax = Vector2.zero;

        Image bottom = MakeImage("Bottom Hazard", panel, MilitaryGUI.Olive);
        MilitaryGUI.StyleHazard(bottom, MilitaryGUI.Olive);
        RectTransform bottomRT = (RectTransform)bottom.transform;
        bottomRT.anchorMin = new Vector2(0f, 0f);
        bottomRT.anchorMax = new Vector2(1f, 0f);
        bottomRT.pivot = new Vector2(0.5f, 0f);
        bottomRT.offsetMin = Vector2.zero;
        bottomRT.offsetMax = new Vector2(0f, 5f);

        // title
        logText = null;
        TMP_Text title = MakeText(panel, "FIELD LOG // OPERATION RECORD", 28f, MilitaryGUI.Amber);
        title.fontStyle = FontStyles.Bold;
        title.characterSpacing = 8f;
        title.alignment = TextAlignmentOptions.Left;
        RectTransform titleRT = (RectTransform)title.transform;
        titleRT.anchorMin = new Vector2(0f, 1f);
        titleRT.anchorMax = new Vector2(1f, 1f);
        titleRT.pivot = new Vector2(0.5f, 1f);
        titleRT.offsetMin = new Vector2(24f, -58f);
        titleRT.offsetMax = new Vector2(-140f, -10f);

        // close chip
        Button close = MakeChip(panel, "CLOSE");
        RectTransform closeRT = (RectTransform)close.transform;
        closeRT.anchorMin = new Vector2(1f, 1f);
        closeRT.anchorMax = new Vector2(1f, 1f);
        closeRT.pivot = new Vector2(1f, 1f);
        closeRT.anchoredPosition = new Vector2(-14f, -12f);
        closeRT.sizeDelta = new Vector2(108f, 32f);
        close.onClick.AddListener(Hide);

        // scrollable log area
        RectTransform viewport = MakeRect("Viewport", panel);
        viewport.anchorMin = new Vector2(0f, 0f);
        viewport.anchorMax = new Vector2(1f, 1f);
        viewport.pivot = new Vector2(0.5f, 0.5f);
        viewport.offsetMin = new Vector2(20f, 20f);
        viewport.offsetMax = new Vector2(-20f, -66f);
        viewport.gameObject.AddComponent<RectMask2D>();
        Image viewportBg = viewport.gameObject.AddComponent<Image>();
        viewportBg.color = MilitaryGUI.PlateDark;
        viewportBg.raycastTarget = false;

        RectTransform content = MakeRect("Log Content", viewport);
        content.anchorMin = new Vector2(0f, 1f);
        content.anchorMax = new Vector2(1f, 1f);
        content.pivot = new Vector2(0.5f, 1f);
        content.offsetMin = new Vector2(14f, 0f);
        content.offsetMax = new Vector2(-14f, 0f);

        logText = content.gameObject.AddComponent<TextMeshProUGUI>();
        logText.alignment = TextAlignmentOptions.TopLeft;
        logText.fontSize = entryFontSize;
        logText.color = MilitaryGUI.TextWarm;
        logText.richText = true;
        logText.textWrappingMode = TextWrappingModes.Normal;
        logText.raycastTarget = false;
        logText.margin = new Vector4(0f, 10f, 0f, 10f);
        TMP_FontAsset font = ResolveFont();
        if (font != null) logText.font = font;

        ContentSizeFitter fitter = content.gameObject.AddComponent<ContentSizeFitter>();
        fitter.verticalFit = ContentSizeFitter.FitMode.PreferredSize;

        scroll = viewport.gameObject.AddComponent<ScrollRect>();
        scroll.content = content;
        scroll.viewport = viewport;
        scroll.horizontal = false;
        scroll.vertical = true;
        scroll.movementType = ScrollRect.MovementType.Clamped;
        scroll.scrollSensitivity = 40f;
    }

    TMP_FontAsset ResolveFont()
    {
        if (uiFont != null) return uiFont;
        DialogueBoxUI box = FindFirstObjectByType<DialogueBoxUI>();
        if (box != null && box.bodyText != null) uiFont = box.bodyText.font;
        return uiFont; // null -> TMP project default
    }

    // ------------------------------------------------------------- helpers

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

    TMP_Text MakeText(Transform parent, string text, float size, Color32 color)
    {
        RectTransform rt = MakeRect("Text", parent);
        Stretch(rt, 0f, 0f, 1f, 1f);
        var tmp = rt.gameObject.AddComponent<TextMeshProUGUI>();
        tmp.text = text;
        tmp.fontSize = size;
        tmp.color = color;
        tmp.raycastTarget = false;
        tmp.margin = Vector4.zero;
        TMP_FontAsset font = ResolveFont();
        if (font != null) tmp.font = font;
        return tmp;
    }

    Button MakeChip(Transform parent, string label)
    {
        RectTransform rt = MakeRect(label + " Chip", parent);
        Image bg = rt.gameObject.AddComponent<Image>();
        bg.color = MilitaryGUI.PlateDark;
        Button button = rt.gameObject.AddComponent<Button>();
        button.targetGraphic = bg;

        TMP_Text tmp = MakeText(rt, label, 19f, MilitaryGUI.Amber);
        tmp.fontStyle = FontStyles.Bold;
        tmp.characterSpacing = 5f;
        tmp.alignment = TextAlignmentOptions.Center;
        return button;
    }

    static void Stretch(RectTransform rt, float minX, float minY, float maxX, float maxY)
    {
        rt.anchorMin = new Vector2(minX, minY);
        rt.anchorMax = new Vector2(maxX, maxY);
        rt.offsetMin = Vector2.zero;
        rt.offsetMax = Vector2.zero;
    }
}
