
default test_room = 0
default preferences.text_cps = 30
label start:
    #     $ quick_menu = False uncomment on deployment
    $ player.apply_room_temperature(72)
    $ player.inventory.add_item("Classified Mission Sheet")
    $ player.inventory.add_item("Radio")
    $ player.inventory.add_item("Paper")
    $ player.inventory.add_item("Pencil")
    play music "audio/Music/Boot Camp/boot_camp.mp3" volume 0.5 
    $ missions["active"].append({
        "title": "Repair the projector",
        "description": "I need to figure out how to repair the projector. The drill sargent ordered me to repair it but I have never fixed anything in my life...",
        "objectives": ["Find a speciality screwdriver", "Replace the front lens", "Replace the back plate","Test the power supply"], 
        "progress": 0, 
    })
    
    $ missions["active"].append({
        "title": "Order a new uniform",
        "description": "I came in to todays meeting without a proper uniform, I should work on getting a new one. I can try looking at the main desk or I can try to ask around for someone that would have a uniform.",
        "objectives": ["Talk to the quartermaster at front desk", "Check the supply room", "Go to the military shop"], 
        "progress": 0,
    })    
    scene stage1 with None
    show screen stagecurtians
    show screen samuel
    show screen drill_sargent
    show screen game_screen
    $ movement_enabled = False
    BEN "I can only feel excitement, as I finally go to sit down."
    scene satgescene9 with None
    BEN "We are going on a real mission, no more training, no more drills. I finally can put my skills to good use."
    BEN "I have accepted my fate long before I woke up this morning knowing what this job entailed"
    BEN "and I intend to make this mission a success by myself."
    scene ani2_background with None
    "I sit down on a wooden chair."
    "people around me muttering and talking."
    "The dampness from the old moldy brick walls."
    scene drillsargpickup with None
    "And the sweat of the soldiers who just got back from training."
    scene 0drillsargpickupstart with None
    "Almost distracts me from the fact that I forgot to put on my uniform this morning."
    "The soldiers all sit in rows of chairs, laid out in a linear sequence, ridged but not sturdy."
    "The room is packed with soldiers and people."
    scene anistagescene
    "A thud sound is made from the front of the room. A metallic box item is placed on the table"
    "the box having a single lens at the front of it and two films atop of it."
    scene 0drillsargpickupstart0
    "The box is dusty; it looks familiar but it is alien to me. As I deliberate on this"
    "a clicking sound plays, and after a moment the room goes quiet."
    "a soft hum starts emanating from the machine."
    scene projector_hum_animation 
    "The box whirls to life, it clicks for a second, and then for only a second there was nothing. Another hitch and there was light."
    show dim_overlay onlayer dimming_layer
    "The light in the room dims, the creaking of the chairs stop" 
    "a familiar figure stands directly infront of the light. Ridged and firm"
    "the familiar figure stands at attention,"
    "and another hitch is herd from the box."
    scene burn1drillsargpickup
    "The light shines bright as the box shows a singular video of a beam." 
    "A beam with the power to destroy cities..."
    "The silence is broken when drill sergeant Jones begins speaking "

    DRI "Men, these are the facts as I understand them: approximately 5 hours ago a class A event occurred near Ruckersville Virginia."
    DRI "We promptly sent a Incident Relief Division to investigate the scene and received reports of a rift in the earth opening up "
    DRI "and several sightings of unknown creatures before we lost contact due to power outages."
    DRI "You will have two jobs: one team's job will be to find out what happened to the team and to terminate every threat,"
    DRI "and the other team will be in charge of securing a suspected target that caused this mess."
    DRI "This is not simply a security problem anymore as fellow members of the army and civilians lives are at stake."
    DRI "I have full confidence in all of you; you are the best unit in the force and I expect you will be ready."

    "The room remains silent with no one but me moving there eyes from the Sargent as he talks" 
    "there is a tense anticipation for what he will say next."
    DRI "This box here is a projector, here is of upmost importance, while it may look mundane and normal…"
    "he takes out the tape and a sound begins playing"
    DRI "But These tapes it plays are capable of playing sounds at a higher decibel frequency than humans can hear."
    DRI "These tapes right here do contain image data, but they also contain data that will play sounds at high decibels" 
    "that are able to plug these rifts."
    DRI "I am not to well versed in the science behind it, but I am told if this tape is played at the center of one of these rifts,"
    DRI "they may close and return to normal. Therefore this tape will be designated as a class A important object."

    "As I look at the projector I notice a hitch in it."
    "The projector seems to stall for a second before starting up again."
    DRI "We are to deploy to a nearby military base tonight. We won’t close these rifts tonight"
    "as we still need a key component to making this technology work."
    DRI "You will be briefed further on this situation during the beginning of the mission tonight."
    DRI "You will also receive authorization to classified information.If you are unable to keep a secret please see me." 
    "That is all You are hereby dismissed."
    hide dim_overlay onlayer dimming_layer 
    show light_turning_on_effect 
    scene stage1unplug_animation 

    "As the lights turn on and the room so does the sound, people start talking amongst themselves"
    "some personal start leaving the room."
    "I feel a slight tap on my shoulder it is from one of my “friends” private Samuel."
    SAM "Psst hey Benjerman"
    "he then hands me a sheet of paper"
    SAM "I was told you would like this it is a report on what happened, there is some stuff in there that I can’t even understand."
    "I feel the sheet fall on my lap as he places it there."

    "I look up at the projector it hitches again as the drill Sargent messes with the plug trying to unplug it."
    "He moves it back and forth in a wiggling motion but it seems to be stuck."
    "It eventually pops out and a spark occurs at the outlet and the projector starts heating up and smoking."
    DRI "..."
    "The drill sargent looks visibly concerned and than looks directly at me staring at him."
    DRI "You, meatbag your just who I need!"

    "I arrive at his location he looks down at me with a scowl."
    DRI "This projector is broken, I am not sure how it broke and it looks like your not doing anything of importance" 
    "therefore your in charge of fixing it"
    "I look at him semi annoyed, he looks back"
    DRI "do you understand what you need to do?"
    BEN "yes sir!"
    DRI "sound off like you got a pair"
    BEN "SIR YES SIR"
    DRI "good you are dismissed."

    "As I turn around I notice two people sitting in there seats, prehaps I should talk to one of them and ask them for help."
    show screen checkKey  
    show screen HUD

label intreactivesection01:
    if not game_state["chapter_1"]["projector_room"]["viewed_tutorial"]:
        scene empty_stage_animation with None
        show light_turning_on_effect
        "I realize my contacts are not in ..."
        "My body feels lighter, I should get my bearings.."
        $ movement_enabled = True
        $ game_state["chapter_1"]["projector_room"]["viewed_tutorial"] = True
        window hide
        $ renpy.pause(45.0, hard=True)


    if not game_state["chapter_1"]["projector_room"]["driwalkedaway"] and movement_enabled:
        scene walkaway1 at fit_screen
        $ renpy.pause(0.85, hard=True)
        $ game_state["chapter_1"]["projector_room"]["driwalkedaway"] = True
        jump intreactivesection01
    else:
        scene expression "images/bg/Starting_Room/9/walkaway9.png" at fit_screen
        $ renpy.pause()  
label DrillSergeantTalk:
    $ movement_enabled = False
    DRI "What is it maggot"
    BEN "I was wondering if you could go over what I need to do one more time."
    DRI "I have a important meeting to get to and I will NOT be late"
    DRI "So write this down somehwere, you FIRST need to repair your projector."
    DRI "Than you need to get yourself in proper uniform!"
    BEN "Oh i-."
    DRI "You better have got all of that maggot! I need to go."
    $ game_state["chapter_1"]["projector_room"]["driwalkedaway"] = True
    $ movement_enabled = True
    scene walkaway1
    jump intreactivesection01
label FrontSeat:
    hide screen HUD
    hide screen tutorial_screen
    hide screen checkKey    
    window show     
    scene bootcampinsideprojectorroomstartm # Or appropriate scene
    "Although I much rather do this myself I have no other options, I walk up towards the front seat the man is small in stature the only defining trait about him I can notice is his turban."
    SUL "..."
    "Regrettably walking up to him he doesn’t notice me I decide to observe what has taken so much of his attention."
    "As I peer closer at him to find out what he is fiddling with I realize he is trying to light a cigar, he is unable to get the match to light."
    "I wait another few seconds before questioning him"
    BEN "What are you doing?"
    hide sultan_talking_pose
    show sultan_talk_pose at right
    SUL "Nothing bro don't worry about it"
    BEN "You know there is a fire sensor above your seat right?"
    SUL "Look bro I barely even know you; you don’t talk to anyone and now you decide to talk to me? What do you want money?"
    "I wait for him to continue feeling the paper that Samuel gave me crumple in my hand."
    SUL "Look” He holds out a $10 bill giving it to me “Just don't tell anyone what you saw okay?"
    BEN "I refuse to take the money instead asking him to help me."
    BEN "I need you to go and help me out with something."
    SUL "What is it bro?"
    BEN "Do you have any idea on how to fix a projector?"
    SUL "P-Projector? You mean that thing the sarg was showing off bro you broke it?”"
    "He gets up quickly and begins packing up his stuff"
    SUL "N-no no I wouldn’t know anything about the projector."
    "He wips has bag around and puts it on his back. He begins to walk out"
    BEN "Wait! Listen to me"
    "he continues to walk out before I run up to him and place a hand on his shoulder."
    BEN "We are both on the same side here it’s the drill sergeants fault listen."
    "A quiet spark is heard only for a moment and smoke comes out from in front of the man he stops and takes a deep breath and says"
    SUL "I would stay away from that projector but If you can’t fix it yourself I would ask Samuel for advice. He seems to follow you around anyway for some reason."
    "He walks out of the room."
    hide sultan_talk_pose

    "As I walks up to the projector I look at the pulled out plug and the electrical residue next to the outlet, I pick up the film the projector left on the desk and look at it"
    "there is crossed out text on it AAXA SCP-A01 I put the film down and pick up the projector itself feeling the hard and bumpy texture looking at the back of it there appears to be a panel held in with screws"
    "as I look at the projector I feel a tap"
    show drill_sarg_talk at right
    "the drill Sargent is still standing there staring at me, I think to myself how long could he have been there waiting before asking him for a screwdriver."
    DRI "I have a very important meeting to attend to, once I am back the mission will begin. Id recommend looking for it yourself,"
    DRI "you need a specialty screwdriver for this and I am not too sure were we keep them. Why don’t you go ask the people at the main desk maybe they can help."
    hide drill_sarg_talk
    hide ben neutral

    jump OutsideAfterScrewdriverAdvice

label BackSeat:
    hide screen HUD
    hide screen tutorial_screen
    hide screen checkKey    
    window show    
    $ move_to_pos(130,450)
    "I head towards the backseat, the person in the backseat seems to have something over there head, it looks like a paper bag."
    show bagman_default at right
    BAG "..."
    "There is a brief moment of hesitancy before I recoil once than I tap the tall man with the bagged head on his shoulder."
    "He turns around shocked revealing there to be a crudely cut out face on the bag."
    BAG "..."
    "I couldn’t tell the emotion on his face but I could feel it. I could feel the heat coming out of his mask. I can hear his heavy breathing,"
    "the bag motioning in and out slowly and rhythmically. I took a slight step back but than he no it spoke up, the bag made a slight ruffling sound"
    "and a gruff and heavy voice came out of what was constraining it."
    BAG "yes c-can I he-help you"
    "the man voice cracks I with an ear pinching tone, there is a slight squeak in his tone."
    "I do a silent sigh of relief at him in the eyes"
    BEN "The projector is broken and the sarge wanted me to fix it. Do you have any advice or knowledge on how to fix this."
    "I wait my response until he speaks up"
    BAG "y-you will need a specialty screwdriver and t-to be careful that thing is dangerous…."
    "He takes another deep breath but not as deep as before he continues on with"
    BAG "I-if I were you I wouldn’t even touch that thing, I-…"
    "He deliberates on his words for a moment; as he does the feeling of unease returns from before the air becomes thicker and the bag on his head becomes more animated he continues on"
    BAG "I can’t say any more…. I-I have to go."
    "He quickly continues packing up his supplies and rushes out, I don’t stop him."
    hide bagman_default

    "With that advice I decide that I shouldn’t touch the projector and I should look for the screwdriver instead as I am leaving I hear the drill Sargent call out to me."
    "I realize he is still standing. He is observing me, I think to myself how long could he have been there waiting before asking him for the specialized screwdriver."
    show drill_sarg_talk at right
    DRI "I have a very important meeting to attend to, once I am back the mission will begin. Id recommend looking for it yourself,"
    DRI "Why don’t you go ask the people at the main desk maybe they can help."
    hide drill_sarg_talk # Corrected from drill_s_talk
    hide ben neutral

    jump OutsideAfterScrewdriverAdvice

