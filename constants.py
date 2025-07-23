"""Lists all constants (mostly strings) used by AP"""
from BaseClasses import Location, Item


GAME = "Super Paper Mario"


class SuperPaperMarioLocation(Location):
    """A Location belonging to an instance of Super Paper Mario"""
    game: str = GAME


class SuperPaperMarioItem(Item):
    """An Item belonging to an instance of Super Paper Mario"""
    game: str = GAME


HE1 = "Lineland Road"
HE2 = "Mount Lineland"
HE3 = "Yold Desert"
HE4 = "Yold Ruins"
MI1 = "Gloam Valley"
MI2 = "Merlee's Mansion"
MI3 = "Merlee's Mansion"
MI4 = "Merlee's Basement"
TA1 = "The Bitlands"
TA2 = "The Tile Pool"
TA3 = "The Dotwood Tree"
TA4 = "Fort Francis"
SP1 = "Outer Space"
SP2 = "Planet Blobule"
SP3 = "Outer Limits"
SP4 = "The Whoa Zone"
GN1 = "Downtown of Crag"
GN2 = "Gap of Crag"
GN3 = "Floro Caverns"
GN4 = "Floro Caverns"
WA1 = "Sammer's Kingdom"
WA2 = "Sammer's Early Duels"
WA3 = "Sammer's Proving Grounds"
WA4 = "Sammer's Endgame"
AN1 = "The Underwhere"
AN2 = "Underwhere Road"
AN3 = "Overthere Stair"
AN4 = "The Overthere"
LS1 = "Castle Bleck Entry"
LS2 = "Castle Bleck Foyer"
LS3 = "Castle Bleck Interior"
LS4 = "Castle Bleck Inner Sanctum"


class SPMEvent:
    """All Event names"""
    SWITCH_YOLD_RUINS_SQUIG_ROOM = "Hit the Blue Switch in 1-4 Squig Room"
    COMPLETED_FLIPSIDE_PIT = "Completed Flipside Pit"
    COMPLETED_FLOPSIDE_PIT = "Completed Flopside Pit"
    VICTORY = "Victory"


