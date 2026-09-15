#all the scenes and their dialogues, separated by state and charakter, to ease further use in the scene classes
#I didn't have time to come up with an elegant way to break the sentences for the DialogueBox
#I just did it manually, so it wouldn't reach outside of the DialogueBox in game

scene_1 = {
    "start":
        ["You slowly open your eyes.",
         "Your head kind of hurts, a slight nausea sits in your stomach.",
         "You look around.",
         "You're sitting in some kind of control console.",
         "A big window is in front of you. It is pitch black.",
         "You stare at it.",
         "It stares back.",
         "You look further and notice a monitor underneath.",
         "A touchpad, joysticks and many, many buttons.",
         "They blink and flash nicely.",
         "Is this some kind of game?",
         "What do you want to do?"
         ],
    "options":
        ["Try the joystick",
         "Try the touchpad"
         ],
    "joystick":
        ["You move the joystick around.",
         "You seem to turn around?",
         "What's this huge swirl of light?",
         "Wait... Is that... the milky way?!"
         ],
    "touchpad": [
        "Woah dude!",
        "I thought you were dead!",
        "Are you alright?"
        ],
    "what happened": [
        "We hit a wormhole.",
        "It was hidden in the nebula we tried to explore.",
        "It beamed us to the other side of the Milky Way, I think...",
        "The travel was rather turbulent, we took quite some damage.",
        "What a Voyager moment, right?",
        "Anyway, the gravity feature was down and you hit your head",
        "pretty hard."
    ],
    "who are you": [
        "I am Robo-John! Your companion.",
        "Turns out, leave humans alone for too long and they'll lose",
        "their minds...",
        "and then their lives, haha.",
        "So I'm here to keep you sane, buddy!",
        "Haha. Fragile little things, you humans.",
        "What is going on?"
    ],
    "wormhole?": [
        "Damn, quite a chunk of your memory is missing! ",
        "I'm always at awe how delicate you humans can be.",
        "You are Nowak!",
        "The first human to conquer space outside of the Milky Way!",
        "Our mission is to explore what we can."
    ],
    "auto_wormhole": [
        "Here! You can see the milky way.",
        "Does this ring a bell for you?"
    ],
    "how long was I out": [
        "It's hard to say.",
        "My sensors were down for some time.",
        "But I'd guess 3 to 4ish days?"
        ],
    "wormhole_n": [
        "Yeah, I remember..",
        "I studied in Warsaw...",
        "I have a wife. And a dog?"
    ],
    "wormhole_r": [
        "That's right.",
        "You left earth 6 years ago.",
        "If you get the ship's sensors running again, we could try",
        "and contact earth. They must be worried.",
        "No contact and no data for a couple of days.",
        "That is not typical for us.",
        "You need to recalibrate the sensors."
    ],
    "catch": [
        "You catch a moving shadow in the corner of your eye.",
        "You turn around and see a bed.",
        "A bed. The faint hum of the ship.",
        "Nothing else."
    ],
    "scoff": [
        "scoff",
        "Eh hello? Are you listening?"
    ],
    "since_scoff": [
        "Since when does he scoff like that?"
    ],
    "calibrate": [
        "Well, as I said the ship took quite some damage",
         "and the sensors need some extra help.",
        "You have to find the right angle",
        "in which the satellites receive any signal.",
        "Although you have have some leeway.",
        "Type a number in the touchpad."
    ],
    "right": [
        "Calibrating Sensors. Please wait",
        "...",
        "Calibrating sensors complete.",
        "Dial SOL-3-COMM-01 to contact the crew.",
        "...",
        "...",
        "...",
        "Just like I thought. The ship is in too bad of a shape.",
        "We need to find ressources to repair it.",
        "I'm going to scan the area.",
        "Scanning area.",
        "...",
        "Scanning complete.",
        "There is a meteoroid cluster nearby.",
        "I gather a faint blinking red light.",
        "We might some ressources there."
    ],
    "wrong": ["No signal. Try something else."],
    "way off": ["I thought you've studied physics to get this job"]
}

