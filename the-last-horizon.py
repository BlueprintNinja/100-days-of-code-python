print(r'''
      _____________________________________________________
     |    _____ _            _                _            |
     |   |_   _| |__   ___  | |    __ _  ___ | |_          |
     |     | | | '_ \ / _ \ | |   / _` |/ __|| __|         |
     |     | | | | | |  __/ | |__| (_| |\__ \| |_          |
     |     |_| |_| |_|\___| |_____\__,_||___/ \__|         |
     |                                                     |
     |    _   _            _                       _       |
     |   | | | | ___  _ __(_)_______  _ __        (_)      |
     |   | |_| |/ _ \| '__| |_  / _ \| '_ \       | |      |
     |   |  _  | (_) | |  | |/ / (_) | | | |      | |      |
     |   |_| |_|\___/|_|  |_/___\___/|_| |_|      |_|      |
     |_____________________________________________________|
''')

print("Welcome to The Last Horizon.")
print("Your mission is to reach the Eternal Vault before the tide consumes the land.")

# Step 1: The Fork in the Path
choice1 = input('The path splits at the edge of a jagged cliff. '
                'To the "left" lies a dark forest; to the "right" is a steep drop. '
                'Where do you go? ').lower()

if choice1 == "left":
    # Step 2: The Silent Bay
    choice2 = input('You emerge at the Silent Bay. The water is unnaturally still. '
                    'A lone lighthouse flickers on a distant rock. '
                    'Do you "wait" for the tide to turn, or "swim" into the mist? ').lower()

    if choice2 == "wait":
        # Step 3: The Vault of Echoes
        choice3 = input("The tide recedes, revealing a stone walkway to the lighthouse. "
                        "Inside, three spectral portals glow with ancient light. "
                        "Which do you enter? 'Crimson', 'Gold', or 'Azure'? ").lower()

        if choice3 == "crimson":
            print("The portal leads to the heart of a dying star. You are incinerated instantly. Game Over.")
        elif choice3 == "gold":
            print("The vault opens! You have secured the artifacts of the ancients. You Win!")
        elif choice3 == "azure":
            print("You step into a void where time does not exist. You are lost forever. Game Over.")
        else:
            print("The portals flicker and vanish, leaving you in total darkness. Game Over.")
    else:
        print("The water is colder than death. The shadows beneath the surface pull you down. Game Over.")

else:
    print("You stepped too close to the edge. The ground crumbles beneath your feet. Game Over.")
