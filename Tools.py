from duckduckgo_search import DDGS
#query="https://www.apollopharmacy.in/medicine/famocid-40mg-tablet"
def get_medicine_information(medicine_name):
    results=DDGS().text(medicine_name,max_results=10)
    return results[0]["body"]