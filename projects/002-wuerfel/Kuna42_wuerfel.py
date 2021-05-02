# Hier könnte ein Beispielcode stehen

from random import randint


class Wurfel:
    def __init__(self, seiten: int):
        # diese Variable speichert ab,
        # wie viele Seiten der Würfel hat
        self.seiten = seiten

    def __int__(self):
        return self.werfen()

    def werfen(self):
        # hier wird eine zufällige Zahl
        # zwischen 1 und der Höchsten Zahl
        # des Würfels ausgegeben.
        return randint(1, self.seiten)


if __name__ == "__main__":
    print("Dieses Programm simuliert einen Würfel und "
          "gibt die Augenzahl des Wurfes aus.\n Wenn sie "
          "einen neuen Wurf haben möchten tippen sie nur "
          "ihre [Enter]-Taste, wenn sie das spiel verlassen "
          "wollen geben sie 'q', 'quit' oder  'exit' ein.\n"
          "Bitte geben sie die Seitenzahl des Würfels ein.")
    wurfel = Wurfel(int(input()))
    while not input() in ("q", "quit", "exit"):
        print(wurfel.werfen())
