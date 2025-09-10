
default stat_filter = ""
default healing_progress = 0.0  
screen status_screen(player_obj):
    modal True
    frame:
        xsize 800
        ysize 800
        xalign 0.5
        yalign 0.5
        background "#0A0A0A"
        style "rounded_frame"

        vbox:
            spacing 15

            fixed:
                xsize 800
                ysize 450
                add "images/stats_icons/full_body_diagram.png" xalign 0.5 yalign 0.5
                button:  
                    xpos 340 ypos 370
                    xsize (630 - 593) ysize (452 - 407)
                    background Frame(Solid("#ff02023c"), 1, 1)  # semi-transparent black outline
                    action Show("condition_details", player_obj=player_obj, part="left_leg")
                    tooltip "Click to view Left Leg details"

                button:  
                    xpos 430 ypos 370
                    xsize (630 - 593) ysize (452 - 407)
                    background Frame(Solid("#ff02023c"), 1, 1)
                    action Show("condition_details", player_obj=player_obj, part="right_leg")
                    tooltip "Click to view Right Leg details"

                button:  
                    xpos 357 ypos 228
                    xsize (710 - 607) ysize (395 - 278)
                    background Frame(Solid("#ff02023c"), 1, 1)
                    action Show("condition_details", player_obj=player_obj, part="body")
                    tooltip "Click to view Body details"

                button:  
                    xpos 330 ypos 255
                    xsize (601 - 574) ysize (383 - 300)
                    background Frame(Solid("#ff02023c"), 1, 1)
                    action Show("condition_details", player_obj=player_obj, part="left_arm")
                    tooltip "Click to view Right Arm details"

                button:  
                    xpos 453 ypos 240
                    xsize (723 - 693) ysize (365 - 276)
                    background Frame(Solid("#ff02023c"), 1, 1)
                    action Show("condition_details", player_obj=player_obj, part="right_arm")
                    tooltip "Click to view Left Arm details"

                button:  
                    xpos 339 ypos 140
                    xsize (736 - 609) ysize (270 - 182)
                    background Frame(Solid("#ff02023c"), 1, 1)
                    action Show("condition_details", player_obj=player_obj, part="head")
                    tooltip "Click to view Head details"

            if player_obj.is_stat_higher("mental_resilience", 50):
                text "Sanity Level" size 30 xalign 0.5 color "#FFFFFF" bold True
                $ sanity = player_obj.stats.get("sanity", {}).get("current_sanity", 50)
                bar value sanity range 100 xmaximum 400 ymaximum 20 style "health_bar" xalign 0.5

            $ average_health, average_cleanliness, average_temperature = player_obj.calculate_averages()
            $ can_view_health = player_obj.is_stat_higher("medical", 100)
            $ can_view_health_small = player_obj.is_stat_higher("medical", 59)
            $ has_thermometer = "thermometer" in player_obj.inventory.items  

            frame:
                vbox:
                    spacing 10
                    text "Averages" size 30 xalign 0.5 color "#FFFFFF" bold True
                    if can_view_health_small:
                        text f"Est. Avg Health: {average_health}%" size 24 color "#FFFFFF"
                        bar value average_health range 100 xmaximum 400 ymaximum 20 style "health_bar" bar_invert (average_health < 50)
                    if can_view_health:
                        text f"Avg Cleanliness: {average_cleanliness}%" size 24 color "#FFFFFF"
                        bar value average_cleanliness range 100 xmaximum 400 ymaximum 20 style "clean_bar"
                    if has_thermometer or can_view_health:
                        text f"Avg Temperature: {average_temperature}°F" size 24 color "#FFFFFF"
                        bar value average_temperature range 100 xmaximum 400 ymaximum 20 style "temp_bar"

            hbox:
                xalign 0.5
                spacing 20
                if not (player.inventory.is_broken("Pencil")):
                    textbutton "Write a report" action [Function(player.inventory.decrease_durability_func, "Pencil",100), Show("medical_summary_sheet", player_obj=player_obj)]
                textbutton "Quick Heal" action Show("heal_menu", player_obj=player_obj) style "inventory_button"
                textbutton "Close" action Hide("status_screen") style "close_button"
