# Common Greek Orthodox name days
# Key: (month, day), Value: list of names celebrated on that day

NAME_DAYS: dict[tuple[int, int], list[str]] = {
    (1, 1):  ['Vasilis', 'Vasiliki', 'Vassia'],
    (1, 7):  ['Giannis', 'Ioanna', 'Gianna'],
    (1, 11): ['Theodosios', 'Theodosia'],
    (1, 17): ['Antonis', 'Antonia'],
    (1, 18): ['Athanasios', 'Thanasis', 'Natasa'],
    (1, 30): ['Triantafillos', 'Triantafyllia'],
    (2, 2):  ['Ypapanti'],
    (2, 10): ['Charalambos', 'Babis'],
    (2, 17): ['Theodoros', 'Theodora', 'Thodoris'],
    (3, 25): ['Evangelos', 'Evangelia', 'Vangelis', 'Vangelio'],
    (4, 23): ['Georgios', 'Georgia', 'Giorgos'],
    (4, 24): ['Elisavet', 'Elizabeth'],
    (5, 5):  ['Irene', 'Eirini'],
    (5, 21): ['Konstantinos', 'Konstantina', 'Kostas', 'Eleni'],
    (6, 29): ['Petros', 'Pavlos', 'Paula'],
    (6, 30): ['Apostolos', 'Apostolia'],
    (7, 17): ['Marina'],
    (7, 20): ['Ilias', 'Ilia'],
    (7, 22): ['Magdalini', 'Magda'],
    (7, 26): ['Paraskevi'],
    (7, 27): ['Panteleimon', 'Pantelis'],
    (8, 6):  ['Christos', 'Christiana'],
    (8, 15): ['Maria', 'Marios', 'Marianna', 'Despina'],
    (8, 29): ['Giannis', 'Ioanna'],
    (9, 14): ['Stavros', 'Stavroula'],
    (9, 17): ['Sofia', 'Elpida', 'Pistis', 'Agapi'],
    (10, 18):['Loukas'],
    (10, 26):['Dimitrios', 'Dimitra', 'Mimis'],
    (11, 1): ['Agioi Pantes'],
    (11, 8): ['Michalis', 'Michail', 'Gavriil', 'Aggelos', 'Angeliki'],
    (11, 9): ['Nektarios'],
    (11, 25):['Aikaterini', 'Katerina'],
    (11, 30):['Andreas'],
    (12, 4): ['Varvara', 'Barbara'],
    (12, 6): ['Nikolaos', 'Nikos', 'Nikolas'],
    (12, 9): ['Anastasia', 'Natasa'],
    (12, 12):['Spyridon', 'Spyros'],
    (12, 25):['Christos', 'Christiana', 'Christina'],
    (12, 27):['Stefanos', 'Stefania'],
}


def get_namedays_today(today) -> list[str]:
    """ Returns the list of names celebrated today, or an empty list. """
    return NAME_DAYS.get((today.month, today.day), [])
