init python:
    # Helper: check if object is inside a circle around player
    def in_range(px, py, ox, oy, radius=200):
        return ((px - ox)**2 + (py - oy)**2) ** 0.5 <= radius


screen dynamic_text_screen():
    if last_label == "intreactivesection01" or test_room == 0:
        # Object positions (x, y)
        $ projectorx, projectory = 650, 300
        $ seatx, seaty = 274, 526
        $ podiumx, podiumy = 1005, 505
        $ rajmanx, rajmany = 441, 508
        $ bagmanx, bagmany = 78, 516
        $ wirex, wirey   = 932, 487
        $ drix, driy = 1149,478
        $ dryx,dryy = 1141,450
        # Projector
        if in_range(benx, beny, projectorx, projectory, radius=200):
            imagebutton:
                idle "images/inventory/inventory_hud/magna.png"
                hover "images/inventory/inventory_hud/magna_hover.png"
                focus_mask True
                xpos projectorx ypos projectory
                action [Hide("dynamic_text_screen"), Show("projector_look_s2")]

        # Seat
        if in_range(benx, beny, seatx, seaty, radius=200):
            imagebutton:
                idle "images/inventory/inventory_hud/magna.png"
                hover "images/inventory/inventory_hud/magna_hover.png"
                focus_mask True
                xpos seatx ypos seaty
                action [Hide("dynamic_text_screen"), Show("seat_look_s1")]

        # Podium
        if in_range(benx, beny, podiumx, podiumy, radius=200):
            imagebutton:
                idle "images/inventory/inventory_hud/magna.png"
                hover "images/inventory/inventory_hud/magna_hover.png"
                focus_mask True
                xpos podiumx ypos podiumy
                action [Hide("dynamic_text_screen"), Show("podium_look_s1")]

        # Rajman
        if in_range(benx, beny, rajmanx, rajmany, radius=200):
            imagebutton:
                idle "images/inventory/inventory_hud/magna.png"
                hover "images/inventory/inventory_hud/magna_hover.png"
                focus_mask True
                xpos rajmanx ypos rajmany
                action [Hide("dynamic_text_screen"), Show("rajman_look_intreactivesection01")]

        # Bagman
        if in_range(benx, beny, bagmanx, bagmany, radius=200):
            imagebutton:
                idle "images/inventory/inventory_hud/magna.png"
                hover "images/inventory/inventory_hud/magna_hover.png"
                focus_mask True
                xpos bagmanx ypos bagmany
                action [Hide("dynamic_text_screen"), Show("bagman_look_s1")]

        # Wire
        if in_range(benx, beny, wirex, wirey, radius=200):
            imagebutton:
                idle "images/inventory/inventory_hud/magna.png"
                hover "images/inventory/inventory_hud/magna_hover.png"
                focus_mask True
                xpos wirex ypos wirey
                action [Hide("dynamic_text_screen"), Show("wire_look_s1")]
        # behindwall
        if in_range(benx, beny, dryx, dryy, radius=200):
            imagebutton:
                idle "images/inventory/inventory_hud/magna.png"
                hover "images/inventory/inventory_hud/magna_hover.png"
                focus_mask True
                xpos dryx ypos dryy
                action [Hide("dynamic_text_screen"), Show("walllooks1")]
    if not game_state["chapter_1"]["projector_room"]["driwalkedaway"]:
        if in_range(benx, beny, dryx, dryy, radius=200):
            imagebutton:
                idle "images/inventory/inventory_hud/magna.png"
                hover "images/inventory/inventory_hud/magna_hover.png"
                focus_mask True
                xpos dryx ypos dryy
                action [Hide("dynamic_text_screen"), Show("projector_look_s1")]



screen projector_look_s2():
    frame:
        xalign 0.5
        yalign 0.5
        padding (20, 20)
        
        vbox:
            spacing 10
            text "I look at the projector screen thinking about the presentation that just played, it is hard to belive that a portal can destroy a whole town..."
            textbutton "Return" action [Hide("projector_look_s2"), Show("checkKey")]

