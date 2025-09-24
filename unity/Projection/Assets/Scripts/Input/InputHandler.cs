using UnityEngine;
using UnityEngine.InputSystem;

public class InputHandler : MonoBehaviour
{
    #region Variables

    private Camera _mainCamera;
    public playsound ps;

    // animation_cards this will be found in 
    public bool animation_card_liftoff = false;
    public animation_card animCard;
    #endregion

    private void Awake()
    {
        _mainCamera = Camera.main;
    }

    public void OnClick(InputAction.CallbackContext context)
    {
        if (!context.started) return;

        var rayHit = Physics2D.GetRayIntersection(_mainCamera.ScreenPointToRay(Mouse.current.position.ReadValue()));
        if (!rayHit.collider) return;

        if (rayHit.collider.CompareTag("cardclickable"))
        {
            if (animCard.introended == true)
            {
                animation_card_liftoff = true;
                ps.soundmanager("click");        
                animCard.playliftoff();
                ps.soundmanager("get");        
                Debug.Log("Playing Liftoff");
            }
            else
            {
                Debug.Log("Card Is Still Moving");
            }
        }
        else
        {
            Debug.Log(rayHit.collider.gameObject.name);
        }
    }
}
