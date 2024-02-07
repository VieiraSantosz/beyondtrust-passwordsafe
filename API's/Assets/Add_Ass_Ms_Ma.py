from time import sleep
import requests
import json
import csv
import os
import warnings
warnings.filterwarnings('ignore', category=requests.packages.urllib3.exceptions.InsecureRequestWarning)


### Configuração Cofre ###
ip_cofre       = 'ip do cofre'
url_cofre      = f'https://{ip_cofre}/BeyondTrust/api/public/v3'
workgroupname  = "BeyondTrust Workgroup"
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
    
    os.system('cls')
    print('\nLogin Feito com Sucesso! - Codigo =', login.status_code)
    print('\nUserId..:', userid, 
          '\nUserName:', username, 
          '\nName....:', name)
    print()
#########################################################


################# Adicionar Asset / Manged System/ Managed Account #################################
def Add_Assets_ManagedSystem_ManagedAccount():
    
    print(f'Adicionar Assets | Managed System | Managed Account!\n')
    
    ##### Adicionar Assets #####    
    with open(r'caminho do arquivo csv') as csvfile:
        
        reader = csv.DictReader(csvfile)

        for row in reader:
            sleep(1)
            
            asset_json = {
                'AssetName'      : row['Asset'],
                'IPAddress'      : row['Ip'],
                'DnsName'        : row['Dns'],
                'DomainName'     : row['Domain'],
                'AssetType'      : row['Type'],
                'OperatingSystem': row['System']
            }
            asset_body = json.dumps(asset_json)
            
            url_asset   = url_cofre + f'/Workgroups/{workgroupname}/Assets'
            post_asset  = session.post(url = url_asset, data = asset_body, headers = datype) 
            
            try:
                info_asset = post_asset.json()
                asset_id   = info_asset['AssetID']
                
                print(f'[+] {row["Asset"]} adicionado em Asset com sucesso. - AssetID: {asset_id} | Status Code = {post_asset.status_code}')
                
            except:
                print(f'[-] Erro {row["Asset"]}: {info_asset} | Status Code = {post_asset.status_code}\n')
              

            ##### Adicionar Assets em Managed System pelo Id #####
            managedsystem_json = {
                'PlatformID'         : int, 
                'AutoManagementFlag' : 'bool'
            }
            managedsystem_body = json.dumps(managedsystem_json)
            
            url_managedsystem  = url_cofre + f'/Assets/{asset_id}/ManagedSystems'
            post_managedsystem = session.post(url = url_managedsystem, data = managedsystem_body, headers = datype)  
             
            info_managedsystem = post_managedsystem.json()
             
            try:                               
                managedsystem_id = info_managedsystem['ManagedSystemID']
                hostname         = info_managedsystem['HostName']  
            
                print(f'[+] {hostname} adicionado em Managed System com sucesso. - ManagedSystemID: {managedsystem_id} | Status Code = {post_managedsystem.status_code}')
            
            except:
                print(f'[-] Erro: {info_managedsystem} | Status Code = {post_managedsystem.status_code}')

            
            ##### Adicionar Managed Account nos Managed System pelo Id #####    
            managedaccount = {
                'Accountname': 'string',
                'Password'   : 'string',
                'Description': 'string'
            }
            
            url_managedaccount  = url_cofre + f'/ManagedSystems/{managedsystem_id}/ManagedAccounts'
            post_managedaccount = session.post(url = url_managedaccount, verify = False, data = managedaccount)
            
            try:
                info_account = post_managedaccount.json()
                
                account_name         = info_account['AccountName']
                managedaccount_id    = info_account['ManagedAccountID']
                
                print(f'[+] Conta {account_name} criado com sucesso no {hostname} - ManagedAccountID: {managedaccount_id} | Status Code = {post_managedaccount.status_code}\n')
                
                with open ('Assets\.idmanagedaccount.csv', 'a') as file:
                    file.write(f'\n{managedaccount_id}')
                
            except:
                    print(f'[-] Erro: {info_account} | Status Code = {post_managedaccount.status_code}')                       
####################################################################################################


################# LogOff #################################
def PostLogOff():
    
    logoff = session.post(url = f'{url_cofre}/Auth/Signout', verify=False)  

    print('Usuario acabou de sair da sessao! - Codigo =', logoff.status_code)
    print()
##########################################################


def main():
    PostLogIn()
    Add_Assets_ManagedSystem_ManagedAccount()
    PostLogOff()
    
if __name__ == '__main__':    
    main()