label OutsideAfterScrewdriverAdvice:
    scene bg_outside_projector_room
    show ben neutral at center
    "Having no other choice I walk outside."
    "As I walked outside I felt the cool stale air from the indoor air conditioner, I smile as the meeting is finally over."
    "I feel the drill sargent rush past me as he heads to his meeting. I watch him run off to the left in a hurry from waiting for me for this long"
    "until I look to the right seeing someone I recgonize. My smile quickly fades into a frown as I look up to see a face I did not want to see."
    "It is Samuel, I think to myself if it is really worth it talking to him."
    show samuel_redbook at right
    "It could lead me into more trouble than its worth I finally decide"
    menu:
        "follow him":
            jump keepsamuel
        "go on my own":
            jump abandonsamuel

label keepsamuel:
    scene bg_outside_projector_room_no_samuel
    hide ben neutral
    show ben neutral at left
    show samuel_redbook at right
    "As I contemplate on my life choices, I finally decide I should go up to him. I approach him as he seems to be reading a book."
    "I glance at the book he is reading it is a red book with a strange symbol on the front of it, it appears to be put in the middle of other shapes making a sun shape."
    "There is text on the book, I don’t understand what it means but it is another language perhaps italian it reads “Nitimur in vetitum”."
    "I start to have second thoughts of my decision to talk to him as I am certain Samuel can’t read Italian. I decide to speak up anyway."
    "I clear my throat and clearly say"
    BEN "Can you help me with something?"
    SAM "This isn’t about another girl is it."
    BEN "What are you talking about?"
    SAM "Oh don’t worry I won’t tell anyone ill help you out."
    "He quickly puts his book in his spare hand and asks"
    SAM "So what is the problem."
    BEN "I need to fix the projector from the meeting we just had."
    SAM "..."
    BEN "It apparently broke down and the sarg blamed it on me."
    SAM "Did you actually not break it, this isn’t like last time is it?"
    BEN "Last time something broke wasn’t my fault either, you just got to trust me on this."
    SAM "Fine but I am leading this time"
    hide samuel_redbook
    hide ben neutral
    scene bg_storage_room
    show ben_idle at left
    show samuel_normal_pose at right
    "I am forcably pulled down the hallway until he stops and lets go of my arm. I feel a slight pain as he twisted my arm when grabbing it. Looking back up I see him approaching a electric door."
    SAM "all spare parts and supplies should be in here"
    "He approaches a keypad next to the door and starts inputting in a passcode. As he starts typing I hear a loud buzz and a red light appears above the keypad."
    "He laughs a bit and enters the code again another buzz but this time it opens."
    "I follow him inside the storage room, it is pitch black inside the room but with a click the light turns on."
    "A single fluorescent light is shining down lighting up the whole room my attention is drawn to the center of the room there is a box with a paper note attached to it."
    "However I am quickly distracted as it seems Samuel has other ideas. I follow him as he starts opening up draws presumably looking for the screwdriver."
    "He is going all over the room making a mess he bumps into me and a loud crash is heard as boxes fall ontop of us."
    "I try to get up but he is too heavy, I annoyingly shout"
    BEN "Your making a mess can you stop!"
    "He pushes the boxes off of him and looks down at me his face slightly red "
    SAM "I-I took it too far, I just got excited I haven’t done something this fun in a while. I was too forceful I am sorry."
    "He offers me his hand and I accept it as he helps me up."
    BEN "y-yeah why don’t you check out that box over there and I will clean this place."
    "I start to pick up the boxes from the floor and put them back into place, luckily most of them were empty."
    "I hear a slight rip from behind me but i ignore it, I hear him walk towards me and say"
    SAM "yeah there was nothing in here but a stupid red pen and this."
    "I place the box down were it was before and I see him holding I note the text on the note reads “Property of DARPA”."
    BEN "well this was a failure."
    "He closes the door and re-enables the lock as we both leave"
    SAM "Maybe we can check out the main desk, they might have a screwdriver"
    "I reluctantly agree and follow him to the main desk."
    hide samuel_normal_pose
    hide ben_idle

    scene bg_main_desk_area
    show ben_neutral at left
    show samuel_normal_pose at right
    "As I approach the main desk I can smell a murky smell in the air, my eyes tear up as I approach the two shadowy figures."
    "Looking down at the floor it seems there is a wet floor sign and a weird liquid substance on the floor."
    "I recently head towards the two shadowy figures until I can see them in plain view there true form."
    "The two shadowy figures are cardboard cutouts with a speaker and microphone attached to it. A advanced drive through so workers can sit inside in nice cool air conditioning lazing around while also take orders."
    "I am startled as I hear a fuzzy voice come out from one of the figures speakers."
    Q2 "What do you wAnT, mAk- it qu-ck."
    BEN "YOU WOULDN”T HAPPEN TO KNOW WERE A SCREWDRIVER IS WOULD YOU? ONE TO REPEAR THE PROJECTOR."
    "The cardboard cutouts remain motionless but a response is heard"
    Q2 "Y-u don- have to scream, what projector?"
    "I explain to the cutouts the whole story in my normal voice, they eventually understand and say"
    Q2 "No I do not, This may be the main desk of this building but our building is not ready and equipped with many of the modern amenities the other buildings have.”"
    "Me and Samuel turn around and he suggests we check upstairs next, we begin walking , I continue to listen to the sound of the speaker as we walk farther away"
    Q2 "This building is the oldest in the camp. We would have to go through dozens of folders and bi--------"
    "The sound fades out as we continue onwards we reach the maintenance hallway, Samuel suggests we take a detour in there to check if a screwdriver is there in the maintenance hall, having no real other leads I agree and follow him inside"

    scene bg_storage_stairwell_fixed
    show ben_idle at left
    show samuel_book_pose at right
    "I quickly search around the hallway only finding empty storage containers."
    "I see a stairway to upstairs I see it is blocked by a green container, it seems like It feel from the shelf it was one as I approach it to pick it up,"
    "I hear Samuel heading towards me, I quickly spin around to see samual book in one hand and paper in the other."
    SAM "Did you find something interesting?"
    "he looks at me and proudly presents it"
    SAM "check this out"
    "he hands me a paper, it seems to be a note of some kind."
    SAM "It was on the main desk I was able to snatch it."
    BEN "how didn’t they notice?"
    SAM "I was able to tell they were too far to do anything and they couldn’t actually see anything from those cardboard cutouts. If the sarg were to see that liquid on the floor he would lose his shit."
    "Well either way if they saw it or not I read the paper"
    BEN "Please discard and shread this message after reading this. The only way I am able to access these files at work is with a FTP setup,"
    BEN "connecting to this address is 136.228.116.222 through one of the computers should redirect to the main server. Only use this for file transfer once the worm is on the system you can power down."
    BEN "Well at least it is something"
    "I say as I bend down and pick up the green container on the floor, As I try to lift it up I realize it is too heavy, I decide the best option is to sit it upright I hear a loud sound in my ear"
    SAM "Hey, what made you join the force?"
    "I drop the box and it almost crushes my leg. I look over and back up a bit, samuel is standing there aloof."
    BEN "Be careful will you, this thing is heavy?"
    SAM "I was just curious thats all."
    "A moment of sclince fills the room I try to think of something to say but I can't think of anything... I feel my face heating up as I remember something and I finally say"
    BEN "I joined for myself thats all."
    SAM "Really that's boring"
    "he walks over to me as I continue trying to open the box."
    SAM "Let me help you out"
    "he starts grabbing at the sides of the container."
    BEN "H-hey let go of remember what I said befor-"
    "the container pops open dust flying out all over the room."
    "As the dust clears I frown looking down at the container it looks like an old computer is inside it, There is a makeup kit inside the box along with a female soldier uniform."
    "I pick up the mackeup kit and inspect I see a broken hand mirror inside."
    $ inventory.append("Broken Hand Mirror")
    "I pick it up and stare back at myself for a good few seconds. I sigh"
    BEN "I told you to be careful. Your breaking other peoples stuff, look what you did to this mirror!"
    "I yell showing him the broken mirror. The room goes silent as I put the mirror in my pocket."
    "I begin walking upstairs, I hear Samuel quickly follow behind me, I think to myself about the mirror I can't fix something that is broken, even if I could nothing would change anyway."
    hide ben_idle
    hide samuel_book_pose

    scene bg_military_entrance
    show ben_neutral at center
    "as I step upstairs I feel the cool AC and an exit to the sweaty basement I feel the tempature drop and the wind hit my face. I don't give it a second thought though."
    "I glance at the sign on the wall there are two ways to go left and right. Reading the signs one says armory to the left and the other says loading bay to the right."
    "I start walking to the right but I just remembered something. I need to pick up my new uniform and weapons for the mission."
    "If the mission is starting tonight I should probably pick them up soon as processing should take around an hour."
    "However if I go now I may not have enough time to fix the projector as fixing it seems like an impossible task already and I already spent a long time just looking for a stupid screwdriver."
    "I need to decide what is more important the sergeants order or my own safety"
    menu:
        "Get Army Uniform":
            jump getuniformwithsamuel
        "Go get screwdriver":
            jump getscrewdriverwithsamuel

label getuniformwithsamuel:
    scene bg_military_entrance
    show ben_neutral at left
    show samuel_normal_pose at right
    BEN "Safety always comes first I think to myself as I turn around heading towards the supply depo."
    "I hear Samuel quickly follow behind me as he starts trying to make conversation."
    SAM "You know the two guys that run the stands where we are headed right? I spoke to them this morning they were kind of depressed. The sarg has been calling them heady and army,"
    SAM "it seems it caught on with some of the recruits. I would try to keep it easy on them."
    "I mentally take a note of what  as we pass by a door that takes my attention it has a paper that has the text COMPUTER LAB drawn onto it."
    "The text is slopply written and in blank sharpie marker ink. The paper is ripped a part of it torn off and on the floor."
    "It also seems like someone or something dented the door. The door is dented enough to see a small crater where the impact was it was about as big as my head."
    "I see that Samuel is getting farther from me and I rush ahead to catch up to him, he seems to notice that I was looking at the door and asks"
    SAM "Do you want to check it out? I think we still have time."
    BEN "No, duty is more important. Maybe if we ever have down time after this we can go check it out together."
    SAM "Your loss."
    "and we both continue. There is a maintenance door that leads into a damp garage area."

    scene bg_elevator
    show ben_neutral at left
    show samuel_normal_pose at right

    "The room is pretty empty aside from two stands setup opposite to an elevator. The room is cold and dark only illuminated by the lights of the elevator and stands."
    "The two people stand there staring into nothingness the sound of a cheerful tune coming from the stand on the left."
    "The stand on the left labeled weapon stand has a bill board on it with the text “Todays menu” and a list of guns ranging from small pistols to large machine guns I can only dream of using."
    "The person manning the stand stands flamboyantly a unmoving smile, his eyes beat red in medieval knight armor, its shine contrasting the painted on pastel background behind him."
    "He seems to be breathing in and out waiting patiently for the next person to arrive at his stand. His most notable feature being his hands."
    "His hands seem to unusually contort at the wrists and his hands are stuck in twisted positions almost like his hands have no bones at all."
    "I feel a slight tap on my shoulder I choose to remain focused on what lay before me looking to the right there is at least some semblance of normalcy as I see a hooded man in all red robes."
    "The stand looks normal enough until I took a closer look first the red hood masking his face, there is something perduring out of his face. It is way too big to be a simple bump there has to be something more."
    "Second what’s behind him, its not a pastel wallpaper but products. He has many products behind him some seemingly unrelated to armor. There are some strange devices I am unable to recognize."
    "Questions pass through my mind like were did he get these from? why did he choose to display them so publicly?"
    "Finally that music, it is slow and methodical yet cheery. It is being played from a old stereo, the tone is almost hypnotic with how slow and droning the loop is."
    "I feel a tap on my shoulder and see Samuel he looks concerned"
    SAM "Are you alright? You have been staring into space for a few minuets , I can order the armor if your scared."
    BEN "No, I am fine. I was just a bit spaced out."
    SAM "You sure, maybe we should go back?"
    "I ignore his question and decide which stand I should approach."
    hide samuel_normal_pose
    show knight default at center
    KNIGHT "..."
    "As I approach the man he seems to grow. His shadow looming over me, he has turned into a giant. his armor shining in the low light of the room, his smile getting wider, a slight mumble coming from it."
    "I was not sure how a face can even look like this he was no man he was a monster."
    "I feel another tap and finally give in looking behind me samuel put his hands on my shoulder almost as a comforting motion to tell me its going to be okay."
    show samuel_sholder_pose at right
    "I take a deep breath and begin the conversation"
    BEN "I am here to place an order in for a new uniform"
    "its face doesn’t move he stands there eyes unblinking almost like he is judging me, asking me “why did you come here”."
    "I almost take a step back but Samuel walks in front of me and loudly states"
    SAM "my friend is here to pick up a new gun!."
    "As I realized my mistake from earlier I notice Its eyeballs move quickly homing in on Samuel almost like they are locking on to a new target."
    "I prepare for impact before I see the monster come to life its bright smile turns into a frown, his eyes slowly start blinking and his hands, his broken hands move up to his face and pull something out."
    "It is small by I see and hear it quite clearly, a pair of earphones the volume so loud I can make out it was playing some k-pop music."
    KNIGHT "What was that you said again."
    "The façade has vanished this was no monster, it was a man a broken tired man."
    "Samuel repeats his question and the man replies in a now defeated still raspy, monotone voice with"
    KNIGHT "I will put in a order for you it should be done before your mission starts."
    "He flips a small switch and a tube comes down from the ceiling."
    KNIGHT "So what kind of weapon do you want to use?"
    menu choice_of_weapons:
        "Pistol":
            $ player_weapon_choice = "Pistol"
            jump process_weapon_choice
        "Rifle":
            $ player_weapon_choice = "Rifle"
            jump process_weapon_choice
        "Shotgun":
            $ player_weapon_choice = "Shotgun"
            jump process_weapon_choice
        "Grenade Launcher (Dream Big)":
            $ player_weapon_choice = "Grenade Launcher"
            jump process_weapon_choice