screen medical_summary_sheet(player_obj):
    modal True
    frame:
        xsize 900
        ysize 700
        xalign 0.5
        yalign 0.5
        background Solid("#F5F5DC")  

        viewport:
            ysize 900

            vbox:
                spacing 5
                xalign 0.5
                yalign 0.5

                if not (player_obj.inventory.has_item("Pencil") and player_obj.inventory.has_item("Paper")):
                    text "I need a pencil and paper to write anything down!" size 24 color "#FF0000" xalign 0.5
                    textbutton "Close" action Hide("medical_summary_sheet") xalign 0.5
                else:
                    text "Self Medical Report:" size 30 color "#000000" bold True xalign 0.5  

                    text f"Date: 20XX/3/{current_chapter + 1}" size 24 color "#000000" xalign 0.5

                    python:
                        composure = player_obj.emotions.get("Composure", {}).get("value", 0)
                        confidence = player_obj.emotions.get("Confidence", {}).get("value", 0)
                        paranoid = player_obj.emotions.get("Paranoid", {}).get("value", 0)  
                        name_text = "Benjamin" if confidence > 70 else "Ben…" if confidence < 30 else "Ben"
                        if paranoid > 50:
                            name_text = "Alec"  
                        elif composure < 30:
                            name_text = "Ben"
                    text f"Name: {name_text}" size 24 color "#000000" xalign 0.5

                    $ medical_level = player_obj.stats.get("medical", {}).get("level", 0)
                    $ authenticity = player_obj.emotions.get("Authenticity", {}).get("value", 0)
                    $ pride = player_obj.emotions.get("Pride", {}).get("value", 0)
                    $ has_thermometer = player_obj.inventory.has_item("thermometer")

                    python:
                        if last_label not in summary_rolls:
                            avg_health, avg_clean, avg_temp = player_obj.calculate_averages()
                            part_order = ["head", "body", "left_leg", "right_leg", "left_arm", "right_arm"]
                            base_chances = [30, 40, 50, 60, 70, 80]
                            parts_rolls = {part_order[idx]: player_obj.perform_roll("medical", base_chance=base_chances[idx]) for idx in range(len(part_order))}
                            summary_rolls[last_label] = {
                                "health": player_obj.perform_roll("medical", base_chance=50),
                                "clean": player_obj.perform_roll("medical", base_chance=60),
                                "parts": parts_rolls,
                                "average_health": avg_health,
                                "average_cleanliness": avg_clean,
                                "average_temperature": avg_temp
                            }
                        all_rolls = summary_rolls[last_label]

                    text "Report:" size 26 color "#000000" bold True xalign 0.5

                    python:
                        average_health = all_rolls["average_health"]
                        health_roll = all_rolls["health"]
                        base_health = "I will go through each section of my body and give my thoughts on it.First off how I feel" if paranoid <= 50 else "I will go through each section of my body and give our thoughts on it first off how I feel"
                        if confidence < 30:
                            base_health += " Well… I am not too sure how I feel…if I had to say"
                        if confidence > 70:
                            if average_health > 70:
                                feeling = "I am feeling great!"
                            elif average_health > 40:
                                feeling = "it’s a little scratch"
                            elif average_health > 20:
                                feeling = "some bleeding never hurt anyone"
                            else:
                                feeling = "I think I am fine…"
                        else:
                            if average_health < 20:
                                feeling = "I need a medic asap"
                            elif average_health < 50:
                                feeling = "It could be better"
                            else:
                                feeling = "I think I am okay"
                        if pride > 70:
                            feeling = "As expected from someone like me, " + feeling
                        if authenticity < 30:
                            feeling += " ...or maybe not?"  
                        health_text = f"{base_health} {feeling}"
                        if health_roll["success"]:
                            health_text += f" (Health: {average_health}%)"
                        else:
                            health_text += " (hopefully?)"
                    text health_text size 20 color "#000000" 

                    python:
                        average_cleanliness = all_rolls["average_cleanliness"]
                        clean_roll = all_rolls["clean"]
                        if current_chapter:
                            clean_text = f"As for how clean I am, I took a shower {current_chapter + 1} days ago."
                        else:
                            clean_text = f"As for how clean I am, I took a shower {current_chapter + 1} day ago."
                        if confidence > 70:
                            clean_text += " and I will take one tomorrow too after the mission ends."
                        if authenticity > 70:
                            clean_text += " although the mission will probably go on for a few more days…"
                        clean_text += " If I had to say something I would say"
                        if authenticity > 70 and clean_roll["success"]:
                            clean_text += f" I am {average_cleanliness}% clean."
                        else:
                            if average_cleanliness > 80:
                                clean_feeling = " I am clean"
                            elif average_cleanliness >= 50:  
                                clean_feeling = " I feel reasonably clean."                                 
                            elif average_cleanliness < 30:
                                clean_feeling = " I stink"
                            elif average_cleanliness < 50:
                                clean_feeling = " I could use a shower"
                            else:
                                clean_feeling = " This might effect how people talk to me… "
                            clean_text += clean_feeling + "."
                        if pride > 70:
                            clean_text += " Naturally, given my standards."
                    text clean_text size 20 color "#000000" 

                    python:
                        average_temperature = all_rolls["average_temperature"]
                        temp_text = "As for the current temperature"
                        if authenticity > 70:
                            temp_text += " if that even matters"
                        temp_text += ", "
                        if has_thermometer:
                            temp_text += f"it's exactly {average_temperature}°F."
                        else:
                            if 60 < average_temperature < 90:
                                temp_text += "it feels normal."
                            elif average_temperature >= 90:
                                temp_text += "it feels too hot!"
                            else:
                                temp_text += "it feels chilly."
                    text temp_text size 20 color "#000000" 

                    null height 20

                    text "Body Report" size 26 color "#000000" bold True xalign 0.5
                    
                    $ part_order = ["head", "body", "left_leg", "right_leg", "left_arm", "right_arm"]

                    for idx, part in enumerate(part_order):
                        python:
                            part_roll = all_rolls["parts"][part]
                            part_health = player_obj.health[part]['health']
                            part_conditions = player_obj.health[part]['conditions']
                            part_note = f"{part.replace('_', ' ').title()}: if I had to say something id say "
                            if part_roll["success"]:
                                part_note += f"it would feel about {part_health}% "
                                if part_conditions:
                                    part_note += f"Issues: {', '.join([c.capitalize() for c in part_conditions])}. "
                                else:
                                    part_note += "No issues."
                                part_note += "It feels " + ("amazing" if part_health > 90 else "solid" if part_health > 60 else "painful") + "."
                            else:
                                vague = "great" if part_health > 80 else "okay" if part_health > 50 else "bad"
                                part_note += f"{vague}?"
                                if part_conditions:
                                    part_note += ", something's off."
                                part_note += " probably"
                            if pride > 70 and part_health > 70:
                                part_note += "(As if this would stop me!)"
                            elif confidence < 30:
                                part_note += "...I think?"
                            if paranoid > 50:
                                part_note = part_note.replace("I ", "We ")  

                        text part_note size 18 color "#000000" 

                    null height 20
                    textbutton "Close" action Hide("medical_summary_sheet") xalign 0.5 style "inventory_button"