class SPMItem:
    """All Item names"""
    CHARACTER_MARIO = "Mario"
    CHARACTER_PEACH = "Peach"
    CHARACTER_BOWSER = "Bowser"
    CHARACTER_LUIGI = "Luigi"

    ABILITY_FLIP = "Mario's Flip"
    # It'd be cool to randomize more abilities
    # Should be possible by leveraging the "No Skills" debuff from Tech Cursyas.
    # ABILITY_UMBRELLA = "Peach's Umbrella"
    # ABILITY_FIRE = "Bowser's Fire Breath"
    # ABILITY_SUPER_JUMP = "Luigi's Super Jump"

    PIXL_TIPPI = "Tippi"
    PIXL_THOREAU = "Thoreau"
    PIXL_BOOMER = "Boomer"
    PIXL_SLIM = "Slim"
    PIXL_THUDLEY = "Thudley"
    PIXL_CARRIE = "Carrie"
    PIXL_FLEEP = "Fleep"
    PIXL_CUDGE = "Cudge"
    PIXL_DOTTIE = "Dottie"
    PIXL_BARRY = "Barry"
    PIXL_DASHELL = "Dashell"
    PIXL_PICCOLO = "Piccolo"

    RED_PURE_HEART = "Red Pure Heart"
    ORANGE_PURE_HEART = "Orange Pure Heart"
    YELLOW_PURE_HEART = "Yellow Pure Heart"
    GREEN_PURE_HEART = "Green Pure Heart"
    CYAN_PURE_HEART = "Cyan Pure Heart"
    BLUE_PURE_HEART = "Blue Pure Heart"
    PURPLE_PURE_HEART = "Purple Pure Heart"
    WHITE_PURE_HEART = "White Pure Heart"

    CHAPTER_1_KEY = "Chapter 1 Key"
    CHAPTER_2_KEY = "Chapter 2 Key"
    CHAPTER_3_KEY = "Chapter 3 Key"
    CHAPTER_4_KEY = "Chapter 4 Key"
    CHAPTER_5_KEY = "Chapter 5 Key"
    CHAPTER_6_KEY = "Chapter 6 Key"
    CHAPTER_7_KEY = "Chapter 7 Key"
    CHAPTER_8_KEY = "Chapter 8 Key"

    CHAPTER_1_1_KEY = "Chapter 1-1 Key"
    CHAPTER_1_2_KEY = "Chapter 1-2 Key"
    CHAPTER_1_3_KEY = "Chapter 1-3 Key"
    CHAPTER_1_4_KEY = "Chapter 1-4 Key"
    CHAPTER_2_1_KEY = "Chapter 2-1 Key"
    CHAPTER_2_2_KEY = "Chapter 2-2 Key"
    CHAPTER_2_3_KEY = "Chapter 2-3 Key"
    CHAPTER_2_4_KEY = "Chapter 2-4 Key"
    CHAPTER_3_1_KEY = "Chapter 3-1 Key"
    CHAPTER_3_2_KEY = "Chapter 3-2 Key"
    CHAPTER_3_3_KEY = "Chapter 3-3 Key"
    CHAPTER_3_4_KEY = "Chapter 3-4 Key"
    CHAPTER_4_1_KEY = "Chapter 4-1 Key"
    CHAPTER_4_2_KEY = "Chapter 4-2 Key"
    CHAPTER_4_3_KEY = "Chapter 4-3 Key"
    CHAPTER_4_4_KEY = "Chapter 4-4 Key"
    CHAPTER_6_1_KEY = "Chapter 6-1 Key"
    CHAPTER_6_2_KEY = "Chapter 6-2 Key"
    CHAPTER_6_3_KEY = "Chapter 6-3 Key"
    CHAPTER_6_4_KEY = "Chapter 6-4 Key"
    CHAPTER_5_1_KEY = "Chapter 5-1 Key"
    CHAPTER_5_2_KEY = "Chapter 5-2 Key"
    CHAPTER_5_3_KEY = "Chapter 5-3 Key"
    CHAPTER_5_4_KEY = "Chapter 5-4 Key"
    CHAPTER_7_1_KEY = "Chapter 7-1 Key"
    CHAPTER_7_2_KEY = "Chapter 7-2 Key"
    CHAPTER_7_3_KEY = "Chapter 7-3 Key"
    CHAPTER_7_4_KEY = "Chapter 7-4 Key"
    CHAPTER_8_1_KEY = "Chapter 8-1 Key"
    CHAPTER_8_2_KEY = "Chapter 8-2 Key"
    CHAPTER_8_3_KEY = "Chapter 8-3 Key"
    CHAPTER_8_4_KEY = "Chapter 8-4 Key"

    MAP_1 = "Map #1"
    MAP_2 = "Map #2"
    MAP_3 = "Map #3"
    MAP_4 = "Map #4"
    MAP_5 = "Map #5"
    MAP_6 = "Map #6"
    MAP_7 = "Map #7"
    MAP_8 = "Map #8"
    MAP_9 = "Map #9"
    MAP_10 = "Map #10"
    MAP_11 = "Map #11"
    MAP_12 = "Map #12"
    MAP_13 = "Map #13"
    MAP_14 = "Map #14"
    MAP_15 = "Map #15"
    MAP_16 = "Map #16"
    MAP_17 = "Map #17"
    MAP_18 = "Map #18"
    MAP_19 = "Map #19"
    MAP_20 = "Map #20"
    MAP_21 = "Map #21"
    MAP_22 = "Map #22"
    MAP_23 = "Map #23"
    MAP_24 = "Map #24"
    MAP_25 = "Map #25"
    MAP_26 = "Map #26"
    MAP_27 = "Map #27"
    MAP_28 = "Map #28"
    MAP_29 = "Map #29"
    MAP_30 = "Map #30"
    MAP_31 = "Map #31"
    MAP_32 = "Map #32"
    MAP_33 = "Map #33"
    MAP_34 = "Map #34"
    MAP_35 = "Map #35"
    MAP_36 = "Map #36"
    MAP_37 = "Map #37"
    MAP_38 = "Map #38"
    MAP_39 = "Map #39"
    MAP_40 = "Map #40"
    MAP_41 = "Map #41"
    MAP_42 = "Map #42"
    MAP_43 = "Map #43"
    MAP_44 = "Map #44"
    MAP_45 = "Map #45"
    MAP_46 = "Map #46"
    MAP_47 = "Map #47"
    MAP_48 = "Map #48"

    FIRE_BURST = "Fire Burst"
    GHOST_SHROOM = "Ghost Shroom"
    ICE_STORM = "Ice Storm"
    POW_BLOCK = "POW Block"
    SHELL_SHOCK = "Shell Shock"
    SHOOTING_STAR = "Shooting Star"
    THUNDER_RAGE = "Thunder Rage"
    VOLT_SHROOM = "Volt Shroom"

    POISON_SHROOM = "Poison Shroom"

    BONE_IN_CUT = "Bone-In Cut"
    BLOCK_BLOCK = "Block Block"
    COURAGE_SHELL = "Courage Shell"
    HOT_SAUCE = "Hot Sauce"
    MIGHTY_TONIC = "Mighty Tonic"
    TURTLEY_LEAF = "Turtley Leaf"

    BIG_EGG = "Big Egg"
    BLACK_APPLE = "Black Apple"
    BLUE_APPLE = "Blue Apple"
    CAKE_MIX = "Cake Mix"
    DAYZEE_TEAR = "Dayzee Tear"
    DRIED_SHROOM = "Dried Shroom"
    FRESH_PASTA_BUNCH = "Fresh Pasta Bunch"
    FRESH_VEGGIE = "Fresh Veggie"
    GOLDEN_LEAF = "Golden Leaf"
    HONEY_JAR = "Honey Jar"
    HORSETAIL = "Horsetail"
    INKY_SAUCE = "Inky Sauce"
    KEEL_MANGO = "Keel Mango"
    LIFE_SHROOM = "Life Shroom"
    LONG_LAST_SHAKE = "Long-Last Shake"
    MILD_COCOA_BEAN = "Mild Cocoa Bean"
    MISTAKE = "Mistake"
    MUSHROOM = "Mushroom"
    PEACHY_PEACH = "Peachy Peach"
    PINK_APPLE = "Pink Apple"
    POWER_STEAK = "Power Steak"
    PRIMORDIAL_FRUIT = "Primordial Fruit"
    RED_APPLE = "Red Apple"
    SAP_SOUP = "Sap Soup"
    SHROOM_SHAKE = "Shroom Shake"
    SLIMY_SHROOM = "Slimy Shroom"
    SMELLY_HERB = "Smelly Herb"
    SUPER_SHROOM = "Super Shroom"
    SUPER_SHROOM_SHAKE = "Super Shroom Shake"
    ULTRA_SHROOM = "Ultra Shroom"
    ULTRA_SHROOM_SHAKE = "Ultra Shroom Shake"
    WHACKA_BUMP = "Whacka Bump"
    YELLOW_APPLE = "Yellow Apple"

    GOLD_BAR = "Gold Bar"
    GOLD_BAR_X3 = "Gold Bar x3"
    GOLD_MEDAL = "Gold Medal"
    HAPPY_FLOWER = "Happy Flower"
    HP_PLUS = "HP Plus"
    MEGA_STAR = "Mega Star"
    MISTAKE_SLEEPY_SHEEP = "Mistake (Sleepy Sheep)"
    MYSTERY_BOX = "Mystery Box"
    PAL_PILL = "Pal Pill"
    POWER_PLUS = "Power Plus"
    SLEEPY_SHEEP = "Sleepy Sheep"
    SLOW_FLOWER = "Slow Flower"
    SPEED_FLOWER = "Speed Flower"
    STAR_MEDAL = "Star Medal"
    STOP_WATCH = "Stop Watch"

    AWESOME_SNACK = "Awesome Snack"
    BERRY_SNOW_BUNNY = "Berry Snow Bunny"
    BLOCK_MEAL = "Block Meal"
    CHOCOLATE_CAKE = "Chocolate Cake"
    CHOCO_PASTA_DISH = "Choco Pasta Dish"
    COUPLES_CAKE = "Couple's Cake"
    DANGEROUS_DELIGHT = "Dangerous Delight"
    DAYZEE_SYRUP = "Dayzee Syrup"
    DYLLIS_BREAKFAST = "Dyllis Breakfast"
    DYLLIS_DELUXE = "Dyllis Deluxe"
    DYLLIS_DINNER = "Dyllis Dinner"
    DYLLIS_DYNAMITE = "Dyllis Dynamite"
    DYLLIS_LUNCH = "Dyllis Lunch"
    DYLLIS_SPECIAL = "Dyllis Special"
    EGG_BOMB = "Egg Bomb"
    ELECTRO_POP = "Electro Pop"
    EMERGENCY_RATION = "Emergency Ration"
    FRIED_EGG = "Fried Egg"
    FRIED_SHROOM_PLATE = "Fried Shroom Plate"
    FRUIT_PARFAIT = "Fruit Parfait"
    FRUITY_CAKE = "Fruity Cake"
    FRUITY_HAMBURGER = "Fruity Hamburger"
    FRUITY_PUNCH = "Fruity Punch"
    FRUITY_SHROOM = "Fruity Shroom"
    GINGERBREAD_HOUSE = "Gingerbread House"
    GOLDEN_CHOCO_BAR = "Golden Choco-bar"
    GOLDEN_MEAL = "Golden Meal"
    GRADUAL_SYRUP = "Gradual Syrup"
    HAMBURGER = "Hamburger"
    HEALTHY_SALAD = "Healthy Salad"
    HEARTFUL_CAKE = "Heartful Cake"
    HEAVY_MEAL = "Heavy Meal"
    HERB_TEA = "Herb Tea"
    HONEY_CANDY = "Honey Candy"
    HONEY_SHROOM = "Honey Shroom"
    HONEY_SUPER = "Honey Super"
    HORSETAIL_TART = "Horsetail Tart"
    HOT_DOG = "Hot Dog"
    INK_PASTA_DISH = "Ink Pasta Dish"
    INKY_SOUP = "Inky Soup"
    KOOPA_DUMPLING = "Koopa Dumpling"
    KOOPA_PILAF = "Koopa Pilaf"
    KOOPA_TEA = "Koopa Tea"
    KOOPASTA_DISH = "Koopasta Dish"
    LOVE_PUDDING = "Love Pudding"
    LOVE_NOODLE_DISH = "Love Noodle Dish"
    LOVELY_CHOCOLATE = "Lovely Chocolate"
    LUXURIOUS_SET = "Luxurious Set"
    MANGO_JUICE = "Mango Juice"
    MANGO_PUDDING = "Mango Pudding"
    MEAT_PASTA_DISH = "Meat Pasta Dish"
    MEGATON_DINNER = "Megaton Dinner"
    METEOR_MEAL = "Meteor Meal"
    MIRACLE_DINNER = "Miracle Dinner"
    MIXED_SHAKE = "Mixed Shake"
    MOUSSE = "Mousse"
    MUSHROOM_CREPE = "Mushroom Crepe"
    ODD_DINNER = "Odd Dinner"
    OMELETTE_PLATE = "Omelette Plate"
    PEACH_JUICE = "Peach Juice"
    PEACH_TART = "Peach Tart"
    PRIMORDIAL_DINNER = "Primordial Dinner"
    GORGEOUS_STEAK = "Gorgeous Steak"
    ROAST_HORSETAIL = "Roast Horsetail"
    ROAST_SHROOM_DISH = "Roast Shroom Dish"
    ROAST_WHACKA_BUMP = "Roast Whacka Bump"
    SAP_MUFFIN = "Sap Muffin"
    SAP_SYRUP = "Sap Syrup"
    SHROOM_BROTH = "Shroom Broth"
    SHROOM_CAKE = "Shroom Cake"
    SHROOM_CHOCO_BAR = "Shroom Choco-bar"
    SHROOM_DELICACY = "Shroom Delicacy"
    SHROOM_PUDDING = "Shroom Pudding"
    SHROOM_STEAK = "Shroom Steak"
    SKY_JUICE = "Sky Juice"
    SLIMY_EXTRACT = "Slimy Extract"
    SNOW_BUNNY = "Snow Bunny"
    SNOW_CONE = "Snow Cone"
    SPACE_FOOD = "Space Food"
    SPAGHETTI_PLATE = "Spaghetti Plate"
    SPICY_DINNER = "Spicy Dinner"
    SPICY_PASTA_DISH = "Spicy Pasta Dish"
    SPICY_SOUP = "Spicy Soup"
    SPIT_ROAST = "Spit Roast"
    STAMINA_JUICE = "Stamina Juice"
    STANDARD_CHOCOLATE = "Standard Chocolate"
    SWEET_CHOCO_BAR = "Sweet Choco-bar"
    SWEET_COOKIE_SNACK = "Sweet Cookie Snack"
    TOWN_SPECIAL = "Town Special"
    TRIAL_STEW = "Trial Stew"
    VEGGIE_SET = "Veggie Set"
    VOLCANO_SHROOM = "Volcano Shroom"
    WARM_COCOA = "Warm Cocoa"
    WEIRD_EXTRACT = "Weird Extract"

    COOKING_DISK_R = "Cooking Disk R"
    COOKING_DISK_W = "Cooking Disk W"
    COOKING_DISK_Y = "Cooking Disk Y"
    COOKING_DISK_B = "Cooking Disk B"
    COOKING_DISK_G = "Cooking Disk G"
    COOKING_DISK_PU = "Cooking Disk PU"

    RUINS_KEY = "Ruins Key"
    OLD_KEY = "Old Key"
    DOOR_KEY_21 = "Door Key (2-1)"
    HOUSE_KEY = "House Key"
    FORT_KEY = "Fort Key"
    HELMET = "Helmet"
    ANCIENT_CLUE = "Ancient Clue"
    DOOR_KEY_42 = "Door Key (4-2)"
    DIMENSION_KEY = "Dimension Key"
    STONE_TABLET = "Stone Tablet"
    WATER_TABLET = "Water Tablet"
    FIRE_TABLET = "Fire Tablet"
    CAVE_KEY_53 = "Cave Key (5-3)"
    CAVE_KEY_54 = "Cave Key (5-4)"
    CARD_KEY = "Card Key"
    FLORO_SPROUT = "Floro Sprout"
    PETRIFIED_PURE_HEART = "Petrified Pure Heart"
    DOOR_KEY_71 = "Door Key (7-1)"
    DOOR_KEY_72 = "Door Key (7-2)"
    DIET_BOOK = "Diet Book"
    DOOR_KEY_74 = "Door Key (7-4)"
    BLUE_ORB = "Blue Orb"
    YELLOW_ORB = "Yellow Orb"
    RED_ORB = "Red Orb"
    CASTLE_BLECK_KEY_8_1 = "Castle Bleck Key (8-1)"
    CASTLE_BLECK_KEY_8_2 = "Castle Bleck Key (8-2)"
    CASTLE_BLECK_KEY_8_3 = "Castle Bleck Key (8-3)"
    CASTLE_BLECK_KEY_8_4 = "Castle Bleck Key (8-4)"

    GOLDFISH_BOWL_FISH = "Goldfish Bowl (Fish)"
    GOLDFISH_BOWL_EMPTY = "Goldfish Bowl (Empty)"
    CRYSTAL_BALL = "Crystal Ball"
    TRAINING_MACHINE = "Training Machine"
    YOU_KNOW_WHAT = "You-Know-What"
    PAPER = "Paper"
    AUTOGRAPH = "Autograph"
    RANDOM_HOUSE_KEY = "Random House Key"
    GOLDEN_CARD = "Golden Card"

    CATCH_CARD = "Catch Card"
    CATCH_CARD_SP = "Catch Card SP"

    CATCH_CARD_GOOMBA = "Catch Card - Goomba"
    CATCH_CARD_DARK_GOOMBA = "Catch Card - Dark Goomba"
    CATCH_CARD_SPIKED_GOOMBA = "Catch Card - Spiked Goomba"
    CATCH_CARD_DARK_SPIKED_GOOMBA = "Catch Card - Dark Spiked Goomba"
    CATCH_CARD_PARAGOOMBA = "Catch Card - Paragoomba"
    CATCH_CARD_DARK_PARAGOOMBA = "Catch Card - Dark Paragoomba"
    CATCH_CARD_GLOOMBA = "Catch Card - Gloomba"
    CATCH_CARD_HEADBONK_GOOMBA = "Catch Card - Headbonk Goomba"
    CATCH_CARD_DARK_HEADBONK_GOOMBA = "Catch Card - Dark Headbonk Goomba"
    CATCH_CARD_KOOPA_TROOPA = "Catch Card - Koopa Troopa"
    CATCH_CARD_MEGA_KOOPA = "Catch Card - Mega Koopa"
    CATCH_CARD_DARK_KOOPA = "Catch Card - Dark Koopa"
    CATCH_CARD_KOOPATROL = "Catch Card - Koopatrol"
    CATCH_CARD_DARK_KOOPATROL = "Catch Card - Dark Koopatrol"
    CATCH_CARD_PARATROOPA = "Catch Card - Paratroopa"
    CATCH_CARD_DARK_PARATROOPA = "Catch Card - Dark Paratroopa"
    CATCH_CARD_BUZZY_BEETLE = "Catch Card - Buzzy Beetle"
    CATCH_CARD_SPIKE_TOP = "Catch Card - Spike Top"
    CATCH_CARD_DARK_SPIKE_TOP = "Catch Card - Dark Spike Top"
    CATCH_CARD_PARABUZZY = "Catch Card - Parabuzzy"
    CATCH_CARD_SPIKY_PARABUZZY = "Catch Card - Spiky Parabuzzy"
    CATCH_CARD_STONE_BUZZY = "Catch Card - Stone Buzzy"
    CATCH_CARD_DARK_STONE_BUZZY = "Catch Card - Dark Stone Buzzy"
    CATCH_CARD_SPINY = "Catch Card - Spiny"
    CATCH_CARD_DARK_SPINY = "Catch Card - Dark Spiny"
    CATCH_CARD_LAKITU = "Catch Card - Lakitu"
    CATCH_CARD_DULL_BONES = "Catch Card - Dull Bones"
    CATCH_CARD_DARK_DULL_BONES = "Catch Card - Dark Dull Bones"
    CATCH_CARD_DRY_BONES = "Catch Card - Dry Bones"
    CATCH_CARD_HAMMER_BRO = "Catch Card - Hammer Bro"
    CATCH_CARD_DARK_HAMMER_BRO = "Catch Card - Dark Hammer Bro"
    CATCH_CARD_BOOMERANG_BRO = "Catch Card - Boomerang Bro"
    CATCH_CARD_DARK_BOOMERANG_BRO = "Catch Card - Dark Boomerang Bro"
    CATCH_CARD_FIRE_BRO = "Catch Card - Fire Bro"
    CATCH_CARD_DARK_FIRE_BRO = "Catch Card - Dark Fire Bro"
    CATCH_CARD_MAGIKOOPA = "Catch Card - Magikoopa"
    CATCH_CARD_DARK_MAGIKOOPA = "Catch Card - Dark Magikoopa"
    CATCH_CARD_KOOPA_STRIKER = "Catch Card - Koopa Striker"
    CATCH_CARD_TOOPA_STRIKER = "Catch Card - Toopa Striker"
    CATCH_CARD_SOOPA_STRIKER = "Catch Card - Soopa Striker"
    CATCH_CARD_DARK_STRIKER = "Catch Card - Dark Striker"
    CATCH_CARD_CLUBBA = "Catch Card - Clubba"
    CATCH_CARD_DARK_CLUBBA = "Catch Card - Dark Clubba"
    CATCH_CARD_SQUIGLET = "Catch Card - Squiglet"
    CATCH_CARD_SQUIG = "Catch Card - Squig"
    CATCH_CARD_SQUOG = "Catch Card - Squog"
    CATCH_CARD_SQUOINKER = "Catch Card - Squoinker"
    CATCH_CARD_DARK_SQUIGLET = "Catch Card - Dark Squiglet"
    CATCH_CARD_SPROING_OING = "Catch Card - Sproing-Oing"
    CATCH_CARD_BOING_OING = "Catch Card - Boing-Oing"
    CATCH_CARD_ZOING_OING = "Catch Card - Zoing-Oing"
    CATCH_CARD_DARK_SPROING_OING = "Catch Card - Dark Sproing-Oing"
    CATCH_CARD_BOOMBOXER = "Catch Card - Boomboxer"
    CATCH_CARD_BEEPBOXER = "Catch Card - Beepboxer"
    CATCH_CARD_BLASTBOXER = "Catch Card - Blastboxer"
    CATCH_CARD_DARK_BOOMBOXER = "Catch Card - Dark Boomboxer"
    CATCH_CARD_PIRANHA_PLANT = "Catch Card - Piranha Plant"
    CATCH_CARD_PUTRID_PIRANHA = "Catch Card - Putrid Piranha"
    CATCH_CARD_FROST_PIRANHA = "Catch Card - Frost Piranha"
    CATCH_CARD_CRAZEE_DAYZEE = "Catch Card - Crazee Dayzee"
    CATCH_CARD_AMAZY_DAYZEE = "Catch Card - Amazy Dayzee"
    CATCH_CARD_DARK_DAYZEE = "Catch Card - Dark Dayzee"
    CATCH_CARD_FUZZY = "Catch Card - Fuzzy"
    CATCH_CARD_PINK_FUZZY = "Catch Card - Pink Fuzzy"
    CATCH_CARD_DARK_FUZZY = "Catch Card - Dark Fuzzy"
    CATCH_CARD_POKEY = "Catch Card - Pokey"
    CATCH_CARD_POISON_POKEY = "Catch Card - Poison Pokey"
    CATCH_CARD_DARK_POKEY = "Catch Card - Dark Pokey"
    CATCH_CARD_CHEEP_CHEEP = "Catch Card - Cheep Cheep"
    CATCH_CARD_BLOOPER = "Catch Card - Blooper"
    CATCH_CARD_BITTACUDA = "Catch Card - Bittacuda"
    CATCH_CARD_JAWBUS = "Catch Card - Jawbus"
    CATCH_CARD_RAWBUS = "Catch Card - Rawbus"
    CATCH_CARD_DARK_JAWBUS = "Catch Card - Dark Jawbus"
    CATCH_CARD_GAWBUS = "Catch Card - Gawbus"
    CATCH_CARD_SPANIA = "Catch Card - Spania"
    CATCH_CARD_DARK_SPANIA = "Catch Card - Dark Spania"
    CATCH_CARD_CURSYA = "Catch Card - Cursya"
    CATCH_CARD_BACK_CURSYA = "Catch Card - Back Cursya"
    CATCH_CARD_TECH_CURSYA = "Catch Card - Tech Cursya"
    CATCH_CARD_HEAVY_CURSYA = "Catch Card - Heavy Cursya"
    CATCH_CARD_REVERSYA_CURSYA = "Catch Card - Reversya Cursya"
    CATCH_CARD_DARK_CURSYA = "Catch Card - Dark Cursya"
    CATCH_CARD_DARK_TECH_CURSYA = "Catch Card - Dark Tech Cursya"
    CATCH_CARD_DARK_HEAVY_CURSYA = "Catch Card - Dark Heavy Cursya"
    CATCH_CARD_DARK_REVERSYA_CURSYA = "Catch Card - Dark Reversya Cursya"
    CATCH_CARD_SWOOPER = "Catch Card - Swooper"
    CATCH_CARD_CHERBIL = "Catch Card - Cherbil"
    CATCH_CARD_ICE_CHERBIL = "Catch Card - Ice Cherbil"
    CATCH_CARD_POISON_CHERBIL = "Catch Card - Poison Cherbil"
    CATCH_CARD_DARK_CHERBIL = "Catch Card - Dark Cherbil"
    CATCH_CARD_BOO = "Catch Card - Boo"
    CATCH_CARD_DARK_BOO = "Catch Card - Dark Boo"
    CATCH_CARD_DARK_DARK_BOO = "Catch Card - Dark Dark Boo"
    CATCH_CARD_ATOMIC_BOO = "Catch Card - Atomic Boo"
    CATCH_CARD_GROWMEBA = "Catch Card - Growmeba"
    CATCH_CARD_BLOMEBA = "Catch Card - Blomeba"
    CATCH_CARD_CHROMEBA = "Catch Card - Chromeba"
    CATCH_CARD_DARK_GROWMEBA = "Catch Card - Dark Growmeba"
    CATCH_CARD_MISTER_I = "Catch Card - Mister I"
    CATCH_CARD_RED_I = "Catch Card - Red I"
    CATCH_CARD_CHAIN_CHOMP = "Catch Card - Chain Chomp"
    CATCH_CARD_RED_CHOMP = "Catch Card - Red Chomp"
    CATCH_CARD_THE_UNDERCHOMP = "Catch Card - The Underchomp"
    CATCH_CARD_DARK_CHOMP = "Catch Card - Dark Chomp"
    CATCH_CARD_BALD_CLEFT = "Catch Card - Bald Cleft"
    CATCH_CARD_MOON_CLEFT = "Catch Card - Moon Cleft"
    CATCH_CARD_DARK_CLEFT = "Catch Card - Dark Cleft"
    CATCH_CARD_SHLURP = "Catch Card - Shlurp"
    CATCH_CARD_SHLORP = "Catch Card - Shlorp"
    CATCH_CARD_DARK_SHLURP = "Catch Card - Dark Shlurp"
    CATCH_CARD_THWOMP = "Catch Card - Thwomp"
    CATCH_CARD_SPINY_TROMP = "Catch Card - Spiny Tromp"
    CATCH_CARD_SPIKY_TROMP = "Catch Card - Spiky Tromp"
    CATCH_CARD_BULLET_BILL = "Catch Card - Bullet Bill"
    CATCH_CARD_BILL_BLASTER = "Catch Card - Bill Blaster"
    CATCH_CARD_RUFF_PUFF = "Catch Card - Ruff Puff"
    CATCH_CARD_DARK_RUFF_PUFF = "Catch Card - Dark Ruff Puff"
    CATCH_CARD_LAVA_BUBBLE = "Catch Card - Lava Bubble"
    CATCH_CARD_TILEOID_G = "Catch Card - Tileoid G"
    CATCH_CARD_TILEOID_B = "Catch Card - Tileoid B"
    CATCH_CARD_TILEOID_R = "Catch Card - Tileoid R"
    CATCH_CARD_TILEOID_Y = "Catch Card - Tileoid Y"
    CATCH_CARD_DARK_TILEOID = "Catch Card - Dark Tileoid"
    CATCH_CARD_MEOWBOMB = "Catch Card - Meowbomb"
    CATCH_CARD_PATROL_MEOW = "Catch Card - PatrolMeow"
    CATCH_CARD_AIR_MEOW = "Catch Card - AirMeow"
    CATCH_CARD_SURPRISE_MEOW = "Catch Card - SurpriseMeow"
    CATCH_CARD_BIG_MEOW = "Catch Card - BigMeow"
    CATCH_CARD_MEOWMAID = "Catch Card - Meowmaid"
    CATCH_CARD_SECURI_MEOW = "Catch Card - SecuriMeow"
    CATCH_CARD_JELLIEN = "Catch Card - Jellien"
    CATCH_CARD_FOTON = "Catch Card - Foton"
    CATCH_CARD_WARPID = "Catch Card - Warpid"
    CATCH_CARD_EELIGON = "Catch Card - Eeligon"
    CATCH_CARD_HOOLIGON = "Catch Card - Hooligon"
    CATCH_CARD_DARK_EELIGON = "Catch Card - Dark Eeligon"
    CATCH_CARD_LONGATOR = "Catch Card - Longator"
    CATCH_CARD_LONGADILE = "Catch Card - Longadile"
    CATCH_CARD_DARK_LONGATOR = "Catch Card - Dark Longator"
    CATCH_CARD_BARRIBAD = "Catch Card - Barribad"
    CATCH_CARD_SOBARRIBAD = "Catch Card - Sobarribad"
    CATCH_CARD_DARK_BARRIBAD = "Catch Card - Dark Barribad"
    CATCH_CARD_PIGARITHM = "Catch Card - Pigarithm"
    CATCH_CARD_HOGARITHM = "Catch Card - Hogarithm"
    CATCH_CARD_DARK_PIGARITHM = "Catch Card - Dark Pigarithm"
    CATCH_CARD_CHOPPA = "Catch Card - Choppa"
    CATCH_CARD_COPTA = "Catch Card - Copta"
    CATCH_CARD_DARK_CHOPPA = "Catch Card - Dark Choppa"
    CATCH_CARD_MUTH = "Catch Card - Muth"
    CATCH_CARD_MEGA_MUTH = "Catch Card - Mega Muth"
    CATCH_CARD_DARK_MUTH = "Catch Card - Dark Muth"
    CATCH_CARD_FLORO_SAPIEN = "Catch Card - Floro Sapien"
    CATCH_CARD_FLORO_CRAGNIEN = "Catch Card - Floro Cragnien"
    CATCH_CARD_NINJOE = "Catch Card - Ninjoe"
    CATCH_CARD_NINJOHN = "Catch Card - Ninjohn"
    CATCH_CARD_NINJERRY = "Catch Card - Ninjerry"
    CATCH_CARD_DARK_NINJOE = "Catch Card - Dark Ninjoe"
    CATCH_CARD_UNDERHAND = "Catch Card - Underhand"
    CATCH_CARD_SKELLOBIT = "Catch Card - Skellobit"
    CATCH_CARD_SPIKY_SKELLOBIT = "Catch Card - Spiky Skellobit"
    CATCH_CARD_DARK_SKELLOBIT = "Catch Card - Dark Skellobit"
    CATCH_CARD_DARK_SPIKY_SKELLOBIT = "Catch Card - Dark Spiky Skellobit"
    CATCH_CARD_SKELLOBOMBER = "Catch Card - Skellobomber"
    CATCH_CARD_SKELLOBAIT = "Catch Card - Skellobait"
    CATCH_CARD_SPIKY_SKELLOBAIT = "Catch Card - Spiky Skellobait"
    CATCH_CARD_RED_MAGIBLOT = "Catch Card - Red Magiblot"
    CATCH_CARD_BLUE_MAGIBLOT = "Catch Card - Blue Magiblot"
    CATCH_CARD_YELLOW_MAGIBLOT = "Catch Card - Yellow Magiblot"
    CATCH_CARD_DARK_MAGIBLOT = "Catch Card - Dark Magiblot"
    CATCH_CARD_MEGABITE = "Catch Card - Megabite"
    CATCH_CARD_GIGABITE = "Catch Card - Gigabite"
    CATCH_CARD_DARK_MEGABITE = "Catch Card - Dark Megabite"
    CATCH_CARD_DARK_MARIO = "Catch Card - Dark Mario"
    CATCH_CARD_DARK_LUIGI = "Catch Card - Dark Luigi"
    CATCH_CARD_DARK_PEACH = "Catch Card - Dark Peach"
    CATCH_CARD_DARK_BOWSER = "Catch Card - Dark Bowser"
    CATCH_CARD_ZOMBIE_SHROOM = "Catch Card - Zombie Shroom"
    CATCH_CARD_GHOUL_SHROOM = "Catch Card - Ghoul Shroom"
    CATCH_CARD_FRACKTAIL = "Catch Card - Fracktail"
    CATCH_CARD_WRACKTAIL = "Catch Card - Wracktail"
    CATCH_CARD_FRACKLE = "Catch Card - Frackle"
    CATCH_CARD_WRACKLE = "Catch Card - Wrackle"
    CATCH_CARD_BIG_BLOOPER = "Catch Card - Big Blooper"
    CATCH_CARD_FRANCIS = "Catch Card - Francis"
    CATCH_CARD_KING_CROACUS = "Catch Card - King Croacus"
    CATCH_CARD_BONECHILL = "Catch Card - Bonechill"
    CATCH_CARD_COUNT_BLECK = "Catch Card - Count Bleck"
    CATCH_CARD_NASTASIA = "Catch Card - Nastasia"
    CATCH_CARD_O_CHUNKS = "Catch Card - O'Chunks"
    CATCH_CARD_MIMI = "Catch Card - Mimi"
    CATCH_CARD_MR_L = "Catch Card - Mr. L"
    CATCH_CARD_BROBOT = "Catch Card - Brobot"
    CATCH_CARD_BROBOT_L_TYPE = "Catch Card - Brobot L-type"
    CATCH_CARD_DIMENTIO = "Catch Card - Dimentio"
    CATCH_CARD_SUPER_DIMENTIO = "Catch Card - Super Dimentio"
    CATCH_CARD_MERLON = "Catch Card - Merlon"
    CATCH_CARD_NOLREM = "Catch Card - Nolrem"
    CATCH_CARD_MERLUVLEE = "Catch Card - Merluvlee"
    CATCH_CARD_MERLEE = "Catch Card - Merlee"
    CATCH_CARD_BESTOVIUS = "Catch Card - Bestovius"
    CATCH_CARD_OLD_MAN_WATCHITT = "Catch Card - Old Man Watchitt"
    CATCH_CARD_MERLUMINA = "Catch Card - Merlumina"
    CATCH_CARD_THE_INTER_NED = "Catch Card - The InterNed"
    CATCH_CARD_THE_INTER_CHET = "Catch Card - The InterChet"
    CATCH_CARD_WELDERBERG = "Catch Card - Welderberg"
    CATCH_CARD_RED_GREEN = "Catch Card - Red & Green"
    CATCH_CARD_GNIP = "Catch Card - Gnip"
    CATCH_CARD_GNAW = "Catch Card - Gnaw"
    CATCH_CARD_SQUIRPS = "Catch Card - Squirps"
    CATCH_CARD_FLINT_CRAGLEY = "Catch Card - Flint Cragley"
    CATCH_CARD_HORNFELS_MONZO = "Catch Card - Hornfels & Monzo"
    CATCH_CARD_KING_SAMMER = "Catch Card - King Sammer"
    CATCH_CARD_SAMMER_GUY = "Catch Card - Sammer Guy"
    CATCH_CARD_SMALL_SAMMER_GUY = "Catch Card - Small Sammer Guy"
    CATCH_CARD_BIG_SAMMER_GUY = "Catch Card - Big Sammer Guy"
    CATCH_CARD_LUVBI = "Catch Card - Luvbi"
    CATCH_CARD_JAYDES = "Catch Card - Jaydes"
    CATCH_CARD_GRAMBI = "Catch Card - Grambi"
    CATCH_CARD_WHACKA = "Catch Card - Whacka"
    CATCH_CARD_MARIO = "Catch Card - Mario"
    CATCH_CARD_LUIGI = "Catch Card - Luigi"
    CATCH_CARD_PEACH_1 = "Catch Card - Princess Peach (1)"
    CATCH_CARD_PEACH_2 = "Catch Card - Peach (2)"
    CATCH_CARD_PEACH_3 = "Catch Card - Peach (3)"
    CATCH_CARD_BOWSER_1 = "Catch Card - Bowser (1)"
    CATCH_CARD_BOWSER_2 = "Catch Card - Bowser (2)"
    CATCH_CARD_TIPPI = "Catch Card - Tippi"
    CATCH_CARD_THOREAU = "Catch Card - Thoreau"
    CATCH_CARD_BOOMER = "Catch Card - Boomer"
    CATCH_CARD_SLIM = "Catch Card - Slim"
    CATCH_CARD_THUDLEY = "Catch Card - Thudley"
    CATCH_CARD_CARRIE = "Catch Card - Carrie"
    CATCH_CARD_FLEEP = "Catch Card - Fleep"
    CATCH_CARD_CUDGE = "Catch Card - Cudge"
    CATCH_CARD_DOTTIE = "Catch Card - Dottie"
    CATCH_CARD_BARRY = "Catch Card - Barry"
    CATCH_CARD_DASHELL = "Catch Card - Dashell"
    CATCH_CARD_PICCOLO = "Catch Card - Piccolo"
    CATCH_CARD_TIPTRON = "Catch Card - Tiptron"
    CATCH_CARD_GOOMBARIO = "Catch Card - Goombario"
    CATCH_CARD_KOOPER = "Catch Card - Kooper"
    CATCH_CARD_BOMBETTE = "Catch Card - Bombette"
    CATCH_CARD_PARAKARRY = "Catch Card - Parakarry"
    CATCH_CARD_BOW = "Catch Card - Bow"
    CATCH_CARD_WATT = "Catch Card - Watt"
    CATCH_CARD_SUSHIE = "Catch Card - Sushie"
    CATCH_CARD_LAKILESTER = "Catch Card - Lakilester"
    CATCH_CARD_GOOMBELLA = "Catch Card - Goombella"
    CATCH_CARD_KOOPS = "Catch Card - Koops"
    CATCH_CARD_MADAME_FLURRIE = "Catch Card - Madame Flurrie"
    CATCH_CARD_YOSHI = "Catch Card - Yoshi"
    CATCH_CARD_VIVIAN = "Catch Card - Vivian"
    CATCH_CARD_ADMIRAL_BOBBERY = "Catch Card - Admiral Bobbery"
    CATCH_CARD_MS_MOWZ = "Catch Card - Ms. Mowz"
    CATCH_CARD_TOAD = "Catch Card - Toad"

    BACK_CURSYA_TRAP = "Back Cursya Trap"


