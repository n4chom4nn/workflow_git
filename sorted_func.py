"""
numbers = [4, 2, 7, 1, 9]
ergebnis = sorted(numbers, reverse=True)
print(ergebnis)
"""
numbers = [4, 2, 7, 1, 9]
ergebnis = sorted(numbers, reverse=True)
print(ergebnis)
items = [("Apfel", 3), ("Banane", 2), ("Kirsche", 5), ("Dattel", 1)]

sortierte_items = sorted(items, key=lambda wasauchimmer: wasauchimmer[1], reverse=True)

print(sortierte_items)

items2 = [("Stirb langsam", 7), ("Banane", 6), ("Kirsche", 5), ("Dattel", 1)]

sortierte_items2 = sorted(items, key=lambda wasauchimmer: wasauchimmer[1], reverse=True)

"""

zahlen = [4, 2, 7, 1, 9]



ergebnis = sorted(zahlen, reverse=True)



print(ergebnis)

"""


## key -> braucht eine Funktion, die sagt, wie sortiert wird


def str_laenge(string):
    return len(string)


namen = ["Arnold", "Peter", "Hans", "Max", "Judith", "Steph"]

## funktion_x() -> sobald ihr Klammern seht, ist es ein Funktionaufruf

# for name in namen:

#     print(f"Der Name {name} hat {str_laenge(name)} Zeichen")

#                        lamba = key-word  variable:    return-Wert

sortierte_namen = sorted(namen, key=lambda name: len(name))

mein_anderer_string = str_laenge("was auch immer")

print(sortierte_namen)