screen proficiency_details(player_obj, stat_name):
    modal True
    frame:
        xsize 800
        ysize 700
        xalign 0.5
        yalign 0.5
        background "#111111"

        vbox:
            spacing 20
            text f"{stat_name.replace('_', ' ').capitalize()} Proficiencies" size 40 xalign 0.5 color "#FFFFFF" bold True

            viewport:
                draggable True
                mousewheel True
                xsize 750
                ysize 500
                vbox:
                    spacing 15
                    if stat_name not in player_obj.proficiencies or not player_obj.proficiencies[stat_name]:
                        text "No proficiencies for this stat yet." size 24 color "#CCCCCC" xalign 0.5
                    else:
                        for prof_name, prof_data in player_obj.proficiencies[stat_name].items():
                            frame:
                                background "#222222"
                                padding (15, 10)
                                hbox:
                                    vbox:
                                        spacing 10
                                        text prof_name.replace("_", " ").capitalize() size 30 color "#00CCFF" bold True
                                        text f"Level: {prof_data['level']}" size 20 color "#CCCCCC"
                                        bar value prof_data["level"] range prof_data['max_xp'] xmaximum 500 ymaximum 20 bar_invert (prof_data["level"] < 5)
                                        text f"Value: {prof_data['current_value']}" size 20 color "#CCCCCC"
                                        bar value prof_data["current_value"] range prof_data["max_xp"] xmaximum 500 ymaximum 20
                                        text f"XP: {prof_data['current_xp']} / {prof_data['max_xp']}" size 20 color "#CCCCCC"
                                        bar value prof_data["current_xp"] range prof_data["max_xp"] xmaximum 500 ymaximum 20

                                        # --- Emotion Bonuses Section ---
                                        $ emotion_bonuses = []
                                        $ total_emotion_bonus = 0
                                        # Loop through all emotions and collect bonuses for this proficiency/stat
                                        for emo_name, emo_data in player_obj.emotions.items():
                                            if "bonus" in emo_data and prof_name in emo_data["bonus"]:
                                                $ bonus = emo_data["bonus"][prof_name]
                                                $ total_emotion_bonus += bonus
                                                $ emotion_bonuses.append((emo_name, bonus))
                                        if emotion_bonuses:
                                            text "Emotion Bonuses:" size 18 color "#FFFFFF"
                                            for emo_name, bonus in emotion_bonuses:
                                                text f"{emo_name.capitalize()}: {'+' if bonus > 0 else ''}{bonus}" size 16 color (("#00FF00" if bonus > 0 else "#FF0000" if bonus < 0 else "#CCCCCC"))
                                        else:
                                            text "Emotion Bonuses: None" size 16 color "#AAAAAA" italic True

                                        # --- Roll Effect Section ---
                                        $ total_effect = prof_data['current_value'] + total_emotion_bonus
                                        text f"Roll Effect: {'+' if total_effect > 0 else ''}{total_effect} to {prof_name.replace('_',' ').capitalize()} rolls" size 18 color (("#00FF00" if total_effect > 0 else "#FF0000" if total_effect < 0 else "#CCCCCC"))

                                    if renpy.loadable(f"images/proficiency_icons/{prof_name}.png"):
                                        add f"images/proficiency_icons/{prof_name}.png" size (50, 50)
                                    else:
                                        add f"images/stats_icons/{stat_name}.png" size (50, 50)  # Fallback to stat icon

            textbutton "Back" action Hide("proficiency_details") xalign 0.5 style "inventory_button"

