from flask import Flask, render_template, request, send_file
import json
import io
import urllib.parse
import os


from src.fv import generate_invoice_pdf_in_memory, refresh_template
from src.validators import validate_payload

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/static/{file_name}", methods=['GET'])
def get_static(file_name):
    try:
        file_path = os.path.join(os.path.dirname(__file__), 'static', file_name)
        return send_file(file_path)
    except Exception as e:
        return {"msg": "Nie ma takiego pliku!"}, 404

@app.route("/refresh", methods=['GET'])
def refresh_template_endpoint():
    refresh_template()
    return "ok"

@app.route("/generate-invoice", methods=['POST'])
def generate_invoice():
    try:
        payload = json.loads(request.data)
        lang = payload.get("headers",{}).get("lang")
        ##failures = validate_payload(payload)
        #if len(failures):
        #    pass
        #    #return {"msg": "Brak wymaganych danych", "errors":failures}, 400
        try:
            file_name = urllib.parse.quote_plus(payload["headers"]["invoiceNumber"] + ".pdf")
        except KeyError as k:
            return {"msg": f"Brak wymaganych danych! - {k}"}, 400
    except Exception as e:
        return {"msg": "Niepoprawne dane !", "details": str(e)}, 400
    try:
        pdf = generate_invoice_pdf_in_memory(
                invoice_data=payload,
                lang=lang
                )
    except Exception as e:
        return {"msg": "Niepoprawne dane!", "details": str(e)}, 400
    try:
        return send_file(
                io.BytesIO(pdf),
                mimetype="application/pdf",
                as_attachment=True,
                download_name=file_name
                )
    except Exception as e:
        return {"msg": "Niepoprawne dane!", "details": str(e)}, 400


if __name__ == "__main__":
    try:
        env = json.load(open(".env.json","r"))
    except:
        raise FileNotFoundError("Cannot load .env.json file!")
    host = env.get("host","1.0.0.0")
    port = env.get("port",8123)
    debug = env.get("debug", False)
    if debug:
        app.run(
                host=env.get("host","0.0.0.0"), 
                port=env.get("port",8123), 
                debug=True
        )
    else:
        from waitress import serve
        print("server started")
        serve(app, host=host, port=port)