scene_2 = {
    "move": [
        "You move through the cosmos.",
        "It feels so surreal. Right, I am Nowak.",
        "But somehow I can barely grasp who I really am.",
        "Is it a dream? Was it ever possible to leave the galaxy?",
        "But I remember snippets of my preparation.",
        "My wife, how we said good bye.",
        "How I trained Robo-John.",
        "The moment we left earth",
        "and I heard the crew cheer on the com.",
        "I just can't remember when we left. 6 years?",
        "I only remember the excitement",
        "when we first saw the border of the galaxy.",
        "Then nothing. It's all black and... just strange."
    ],
    "cat_appears": [
        "Hey, there. Having a headache?"
    ],
    "player_sees_cat": [
        "A black cat?!",
        "Who are you?!"
    ],
    "eggplant_intro": [
        "I'm Eggplant."
    ],
    "cat_contrast": [
        "I surely didn't know we have a cat on board!"
    ],
    "robo_funny": [
        "You humans, always think you're so funny."
    ],
    "player_confused": [
        "No, there is a cat sitting next to me?"
    ],
    "robo_scan": [
        "Haha, you want me to scan the ship now?"
    ],
    "cat_pieces": [
        "Don't mind him. He likes to ignore my existence.",
        "You are trying to put the pieces together, right?",
        "Something's missing up there."
    ],
    "player_how_know": [
        "How do you know?"
    ],
    "cat_logs": [
        "It's always the same."
    ],
    "robo_arrive": [
        "We'll arrive shortly.",
        "Prepare yourself for leaving the ship."
    ],

    "cat_warning": [
        "When you leave the ship,",
        "pay attention to the details.",
        "Do not trust Robo-John."
    ],
    "player_hallucinate": [
        "What the hell is this cat?",
        "Did I hurt my head so badly that I start to hallucinate?",
        "But I thought Robo-John was here to keep me sane?",
        "He's reacting weird.",
        "I am pretty sure I taught him different ways for",
        "psychological care.."
    ],
    "robo_landing": [
        "Landing sequence finished.",
        "You can leave the ship now."
    ],

    "leave_ship": [
        "You pass the pressure chamber.",
        "Let it do its work.",
        "Once the door opens you step a foot outside.",
        "A heavy impression of a deja vu hits you.",
        "But it's not possible.",
        "We are on the other side of the Milky Way.",
        "You couldn't even dream of this place.",
        "But the mind plays tricks like this somehow."
    ],
    "store_appears": [
        "In front of you, on the cluster you landed on, is a building.",
        "On top of it is a shield,",
        "the writing is flashing in a green light.",
        "You get the impression you should be able to read the sign,",
        "but it appears as rubbish again.",
        "If you weren't on the other side of the galaxy,",
        "you'd think it was a small convenience store,",
        "the kind you'd find on any street corner back home."
    ],
    "robo_materials": [
        "You need to search for duranium.",
        "My scan shows that life here was just as advanced as ours.",
        "At least the machinery shows it.",
        "You might find the materials or something just as good."
    ],
    "approach_store": [
        "You walk to the store or whatever this is.",
        "The weight of your gun seems to pull on the belt of your suit.",
        "Your heart starts racing.",
        "What if we are not alone here?",
        "Nervously your hand hovers by the gun.",
        "You just want to call home.",
        "No stress, no fight.",
        "Continue the mission.",
        "Hope that everything turns out right.",
        "You reached the stairs.",
        "Some electronics that look like an old radio",
        "but in a futuristic style is attached above the entry.",
        "A weird unknown language is playing softly.",
        "Rubbish, again.",
        "Robo-John, can you translate this?"
    ],
    "robo_silence": [
        "..."
    ],
    "player_robo_question": [
        "Robo-John?"
    ],
    "robo_syntax": [
        "Continue.",
        "The syntax is weird."
    ],
}

scene_3 = {
    "enter_store": [
        "You enter the store. It is empty.",
        "You can't shake the feeling that it was just left behind.",
        "The cash register is still blinking.",
        "The coffee maker is steaming,",
        "as if the coffee was just brewed.",
        "You step to it and touch the glass.",
        "It is hot.",
        "Behind the register there is a hot dog station.",
        "The sausages are still turning around, getting heated.",
        "You look around and notice many shelves filled with food",
        "and drinks.",
        "There is one shelf with souvenirs it seems.",
        "An alien plushie catches your eye.",
        "Yes, an alien.",
        "Just as the aliens from movies on earth look like.",
        "A thin creature with a big head and big black eyes.",
        "It is green.",
        "You turn around even more.",
        "There is another shelf with motor oil",
        "and other materials used in vehicles.",
        "Also a big box with the writing 'Duranium'.",
        "You found it!"
    ],

    "argue": [
        "Dude, I programmed you!",
        "I know how good you are.",
        "At least try."
    ],
    "cat_shadow": [
        "He doesn't want you to know."
    ],
    "argue_player": [
        "Goosebumps cover your skin.",
        "This soft voice again.",
        "You look around.",
        "Out of the shadows appears the black cat again.",
        "How can it breathe here?",
        "It really must be a fabrication of my head.",
        "I'm going crazy.",
        "And my trusted artificial intelligence seems to not care.",
        "Whatever, somehow I have to manage until I can call earth.",
        "I have to report on this matter.",
        "Robo-John!!"
    ],
    "robo_glitch_welcome": [
        "...welc0me b@ck."
    ],
    "argue_player_2": [
        "Are you having a stroke?"
    ],
    "robo_welcome_back": [
        "WELCOME BACK."
    ],
    "argue_player_3": [
        "Your blood runs cold.",
        "That is horrible.",
        "This can't be.",
        "The sensation of the deja vu overcomes you again.",
        "If you wouldn't be in a suit,",
        "you'd vomit just here at this spot.",
        "What the fuck is happening?!"
    ],
    "robo_aliens": [
        "Haha, that's some humor I like.",
        "The aliens, man.",
        "They are always up for some trickery."
    ],
    "cat_mission": [
        "Nowak, pull yourself together.",
        "Pay attention to the details.",
        "The true mission is not the one you think it is."
    ],

    "notice_door": [
        "You look even further and notice a door."
    ],
    "door_choice_intro": [
        "Willing to investigate?",
        "Or check out the store some more?"
    ]
}