screen player_stats_screen(player_obj):
    modal True
    frame:
        xsize 1000
        ysize 800
        xalign 0.5
        background "#111111"

        at transform:
            alpha 0.0
            linear 0.5 alpha 1.0

        vbox:
            spacing 20
            text f"{player_obj.name} Stats" size 40 xalign 0.5 color "#FFFFFF" bold True

            hbox:
                spacing 20
                xalign 0.5
                if player_obj.name == "Benjamin":
                    textbutton "Stats" action SetVariable("selected_category", "stats") style "category_button"
                textbutton "Emotions" action SetVariable("selected_category", "emotions") style "category_button"
                if player_obj.name == "Benjamin":
                    textbutton "Relationships" action SetVariable("selected_category", "relationships") style "category_button"
                textbutton "Close" action Hide("player_stats_screen") style "category_button" 

            viewport:
                draggable True
                mousewheel True
                xsize 950
                ysize 600
                vbox:
                    spacing 20

                    if selected_category == "stats":
                        text "All Stats" size 30 color "#FFFFFF" xalign 0.5 bold True
                        grid 2 len(set(soft_skills + hard_skills)):  # 3 columns, rows based on number of stats
                            xalign 0.5
                            spacing 20
                            for stat_name in sorted(set(soft_skills + hard_skills)):
                                if stat_name in player_obj.stats:
                                    $ stat_data = player_obj.stats[stat_name]
                                    frame:
                                        background (("#003366" if stat_name in soft_skills else "#f58004"))
                                        padding (5, 5)
                                        xsize 450
                                        vbox:
                                            spacing 5
                                            hbox:
                                                add f"images/stats_icons/{stat_name}.png" size (30, 30)
                                                text stat_name.replace("_", " ").capitalize() size 20 color "#FFFFFF" bold True
                                            text f"Level: {stat_data['level']}" size 16 color "#CCCCCC"
                                            bar value stat_data["level"] range stat_data['max_xp'] xmaximum 200 ymaximum 10 bar_invert (stat_data["level"] < 5)
                                            text f"Bonus: {stat_data.get('current_value', 0)}" size 16 color "#CCCCCC"
                                            bar value stat_data.get("current_value", 0) range stat_data['max_xp'] xmaximum 200 ymaximum 10
                                            text f"XP: {stat_data['current_xp']} / {stat_data['max_xp']}" size 16 color "#CCCCCC"
                                            bar value stat_data['current_xp'] range stat_data['max_xp'] xmaximum 200 ymaximum 10
                                            if stat_data["current_xp"] >= stat_data["max_xp"]:
                                                textbutton "Level Up!" action Function(player_obj.level_up, stat_name) style "level_up_button" xsize 200
                                            text "Effects:" size 16 color "#FFFFFF" bold True
                                            text f"+{stat_data.get('current_value', 0)} base bonus to {stat_name.capitalize().replace('_', ' ')} rolls" size 14 color "#CCCCCC" tooltip "This stat adds directly to your success chance in related skill checks."
                                            text "Emotion Influences:" size 14 color "#FFFFFF"
                                            $ total_emotion_bonus, emotion_bonuses = player_obj._get_emotion_bonus(stat_name)
                                            $ filtered_bonuses = [(emo, bonus) for emo, bonus in emotion_bonuses if player_obj.emotions[emo]["value"] >= 10]
                                            if filtered_bonuses:
                                                for emo, bonus_val in filtered_bonuses:
                                                    text f"{emo.capitalize()}: {'+' if bonus_val > 0 else ''}{bonus_val} bonus" size 12 color (("#00FF00" if bonus_val > 0 else "#FF0000"))
                                            else:
                                                text "No direct emotion bonuses." size 12 color "#AAAAAA" italic True
                                            $ total_bonus = stat_data.get('current_value', 0) + total_emotion_bonus
                                            text f"Effect after bonus: {'+' if total_bonus > 0 else ''}{total_bonus}" size 14 color (("#00FF00" if total_bonus > 0 else "#FF0000" if total_bonus < 0 else "#CCCCCC")) 
                                            null height 5
                                            textbutton "View Proficiencies" action Show("proficiency_details", player_obj=player_obj, stat_name=stat_name) xalign 0.5 style "inventory_button" tooltip f"View details and proficiencies for {stat_name.capitalize()}"

                    elif selected_category == "emotions":
                        text "Emotions" size 30 color "#FFFFFF" xalign 0.5 bold True
                        null height 10
                        $ all_emotions = sorted(player_obj.emotions.items(), key=lambda x: x[1]["value"], reverse=True)
                        $ total_value = sum(data["value"] for _, data in all_emotions) or 1  # Avoid division by zero
                        $ emotion_colors = ["#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#FF00FF", "#00FFFF", "#FFA500", "#800080", "#008000", "#FFC0CB"]  # List of colors for bars
                        
                        if not all_emotions:
                            text "No emotions data available." size 24 color "#AAAAAA" xalign 0.5 italic True
                        else:
                            viewport:
                                xsize 900 ysize 500
                                mousewheel True
                                draggable True
                                vbox:
                                    spacing 15
                                    text "Emotion Breakdown" size 26 color "#FFFFFF" xalign 0.5
                                    for idx, (emo, data) in enumerate(all_emotions):
                                        if data["value"] > 0:
                                            $ color = emotion_colors[idx % len(emotion_colors)]
                                            frame:
                                                background "#222222"
                                                padding (10, 10)
                                                xfill True
                                                vbox:
                                                    spacing 5
                                                    hbox:
                                                        spacing 10
                                                        text f"{emo.capitalize()}: {data['value']} ({(data['value'] / total_value * 100):.1f}%)" size 20 color "#FFFFFF"
                                                    bar value data['value'] range 100 xmaximum 800 ymaximum 20 left_bar color right_bar "#333333"
                                                    
                                                    # Bonuses list
                                                    if "bonus" in data and data["bonus"]:
                                                        text "Stat Bonuses:" size 16 color "#CCCCCC"
                                                        for stat, bonus in data["bonus"].items():
                                                            text f"{stat.replace('_',' ').capitalize()}: {'+' if bonus > 0 else ''}{bonus}" size 14 color (("#00FF00" if bonus > 0 else "#FF0000" if bonus < 0 else "#CCCCCC"))
                                                    else:
                                                        text "No stat bonuses." size 14 color "#AAAAAA" italic True

                    elif selected_category == "relationships":
                        if not player_obj.relationships:
                            text "No relationships established yet." size 24 color "#CCCCCC" xalign 0.5
                        else:
                            text "Relationship Alignment Chart" size 30 color "#FFFFFF" bold True xalign 0.5
                            fixed:
                                xsize 950
                                ysize 500
                                xalign 0.5

                                add "images/stats_icons/alignment_triangle.png" xalign 0.5 yalign 0.6

                                frame:
                                    background "#00000000"  
                                    xsize 950
                                    ysize 150
                                    xalign 0.5
                                    ypos 0
                                    vbox:
                                        spacing 5
                                        hbox:
                                            spacing 10
                                            xalign 0.5
                                            text "Allies" color "#00FF00" size 24 bold True xsize 100
                                            python:
                                                allies_list = []
                                                for p, r in player_obj.relationships.items():
                                                    if r.get("met"):
                                                        trust = r.get("trust", 0)
                                                        friendship = r.get("friendship", 0)
                                                        hostility = r.get("hostility", 0)
                                                        ally_raw = trust + friendship
                                                        enemy_raw = hostility * 2
                                                        neutral_raw = max(0, 200 - (ally_raw + enemy_raw) * 0.5)
                                                        total_raw = ally_raw + enemy_raw + neutral_raw
                                                        ally_w = ally_raw / total_raw if total_raw > 0 else 0
                                                        if ally_w > 0.5:
                                                            allies_list.append(p)
                                            if allies_list:
                                                for person in allies_list:
                                                    button:
                                                        if renpy.loadable(f"images/relationship_icons/{person.lower()}.png"):
                                                            add f"images/relationship_icons/{person.lower()}.png" size (40, 40)
                                                        else:
                                                            text person.capitalize() size 18 color "#FFFFFF"
                                                        action Show("relationship_details", player_obj=player_obj, person=person)
                                                        tooltip player_obj.get_relationship_description(person)
                                            else:
                                                text "None" size 18 color "#AAAAAA" italic True
                                        
                                        hbox:
                                            spacing 10
                                            xalign 0.5
                                            text "Neutrals" color "#FFFF00" size 24 bold True xsize 100
                                            python:
                                                neutrals_list = []
                                                for p, r in player_obj.relationships.items():
                                                    if r.get("met"):
                                                        trust = r.get("trust", 0)
                                                        friendship = r.get("friendship", 0)
                                                        hostility = r.get("hostility", 0)
                                                        ally_raw = trust + friendship
                                                        enemy_raw = hostility * 2
                                                        neutral_raw = max(0, 200 - (ally_raw + enemy_raw) * 0.5)
                                                        total_raw = ally_raw + enemy_raw + neutral_raw
                                                        neutral_w = neutral_raw / total_raw if total_raw > 0 else 0
                                                        if neutral_w > 0.5:
                                                            neutrals_list.append(p)
                                            if neutrals_list:
                                                for person in neutrals_list:
                                                    button:
                                                        if renpy.loadable(f"images/relationship_icons/{person.lower()}.png"):
                                                            add f"images/relationship_icons/{person.lower()}.png" size (40, 40)
                                                        else:
                                                            text person.capitalize() size 18 color "#FFFFFF"
                                                        action Show("relationship_details", player_obj=player_obj, person=person)
                                                        tooltip player_obj.get_relationship_description(person)
                                            else:
                                                text "None" size 18 color "#AAAAAA" italic True
                                        
                                        hbox:
                                            spacing 10
                                            xalign 0.5
                                            text "Enemies" color "#FF0000" size 24 bold True xsize 100
                                            python:
                                                enemies_list = []
                                                for p, r in player_obj.relationships.items():
                                                    if r.get("met"):
                                                        trust = r.get("trust", 0)
                                                        friendship = r.get("friendship", 0)
                                                        hostility = r.get("hostility", 0)
                                                        ally_raw = trust + friendship
                                                        enemy_raw = hostility * 2
                                                        neutral_raw = max(0, 200 - (ally_raw + enemy_raw) * 0.5)
                                                        total_raw = ally_raw + enemy_raw + neutral_raw
                                                        enemy_w = enemy_raw / total_raw if total_raw > 0 else 0
                                                        if enemy_w > 0.5:
                                                            enemies_list.append(p)
                                            if enemies_list:
                                                for person in enemies_list:
                                                    button:
                                                        if renpy.loadable(f"images/relationship_icons/{person.lower()}.png"):
                                                            add f"images/relationship_icons/{person.lower()}.png" size (40, 40)
                                                        else:
                                                            text person.capitalize() size 18 color "#FFFFFF"
                                                        action Show("relationship_details", player_obj=player_obj, person=person)
                                                        tooltip player_obj.get_relationship_description(person)
                                            else:
                                                text "None" size 18 color "#AAAAAA" italic True

                                text "Ally" xalign 0.5 ypos 60 color "#00FF00" size 28 bold True  
                                text "Enemy" xalign 0.05 yalign 0.95 color "#FF0000" size 28 bold True
                                text "Neutral" xalign 0.95 yalign 0.95 color "#FFFF00" size 28 bold True

                                for person, rel_data in player_obj.relationships.items():
                                    if rel_data.get("met"):
                                        $ trust = rel_data.get("trust", 0)
                                        $ friendship = rel_data.get("friendship", 0)
                                        $ hostility = rel_data.get("hostility", 0)

                                        $ ally_raw = trust + friendship
                                        $ enemy_raw = hostility * 2  
                                        $ neutral_raw = max(0, 200 - (ally_raw + enemy_raw) * 0.5)  

                                        $ total_raw = ally_raw + enemy_raw + neutral_raw
                                        $ ally_w = ally_raw / total_raw if total_raw > 0 else 1.0 / 3
                                        $ enemy_w = enemy_raw / total_raw if total_raw > 0 else 1.0 / 3
                                        $ neutral_w = neutral_raw / total_raw if total_raw > 0 else 1.0 / 3

                                        $ sum_w = ally_w + enemy_w + neutral_w
                                        if sum_w > 0:
                                            $ ally_w /= sum_w
                                            $ enemy_w /= sum_w
                                            $ neutral_w /= sum_w

                                        $ pos_x = ally_w * 0.5 + enemy_w * 0.0 + neutral_w * 1.0
                                        $ pos_y = (ally_w * 0.0 + enemy_w * 1.0 + neutral_w * 1.0) * 0.7 + 0.3

                                        button:
                                            xalign pos_x
                                            yalign pos_y
                                            if renpy.loadable(f"images/relationship_icons/{person.lower()}.png"):
                                                add f"images/relationship_icons/{person.lower()}.png" size (40, 40)
                                            else:
                                                text person.capitalize() size 20 color "#FFFFFF" hover_color "#00CCFF"
                                            action Show("relationship_details", player_obj=player_obj, person=person)
                                            tooltip player_obj.get_relationship_description(person)

            textbutton "Back to Menu" action Return() xalign 0.5 yalign 0.95 style "inventory_button" 