screen seat_look_s1():
    frame:
        xalign 0.5
        yalign 0.5
        padding (20, 20)
        
        vbox:
            spacing 10
            if not game_state["chapter_1"]["projector_room"]["picked_tissue_up"]:
                text "There is a tissue on my seat, it must have fell out of my pocket. I pick up the tissue"
                textbutton "Pick Up" action [Function(player.inventory.add_item, "Tissue"), SetDict(game_state["chapter_1"]["projector_room"], "picked_tissue_up", True), Hide("seat_look_s1"), Jump("intreactivesection01")]
            else:
                text "There is nothing here..."
                textbutton "Return" action [Hide("seat_look_s1"), Show("checkKey")]

screen podium_look_s1():
    frame:
        xalign 0.5
        yalign 0.5
        padding (20, 20)
        
        vbox:
            spacing 10
            text "Looking at the podium, I think of something in that position."
            textbutton "Return" action [Hide("podium_look_s1"), Show("checkKey")]

screen rajman_look_intreactivesection01():
    python:
        if 'rajman_intel_success' not in game_state["rolls"]["roll_results"]:
            roll_result = player.perform_roll(skill_name='perception', base_chance=40)
            game_state["rolls"]["roll_results"]['rajman_intel_success'] = roll_result

    frame:
        xalign 0.5
        yalign 0.5
        padding (20, 20)

        vbox:
            spacing 10
            text "I look at the man the things I notice most about him his is turban, he is wearing an ottoman style turban possibly for religious reasons but i am not sure."
            $ rajman_roll = game_state["rolls"]["roll_results"].get('rajman_intel_success', {})
            if rajman_roll.get('success', False):
                text "I however do notice that he is hiding something, he is looking at his pocket at something smoking"
            else:
                text f"" size 18 color "#FF0000"
            textbutton "Return" action [Hide("rajman_look_intreactivesection01"), Show("checkKey")]

screen projector_look_s1():
    python:
        if 'projector_success' not in game_state["rolls"]["roll_results"]:
            roll_result = player.perform_roll(skill_name='perception', base_chance=20)
            game_state["rolls"]["roll_results"]['projector_success'] = roll_result

    frame:
        xalign 0.5
        yalign 0.5
        padding (20, 20)

        vbox:
            spacing 10
            text "The Drill Sargent is standing there he is wearing a standard issue uniform and a blue hat with the words MP on it. There appears to be dust on his hat. I don't feel like talking to him as it seems like a bad idea."
            $ projector_roll = game_state["rolls"]["roll_results"].get('projector_success', {})
            if projector_roll.get('success', False):
                text "I also notice the drill Sargent has a scar on his left arm, he seems to be covering it up with his uniform deliberately"
            else:
                text f"" size 18 color "#FF0000"
            textbutton "Return" action [Hide("projector_look_s1"), Show("checkKey")]

screen bagman_look_s1():
    frame:
        xalign 0.5
        yalign 0.5
        padding (20, 20)

        vbox:
            spacing 10
            text "There is a man with a bag on his head.... I will call him bagman from now on."
            textbutton "Return" action [Hide("bagman_look_s1"), Show("checkKey")]

screen wire_look_s1():
    frame:
        xalign 0.5
        yalign 0.5
        padding (20, 20)

        vbox:
            spacing 10
            text "The wire is unplugged, it connects the projector screen to the wall. I would plug it back in but I feel like that would be a bad idea."
            textbutton "Return" action [Hide("wire_look_s1"), Show("checkKey")]
screen walllooks1():
    frame:
        xalign 0.5
        yalign 0.5
        padding (20, 20)

        vbox:
            spacing 10
            text "There is a misscolored part of the brick wall, it has been like this since orientation."
            textbutton "Return" action [Hide("walllooks1"), Show("checkKey")]
