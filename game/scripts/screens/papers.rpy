# Define styles to mimic the CSS
style scp_document_frame:
    background Solid("#ffffff")  # White paper background
    xpadding 40 ypadding 30
    xmaximum 800
    ymaximum 1000  # Limit the maximum height to prevent excessive scrollbar length
    align (0.5, 0.0)  # Center horizontally, align to top
    # Removed invalid duplicate background and outline; border simulated below

style scp_header_text:
    color "#000"
    size 24  # Slightly smaller to reduce overlapping
    bold True
    font "DejaVuSans.ttf"  # Default Ren'Py font; replace if needed

style scp_header_subtext:
    color "#555"
    size 12  # Slightly smaller
    font "DejaVuSans.ttf"
    kerning 2.0  # Use kerning to simulate letter-spacing

style scp_classification_box_outer:  # New style for outer border
    background Solid("#a00")
    padding (2, 2, 2, 2)
    align (1.0, 0.0)  # Align to top-right to avoid overlapping

style scp_classification_box_inner:
    background Solid("#ffffff")
    xpadding 10 ypadding 5

style scp_classification_text:
    color "#000"
    bold True
    size 12  # Smaller

style scp_classification_level:
    color "#a00"
    size 16  # Smaller
    bold True

style scp_memo_title:
    color "#000"
    size 20  # Smaller
    bold True
    align (0.5, 0.5)

style scp_memo_meta_outer:  # New for meta border simulation
    background Solid("#eee")
    padding (1, 1, 1, 1)

style scp_memo_meta_inner:
    background Solid("#f9f9f9")
    xpadding 15 ypadding 10
    size 14

style scp_content_text:
    color "#333"
    size 14  # Smaller to prevent overlapping
    justify True  # Mimics text-align: justify
    hover_color "#000"  # Change color on hover to simulate "selectability"

style scp_footer_text:
    color "#777"
    size 10  # Smaller
style image_security_code_text:
    color "#777"
    size 10  # Smaller
    align (0.4, 0.4)
style scp_divider:
    background Solid("#ccc")
    ysize 1
    xfill True
    ymargin 20

style scp_content_divider:
    background Solid("#eee")
    ysize 1
    xfill True
    ymargin 15

style scp_viewport_inner_frame:
    background None  # Transparent background
    xpadding 20 ypadding 20