label process_weapon_choice:
    KNIGHT "Good choice, I wouldn’t personally go for that one but oh well."
    "He places the paper back in the tube and flicks a switch. I watch as the paper quickly goes up into the unknown."
    KNIGHT "Anything else?"
    BEN "..."
    "he than grabs his headphones and puts them back in his ears."
    hide knight default
    hide samuel_sholder_pose
    show ben_neutral at left
    show samuel_normal_pose at right

    "Perhaps I was overthinking everything and this would go more smoothly than I have previously thought, as we walk over to the next stand I look over to Samuel and he gives me the thumbs up."
    "We than head over to the next stand [right stand]"
    show red_hood default at center
    RED_HOOD "..."
    "I take a deep breath as I approach the stand, the hooded man seems to notice me his head moves up and  in a low voice"
    RED_HOOD "Hello you two, you must be benjamin right? Today’s reading said you would come."
    BEN "Who told you I would come?"
    RED_HOOD "No matter, I have the order you were about to place ready."
    "He hands me a new uniform the right one."
    $ inventory.append("New Uniform")
    SAM "Alright, lets get you out of that uniform, lets head to the bathroom."
    BEN "I can’t accept this, what just happened is just too convenient. I have an urge a pulse even I need to figure out how this happened no matter the cost."
    BEN "hold up a second"
    "I put my hand up to Samuel as I face the man I say"
    BEN "How the hell did you know what I was going to order!"
    RED_HOOD "You best not seek knowledge that you are unprepared to learn about for the truth is far worse than what you should know."
    SAM "..."
    BEN "Cut the bullshit, who told you?"
    RED_HOOD "..."
    BEN "Tell me! Tell me now!"
    "and sighs he lifts his hood up a tiny amount revealing for only a second a single horn sticking out of his head before he puts the robe back down."
    RED_HOOD "Both of you mustn’t come back here for I have revealed some of my inner self."
    "we both walk backwards my uniform in hand until he are a safe enough distance from him."
    SAM "we will talk about this later."
    hide red_hood default
    hide samuel_normal_pose
    hide ben_neutral

    scene bg_main_desk_area
    show ben_neutral at center
    "Me and Samuel head to the bathroom. I tell Samuel to wait outside as I enter the bathroom and begin to undress."
    "First my shirt comes off than my pants fall down, I grab the new uniform feeling how it was perfectly, I feel as the stiff fabric stretches with my skin as I pull my new pants up"
    "the pants almost being too big for me if it wasn’t for the belt holding them in place, I think about how dirty this uniform will get after the mission how this may be the only one time I see it clean and in prefect condition."
    "I feel the shirt slip on next as I slide it down my muscular body looking in the mirror I see myself and hype myself up for the mission to come."
    "I feel the polyester touch across my body as it rigidly comes into place. Next comes on the shoes they are heavy put reliable I than grab my helmet putting it on my head"
    "seeing the pointy metal come out of the top I think to myself it may be able to be used as a tool."
    "I than take one last look at myself in the mirror and leave the changing room."
    hide ben_neutral

    scene bg_elevator
    show drill_sarg_talk at center
    show samuel_normal_pose at right
    "As I leave I see the drill Sargent talking to Samuel outside he looks disappointed"
    DRI "So you were unable to fix this old thing? Well I hope you find a mechanic during the mission because we are getting ready to leave the base."
    DRI "Follow me outside you two maggots we are already late as is."
    "His frown worsens"
    "He looks to Samuel and chuckles"
    DRI "I know you two like chatting so I am separating you into different squads. This mission is important and I wouldn’t want you to screw this up. You will follow me do you understand"
    BEN "sir yes sir!"
    SAM "sir yes sir!"
    "and begin to follow him outside as the garage door opens up lighting up the room we see a line of soldiers waiting outside all rigid in form waiting for there orders."
    "We both head into our respective squads…"
    jump outsidewithuniform

label getscrewdriverwithsamuel:
    scene bg_military_entrance
    show ben_neutral at left
    show samuel_redbook at right
    BEN "Contemplating my options I figure that I might as well start this pointless search for my screwdriver, I try to forget about the screwdriver."
    "I head to the right as me and Samuel walk to the right he begins to start some small talk"
    SAM "that book from earlier –"
    BEN "Yeah don’t worry about it, I won’t tell anyone you read picture books."
    SAM "Hey! Its not a picture book."
    "He moves the book back into both hands and begins reading"
    SAM "There exists two states in this world, the is and isn’t."
    BEN "I already told you, I won’t tell anyone you don’t need to make this worse than it already is"
    SAM "Once the lost artifacts are bought into one place…"
    "I move my hand and close the book myself as we walk and say"
    BEN "look man, I know that story is probably great and all but we have bigger problems we need to solve. Like getting that screwdriver!"
    SAM "This has to be connected to the mission, those scenes on the projector there similar to what is written in this book."
    "I dismiss his claim and we both continue onwards towards a giant window."

    scene bg_city_freedom
    "We both stop a bit and admire the outside, The window reveals open roads going into other buildings that look smaller from here than they actually are."
    "We can see trucks and military cars driving on the paved cement. We watch as two people in a jeep make hand motions talking to each other there car driving off into other facilities and the unknown."
    "We can see the calm sky seeing the morning sun come up over the horizon the clouds shapes are uniform."
    "We are at peace until the ground starts shaking, looking up the clouds disperse and open a fleet of osprey aircraft come whirling in and head towards the front of the building we are in."
    "We both can see and feel the aircraft fly above us disrupting the peace."
    "I hear someone stand, looking behind me I see the turban man from earlier getting up from his seat."
    hide ben_neutral
    hide samuel_redbook
    show sultan_talking_pose at center
    RAM "You never got my name did you?"
    "Looking at him with his lit cigar in his mouth  staring at me with tired eyes"
    RAM "You can call me the ram."
    "He takes another puff of his cigar."
    show ben_neutral at left
    show samuel_normal_pose at right
    "Me and Samuel stare at him for a few seconds processing that odd sounding name before he looks at my hands and looks back up at me and says"
    RAM "So you really are going to fix that projector bro?"
    "He gives me a side eye before sitting down again"
    RAM "I dealt with something similar on a previous mission."
    "Me and Samuel decide to sit down and listen to his story, he continues"
    RAM "I was in charge of protecting a audio device, it would play a simple lullaby it was meant to calm someone known as the giant . My squad was a team of four, but we lost one during the mission."
    RAM "The mission started off poorly. We were all ill equipped. Me and red hood were in charge of recon while the knight and private p were supposed to play that damn device."
    SAM "what happened to the other two people"
    RAM "That is their story to tell not mine."
    RAM "The damn thing ran out of battery” His face scrunches up and his anger builds “The main fucking device meant to save us ran on double a batteries"
    "he coughs cigar smoke coming out of his mouth he seems to be less tense than before as "
    RAM "This place is a joke. I wouldn’t trust that projector for a second."
    BEN "We were given orders to fix this projector and we will fulfill them"
    RAM "..."
    "I watch as the smoke cloud rises from his cigar it slowly rising up and disappearing into the air. He shakes his head"
    RAM "This is why I stayed in the military, to prevent people like you from dying"
    "he sighs looking defeated"
    RAM "This stress has been getting to me recently that this mission may be another failure, that we may not come back alive again."
    SAM "We won’t let that happen."
    RAM "I almost started a small fire in the storage room."
    "Me and samuel look at each other we both have been their earlier today and didn’t see him there he continues"
    RAM "I was smoking a cigar and I tossed it on the floor carelessly I was going to let it stay their but once I heard you two trying the combination to the storage room; I stomped it out and picked it back up quickly. Luckly, you got the code wrong at first."
    "I look at Samuel he is slightly embarrassed, ram notices this but does not say anything"
    RAM "I was able to sneak out of the room but I felt really guilty after about what I have done. I don’t know what would have happened if I let it go."
    RAM "I wasn’t in a good mental state earlier, after this smoke break I cooled off. Here hold out your hands"
    " as he swings his bag over and goes through it.” I hold out my hands as he asked and he pulls something out of has backpack and puts it in my hands he holds it tightly he whispers to me"
    RAM "Thanks for listening to me bro. This saved me once before maybe it can save you."
    "and he releases it from his hand and runs off."
    hide sultan_talking_pose

    "Looking down I see a screwdriver in my hand It seems to have an irregular shape it looked like it had two screwdriver heads bolted into it. They were both labeled with white text saying “single” and “double” on it."
    $ inventory.append("Special Screwdriver")
    "I look at samuel and he gives me the thumbs up and we both grin."
    SAM "Lets head back and fix that projector, we wouldn’t want to keep the sargent waiting would we?"
    "We both lined up with each other as we did many time before and I give him the signal to start counting he started counting down from three and than we sprinted back to the projector room."
    "He was in the lead till we reached the staircase, he almost feel and tripped over his own shoelace and I caught his hand and helped him back up saying"
    BEN "Be careful, if we go too fast we can get into trouble."
    "We both walk slowly down the stairs and start the race back up again after we leave the previous room as we reach the projector room we catch our breach I say in between my breaths"
    BEN "I think….I won."
    SAM "Not…a….chance..."
    hide ben_neutral
    hide samuel_normal_pose

    scene bootcampinsideprojectorroomstartm
    show ben_idle at left
    show samuel_normal_pose at right
    "We both agree that this was a tie and we head over to the projector after some time, I look at the projector as a whole seeing both films in there proper places"
    "I read the labels on the big tape reading the label it says AAXA SCP-A01 on the right gear and AAXA SCP-A02 on the left."
    BEN "I ask Samuel about these"
    SAM "I have no idea, maybe that is the manufacturing label or something?"
    "looking down I see the back of the projector there are four nuts. I look at the single screwdrivers in my hand and get to work."
    "I use the screwdriver head labeled single, the first screw comes out fine and than the second and the third until the back finally plops out onto the floor."
    "Looking inside the device I see many gears and knobs some of them labeled. Also a strange compartment requiring two screws to be removed."
    "These screws were attached to each other, I have never seen anything like this before, their oblique angels making it hard to find out what to do."
    "I ask samuel what this is he looks at it confused than asks me for my screwdriver, I hand it over it him and he picks it up."
    "He thinks for a bit than moves the screwdriver head into place so the one labeled “double” is in line with the one labeled “single” and presses it in."
    "As he presses it in there is a moment of silence before it properly clicks the satisfying sound of the click in my ears brightens my mood a bit as he begins to turn it."
    "Two of the screws pop out at once it seems like they were meant for this specific screwdriver."
    "I switch the screwdriver back to the single mode and I unscrew the last screw the final piece coming out revealing what looks to be a singular burnt out light bulb."
    "I begin to unscrew it but I feel a large shock as I pull my hand back I notice a small prick in my hand, I pull what looks like a small piece of red glass out"
    "it seems to be a glass shard as I start to bleed. I than watch as the lightbulb suddenly turns on as if it was not broken at all it shining a bright red color."
    "Me and Samuel look at each other as he is holding the unplugged power cord to the projector confused”."
    "The tapes start spinning and it makes a loud screeching sound enough for everyone in the base to hear."
    "Me and Samuel cover our ears, the sound still blasting through it. I watch as samuel quickly goes over and plugs the projector in and the sound stops."
    "A red light coming from the projector shows on the wall revealing text on a blue background it has a title that reads“ The unstable darkness” reading the text below"
    "“There exists many artifacts in this world lost to time. Some are secured and contained while others remain lost or stolen to time."
    "One of these affects the two states in this world, the is and isn’t. Combining both into one making fiction into reality, making the false into the true.”"
    "I look at the screen staring at it for a few seconds before I hear I click and a screech come from the projector as the projector light turns white and the slide changes to the next slide revealing what was in the slideshow from earlier today"
    "I pick up the screwdriver and pocked it while responding"
    BEN "Hey I was reading that!"
    "Samuel is about to respond when we hear footsteps behind us looking back we see the drill Sargent walk into the room smiling"
    hide ben_idle
    hide samuel_normal_pose
    show drill_sarg_very_happy at center
    DRI "Well you too really did an exceptional job."
    "He walks up to the projector and unplugs it picking it up as he does, "
    DRI "Your just in time too, we are loading up and preparing to start the mission, lets move out you two!."
    BEN "Sir yes sir!"
    SAM "Sir yes sir!"
    "I grunt as I feel a weight put onto my hand as he plops the projector into my now empty hands and we follow behind him"
    jump outsidewithoutuniform