screen relationship_details(player_obj, person):
    modal True
    frame:
        xsize 500
        ysize 600
        xalign 0.5
        yalign 0.5
        background "#222222"
        padding (20, 20)

        vbox:
            spacing 15
            text f"{person.capitalize()} Relationship Details" size 30 xalign 0.5 color "#00CCFF" bold True

            $ rel_data = player_obj.relationships.get(person, {})
            $ trust = rel_data.get("trust", 0)
            $ friendship = rel_data.get("friendship", 0)
            $ hostility = rel_data.get("hostility", 0)

            text "Description:" size 24 color "#FFFFFF"
            text player_obj.get_relationship_description(person) size 20 color "#CCCCCC" xalign 0.5

            text "Trust:" size 20 color "#FFFFFF"
            bar value trust range 100 xmaximum 400 ymaximum 20
            text "Friendship:" size 20 color "#FFFFFF"
            bar value friendship range 100 xmaximum 400 ymaximum 20
            text "Hostility:" size 20 color "#FFFFFF"
            bar value hostility range 100 xmaximum 400 ymaximum 20 bar_invert True  # Inverted to show high as "worse"
            null height 20
            textbutton "Close" action Hide("relationship_details") xalign 0.5 style "inventory_button"
screen heal_menu(player_obj):
    modal True
    frame:
        xsize 500
        ysize 550
        xalign 0.5
        yalign 0.5
        background "#111111"
        at transform:
            alpha 0.0
            linear 0.5 alpha 1.0

        vbox:
            spacing 20
            if not healing_progress:
                text "Select a Body Part to Heal" size 30 xalign 0.5 color "#FFFFFF" bold True
                for part in ["head", "body", "left_arm", "right_arm", "left_leg", "right_leg"]:
                    textbutton part.replace("_", " ").capitalize() action Show("medkit_item_menu", player_obj=player_obj, part=part) style "inventory_button" tooltip f"Heal {part} (Medical skill affects effectiveness)"
                textbutton "Cancel" action Hide("heal_menu") style "inventory_button" xalign 0.5
            else:
                text "I am healing a part already"
                textbutton "Cancel" action Hide("heal_menu") style "inventory_button" xalign 0.5