class SPMLocation:
    """All Location names"""
    STARTING_CHARACTER = "Starting Character"
    STARTING_PIXL = "Starting Pixl"

    FLIPSIDE_MERLONS_GIFT = "Flipside Tower - Merlon's Gift"
    FLIPSIDE_3F_CHEST_IN_PICCOLO_BLOCK = "Flipside 3F - Chest in Piccolo block"
    FLIPSIDE_3F_EAT_A_SPICY_SOUP = "Flipside 3F - Eat a Spicy Soup"
    FLIPSIDE_3F_CHEST_AFTER_INVISIBLE_BLOCKS = "Flipside 3F - Chest after invisible blocks"
    FLIPSIDE_1F_OUTSKIRTS_LEFT_CHEST_IN_HOLE = "Flipside 1F Outskirts - Left chest in hole"
    FLIPSIDE_1F_OUTSKIRTS_RIGHT_CHEST_IN_HOLE = "Flipside 1F Outskirts - Right chest in hole"
    FLIPSIDE_B2_CHEST_AFTER_PIPE = "Flipside B2 - Chest after pipe"
    FLIPSIDE_3F_FISHBOWL = "Flipside 3F - Talk to the kid"
    FLIPSIDE_B1_FREE_FISH = "Flipside B1 - Free Captain Gills"
    FLOPSIDE_B2_CHEST_AFTER_PIPE = "Flopside B2 - Chest after pipe"
    FLOPSIDE_3F_CHEST_IN_PICCOLO_BLOCK = "Flopside 3F - Chest in Piccolo block"
    FLOPSIDE_3F_CHEST_AFTER_INVISIBLE_BLOCKS = "Flopside 3F - Chest after invisible blocks"
    FLOPSIDE_B2_CHASM_CHEST = "Flopside B2 Chasm - Chest"
    FLOPSIDE_B1_BEVERAGARIUM_CHEST1 = "Flopside B1 Beveragarium - Chest 1"
    FLOPSIDE_B1_BEVERAGARIUM_CHEST2 = "Flopside B1 Beveragarium - Chest 2"
    FLOPSIDE_B1_OUTSKIRT_CHEST_BEHIND_PILLAR = "Flopside B1 Outskirt - Chest Behind Pillar"

    # Heart Pillars
    FLIPSIDE_HEART_PILLAR_RED = "Flipside 3F - Red Heart Pillar"
    FLIPSIDE_HEART_PILLAR_ORANGE = "Flipside 1F Outskirts - Orange Heart Pillar"
    FLIPSIDE_HEART_PILLAR_YELLOW = "Flipside B1 Outskirts - Yellow Heart Pillar"
    FLIPSIDE_HEART_PILLAR_GREEN = "Flipside 2F Outskirts - Green Heart Pillar"
    FLOPSIDE_HEART_PILLAR_CYAN = "Flopside 1F Outskirts - Cyan Heart Pillar"
    FLOPSIDE_HEART_PILLAR_BLUE = "Flopside 3F - Blue Heart Pillar"
    FLOPSIDE_HEART_PILLAR_PURPLE = "Flopside B1 Outskirts - Purple Heart Pillar"
    FLOPSIDE_HEART_PILLAR_WHITE = "Flopside 2F Outskirts - White Heart Pillar"

    # Shop Locations
    FLIPSIDE_HOWZITS_1 = "Flipside 2F - Howzit's Shop #1"
    FLIPSIDE_HOWZITS_2 = "Flipside 2F - Howzit's Shop #2"
    FLIPSIDE_HOWZITS_3 = "Flipside 2F - Howzit's Shop #3"
    FLIPSIDE_HOWZITS_4 = "Flipside 2F - Howzit's Shop #4"
    FLIPSIDE_HOWZITS_5 = "Flipside 2F - Howzit's Shop #5"
    FLIPSIDE_HOWZITS_6 = "Flipside 2F - Howzit's Shop #6"
    FLIPSIDE_HOWZITS_7 = "Flipside 2F - Howzit's Shop #7"
    FLIPSIDE_HOWZITS_8 = "Flipside 2F - Howzit's Shop #8"
    FLIPSIDE_HOWZITS_9 = "Flipside 2F - Howzit's Shop #9"
    FLIPSIDE_HOWZITS_10 = "Flipside 2F - Howzit's Shop #10"

    FLIPSIDE_ITTY_BITS_1 = "Flipside B1 - Itty Bits Shop #1"
    FLIPSIDE_ITTY_BITS_2 = "Flipside B1 - Itty Bits Shop #2"
    FLIPSIDE_ITTY_BITS_3 = "Flipside B1 - Itty Bits Shop #3"

    FLOPSIDE_NOTSOS_1 = "Flopside 2F - Notso's Shop #1"
    FLOPSIDE_NOTSOS_2 = "Flopside 2F - Notso's Shop #2"
    FLOPSIDE_NOTSOS_3 = "Flopside 2F - Notso's Shop #3"
    FLOPSIDE_NOTSOS_4 = "Flopside 2F - Notso's Shop #4"
    FLOPSIDE_NOTSOS_5 = "Flopside 2F - Notso's Shop #5"
    FLOPSIDE_NOTSOS_6 = "Flopside 2F - Notso's Shop #6"
    FLOPSIDE_NOTSOS_7 = "Flopside 2F - Notso's Shop #7"
    FLOPSIDE_NOTSOS_8 = "Flopside 2F - Notso's Shop #8"
    FLOPSIDE_NOTSOS_9 = "Flopside 2F - Notso's Shop #9"
    FLOPSIDE_NOTSOS_10 = "Flopside 2F - Notso's Shop #10"

    FLOPSIDE_ITTY_BITS_1 = "Flopside B1 - Itty Bits Shop #1"
    FLOPSIDE_ITTY_BITS_2 = "Flopside B1 - Itty Bits Shop #2"
    FLOPSIDE_ITTY_BITS_3 = "Flopside B1 - Itty Bits Shop #3"

    YOLD_TOWN_HOWZITS_1 = "Yold Town - Howzit's Shop #1"
    YOLD_TOWN_HOWZITS_2 = "Yold Town - Howzit's Shop #2"
    YOLD_TOWN_HOWZITS_3 = "Yold Town - Howzit's Shop #3"
    YOLD_TOWN_HOWZITS_4 = "Yold Town - Howzit's Shop #4"
    YOLD_TOWN_HOWZITS_5 = "Yold Town - Howzit's Shop #5"
    YOLD_TOWN_HOWZITS_6 = "Yold Town - Howzit's Shop #6"
    YOLD_TOWN_HOWZITS_7 = "Yold Town - Howzit's Shop #7"
    YOLD_TOWN_HOWZITS_8 = "Yold Town - Howzit's Shop #8"
    YOLD_TOWN_HOWZITS_9 = "Yold Town - Howzit's Shop #9"
    YOLD_TOWN_HOWZITS_10 = "Yold Town - Howzit's Shop #10"

    DOTWOOD_TREE_ITTY_BITS_1 = "Dotwood Tree - Itty Bits Shop #1"
    DOTWOOD_TREE_ITTY_BITS_2 = "Dotwood Tree - Itty Bits Shop #2"
    DOTWOOD_TREE_ITTY_BITS_3 = "Dotwood Tree - Itty Bits Shop #3"

    OUTER_LIMITS_HOWZITS_TWINKLE_MART_1 = "Outer Limits - Howzit's Twinkle Mart #1"
    OUTER_LIMITS_HOWZITS_TWINKLE_MART_2 = "Outer Limits - Howzit's Twinkle Mart #2"
    OUTER_LIMITS_HOWZITS_TWINKLE_MART_3 = "Outer Limits - Howzit's Twinkle Mart #3"

    DOWNTOWN_CRAG_HOWZITS_1 = "Downtown Crag - Howzit's Shop #1"
    DOWNTOWN_CRAG_HOWZITS_2 = "Downtown Crag - Howzit's Shop #2"
    DOWNTOWN_CRAG_HOWZITS_3 = "Downtown Crag - Howzit's Shop #3"
    DOWNTOWN_CRAG_HOWZITS_4 = "Downtown Crag - Howzit's Shop #4"
    DOWNTOWN_CRAG_HOWZITS_5 = "Downtown Crag - Howzit's Shop #5"
    DOWNTOWN_CRAG_HOWZITS_6 = "Downtown Crag - Howzit's Shop #6"
    DOWNTOWN_CRAG_HOWZITS_7 = "Downtown Crag - Howzit's Shop #7"
    DOWNTOWN_CRAG_HOWZITS_8 = "Downtown Crag - Howzit's Shop #8"
    DOWNTOWN_CRAG_HOWZITS_9 = "Downtown Crag - Howzit's Shop #9"
    DOWNTOWN_CRAG_HOWZITS_10 = "Downtown Crag - Howzit's Shop #10"

    DOWNTOWN_CRAG_ITTY_BITS_1 = "Downtown Crag - Itty Bits Shop #1"
    DOWNTOWN_CRAG_ITTY_BITS_2 = "Downtown Crag - Itty Bits Shop #2"

    THE_OVERTHERE_ITTY_BITS_1 = "The Overthere - Itty Bits Shop #1"
    THE_OVERTHERE_ITTY_BITS_2 = "The Overthere - Itty Bits Shop #2"

    # region Pits
    FLIPSIDE_PIT_10 = "Flipside Pit - Floor 10 Chest"
    FLIPSIDE_PIT_20 = "Flipside Pit - Floor 20 Chest"
    FLIPSIDE_PIT_30 = "Flipside Pit - Floor 30 Chest"
    FLIPSIDE_PIT_40 = "Flipside Pit - Floor 40 Chest"
    FLIPSIDE_PIT_50 = "Flipside Pit - Floor 50 Chest"
    FLIPSIDE_PIT_60 = "Flipside Pit - Floor 60 Chest"
    FLIPSIDE_PIT_70 = "Flipside Pit - Floor 70 Chest"
    FLIPSIDE_PIT_80 = "Flipside Pit - Floor 80 Chest"
    FLIPSIDE_PIT_90 = "Flipside Pit - Floor 90 Chest"
    FLIPSIDE_PIT_100 = "Flipside Pit - Floor 100 Chest"
    FLIPSIDE_PIT_WRACKTAIL = "Flipside Pit - Wracktail"
    FLOPSIDE_PIT_10 = "Flopside Pit - Floor 10 Chest"
    FLOPSIDE_PIT_20 = "Flopside Pit - Floor 20 Chest"
    FLOPSIDE_PIT_30 = "Flopside Pit - Floor 30 Chest"
    FLOPSIDE_PIT_40 = "Flopside Pit - Floor 40 Chest"
    FLOPSIDE_PIT_50 = "Flopside Pit - Floor 50 Chest"
    FLOPSIDE_PIT_60 = "Flopside Pit - Floor 60 Chest"
    FLOPSIDE_PIT_70 = "Flopside Pit - Floor 70 Chest"
    FLOPSIDE_PIT_80 = "Flopside Pit - Floor 80 Chest"
    FLOPSIDE_PIT_90 = "Flopside Pit - Floor 90 Chest"
    FLOPSIDE_PIT_100_1 = "Flopside Pit - Floor 100 Chest #1"
    FLOPSIDE_PIT_100_2 = "Flopside Pit - Floor 100 Chest #2"
    FLOPSIDE_PIT_100_3 = "Flopside Pit - Floor 100 Chest #3"
    FLOPSIDE_PIT_100_4 = "Flopside Pit - Floor 100 Chest #4"
    FLOPSIDE_PIT_100_5 = "Flopside Pit - Floor 100 Chest #5"
    FLOPSIDE_PIT_100_6 = "Flopside Pit - Floor 100 Chest #6"
    FLOPSIDE_PIT_100_7 = "Flopside Pit - Floor 100 Chest #7"
    FLOPSIDE_PIT_100_8 = "Flopside Pit - Floor 100 Chest #8"
    FLOPSIDE_PIT_SHADOO = "Flopside Pit - Shadoo"
    # endregion

    # region Chapter 1
    C11_OPEN_ITEM_ABOVE_BESTOVIUS_HOUSE = "1-1 - Open item above Bestovius' House"
    C11_OPEN_ITEM_INSIDE_BESTOVIUS_HOUSE_HALLWAY = "1-1 - Open item inside Bestovius' House hallway"
    C11_FIRST_OPEN_ITEM_INSIDE_BESTOVIUS_ROOM = "1-1 - First open item inside Bestovius' Room"
    C11_SECOND_OPEN_ITEM_INSIDE_BESTOVIUS_ROOM = "1-1 - Second open item inside Bestovius' Room"
    C11_TALK_TO_BESTOVIUS = "1-1 - Talk to Bestovius"
    C11_CHEST_INSIDE_FIRST_PIPE = "1-1 - Chest inside first pipe"
    C11_OPEN_ITEM_BEHIND_PIPE = "1-1 - Open item behind pipe"
    C11_CHEST_AFTER_STAR_BLOCK = "1-1 - Chest after Star Block"
    C11_STAR_BLOCK = "1-1 - Star Block"

    C12_CHEST_IN_SHORTCUT = "1-2 - Chest in shortcut"
    C12_OPEN_ITEM_ON_TOP_OF_WATCHITTS_HOUSE = "1-2 - Open item on top of Watchitt's house"
    C12_OPEN_ITEM_BEHIND_GREENS_BED = "1-2 - Open item behind Green's bed"
    C12_THOREAU_CHEST = "1-2 - Thoreau chest"
    C12_STAR_BLOCK = "1-2 - Star Block"

    C13_OPEN_ITEM_BEHIND_ROCK_IN_FIRST_ROOM = "1-3 - Open item behind rock in red palm tree room"
    C13_OPEN_ITEM_BEHIND_ROCK_IN_SECOND_ROOM = "1-3 - Open item behind rock in rock arrow room"
    C13_OPEN_ITEM_BEHIND_ROCK_IN_SIXTH_ROOM = "1-3 - Open item behind rock in yellow platform room"
    C13_STAR_BLOCK = "1-3 - Star Block"

    C14_CHEST_IN_SECOND_ROOM = "1-4 - Chest in second room"
    C14_CHEST_IN_SMALL_SPIKY_TROMP_ROOM = "1-4 - Chest in small spiky tromp room"
    C14_OPEN_KEY_BEHIND_BLOCKS = "1-4 - Open key behind blocks"
    C14_OPEN_KEY_BETWEEN_FIRE_BARS = "1-4 - Open key between fire bars"
    C14_HIDDEN_CHEST_AFTER_3D_PATH = "1-4 - Hidden chest after 3D path"
    C14_ORANGE_PURE_HEART = "1-4 - Orange Pure Heart"
    # endregion

    # region Chapter 2
    C21_CHEST_AFTER_SQUIGS = "2-1 - Chest after Squigs"
    C21_BOOMER_CHEST = "2-1 - Boomer Chest"
    C21_CHEST_BEHIND_BOOMER_CHEST = "2-1 - Chest behind Boomer chest"
    C21_LEFT_CHEST_BEFORE_STAR_BLOCK = "2-1 - Left chest before Star Block"
    C21_RIGHT_CHEST_BEFORE_STAR_BLOCK = "2-1 - Right chest before Star Block"
    C21_STAR_BLOCK = "2-1 - Star Block"

    C22_CHEST_ABOVE_ENTRANCE = "2-2 - Chest above entrance"
    C22_CHEST_ON_ROOF = "2-2 - Chest on roof"
    C22_OPEN_ITEM_DRAGGED_BY_ROPE = "2-2 - Open item dragged by rope"
    C22_OPEN_ITEM_HUNG_BY_ROPE = "2-2 - Open item hung by rope"
    C22_CHEST_ABOVE_SPIKE_ROOF = "2-2 - Chest above spike roof"
    C22_STAR_BLOCK = "2-2 - Star Block"

    C23_CHEST_BEHIND_BLOCKS = "2-3 - Chest behind blocks"
    C23_SLIM_CHEST = "2-3 - Slim chest"
    C23_STAR_BLOCK = "2-3 - Star Block"

    C24_OPEN_ITEM_BEHIND_ROOM_08_SIGN = "2-4 - Open item behind Room 08 sign"
    C24_YELLOW_PURE_HEART = "2-4 - Yellow Pure Heart"
    # endregion

    # region Chapter 3
    C31_TALK_TO_BARRY_AFTER_DEFEATING_FRANCIS = "3-1 - Talk to Barry after defeating Francis"
    C31_CHEST_IN_WARP_ZONE_RIGHT_PIPE = "3-1 - Chest in warp zone right pipe"
    C31_OPEN_ITEM_IN_BACKGROUND = "3-1 - Open item in background"
    C31_CHEST_IN_BACKGROUND_PIPE = "3-1 - Chest in background pipe"
    C31_CHEST_ABOVE_COLORFUL_PERSONS = "3-1 - Chest above colorful persons"
    C31_OPEN_ITEM_IN_BACKGROUND_2 = "3-1 - Open item in background 2"
    C31_BOWSER = "3-1 - Bowser"
    C31_STAR_BLOCK = "3-1 - Star Block"

    C32_HIDDEN_CHEST_NEAR_PIPE = "3-2 - Hidden chest near pipe"
    C32_THUDLEY_CHEST = "3-2 - Thudley chest"
    C32_STAR_BLOCK = "3-2 - Star Block"

    C33_CHOMPS_CHEST = "3-3 - Chomps chest"
    C33_STAR_BLOCK = "3-3 - Star Block"

    C34_CHEST_IN_PIPE_OUTSIDE_OF_CASTLE = "3-4 - Chest in pipe outside of castle"
    C34_FREE_CARRIE = "3-4 - Free Carrie"
    C34_RIGHT_FRANCIS_CHAMBER_CHEST = "3-4 - Right Francis chamber chest"
    C34_LEFT_FRANCIS_CHAMBER_CHEST = "3-4 - Left Francis chamber chest"
    C34_GREEN_PURE_HEART = "3-4 - Green Pure Heart"
    # endregion

    # region Chapter 4
    C41_SQUIRPS = "4-1 - Squirps"
    C41_OPEN_ITEM_BEHIND_ASTEROID_1 = "4-1 - Open item behind asteroid 1"
    C41_OPEN_ITEM_BEHIND_ASTEROID_2 = "4-1 - Open item behind asteroid 2"
    C41_STAR_BLOCK = "4-1 - Star Block"

    C42_FLIP_THE_DIMENSIONAL_RIFT = "4-2 - Flip the dimensional rift"
    C42_OPEN_ITEM_IN_CHASM_3_D = "4-2 - Open item in chasm 3D"
    C42_OPEN_ITEM_BEHIND_PIPE_NEAR_BLAPPYS_HOUSE = "4-2 - Open item behind pipe near Blappy's house"
    C42_TALK_TO_BLAPPY = "4-2 - Talk to Blappy"
    C42_FLEEP = "4-2 - Fleep"
    C42_STAR_BLOCK = "4-2 - Star Block"

    C43_OPEN_ITEM_BEHIND_FIRST_BLOCKS = "4-3 - Open item behind first blocks"
    C43_OPEN_ITEM_BEHIND_BLOCKS_IN_MANY_WORMHOLE_ROOM = "4-3 - Open item behind blocks in many wormhole room"
    C43_VISIBLE_OPEN_ITEM_IN_BLOCKS = "4-3 - Visible open item in blocks"
    C43_STAR_BLOCK = "4-3 - Star Block"

    C44_CHEST_NEAR_BARRIBAD = "4-4 - Chest near Barribad"
    C44_CHEST_ABOVE_LOCKED_DOOR = "4-4 - Chest above locked door"
    C44_CHEST_IN_3_BLOCK_ROOM = "4-4 - Chest in 3 block room"
    C44_BLUE_PURE_HEART = "4-4 - Blue Pure Heart"
    # endregion

    # region Chapter 5
    C51_CHEST_NEAR_WHACKA = "5-1 - Chest near Whacka"
    C51_CHEST_AFTER_SHLORPS = "5-1 - Chest after Shlorps"
    C51_CHEST_IN_CHASM_3_D = "5-1 - Chest in chasm 3D"
    C51_STAR_BLOCK = "5-1 - Star Block"

    C52_FIRE_TABLET = "5-2 - Fire Tablet"
    C52_OPEN_ITEM_IN_BACKGROUND = "5-2 - Open item in background"
    C52_OPEN_ITEM_IN_FRONT_OF_PIPE = "5-2 - Open item in front of pipe"
    C52_STONE_TABLET = "5-2 - Stone Tablet"
    C52_WATER_TABLET = "5-2 - Water Tablet"
    C52_CUDGE = "5-2 - Cudge"
    C52_CHEST_NEAR_STAR_BLOCK = "5-2 - Chest near Star Block"
    C52_STAR_BLOCK = "5-2 - Star Block"

    C53_OPEN_ITEM_IN_CAVE = "5-3 - Open item in cave"
    C53_SAVE_CRAGLEY_S_CREW = "5-3 - Save Cragley's crew"
    C53_STAR_BLOCK = "5-3 - Star Block"

    C54_DOTTIE = "5-4 - Dottie"
    C54_OPEN_ITEM_NEAR_PROCESSING_CENTER = "5-4 - Open item near Processing Center"
    C54_OPEN_ITEM_BEHIND_PIPE = "5-4 - Open item behind pipe"
    C54_FLIP_THE_SKULL = "5-4 - Flip the skull"
    C54_DEFEAT_FLORO_CHUNKS = "5-4 - Defeat Floro'Chunks"
    C54_INDIGO_PURE_HEART = "5-4 - Indigo Pure Heart"
    # endregion

    # region Chapter 6
    C61_PETRIFIED_PURE_HEART = "6-1 - Petrified Pure Heart"
    C61_STAR_BLOCK = "6-1 - Star Block"

    C62_STAR_BLOCK = "6-2 - Star Block"

    C63_STAR_BLOCK = "6-3 - Star Block"

    C64_SAMMER_KING_REWARD_1 = "6-4 - Sammer King reward 1"
    C64_SAMMER_KING_REWARD_2 = "6-4 - Sammer King reward 2"
    C64_SAMMER_KING_REWARD_3 = "6-4 - Sammer King reward 3"
    C64_SAMMER_KING_REWARD_4 = "6-4 - Sammer King reward 4"
    C64_SAMMER_KING_REWARD_5 = "6-4 - Sammer King reward 5"
    C64_SAMMER_KING_REWARD_6 = "6-4 - Sammer King reward 6"
    C64_SAMMER_KING_REWARD_7 = "6-4 - Sammer King reward 7"
    C64_STAR_BLOCK = "6-4 - Star Block"
    # endregion

    # region Chapter 7
    C71_CHEST_AFTER_GIGABYTE = "7-1 - Chest after Gigabyte"
    C71_OPEN_ITEM_ABOVE_PIPE = "7-1 - Open item above pipe"
    C71_GIVE_THE_PETRIFIED_PURE_HEART_TO_JAYDES = "7-1 - Give the Petrified Pure Heart to Jaydes"
    C71_LUIGI = "7-1 - Luigi"
    C71_HIDDEN_OPEN_ITEM_NEAR_LUIGI = "7-1 - Hidden open item near Luigi"
    C71_HIDDEN_CHEST_IN_LUIGI_S_ROOM = "7-1 - Hidden chest in Luigi's room"
    C71_STAR_BLOCK = "7-1 - Star Block"

    C72_CHEST_IN_FIRST_DARK_ROOM = "7-2 - Chest in first dark room"
    C72_DEFEAT_BOWSER = "7-2 - Defeat Bowser"
    C72_TALK_TO_HAGRA_AND_GET_THE_BOOK_FROM_THE_D_MAN = "7-2 - Talk to Hagra and get the book from the D-Man"
    C72_BRING_THE_DIET_BOOK_TO_HAGRA = "7-2 - Bring the Diet Book to Hagra"
    C72_STAR_BLOCK = "7-2 - Star Block"

    C73_CHEST_RIGHT_OF_25 = "7-3 - Chest right of 25"
    C73_CHEST_AT_34 = "7-3 - Chest at 34"
    C73_CHEST_LEFT_OF_47 = "7-3 - Chest left of 47"
    C73_WAKE_PEACH_UP = "7-3 - Wake Peach up"
    C73_CHEST_AT_68 = "7-3 - Chest at 68"
    C73_CHEST_RIGHT_OF_69 = "7-3 - Chest right of 69"
    C73_CHEST_RIGHT_OF_CYRRUS = "7-3 - Chest right of Cyrrus"
    C73_CHEST_ATOP_BUILDING_AT_80 = "7-3 - Chest atop building at 80"
    C73_CHEST_BEHIND_STAR_BLOCK = "7-3 - Chest behind Star Block"
    C73_STAR_BLOCK = "7-3 - Star Block"

    C74_SAVE_SUNBI = "7-4 - Save Sunbi"
    C74_CHEST_AFTER_GIGABYTE = "7-4 - Chest after Gigabyte"
    C74_FREE_WHIBBI = "7-4 - Free Whibbi"
    C74_TALK_TO_YEBBI = "7-4 - Talk to Yebbi"
    C74_OPEN_ITEM_ABOVE_TWO_DOORS = "7-4 - Open item above two doors"
    C74_TALK_TO_REBBI = "7-4 - Talk to Rebbi"
    C74_BIG_CHEST_BELOW_REBBI = "7-4 - Big chest below Rebbi"
    C74_TALK_TO_BLUBI_AFTER_WHIBBI = "7-4 - Talk to Blubi after Whibbi"
    C74_CHEST_BEHIND_STAIRS = "7-4 - Chest behind stairs"
    C74_CHEST_FAR_RIGHT_OF_MELEE = "7-4 - Chest far right of melee"
    C74_WHITE_PURE_HEART = "7-4 - White Pure Heart"
    # endregion

    # region Chapter 8
    C81_RIGHT_CHEST_ABOVE_PEACH_CUTSCENE_START = "8-1 - Right chest above Peach cutscene start"
    C81_LEFT_CHEST_ABOVE_PEACH_CUTSCENE_START = "8-1 - Left chest above Peach cutscene start"
    C81_CHEST_IN_SOOPA_STRIKER_HALLWAY = "8-1 - Chest in Soopa Striker hallway"

    C82_LEFT_CHEST_ABOVE_MERLON_ROOM = "8-2 - Left chest above Merlon room"
    C82_MIDDLE_CHEST_ABOVE_MERLON_ROOM = "8-2 - Middle chest above Merlon room"
    C82_RIGHT_CHEST_ABOVE_MERLON_ROOM = "8-2 - Right chest above Merlon room"
    C82_OPEN_ITEM_BEHIND_5TH_PIPE = "8-2 - Open item behind 5th pipe"
    C82_CHEST_IN_CURSYA_ROOM = "8-2 - Chest in Cursya room"
    C82_FIRST_HUNG_ITEM = "8-2 - First hung item"
    C82_SECOND_HUNG_ITEM = "8-2 - Second hung item"
    C82_THIRD_HUNG_ITEM = "8-2 - Third hung item"
    C82_DEFEAT_THE_CHROMEBA = "8-2 - Defeat the Chromeba"
    C82_MERLEES_THUNDER_RAGE = "8-2 - Merlee's Thunder Rage"

    C83_RIGHT_CHEST_BEHIND_FIRST_HALL_OF_MIRRORS = "8-3 - Right chest behind first hall of mirrors"
    C83_LEFT_CHEST_BEHIND_FIRST_HALL_OF_MIRRORS = "8-3 - Left chest behind first hall of mirrors"
    C83_CHEST_AFTER_BLOCK_PUZZLE = "8-3 - Chest after block puzzle"
    C83_RIGHT_CHEST_BEHIND_SECOND_HALL_OF_MIRRORS = "8-3 - Right chest behind second hall of mirrors"
    C83_LEFT_CHEST_BEHIND_SECOND_HALL_OF_MIRRORS = "8-3 - Left chest behind second hall of mirrors"

    C84_CHEST_AFTER_TINY_PASSAGE = "8-4 - Chest after tiny passage"
    C84_CHEST_IN_FIRST_3_D_HALLWAYS = "8-4 - Chest in first 3D hallways"
    C84_CHEST_IN_SECOND_3_D_HALLWAYS = "8-4 - Chest in second 3D hallways"
    C84_CHEST_IN_THIRD_3_D_HALLWAYS = "8-4 - Chest in third 3D hallways"
    # endregion

    # Fleep Maps
    FLIPSIDE_3RD_FLOOR_MAP_01 = "Flipside 3F - Map #01"
    BETWEEN_DIMENSIONS = "Between Dimensions"
    FLIPSIDE_B1_MAP_03 = "Flipside B1 - Map #03"
    FLIPSIDE_ARCADE_MAP_04 = "Flipside Arcade - Map #04"
    FLOPSIDE_3RD_FLOOR_MAP_05 = "Flopside 3F - Map #05"
    M11_MAP_06 = "1-1 - Map #06"
    M12_MAP_07 = "1-2 - Map #07"
    M12_MAP_08 = "1-2 - Map #08"
    M13_MAP_09 = "1-3 - Map #09"
    M13_MAP_10 = "1-3 - Map #10"
    M14_MAP_11 = "1-4 - Map #11"
    M21_MAP_12 = "2-1 - Map #12"
    M22_MAP_13 = "2-2 - Map #13"
    M22_MAP_14 = "2-2 - Map #14"
    M23_MAP_15 = "2-3 - Map #15"
    M24_MAP_16 = "2-4 - Map #16"
    M24_MAP_17 = "2-4 - Map #17"
    M31_MAP_18 = "3-1 - Map #18"
    M31_MAP_19 = "3-1 - Map #19"
    M32_MAP_20 = "3-2 - Map #20"
    M32_MAP_21 = "3-2 - Map #21"
    M33_MAP_22 = "3-3 - Map #22"
    M34_MAP_23 = "3-4 - Map #23"
    M34_MAP_24 = "3-4 - Map #24"
    M42_MAP_25 = "4-2 - Map #25"
    M42_MAP_26 = "4-2 - Map #26"
    M43_MAP_27 = "4-3 - Map #27"
    M44_MAP_28 = "4-4 - Map #28"
    M44_MAP_29 = "4-4 - Map #29"
    M51_MAP_30 = "5-1 - Map #30"
    M51_MAP_31 = "5-1 - Map #31"
    M52_MAP_32 = "5-2 - Map #32"
    M52_MAP_33 = "5-2 - Map #33"
    M53_MAP_34 = "5-3 - Map #34"
    M53_MAP_35 = "5-3 - Map #35"
    M54_MAP_36 = "5-4 - Map #36"
    M54_MAP_37 = "5-4 - Map #37"
    M71_MAP_38 = "7-1 - Map #38"
    M71_MAP_39 = "7-1 - Map #39"
    M72_MAP_40 = "7-2 - Map #40"
    M72_MAP_41 = "7-2 - Map #41"
    M73_MAP_42 = "7-3 - Map #42"
    M74_MAP_43 = "7-4 - Map #43"
    M74_MAP_44 = "7-4 - Map #44"
    M74_MAP_45 = "7-4 - Map #45"
    M81_MAP_46 = "8-1 - Map #46"
    M83_MAP_47 = "8-3 - Map #47"
    M84_MAP_48 = "8-4 - Map #48"

    # Piccolo fetch quest
    PICCOLO_FETCH_WATCHITT_1 = "1-2 - Talk to Watchitt after talking to Merlee, Merluvlee and Bestovius"
    PICCOLO_FETCH_MERLUMINA = "1-4 - Ask Merlumina to sign the Paper"
    PICCOLO_FETCH_WATCHITT_2 = "1-2 - Give the Autograph to Watchitt"
    PICCOLO_FETCH_BESTOVIUS = "1-1 - Bring the You-Know-What to Bestovius"
    PICCOLO_FETCH_MERLUVLEE = "Flipside 2F - Take the Training Machine to Merluvlee"
    PICCOLO_FETCH_MERLEE = "Flopside 2F - Take the Crystal Ball to Merlee"
    PICCOLO_FETCH_END = "Flopside 1F - Chest in locked house"

    # Chapter Ends
    CHAPTER_1_1_END = "Chapter 1-1 End"
    CHAPTER_1_2_END = "Chapter 1-2 End"
    CHAPTER_1_3_END = "Chapter 1-3 End"
    CHAPTER_1_4_END = "Chapter 1-4 End"
    CHAPTER_2_1_END = "Chapter 2-1 End"
    CHAPTER_2_2_END = "Chapter 2-2 End"
    CHAPTER_2_3_END = "Chapter 2-3 End"
    CHAPTER_2_4_END = "Chapter 2-4 End"
    CHAPTER_3_1_END = "Chapter 3-1 End"
    CHAPTER_3_2_END = "Chapter 3-2 End"
    CHAPTER_3_3_END = "Chapter 3-3 End"
    CHAPTER_3_4_END = "Chapter 3-4 End"
    CHAPTER_4_1_END = "Chapter 4-1 End"
    CHAPTER_4_2_END = "Chapter 4-2 End"
    CHAPTER_4_3_END = "Chapter 4-3 End"
    CHAPTER_4_4_END = "Chapter 4-4 End"
    CHAPTER_5_1_END = "Chapter 5-1 End"
    CHAPTER_5_2_END = "Chapter 5-2 End"
    CHAPTER_5_3_END = "Chapter 5-3 End"
    CHAPTER_5_4_END = "Chapter 5-4 End"
    CHAPTER_6_END = "Chapter 6 End"
    CHAPTER_7_1_END = "Chapter 7-1 End"
    CHAPTER_7_2_END = "Chapter 7-2 End"
    CHAPTER_7_3_END = "Chapter 7-3 End"
    CHAPTER_7_4_END = "Chapter 7-4 End"
    CHAPTER_8_1_END = "Chapter 8-1 End"
    CHAPTER_8_2_END = "Chapter 8-2 End"
    CHAPTER_8_3_END = "Chapter 8-3 End"
    CHAPTER_8_4_END = "Defeated Super Dimentio"


