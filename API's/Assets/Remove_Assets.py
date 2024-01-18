import requests
import json
import urllib3
import ssl
from time import sleep
import csv
from requests.packages.urllib3.exceptions import InsecureRequestWarning
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


### Configuração Cofre ###
ip_cofre       = 'ip do cofre'
url_cofre      = f'https://{ip_cofre}/BeyondTrust/api/public/v3'
workgroupName  = "BeyondTrust Workgroup"
##########################


### Configuração API ###
chave_api = 'xxxxx'
user      = 'user'
headers   = {'Authorization': f'PS-Auth key={chave_api};' f'runas={user};'}

datype  = {'Content-type': 'application/json'}
proxy   = {'http': None,'https': None}
########################


################# Persistencia de Login #################
session             = requests.session()
session.proxies     = proxy
session.trust_env   = False
session.verify      = False
session.headers.update(headers)
#########################################################


################# LogIn #################################
def PostLogIn():
    
    login = session.post(url = f'{url_cofre}/Auth/SignAppin', verify = False) 
    
    info_login = login.json()
    
    userid      = info_login['UserId']
    username    = info_login['UserName']
    name        = info_login['Name']
    
    print("\nLogin Feito com Sucesso! - Codigo =", login.status_code)
    print("\nUserId..:", userid, 
          "\nUserName:", username, 
          "\nName....:", name)
    print()
#########################################################


################# Remover Asset #################################
def Remove_Asset_by_id():
    
    print("Remover Assets!\n")
    
    with open(r'Caminho do arquivo csv') as csvfile:
        
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            asset_id = row['AssetID']
            
            url_get_asset   = url_cofre + f"/Assets/{asset_id}"
            get_asset       = session.get(url = url_get_asset, verify=False)
            
            info_asset = get_asset.json()
            get_asset.raise_for_status()
            
            asset_name = info_asset['AssetName'] 
            
            url_remove_asset    = url_cofre + f"/Assets/{asset_id}"
            remove_asset        = session.delete(url = url_remove_asset, verify=False)
            
            remove_asset.raise_for_status()

            if (remove_asset.status_code < 399):
                print(f"[+] {asset_name} removido com sucesso. | Status Code = {remove_asset.status_code}")
            
            else:
                print(f"[-] {asset_name} não removido. Erro: {remove_asset.json()} | Status Code = {remove_asset.status_code}")
####################################################################


################# LogOff #################################
def PostLogOff():
    
    logoff = session.post(url = f'{url_cofre}/Auth/Signout', verify=False)  

    print("\nUsuario acabou de sair da sessao! - Codigo =", logoff.status_code)
    print()
##########################################################


def main():
    PostLogIn()
    Remove_Asset_by_id()
    PostLogOff()
    
if __name__ == '__main__':
    main()