screen condition_details(player_obj, part):
    modal True
    frame:
        xsize 800
        ysize 600
        xalign 0.5
        yalign 0.5
        background "#111111"
        at transform:
            alpha 0.0
            linear 0.5 alpha 1.0

        vbox:
            xfill True
            spacing 20
            text f"{part.replace('_', ' ').title()} Status" size 40 xalign 0.5 color "#FFFFFF" bold True

            $ part_health = player_obj.health[part]['health']
            $ part_conditions = player_obj.health[part]['conditions']
            $ part_cleanliness = player_obj.health[part]['cleanliness']
            $ part_temp = player_obj.health[part]['temperature']
            $ can_view_health = player_obj.is_stat_higher("medical", 100)
            $ can_view_health_small = player_obj.is_stat_higher("medical", 59)
            $ has_thermometer = player_obj.inventory.has_item("thermometer")
            $ has_medkit = player_obj.inventory.has_item('medkit')
            $ medical_level = player_obj.stats.get("medical", {}).get("level", 0)
            $ pain_tolerance_bonus = player_obj.stats.get("pain_tolerance", {}).get("current_value", 0) / 10
            $ composure_bonus = player_obj.emotions.get("Composure", {}).get("value", 0) / 20
            $ adjusted_health_view = part_health + pain_tolerance_bonus + composure_bonus

            if can_view_health:
                text f"Health: {part_health}%" size 24 xalign 0.5 color "#FFFFFF"
                bar value part_health range 100 xmaximum 600 ymaximum 25 xalign 0.5 bar_invert (part_health < 50)
            elif can_view_health_small:
                text f"Estimated Health: {adjusted_health_view:.0f}%" size 24 xalign 0.5 color "#FFFFFF"
                if adjusted_health_view > 90:
                    text f"My {part} Feels Great!" size 24 xalign 0.5 color "#00FF00"
                elif adjusted_health_view > 50:
                    text f"My {part} Feels Fine." size 24 xalign 0.5 color "#FFD700"
                else:
                    text "It Hurts!" size 24 xalign 0.5 color "#FF0000"
            else:
                if part_health < (50 - pain_tolerance_bonus):
                    text "It Hurts!" size 24 xalign 0.5 color "#FF0000"
                else:
                    text "It feels alright." size 24 xalign 0.5 color "#AAAAAA"

            if can_view_health_small or (player_obj.emotions.get("Composure", {}).get("value", 0) > 50):
                text "Conditions:" size 30 xalign 0.5 color "#FFFFFF" bold True
                if part_conditions:
                    for condition in part_conditions:
                        text condition.capitalize() size 24 xalign 0.5 color "#CCCCCC"
                else:
                    text "No Current Conditions." size 24 xalign 0.5 color "#CCCCCC"
                text f"Hygiene: {part_cleanliness}%" size 24 xalign 0.5 color "#FFFFFF"
                bar value part_cleanliness range 100 xmaximum 600 ymaximum 25 xalign 0.5

            if has_thermometer or can_view_health or (player_obj.emotions.get("Authenticity", {}).get("value", 0) > 60):
                text f"Temperature: {part_temp}°F" size 24 xalign 0.5 color "#FFFFFF"
                bar value part_temp range 100 xmaximum 600 ymaximum 25 xalign 0.5

            if has_medkit:
                $ pride_bonus = player_obj.emotions.get("Pride", {}).get("value", 0) / 10
                $ heal_time = max(1, 10 - medical_level - pride_bonus)
                text f"Estimated Heal Time: {heal_time:.1f} minutes" size 20 xalign 0.5 color "#AAAAAA" italic True
                textbutton "Use Medkit" action Show("medkit_item_menu", player_obj=player_obj, part=part) style "inventory_button" xalign 0.5

            textbutton "Close" action Hide("condition_details") style "inventory_button" xalign 0.5