class SPMRegion:
    """Regions are named as AAABB where AAA is the 3 character level code and
    BB is the screen number.
    Some levels/screens may have been divided into more regions such as
    AAABB_LAYER0. This is necessary because some screens might change the
    access rules for items inside depending on which entrance you use.
    """
    # Flipside
    MAC01_LAYER1 = "Flipside 3F - Layer 1"
    MAC01_LAYER2 = "Flipside 3F - Layer 2"
    MAC02_LAYER1 = "Flipside 2F - Layer 1"  # And tower, starting region
    MAC02_L_TOWER = "Flipside Tower"
    MAC02_LAYER2 = "Flipside 2F - Layer 2"
    MAC02_LAYER3 = "Flipside 2F Outskirts - Layer 3"
    MAC03_LAYER1 = "Flipside 1F - Mirror Hall"
    MAC03_LAYER2 = "Flopside 1F - Mirror Hall"
    MAC04_LAYER1 = "Flipside B1"
    MAC04_ITTY_BITS = "Flipside B1 - Itty Bits"
    # MAC04_ARCADE_PIPE = "Flipside Beveragarium - Pipe Room"
    MAC05_LAYER1 = "Flipside B2 - Layer 1"
    MAC05_LAYER2 = "Flipside B2 - Layer 2"
    MAC06_LAYER1 = "Flipside 1F Outskirts - Interior Side"
    MAC06_LAYER2 = "Flipside 1F Outskirts - Pillar Side"
    MAC07_LAYER1 = "Flipside B1 Outskirts - Layer 1"
    MAC07_LAYER2 = "Flipside B1 Outskirts - Layer 2"
    MAC08 = "Flipside 1F Outskirts - Chasm"
    MAC09_LAYER1 = "Flipside 1F - Layer 1"
    MAC09_LAYER2 = "Flipside 1F - Layer 2"
    MAC09_LAYER3 = "Flipside 1F - Layer 3"
    L_FLIPSIDE_PIT = "Flipside Pit of 100 Trials"

    # Flopside
    MAC11_LAYER1 = "Flopside 3F - Layer 1"
    MAC11_LAYER2 = "Flopside 3F - Layer 2"
    MAC12_LAYER1 = "Flopside 2F - Layer 1"
    MAC12_L_TOWER = "Flopside Tower"
    MAC12_LAYER2 = "Flopside 2F - Layer 2"
    MAC12_LAYER3 = "Flopside 2F - Layer 3"
    MAC14_RIGHT = "Flopside B1 - Right Side"
    MAC14_LEFT = "Flopside B1 - Left Side"
    MAC14_L_ITTY_BITS = "Flopside B1 - Itty Bits"
    MAC14_L_BACK_BEVERAGARIUM = "Flopside Beveragarium - Back Room"
    MAC15_LAYER1 = "Flopside B2 - Layer 1"
    MAC15_LAYER2 = "Flopside B2 - Layer 2"
    MAC16_LAYER1 = "Flopside 1F Outskirts - Layer 1"
    MAC16_LAYER2 = "Flopside 1F Outskirts - Layer 2"
    MAC17_LAYER1 = "Flopside B1 Outskirts - Layer 1"
    MAC17_LAYER2 = "Flopside B1 Outskirts - Layer 2"
    MAC18 = "Flopside B2 - Chasm"
    MAC19_LAYER1 = "Flopside 1F - Layer 1"
    MAC19_LAYER2 = "Flopside 1F - Layer 2"
    MAC19_LAYER3 = "Flopside 1F - Layer 3"
    # MAC22  # Cutscenes
    # MAC30  # Arcade
    L_FLOPSIDE_PIT = "Flopside Pit of 100 Trials"

    # 1-1: The Adventure Unfolds
    HE101 = f"{HE1} - Outside Bestovius' House"
    HE102 = f"{HE1} - Hills"
    HE103 = f"{HE1} - Underground"
    HE104 = f"{HE1} - Stairs"
    HE105 = f"{HE1} - Star Block"
    HE106 = f"{HE1} - Bestovius' Room"

    # 1-2: Afoot in the Foothills
    HE201 = f"{HE2} - Climb with Spinning Devices"
    HE202 = f"{HE2} - Spiny Tromp Hill"
    HE203 = f"{HE2} - Yold Town"
    HE204 = f"{HE2} - Red's House"
    HE205 = f"{HE2} - Green's House"
    HE206 = f"{HE2} - Underground Thwomps"
    HE207 = f"{HE2} - Locked Room with Thoreau"
    HE208 = f"{HE2} - Underground Coins"
    HE209 = f"{HE2} - Underground Corridor"

    # 1-3: The Sands of Yold
    HE301 = f"{HE3} - Red Palm Tree"
    HE302 = f"{HE3} - Rock Arrow"
    HE303 = f"{HE3} - Save Block"
    HE304 = f"{HE3} - O'Chunks"
    HE305 = f"{HE3} - Underground"
    HE306 = f"{HE3} - Yellow Moving Platform"
    HE307 = f"{HE3} - Blue Stone"
    HE308 = f"{HE3} - Star Block"

    # 1-4: Monster of the Ruins
    HE401 = f"{HE4} - Entrance"
    HE402 = f"{HE4} - 3 Sand Pits"
    HE403 = f"{HE4} - Fire Bar"
    HE404 = f"{HE4} - Spiky Tromp"
    HE405 = f"{HE4} - Large Sand Pit"
    HE406 = f"{HE4} - Blue Switch"
    HE407 = f"{HE4} - Sealed Item"
    HE408 = f"{HE4} - Spiky Tromp Cages"
    HE409 = f"{HE4} - Staircase"
    HE410 = f"{HE4} - Fracktail"
    HE411 = f"{HE4} - Star Block"
    HE412 = f"{HE4} - Hidden Platform"

    # 2-1: Bogging to Merlee's
    MI101 = f"{MI1} - Entrance"
    # MI102 = f"{MI1} - "
    # MI103 = f"{MI1} - "
    # MI104 = f"{MI1} - "
    # MI105 = f"{MI1} - "
    # MI106 = f"{MI1} - "
    # MI107 = f"{MI1} - "
    # MI108 = f"{MI1} - "
    # MI109 = f"{MI1} - "
    # MI110 = f"{MI1} - "
    # MI111 = f"{MI1} - "

    # 2-2: Tricks, Treats, Traps
    MI201 = f"{MI2} - Entrance"
    # MI202 = f"{MI2} - "
    # MI203 = f"{MI2} - "
    # MI204 = f"{MI2} - "
    # MI205 = f"{MI2} - "
    # MI206 = f"{MI2} - "
    # MI207 = f"{MI2} - "
    # MI208 = f"{MI2} - "
    # MI209 = f"{MI2} - "
    # MI210 = f"{MI2} - "
    # MI211 = f"{MI2} - "

    # 2-3: Breaking the Bank
    MI301 = f"{MI3} - Entrance"
    # MI302 = f"{MI3} - "
    # MI303 = f"{MI3} - "
    # MI304 = f"{MI3} - "
    # MI305 = f"{MI3} - "
    # MI306 = f"{MI3} - "

    # 2-4: The Basement Face-Off
    MI401 = f"{MI4} - Entrance"
    # MI402 = f"{MI4} - "
    # MI403 = f"{MI4} - "
    # MI404 = f"{MI4} - "
    # MI405 = f"{MI4} - "
    # MI406 = f"{MI4} - "
    # MI407 = f"{MI4} - "
    # MI408 = f"{MI4} - "
    # MI409 = f"{MI4} - "
    # MI410 = f"{MI4} - "
    # MI411 = f"{MI4} - "
    # MI412 = f"{MI4} - "
    # MI413 = f"{MI4} - "
    # MI414 = f"{MI4} - "
    # MI415 = f"{MI4} - "

    # 3-1: When Geeks Attack
    TA101 = f"{TA1} - Entrance"
    # TA102 = f"{TA1} - "
    # TA103 = f"{TA1} - "
    # TA104 = f"{TA1} - "
    # TA105 = f"{TA1} - "
    # TA106 = f"{TA1} - "
    # TA107 = f"{TA1} - "
    # TA108 = f"{TA1} - "
    # TA109 = f"{TA1} - "

    # 3-2: Bloops Ahoy
    TA201 = f"{TA2} - Entrance"
    # TA202 = f"{TA2} - "
    # TA203 = f"{TA2} - "
    # TA204 = f"{TA2} - "
    # TA205 = f"{TA2} - "
    # TA206 = f"{TA2} - "

    # 3-3: Up, Up, and a Tree
    TA301 = f"{TA3} - Entrance"
    # TA302 = f"{TA3} - "
    # TA303 = f"{TA3} - "
    # TA304 = f"{TA3} - "
    # TA305 = f"{TA3} - "
    # TA306 = f"{TA3} - "
    # TA307 = f"{TA3} - "
    # TA308 = f"{TA3} - "

    # 3-4: The Battle of Fort Francis
    TA401 = f"{TA4} - Entrance"
    # TA402 = f"{TA4} - "
    # TA403 = f"{TA4} - "
    # TA404 = f"{TA4} - "
    # TA405 = f"{TA4} - "
    # TA406 = f"{TA4} - "
    # TA407 = f"{TA4} - "
    # TA408 = f"{TA4} - "
    # TA409 = f"{TA4} - "
    # TA410 = f"{TA4} - "
    # TA411 = f"{TA4} - "
    # TA412 = f"{TA4} - "
    # TA413 = f"{TA4} - "
    # TA414 = f"{TA4} - "
    # TA415 = f"{TA4} - "

    # 4-1: Into Outer Space
    SP101 = f"{SP1} - Entrance"
    # SP102 = f"{SP1} - "
    # SP103 = f"{SP1} - "
    # SP104 = f"{SP1} - "
    # SP105 = f"{SP1} - "
    # SP106 = f"{SP1} - "
    # SP107 = f"{SP1} - "

    # 4-2: A Paper Emergency
    SP201 = f"{SP2} - Entrance"
    # SP202 = f"{SP2} - "
    # SP203 = f"{SP2} - "
    # SP204 = f"{SP2} - "
    # SP205 = f"{SP2} - "
    # SP206 = f"{SP2} - "
    # SP207 = f"{SP2} - "
    # SP208 = f"{SP2} - "
    # SP209 = f"{SP2} - "
    # SP210 = f"{SP2} - "

    # 4-3: The Gates of Space
    SP301 = f"{SP3} - Entrance"
    # SP302 = f"{SP3} - "
    # SP303 = f"{SP3} - "
    # SP304 = f"{SP3} - "
    # SP305 = f"{SP3} - "
    # SP306 = f"{SP3} - "
    # SP307 = f"{SP3} - "

    # 4-4: The Mysterious Mr. L
    SP401 = f"{SP4} - Entrance"
    # SP402 = f"{SP4} - "
    # SP403 = f"{SP4} - "
    # SP404 = f"{SP4} - "
    # SP405 = f"{SP4} - "
    # SP406 = f"{SP4} - "
    # SP407 = f"{SP4} - "
    # SP408 = f"{SP4} - "
    # SP409 = f"{SP4} - "
    # SP410 = f"{SP4} - "
    # SP411 = f"{SP4} - "
    # SP412 = f"{SP4} - "
    # SP413 = f"{SP4} - "
    # SP414 = f"{SP4} - "
    # SP415 = f"{SP4} - "
    # SP416 = f"{SP4} - "
    # SP417 = f"{SP4} - "

    # 5-1: Downtown of Crag
    GN101 = f"{GN1} - Entrance"
    # GN102 = f"{GN1} - "
    # GN103 = f"{GN1} - "
    # GN104 = f"{GN1} - "
    # GN105 = f"{GN1} - "

    # 5-2: Pixls, Tablets and Crag
    GN201 = f"{GN2} - Entrance"
    # GN202 = f"{GN2} - "
    # GN203 = f"{GN2} - "
    # GN204 = f"{GN2} - "
    # GN205 = f"{GN2} - "
    # GN206 = f"{GN2} - "

    # 5-3: A Crag in the Dark
    GN301 = f"{GN3} - Entrance"
    # GN302 = f"{GN3} - "
    # GN303 = f"{GN3} - "
    # GN304 = f"{GN3} - "
    # GN305 = f"{GN3} - "
    # GN306 = f"{GN3} - "
    # GN307 = f"{GN3} - "
    # GN308 = f"{GN3} - "
    # GN309 = f"{GN3} - "
    # GN310 = f"{GN3} - "
    # GN311 = f"{GN3} - "
    # GN312 = f"{GN3} - "
    # GN313 = f"{GN3} - "
    # GN314 = f"{GN3} - "
    # GN315 = f"{GN3} - "
    # GN316 = f"{GN3} - "

    # 5-4: The Menace of King Croacus
    GN401 = f"{GN4} - Entrance"
    # GN402 = f"{GN4} - "
    # GN403 = f"{GN4} - "
    # GN404 = f"{GN4} - "
    # GN405 = f"{GN4} - "
    # GN406 = f"{GN4} - "
    # GN407 = f"{GN4} - "
    # GN408 = f"{GN4} - "
    # GN409 = f"{GN4} - "
    # GN410 = f"{GN4} - "
    # GN411 = f"{GN4} - "
    # GN412 = f"{GN4} - "
    # GN413 = f"{GN4} - "
    # GN414 = f"{GN4} - "
    # GN415 = f"{GN4} - "
    # GN416 = f"{GN4} - "
    # GN417 = f"{GN4} - "

    #
    WA101 = f"{WA1} - Entrance"
    # WA102 = f"{WA1} - Gate 1"
    # WA103 = f"{WA1} - Gate 2"
    # WA104 = f"{WA1} - Gate 3"
    # WA105 = f"{WA1} - Gate 4"
    # WA106 = f"{WA1} - Gate 5"
    # WA107 = f"{WA1} - Gate 6"
    # WA108 = f"{WA1} - Gate 7"
    # WA109 = f"{WA1} - Gate 8"
    # WA110 = f"{WA1} - Gate 9"
    # WA111 = f"{WA1} - Gate 10"
    # WA112 = f"{WA1} - Gate 11"
    # WA113 = f"{WA1} - Gate 12"
    # WA114 = f"{WA1} - Gate 13"
    # WA115 = f"{WA1} - Gate 14"
    # WA116 = f"{WA1} - Gate 15"
    # WA117 = f"{WA1} - Gate 16"
    # WA118 = f"{WA1} - Gate 17"
    # WA119 = f"{WA1} - Gate 18"
    # WA120 = f"{WA1} - Gate 19"
    # WA121 = f"{WA1} - Gate 20"
    # WA122 = f"{WA1} - Gate 21"
    # WA123 = f"{WA1} - Gate 22"
    # WA124 = f"{WA1} - Gate 23"
    # WA125 = f"{WA1} - Gate 24"
    # WA126 = f"{WA1} - Gate 25"
    # WA127 = f"{WA1} - World of Nothing"

    #
    WA201 = f"{WA2} - Gate 26"
    # WA202 = f"{WA2} - Gate 27"
    # WA203 = f"{WA2} - Gate 28"
    # WA204 = f"{WA2} - Gate 29"
    # WA205 = f"{WA2} - Gate 30"
    # WA206 = f"{WA2} - Gate 31"
    # WA207 = f"{WA2} - Gate 32"
    # WA208 = f"{WA2} - Gate 33"
    # WA209 = f"{WA2} - Gate 34"
    # WA210 = f"{WA2} - Gate 35"
    # WA211 = f"{WA2} - Gate 36"
    # WA212 = f"{WA2} - Gate 37"
    # WA213 = f"{WA2} - Gate 38"
    # WA214 = f"{WA2} - Gate 39"
    # WA215 = f"{WA2} - Gate 40"
    # WA216 = f"{WA2} - Gate 41"
    # WA217 = f"{WA2} - Gate 42"
    # WA218 = f"{WA2} - Gate 43"
    # WA219 = f"{WA2} - Gate 44"
    # WA220 = f"{WA2} - Gate 45"
    # WA221 = f"{WA2} - Gate 46"
    # WA222 = f"{WA2} - Gate 47"
    # WA223 = f"{WA2} - Gate 48"
    # WA224 = f"{WA2} - Gate 49"
    # WA225 = f"{WA2} - Gate 50"

    #
    WA301 = f"{WA3} - Gate 51"
    # WA302 = f"{WA3} - Gate 52"
    # WA303 = f"{WA3} - Gate 53"
    # WA304 = f"{WA3} - Gate 54"
    # WA305 = f"{WA3} - Gate 55"
    # WA306 = f"{WA3} - Gate 56"
    # WA307 = f"{WA3} - Gate 57"
    # WA308 = f"{WA3} - Gate 58"
    # WA309 = f"{WA3} - Gate 59"
    # WA310 = f"{WA3} - Gate 60"
    # WA311 = f"{WA3} - Gate 61"
    # WA312 = f"{WA3} - Gate 62"
    # WA313 = f"{WA3} - Gate 63"
    # WA314 = f"{WA3} - Gate 64"
    # WA315 = f"{WA3} - Gate 65"
    # WA316 = f"{WA3} - Gate 66"
    # WA317 = f"{WA3} - Gate 67"
    # WA318 = f"{WA3} - Gate 68"
    # WA319 = f"{WA3} - Gate 69"
    # WA320 = f"{WA3} - Gate 70"
    # WA321 = f"{WA3} - Gate 71"
    # WA322 = f"{WA3} - Gate 72"
    # WA323 = f"{WA3} - Gate 73"
    # WA324 = f"{WA3} - Gate 74"
    # WA325 = f"{WA3} - Gate 75"

    #
    WA401 = f"{WA4} - Gate 76"
    # WA402 = f"{WA4} - Gate 77"
    # WA403 = f"{WA4} - Gate 78"
    # WA404 = f"{WA4} - Gate 79"
    # WA405 = f"{WA4} - Gate 80"
    # WA406 = f"{WA4} - Gate 81"
    # WA407 = f"{WA4} - Gate 82"
    # WA408 = f"{WA4} - Gate 83"
    # WA409 = f"{WA4} - Gate 84"
    # WA410 = f"{WA4} - Gate 85"
    # WA411 = f"{WA4} - Gate 86"
    # WA412 = f"{WA4} - Gate 87"
    # WA413 = f"{WA4} - Gate 88"
    # WA414 = f"{WA4} - Gate 89"
    # WA415 = f"{WA4} - Gate 90"
    # WA416 = f"{WA4} - Gate 91"
    # WA417 = f"{WA4} - Gate 92"
    # WA418 = f"{WA4} - Gate 93"
    # WA419 = f"{WA4} - Gate 94"
    # WA420 = f"{WA4} - Gate 95"
    # WA421 = f"{WA4} - Gate 96"
    # WA422 = f"{WA4} - Gate 97"
    # WA423 = f"{WA4} - Gate 98"
    # WA424 = f"{WA4} - Gate 99"
    # WA425 = f"{WA4} - Gate 100"
    # WA426 = f"{WA4} - Sammer's Throne"  # King Sammer (Gives the 7 TTYD partner Catch Cards)

    # 7-1: Subterranean Vacation
    AN101 = f"{AN1} - Healing Fountain"
    # AN102 = f"{AN1} - Two Floors"
    # AN103 = f"{AN1} - River Twigg Surface"
    # AN104 = f"{AN1} - Iron Floor"
    # AN105 = f"{AN1} - Star Block"
    # AN106 = f"{AN1} - River Twigg Bottom"
    # AN107 = f"{AN1} - 3 Orange Spout"
    # AN108 = f"{AN1} - Pipes"
    # AN109 = f"{AN1} - Underground Blocks"
    # AN110 = f"{AN1} - Underground Blue Switch"
    # AN111 = f"{AN1} - Underground Gigabite"

    # 7-2: The Sealed Doors Three
    AN201 = f"{AN2} - Entrance"
    # AN202 = f"{AN2} - "
    # AN203 = f"{AN2} - "
    # AN204 = f"{AN2} - "
    # AN205 = f"{AN2} - "
    # AN206 = f"{AN2} - "
    # AN207 = f"{AN2} - "
    # AN208 = f"{AN2} - "
    # AN209 = f"{AN2} - "
    # AN210 = f"{AN2} - "

    # 7-3: The Forbidden Apple
    AN301 = f"{AN3} - Entrance"
    # AN302 = f"{AN3} - "
    # AN303 = f"{AN3} - "
    # AN304 = f"{AN3} - "
    # AN305 = f"{AN3} - "
    # AN306 = f"{AN3} - "
    # AN307 = f"{AN3} - "
    # AN308 = f"{AN3} - "
    # AN309 = f"{AN3} - "
    # AN310 = f"{AN3} - "
    # AN311 = f"{AN3} - "
    # AN312 = f"{AN3} - "
    # AN313 = f"{AN3} - "
    # AN314 = f"{AN3} - "
    # AN315 = f"{AN3} - "
    # AN316 = f"{AN3} - "

    # 7-4: A Bone-Chilling Tale
    AN401 = f"{AN4} - Entrance"
    # AN402 = f"{AN4} - "
    # AN403 = f"{AN4} - "
    # AN404 = f"{AN4} - "
    # AN405 = f"{AN4} - "
    # AN406 = f"{AN4} - "
    # AN407 = f"{AN4} - "
    # AN408 = f"{AN4} - "
    # AN409 = f"{AN4} - "
    # AN410 = f"{AN4} - "
    # AN411 = f"{AN4} - "
    # AN412 = f"{AN4} - "

    # 8-1: The Impending Darkness
    LS101 = f"{LS1} - Entrance"
    # LS102 = f"{LS1} - "
    # LS103 = f"{LS1} - "
    # LS104 = f"{LS1} - "
    # LS105 = f"{LS1} - "
    # LS106 = f"{LS1} - "
    # LS107 = f"{LS1} - "
    # LS108 = f"{LS1} - "
    # LS109 = f"{LS1} - "
    # LS110 = f"{LS1} - "
    # LS111 = f"{LS1} - "
    # LS112 = f"{LS1} - "

    # 8-2: The Crash
    LS201 = f"{LS2} - Entrance"
    # LS202 = f"{LS2} - "
    # LS203 = f"{LS2} - "
    # LS204 = f"{LS2} - "
    # LS205 = f"{LS2} - "
    # LS206 = f"{LS2} - "
    # LS207 = f"{LS2} - "
    # LS208 = f"{LS2} - "
    # LS209 = f"{LS2} - "
    # LS210 = f"{LS2} - "
    # LS211 = f"{LS2} - "
    # LS212 = f"{LS2} - "
    # LS213 = f"{LS2} - "
    # LS214 = f"{LS2} - "
    # LS215 = f"{LS2} - "
    # LS216 = f"{LS2} - "
    # LS217 = f"{LS2} - "
    # LS218 = f"{LS2} - "

    # 8-3: Countdown to Destruction
    LS301 = f"{LS3} - Entrance"
    # LS302 = f"{LS3} - "
    # LS303 = f"{LS3} - "
    # LS304 = f"{LS3} - "
    # LS305 = f"{LS3} - "
    # LS306 = f"{LS3} - "
    # LS307 = f"{LS3} - "
    # LS308 = f"{LS3} - "
    # LS309 = f"{LS3} - "
    # LS310 = f"{LS3} - "
    # LS311 = f"{LS3} - "
    # LS312 = f"{LS3} - "
    # LS313 = f"{LS3} - "

    # 8-4: Tippi and Count Bleck
    LS401 = f"{LS4} - Entrance"
    # LS402 = f"{LS4} - "
    # LS403 = f"{LS4} - "
    # LS404 = f"{LS4} - "
    # LS405 = f"{LS4} - "
    # LS406 = f"{LS4} - "
    # LS407 = f"{LS4} - Labyrinth 1"
    # LS408 = f"{LS4} - Labyrinth 2"
    # LS409 = f"{LS4} - Labyrinth 3"
    # LS410 = f"{LS4} - Final Staircase"
    # LS411 = f"{LS4} - Final Fight"  # This room changes into many different forms based off sequence
    # LS412 = f"{LS4} - "
    # LS413 = f"{LS4} - "

    # Cutscenes / Menus
    # AA101 = "Outside Mario's House"
    # AA102 = "Inside Mario's House"
    # AA201 = "Outside Bowser's Castle"
    # AA202 = "Inside Bowser's Castle"
    # AA301 = "Credits screen with Blumiere & Timpani"
    # AA401 = "Main Menu"

    # BOS_01 - Boss Area (Chapter 3 Dimentio)

    # DOS_01 - Test Arena?

    # Pit Rooms?
    # DAN_11
    # DAN_12
    # DAN_13
    # DAN_14


