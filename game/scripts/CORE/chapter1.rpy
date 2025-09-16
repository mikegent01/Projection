default current_chapter = 0
default game_state = {
    "major_items": {
        "projector": {
                "projector_status": "broken", 
                "projector_health": 5, # when 0 game over
                "projector_backplate": False,
                "films_in_projector": 2,
                "projector_durability": 100,
                "screws_in_projector": 7,
                "duel_screw_attached": False
            }
    },
    "rolls": {
        "roll_results": {}
    },
    "chapter_1": {
        "projector_room": {
            "picked_tissue_up": False,
            "viewed_tutorial": False,
            "driwalkedaway": False
        }
    }
}