screen medkit_item_menu(player_obj, part):
    modal True
    frame:
        xsize 600
        ysize 500
        xalign 0.5
        yalign 0.5
        background "#111111"
        at transform:
            alpha 0.0
            linear 0.5 alpha 1.0

        vbox:
            spacing 20
            text "Select an Item to Use" size 30 xalign 0.5 color "#FFFFFF" bold True
            viewport:
                draggable True
                mousewheel True
                ysize 350
                vbox:
                    spacing 10
                    for item, info in medkit_contents.items():
                        python:
                            button_text = f"{item.capitalize()}"
                            if player_obj.is_stat_higher("medical", 40) or (player_obj.emotions.get("Intelligence", {}).get("value", 0) > 70):
                                button_text += f" (Heals: {', '.join(info['conditions'])}, Health: +{info['healing']})"
                        textbutton button_text action [Hide("medkit_item_menu"), Show("healing_confirmation", player_obj=player_obj, part=part, item=item)] style "inventory_button" tooltip "Apply to treat conditions (will take time)"
            textbutton "Cancel" action Hide("medkit_item_menu") style "inventory_button" xalign 0.5
screen healing_confirmation(player_obj, part, item):
    modal True
    frame:
        xsize 400
        ysize 200
        xalign 0.5
        yalign 0.5
        background "#111111"

        vbox:
            spacing 10
            text "Confirm Healing" size 30 xalign 0.5 color "#FFFFFF"
            python:
                base_time = 60 * 30  # Max 30 minutes in seconds (adjust scale if needed; e.g., for testing, divide by 60)
                composure_bonus = player_obj.emotions.get("Composure", {}).get("value", 0) / 5  # Reduce time
                confidence_penalty = max(0, 50 - player_obj.emotions.get("Confidence", {}).get("value", 0)) / 10  # Add time
                heal_duration = min(base_time, base_time * (1 - composure_bonus / 100) + (confidence_penalty * 30))  # Max 30 min
                heal_minutes = heal_duration / 60
            text f"This will take about {heal_minutes:.1f} minutes. Proceed?" size 20 xalign 0.5 color "#CCCCCC"

            hbox:
                xalign 0.5
                spacing 20
                textbutton "Yes" action [Hide("healing_confirmation"), Function(start_healing_timer, player_obj, part, item, heal_duration)] style "inventory_button"
                textbutton "No" action Hide("healing_confirmation") style "inventory_button"

