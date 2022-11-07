import requests
import json
from lxml import etree

import pandas as pd

def elem2dict(node: etree) -> dict:
    """
    adapted from https://gist.github.com/jacobian/795571
    Convert an lxml.etree node tree into a dict.
    """
    result = {}

    for element in node.iterchildren():
        # Remove namespace prefix
        key = element.tag.split('}')[1] if '}' in element.tag else element.tag

        # Process element as tree element if the inner XML contains non-whitespace content
        if element.text and element.text.strip():
            value = element.text
        else:
            value = elem2dict(element)
        if key in result:

            
            if type(result[key]) is list:
                result[key].append(value)
            else:
                tempvalue = result[key].copy()
                result[key] = [tempvalue, value]
        else:
            result[key] = value
    return result


def get_nport_values(url: str, website: str, email: str) -> pd.DataFrame:
    headers = {"User-Agent": f"{website} {email}"}
    nport = requests.get(url, headers=headers)
    nport.raise_for_status()
    doc = etree.fromstring(nport.content)
    investments = doc.xpath("//nport:invstOrSec", namespaces={'nport':'http://www.sec.gov/edgar/nport'})
    data = [elem2dict(i) for i in investments]
    df = pd.DataFrame(data)
    for c in ['balance', 'valUSD', 'pctVal']:
        df[c] = pd.to_numeric(df[c])
    return df
