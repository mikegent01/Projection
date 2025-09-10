default radio_mode_idx = 0
default radio_volume = 0.5
default radio_power = False
default radio_battery = 100

define RADIO_BATTERY_TICK_SECONDS = 60.0

init -1:
    style radio_text is default:
        color "#FFFFFF"
        outlines [(2, "#000000", 0, 0)]
    style radio_textbutton_text is radio_text

transform radio_big:
    xalign 0.5
    zoom 1.8

init python:
    if "radio_battery" not in config.overlay_screens:
        config.overlay_screens.append("radio_battery")

    radio_modes = ["CH 1", "CH 2", "CH 3", "CH 4"]
    DEFAULT_IDLE_TRACK = "SFX/radio/radio.wav"

    RADIO_LIBRARY = {
        "intreactivesection01": [
            { "file": "SFX/radio/EMS.mp3",           "loop": True  },
            { "file": "SFX/radio/radio.wav",         "loop": True  },
            { "file": "SFX/radio/ch0/fuelorder.wav", "loop": False },
            { "file": "SFX/radio/ch0/djoke.mp3",     "loop": False },
        ],
    }

    renpy.music.register_channel("radio", mixer="music", loop=True)

    def _radio_get_tracks_for_label():
        lb = getattr(renpy.store, "last_label", "intreactivesection01")
        return RADIO_LIBRARY.get(lb, RADIO_LIBRARY["intreactivesection01"])

    def apply_radio_volume():
        renpy.music.set_volume(max(0.0, min(1.0, renpy.store.radio_volume)), channel="radio")

    def radio_play_entry(entry):
        fallback = DEFAULT_IDLE_TRACK
        if not entry:
            renpy.music.play(fallback, channel="radio", loop=True)
            renpy.music.set_volume(renpy.store.radio_volume, channel="radio")
            return
        f = entry.get("file")
        loop_flag = bool(entry.get("loop", False))
        if loop_flag:
            renpy.music.play(f, channel="radio", loop=True)
        else:
            if f == fallback:
                renpy.music.play(f, channel="radio", loop=True)
            else:
                renpy.music.play(f, channel="radio", loop=False)
                renpy.music.queue(fallback, channel="radio", loop=True)
        renpy.music.set_volume(renpy.store.radio_volume, channel="radio")

    def radio_update_playback():
        if not renpy.store.radio_power:
            return
        tracks = _radio_get_tracks_for_label()
        i = max(0, min(renpy.store.radio_mode_idx, len(tracks) - 1))
        renpy.store.radio_mode_idx = i
        entry = tracks[i] if 0 <= i < len(tracks) else None
        radio_play_entry(entry)

    def radio_volume_down():
        renpy.store.radio_volume = max(0.0, round(renpy.store.radio_volume - 0.1, 2))
        if renpy.store.radio_power:
            renpy.music.set_volume(renpy.store.radio_volume, channel="radio")

    def radio_volume_up():
        renpy.store.radio_volume = min(1.0, round(renpy.store.radio_volume + 0.1, 2))
        if renpy.store.radio_power:
            renpy.music.set_volume(renpy.store.radio_volume, channel="radio")

    def radio_set_mode(i):
        renpy.store.radio_mode_idx = i
        if renpy.store.radio_power:
            radio_update_playback()

    def radio_power_on():
        if renpy.store.radio_battery <= 0:
            renpy.notify("Battery empty.")
            return
        renpy.store.radio_power = True
        radio_update_playback()
        apply_radio_volume()

    def radio_power_off():
        renpy.store.radio_power = False
        renpy.music.stop(channel="radio")

    def radio_on_show():
        if renpy.store.radio_power:
            radio_update_playback()
            apply_radio_volume()
        else:
            renpy.music.stop(channel="radio")

    def radio_battery_tick():
        if renpy.store.radio_power and renpy.store.radio_battery > 0:
            renpy.store.radio_battery -= 1
            if renpy.store.radio_battery <= 0:
                renpy.store.radio_battery = 0
                renpy.store.radio_power = False
                renpy.music.stop(channel="radio")
                renpy.hide_screen("radio_ui")
                renpy.notify("Battery depleted.")

screen radio_ui(style_prefix="radio"):
    modal True
    zorder 100
    on "show" action Function(radio_on_show)

    frame:
        xalign 0.5
        yalign 0.5
        background Solid("#000000b7")
        padding (12, 12, 12, 12)  # was: padding 12

        has vbox
        spacing 6

        hbox:
            spacing 12
            xalign 0.5
            textbutton "ON":
                action Function(radio_power_on)
                selected radio_power
            textbutton "OFF":
                action Function(radio_power_off)
                selected (not radio_power)

        $ vol_pct = int(round(radio_volume * 100))
        text "[radio_modes[radio_mode_idx]] • VOL [vol_pct]%":
            size 12
            xalign 0.5

        hbox:
            spacing 12
            xalign 0.5
            textbutton "CH 1":
                action Function(radio_set_mode, 0)
                sensitive radio_power
            textbutton "CH 2":
                action Function(radio_set_mode, 1)
                sensitive radio_power
            textbutton "CH 3":
                action Function(radio_set_mode, 2)
                sensitive radio_power
            textbutton "CH 4":
                action Function(radio_set_mode, 3)
                sensitive radio_power

        hbox:
            spacing 12
            xalign 0.5
            textbutton "− Vol":
                action Function(radio_volume_down)
                sensitive radio_power
            textbutton "+ Vol":
                action Function(radio_volume_up)
                sensitive radio_power

        add "inventory/radio.png" at radio_big

        textbutton "Close":
            xalign 0.5
            action Hide("radio_ui")

screen radio_battery(style_prefix="radio"):
    zorder 200
    if radio_power:
        timer RADIO_BATTERY_TICK_SECONDS repeat True action Function(radio_battery_tick)
        text "Battery: [radio_battery]%":
            xalign 1.0
            yalign 0.03
            xoffset -10
            size 12