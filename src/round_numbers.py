def round_price(amount: float) -> float:
    """
    (Dz. U. Nr 90, poz. 798) kwoty wykazywane w fakturze zaokrągla się do pełnych groszy, przy czym końcówki poniżej 0,5 grosza pomija się,
    a końcówki 0,5 grosza i wyższe zaokrągla się do 1 grosza.

    Zaokrągla kwotę zgodnie z polskimi przepisami:
    - Końcówki poniżej 0,5 grosza pomija się
    - Końcówki 0,5 grosza i wyższe zaokrągla się w górę do 1 grosza
    """
    grosze = round(amount * 100, 4)  # Konwersja na grosze, precyzja do 4 miejsc
    grosze_zaokraglone = int(grosze) if grosze % 1 < 0.5 else int(grosze) + 1
    
    return "{:.2f}".format(grosze_zaokraglone / 100, 2)

if __name__ == "__main__":
    print(round_price(123.1155))
    print(round_price(123.116))
    print(round_price(123.115))
    print(round_price(123.114))
    print(round_price(123.11))
    print(round_price(123.1))
    print(round_price(123.0))
    print(round_price(123))
