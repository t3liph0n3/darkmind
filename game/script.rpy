# The script of the game goes in this file.

# Declare characters used by this game. The color argument colorizes the
# name of the character.

define e = Character("Eileen")


# The game starts here.

label start:
    python:

        def siloRun (rig, silo):
            for x in silo:
                appC  = appCho(rig)
                proBat(silo[x],appC)

        def appCho (rig):
            for x in rig:
                "[rig[x]], is a choice"
                return rig[x]



    # Show a background. This uses a placeholder by default, but you can
    # add a file (named either "bg room.png" or "bg room.jpg") to the
    # images directory to show it.

    scene bg room

    # This shows a character sprite. A placeholder is used, but you can
    # replace it by adding a file named "eileen happy.png" to the images
    # directory.

    show eileen happy

    # These display lines of dialogue.

    e "You've created a new Ren'Py game."

    call proBat([1,0,1,1,0],[1,0,1,0,1])

    e "Once you add a story, pictures, and music, you can release it to the world!"


    # This ends the game.
label death:
    "You died"

    return

label proBat(proL, appL):
    "you are here"
    python:
        for x in proL:
            print "[x] is x"
            if proL[x] > appL[x]:
                Jump(death)
        print "Success"
        Return
