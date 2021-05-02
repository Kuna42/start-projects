import random

#User mit der Application vertraut machen

print("Das hier ist ein Zufallsgenerator-Würfel-Programm.\n\n"
      "Das Programm bietet ihnen die Möglichkeit im folgenden "
      "festzulegen wie viele Würfelseiten ihr Würfel haben soll.\n"
      "Anschließend dürfen sie dann raten auf welche Würfelseite der Würfel gefallen ist.\n"
      "Sie erhalten als/ein kleinen Tipp ob ihre Zahl zu hoch oder zu niedrig ist.\n\n"
      "Im Prinzip Würfeln sie selbst und bestimmen auch wie hoch die Anzahl der Würfelseiten sein soll. \n")

#Den Benutzer auffordern die Zahl einzugeben

print("Bitte geben sie ein wie viel Würfelseiten ihr Würfel haben soll: ")

WS = int(input())

if WS < 6:
    print("Der Würfel sollte mindestens 6 seiten besitzen. \n\n"
          "Versuchen sie es erneut. ")


if WS > 5:

    random_number = random.randint(1, WS)

    guess_count = 0

    while True:
        # getting user input

        user_guessed_number = int(input("Bitte raten sie das richtige Würfelauge: "))

        # checking for the equality
        if user_guessed_number == random_number:
            print(f"Sie haben den gesuchten Wert in {guess_count} versuchen erraten.")
            # breaking the loop
            break
        elif user_guessed_number < random_number:
            print("Ihre Nummer entspricht nicht dem Würfelauge. (Sie ist zu niedrig)")
        elif user_guessed_number > random_number:
            print("Ihre Nummer entspricht nicht dem Würfelauge. (Sie ist zu hoch)")