label abandonsamuel:
    scene bg_outside_projector_room
    show ben_neutral at center
    "I look to the left of the door seeing Samuel standing there reading a book, I pay less attention to him as I head towards the first place I think a screwdriver would be the storage room."
    scene bg_storage_room
    show ben_neutral at center
    "As I approach the storage room I notice a keypad next to the door I head towards the door and examine the keypad."
    "It has letters on it instead of numbers it seems I am spoused to enter a passphrase."
    "I quickly look to my left and look to my right and enter a random passphrase I thing in my head “Butts2012” after a few seconds of nothingness a buzz and a light red glow appear."
    "I stand there staring at the keypad watching the light fade back into place I laugh a bit to myself realizing that my journey ended as fast as it started."
    "I am startled as I hear someone walk up to me a soldier must have overheard me laughing."
    "Looking closer they seem familiar, I realize that they were in the meeting from before, it was the person sitting in the front seat."
    show sultan_talking_pose at right
    RAM "(if not met yet He reaches his hand out to me “want a cig bro?” I am caught off guard by this and instantly deny him)"
    RAM "So what are you laughing about bro?"
    "I watch as the smoke comes out of the lit cigar making little clouds go up into the sky and I respond with"
    BEN "I am [still] (if talked before) looking for a specialty screwdriver do you have any idea were one would be?"
    "He takes the cigar out of his mouth and walks up to the locked door, I watch him enter the passcode with ease almost like he has done this many times before"
    "I follow him inside the storage room and he walks of to a storage draw and slides it open revealing what must be a dozen screwdrivers."
    BEN "I thank him and head back to the projector room to grab the projector to fix, once I come back projector in hand I notice he is still standing in there"
    "using the closet as a place to hide his smoking habits from the public. I look at the projector as a whole seeing both films in there proper places I read the labels on the big tape reading the label"
    "it says AAXA SCP-A01 on the right gear and AAXA SCP-A02 on the left looking down I see the back of the projector there are four nuts."
    "I look at the screwdrivers laid out before me and get to work picking up the screwdriver that fits, the first screw comes out fine and than the second and the third"
    "until the back finally plops out onto the floor. Looking inside the device I see many gears and knobs some of them labeled. Also a strange compartment requiring two screws to be removed."
    "These screws were attached to each other, I have never seen anything like this before, their oblique angels making it hard to find out what screwdriver was needed."
    "After going through each screwdriver one by one I was unable to find out what was needed."
    "As I look at the gears trying to find out what was wrong I hear a flick almost like someone is tossing something and than a burst sound."
    "Looking behind me I see a bright light and than feel a intense heat, the cardboard boxes caught fire!"
    RAM "It wasn’t me bro, I don’t know how this could have happened."
    "He then begins to walk out of the room as the fire spreads not bothering to look back."
    hide sultan_talking_pose
    "The fire spreads from box to box as if it was a chorus singing a song, some big boxes some small boxes the room was quickly getting hotter the white smoke turned to black smoke and the fire soon engulfed the room."
    "I rush towards the projector and pick it up. I quickly run out of the room behind the man, I grab onto his shoulder before the adrenaline wears of and my hand slips"
    "I have to place the heavy projector back down. I kneel down and place it down, I am out of breath… I look up at him as he casually lights his next cigar."
    show sultan_talking_pose at right
    "The world spins around me as I hear beeping and screaming, the smoke creeping out of the storage cabinet into the main hall."
    "I hear a slight creak and feel as it starts raining. With the last bit of my energy I stand up in a turtle position and cover the projector with my body"
    "making sure it does not get soaked as I hear the chaos around me, I hear footsteps and screaming and feel the intense heat hit my back as the fire spread, I start to wince from the pain"
    "and decide it is best that I should just close my eyes and open them back up when this is all over, so I do I revert inwards thinking about my life decisions that bought me here."
    BEN "Maybe if I chose Samuel this wouldn’t have happened. Maybe I should have never joined the army. Maybe if I took action earlier she-."
    BEN "I stop myself no, it is my duty to complete this task, this mission. I chose to serve this country no one else did, no one else would. I take a deep breath and prepare to protect this projector with my life."
    "The few minutes felt like a blur to me, I feel as if my instincts have kicked in and I am unable to move, I feel my legs quiver and the water drip down my shirt."
    "I stayed in that position making sure the projector didn’t get wet like my life depended on it, until my legs finally gave in and I fell onto the floor avoiding the projector."
    "I lay there motionless for many more minuets as I catch my breath, I look up at the ceiling the sprinklers turning off and than looking straight ahead at the man that caused all of this."
    "As I regain my energy I sit back up and stand up I slap the cigar out of his hands, I step on it no I stomp on it as hard as I can putting out the bud until it is fully out."
    hide sultan_talking_pose
    "Looking around I notice a crowd of at least 5 people has gathered around us undoubtedly coming here due to the fire."
    "I ignore them though and return to the projector, it seems like the back piece of the projector was still in the room from when I took it off."
    "However aside from some burn marks on the front the projector seems fine, I look inside the room I was just in most of the floor is flooded, there are various tools and trinkets floating in the water and some ash"
    "the back plate of the projector is nowhere in site if I wanted to get it back on id have to search the room for it."
    "There are two people in fire retardant suits in the room assessing the damages they don’t look particularly happy about it and I am sure ill see them again once they see the camera footage of how this happened."
    show sultan_talk_pose at right
    RAM "Well bro, if I were you id get your clothes replaced and get your weapons the mission starts tonight after all."
    "I think to myself if this is really the best course of action, should I really listen to the man who almost broke my projector and caused this whole debacle in the first place"
    "or should I go get my uniform so I am at least ready for the mission to begin or should I just try to fix this mess I am already and focus on fixing the projector."
    menu:
        "Get Army Uniform":
            jump getuniformwithoutsamuel
        "Go get screwdriver": # This was "Go fix projector"
            jump fixprojectoralone
label getuniformwithsamuel_alt:
    scene bg_military_entrance
    show ben_neutral at left
    show samuel_normal_pose at right
    BEN "Safety always comes first I think to myself as I turn around heading towards the supply depo."
    "I hear Samuel quickly follow behind me as he starts trying to make conversation."
    SAM "You know the two guys that run the stands where we are headed right? I spoke to them this morning they were kind of depressed."
    SAM "The sarg has been calling them heady and army, it seems it caught on with some of the recruits. I would try to keep it easy on them."
    "I mentally take a note of what  as we pass by a door that takes my attention it has a paper that has the text COMPUTER LAB drawn onto it."
    "The text is slopply written and in blank sharpie marker ink. The paper is ripped a part of it torn off and on the floor."
    "It also seems like someone or something dented the door. The door is dented enough to see a small crater where the impact was it was about as big as my head."
    "I see that Samuel is getting farther from me and I rush ahead to catch up to him, he seems to notice that I was looking at the door and asks"
    SAM "Do you want to check it out? I think we still have time."
    BEN "No, duty is more important. Maybe if we ever have down time after this we can go check it out together."
    SAM "Your loss."
    "and we both continue. There is a maintenance door that leads into a damp garage area."

    scene bg_elevator
    show ben_neutral at left
    show samuel_normal_pose at right

    "The room is pretty empty aside from two stands setup opposite to an elevator. The room is cold and dark only illuminated by the lights of the elevator and stands."
    "The two people stand there staring into nothingness the sound of a cheerful tune coming from the stand on the left."
    "The stand on the left labeled weapon stand has a bill board on it with the text “Todays menu” and a list of guns ranging from small pistols to large machine guns I can only dream of using."
    "The person manning the stand stands flamboyantly a unmoving smile, his eyes beat red in medieval knight armor, its shine contrasting the painted on pastel background behind him."
    "He seems to be breathing in and out waiting patiently for the next person to arrive at his stand. His most notable feature being his hands."
    "His hands seem to unusually contort at the wrists and his hands are stuck in twisted positions almost like his hands have no bones at all."
    "I feel a slight tap on my shoulder I choose to remain focused on what lay before me looking to the right there is at least some semblance of normalcy as I see a hooded man in all red robes."
    "The stand looks normal enough until I took a closer look first the red hood masking his face, there is something perduring out of his face. It is way too big to be a simple bump there has to be something more."
    "Second what’s behind him, its not a pastel wallpaper but products. He has many products behind him some seemingly unrelated to armor. There are some strange devices I am unable to recognize."
    "Questions pass through my mind like were did he get these from? why did he choose to display them so publicly?"
    "Finally that music, it is slow and methodical yet cheery. It is being played from a old stereo, the tone is almost hypnotic with how slow and droning the loop is."
    "I feel a tap on my shoulder and see Samuel he looks concerned"
    SAM "Are you alright? You have been staring into space for a few minuets , I can order the armor if your scared."
    BEN "No, I am fine. I was just a bit spaced out."
    SAM "You sure, maybe we should go back?"
    "I ignore his question and decide which stand I should approach."
    hide samuel_normal_pose
    show knight default at center
    KNIGHT "..."
    "As I approach the man he seems to grow. His shadow looming over me, he has turned into a giant. His armor shining in the low light of the room,"
    "his smile getting wider, a slight mumble coming from it. I was not sure how a face can even look like this he was no man he was a monster."
    "I feel another tap and finally give in looking behind me samuel put his hands on my shoulder almost as a comforting motion to tell me its going to be okay."
    show samuel_sholder_pose at right
    "I take a deep breath and begin the conversation"
    BEN "I am here to place an order in for a new uniform"
    "its face doesn’t move he stands there eyes unblinking almost like he is judging me, asking me “why did you come here”."
    "I almost take a step back but Samuel walks in front of me and loudly states"
    SAM "my friend is here to pick up a new gun!."
    "As I realized my mistake from earlier I notice Its eyeballs move quickly homing in on Samuel almost like they are locking on to a new target."
    "I prepare for impact before I see the monster come to life its bright smile turns into a frown, his eyes slowly start blinking and his hands,"
    "his broken hands move up to his face and pull something out. It is small by I see and hear it quite clearly, a pair of earphones the volume so loud I can make out it was playing some k-pop music."
    KNIGHT "What was that you said again."
    "The façade has vanished this was no monster, it was a man a broken tired man."
    "Samuel repeats his question and the man replies in a now defeated still raspy, monotone voice with"
    KNIGHT "I will put in a order for you it should be done before your mission starts."
    "He flips a small switch and a tube comes down from the ceiling."
    KNIGHT "So what kind of weapon do you want to use?"
    menu choice_of_weapons_alt: 
        "Pistol":
            $ player_weapon_choice = "Pistol"
            jump process_weapon_choice # This label was already used, ensure okay or make unique
        "Rifle":
            $ player_weapon_choice = "Rifle"
            jump process_weapon_choice
        "Shotgun":
            $ player_weapon_choice = "Shotgun"
            jump process_weapon_choice
        "Grenade Launcher (Dream Big)":
            $ player_weapon_choice = "Grenade Launcher"
            jump process_weapon_choice

