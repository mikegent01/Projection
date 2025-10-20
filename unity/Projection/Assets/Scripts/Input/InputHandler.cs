using UnityEngine;
using UnityEngine.InputSystem;

public class InputHandler : MonoBehaviour
{
    #region Variables

    private Camera _mainCamera;
    public dialouge dl;
    public Game_Master gm;
    public playsound ps;

    // animation_cards this will be found in 
    public bool animation_card_liftoff = false;
    public animation_card animCard;
    #endregion

    private void Awake()
    {
        _mainCamera = Camera.main;
    }
    public void Update()
    {
        if (Mouse.current.leftButton.wasPressedThisFrame)
        {
            if (dl.enabledl == true)
            {
                Debug.Log("Going to next line!");
                dl.Nextline();
            }
        }        
    }
    public void OnClick(InputAction.CallbackContext context)
    {
        if (!context.started) return;

        var rayHit = Physics2D.GetRayIntersection(_mainCamera.ScreenPointToRay(Mouse.current.position.ReadValue()));
        if (!rayHit.collider) return;

        if (rayHit.collider.CompareTag("cardclickable"))
        {
            if (animCard.Introended == true && gm.chapternum == 0)
            {
                animation_card_liftoff = true;
                ps.Soundmanager(2); // click
                animCard.Playliftoff();
                ps.Soundmanager(3); // get
                Debug.Log("Playing Liftoff");
            }
            else
            {
                Debug.Log("Card Is Still Moving or chapter not in game yet");
            }
        }
        else
        {
            Debug.Log(rayHit.collider.gameObject.name);
        }
    }
}