# 001 definition
screen scp_memo():
    frame:
        style "scp_document_frame"
        viewport:
            yadjustment ui.adjustment()  # Directly use ui.adjustment() for scrolling
            mousewheel True  # Allows scrolling with mouse wheel
            scrollbars "vertical"  # Shows a vertical scrollbar
            ysize 900  # Set a fixed height for the viewport to control scrollbar length (adjust as needed)

            # Inner frame for padding
            frame:
                style "scp_viewport_inner_frame"

                # Main content vbox with extra spacing
                vbox:
                    spacing 20  # Increased spacing to prevent overlapping

                    # Simulate thick top border with a black bar at the top
                    fixed:
                        ysize 5
                        xfill True
                        add Solid("#000")

                    # SCP Header
                    hbox:
                        spacing 20
                        yalign 0.0  # Align to top to prevent vertical overlapping

                        # Logo (made smaller: reduced fixed size and zoom)
                        fixed:
                            xsize 40 ysize 40  # Smaller container
                            align (0.5, 0.0)  # Align to top
                            add "images/news/SCP_Foundation_(emblem).svg" at truecenter:  # Adjust path if needed
                                xzoom 0.1 yzoom 0.1  # Smaller scale (adjust as needed)

                        # Header Text
                        vbox:
                            xfill True
                            yalign 0.0  # Align to top
                            spacing 5  # Space between header lines
                            text "SCP FOUNDATION" style "scp_header_text"
                            text "SECURE. CONTAIN. PROTECT." style "scp_header_subtext"

                        # Classification Box (simulated border)
                        frame style "scp_classification_box_outer":
                            frame style "scp_classification_box_inner":
                                vbox:
                                    spacing 3  # Space inside classification box
                                    text "[ 'LEVEL 3 CLEARANCE REQUIRED'.upper() ]" style "scp_classification_text"
                                    text "[ 'CLASSIFIED'.upper() ]" style "scp_classification_level"

                    # Divider
                    null style "scp_divider"

                    # Letter Content
                    vbox:
                        spacing 15  # Increased spacing

                        text "[ 'INTERNAL MEMORANDUM #0001'.upper() ]" style "scp_memo_title"

                        # Memo Meta (simulated border)
                        frame style "scp_memo_meta_outer":
                            frame style "scp_memo_meta_inner":
                                vbox:
                                    spacing 5  # Space between meta lines
                                    text "{b}Date:{/b} ██████████" style "scp_content_text"
                                    text "{b}From:{/b} O5-██ / Dir. B█████" style "scp_content_text"
                                    text "{b}To:{/b} Site Director REDACTED, Alpha-1 Lead" style "scp_content_text"
                                    text "{b}Subject:{/b} Anomaly Survey - Operation REDACTED" style "scp_content_text"

                        null style "scp_content_divider"

                        text "When this memorandum is received and acknowledged, standard data sanitization protocols apply. Destroy physical copies after digital confirmation." style "scp_content_text"
                        text "Stabilization efforts appear successful following initial containment. Primary anomaly source confirmed at coordinates X██.Y████, Z██.A████. Entity designation pending, it exhibits reality-bending properties of significant magnitude, though containment appears feasible. You will lead Mobile Task Force Alpha-1 (\"Red Right Hand\") designation pending to conduct thorough reconnaissance of the affected area. Gather all available data on entity behavior, properties, and local environmental effects. If the entity becomes aware of MTF presence, immediately initiate Protocol Chimera-Gamma as outlined in Addendum 0001-A (Ref: Doc ███-██). Do {b}NOT{/b} deviate." style "scp_content_text"
                        text "Standing orders from O5 Command explicitly forbid direct interaction with the anomaly at this stage. Continuous passive surveillance is authorized until further notice or issuance of an engagement order. Prioritize personnel safety and data integrity." style "scp_content_text"
                        text "Attached is the final image transmitted by Exploration Team Bravo-2 prior to signal loss. Recover their data packet; its contents are considered critical intelligence. Deliver recovered materials directly to Site-19 secure archives upon return." style "scp_content_text"

                        # Attached Image with rotation and hover effect (uncommented and adjusted)
                        null height 25  # Simulate top margin
                        frame:
                            xalign 0.5
                            background Frame(Solid("#fdfdfd"), Borders(5, 5, 5, 5), tile=False)
                            add Transform("images/news/house.png", rotate=-1.5, zoom=0.3)
                            hover_background Frame(Solid("#fdfdfd"), Borders(5, 5, 5, 5), tile=False)  # If needed for hover

                    # Footer with extra margin
                    text "Image Security Code: 51856." style "image_security_code_text"
                    null height 30  # Add space before footer
                    textbutton "Close" action [ Hide("scp_memo")] 
                    
                    null height 20  # Padding at the bottom to shorten scrollbar
                    fixed:
                        ysize 5
                        xfill True
                        add Solid("#000")
                    text "Document 001-M-0001 - Property of the SCP Foundation & DOD - Unauthorized Access Prohibited" style "scp_footer_text"
# ---------------- Helpers & Transforms ----------------
init -2 python:
    # Simple horizontal rule
    def hr(color="#dddddd", height=1):
        return Frame(Solid(color), 0, 0, tile=False, xsize=1, ysize=height)

transform paper_shadow:
    alpha 0.20
    xoffset 0
    yoffset 18

transform paper_appear:
    on show:
        alpha 0.0
        linear 0.18 alpha 1.0
    on hide:
        linear 0.12 alpha 0.0

transform tab_float:
    subpixel True
    rotate -2
    yoffset -14
########################################################################################
########################################################################################
########################################################################################


