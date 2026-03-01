import springernature_api_client.tdm as tdm
import springernature_api_client.openaccess as openaccess
import springernature_api_client.metadata as metadata

api_key = "853444fd144bef2151d80cea41ac755e"

springer_tdm_policy_link = "https://www.springernature.com/gp/researchers/text-and-data-mining"
 
tdm_client = tdm.TDMAPI(api_key=f"api_key/0/500")

response = tdm_client.search(q='keyword:"food fermentation"', p=20, s=1, fetch_all=False, is_premium=False)

print(response)