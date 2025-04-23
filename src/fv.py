import json
import pdfkit
from jinja2 import Environment, FileSystemLoader
import sys
import os
from src.color import color, Color
from src.numbers_as_words import get_price_as_words
from src.round_numbers import  round_price
from src.translations import Translations

help_text = """=== pyFV
a program to generate Faktura VAT
isPies? Tak, of course.

options:
    --name           - provide additional path for output files, provide it as last argument
    --skippdf        - generate only HTML file
    --help           - show help

Examples:
--- generate both HTML and PDF for default location from file json_data.json
    python3 main.py json_data.json  
--- generate only HTML for custom location from file json_data.json located in ./my_dir/
    python3 main.py --skippdf --name ./my_dir/json_data.json
--- generate for custom location ./generated_fvs/ from file json_data.json located in ./fv_data/data.json
    python3 main.py --name ./generated_fvs ./fv_data/data.json
"""
debug = False

results_folder = "results"
templates_folder = "templates"

# setup dirs
main_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

## templates and results paths
template_dir = os.path.join(main_dir, templates_folder)
results_dir = os.path.join(main_dir, results_folder)

# setup Jinja2 stuff
env = Environment(loader=FileSystemLoader(template_dir))
template = env.get_template("invoice_template.html")

def refresh_template():
    global template
    template = env.get_template("invoice_template.html")

def print_status(msg:str, really:bool, invoice_number, prefix:str="Faktura ", msg_color:Color=Color.reset):
    if really:
        print(f"{color(prefix, Color.blue)}{color(invoice_number, Color.bold)}: {color(msg, msg_color)}")

def generate_invoice_name(invoice_data:dict):
    return f"""faktura {invoice_data["headers"]["invoiceNumber"].replace("/","_")}"""

def generate_invoice_html(invoice_data:dict, lang:None|str=None):
    return template.render(invoice=invoice_data, t=Translations(lang))

def generate_result_path(invoice_name, file_extension, additional_results_folder=None):
    if additional_results_folder is not None:
        return os.path.join(results_dir, additional_results_folder, f"{invoice_name}.{file_extension}")
    else:
        return os.path.join(results_dir, f"{invoice_name}.{file_extension}")


def save_html_to_file(html_content:str, filename:str="invoice.html"):
    file_path = os.path.dirname(os.path.abspath(filename))
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)


def convert_html_to_pdf(html_file, pdf_file):
    pdfkit.from_file(html_file, pdf_file)

def calculate_summary(invoice_data:dict) -> dict:
    invoice_data["summary"]["netValue"] = 0
    invoice_data["summary"]["grossValue"] = 0
    invoice_data["summary"]["vatValue"] = 0

    for i, item in enumerate(invoice_data["invoiceItems"]):
        # net
        net = item ["totalNetPrice"]= item["quantity"] * item["unitNetPrice"]
        invoice_data["summary"]["netValue"] += net

        # vat
        vat = (net * ( item["vatRatePercent"] / 100 ))
        invoice_data["summary"]["vatValue"] += vat
        invoice_data["invoiceItems"][i]["totalNetPrice"]= round_price(item["totalNetPrice"])
        invoice_data["invoiceItems"][i]["unitNetPrice"]= round_price(item["unitNetPrice"])

    invoice_data["summary"]["grossValue"] = round_price(invoice_data["summary"]["netValue"] + invoice_data["summary"]["vatValue"])
    invoice_data["summary"]["vatValue"] = round_price(invoice_data["summary"]["vatValue"])
    invoice_data["summary"]["totalInWords"] = get_price_as_words(float(invoice_data["summary"]["grossValue"]), "pl")
    invoice_data["summary"]["netValue"] = round_price(invoice_data["summary"]["netValue"])

    return invoice_data



def generate_invoice_pdf_in_memory(invoice_data:dict, console:bool=False, lang:None|str=None):
    print(lang)
    invoice_number = invoice_data["headers"]["invoiceNumber"]
    invoice_data = calculate_summary(invoice_data)

    if console:
        print_status("Faktura wczytana pomyślnie", console, invoice_number)
    
    # generate html
    html_content = generate_invoice_html(invoice_data, lang)
    pdf = pdfkit.from_string(html_content, False) #configuration=PDFKIT_CONFIG)


    # inform that it's end
    if console:
        print_status(f"proces zakończono pomyślnie!", console, invoice_number, msg_color=Color.green)
    return pdf




def generate_invoices(json_path:str|None = None, invoice_as_dict:dict|None=None, additional_results_folder:str|None=None, console:bool=False, skip_pdf:bool=False, skip_html:bool=False):
    # lod data
    if json_path is not None:
        print(json_path)
        with open(json_path, "r", encoding="utf-8") as f:
            invoice_data = json.load(f)
    elif invoice_as_dict is not None:
        invoice_data = invoice_as_dict
    else:
        raise AssertionError("Either invoice_data or json_path have to be provided!")


    # generate name
    invoice_name = generate_invoice_name(invoice_data)
    invoice_number = invoice_data["headers"]["invoiceNumber"]
    invoice_data = calculate_summary(invoice_data)

    print_status("Faktura wczytana pomyślnie", console, invoice_number)
    
    # generate html
    html_content = generate_invoice_html(invoice_data)

    # generate results
    result_path_html = generate_result_path(invoice_name, "html", additional_results_folder)
    result_path_pdf = generate_result_path(invoice_name, "pdf", additional_results_folder)

    if skip_html:
        print_status("Nie wspierana opcja", console, invoice_number, msg_color=Color.red)
    save_html_to_file(
            html_content, 
            result_path_html
            )
    print_status(f"wygenerowano plik HTML - {result_path_html}", console, invoice_number)
    if not skip_pdf:
        convert_html_to_pdf(
                result_path_html,
                result_path_pdf
                )
        print_status(f"wygenerowano plik PDF - {result_path_pdf}", console, invoice_number)

    # inform that it's end
    print_status(f"proces zakończono pomyślnie!", console, invoice_number, msg_color=Color.green)

if __name__ == "__main__":
    custom_dir = None
    json_dir = sys.argv[-1]
    skip_pdf, skip_html = False, False
    if "--debug" in sys.argv:
        debug = True
    for arg in sys.argv:
        if arg.startswith("--"):
            try:
                match arg.replace("-",""):
                    case "debug":
                        continue
                    case "name":
                        custom_dir = sys.argv[sys.argv.index(arg) + 1]
                    case "skippdf":
                        skip_pdf = True
                    case "skiphtml":
                        skip_html = True
                    case "help":
                        print(help_text)
                        exit(1)

            except Exception as e:
                print(color(f"Cannot fetch argument value for '{arg}' Check arguments or run with '--debug' as first argument to see the full error", Color.red))
                if debug:
                    raise 
                exit(1)
    generate_invoices(
        json_path=json_dir, 
        additional_results_folder=custom_dir,
        console=True,
        skip_html=skip_html,
        skip_pdf=skip_pdf
        )