label process_weapon_choice_alt: 
    KNIGHT "Good choice, I wouldn’t personally go for that one but oh well."
    "He places the paper back in the tube and flicks a switch. I watch as the paper quickly goes up into the unknown."
    KNIGHT "Anything else?"
    BEN "..."
    "he than grabs his headphones and puts them back in his ears."
    hide knight default
    hide samuel_sholder_pose
    show ben_neutral at left
    show samuel_normal_pose at right

    "Perhaps I was overthinking everything and this would go more smoothly than I have previously thought, as we walk over to the next stand I look over to Samuel and he gives me the thumbs up."
    "We than head over to the next stand [right stand]"
    show red_hood default at center
    RED_HOOD "..."
    "I take a deep breath as I approach the stand, the hooded man seems to notice me his head moves up and  in a low voice"
    RED_HOOD "Hello you two, you must be benjamin right? Today’s reading said you would come."
    BEN "Who told you I would come?"
    RED_HOOD "No matter, I have the order you were about to place ready."
    "He hands me a new uniform the right one."
    $ inventory.append("New Uniform")
    SAM "Alright, lets get you out of that uniform, lets head to the bathroom."
    BEN "I can’t accept this, what just happened is just too convenient. I have an urge a pulse even I need to figure out how this happened no matter the cost."
    BEN "hold up a second"
    "I put my hand up to Samuel as I face the man I say"
    BEN "How the hell did you know what I was going to order!"
    RED_HOOD "You best not seek knowledge that you are unprepared to learn about for the truth is far worse than what you should know."
    SAM "..."
    BEN "Cut the bullshit, who told you?"
    RED_HOOD "..."
    BEN "Tell me! Tell me now!"
    "and sighs he lifts his hood up a tiny amount revealing for only a second a single horn sticking out of his head before he puts the robe back down."
    RED_HOOD "Both of you mustn’t come back here for I have revealed some of my inner self."
    "we both walk backwards my uniform in hand until he are a safe enough distance from him."
    SAM "we will talk about this later."
    hide red_hood default
    hide samuel_normal_pose
    hide ben_neutral

    scene bg_main_desk_area # Placeholder for bathroom
    show ben_neutral at center # Changing
    "Me and Samuel head to the bathroom. I tell Samuel to wait outside as I enter the bathroom and begin to undress."
    "First my shirt comes off than my pants fall down, I grab the new uniform feeling how it was perfectly, I feel as the stiff fabric stretches with my skin as I pull my new pants up"
    "the pants almost being too big for me if it wasn’t for the belt holding them in place, I think about how dirty this uniform will get after the mission how this may be the only one time I see it clean and in prefect condition."
    "I feel the shirt slip on next as I slide it down my muscular body looking in the mirror I see myself and hype myself up for the mission to come."
    "I feel the polyester touch across my body as it rigidly comes into place. Next comes on the shoes they are heavy put reliable I than grab my helmet putting it on my head"
    "seeing the pointy metal come out of the top I think to myself it may be able to be used as a tool."
    "I than take one last look at myself in the mirror and leave the changing room."
    hide ben_neutral

    scene bg_elevator # Back to garage
    show drill_sarg_talk at center
    show samuel_normal_pose at right
    "As I leave I see the drill Sargent talking to Samuel outside he looks disappointed"
    DRI "So you were unable to fix this old thing? Well I hope you find a mechanic during the mission because we are getting ready to leave the base."
    DRI "Follow me outside you two maggots we are already late as is."
    "His frown worsens"
    "He looks to Samuel and chuckles"
    DRI "I know you two like chatting so I am separating you into different squads. This mission is important and I wouldn’t want you to screw this up. You will follow me do you understand"
    BEN "sir yes sir!"
    SAM "sir yes sir!"
    "and begin to follow him outside as the garage door opens up lighting up the room we see a line of soldiers waiting outside all rigid in form waiting for there orders."
    "We both head into our respective squads…"
    jump outsidewithuniform

label getscrewdriverwithsamuel_alt:
    scene bg_military_entrance
    show ben_neutral at left
    show samuel_redbook at right
    BEN "Contemplating my options I figure that I might as well start this pointless search for my screwdriver, I try to forget about the screwdriver."
    "I head to the right as me and Samuel walk to the right he begins to start some small talk"
    SAM "that book from earlier –"
    BEN "Yeah don’t worry about it, I won’t tell anyone you read picture books."
    SAM "Hey! Its not a picture book."
    "He moves the book back into both hands and begins reading"
    SAM "There exists two states in this world, the is and isn’t."
    BEN "I already told you, I won’t tell anyone you don’t need to make this worse than it already is"
    SAM "Once the lost artifacts are bought into one place…"
    "I move my hand and close the book myself as we walk and say"
    BEN "look man, I know that story is probably great and all but we have bigger problems we need to solve. Like getting that screwdriver!"
    SAM "This has to be connected to the mission, those scenes on the projector there similar to what is written in this book."
    "I dismiss his claim and we both continue onwards towards a giant window."

    scene bg_city_freedom
    "We both stop a bit and admire the outside, The window reveals open roads going into other buildings that look smaller from here than they actually are."
    "We can see trucks and military cars driving on the paved cement. We watch as two people in a jeep make hand motions talking to each other there car driving off into other facilities and the unknown."
    "We can see the calm sky seeing the morning sun come up over the horizon the clouds shapes are uniform."
    "We are at peace until the ground starts shaking, looking up the clouds disperse and open a fleet of osprey aircraft come whirling in and head towards the front of the building we are in."
    "We both can see and feel the aircraft fly above us disrupting the peace."
    "I hear someone stand, looking behind me I see the turban man from earlier getting up from his seat."
    hide ben_neutral
    hide samuel_redbook
    show sultan_talking_pose at center
    RAM "You never got my name did you?"
    "Looking at him with his lit cigar in his mouth  staring at me with tired eyes"
    RAM "You can call me the ram."
    "He takes another puff of his cigar."
    show ben_neutral at left
    show samuel_normal_pose at right
    "Me and Samuel stare at him for a few seconds processing that odd sounding name before he looks at my hands and looks back up at me and says"
    RAM "So you really are going to fix that projector bro?"
    "He gives me a side eye before sitting down again"
    RAM "I dealt with something similar on a previous mission."
    "Me and Samuel decide to sit down and listen to his story, he continues"
    RAM "I was in charge of protecting a audio device, it would play a simple lullaby it was meant to calm someone known as the giant . My squad was a team of four, but we lost one during the mission."
    RAM "The mission started off poorly. We were all ill equipped. Me and red hood were in charge of recon while the knight and private p were supposed to play that damn device."
    SAM "what happened to the other two people"
    RAM "That is their story to tell not mine."
    RAM "The damn thing ran out of battery” His face scrunches up and his anger builds “The main fucking device meant to save us ran on double a batteries"
    "he coughs cigar smoke coming out of his mouth he seems to be less tense than before as "
    RAM "This place is a joke. I wouldn’t trust that projector for a second."
    BEN "We were given orders to fix this projector and we will fulfill them"
    RAM "..."
    "I watch as the smoke cloud rises from his cigar it slowly rising up and disappearing into the air. He shakes his head"
    RAM "This is why I stayed in the military, to prevent people like you from dying"
    "he sighs looking defeated"
    RAM "This stress has been getting to me recently that this mission may be another failure, that we may not come back alive again."
    SAM "We won’t let that happen."
    RAM "I almost started a small fire in the storage room."
    "Me and samuel look at each other we both have been their earlier today and didn’t see him there he continues"
    RAM "I was smoking a cigar and I tossed it on the floor carelessly I was going to let it stay their but once I heard you two trying the combination to the storage room; I stomped it out and picked it back up quickly. Luckly, you got the code wrong at first."
    "I look at Samuel he is slightly embarrassed, ram notices this but does not say anything"
    RAM "I was able to sneak out of the room but I felt really guilty after about what I have done. I don’t know what would have happened if I let it go."
    RAM "I wasn’t in a good mental state earlier, after this smoke break I cooled off. Here hold out your hands"
    " as he swings his bag over and goes through it.” I hold out my hands as he asked and he pulls something out of has backpack and puts it in my hands he holds it tightly he whispers to me"
    RAM "Thanks for listening to me bro. This saved me once before maybe it can save you."
    "and he releases it from his hand and runs off."
    hide sultan_talking_pose

    "Looking down I see a screwdriver in my hand It seems to have an irregular shape it looked like it had two screwdriver heads bolted into it. They were both labeled with white text saying “single” and “double” on it."
    $ inventory.append("Special Screwdriver")
    "I look at samuel and he gives me the thumbs up and we both grin."
    SAM "Lets head back and fix that projector, we wouldn’t want to keep the sargent waiting would we?"
    "We both lined up with each other as we did many time before and I give him the signal to start counting he started counting down from three and than we sprinted back to the projector room."
    "He was in the lead till we reached the staircase, he almost feel and tripped over his own shoelace and I caught his hand and helped him back up saying"
    BEN "Be careful, if we go too fast we can get into trouble."
    "We both walk slowly down the stairs and start the race back up again after we leave the previous room as we reach the projector room we catch our breach I say in between my breaths"
    BEN "I think….I won."
    SAM "Not…a….chance..."
    hide ben_neutral
    hide samuel_normal_pose

    scene bootcampinsideprojectorroomstartm
    show ben_idle at left
    show samuel_normal_pose at right
    "We both agree that this was a tie and we head over to the projector after some time, I look at the projector as a whole seeing both films in there proper places"
    "I read the labels on the big tape reading the label it says AAXA SCP-A01 on the right gear and AAXA SCP-A02 on the left."
    BEN "I ask Samuel about these"
    SAM "I have no idea, maybe that is the manufacturing label or something?"
    "looking down I see the back of the projector there are four nuts. I look at the single screwdrivers in my hand and get to work."
    "I use the screwdriver head labeled single, the first screw comes out fine and than the second and the third until the back finally plops out onto the floor."
    "Looking inside the device I see many gears and knobs some of them labeled. Also a strange compartment requiring two screws to be removed."
    "These screws were attached to each other, I have never seen anything like this before, their oblique angels making it hard to find out what to do."
    "I ask samuel what this is he looks at it confused than asks me for my screwdriver, I hand it over it him and he picks it up."
    "He thinks for a bit than moves the screwdriver head into place so the one labeled “double” is in line with the one labeled “single” and presses it in."
    "As he presses it in there is a moment of silence before it properly clicks the satisfying sound of the click in my ears brightens my mood a bit as he begins to turn it."
    "Two of the screws pop out at once it seems like they were meant for this specific screwdriver."
    "I switch the screwdriver back to the single mode and I unscrew the last screw the final piece coming out revealing what looks to be a singular burnt out light bulb."
    "I begin to unscrew it but I feel a large shock as I pull my hand back I notice a small prick in my hand, I pull what looks like a small piece of red glass out"
    "it seems to be a glass shard as I start to bleed. I than watch as the lightbulb suddenly turns on as if it was not broken at all it shining a bright red color."
    "Me and Samuel look at each other as he is holding the unplugged power cord to the projector confused”."
    "The tapes start spinning and it makes a loud screeching sound enough for everyone in the base to hear."
    "Me and Samuel cover our ears, the sound still blasting through it. I watch as samuel quickly goes over and plugs the projector in and the sound stops."
    "A red light coming from the projector shows on the wall revealing text on a blue background it has a title that reads“ The unstable darkness” reading the text below"
    "“There exists many artifacts in this world lost to time. Some are secured and contained while others remain lost or stolen to time."
    "One of these affects the two states in this world, the is and isn’t. Combining both into one making fiction into reality, making the false into the true.”"
    "I look at the screen staring at it for a few seconds before I hear I click and a screech come from the projector as the projector light turns white and the slide changes to the next slide revealing what was in the slideshow from earlier today"
    "I pick up the screwdriver and pocked it while responding"
    BEN "Hey I was reading that!"
    "Samuel is about to respond when we hear footsteps behind us looking back we see the drill Sargent walk into the room smiling"
    hide ben_idle
    hide samuel_normal_pose
    show drill_sarg_very_happy at center
    DRI "Well you too really did an exceptional job."
    "He walks up to the projector and unplugs it picking it up as he does, "
    DRI "Your just in time too, we are loading up and preparing to start the mission, lets move out you two!."
    BEN "Sir yes sir!"
    SAM "Sir yes sir!"
    "I grunt as I feel a weight put onto my hand as he plops the projector into my now empty hands and we follow behind him"
    jump outsidewithoutuniform

