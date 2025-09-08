
#movement
default benx = 150 
default minbenx = 75
default maxbenx = 1065
default beny = 450 
default minbeny = 450
default maxbeny = 5000
default walk_frame = 4
default facing_left = False
default jumping = False
default moving_left = False
default moving_right = False
default auto_moving = False
default jump_velocity = 0
default gravity = 2
default jump_strength = -15
default movement_enabled = False
screen checkKey():
    if movement_enabled:
        key "K_d" action If(not auto_moving, SetVariable("moving_right", True))
        key "keyup_K_d" action If(not auto_moving, [SetVariable("moving_right", False), SetVariable("walk_frame", 4)])        
        key "keyup_K_a" action If(not auto_moving, [SetVariable("moving_left", False), SetVariable("walk_frame", 4)])
        key "K_a" action If(not auto_moving, SetVariable("moving_left", True))        
        key "K_SPACE" action If(not auto_moving and beny >= minbeny, [SetVariable("jumping", True), SetVariable("jump_velocity", jump_strength)])   
screen game_screen():

    if not movement_enabled:
        # Mouse-based facing direction when movement is disabled
        $ mx, my = renpy.get_mouse_pos()
        $ dx = mx - benx - 73
        $ dy = my - beny - 70

        $ sprite = "images/char/Benjerman/walk/smolbenmiddle.png"

        if abs(dx) <= 5 and abs(dy) <= 5:
            $ sprite = "images/char/Benjerman/walk/smolbenmiddle.png"
        else:
            $ import math
            $ angle = math.degrees(math.atan2(dy, dx))  

            if -22.5 <= angle < 22.5:
                $ sprite = "images/char/Benjerman/walk/smallbenright.png"
            elif 22.5 <= angle < 67.5:
                $ sprite = "images/char/Benjerman/walk/smallbenbottomright.png"
            elif 67.5 <= angle < 112.5:
                $ sprite = "images/char/Benjerman/walk/smallbenbottom.png"
            elif 112.5 <= angle < 157.5:
                $ sprite = "images/char/Benjerman/walk/smallbenbottomleft.png"
            elif angle >= 157.5 or angle < -157.5:
                $ sprite = "images/char/Benjerman/walk/smallbenleft.png"
            elif -157.5 <= angle < -112.5:
                $ sprite = "images/char/Benjerman/walk/smolbenupperleft.png"
            elif -112.5 <= angle < -67.5:
                $ sprite = "images/char/Benjerman/walk/smallbenup.png"
            elif -67.5 <= angle < -22.5:
                $ sprite = "images/char/Benjerman/walk/smolbenupperright.png"

        image sprite:
            xpos benx
            ypos beny

    else:
        image "smolbenwalk":
            xpos benx
            ypos beny
            xzoom ( -1.0 if facing_left else 1.0 )

    timer 0.05 repeat True action Function(update_game)
init python:
    def update_game():
           global benx, beny, walk_frame, jumping, jump_velocity, facing_left, auto_moving
           
           if auto_moving:
               dx = target_x - benx
               dy = target_y - beny
               
               if abs(dx) <= 10 and abs(dy) <= 10:
                   benx = target_x
                   beny = target_y
                   auto_moving = False
                   walk_frame = 4  # Reset to idle
                   # If above ground after move, initiate fall
                   if beny < minbeny:
                       jumping = True
                       jump_velocity = 0
                   return
               
               # Move x
               step_x = 0
               if dx > 0:
                   step_x = min(10, dx)
                   benx += step_x
                   facing_left = False
               elif dx < 0:
                   step_x = max(-10, dx)
                   benx += step_x
                   facing_left = True
               
               # Move y linearly
               step_y = 0
               if dy > 0:
                   step_y = min(10, dy)
                   beny += step_y
               elif dy < 0:
                   step_y = max(-10, dy)
                   beny += step_y
               
               # Animate if moving
               if step_x != 0 or step_y != 0:
                   walk_frame = (walk_frame + 1) % 5
           
           else:
               # Normal player control
               if moving_right and not moving_left:
                   benx += 10  
                   facing_left = False
                   walk_frame = (walk_frame + 1) % 5
               elif moving_left and not moving_right:
                   benx -= 10
                   facing_left = True
                   walk_frame = (walk_frame + 1) % 5
               if jumping:
                   beny += jump_velocity
                   jump_velocity += gravity
                   if beny >= minbeny:
                       beny = minbeny
                       jumping = False
                       walk_frame = 4
                       jump_velocity = 0
           
           beny = max(min(beny, maxbeny), 0)
           benx = max(min(benx, maxbenx), minbenx)
    def move_to_pos(tx, ty):
        global auto_moving, movement_enabled, target_x, target_y, jumping, moving_left, moving_right, jump_velocity
        target_x = tx
        target_y = ty
        movement_enabled = True
        auto_moving = True
        jumping = False
        jump_velocity = 0
        moving_left = False
        moving_right = False            