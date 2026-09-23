using UnityEngine;
using UnityEngine.UI;

/// <summary>
/// Shared military look for the game's GUI: olive drab / gunmetal panels,
/// amber stencil markings, hazard-stripe accents. Both DialogueBoxUI and
/// the field-log history overlay pull from here so the theme stays
/// consistent and can be tweaked in one place.
/// </summary>
public static class MilitaryGUI
{
    public static readonly Color32 PanelDark = new Color32(0x1B, 0x1E, 0x16, 0xFF); // near-black olive
    public static readonly Color32 PanelMid = new Color32(0x2A, 0x2D, 0x24, 0xFF);  // olive drab, dark
    public static readonly Color32 PlateDark = new Color32(0x12, 0x14, 0x0E, 0xFF); // nameplate / recesses
    public static readonly Color32 Amber = new Color32(0xE0, 0xB3, 0x51, 0xFF);     // stencil amber
    public static readonly Color32 Olive = new Color32(0x7C, 0x8A, 0x4F, 0xFF);     // olive marking
    public static readonly Color32 TextWarm = new Color32(0xEA, 0xE8, 0xDA, 0xFF);  // warm off-white
    public static readonly Color32 TextMuted = new Color32(0x9C, 0xA0, 0x88, 0xFF); // faded khaki
    public static readonly Color32 DimShade = new Color32(0x05, 0x06, 0x04, 0xC0);  // overlay dim

    static Sprite hazardSprite;
    static Texture2D hazardTexture;

    /// <summary>
    /// Diagonal caution stripes (light + near-black). Tile it on an Image
    /// (<see cref="Image.type"/> = Tiled) and tint via the Image color —
    /// the light band takes the tint, so one sprite serves every accent.
    /// </summary>
    public static Sprite HazardStripes()
    {
        if (hazardSprite != null) return hazardSprite;

        const int size = 16;
        if (hazardTexture == null)
        {
            hazardTexture = new Texture2D(size, size, TextureFormat.RGBA32, false);
            hazardTexture.wrapMode = TextureWrapMode.Repeat;
            hazardTexture.filterMode = FilterMode.Bilinear;
            for (int y = 0; y < size; y++)
            {
                for (int x = 0; x < size; x++)
                {
                    // 45-degree bands, 8px period
                    bool light = ((x + y) % 8) < 4;
                    hazardTexture.SetPixel(x, y, light
                        ? new Color(1f, 1f, 1f, 1f)
                        : new Color(0.06f, 0.06f, 0.05f, 1f));
                }
            }
            hazardTexture.Apply();
        }
        hazardSprite = Sprite.Create(hazardTexture, new Rect(0, 0, size, size),
            new Vector2(0.5f, 0.5f), 16f);
        return hazardSprite;
    }

    /// <summary>Apply the hazard-stripe look to an accent Image.</summary>
    public static void StyleHazard(Image img, Color32 tint)
    {
        if (img == null) return;
        img.sprite = HazardStripes();
        img.type = Image.Type.Tiled;
        img.color = tint;
        img.raycastTarget = false;
    }
}