label abandonsamuel_alt:
    scene bg_outside_projector_room
    show ben_neutral at center
    "I look to the left of the door seeing Samuel standing there reading a book, I pay less attention to him as I head towards the first place I think a screwdriver would be the storage room."
    scene bg_storage_room
    show ben_neutral at center
    "As I approach the storage room I notice a keypad next to the door I head towards the door and examine the keypad."
    "It has letters on it instead of numbers it seems I am spoused to enter a passphrase."
    "I quickly look to my left and look to my right and enter a random passphrase I thing in my head “Butts2012” after a few seconds of nothingness a buzz and a light red glow appear."
    "I stand there staring at the keypad watching the light fade back into place I laugh a bit to myself realizing that my journey ended as fast as it started."
    "I am startled as I hear someone walk up to me a soldier must have overheard me laughing."
    "Looking closer they seem familiar, I realize that they were in the meeting from before, it was the person sitting in the front seat."
    show sultan_talking_pose at right
    RAM "(if not met yet He reaches his hand out to me “want a cig bro?” I am caught off guard by this and instantly deny him)"
    RAM "So what are you laughing about bro?"
    "I watch as the smoke comes out of the lit cigar making little clouds go up into the sky and I respond with"
    BEN "I am [still] (if talked before) looking for a specialty screwdriver do you have any idea were one would be?"
    "He takes the cigar out of his mouth and walks up to the locked door, I watch him enter the passcode with ease almost like he has done this many times before"
    "I follow him inside the storage room and he walks of to a storage draw and slides it open revealing what must be a dozen screwdrivers."
    BEN "I thank him and head back to the projector room to grab the projector to fix, once I come back projector in hand I notice he is still standing in there"
    "using the closet as a place to hide his smoking habits from the public. I look at the projector as a whole seeing both films in there proper places I read the labels on the big tape reading the label"
    "it says AAXA SCP-A01 on the right gear and AAXA SCP-A02 on the left looking down I see the back of the projector there are four nuts."
    "I look at the screwdrivers laid out before me and get to work picking up the screwdriver that fits, the first screw comes out fine and than the second and the third"
    "until the back finally plops out onto the floor. Looking inside the device I see many gears and knobs some of them labeled. Also a strange compartment requiring two screws to be removed."
    "These screws were attached to each other, I have never seen anything like this before, their oblique angels making it hard to find out what screwdriver was needed."
    "After going through each screwdriver one by one I was unable to find out what was needed."
    "As I look at the gears trying to find out what was wrong I hear a flick almost like someone is tossing something and than a burst sound."
    "Looking behind me I see a bright light and than feel a intense heat, the cardboard boxes caught fire!"
    RAM "It wasn’t me bro, I don’t know how this could have happened."
    "He then begins to walk out of the room as the fire spreads not bothering to look back."
    hide sultan_talking_pose
    "The fire spreads from box to box as if it was a chorus singing a song, some big boxes some small boxes the room was quickly getting hotter the white smoke turned to black smoke and the fire soon engulfed the room."
    "I rush towards the projector and pick it up. I quickly run out of the room behind the man, I grab onto his shoulder before the adrenaline wears of and my hand slips"
    "I have to place the heavy projector back down. I kneel down and place it down, I am out of breath… I look up at him as he casually lights his next cigar."
    show sultan_talking_pose at right
    "The world spins around me as I hear beeping and screaming, the smoke creeping out of the storage cabinet into the main hall."
    "I hear a slight creak and feel as it starts raining. With the last bit of my energy I stand up in a turtle position and cover the projector with my body"
    "making sure it does not get soaked as I hear the chaos around me, I hear footsteps and screaming and feel the intense heat hit my back as the fire spread, I start to wince from the pain"
    "and decide it is best that I should just close my eyes and open them back up when this is all over, so I do I revert inwards thinking about my life decisions that bought me here."
    BEN "Maybe if I chose Samuel this wouldn’t have happened. Maybe I should have never joined the army. Maybe if I took action earlier she-."
    BEN "I stop myself no, it is my duty to complete this task, this mission. I chose to serve this country no one else did, no one else would. I take a deep breath and prepare to protect this projector with my life."
    "The few minutes felt like a blur to me, I feel as if my instincts have kicked in and I am unable to move, I feel my legs quiver and the water drip down my shirt."
    "I stayed in that position making sure the projector didn’t get wet like my life depended on it, until my legs finally gave in and I fell onto the floor avoiding the projector."
    "I lay there motionless for many more minuets as I catch my breath, I look up at the ceiling the sprinklers turning off and than looking straight ahead at the man that caused all of this."
    "As I regain my energy I sit back up and stand up I slap the cigar out of his hands, I step on it no I stomp on it as hard as I can putting out the bud until it is fully out."
    hide sultan_talking_pose
    "Looking around I notice a crowd of at least 5 people has gathered around us undoubtedly coming here due to the fire."
    "I ignore them though and return to the projector, it seems like the back piece of the projector was still in the room from when I took it off."
    "However aside from some burn marks on the front the projector seems fine, I look inside the room I was just in most of the floor is flooded, there are various tools and trinkets floating in the water and some ash"
    "the back plate of the projector is nowhere in site if I wanted to get it back on id have to search the room for it."
    "There are two people in fire retardant suits in the room assessing the damages they don’t look particularly happy about it and I am sure ill see them again once they see the camera footage of how this happened."
    show sultan_talk_pose at right
    RAM "Well bro, if I were you id get your clothes replaced and get your weapons the mission starts tonight after all."
    "I think to myself if this is really the best course of action, should I really listen to the man who almost broke my projector and caused this whole debacle in the first place"
    "or should I go get my uniform so I am at least ready for the mission to begin or should I just try to fix this mess I am already and focus on fixing the projector."
    menu:
        "Get Army Uniform":
            jump getuniformwithoutsamuel
        "Go fix projector": 
            jump fixprojectoralone_alt

label fixprojectoralone_alt:
    scene bg_storage_room 
    show ben_neutral at center # Soaked, possibly holding projector
    BEN "I decide to stick with my main mission."
    BEN "Even though my clothes are soaked I need to fix this projector."
    "I take a deep breath and start focusing. I start by doing a damage assessment on the projector."
    "The front lens seems to be damaged while the back piece is missing, most likely destroyed from the fire."
    "The internal parts seem damp, there is possible water damage done to this."
    "The normal screws I took out from earlier are also missing."
    "I need to go back into the storage room to search for the missing parts."
    "I mentally take note of all that is missing and prepare to return to the storage room."
    "I get up from my kneeling stature and I am met with a man in a firefighters uniform staring at me sternly."
    show q3_firefighter_stern at right # Assuming Q3 is firefighter character, need pose
    Q3 "So you’re the sergeants lap dog huh? I heard a lot about you."
    "I stare back at him thinking of what I should say next."
    Q3 "You caused a lot of trouble here you know that?" # Laughing, mocking
    BEN "What are you talking about?"
    Q3 "You were in that room when the fire started right? You could have stopped it but you chose to protect that thing."
    "He points to the projector."
    BEN "This is an important piece of military equipment, it is vital to the mission." # Annoyed
    Q3 "You crayon eaters are always too focused on your damn mission! People could have died in this fire, do you understand that?" # Annoyed
    "I simply stare back at him confused on what he is talking about he scoffs at me and mumbles something while walking off."
    hide q3_firefighter_stern

    "I decide to begin my assessment if it is safe enough to enter back into the room to try to recover the missing screws and backplate."
    "I walk past some people and look into the room. The room has another firefighter in it he looks tired he is holding a bucket."
    "There is some puddles and a lot of burn marks and sut on the floor it looks safe enough to enter."
    "I walk into the entrance of the room my already wet shoes making a squishing sound causing the firefighters to notice me."
    show q3_firefighter_tired at right # Tired firefighter pose
    Q3 "Listen I know you went through a lot this morning but you can’t walk around like that."
    Q3 "I am getting off shift soon so follow me."
    "He puts the bucket he is holding on the floor and walks out of the room guiding me to follow him."
    hide q3_firefighter_tired
    "I obliged picking up the projector and following him past the storage room door into what seems to be a maintenance hallway"
    "my shoes making the same squishing sound as we both walked in silence."
    "Going through a door I see many rectangular storage devices and a stairway to upstairs I see it is blocked by a green container."
    "The firefighter taps on one of the storage devices and it effortlessly opens revealing civilian clothing."
    show q3_firefighter_default at right # Default firefighter pose
    Q3 "Take them." # Implied from "tosses them... telling me to take them"
    "He takes off his firefighter shoes and tosses them to me."
    "I put down the projector and I take off my wet shoes and slip into his shoes, them feeling warm and used."
    "It felt kind of gross wearing someone else’s clothes but It did feel better than what I was wearing before."
    "As the man picks up the full rectangular storage container I tell him"
    BEN "thank you"
    Q3 "Try not to get these dirty too okay?"
    "as he walks upstairs with his civilian clothes."
    hide q3_firefighter_default

    "I pick up my projector and head back to the storage room."
    scene bg_storage_room # Back in the burnt storage room
    show ben_neutral at left
    "As I arrive I can see the crowd has thinned only a few people remain the smoking man he is standing in front of the burnt down room smoking a new cigar."
    show sultan_talking_pose at right # Assuming SUL is the smoking man
    "I walk past him and confront him yet again"
    BEN "Do you have any remorse?"
    "He takes out the cigar from his mouth and waits a bit before blowing another puff until he finally says"
    SUL "Yeah a bit, my mistake man.."
    "I walk past him and enter the room telling him that he has problems."
    hide sultan_talking_pose
    "As I enter the room I head to wear I originally had put the projector finding the spot were it was before strangely dry."
    "I look my around the room and find 3 of the 4 screws I unscrewed picking them up and putting them in my pocket."
    "I begin to pick up some of the burnt boxes the bottom of them spilling out there contents making the floor an even bigger mess."
    "Realizing that this was a mistake I put the burnt boxes back down and I picked up the mess they made."
    "I check near the trash can were the fire started and find a burnt out cigar soaked in water and something next to it."
    "I am confused why this screwdriver would be here though but I don’t question it."
    "After some more time and box moving I eventually find the back plate it took a lot of damage from the initial fire and it seems like it is unrecoverable."
    "I leave the backplate on the floor, I am careless as I put it down and I hear it fall and hit the floor."
    "I notice a hidden trap door on the floor where it fell, it seems the fire damage burnt off its hinge and opened up this trap door revealing a ladder going deeper into the facility."
    "I decide to investigate this trap door as it could have more clues. I leave the projector upstairs and begin my decent into the underground."

    scene black # Or a dark basement scene
    "As I travel down the ladder I notice how the light slowly dims until it is pitch black."
    "I think to myself as I descend down into the darkness that this was probably a bad idea."
    "And that I can climb back up before it gets too dark but my exploratory instincts kick in and I continue to descend."
    "I eventually reach the bottom of the ladder the room pitch black and I can only navigate the room by my other senses."
    "I begin to feel around the walls of this room and I start moving to the right of the ladder I hit another wall more concrete."
    "Moving to the right again I feel more concrete and glass I am careful around the glass as I feel around the section I feel is jagged and sharp almost like the glass is broken."
    "There is some sort of dry liquid on the glass it is rough and crumbly. If I had a light I would be able to tell what it is."
    "Moving more across the wall I reach the left side of the room feeling around there is a door on it is a stappled piece of paper."
    "I rip the paper off of the door and put it in my pocket I also feel something hit my foot, it hurts a bit from walking into it but I bend down and put it in my pocket."
    "I continue following the wall until I reach the ladder again. I decide it is time to climb back up."

    scene bg_storage_room # Back to storage room, light returns
    show ben_neutral at center
    "Climbing back up I reflect on what I just did thinking it was probably not the best idea to go into a pitch dark room without telling anyone."
    "But nevertheless the light gets brighter and brighter until I can see again. I examine what I put in my pocket first the tool."
    "The tool looks like a screwdriver. I pick up the screwdriver from my pocket and examine it closer."
    "Looking at it the screwdriver looks weird. It appears to be a duel headed screwdriver,"
    "this screwdriver having an irregular shape it looked like it had two screwdriver heads bolted into it. They were both labeled with white text saying “single” and “double” on it."
    "I decided to put it in my backpack perhaps this was the screwdriver I was looking for."
    $ inventory.append("Special Screwdriver") # Assuming this is the same screwdriver
    "I check the paper I take out the crumpled paper from my pocket and read it over I find it is a timetable log."
    "It seems like they were doing some experimentation in the laboratory and it seems the experiments were failures."
    "There were many things labeled from testing medical injections to testing new equipment I have never even heard of."
    "All of the equipment listed had a monkeys paw effect to it. One piece of equipment I noticed in particular looked like futuristic power suits"
    "that were able to withstand 2 metric tons of weight being pressed against it but when the user tried to take it off after sustaining damage there skin would peel off with the suit."
    "The more damage the more skin peels off. Another thing of note from the papers were that those three letters appeared again but there was different numbers after them SCP."
    "I think to myself there must be a connection somewhere to these three letters, perhaps it has something to do with these experiments."
    "I pocket the paper thinking that it may be important for later."
    "I decide to head back to the main room to try to repair the projector."
    hide ben_neutral

    scene bootcampinsideprojectorroomstartm # Or current projector room scene
    show ben_neutral at left # Ben brings projector
    "I pick up the projector and head into the projector room I see that the room is vacant aside from a person with a bag on there head sitting there."
    show bagman_default at right
    "He stares at me and than stares at the projector. The bagman walks up to me and says"
    BAG "I-I will help you… I don’t want another incident happening."
    "I lay the projector down and the bagman comes over to me I ask before we start"
    BEN "How can I trust you to not break this thing?"
    BAG "I-I was a lead researcher…" # Hesitates
    BEN "You were? What happened."
    BAG "Before my dismissal I –" # Stops himself
    BAG "Lets just fix this, here I will help you."
    "I look at the projector as a whole seeing both films in there proper places I read the labels on the big tape reading the label it says AAXA SCP-A01 on the right gear and AAXA SCP-A02 on the left."
    "I ask the bag headed man about these and he perks up responds with"
    BAG "They are those tapes object class and designation. AAXA means it is class c and A01 stands for the first month and day."
    BAG "You don’t have to worry about them just know the higher the class the more dangerous the object is."
    "His speech is noticeably less shuddery and more clear it seems he is very interested in this topic."
    "Looking down I see the back of the projector the plate is on the table were I placed it there are three nuts on the floor."
    "The bagman walks over to me and guides my hand to a component of the projector another panel that is screwed in I look at the single screwdrivers in my hand and get to work."
    "I use the screwdriver head labeled single, the first screw comes out fine and than the second and the third until the part finally plops out onto the floor."
    "He continues while he helps me work"
    BAG "Each department has their own official designation of these objects many of them produce anomalous properties."
    BAG "The foundation is trying to standardize these classifications but the dod likes there own way of doing things."
    "Looking inside the device I see many gears and knobs some of them labeled. Also a strange compartment requiring two screws to be removed."
    "These screws were attached to each other, I have never seen anything like this before, their oblique angels making it hard to find out what to do."
    "I ask bagman what this is he looks at it than asks me for my screwdriver, I hand it over it him and he picks it up."
    "He than moves the screwdriver head into place so the one labeled “double” is in line with the one labeled “single” and presses it in."
    "As he presses it he continues"
    BAG "These are only given scientists and important people, they are used to keep normal people from accessing this projector."
    BAG "I don’t even think the sarg knows these are required. They are designed specifically of this SCP."
    "before it properly clicks the satisfying sound of the click in my ears brightens my mood a bit as he begins to turn it."
    "Two of the screws pop out at once it seems like they were meant for this specific screwdriver. He switches the screwdriver back to the single mode"
    "and he begins to unscrew the last screw the final piece coming out revealing what looks to be a singular burnt out light bulb."
    BAG "This bulb is dangerous watch this"
    "he began to unscrew it but a shock sound is heard and he pulled his hand back I notice a small prick in his hand were he held it,"
    "he pulled out what looks like a small piece of red glass out of his hand he starts to bleed and puts his hand in his mouth."
    "I than watch as the lightbulb suddenly turns on as if it was not broken at all it shining a bright red color."
    "Me and bagman look at each other before he tells me to cover my ears. The tapes start spinning and it makes a loud screeching sound enough for everyone in the base to hear."
    "The sound still blasting through it. I watch as bagman says something and quickly goes over and plugs the projector in and the sound stops the screwdriver falling on the floor."
    "A red light coming from the projector shows on the wall revealing text on a blue background it has a title that reads “The unstable darkness” reading the text below"
    "“There exists many artifacts in this world lost to time. Some are secured and contained while others remain lost or stolen to time."
    "One of these affects the two states in this world, the is and isn’t. Combining both into one making fiction into reality, making the false into the true.”"
    "I look at the screen staring at it for a few seconds before I hear I click and a screech come from the projector as the projector light turns white and the slide changes to the next slide revealing what was in the slideshow from earlier today"
    "I pick up the screwdriver and pocked it while responding"
    BEN "Hey I was reading that!"
    "Bagman is about to respond when we hear footsteps behind us looking back we see the drill Sargent walk into the room smiling"
    hide ben_neutral
    hide bagman_default
    show drill_sarg_very_happy at center
    DRI "Well you two really did an exceptional job."
    "He walks up to the projector and unplugs it picking it up as he does, "
    DRI "Your just in time too, we are loading up and preparing to start the mission, lets move out you two!."
    BEN "Sir yes sir!"
    "while he returns to becoming a stuttering mess bagman’s face beat red." # This refers to Bagman
    "I grunt as I feel a weight put onto my hand as he plops the projector into my now empty hands he tells bagman to go on ahead that he wants to talk to me in private,"
    "bagman quickly runs out of the room and after a few seconds the sargent tells me"
    DRI "If I were you, I would stay away from him. He may be smart but he is dangerous he caused a lot of issues for my department in the past."
    "I think to myself what this could mean while following him out into the outside…"
    jump getuniformwithsamuel_alt # Adjusted to point to the renamed duplicate

