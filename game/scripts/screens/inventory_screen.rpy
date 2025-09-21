# --- Styles (Keep these as they are) ---
style inventory_button:
    padding (10, 5)
    xalign 0.5

style slot_frame:
    background "#728477"
    padding (5, 5, 5, 5)
    xysize (100, 100)

style section_frame:
    background "#113111"
    padding (15, 15)

style stat_icon:
    xysize (50, 50)


# --- --- --- INVENTORY SYSTEM --- --- ---

# --- Main Inventory Screen ---
# This screen now takes the player object as an argument
screen inventory(player_obj=None):
    modal True
    tag inventory

    frame:
        style "section_frame"
        xysize (1100, 750)
        xalign 0.5
        yalign 0.5

        hbox:
            spacing 20

            # --- Left Pane: Inventory Grid ---
            vbox:
                frame:
                    style "section_frame"
                    ysize (710)
                    xsize (500)

                    vbox:
                        spacing 10
                        text "Inventory" size 30 xalign 0.5 color "#FFFFFF"
                        python:
                            # Access the inventory data through the player_obj
                            _inv_items = player_obj.inventory.items
                            _inv_capacity = player_obj.inventory.capacity
                            _grid_cols = 4
                            _grid_rows = (_inv_capacity // _grid_cols) + (1 if _inv_capacity % _grid_cols else 0)
                        # You would add a get_total_weight() method to your Inventory class to use this.
                        # text f"Weight: {player_obj.inventory.get_total_weight():.1f} kg" size 16 xalign 0.5 color "#CCCCCC"
                        text f"Slots: {len(_inv_items)} / {_inv_capacity}" size 16 xalign 0.5 color "#CCCCCC"

                        viewport:
                            draggable True
                            mousewheel True
                            scrollbars "vertical"
                            ysize 580

                            grid _grid_cols _grid_rows:
                                xfill True
                                spacing 10

                                for i in range(_inv_capacity):
                                    if i < len(_inv_items):
                                        $ item_dict = _inv_items[i]  # This is the dict (e.g., {"name": "tissue", "current_durability": 3})
                                        $ item_id = item_dict["name"]  # Extract the name string
                                        python:
                                            # The items_database is still global
                                            _details = items_database.get(item_id)
                                            _tooltip_text = "Unknown Item"
                                            if _details:
                                                _tooltip_text = _details.get("description", item_id)
                                            _img_path = "images/inventory/" + item_id.replace(" ", "_") + ".png"
                                            # Durability for tooltip
                                            _dur = item_dict["current_durability"]
                                            _max_dur = _details.get("max_durability", -1) if _details else -1
                                            _dur_text = f" (Dur: {_dur if _dur >= 0 else 'Inf'}{'/' + str(_max_dur) if _max_dur >= 0 else ''})"
                                            _broken_text = " (Broken)" if item_dict.get("broken", False) else ""
                                            _tooltip_text += _dur_text + _broken_text

                                        if _details:
                                            button:
                                                style "slot_frame"
                                                xysize (90, 90)
                                                action SetVariable("selected_item", item_dict)  # Set to the full dict for details (including durability)
                                                tooltip _tooltip_text

                                                if renpy.loadable(_img_path):
                                                    add _img_path xalign 0.5 yalign 0.5 zoom 0.6
                                                else:
                                                    text item_id size 10 xalign 0.5 yalign 0.5
                                    else:
                                        frame:
                                            style "slot_frame"
                                            xysize (90, 90)
                                            background "#556655"
                                            text "Empty" xalign 0.5 yalign 0.5 color "#AAAAAA" size 10

            # --- Right Pane: Details or Equipped View ---
            vbox:
                frame:
                    style "section_frame"
                    ysize (650)
                    xsize (540)

                    viewport:
                        scrollbars "vertical"
                        mousewheel True

                        if selected_item:
                            # Pass the player_obj and the full item dict
                            use item_details_panel(player_obj=player_obj, item_dict=selected_item)
                        else:
                            # Pass the player_obj to the equipped panel
                            use equipped_items_panel(player_obj=player_obj)

                null height 10
                hbox:
                    xalign 0.5
                    spacing 15
                    #textbutton "Crafting" action Show("crafting_screen", player_obj=player_obj) style "inventory_button"
                    #textbutton "Liquids" action Show("combine_liquids_screen", player_obj=player_obj) style "inventory_button"
                    textbutton "Close" action [SetVariable("selected_item", None), Hide("inventory")] style "inventory_button"
screen crafting_screen(player_obj):
    modal True
    tag crafting

    frame:
        style "section_frame"
        xysize (800, 600)
        xalign 0.5 yalign 0.5

        vbox:
            spacing 10
            text "Workshop" size 30 xalign 0.5 color "#FFFFFF"

            hbox:
                xalign 0.5
                spacing 20
                textbutton "Construction" action SetVariable("current_mode", "construction") style "inventory_button" sensitive (current_mode != "construction")
                textbutton "Destruction" action SetVariable("current_mode", "destruction") style "inventory_button" sensitive (current_mode != "destruction")

            if current_mode == "construction":
                hbox:
                    spacing 15
                    vbox:
                        text "Available Items" size 20 color "#FFFFFF"
                        viewport:
                            ysize 400 xsize 300
                            scrollbars "vertical" mousewheel True
                            vbox:
                                spacing 5
                                for item in player_obj.inventory.items:
                                    $ item_id = item["name"]
                                    if item_id not in selected_items:
                                        $ details = items_database.get(item_id)
                                        if details:
                                            hbox:
                                                spacing 10
                                                $ img_path = "images/inventory/" + item_id.replace(" ", "_") + ".png"
                                                if renpy.loadable(img_path):
                                                    add img_path zoom 0.3
                                                else:
                                                    frame:
                                                        xysize(20,20)

                                                text item_id size 14 color "#DDDDDD"
                                                textbutton "Select" action Function(select_item, item_id) style "inventory_button" text_size 14 padding (5,2) sensitive (len(selected_items) < 2)

                    vbox:
                        spacing 10
                        text "Selected for Combining" size 20 color "#FFFFFF"
                        frame:
                            style "slot_frame"
                            background "#2E4F2E"
                            xsize 400 ysize 150
                            padding (10, 10, 10, 10)
                            if not selected_items:
                                text "Select 2 items" xalign 0.5 yalign 0.5 color "#AAAAAA"
                            else:
                                grid 2 1:
                                     for sel_id in selected_items:
                                         $ sel_details = items_database.get(sel_id)
                                         if sel_details:
                                             vbox:
                                                 $ img_path = "images/inventory/" + sel_id.replace(" ", "_") + ".png"
                                                 if renpy.loadable(img_path):
                                                     add img_path zoom 0.4 xalign 0.5
                                                 else:
                                                     text sel_id size 12 xalign 0.5

                                                 text sel_id size 12 color "#DDDDDD" xalign 0.5
                                                 textbutton "Remove" action Function(remove_from_list, selected_items, sel_id) style "inventory_button" text_size 12 padding (5,2)

                        text "Select Holding Item (Required for some recipes):" size 16 color "#FFFFFF"
                        viewport:
                             ysize 100 xsize 400
                             scrollbars "horizontal"
                             mousewheel True
                             hbox:
                                 spacing 8
                                 textbutton "None" action SetVariable("selected_holding_item", None) style "inventory_button" text_size 12 padding (5,2) sensitive (selected_holding_item is not None)

                                 for hold_item in holding_items:
                                     textbutton hold_item action SetVariable("selected_holding_item", hold_item) style "inventory_button" text_size 12 padding (5,2) sensitive (selected_holding_item != hold_item)

                        null height 10
                        textbutton "Combine" action Function(combine_items, player_obj) style "inventory_button" sensitive (len(selected_items) == 2)  # Pass player_obj

            elif current_mode == "destruction":
                 vbox:
                     text "Select Item to Deconstruct" size 20 color "#FFFFFF"
                     viewport:
                         ysize 400 xsize 700
                         scrollbars "vertical" mousewheel True
                         grid 5 5:
                             spacing 10
                             for item in player_obj.inventory.items:
                                 python:
                                     item_id = item["name"]
                                     _details = items_database.get(item_id)
                                     _tooltip_text = "Unknown Item"
                                     _can_deconstruct = item_id in deconstruction_recipes
                                     if _details:
                                         _tooltip_text = _details.get("description", item_id)
                                         if not _can_deconstruct:
                                             _tooltip_text = "Cannot deconstruct"
                                     _img_path = "images/inventory/" + item_id.replace(" ", "_") + ".png"

                                 if _can_deconstruct:
                                     button:
                                         style "slot_frame"
                                         action [Function(deconstruct_item, player_obj, item_id), Hide("crafting")]  # Pass player_obj
                                         tooltip _tooltip_text
                                         if renpy.loadable(_img_path):
                                             add _img_path xalign 0.5 yalign 0.5 zoom 0.7
                                         else:
                                             text item_id size 12 xalign 0.5 yalign 0.5

                                 else:
                                     frame:
                                         style "slot_frame"
                                         background "#444444"
                                         tooltip _tooltip_text
                                         if _details:
                                             if renpy.loadable(_img_path):
                                                 add _img_path xalign 0.5 yalign 0.5 zoom 0.7 alpha 0.5
                                             else:
                                                 text item_id size 12 xalign 0.5 yalign 0.5 color "#888888"


            null height 20
            textbutton "Close Workshop" action [SetVariable("selected_items", []), SetVariable("selected_holding_item", None), Hide("crafting")] style "inventory_button" xalign 0.5
screen item_details_panel(player_obj, item_dict):
    $ item_id = item_dict["name"]  # Extract name for database lookup
    $ details = items_database.get(item_id)
    $ item_weight = player_obj.inventory.get_item_weight(item_id)
    $ item_desc = details.get("description", "No description.") if details else "No description."
    $ dur = item_dict["current_durability"]
    $ max_dur = details.get("max_durability", -1) if details else -1
    $ dur_text = f"Durability: {dur if dur >= 0 else 'Infinite'}{' / ' + str(max_dur) if max_dur >= 0 else ''}"
    $ broken_text = " (Broken)" if item_dict.get("broken", False) else ""

    if details:
        vbox:
            spacing 15
            text "Selected Item" size 25 xalign 0.5 color "#FFFFFF"

            frame:
                style "slot_frame"
                xysize (180, 180)
                xalign 0.5
                $ img_path = "images/inventory/" + item_id.replace(" ", "_") + ".png"
                if renpy.loadable(img_path):
                    add img_path xalign 0.5 yalign 0.5
                else: 
                    text item_id size 14 xalign 0.5 yalign 0.5

            text f"Name: {item_id}" size 18 color "#FFFFFF" xalign 0.5
            text f"Weight: {item_weight} kg" size 16 color "#CCCCCC" xalign 0.5
            text f"Type: {details.get('type', 'N/A')}" size 16 color "#CCCCCC" xalign 0.5
            text f"Desc: {item_desc}" size 16 color "#DDDDDD" xalign 0.5
            text dur_text size 16 color "#CCCCCC" xalign 0.5
            if broken_text:
                text broken_text size 16 color "#FF0000" xalign 0.5 italic True

            null height 10
            hbox:
                xalign 0.5
                spacing 10
                # Pass the player_obj to the slot selection screen (use item_id as string)
                textbutton "Equip" action Show("slot_selection_screen", player_obj=player_obj, item_id=item_id) style "inventory_button"
                # Call the method on the player's inventory object (use item_id)
                textbutton "Use" action [Function(player_obj.inventory.use_item, item_id), SetVariable("selected_item", None), Hide("inventory")] style "inventory_button"
                textbutton "Discard" action [Function(player_obj.inventory.remove_item, item_id), SetVariable("selected_item", None)] style "inventory_button"
            textbutton "Deselect" action SetVariable("selected_item", None) style "inventory_button"
    else:
        text "Error: Item details not found." xalign 0.5 color "#FF8888"

# --- Reusable Equipment Slot Display ---
screen equipment_slot_display(player_obj, slot_name, current_item_id):
    $ item_dict = current_item_id  # Now a dict (from equipment)
    $ item_id = item_dict["name"] if item_dict else None  # Extract name
    $ details = items_database.get(item_id) if item_id else None
    frame:
        style "slot_frame"
        xysize (120, 120)
        tooltip slot_name.replace("_", " ").title()
        vbox:
            if details:
                $ img_path = "images/inventory/" + item_id.replace(" ", "_") + ".png"
                if renpy.loadable(img_path):
                    add img_path xalign 0.5 yalign 0.5 zoom 0.7
                else:
                    text item_id size 12 xalign 0.5 yalign 0.5
                hbox:
                    xalign 0.5
                    spacing 10
                    # Call the methods on the player's inventory
                    textbutton "U" action [Function(player_obj.inventory.use_item, item_id), Hide("inventory")] style "inventory_button" text_size 12 padding (4,4) tooltip "Use"
                    textbutton "X" action Function(player_obj.inventory.unequip, slot_name) style "inventory_button" text_size 12 padding (4,4) tooltip "Unequip"
            else:
                text "Empty" xalign 0.5 yalign 0.5 color "#AAAAAA" size 14 italic True

# --- Equipped Items Panel ---
screen equipped_items_panel(player_obj):
    vbox:
        spacing 20
        hbox:
            xalign 0.5
            # Pass the player_obj and get the item dict from the player's equipment dictionary
            use equipment_slot_display(player_obj=player_obj, slot_name="head", current_item_id=player_obj.inventory.equipment['head'])
        hbox:
            xalign 0.5
            spacing 20
            use equipment_slot_display(player_obj=player_obj, slot_name="left_hand", current_item_id=player_obj.inventory.equipment['left_hand'])
            use equipment_slot_display(player_obj=player_obj, slot_name="body", current_item_id=player_obj.inventory.equipment['body'])
            use equipment_slot_display(player_obj=player_obj, slot_name="right_hand", current_item_id=player_obj.inventory.equipment['right_hand'])
        hbox:
            xalign 0.5
            spacing 20
            use equipment_slot_display(player_obj=player_obj, slot_name="left_leg", current_item_id=player_obj.inventory.equipment['left_leg'])
            use equipment_slot_display(player_obj=player_obj, slot_name="right_leg", current_item_id=player_obj.inventory.equipment['right_leg'])

# --- Slot Selection Screen ---
screen slot_selection_screen(player_obj, item_id):
    modal True
    $ details = items_database.get(item_id)
    $ item_type = details.get("type") if details else None

    frame:
        style "section_frame"
        xysize (400, 350)
        xalign 0.5 yalign 0.5
        vbox:
            spacing 15
            text f"Equip {item_id} To:" size 20 xalign 0.5 color "#FFFFFF"
            # Call the equip method on the player's inventory
            if item_type == "head":
                textbutton "Head" action [Function(player_obj.inventory.equip, item_id, "head"), Hide("slot_selection_screen")] style "inventory_button"
            elif item_type == "body":
                textbutton "Body" action [Function(player_obj.inventory.equip, item_id, "body"), Hide("slot_selection_screen")] style "inventory_button"
            elif item_type == "weapon" or item_type == "tool":
                textbutton "Left Hand" action [Function(player_obj.inventory.equip, item_id, "left_hand"), Hide("slot_selection_screen")] style "inventory_button"
                textbutton "Right Hand" action [Function(player_obj.inventory.equip, item_id, "right_hand"), Hide("slot_selection_screen")] style "inventory_button"
            # ... and so on for other types ...
            else:
                text "This item type cannot be equipped directly." color "#FFAAAA" xalign 0.5
            textbutton "Cancel" action Hide("slot_selection_screen") style "inventory_button"


# --- --- --- CHARACTER STATUS SCREEN --- --- ---
# This screen also now requires the player object
screen character_status_screen(player_obj):
    modal True
    tag status

    frame:
        style "section_frame"
        xysize (900, 700)
        xalign 0.5 yalign 0.5

        vbox:
            spacing 10
            text "Character Status" size 30 xalign 0.5 color "#FFFFFF"

            hbox:
                xalign 0.5 spacing 15
                textbutton "Body" action SetVariable("selected_tab", "Body") style "inventory_button" sensitive (selected_tab != "Body")
                textbutton "Stats" action SetVariable("selected_tab", "Stats") style "inventory_button" sensitive (selected_tab != "Stats")
                textbutton "Emotions" action SetVariable("selected_tab", "Emotions") style "inventory_button" sensitive (selected_tab != "Emotions")

            null height 15

            # --- Body Status Tab ---
            if selected_tab == "Body":
                # NOTE: You would need to add a calculate_averages() method to your GameCharacter class
                # python:
                #     avg_health, avg_clean, avg_temp = player_obj.calculate_averages()
                # text f"Overall: Health {avg_health}% | Cleanliness {avg_clean}% | Temp {avg_temp}°" size 18 xalign 0.5 color "#CCCCCC"
                viewport:
                    ysize 500
                    scrollbars "vertical" mousewheel True
                    grid 2 3:
                        spacing 15
                        # Loop through the player's health dictionary
                        for part, status_dict in player_obj.health.items():
                            frame:
                                style "section_frame"
                                background "#2E4F2E"
                                padding (10, 10, 10, 10)
                                vbox:
                                    spacing 5
                                    text part.replace("_", " ").title() size 18 color "#FFFF88"
                                    text f"Status: {status_dict.get('status', 'N/A')}" size 14
                                    text "Health:" size 14
                                    bar value status_dict.get('health', 0) range 100 xsize 150
                                    # ... and so on for other bars
                                    text "Conditions:" size 14
                                    if not status_dict.get('conditions'):
                                        text "- None -" size 12 color "#AAAAAA"
                                    else:
                                        for condition in status_dict.get('conditions'):
                                            text f"- {condition}" size 12 color "#FFAAAA"
                                    # Pass the player_obj to the medkit screen
                                    textbutton "Treat" action Show("medkit_screen", player_obj=player_obj, target_part=part) style "inventory_button" text_size 12 padding(5,2)

            # --- Stats Tab ---
            elif selected_tab == "Stats":
                viewport:
                    ysize 500
                    scrollbars "vertical" mousewheel True
                    vbox:
                        spacing 15
                        # Loop through the player's stats dictionary
                        for stat_name, data in player_obj.stats.items():
                            # ... (rest of the stat display logic, using 'data' from the loop) ...
                            text stat_name.title() size 18
                            text f"Level: {data.get('level', 0)}" size 14

            # --- Emotions Tab ---
            elif selected_tab == "Emotions":
                python:
                    # Call the method on the player object
                    top_emotions = player_obj.get_top_emotions()
                    # A simplified way to get the rest
                    other_emotions = [item for item in player_obj.emotions.items() if item not in top_emotions]
                hbox:
                    # ... (rest of emotion display logic) ...
                    pass

            null height 15
            textbutton "Close Status" action Hide("status") style "inventory_button" xalign 0.5

# --- Medkit Screen ---
screen medkit_screen(player_obj, target_part=None):
    modal True
    tag medkit

    frame:
        style "section_frame"
        xysize (600, 500)
        xalign 0.5 yalign 0.5

        vbox:
            spacing 10
            text "Medkit" size 25 color "#FFFFFF" xalign 0.5
            if target_part:
                text f"(Treating: {target_part.replace('_',' ').title()})" size 16 color "#CCCCCC" xalign 0.5

            viewport:
                ysize 350
                scrollbars "vertical" mousewheel True
                vbox:
                    spacing 8
                    if not medkit_contents:
                        text "Medkit is empty." color "#AAAAAA" xalign 0.5
                    else:
                        for item_name, info in medkit_contents.items():
                            frame:
                                # ... (display logic is fine) ...
                                if target_part:
                                    # Call the method on the player object
                                    textbutton f"Use on {target_part.replace('_',' ').title()}" action [Function(player_obj.use_medkit_item, target_part, item_name), Hide("medkit")] style "inventory_button"
            null height 15
            textbutton "Close Medkit" action Hide("medkit") style "inventory_button" xalign 0.5
init python:
    def select_item(item):
        if item not in selected_items and len(selected_items) < 2:
            selected_items.append(item)    
    holding_items = ["Glue", "Screwdriver", "Tape"] 