#!/usr/bin/env python
from sys import exit
from os import system
from functions import (
    search, 
    driver_quit,
    get_search_results,
    init_driver,
    get_episodes,
    get_video_url,
    get_video,
    download_video,
)
from banners import ( 
    header, 
    TITLE, 
    BROWSE_HEADER, 
    EPISODES_HEADER,
)

URL = "http://hentaimama.io"

def exit_check(user_input, driver=False):
    if user_input == "exit" or user_input == "quit":
        if driver:
            print("[+] Kill signal received...")
            driver_quit(driver)
            print("[+] Exiting...")
            exit(0)
        else:
            exit(0)
    else:
        pass

def validate_input(user_input, list_length):
    try:
        test = int(user_input)
    except ValueError:
        print("[x] Please enter a valid integer...")
        return False
    else:
        if int(user_input) > list_length or int(user_input) < 1:
            print("[x] Please select an item from the list...")
            return False
        else:
            return True

def browse_loop(titles, links, op):
    
    while True:
        system('clear')

        if op == 'browse':
            header(BROWSE_HEADER)
        else:
            header(EPISODES_HEADER)

        for t in range(len(titles)):
            print(f"{t + 1}. {titles[t]}")
        
        choice = input("\n[+] Select: ")
        exit_check(choice)
        valid_choice = validate_input(choice, len(titles))

        if valid_choice:
            return choice
            break
        else:
            continue            

def main_loop():

    while True:
        system('clear')
        driver = init_driver(URL)

        header(TITLE)
        key_word = input("[+] Search: ")
        
        exit_check(key_word, driver)
        
        driver = search(driver, key_word)
        titles, links  = get_search_results(driver)
        choice = browse_loop(titles, links, 'browse')

        driver = init_driver(links[int(choice) - 1])
        episode_titles, episode_links = get_episodes(driver)
        episode_choice = browse_loop(episode_titles, episode_links, 'episodes')

        driver = init_driver(episode_links[int(episode_choice) - 1])
        video_url = get_video_url(driver)

        driver = init_driver(video_url)
        dl_url, status = get_video(driver)

        if status:
            download_video(dl_url, titles[int(choice) - 1], episode_titles[int(episode_choice) - 1])
        else:
            input("[+] Press any key to continue...")
            continue

        #download_video(titles[int(choice) - 1], episode_titles[int(episode_choice) - 1], episode_links[int(episode_choice) - 1])
    