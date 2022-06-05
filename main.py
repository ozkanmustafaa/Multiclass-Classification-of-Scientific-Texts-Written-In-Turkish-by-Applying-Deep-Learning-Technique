# coding=utf-8

from __future__ import print_function
import mechanize
import requests
import array as arr

from bs4 import BeautifulSoup

f = open("output.txt")

url = "https://tez.yok.gov.tr/UlusalTezMerkezi/tarama.jsp"

def get_details(tez_no):
    browser = mechanize.Browser()

    browser.open(url)
    browser.select_form(name="GForm")
    browser["TezNo"] = str(x)

    response = browser.submit()
    content = response.read()

    details_start = content.find("tezDetay('")
    details_end = content.find(")", details_start)

    details = content[details_start + len("tezDetay("):details_end]
    web_id, web_no = details.split(",")
    web_id, web_no = map(lambda x: x[1:-1], (web_id, web_no))
    tez_url = "https://tez.yok.gov.tr/UlusalTezMerkezi/tezDetay.jsp?id=%s&no=%s" % (web_id, web_no)

    page = requests.get(tez_url)
    soup = BeautifulSoup(page.content, 'html.parser')

    tez_name = soup.find_all("tr")[1].find_all("td")[2].text.split("Yazar")[0].strip()
    tez_detay = soup.find_all("tr")[3].find_all("td")[0].text.strip()

    tez_detay_str = ""
    # for i in tez_detay:
    #     tez_detay_str = tez_detay_str + " " + tez_detay[i]
    # print(tez_detay_str)

    # Fix white space related problems
    tez_name = tez_name.replace("\n", " ").replace("\r", "")
    tez_detay = tez_detay.replace("\n", " ").replace("\r", "")

    result = {
        "name": tez_name,
        "detay": tez_detay
    }

    name_parts = tez_name.split(" / ")

    if len(name_parts) == 2 and name_parts[1][0].isupper():
        result["name"] = name_parts[0]
        result["translation"] = name_parts[1]

    #return (u"İsim: %s" % result["name"])
    #return (u"Detay: %s" % result["detay"])

    if result.get("translation"):
    #    return (u"İsim: %s" % result["translation"])
        return (u"Detay: %s" % result["detay"])

if __name__ == "__main__":
    tez_no = arr.array('i', [363549,
490121,
328340,
469071,
349894,
606992,
546712,
527393,
416526,
371800,
328498,
327105,
328449,
299115,
299101,
266459,
642837,
606692,
571024,
603654,
597485,
561838,
581481,
544356,
563560,
605025,
595791,
595834,
486725,
542780,
526427,
507209,
528331,
517421,
457650,
457880,
490125,
476262,
444438,
442008,
442283,
409943,
416435,
368798,
382776,
340956,
328475,
387290,
328346,
309883,
306882,
307092,
266169,
282871
    ])
    try:
        for x in tez_no:
            details = get_details(x)
            print(x)
            print(details.encode('utf-8'), file=f)
        f.close()
    except:
        print("Tez bulunamadı!")
