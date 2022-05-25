import requests as req


def get_rate():
    resp = req.get("https://www.cbr.ru/scripts/XML_daily.asp")
    raw_resp = resp.text
    usd_block=raw_resp.find('<NumCode>840</NumCode>')
    cut_resp=raw_resp[usd_block:]
    value_tag = '<Value>'
    usd_rate_start_position = cut_resp.find(value_tag) + len(value_tag)
    usd_rate_finish_position = cut_resp.find('</Value>')
    usd_rate = float((cut_resp[usd_rate_start_position : usd_rate_finish_position]).replace(',','.'))
    return usd_rate


