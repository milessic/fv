import json
import os

source_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),"templates", "json_template.json")
template = json.load(open(source_path,"r"))


def validate_payload(payload) -> list:
    r"it only check if data is complete in terms of keys, it doesn't check values!"
    failures = []
    for k1,v1 in template.items():
        if k1 == "summary":
            continue
        if payload.get(k1) is None:
            failures.append(f"1-{k1}")
            continue
        # list - items
        if isinstance(v1, list):
            for i in payload["invoiceItems"]:
                for k2 in template.invoiceItems[0]:
                    if k2 not in i:
                        failures.append(f"2-items[{i}][{k2}]")
        # dict
        if isinstance(v1, dict):
            for k2, v2 in v1.items():
                if isinstance(v2, dict):
                    for k3 in payload[k1][k2].keys():
                        if k3 not in payload[k1][k2]:
                            failures.append(f"3-[{k1}][{k2}][{k3}]")
                else:
                    if k2 not in payload[k1]:
                        failures.append(f"3-[{k1}][{k2}][{v2}]")


    return failures
        


    