class SPMEntrance:
    """The namespace of all entrances into rooms.
    The variable name is the name from spm_practice_codes, which is how you *enter* the room.
    The value is named based off how you *exit* the room.
    The part before the first _ is the room name and number
    The part after the first _ is the entrance name from spm_practice_codes

    - DEFAULT: Room origin?
    - FALL: Fall into, One-Way entrances
    - ELV: Elevator
    - PURE_HEART_RET: Unknown
    - DOKAN: Pipe
    - AODOKAN: Blue Pipe (Constructed by Welderburg)
    - JUMP: Jump into

    # Custom Entrances for logic separation have a `L_` after the first `_`
    - L_WALL: Cross a wall, usually by bombing it
    - L_BRIDGE: Cross a bridge, usually by flipping with Mario
    - L_FLEEP: Use Fleep
    """
    # region Flipside Entrances
    # MAC01_DEFAULT  # Flipside 3F
    MAC01_DOKAN_1 = "Flipside 3F - Layer 2 - Pipe"  # MAC02_DOKAN_1
    MAC01_ELV1 = "Flipside 3F - Layer 1 - Elevator Down"  # MAC02_ELV2
    # MAC01_PURE_HEART_RET
    # MAC01_FALL_1 = "Flipside 3F - Layer 1 - Jump Up"  # There's not an exit for this so might need a spring

    # MAC02_DEFAULT  # Flipside 2F / Tower
    MAC02_DOKAN_1 = "Flipside 2F - Layer 2 - Pipe"  # MAC01_DOKAN_1
    MAC02_DOKAN_2 = "Flipside 2F Outskirts - Layer 3 - Pipe"  # MAC06_DOKAN_1
    # MAC02_DOKAN_3 = "Flipside Tower - Return Pipe"
    MAC02_AODOKAN_1 = "Flipside 2F - Layer 1 - Left Blue Pipe"  # MAC05_AODOKAN_1
    MAC02_AODOKAN_2 = "Flipside 2F - Layer 1 - Right Blue Pipe"  # MAC12_AODOKAN_1
    MAC02_DOA6_I_1 = "Flipside Tower - Red Door (1-1)"
    MAC02_DOA6_I_2 = "Flipside Tower - Red Door (1-2)"
    MAC02_DOA6_I_3 = "Flipside Tower - Red Door (1-3)"
    MAC02_DOA6_I_4 = "Flipside Tower - Red Door (1-4)"
    # yeah no DOA7 ig
    MAC02_DOA8_I_1 = "Flipside Tower - Orange Door (2-1)"
    MAC02_DOA8_I_2 = "Flipside Tower - Orange Door (2-2)"
    MAC02_DOA8_I_3 = "Flipside Tower - Orange Door (2-3)"
    MAC02_DOA8_I_4 = "Flipside Tower - Orange Door (2-4)"
    MAC02_DOA9_I_1 = "Flipside Tower - Yellow Door (3-1)"
    MAC02_DOA9_I_2 = "Flipside Tower - Yellow Door (3-2)"
    MAC02_DOA9_I_3 = "Flipside Tower - Yellow Door (3-3)"
    MAC02_DOA9_I_4 = "Flipside Tower - Yellow Door (3-4)"
    MAC02_DOA10_I_1 = "Flipside Tower - Green Door (4-1)"
    MAC02_DOA10_I_2 = "Flipside Tower - Green Door (4-2)"
    MAC02_DOA10_I_3 = "Flipside Tower - Green Door (4-3)"
    MAC02_DOA10_I_4 = "Flipside Tower - Green Door (4-4)"
    MAC02_DOA11_I_1 = "Flipside Tower - Cyan Door (5-1)"
    MAC02_DOA11_I_2 = "Flipside Tower - Cyan Door (5-2)"
    MAC02_DOA11_I_3 = "Flipside Tower - Cyan Door (5-3)"
    MAC02_DOA11_I_4 = "Flipside Tower - Cyan Door (5-4)"
    MAC02_DOA12_I_1 = "Flipside Tower - Blue Door (6-1)"
    MAC02_DOA12_I_2 = "Flipside Tower - Blue Door (6-2)"
    MAC02_DOA12_I_3 = "Flipside Tower - Blue Door (6-3)"
    MAC02_DOA12_I_4 = "Flipside Tower - Blue Door (6-4)"
    MAC02_DOA13_I_1 = "Flipside Tower - Purple Door (7-1)"
    MAC02_DOA13_I_2 = "Flipside Tower - Purple Door (7-2)"
    MAC02_DOA13_I_3 = "Flipside Tower - Purple Door (7-3)"
    MAC02_DOA13_I_4 = "Flipside Tower - Purple Door (7-4)"
    MAC02_ELV1 = "Flipside 2F - Layer 1 - Elevator Down"  # MAC_09_ELV1
    MAC02_ELV2 = "Flipside 2F - Layer 1 - Elevator Up"  # MAC01_ELV1
    # MAC02_DEARU_IE  # Spawns at tower bottom in front of elevator, doesn't use elevator
    # MAC02_PURE_HEART_RET
    # MAC02_PURE_HEART  # Cutscene purposes only? Shows a door as if the door is opening or heart is being filled in
    MAC02_L_3D_1_2 = "Flipside 2F - Layer 1 -> 2"
    MAC02_L_3D_2_1 = "Flipside 2F - Layer 2 -> 1"
    MAC02_L_3D_2_3 = "Flipside 2F - Layer 2 -> 3"
    MAC02_L_3D_3_2 = "Flipside 2F - Layer 3 -> 2"
    MAC02_L_FALL = "Flipside Tower - Fall"
    MAC02_L_TOWER_ELV1 = "Flipside Tower - Elevator Down"
    MAC02_L_TOWER_ELV2 = "Flipside Tower - Elevator Up"

    # MAC03_DEFAULT  # Flipside/Flopside Mirror Hall
    MAC03_DOA6_R = "Flipside 1F - Mirror Hall - Right Door"  # MAC09_DOA6_I
    MAC03_DOA16_R = "Flopside 1F - Mirror Hall - Left Door"  # MAC19_DOA16_R
    MAC03_L_3D_2_1 = "Flipside 1F - Mirror Hall - Layer 2 -> 1"
    MAC03_L_3D_1_2 = "Flipside 1F - Mirror Hall - Layer 1 -> 2"

    # MAC04_DEFAULT  # Flipside B1
    MAC04_DOKAN = "Flipside B1 - Bar Pipe"  # MAC30_DOKAN
    MAC04_ELV1 = "Flipside B1 - Elevator Up"  # MAC09_ELV2
    MAC04_ELV2 = "Flipside B1 - Elevator Down"  # MAC05_ELV1
    MAC04_L_SHRINK = "Flipside B1 - Shrink to Itty Bits"

    # MAC05_DEFAULT  # Flipside B2 Outskirts
    MAC05_DOKAN_1 = "Flipside B2 Outskirts - Layer 1 - Sealed Pipe"  # Flipside Pit of 100 Trials
    MAC05_DOKAN_2 = "Flipside B2 Outskirts - Layer 2 - Pipe"  # MAC07_DOKAN_1
    MAC05_AODOKAN_1 = "Flipside B2 Outskirts - Layer 1 - Blue Pipe"  # MAC02_AODOKAN_1
    MAC05_ELV1 = "Flipside B2 Outskirts - Layer 1 - Elevator Up"  # MAC04_ELV2
    MAC05_L_3D_2_1 = "Flipside B2 Outskirts - Layer 2 -> 1"
    MAC05_L_3D_1_2 = "Flipside B2 Outskirts - Layer 1 -> 2"

    # MAC06_DEFAULT  # Flipside 1F Outskirts
    MAC06_DOKAN_1 = "Flipside 1F Outskirts - Layer 1 - Right Pipe"  # MAC02_DOKAN_2
    MAC06_DOKAN_2 = "Flipside 1F Outskirts - Layer 1 - Left Pipe"  # MAC07_DOKAN_2
    # MAC06_PURE_HEART_RET
    MAC06_JUMP = "Flipside 1F Outskirts - Layer 1 - Chasm Fall"  # MAC08_DEFAULT
    MAC06_L_3D_1_2 = "Flipside 1F Outskirts - Layer 1 -> 2"
    MAC06_L_3D_2_1 = "Flipside 1F Outskirts - Layer 2 -> 1"

    # MAC07_DEFAULT  # Flipside B1 Outskirts
    MAC07_DOKAN_1 = "Flipside B1 Outskirts - Layer 1 - Right Pipe"  # MAC05_DOKAN_2
    MAC07_DOKAN_2 = "Flipside B1 Outskirts - Layer 1 - Left Pipe"  # MAC06_DOKAN_2
    MAC07_L_3D_2_1 = "Flipside B1 Outskirts - Layer 2 -> 1"
    MAC07_L_3D_1_2 = "Flipside B1 Outskirts - Layer 1 -> 2"

    MAC08_DEFAULT = "Flipside 1F - Jump Out"  # MAC06_JUMP

    # MAC09_DEFAULT  # Flipside 1F
    MAC09_DOA6_I = "Flipside 1F - Door"  # MAC03_DOA6_R
    MAC09_ELV1 = "Flipside 1F - Elevator Up"  # MAC02_ELV1
    MAC09_ELV2 = "Flipside 1F - Elevator Down"  # MAC04_ELV1
    MAC09_L_3D_1_2 = "Flipside 1F - Layer 1 -> 2"
    MAC09_L_3D_2_1 = "Flipside 1F - Layer 2 -> 1"
    MAC09_L_3D_2_3 = "Flipside 1F - Layer 2 -> 3"
    MAC09_L_3D_3_2 = "Flipside 1F - Layer 3 -> 2"
    # endregion

    # region Flopside Entrances
    # MAC11_DEFAULT  # Flopside 3F
    MAC11_DOKAN_1 = "Flopside 3F - Layer 2 - Right Pipe"  # MAC12_DOKAN_1
    MAC11_ELV1 = "Flopside 3F - Layer 1 - Elevator Down"  # MAC12_ELV1
    # MAC11_PURE_HEART_RET
    MAC11_FALL_1 = "Flopside 3F - Layer 1 - Fall Into"  # There's not an exit for this so might need a spring

    # MAC12_DEFAULT  # Flopside 2F
    MAC12_DOKAN_1 = "Flopside 2F - Layer 2 - Pipe"  # MAC11_DOKAN_1
    MAC12_DOKAN_2 = "Flopside 2F - Layer 3 - Blocked Pipe"  # MAC17_DOKAN_1
    MAC12_AODOKAN_1 = "Flopside 2F - Layer 1 - Left Blue Pipe"  # MAC02_AODOKAN_2
    MAC12_AODOKAN_2 = "Flopside 2F - Layer 1 - Right Blue Pipe"  # MAC15_AODOKAN_1
    # MAC12_DOKAN_6 = "Flopside Tower - Return Pipe"
    MAC12_DOA6_I_1 = "Flopside Tower - Black Door 1"  # Chapter 8-1
    MAC12_DOA6_I_2 = "Flopside Tower - Black Door 2"  # Chapter 8-2
    MAC12_DOA6_I_3 = "Flopside Tower - Black Door 3"  # Chapter 8-3
    MAC12_DOA6_I_4 = "Flopside Tower - Black Door 4"  # Chapter 8-4
    MAC12_ELV1 = "Flopside 2F - Layer 1 - Elevator Up"  # MAC11_ELV1
    MAC12_ELV2 = "Flopside 2F - Layer 1 - Elevator Down"  # MAC19_ELV1
    # MAC12_PURE_HEART_RET
    # MAC12_WORLD_END  # Cutscene
    MAC12_L_FALL = "Flopside Tower - Fall"
    MAC12_L_TOWER_ELV1 = "Flopside Tower - Elevator Down"
    MAC12_L_TOWER_ELV2 = "Flopside Tower - Elevator Up"
    MAC12_L_3D_1_2 = "Flopside 2F - Layer 1 -> 2"
    MAC12_L_3D_2_1 = "Flopside 2F - Layer 2 -> 1"
    MAC12_L_3D_2_3 = "Flopside 2F - Layer 2 -> 3"
    MAC12_L_3D_3_2 = "Flopside 2F - Layer 3 -> 2"

    # MAC14_DEFAULT  # Flopside B1
    MAC14_ELV1 = "Flopside B1 - Elevator Down"  # MAC15_ELV1
    MAC14_ELV2 = "Flopside B1 - Elevator Up"  # MAC19_ELV2
    MAC14_L_FLIP_R = "Flopside B1 - Left -> Right"
    MAC14_L_FLIP_L = "Flopside B1 - Right -> Left"
    MAC14_L_SHRINK = "Flopside B1 - Itty Bits"
    MAC14_L_FLIP_B = "Flopside B1 - Beveragarium"

    # MAC15_DEFAULT  # Flopside B2
    MAC15_DOKAN_1 = "Flopside B2 - Layer 1 - Sealed Pipe"  # Flopside Pit of 100 Trials
    MAC15_DOKAN_2 = "Flopside B2 - Layer 2 - Pipe"  # MAC17_DOKAN_2
    MAC15_AODOKAN_1 = "Flopside B2 - Layer 2 - Blue Pipe"  # MAC12_AODOKAN_2
    MAC15_ELV1 = "Flopside B2 - Layer 1 - Elevator Up"  # MAC14_ELV1
    MAC15_JUMP = "Flopside B2 - Layer 2 - Chasm Fall"  # MAC18_DEFAULT
    MAC15_L_3D_1_2 = "Flopside B2 - Layer 1 -> 2"
    MAC15_L_3D_2_1 = "Flopside B2 - Layer 2 -> 1"

    # MAC16_DEFAULT  # Flopside 1F Outskirts
    MAC16_DOKAN_1 = "Flopside 1F Outskirts - Layer 1 - Left Blocked Pipe"  # MAC12_DOKAN_2
    MAC16_DOKAN_2 = "Flopside 1F Outskirts - Layer 1 - Right Pipe"  # MAC15_DOKAN_2
    MAC16_L_3D_1_2 = "Flopside 1F Outskirts - Layer 1 -> 2"
    MAC16_L_3D_2_1 = "Flopside 1F Outskirts - Layer 2 -> 1"

    # MAC17_DEFAULT  # Flopside B1 Outskirts
    MAC17_DOKAN1 = "Flopside B1 Outskirts - Left Pipe"
    MAC17_DOKAN2 = "Flopside B1 Outskirts - Right Pipe"

    MAC18_DEFAULT = "Flopside B2 - Jump Out"  # MAC15_JUMP

    # MAC19_DEFAULT  # Flopside 1F
    MAC19_DOA16_R = "Flopside 1F - Layer 1 - Door"  # MAC03_DOA16_R
    MAC19_ELV1 = "Flopside 1F - Layer 3 - Elevator Up"  # MAC12_ELV2
    MAC19_ELV2 = "Flopside 1F - Layer 3 - Elevator Down"  # MAC14_ELV2
    MAC19_L_3D_1_2 = "Flopside 1F - Layer 1 -> 2"
    MAC19_L_3D_2_1 = "Flopside 1F - Layer 2 -> 1"
    MAC19_L_3D_2_3 = "Flopside 1F - Layer 2 -> 3"
    MAC19_L_3D_3_2 = "Flopside 1F - Layer 3 -> 2"

    # MAC22_DEFAULT  # Flipside Tower Scene
    # MAC22_EPI_00  # Flipside Tower Postgame Cutscene

    # MAC30_DEFAULT  # Arcade
    MAC30_DOKAN = "Arcade - Pipe"  # MAC04_DOKAN
    # MAC30_END  # Arcade Menu
    # endregion

    # region Chapter 1 Entrances
    # HE101_DEFAULT  # Lineland Road
    HE101_IE_DOA_02 = f"{SPMRegion.HE101} - Bestovius' House, Hidden Door"  # HE106_IE_DOA
    HE101_DOKAN_2 = f"{SPMRegion.HE101} - Front Pipe near Bestovius' House"  # HE103_DOKAN_1
    HE101_DOKAN_3 = f"{SPMRegion.HE101} - Back Pipe near Bestovius' House"  # N/A - Not Enterable
    HE101_DOA1_L = f"{SPMRegion.HE101} - Chapter Door"  # N/A - Not Enterable
    HE101_DOA2_L = f"{SPMRegion.HE101} - Sealed Door"  # HE102_DOA1_L

    # HE102_DOKAN_M  # Pipe under screen?
    HE102_DOA1_L = f"{SPMRegion.HE102} - Left Door"  # HE101_DOA2_L
    HE102_DOA2_L = f"{SPMRegion.HE102} - Right Door"  # HE104_DOA1_L

    # HE103_DEFAULT = "Lineland Road Underground"
    HE103_DOKAN_1 = f"{SPMRegion.HE103} - Top Pipe"  # N/A - Not Enterable
    HE103_DOKAN_2 = f"{SPMRegion.HE103} - Right Pipe"  # HE101_DOKAN_3

    # HE104_DEFAULT = "Lineland Road 3"
    HE104_DOA1_L = f"{SPMRegion.HE104} - Left Door"  # HE102_DOA2_L
    HE104_DOA2_L = f"{SPMRegion.HE104} - Right Door"  # HE105_DOA1_L

    # HE105_DEFAULT = "Lineland Road 4"
    HE105_DOA1_L = f"{SPMRegion.HE105} - Left Door"  # HE104_DOA2_L

    # HE106_DEFAULT = "Lineland Road - Bestovius' Room"
    HE106_IE_DOA = f"{SPMRegion.HE106} - Door"  # HE101_IE_DOA_02

    # Mount Lineland (1-2)
    # HE201_DEFAULT = f"{SPMRegion.HE201} - Chapter start"
    # HE201_DOKAN_M = f"{SPMRegion.HE101} - Pipe"
    HE201_DOA1_I = f"{SPMRegion.HE201} - Right Door"  # HE202_DOA1_I
    HE201_DOA2_I = f"{SPMRegion.HE201} - Hidden Shortcut Door"  # HE201_DOA2_I
    # HE201_  # Yeah there's no name for this entrance, it's the same as default ig

    # HE202_DEFAULT
    HE202_DOA1_I = f"{SPMRegion.HE202} - Left Door"  # HE201_DOA1_I
    HE202_DOA2_I = f"{SPMRegion.HE202} - Floating Door"  # N/A Not Enterable
    HE202_DOA3_I = f"{SPMRegion.HE202} - Right Door"  # HE203_DOA1_I

    # HE203_DEFAULT
    HE203_DOKAN_1 = f"{SPMRegion.HE203} - Pipe before Red's bridge"  # HE203_H_DOKAN_1
    HE203_DOKAN_2 = f"{SPMRegion.HE203} - Pipe behind bricks"  # HE208_DOKAN_1
    HE203_DOKAN_3 = f"{SPMRegion.HE203} - Pipe in house behind partition"  # HE206_DOKAN_1
    HE203_DOKAN_4 = f"{SPMRegion.HE203} - Pipe before Green's bridge"  # HE203_H_DOKAN_4
    HE203_H_DOKAN_1 = f"{SPMRegion.HE203} - Left Background Pipe"  # HE203_DOKAN_1
    HE203_H_DOKAN_4 = f"{SPMRegion.HE203} - Right Background Pipe"  # HE203_DOKAN_4
    HE203_DOA1_I = f"{SPMRegion.HE203} - Left Door"  # HE202_DOA3_I
    # HE203_WORLD_END  # Cutscene
    HE203_BG_IE1_IRIGUCHI = f"{SPMRegion.HE203} - Red's House"  # HE204_DEFAULT
    HE203_BG_IE2_IRIGUCHI = f"{SPMRegion.HE203} - Green's House"  # HE205_DEFAULT
    # HE203_NG_LEFT = f"{SPMRegion.HE203} - Kicked out of Red's House"
    # HE203_OK_LEFT  # Cutscene, red's bridge is built
    # HE203_NG_RIGHT = f"{SPMRegion.HE203} - Kicked out of Green's House"
    # HE203_OK_RIGHT  # Cutscene, green's bridge is built

    HE204_DEFAULT = f"{SPMRegion.HE204} - Door"  # HE203_BG_IE1_IRIGUCHI
    # HE204_OK  # Cutscene, return from bridge built

    HE205_DEFAULT = f"{SPMRegion.HE205} - Door"  # HE203_BG_IE2_IRIGUCHI
    # HE205_OK  # Cutscene, return from bridge built

    # HE206_DEFAULT
    HE206_DOKAN_1 = f"{SPMRegion.HE206} - Left Pipe"  # HE203_DOKAN_3
    HE206_DOA1_I = f"{SPMRegion.HE206} - Right Door"  # HE209_DOA1_I

    HE207_DOA1_I = f"{SPMRegion.HE207} - Door"  # HE209_DOA2_I

    HE208_DOKAN_1 = f"{SPMRegion.HE208} - Door"  # HE203_DOKAN_2

    HE209_DOA1_I = f"{SPMRegion.HE209} - Left Door"  # HE206_DOA1_I
    HE209_DOA2_I = f"{SPMRegion.HE209} - Right Door"  # HE207_DOA1_I

    # HE301_DEFAULT
    # HE301_DOKAN_M
    HE301_DOA1_I = f"{SPMRegion.HE301} - Door below red palm tree"  # HE303_DOA1_I
    HE301_DOA2_I = f"{SPMRegion.HE301} - Right door"  # HE302_DOA1_I
    # HE301_  # another entrance without a name

    # HE302_DEFAULT
    HE302_DOA1_I = f"{SPMRegion.HE302} - Left Door"  # HE301_DOA2_I

    # HE303_DEFAULT
    HE303_DOKAN_1 = f"{SPMRegion.HE303} - Pipe on floating bricks"  # HE305_DOKAN_1
    # HE303_DOKAN_M
    HE303_DOA1_I = f"{SPMRegion.HE303} - Left Door"  # HE301_DOA1_I
    HE303_DOA2_I = f"{SPMRegion.HE303} - Right Door"  # HE304_DOA1_I

    # HE304_DEFAULT
    HE304_DOA1_I = f"{SPMRegion.HE304} - Left Door"  # HE303_DOA2_I
    HE304_DOA2_I = f"{SPMRegion.HE304} - Right Door"  # HE306_DOA2_I

    # HE305_DEFAULT
    HE305_DOKAN_1 = f"{SPMRegion.HE305} - Pipe"  # HE303_DOKAN_1

    # HE306_DEFAULT
    HE306_DOA1_I = f"{SPMRegion.HE306} - Left door on floating bricks"  # HE307_DOA1_I
    HE306_DOA2_I = f"{SPMRegion.HE306} - Door on ground"  # HE304_DOA2_I
    HE306_DOA3_I = f"{SPMRegion.HE306} - Right door on floating bricks"  # HE308_DOA1_I

    # HE307_DEFAULT
    HE307_DOA1_I = f"{SPMRegion.HE307} - Door"  # HE306_DOA1_I

    # HE308_DEFAULT
    HE308_DOA1_I = f"{SPMRegion.HE308} - Door"  # HE306_DOA3_I

    # HE401_DEFAULT
    # HE401_DOKAN_M
    HE401_DOA1_I = f"{SPMRegion.HE401} - Door"  # HE402_DOA1_I
    # HE401_  # another entrance without a name

    # HE402_DEFAULT
    HE402_DOA1_I = f"{SPMRegion.HE402} - Left Door"  # HE401_DOA1_I
    HE402_DOA2_I = f"{SPMRegion.HE402} - Right Door"  # HE403_DOA1_I

    # HE403_DEFAULT
    HE403_DOA1_I = f"{SPMRegion.HE403} - Left Door"  # HE402_DOA2_I
    HE403_DOA2_I = f"{SPMRegion.HE403} - Middle Door"  # HE405_DOA1_I
    HE403_DOA3_I = f"{SPMRegion.HE403} - Right Door"  # HE404_DOA1_I

    # HE404_DEFAULT
    HE404_DOA1_I = f"{SPMRegion.HE404} - Door"  # HE403_DOA3_I

    # HE405_DEFAULT
    HE405_DOA1_I = f"{SPMRegion.HE405} - Left Door"  # HE403_DOA2_I
    HE405_DOA2_I = f"{SPMRegion.HE405} - Right Upper Door"  # HE406_DOA1_I
    HE405_DOA3_I = f"{SPMRegion.HE405} - Right Lower Door"  # HE412_DOA1_I

    # HE406_DEFAULT
    HE406_DOA1_I = f"{SPMRegion.HE406} - Door"  # HE405_DOA2_I

    # HE407_DEFAULT
    HE407_DOA1_I = f"{SPMRegion.HE407} - Left Door"  # HE412_DOA2_I
    HE407_DOA2_I = f"{SPMRegion.HE407} - Right Door"  # HE408_DOA1_I

    # HE408_DEFAULT
    # HE408_DOKAN_M
    HE408_DOA1_I = f"{SPMRegion.HE408} - Lower Door"  # HE407_DOA2_I
    HE408_DOA2_I = f"{SPMRegion.HE408} - Upper Door"  # HE409_DOA1_I

    # HE409_DEFAULT
    HE409_DOKAN_1 = f"{SPMRegion.HE409} - Pipe"  # HE410_DOKAN_1
    HE409_DOA1_I = f"{SPMRegion.HE409} - Door"  # HE408_DOA2_I

    # HE410_DEFAULT
    HE410_DOKAN_1 = f"{SPMRegion.HE410} - Pipe"  # HE409_DOKAN_1
    HE410_DOA1_I = f"{SPMRegion.HE410} - Door"  # HE411_DOA1_I

    # HE411_DEFAULT
    HE411_DOA1_I = f"{SPMRegion.HE411} - Door"  # HE410_DOA1_I

    # HE412_DEFAULT
    HE412_DOA1_I = f"{SPMRegion.HE412} - Left Door"  # HE405_DOA3_I
    HE412_DOA2_I = f"{SPMRegion.HE412} - Right Door"  # HE407_DOA1_I
    # endregion

    # region Chapter 2

    # endregion


ALL_ENTRANCES = sorted({value for name, value in SPMEntrance.__dict__.items() if not name.startswith("__")})
ALL_EVENTS = sorted({value for name, value in SPMEvent.__dict__.items() if not name.startswith("__")})
ALL_ITEMS = sorted({value for name, value in SPMItem.__dict__.items() if not name.startswith("__")})
ALL_LOCATIONS = sorted({value for name, value in SPMLocation.__dict__.items() if not name.startswith("__")})
ALL_REGIONS = sorted({value for name, value in SPMRegion.__dict__.items() if not name.startswith("__")})
