using UnityEngine;

public class char2controller : MonoBehaviour
{
 [SerializeField] Sprite[] Char2Sprites;
    public void ChangeSprite2(int spritename)
    {
        gameObject.GetComponent<SpriteRenderer>().sprite = Char2Sprites[spritename];
    }

}
