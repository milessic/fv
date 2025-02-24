from num2words import num2words

def get_price_as_words(price: float, lang: str = "pl") -> str:
    zlote = int(price)
    grosze = round((price - zlote) * 100)
    
    zlote_slownie = num2words(zlote, lang=lang)
    grosze_slownie = num2words(grosze, lang=lang)
    
    zlote_jednostka = "złoty" if zlote == 1 else "złote" if 2 <= zlote % 10 <= 4 and (zlote % 100 < 10 or zlote % 100 >= 20) else "złotych"
    grosze_jednostka = "grosz" if grosze == 1 else "grosze" if 2 <= grosze % 10 <= 4 and (grosze % 100 < 10 or grosze % 100 >= 20) else "groszy"
    
    return f"{zlote_slownie} {zlote_jednostka} {grosze_slownie} {grosze_jednostka}"

if __name__ == "__main__":
    print(get_price_as_words(100))
    print(get_price_as_words(100.23))
    print(get_price_as_words(100.23213))
    print(get_price_as_words(12555.1))
    print(get_price_as_words(12555.1, "en"))
    print(get_price_as_words(12555.1, "de"))