# ---------------- Styles ----------------
init -1:
    # Paper look
    style paper_card is frame
    style paper_card:
        background Solid("#fffdf8")    # soft off-white paper
        padding (34, 28)

    # Text styles
    style paper_text is default
    style paper_text:
        size 24
        color "#222"
        line_spacing 3

    style paper_title is paper_text
    style paper_title:
        size 30
        bold True
        color "#1a1d21"
        xalign 0.5
        text_align 0.5

    style paper_meta is paper_text
    style paper_meta:
        size 18
        color "#5a6573"

    style paper_body is paper_text
    style paper_body:
        size 24
        color "#2a2f36"

    style paper_ip_frame is frame
    style paper_ip_frame:
        background Solid("#f2f4f7")
        padding (16, 14)
        left_padding 20
        right_padding 20
        xalign 0.5

    style paper_ip_text is paper_text
    style paper_ip_text:
        size 28
        color "#121417"
        bold True
        xalign 0.5
        text_align 0.5

    style paper_warn is frame
    style paper_warn:
        background Solid("#fff3f3")
        padding (12, 10)
        left_padding 16
        right_padding 16

    style paper_warn_text is paper_text
    style paper_warn_text:
        size 22
        color "#8f1b1b"
        bold True
        xalign 0.5
        text_align 0.5

    style paper_footer is paper_text
    style paper_footer:
        size 16
        color "#67707a"
        xalign 0.5
        text_align 0.5

    # Tab label
    style paper_tab is frame
    style paper_tab:
        background Solid("#f4d06f")   # manila/yellow tab
        padding (8, 6)
        left_padding 14
        right_padding 14

    style paper_tab_text is text
    style paper_tab_text:
        size 18
        color "#3a2f12"
        bold True

    # Scrollbar + Buttons
    style paper_vbar is vscrollbar
    style paper_vbar:
        xsize 10
        unscrollable "hide"

    style paper_btn is button
    style paper_btn:
        background Solid("#e9eef5")
        hover_background Solid("#dde6f2")
        xpadding 16
        ypadding 10

    style paper_btn_text is button_text
    style paper_btn_text:
        color "#1c2a3a"
        size 20
        bold True

    style paper_btn_primary is button
    style paper_btn_primary:
        background Solid("#1e3a5f")
        hover_background Solid("#2a4d7e")
        xpadding 18
        ypadding 10

    style paper_btn_primary_text is button_text
    style paper_btn_primary_text:
        color "#ffffff"
        size 20
        bold True


