import time
from typing import Any
import requests
import random
import urllib.parse
import os
from colorama import Fore, Style, init
import argparse
import re
import pyfiglet
from random import randint, choices
import logger
import json

init(autoreset=True)

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def art():
    print("\033[0m\n\033[1;96m---------------------------------------\033[0m\n\033[1;93mScript created by: Bicabo98\033[0m\n\033[1;92mMy QQ:1069324346\033[0m\n\033[1;91mVisit my GitHub: \nhttps://github.com/Bicabo98\033[0m\n\033[1;96m---------------------------------------\033[0m\n\033[1;38;2;139;69;19;48;2;173;216;230m-------------[Bool Bot]-------------\033[0m\n\033[1;96m---------------------------------------\033[0m")
    print("\033[1;93m我是个python菜鸟，现在初尝试python\033[0m")
    print("\033[1;93mI am python rookie, please dont hurt me, let me know if you want to new features\033[0m")
    result = pyfiglet.figlet_format("Bicabo98")
    print(result)



headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Content-Type': 'application/json',
    'Connection': 'keep-alive',
    'Origin': 'https://web.billion.tg',
    'Referer': 'https://web.billion.tg/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Ch-Ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    'Sec-Ch-Ua-mobile': '?1',
    'Sec-Ch-Ua-platform': '"Android"',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.6422.165 Mobile Safari/537.36',
    'X-Requested-With': 'org.telegram.messenger'
}

def countdown_timer(seconds):
    while seconds > 0:
        mins, secs = divmod(seconds, 60)
        hours, mins = divmod(mins, 60)
        print(f"{Fore.CYAN + Style.BRIGHT}Wait {hours:02}:{mins:02}:{secs:02}", end='\r')
        time.sleep(1)
        seconds -= 1
    print("Wait 00:00:00          ", end='\r')

def read_data_file(file_path):
    accounts = []
    with open(file_path, "r") as file:
        lines = file.readlines()
        for line in lines:
            encoded_data = line.strip()
            if encoded_data:
                accounts.append(encoded_data)
    return accounts


def decode_data(encoded_data):
    params = dict(item.split('=') for item in encoded_data.split('&'))

    decoded_user = urllib.parse.unquote(params['user'])
    #decoded_start_param = urllib.parse.unquote(params['start_param'])

    return decoded_user


def get_staking_balance(decoded_data, session,wallet_address: str):
    url = "https://betatest-rpc-node-http.bool.network/"
    chain_id = TRANSACTION_METHODS['eth_chainId']
    chain_id['id'] = 1
    get_balance = TRANSACTION_METHODS['eth_getBalance']
    get_balance['id'] = 2
    get_balance['params'][0] = wallet_address
    json_data = [chain_id, get_balance]

    response = session.post(url, headers=headers, json=json_data)
    response.raise_for_status()  
    transaction_data = response.json()  

    hex_balance = transaction_data[1].get('result')
    dec_balance = int(hex_balance, 16)
    return int(dec_balance / 1e18)



def processing_tasks(decoded_data, session):

    try:
        DISABLED_TASKS: list[str] = ['CONNECT_WALLET', 'INVITE_FRIENDS', 'BOOST_TG', 'SEND_SIMPLE_TON_TRX']
        JOIN_TG_CHANNELS: bool = True

        url = "https://api.billion.tg/api/v1/tasks/"

        response = session.get(url, headers=headers)
        response.raise_for_status()  
        response_json = response.json() 
        tasks = response_json['response']

        for task in tasks:
            if not task['isCompleted'] and task['type'] not in DISABLED_TASKS:
                countdown_timer(5)
                print(f"{decoded_data['first_name']} | Performing task <lc>{task['taskName']}</lc>...")
                match task['type']:
                    case 'SUBSCRIPTION_TG':
                        if JOIN_TG_CHANNELS:
                            print(f"{decoded_data['first_name']} | Please do yourself to join TG channel <lc>{task['link']}</lc>")
                            continue
                        else:
                            continue
                    case 'REGEX_STRING':
                        print(f"{decoded_data['first_name']} | Please do yourself to Change your name title <lc>{task['link']}</lc>")
                        continue
                    case _:
                        result = perform_task(decoded_data, session, task_id=task['uuid'])
                
                if result:
                    print(
                        f"{decoded_data['first_name']} | Task <lc>{task['taskName']}</lc> completed! | "
                        f"Reward: <e>+{task['secondsAmount']}</e> seconds")
                else:
                    print(f"{decoded_data['first_name']} | Failed to complete task <lc>{task['taskName']}</lc>")

    except Exception as error:
        print(f"{decoded_data['first_name']} | Unknown error when processing tasks: {error}")
        countdown_timer(3)

                  
    
