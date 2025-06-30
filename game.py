# -*- coding: utf-8 -*-
"""
TYCoon(beta)
"""

import time
import threading
import logging

from tqdm import trange
from time import sleep
from pt import print_color, clear, line, print_space
from pt import con as pt_con



tyc_ver = "1.0"
tyc_support_pt_ver = "5.16"

tyc_change_log = """
1.0:
    1release
"""

tyc_logger = logging.getLogger("TYC_logger")

# Game state
money = 0
level = 1
game_finished = False
# All buildings information
all_buildings_info = {
    "小賣鋪": {
        "price": 50,
        "get_back": 5,
    },
    "雜貨店": {
        "price": 100,
        "get_back": 10,
    },
    "花店": {
        "price": 150,
        "get_back": 15,
    },
    "超市": {
        "price": 200,
        "get_back": 20,
    },
    "便利商店": {
        "price": 300,
        "get_back": 30,
    },
    "藥局": {
        "price": 400,
        "get_back": 40,
    },
    "百貨公司": {
        "price": 500,
        "get_back": 50,
    },
    "餐廳": {
        "price": 600,
        "get_back": 60,
    },
    "購物中心": {
        "price": 1000,
        "get_back": 100,
    },
    "商業大廈": {
        "price": 2000,
        "get_back": 200,
    },
    "購物廣場": {
        "price": 5000,
        "get_back": 500,
    },
}

for build in all_buildings_info:
    all_buildings_info[build]["bought_it"] = False


def con(color="reset", text="要繼續嗎 enter？退出輸入exit\n"):
    global game_finished
    tmp_con = pt_con(color, text, ExitInput=False)
    if tmp_con.lower().strip() == "exit":
        game_finished = True
        print_color("bold", "遊戲結束!")
        exit()
    return tmp_con

def main():
    global tyc_ver
    print_color("bg_cyan", "TYCoon v" + tyc_ver)
    print()
    con()
    print_color("light_blue", "更改日志：")
    print()
    print_color("cyan", tyc_change_log)
    con()
    game()


def game():
    global game_finished
    global money
    clear()
    print_color("reset", "") # Reset terminal color
    game_starter = threading.Thread(target=get_money)
    game_starter.start()
    all_chooses = ["2.顯示資訊", "3.購買建築", "4.工作", "5.玩家等級"]
    while True:
        #################
        print_color("orange", "TYCoon v" + tyc_ver)
        print_color("dim", "    by TW_bh")
        print()
        print_color("reset", "金錢：" + str(money))
        line()
        print()
        #
        print_color("dim", "0.退出遊戲")
        print()
        print_color("dim", "1.清除文字")
        print()
        #
        for choose in all_chooses:
            print_color("sky_blue", choose)
            print()
        #
        print_color("")
        #
        line()
        #################
        choice = con("orange", "請輸入選項： ") 
        if choice in ["0", "退出遊戲", "exit", "quit"]:
            game_finished = True
            print_color("bold", "遊戲結束!")
            break
        elif choice == "1":
            clear()
            continue
        elif choice == "2":
            show_info()
        elif choice == "3":
            buy_building()
        elif choice == "4":
            work()
        elif choice == "5":
            player_level()
        else:
            print_color("red", "未知命令!")
            print()
        print_color("reset", "", end="\n\n")

def show_info():
    global money, all_buildings_info
    clear()
    print_color("sky_blue", "目前金錢：")
    print_color("green", str(money))
    print()
    #
    print_space("sky_blue", "名稱", 10, from_front=False)
    print_space("sky_blue", "資訊", 8)
    print()
    for building in all_buildings_info:
        print_space("sky_blue", building, 8, from_front=False, fill_item="  ")
        if all_buildings_info[building]["bought_it"] is True:
            print_color("green", "已購買")
        else:
            print_color("red", "未購買")
        print()
    con()

def buy_building():
    global money, all_buildings_info
    print_color("reset", "", end="\n")
    #
    line()
    print_color("orange", "購買建築")
    line()
    print()
    #
    print_color("sky_blue", "目前金錢：")
    print_color("green", str(money))
    print()
    #
    print_space("sky_blue", "名稱", 12, from_front=False)
    print_space("sky_blue", "價格", 10)
    print_space("sky_blue", "回報", 10)
    print()
    #
    build_num_dict = {}
    build_num = 0
    for building in all_buildings_info:
        build_num += 1
        build_num_dict[building] = build_num
        print_space("reset", str(build_num), 2, from_front=False)
        print_space("sky_blue", building, 10, from_front=False)
        print_space("green", str(all_buildings_info[building]["price"]), 10)
        print_space("green", str(all_buildings_info[building]["get_back"]), 12)
        print()
    #
    choice = con("orange", "請輸入要購買的建築名稱： ")
    choosed_building = build_num_dict.get(choice)
    if choosed_building is None:
        print_color("red", "無此建築!")
        print()
        con()
        return None
    else:
        if all_buildings_info[choosed_building]["bought_it"] is True:
            print_color("red", "已經購買過了!")
            print()
            con()
            return None
        if money < all_buildings_info[choosed_building]["price"]:
            print_color("red", "金錢不足!")
            print()
            con()
            return None
        money -= all_buildings_info[choice]["price"]
        all_buildings_info[choice]["bought_it"] = True
        print_color("green", "購買成功!")
        print()
        con()
        return None

def work():
    global money
    print_color("reset", "", end="\n")
    #
    line()
    print_color("orange", "工作")
    line()
    print()
    #
    print_color("reset", "工作中...")
    print()
    for i in trange(100, desc="工作進度", ncols=80, leave=False, ascii="●>"):
        time.sleep(0.2)
    #
    work_money = 10
    money += work_money
    print_color("green", f"工作結束，薪水{str(work_money)}元。")
    print()
    con()

def player_level():
    global money, level
    print_color("reset", "", end="\n")
    #
    line()
    print_color("orange", "玩家等級")
    line()
    print()
    #
    print_color("sky_blue", "目前等級：")
    print_color("reset", str(level))
    print()
    #
    upgrade = con("orange", "是否升級(1000元)？(y/n) ")
    if upgrade.lower().strip() == "y":
        if money < 1000:
            print_color("red", "金錢不足，無法升級!")
            print()
            con()
            return None
        money -= 1000
        level += 1
        print_color("green", "升級成功!")
    else:
        print_color("yellow", "未升級")
    #
    con()
    return None


def get_money():
    global game_finished, money, all_buildings_info
    while game_finished is False:
        for i in all_buildings_info:
            if all_buildings_info[i]["bought_it"] is True:
                money += all_buildings_info[i]["get_back"]
        time.sleep(1)
    return None

if __name__ == "__main__":
    main()