# ---------------- 002 ----------------
screen network_notice(
    date="4/18/XX",
    notice_id="OSNW-CHG-8831-B",
    sector="REDACTED",
    new_ip="136.228.116.222",
    old_ip="136.228.116.222",
    paper_label="002",
    bg_image=None
):
    modal True
    zorder 100

    if bg_image:
        add bg_image
    add Solid("#00000088")

    # Target paper size: big, but with a safe margin so nothing clips.
    $ paper_w = int(min(config.screen_width - 48, config.screen_width * 0.92))
    $ paper_h = int(min(config.screen_height - 48, config.screen_height * 0.88))

    # These match style paper_card: padding (34, 28)
    $ pad_x = 34
    $ pad_y = 28

    # Inner height for the viewport (fit inside padding)
    $ inner_h = max(200, paper_h - (pad_y * 2))

    fixed:
        xalign 0.5
        yalign 0.5
        xminimum paper_w
        yminimum paper_h
        xmaximum paper_w
        ymaximum paper_h

        # Soft shadow
        add Solid("#000000") at paper_shadow

        # Paper
        frame style "paper_card" at paper_appear:
            xsize paper_w
            ysize paper_h

            # Scrollable content + internal scrollbar
            hbox:
                spacing 8
                xfill True
                yfill True

                viewport id "paper_vp":
                    xfill True
                    ysize inner_h
                    mousewheel True
                    draggable True

                    vbox:
                        spacing 12
                        xfill True
                        # Content padding lives inside the viewport so text doesn't hug edges

                        # Title + Meta
                        text "Notice of Internet Protocol Address Change" style "paper_title"
                        add Frame(Solid("#e3e7ed"), 0, 0, tile=False, xsize=1, ysize=1)

                        text "Date Printed: [date]" style "paper_meta"
                        text "Notice ID: [notice_id]" style "paper_meta"

                        null height 8
                        add Frame(Solid("#e9edf3"), 0, 0, tile=False, xsize=1, ysize=1)
                        null height 8

                        # Body
                        text "This is an automated message generated for system administrators and relevant personnel." style "paper_body" xfill True
                        text "Please be informed that the primary gateway IP address for Sector [sector] has been updated. The new IP address is:" style "paper_body" xfill True

                        frame style "paper_ip_frame":
                            xfill True
                            text "[new_ip]" style "paper_ip_text"

                        text "This replaces the previous IP address [old_ip] effective immediately. Ensure all services, firewalls, or configurations dependent on the old IP are updated to maintain operational continuity." style "paper_body" xfill True

                        null height 10
                        add Frame(Solid("#eef1f5"), 0, 0, tile=False, xsize=1, ysize=1)
                        null height 8

                        text "If you have any questions or require technical assistance, please contact Network Operations Command via secure channels." style "paper_body" xfill True

                        frame style "paper_warn":
                            text "DO NOT DISCARD THIS NOTICE. FILE APPROPRIATELY." style "paper_warn_text"

                        add Frame(Solid("#f3f5f8"), 0, 0, tile=False, xsize=1, ysize=1)
                        text "Classification: UNCLASSIFIED // FOR OFFICIAL USE ONLY" style "paper_footer"

                        null height 10

                        hbox:
                            xalign 1.0
                            spacing 10
                            textbutton "Close" style "paper_btn_primary" action Hide("network_notice"):
                                keysym "K_ESCAPE"

                # Vertical scrollbar stays inside the paper
                vbar value YScrollValue("paper_vp") style "paper_vbar"

        # Tab label pinned to the paper’s top-right corner
        frame style "paper_tab" at tab_float:
            xalign 1.0
            yalign 0.0
            xoffset -10
            yoffset -10
            text "[paper_label]" style "paper_tab_text"

########################################################################################
########################################################################################
########################################################################################
# Define styles (same as before, using defaults since fonts were removed)
style masthead_title:
    size 60
    color "#111"
    xalign 0.5

style sub_title:
    size 18
    color "#555"
    xalign 0.5
    italic True

style date_issue:
    size 16
    color "#666"

style headline:
    size 48
    color "#000"
    bold True

style byline:
    size 18
    color "#444"
    italic True

style story_text:
    size 18
    color "#222"
    justify True

style image_caption:
    size 16
    color "#555"
    italic True
    xalign 0.5

style page_footer:
    size 14
    color "#777"
    xalign 0.5

