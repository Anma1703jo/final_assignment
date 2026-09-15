from game import Game
from flow import Scene1, Scene2, Scene3, Scene4

#that's the file that runs for playing the game

game = Game()

while game.running:
    #show the main menu and stuff
    game.curr_menu.display_menu()

    while game.playing:
        scene1 = Scene1(game)
        scene1.run()

        scene2 = Scene2(game)
        scene2.run()

        scene3 = Scene3(game, path=scene2.chosen_path)
        scene3.run()

        scene4 = Scene4(game, path=scene3.chosen_path)
        scene4.run()

        if scene4.chosen_ending == "ending_2":
            game.playing = False

#this while loop is the time loop mechanic basically, so only if "ending_2" was chosen, the game playing ends