def perform_task(decoded_data, session,task_id: str):
    try:
        url = "https://api.billion.tg/api/v1/tasks/"
        json={'uuid': task_id}
        response = session.post(url, headers=headers, json=json)
        response.raise_for_status()  # 
        response_json = response.json()  #
        return response_json['response']['isCompleted']
    
    except Exception as e:
        print(f"{decoded_data['first_name']} | Unknown error while check in task {task_id} | Error: {e}")
        countdown_timer(3)

    
def get_info_data(auth_data, session):
    url = "https://api.billion.tg/api/v1/users/me"
    headers["Authorization"] = "Bearer " + auth_data
    response = session.get(url, headers=headers)
    response.raise_for_status()  # 
    response_data = response.json()  #
    print("get_info_data:",response_data)
    return response_data['response']['user']
    

def login(decoded_data, session):
    url = "https://api.billion.tg/api/v1/auth/login"
    headers["Tg-Auth"] =  decoded_data
    try:
        response = session.get(url, headers=headers)
        response.raise_for_status()  # 
        response_data = response.json()  #
        print("response_data:",response_data)
       
        
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

    if response_data['response']:
                login_data = response_data['response']
                if login_data['isNewUser']:
                    print(f'New User registered!')
    return login_data['accessToken']


def main():
    file_path = "data.txt"
    encoded_data_list = read_data_file(file_path)
    arg = argparse.ArgumentParser()
    arg.add_argument("--proxy", default="proxies.txt")
    args = arg.parse_args()
    proxy_file_path = args.proxy
    if not os.path.exists(proxy_file_path):
        print(f"Error: Proxy file '{proxy_file_path}' does not exist.")
        return
    proxies = open(args.proxy).read().splitlines()
    print("检测到代理数量:", len(proxies))
    use_proxy = True if len(proxies) > 0 else False
    print("use proxy:", use_proxy)

    auto_task = True


    try:
        while True:
            # clear_terminal()
            art()
            for index, encoded_data in enumerate(encoded_data_list, start=1):

                if use_proxy:
                    proxy = proxies[index % len(proxies)]
                    session = requests.Session()
                    session.proxies.update({"http": proxy, "https": proxy})
                    print("use proxy:", proxy)


                print(f"{Fore.CYAN + Style.BRIGHT}------Account No.{index}------")
                decoded_data = decode_data(encoded_data)
                decoded_data = json.loads(decoded_data)
                print("decoded_data:", decoded_data)
                auth_data = login(encoded_data, session)
                user_info = get_info_data(auth_data,session)

                death_date = user_info['deathDate']
                balance = int(death_date - time.time())
                is_alive = user_info['isAlive']
                print(f"{decoded_data['first_name']} | Balance: <e>{balance}</e> seconds | Is user alive: <lc>{is_alive}</lc>")
                
                
                if auto_task:
                    processing_tasks(decoded_data, session)

                countdown_timer(4)

            print("==============  Execution completed, waiting for the next round =================")
            countdown_timer(7200)
    except KeyboardInterrupt:
        print("\n程序已被用户中断。正在清理资源并退出...")
        print("\nThe program has been interrupted by the user. Cleaning up resources and exiting...")

if __name__ == "__main__":
    main()