# 003
screen vatican_newspaper():
    window:
        background "#fdfaf600"  # Off-white background

    frame:
        align (0.5, 0.5)
        maximum (900, None)  # Width fixed, height flexible
        background "#fff"
        padding (25, 25)
        has vbox:
            spacing 20

            # Masthead (fixed at top, not scrollable, with border simulation)
            vbox:
                spacing 10
                xfill True
                text "The Vatican Chronicle" style "masthead_title"
                text "Reporting Truth, Faith, and Global Events" style "sub_title"
                hbox:
                    xfill True
                    spacing 20
                    text "VOL. CLXXXV, NO. 003" style "date_issue" xalign 0.0
                    text "WEDNESDAY, AUGUST 10" style "date_issue" xalign 0.5
                    text "PRICE: $2.50" style "date_issue" xalign 1.0

                null height 5  # Space
                frame:  # Border bottom simulation
                    xfill True
                    ysize 3
                    background Solid("#333")

            # Scrollable content area (using hbox for viewport + scrollbar to avoid side errors)
            hbox:
                spacing 10  # Space between content and scrollbar

                viewport id "vp":
                    ymaximum 1000  # Max visible height before scrolling (adjust as needed)
                    yadjustment ui.adjustment()  # Proper Adjustment object
                    mousewheel True  # Allows mouse wheel scrolling
                    draggable True  # Allows dragging to scroll
                    xfill True  # Take available width

                    vbox:
                        spacing 20
                        xfill True

                        if config.screen_width > 768:
                            # Main Story (full width now, no sidebar)
                            frame:
                                xfill True
                                background None  # Transparent for newspaper feel
                                has vbox:
                                    spacing 15

                                    text "PETER THE ROMAN: Vatican City Witnesses Historic Coronation As New Pontiff Ascends Papal Throne" style "headline"

                                    text "By Our Vatican Correspondent, ANGELO ROSSI" style "byline"

                                    image "news/pope.png":  # Image path updated
                                        xalign 0.5
                                        yalign 0.5
                                        xzoom 1.0

                                    text "This photo captures Pope Peter the Roman from an upper angle as he looks forward, with a backdrop of clouds." style "image_caption"

                                    # Story text in a single block to avoid any squishing (combined for full width flow)
                                    text """{size=48}{b}V{/b}{/size}ATICAN CITY – After an unprecedented two months of waiting and debate, white smoke has arisen from the holy city. Thousands of Catholics descended upon St. Peter’s Square to celebrate the coronation of the new Pope. This comes after a tense few months of uncertainty as the papal conclave failed to produce a new Pope. The Vatican has chosen to give the role of Pope to a relatively unknown cardinal from Venice. The Pope, who donned the name Petrus Romanus, said in his opening Urbi et Orbi address, “Io sono infatti persuaso che né morte né vita, né angeli né principati, né presente né avvenire, né potenze, né altezza né profondità, né alcun’altra creatura potrà mai separarci dall’amore di Dio che è in Cristo Gesù, nostro Signore.” The choice of this quote from Romans 8:38-39 resonates with the public as many Catholics look to God for guidance in these trying times. Many analysts say the Pope is a compromise Pope. Not much is known about how the Pope will lead the Holy See; however, the choice of name for the Pope holds great significance as it is a direct reference to the prophecy of Petrus Romanus about a Pope named Peter the Roman who will pasture his sheep in many tribulations. When these things are finished, the city of seven hills will be destroyed, and the dreadful judge will judge his people. When asked, the Vatican declined to comment. Nevertheless, this Pope will offer guidance to many Catholics who feel lost or abandoned during the four-month period now known by many, including non-Catholics, as “The Black Months.”""" style "story_text"

                        else:
                            # Stacked layout for smaller screens (single column, full width)
                            vbox:
                                spacing 20

                                # Main Story
                                text "PETER THE ROMAN: Vatican City Witnesses Historic Coronation As New Pontiff Ascends Papal Throne" style "headline" size 36  # Smaller headline

                                text "By Our Vatican Correspondent, ANGELO ROSSI" style "byline"

                                image "news/pope.png":
                                    xalign 0.5
                                    yalign 0.5
                                    xzoom 0.8  # Slightly smaller for mobile

                                text "This photo captures Pope Peter the Roman from an upper angle as he looks forward, with a backdrop of clouds." style "image_caption"

                                # Single-column story text (kept exactly as in HTML, combined)
                                text """{size=48}{b}V{/b}{/size}ATICAN CITY – After an unprecedented two months of waiting and debate, white smoke has arisen from the holy city. Thousands of Catholics descended upon St. Peter’s Square to celebrate the coronation of the new Pope. This comes after a tense few months of uncertainty as the papal conclave failed to produce a new Pope. The Vatican has chosen to give the role of Pope to a relatively unknown cardinal from Venice. The Pope, who donned the name Petrus Romanus, said in his opening Urbi et Orbi address, “Io sono infatti persuaso che né morte né vita, né angeli né principati, né presente né avvenire, né potenze, né altezza né profondità, né alcun’altra creatura potrà mai separarci dall’amore di Dio che è in Cristo Gesù, nostro Signore.” The choice of this quote from Romans 8:38-39 resonates with the public as many Catholics look to God for guidance in these trying times. Many analysts say the Pope is a compromise Pope. Not much is known about how the Pope will lead the Holy See; however, the choice of name for the Pope holds great significance as it is a direct reference to the prophecy of Petrus Romanus about a Pope named Peter the Roman who will pasture his sheep in many tribulations. When these things are finished, the city of seven hills will be destroyed, and the dreadful judge will judge his people. When asked, the Vatican declined to comment. Nevertheless, this Pope will offer guidance to many Catholics who feel lost or abandoned during the four-month period now known by many, including non-Catholics, as “The Black Months.”""" style "story_text"

                        # Footer (inside scrollable area, at bottom, with top border)
                        null height 30
                        frame:
                            xfill True
                            ysize 1
                           # background Solid("#eee")
                        null height 10
                        text "The Vatican Chronicle • Serving the Faithful Since 1838 • All Rights Reserved © 20XX" style "page_footer"

                vbar value YScrollValue("vp")  # The scrollbar

    # Optional: Close button and key
    textbutton "Close" action Hide("vatican_newspaper") align (0.98, 0.02)