screen healing_timer(heal_duration, player_obj, part, item):
    # Non-modal (modal False) so player can interact with game
    modal False
    zorder 200  # On top
    frame:
        xalign 1.0 yalign 0.0  # Top-right corner
        xsize 300 ysize 150
        background "#000000AA"
        vbox:
            spacing 5
            text "Healing in Progress..." size 24 xalign 0.5 color "#FFFFFF"
            text f"Time left: [healing_progress:.1f] / {heal_duration / 60:.1f} min" size 18 xalign 0.5 color "#CCCCCC"
            bar value healing_progress range 1.0 xmaximum 250 ymaximum 15 xalign 0.5  # Progress from 0 to 1

    # Repeating timer to update progress every 1 second
    timer 1.0 repeat True action SetVariable("healing_progress", min(1.0, healing_progress + (1.0 / heal_duration)))

    # Final timer to complete healing and hide
    timer heal_duration action [Function(player_obj.use_medkit_item, part, item), SetVariable("healing_progress", 0.0), Hide("healing_timer"), Notify("Healing complete!")]

default summary_rolls = {}
init python:
    def start_healing_timer(player_obj, part, item, heal_duration):
        # Reset progress
        global healing_progress
        healing_progress = 0.0
        renpy.show_screen("healing_timer", heal_duration=heal_duration, player_obj=player_obj, part=part, item=item)