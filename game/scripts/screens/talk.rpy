screen speakpeople():

    if last_label == "intreactivesection01" or test_room == 0:
        # NPC positions (reuse the same spots as your look system)
        $ rajmanx, rajmany = 341, 376   # "Front" person
        $ bagmanx, bagmany = 8, 376    # "Back" person
        # If you want the Drill Sergeant to be talkable too, you can use:
        $ drix, driy = 1027,376


        # Talk to the person in the front (Rajman)
        if in_range(benx, beny, rajmanx, rajmany, radius=250):
            imagebutton:
                idle "images/inventory/inventory_hud/speechbubble.png"
                hover "images/inventory/inventory_hud/speechbubble_hover.png"
                focus_mask True
                xpos rajmanx ypos rajmany
                action [Hide("speakpeople"), Jump("FrontSeat")]
                tooltip "Talk to person in front"

        # Talk to the person in the back (Bagman)
        if in_range(benx, beny, bagmanx, bagmany, radius=200):
            imagebutton:
                idle "images/inventory/inventory_hud/speechbubble.png"
                hover "images/inventory/inventory_hud/speechbubble_hover.png"
                focus_mask True
                xpos bagmanx ypos bagmany
                action [Hide("speakpeople"), Jump("BackSeat")]
                tooltip "Talk to person in back"

    if not game_state["chapter_1"]["projector_room"]["driwalkedaway"]:
            if in_range(benx, beny, drix, driy, radius=200):
                imagebutton:
                    idle "images/inventory/inventory_hud/speechbubble.png"
                    hover "images/inventory/inventory_hud/speechbubble_hover.png"
                    focus_mask True
                    xpos drix ypos driy
                    action [Hide("speakpeople"), Jump("DrillSergeantTalk")]