########################################################################################
########################################################################################
########################################################################################
screen cuz_document():
    modal True
    zorder 100

    add Solid("#00000088")

    $ paper_w = int(min(config.screen_width - 48, config.screen_width * 0.92))
    $ paper_h = int(min(config.screen_height - 48, config.screen_height * 0.88))
    $ pad_x = 34
    $ pad_y = 28
    $ inner_h = max(200, paper_h - (pad_y * 2))

    fixed:
        xalign 0.5
        yalign 0.5
        xminimum paper_w
        yminimum paper_h
        xmaximum paper_w
        ymaximum paper_h

        # Soft shadow
        add Solid("#000000") at paper_shadow

        # Paper frame
        frame style "paper_card" at paper_appear:
            xsize paper_w
            ysize paper_h

            hbox:
                spacing 8
                xfill True
                yfill True

                viewport id "cuz_vp":
                    xfill True
                    ysize inner_h
                    mousewheel True
                    draggable True

                    vbox:
                        spacing 12
                        xfill True

                        text "Know your Hazard - Sheet 001 - C.U.Z – DOD – SITE 12" style "paper_title"
                        add Frame(Solid("#e3e7ed"), 0, 0, tile=False, xsize=1, ysize=1)

                        text "Object: Contaminated Unbalanced Zones" style "paper_body"
                        text "Class: Hazardous" style "paper_body"

                        null height 10

                        text "Description: Colloquially known as unstable zones are places were grounded land is unable to reach hydrostatic equilibrium causing any matter that comes into contact with it to undergo a state of momentary super position until the matter collapses in on itself until it ends up in another position. This new position has yet to be located and has formally been dubbed the backrooms. A series of tests for this demonstration were ran for educational purposes here are there results." style "paper_body"

                        null height 10
                        text "Test Results" style "paper_meta"
                        image "images/news/table01.png" 


                        null height 15

                        text "Avoidance: All known unstable zones have been marked with caution tape and are located in secure areas, however it is best to adhere to the following guidelines if another one is found:" style "paper_body"

                        text "• Do not come into contact anywhere near the zone in a 5x5x5 area" style "paper_body"
                        text "• Do inform your nearest research associate" style "paper_body"
                        text "• Do not attempt to secure the area" style "paper_body"
                        text "• Do prevent anyone from entering the area" style "paper_body"

                        null height 10
                        text "Normal View                | Blue light Source:" style "paper_meta"
                        hbox:
                            spacing 20
                            image "images/news/normal.png" xzoom 0.4 yzoom 0.4
                            image "images/news/underhyperscope.jpg" xzoom 0.4 yzoom 0.4

                        null height 10
                        text "Conclusion: The Contaminated Unbalanced Zones have evolved from there initial finding leading to them being a staple in dimensional research, many excavations teams and researchers use these as entryways into the world beyond" style "paper_body"

                        null height 20
                        textbutton "Close" style "paper_btn_primary" action Hide("cuz_document") xalign 0.5

                vbar value YScrollValue("cuz_vp") style "paper_vbar"

        frame style "paper_tab" at tab_float:
            xalign 1.0
            yalign 0.0
            xoffset -10
            yoffset -10
            text "004" style "paper_tab_text"