label getuniformwithoutsamuel:
    scene bg_storage_room # Or appropriate scene after fire/decision
    show ben_neutral at center # Ben is likely soaked
    BEN "I need to get a new uniform and my weapon." # This was part of the thought process before menu
    "I pick up the soaked projector carefully trying not to cut myself on the broken part and glance overat the man who caused this (if he's still around)." # Sultan may or may not be present
    "My goal was not to fix this projector it was get a new uniform. I think back to passing by samuel if I could have gotten him to carry this projector for me."
    "I decide the best course of action is to ask the main desk."

    scene bg_main_desk_area
    show ben_neutral at center # Carrying projector
    "As I walk to the main desk I find two cardboard cutouts of people placed lazily manning the stand. Walking up to the desk I step in a puddle of water getting my already soaked shoes more wet,"
    "slightly annoyed I put the projector on the table with a plunk and static starts coming from the cutouts."
    BEN "Hello? Is anyone there."
    "More static plays from the cutouts, already annoyed I call out"
    BEN "HELLO!?"
    "and receive no response looking closer at the cutouts I realize there are wires attached to them leading into a backroom."
    "I decide to follow them I go around the desk and open the backroom door to find a empty lounge room."
    "The state of it is not the best there is a single couch a mini fridge and a old tv playing static. The walls were peeling off and there was a ton of empty soda cans on the floor."
    "Looking around the room further I notice the wire leads up to a single microphone laid out on the couch covered by books and empty plastic snack bags."
    "I pick up the microphone and speak into it hearing my voice from the other room I realize that this microphone is connected to a speak, it seems they set up this system so they can man the front desk while lounging around."
    "I look a book that I picked up it was labeled “One hundred and one ways to survive a class k scenario”."
    "I humored the book opening it up but was surprised to see a single page stappled into the book locking the other pages out."
    "The page looks like it was written by someone rather than typed out the plain list had detailed instructions on how to use a device called the music nox it described a device that would be able to calm any anomaly into submission."
    "In the book there was big red text written in marker seemingly after the fact saying “MAKE SURE TO BRING SPARE BATTERYS” with the bottom text crossed out."
    "This having no relevant information to the current mission I close the book and place it back where it was before back onto the pile."
    "I head back out of the room that bringing me no closer to getting my uniform I pick back up the projector it feeling more heavy than before,"
    "as I pick it up I think I hear a small clicking sound but upon putting it back down and examining it to see if it is broken it seems that it was just my imagination."
    "I decide to head to the right to the elevator, the elevator has only a single button and it glows a faint yellow hue."

    scene bg_elevator
    show ben_neutral at left # Carrying projector
    show ema default at right # Girl at elevator
    "As I arrive I notice a girl waiting at the elevator she looks skinny in figure and is wearing a standard female military uniform she had a pistol on at her side."
    "Her hair was long and dirty covering most of her face making her eyes hidden. As I wondered who exactally she was."
    "The elevator opens and she walks inside I quickly follow behind her almost missing the door closing."
    "The elevator is cramped and sweaty the old thing makes a screeching sound as it closed, the only light from the elevator being a single led bar in the ceiling,"
    "there were two buttons labeled with images, one of a up arrow and the other a down arrow. She pressed the up arrow already and with a small hitch the elevator starts moving up."
    "We stand there in silence for a few seconds before she breaks the silence her voice is smooth and melodic."
    EMA "You look like you were hit by truck"
    BEN "Yeah, I get that a lot."
    EMA "Your pretty funny you know that. Here you can take this."
    "She handed me a small candy. It was wrapped in red wrapping paper and it was circular shaped."
    $ inventory.append("Red Candy")
    "The elevator dinged open revealing a parking garage."
    hide ema default
    "The garage was mainly empty aside from two stands to the left there was someone dressed as a knight and to the right someone was dressed in a red hood."
    "Both of these people made me uneasy, as I go to examine them further I hear the same voice from before behind me"
    show ema default at right
    EMA "I wouldn’t worry too much about these two, they have been through a lot."
    "She walks towards the man in armor. I follow closely behind her, she talks to the man in armor."
    hide ema default
    show knight default at center
    "His armor shines in the light almost too bright its shine contrasting the painted on pastel background behind him."
    "He is active in conversation engaging with the girl from before he hands her a pack of cigars and pistol ammunition."
    "Refocusing back on him his most notable feature being his hands. His hands seem to unusually contort at the wrists and his hands are stuck in twisted positions"
    "almost like his hands have no bones at all. He uses one hand to push the other hand back into place and they snap together like lego pieces."
    "The girl takes the stuff on the table and he waves goodbye to her."
    BEN "I would like to order a weapon for today’s deployment"
    KNIGHT "What was that you said again."
    BEN "I repeat his question"
    KNIGHT "I will put in a order for you it should be done before your mission starts."
    "He flips a small switch and a tube comes down from the ceiling. He takes out a small paper and asks"
    KNIGHT "So what kind of weapon do you want to use?"
    menu choice_of_weapons_alone2: # Adjusted menu name for uniqueness
        "Pistol  ":
            $ player_weapon_choice = "Pistol"
            jump process_weapon_choice_alone2 # Jump to unique label
        "Rifle  ":
            $ player_weapon_choice = "Rifle"
            jump process_weapon_choice_alone2
        "Shotgun  ":
            $ player_weapon_choice = "Shotgun"
            jump process_weapon_choice_alone2

label process_weapon_choice_alone2: # Unique label
    KNIGHT "Good choice, I wouldn’t personally go for that one but oh well."
    "He places the paper back in the tube and flicks a switch. I watch as the paper quickly goes up into the unknown."
    KNIGHT "Anything else?"
    BEN "..."
    "he than grabs something from his pocked, he puts it in his ear upon further inspection I realize it is headphones. He seems to go back into his own world as his eyes glaze over and the music starts playing in his hear."
    hide knight default
    "I look to the right and see that the lady also has moved onto that stand, something seems wrong with the man at the stand."
    show red_hood default at center
    show ema default at left
    "He is in a red hood but there is something perduring out of his face. I begin to panic in thought a bit but I remember what the girl from earlier told me, she did not want me to think too much about it so I will take her advice."
    "I take a deep breath and I wait in line behind her."
    "I see the hooded man turn around revealing the back of his garments his hood hides his face from full view he grabs an object from a shelf in his stand and asks the girl"
    RED_HOOD "Would you like today’s fortune?"
    EMA "..."
    RED_HOOD "Todays fortune foretells some come complications, you best stay in that computer room of yours.."
    "She seemingly ignores him and walks off"
    hide ema default
    BEN "I would like to put in a order for a new uniform."
    RED_HOOD "I know, that lady already told me."
    BEN "How did she know!"
    RED_HOOD "That is not for me to say, maybe she just had a hunch"
    "he tells me as he walks into the back of his stand. I stand there alone in silence he eventually comes back with a folded up freshly ironed uniform."
    $ inventory.append("New Uniform")
    "He places the uniform ontop of the projector I am holding adding more weight to the already heavy load I am carrying."
    "I head with both the projector and uniform in hand to the bathroom."
    hide red_hood default
    hide ben_neutral

    scene bg_main_desk_area # Placeholder for bathroom
    show ben_neutral at center # Changing
    "I enter an empty stall and put the projector on the floor. The giant machine standing there First my shirt comes off than my pants fall down, I grab the new uniform feeling how it was perfectly"
    "the one from this morning falling on top of the projector. I feel as the stiff fabric stretches with my skin as I pull my new pants up the pants almost being too big for me if it wasn’t for the belt holding them in place."
    "I feel the shirt slip on next as I slide it down my muscular body looking in the mirror I see myself and the broken projector below. I reflect on my life choices as I stare at my reflection everything that lead me up to this moment."
    "I feel the polyester touch across my body as it rigidly comes into place. Next comes on the shoes they are heavy put reliable I than grab my helmet putting it on my head"
    "seeing the pointy metal come out of the top I think to myself it may be able to be used as a tool."
    "I than take one last look at myself in the mirror and leave the changing room."
    hide ben_neutral

    scene bg_elevator # Back to garage
    show ben_neutral at center # In new uniform, carrying projector
    "As I leave the bathroom I see the room still empty no one to by seen, I quickly pick up my old uniform and place it on top of the projector, I begin walking towards the staging area of the mission."
    "As I walk out of the room I see the man in the red hood call out to me in a still hushed voice although he was shouting."
    show red_hood default at right
    "I walk over to him and he offers to hold onto my previous uniform for me."
    "I think about this and figure It would be best to accept his offer he walks out from behind his stand and takes the folded garment himself without saying a word and walks into the backroom."
    hide red_hood default
    "I stand there for a few seconds before regaining my composure, I thank continue on by myself towards the exit door."
    "Upon arriving outside I see soldiers lined up and I see Samuel talking to the drill Sargent I walk up to him"
    jump outsidewithuniform

