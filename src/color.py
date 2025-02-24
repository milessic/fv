f"""
Colors may vary on your operating system, but red, green shuold be the same on all of these.

You may adjust values of "Color" class for your needs
"""
try:
    from enum import Enum
    class Color(Enum):
        red = "\033[1;31m"
        bold_orange = "\033[33m"
        orange = "\033[1;33m"
        yellow = "\033[1;33m"
        blue = "\033[1;34m"
        cyan = "\033[1;36m"
        green = "\033[0;32m"
        reset = "\033[0;0m"
        bold = "\033[;1m"
        reverse = "\033[;7m"
except Exception as e:
    class Color:
        red = "\033[1;31m"
        bold_orange = "\033[33m"
        orange = "\033[1;33m"
        yellow = "\033[1;33m"
        blue = "\033[1;34m"
        cyan = "\033[1;36m"
        green = "\033[0;32m"
        reset = "\033[0;0m"
        bold = "\033[;1m"
        reverse = "\033[;7m"

def color(text:str, clr:Color):
    try:
        return(f"{clr.value}{text}{Color.reset.value}")
    except KeyError:
        print(color(f"There is no color as '{clr}'!\nList of colors: {Color.__dict__}", Color.red))
    except AttributeError:
        raise AttributeError("Your Python version is too old for Enums! Instead of function 'color()' use class 'Color' like this: f'{Color.red}THIS IS RED{Color.reset}'")

if __name__ == "__main__":
    # usage:
    print(color("hejka", Color.red), color("naklejka", Color.green))