scene_3_door = {
    "investigate": [
        "You go through the door.",
        "You enter a bathroom.",
        "The lights are flashing, it's kind of eerie.",
    ],
    "cat_start": [
        "It's rough, isn't it?",
        "How he behaves?",
        "I'm sure you didn't make him this way."
    ],
    "cat_sink": [
        "The cat. There it is again.",
        "It is sitting in the sink."
    ],
    "cat_notice": [
        "You notice something's off, don't you?"
    ],
    "player_dejavu": [
        "Yeah.. I have the impression, as I've been here before.",
        "I can not explain it.",
        "It can't be.",
        "We are so far from the earth.",
        "And somehow it is, as if I'd went out in the evening",
        "to grab a snack and a beer from our corner shop."
    ],
    "cat_hm": [
        "Hm, right.."
    ],
    "player_oxygen": [
        "Why are you following me?",
        "How are you able to breathe here?",
    ],
    "cat_what": [
        "What do you mean?"
    ],
    "player_vacuum": [
        "There is no oxygen here.",
        "We're in a vacuum."
    ],
    "cat_focus": [
        "You think too much,",
        "but not about the important things.",
        "Focus, Nowak. Focus."
    ],

    "outside": [
        "Why can't I shake the feeling,",
        "that I have done all this before?"
    ],
    "cat_because": [
        "Because you did.."
    ],

    "stay_store": [
        "You found it! Amazing,",
        "now return to the ship.",
        "Put the Duranium in the external processing port",
        "and come back inside.",
        "We could finally call home, my little ET!"
    ],

    "back_in_ship": [
        "Okay, let's dial earth again!"
    ],
    "alarm": [
        "Suddenly an alarm goes off.",
        "It is deafening.",
        "What is going on?!"
    ],
    "robo_attack": [
        "We are being attacked!",
        "Ships have appeared.",
        "2.. 3.. 4..",
        "I can not count them?!",
        "We have to leave.",
        "We have to attack back!"
    ],
    "cat_dont": [
        "Don't.",
        "It's not worth it."
    ],

    "attack": [
        "You start the ship and point the weapons at the ships.",
        "You try to shoot, but seem to miss.",
        "It is as if the ships would consist of mist,",
        "or a faint memory.",
        "You shoot through them.",
        "You try to fly away, somewhere safe."
    ],
    "robo_well_done": [
        "Well done!",
        "Only one ship is left!"
    ],
    "player_confused_attack": [
        "What?",
        "I thought I missed the whole time?"
    ],
    "last_ship": [
        "You aim at the last ship and shoot."
    ],

    "run": [
        "You start the vehicle and try to escape."
    ],
    "cat_why": [
        "Why are you trying this again?",
        "There is no threat out there."
    ],
    "player_shooting": [
        "They are shooting at us!"
    ],
    "robo_shoot_back": [
        "Shoot back!",
        "We can not end like this!"
    ],
    "cat_someday": [
        "Someday, you'll learn."
    ],

    "stay": [
        "But you stay still.",
        "It dawns on you."
    ],
    "cat_understood": [
        "You look like you finally understood."
    ],
    "player_comes_back": [
        "Yes..",
        "it all comes back to me slowly."
    ],
    "robo_move": [
        "Move it!",
        "Or this will be our end!"
    ],
    "player_no_end": [
        "There is no end, is there?",
        "We've done this before."
    ],
    "cat_time": [
        "Yes.",
        "The space is full of wonders,",
        "including breaking time as we know it."
    ],
    "player_how_often": [
        "How often have we done this?"
    ],
    "cat_every_time": [
        "...",
        "You ask this every time."
    ],

    "ending_1": [
        "Farewell, it's been a pleasure to do this again."
    ],
    "ending_2": [
        "Everything becomes bright.",
        "The light fades.",
        "And for the first time.",
        "It does not come back."
    ],
    "robo_shield": [
        "Shield integrity down by 15%.",
        "Hurry up man!"
    ]
}