label outsidewithuniform:
    scene bg_landing_zone_generic
    show ben_neutral at left # In uniform
    show drill_sarg_talk at center
    show samuel_normal_pose at right
    DRI "Everyone is already gathered outside and people are gathering for a very important meeting you will follow me and points will be dedcuted since you are late."
    BEN "SIR YES SIR"
    SAM "SIR YES SIR"
    "and we follow him outside to the landing zone. There are 5 ospery ships outside and soldiers lined up in rows."
    "I quickly head towards my platoon and stand in position. As i stand at the landing zone as a osprey lands, I look to the left to see samuel smiling and starting at the ospery,"
    "looking right I see the sargent standing firm looking determined. The drill sargent speaks pointing to me"
    DRI "Dirtbag, you may have proven yourself in fixing that projector but this will be the real test."
    "The wind from the ospery causes me to put my hands up to cover my eyes from the sheer force of it."
    DRI "This mission may be the last one you go on."
    DRI "I will be staying here, it is your problem now"
    "walking off."
    hide drill_sarg_talk
    hide samuel_normal_pose
    "As he leaves I look back to the center the osprey a sargent walks downs the retractable stairs sizing up everyone."
    show lt_stern at center
    LT "We have a serious sitution on our hands."
    LT "The LZ will be hot by the time of arrival 30 mikes. Once you reach the landing zone you will secure it and evacuate any non combatince as you match your to point alpha."
    LT "Point alpha is a residential complex were your main target designated as the nest. Is there any questions?"
    LT "Good, *points to benjerman* make sure you bring that projector, it is essechial it gets dilvered to the nest"
    BEN "Yes sir!"
    "The drill sargent directs us all onto multiple opserys me and samuel are split up for the first time in awhile."
    "I almost start to worry about but than I calm I don't really care how he holds up on his own I sit down on my seat it feels nice and coushiny."
    hide ben_neutral
    hide lt_stern
    scene bg_osprey_interior_generic
    show ben_sitting at left
    "The first time I have sat down since the inital meeting. The lutenent jumps onto the ship i feel it shake a bit. I feel a tap on my sholder and look to my right."
    show bagman_default at center
    "I get startled as I see someone with a bag on there head sitting next to me."
    BAG "y-you forgot your weapon a-and your uniform"
    BEN "Huh?"
    "he turns around hiding his already hidden face with his hands."
    BAG "..."
    BEN "Why the hell are you wearing a bag of your head and not a helmet. Take that off,"
    "I reach for his bag and he slaps my hand saying"
    BAG "Don't touch that."
    "I figure it is best to not continue my advances to unmask him."
    LT "Is there a problem soldier."
    BEN "Yes sir! This projector is still broken sir!"
    LT "Well shit! You better hope their is a mechanic at the LZ."
    BEN "What if there isn’t?"
    LT "Well that is just too bad you will have to repair it yourself in a live fire zone, good luck maggot."
    "I feel heat in my lap looking down I see the projector is oddly warm. As I look down at the projector on my lap I notice a small part of it moving as the lutenent speaks up"
    LT "We have a very important mission on our hands, multiple undislosed beams of energy have began etruding from the earth. These beams seems to be eminating enrgy capable of blocking out radio and microwaves"
    LT "and have been classfied as a cognitohazard. You will be provided protective glasses and gear cabable of blocking out most of the harmful effects.”"
    "As he talks I put my hand trying to stop the small part from moving, I pull back instinctively as I feel a cut on my finger, it seems the part that was moving was sharp as he continues."
    LT "There are multiple power outages and unkowns when we arrive near the landing zone."
    "A loud screech is heard from the projector and a red light is projected out of it."
    "The lieutenant runs over to me grabbing the screeching projector.  something to me but the sound is way too loud for me to make out what he is saying."
    "He quickly brings the projector into the front of the osprey and the sound is muffled but still clear behind the door after a few minuets a loud spark is heard and the sound stops."
    "He walks back into the room side eyeing me and says"
    LT "Well it seems like you DID fix the projector. Maybe you are not as useless as you claim to be. Too bad the spark plug is burnt out."
    LT "The operation will be designated as operation flashpoint this operation will come in three phases our batalltion has been designated as delta 9 or DT9 for short."
    LT "We will be working in collaberation with another batalltion designated Nu-7. Doing a radiowave anylisis we were able to determine the central location of the main energy sources."
    BAG "W-what was that."
    "His voice is so low I almost did not notice him, nevertheless I answer with"
    BEN "I will tell you later"
    LT "Our main priortiy is to capture and secure the suspected perpetrator of this incident. Looking at your tactical map we will enter from the side windows on the second floor"
    LT "while team delta will enter through the side and main entrances. As you will be in two groups of three you will recommended to form a echelon right formation but if the situation calls for it you may break formation."
    LT "I and the other teams lutenent will stand gaurd outside while you breach and clear the rooms. It will be mandatory during this section to wear the protective gear provided to you, there is no telling what can await you inside that house."
    "I try to focus on something else to calm this madness I look to my side for my sidearm and realize, I never got any weapon."
    "I think about if I should tell this to the lutient but I already caused so much trouble for him already."
    "As I deliberate on if I should my thought is interrupted as "
    LT "Our targets details are classfied however it is imperative that we capture the target alive as he is the key to solving all of this. For any other unautherized personal a shoot on sight policy"
    LT "has been vetted and put in place by the ethics commite. Other organizations will be working closely with us on this mission so the policy is only autherized within 30ft of the targets location."
    LT "I can not stress the importance of capturing the target alive, Your secondary objectives are securing important personal and eliminating all unkown threats in the area."
    LT "The other phases of the plan will be relayed to you once the main objective is complete, do I have any questions?"
    "I look down on my empty lap and look back up, I see bagman give me a quick glance than look back up at the lieutenant."
    "He looks at me and chuckles "
    LT "You will get the projector and sidearm back don’t worry, I will add some straps to it so you can wear it on your back.."
    "The Osprey flies on..."
    return

label outsidewithoutuniform:
    scene bg_landing_zone_generic
    show ben_neutral at left
    show drill_sarg_talk at center
    DRI "Everyone is already gathered outside and people are gathering for a very important meeting you will follow me and points will be dedcuted since you are late."
    BEN "SIR YES SIR"
    "and we follow him outside to the landing zone. There are 5 ospery ships outside and soldiers lined up in rows."
    "I quickly head towards my platoon and stand in position. As i stand at the landing zone as a osprey lands, I look to the left to see samuel smiling and starting at the ospery,"
    "looking right I see the sargent standing firm looking determined. The drill sargent speaks pointing to me"
    DRI "Dirtbag, you may have proven yourself in fixing that projector but this will be the real test."
    "The wind from the ospery causes me to put my hands up to cover my eyes from the sheer force of it."
    DRI "This mission may be the last one you go on."
    DRI "I will be staying here, it is your problem now"
    "walking off."
    hide drill_sarg_talk
    "As he leaves I look back to the center the osprey a sargent walks downs the retractable stairs sizing up everyone."
    show lt_stern at center
    LT "We have a serious sitution on our hands."
    LT "The LZ will be hot by the time of arrival 30 mikes. Once you reach the landing zone you will secure it and evacuate any non combatince as you match your to point alpha."
    LT "Point alpha is a residential complex were your main target designated as the nest. Is there any questions?"
    LT "Good, *points to benjerman* make sure you bring that projector, it is essechial it gets dilvered to the nest"
    BEN "Yes sir!"
    "The drill sargent directs us all onto multiple opserys me and samuel are split up for the first time in awhile."
    "I almost start to worry about but than I calm I don't really care how he holds up on his own I sit down on my seat it feels nice and coushiny."
    hide ben_neutral
    hide lt_stern
    scene bg_osprey_interior_generic
    show ben_sitting at left
    "The first time I have sat down since the inital meeting. The lutenent jumps onto the ship i feel it shake a bit. I feel a tap on my sholder and look to my right."
    show bagman_default at center
    "I get startled as I see someone with a bag on there head sitting next to me."
    BAG "y-you forgot your weapon a-and your uniform"
    BEN "Huh?"
    "he turns around hiding his already hidden face with his hands."
    BEN "Why the hell are you wearing a bag of your head and not a helmet. Take that off,"
    "I reach for his bag and he slaps my hand saying"
    BAG "Don't touch that."
    "I figure it is best to not continue my advances to unmask him."
    LT "Is there a problem soldier."
    BEN "Yes sir! I do not have my weapon or my uniform."
    LT "We are behind schedule already so you will have to make due with what you have."
    BEN "But i have nothing!"
    LT "Well that is just too bad you will have to suck it up! I will read out your orders too."
    LT "Do you understand maggot!"
    "I feel someone put something on my lap lap looking down I see a pistol."
    $ inventory.append("Pistol")
    LT "I said DO YOU UNDERSTAND MAGGOT."
    BEN "SIR YES SIR."
    "As I look down at the gun on my lap the lutenent speaks up"
    LT "We have a very important mission on our hands, multiple undislosed beams of energy have began etruding from the earth. These beams seems to be eminating enrgy capable of blocking out radio and microwaves"
    LT "and have been classfied as a cognitohazard. You will be provided protective glasses and gear cabable of blocking out most of the harmful effects.”"
    "As he talks I hold the weapon in my lap feeling the tightness of the grip, feeling each bump and indent on the gun. I move my hand to the release as he continues."
    LT "There are multiple power outages and unkowns when we arrive near the landing zone. The operation will be designated as operation flashpoint this operation will come in three phases our batalltion has been designated as delta 9 or DT9 for short."
    LT "We will be working in collaberation with another batalltion designated Nu-7. Doing a radiowave anylisis we were able to determine the central location of the main energy sources."
    "The magazine falls out of the gun onto my lap I pick it up and look inside seeing all the bullets that will eventually be used in this gun. I slowly slot the magazine back into the gun."
    LT "Our main priortiy is to capture and secure the suspected perpetrator of this incident. Looking at your tactical map we will enter from the side windows on the second floor"
    LT "while team delta will enter through the side and main entrances. As you will be in two groups of three you will recommended to form a echelon right formation but if the situation calls for it you may break formation."
    LT "I and the other teams lutenent will stand gaurd outside while you breach and clear the rooms. It will be mandatory during this section to wear the protective gear provided to you, there is no telling what can await you inside that house."
    "I move my hand upwards slowly and rhythmically feeling the stock and eventually the whole cylinder of the gun, there are many guns like this here but this one is mine. I cock back the gun slowly. as "
    LT "Our targets details are classfied however it is imperative that we capture the target alive as he is the key to solving all of this. For any other unautherized personal a shoot on sight policy"
    LT "has been vetted and put in place by the ethics commite. Other organizations will be working closely with us on this mission so the policy is only autherized within 30ft of the targets location."
    LT "I can not stress the importance of capturing the target alive, Your secondary objectives are securing important personal and eliminating all unkown threats in the area."
    LT "The other phases of the plan will be relayed to you once the main objective is complete, do I have any questions?"
    "I leave my gun on my lap and look back up, I see bagman give me a quick glance than look back up at the lieutenant. Everyone looking at the lieutenant"
    "The journey continues..."
    return

#EOF