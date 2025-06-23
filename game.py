"""
五子棋
by TW_bh
"""

import time
import os
import json
from time import sleep
from pt import (
    print_color,
    con,
    clear,
    credit,
    select_folder_dir,
    color_text,
    print_space,
)

五子棋_ver: str = "3.7"
五子棋_support_pt_ver = "5.9"

五子棋_change_log: str = """
3.0:
    **2025-05-11__Sunday**
    1更新pt版本。,pt_v4.5
    2修復使用的模組未匯入。,未 import os
    3將錯誤方法修正。,os.path.join代替直接路徑 + 檔案
    4更改打開 & 儲存檔案。,修復神奇的驗證
    5增加時間顯示。
    6讓x & y軸更明顯。
    7修復錯誤

3.1:
    1更新pt。,pt v4.18

3.2:
    1新增game副程式act_input。
    2更改print_board高亮，原為int，現為str。,更改給予的變數類型

3.3:
    **2025-05-29**
    **pt v4.25
    1修復打開檔案時，有資料夾沒有檔案造成的遊戲崩潰。

3.4:
    **2025-05-31**
    **pt v5.2
    1修復錯誤。,總之就是非常多！

3.5:
    **2025-06-01**
    **pt v5.2
    1重寫check_win，現在可以自訂獲勝數。
    2更改save，如已有檔案，先詢問。

3.6:
    **2025-06-07**
    **pt v5.3
    1優化。
    2更新open_file()。

3.7:
    **2025-06-13**
    1修復錯誤邏輯。
    2現在設定(win_need, player, board_size)有預設了。
    3更新print_board()。
"""

start_time = 0
count_time = 0
board_size_x: int = 20
board_size_y: int = 20
board: dict = {}
turn: str = "藍"  # sky_blue
##藍sky_blue→橘orange→青cyan→棕brown  詳見：player_num: dict
turn_num: int = 1

player_count: int = 2
##紀錄有幾個玩家遊玩

win_need: int = 5
##連幾格獲勝

player_color: dict = {
    "空": "bold",
    ##
    "藍": "sky_blue",
    "橘": "orange",
    "青": "cyan",
    "棕": "brown",
    "紫": "purple",
    "灰": "dark_gray",
    "紅": "red",
    "綠": "green",
}
player_num: dict = {
    1: "藍",
    2: "橘",
    3: "青",
    4: "棕",
    5: "紫",
    6: "灰",
    7: "紅",
    8: "綠",
}
##計算最多人數
max_player_count: int = 0
for init_num in player_num:
    max_player_count = init_num


def main():
    global board_size_x, board_size_y
    global player_count, max_player_count
    global win_need
    credit(True)
    print_color("bg_cyan", "五子棋版本v" + 五子棋_ver)
    print()
    con()
    print_color("bright_blue", "更改內容:")
    print()
    print_color("light_blue", 五子棋_change_log)
    print()
    while True:
        ##win_need
        win_need_str = con("light_cyan", "（enter為預設，預設為5）連幾格獲勝： ")
        if win_need_str == "":
            break
        try:
            win_need = int(win_need_str)
        except ValueError:
            print_color("light_red", "輸入錯誤：非數字。")
            continue
        break
    #
    ##player
    while True:
        player_count_str = con("light_cyan", "（enter為預設，預設為2）玩家人數： ")
        if player_count_str == "":
            break
        try:
            player_count = int(player_count_str)
        except ValueError:
            print_color("light_red", "輸入錯誤：非數字。")
            continue
        if player_count <= 1:
            print_color("light_red", "人數過低")
            continue
        elif player_count > max_player_count:
            print_color("light_red", "人數過多")
            continue
        break
    #
    ##board_size_x 
    while True:
        ##x
        board_size_x_str = con("light_cyan", "（enter為預設，預設為20）橫向棋盤長度： ")
        if board_size_x_str == "":
            break
        try:
            board_size_x = int(board_size_x_str) + 1
        except ValueError:
            print_color("light_red", "輸入錯誤：非數字。")
            continue
        if board_size_x < 6:
            print_color("light_red", "範圍太小")
            continue
        break
    while True:
        ##y
        board_size_y_str = con("light_cyan", "（enter為預設，預設為20）y直向棋盤長度： ")
        if board_size_y_str == "":
            break
        try:
            board_size_y = int(board_size_y_str) + 1
        except ValueError:
            print_color("light_red", "輸入錯誤：非數字。")
            continue
        if board_size_y < 6:
            print_color("light_red", "範圍太小")
            continue
        break
    print()
    init()
    game()


def print_board(act_y=None):
    global board_size_x, board_size_y, board
    # x數字
    print_color("reset", " \\")
    for x in range(1, board_size_x):
        x_str = str(x)
        print_space("light_yellow", x_str, (len(str(board_size_x)) - len(x_str)) * 2)
        print_color("reset", " ")
    ##顯示x軸的位子
    print_color("bright_cyan", "<-- x")
    print()
    # 棋盤&y數字
    for y in range(1, board_size_y):
        ##數字
        y_str = str(y)
        print_space("light_yellow", y_str, (len(str(board_size_y)) - len(y_str)) * 2)
        ##棋盤
        for x in range(1, board_size_x):
            xy = str(x) + "~" + str(y)
            ##選擇的位子高亮 
            if board[xy] == "空" and str(y) == act_y:
                print_color("lime_green", board[xy])
            ##player_color裡有「空」
            elif board[xy] in player_color:
                print_color(player_color[board[xy]], board[xy])
            print_color("reset", " ")
        print()
    ##提升y軸的位子
    print_color("bright_cyan", "↑")
    print()
    print_color("bright_cyan", "y")
    print()
    print()


def check_win():
    global board_size_x, board_size_y, board, win_need
    for y in range(1, board_size_y):
        for x in range(1, board_size_x):
            xy = str(x) + "~" + str(y)
            tmp = board[xy]
            #
            right_num = 0
            for xplus in range(win_need):
                x_tmp = x + xplus
                if check(tmp, y, x_tmp) is True:
                    right_num += 1
                else:
                    break
            if right_num >= win_need:
                won(tmp)
            ##
            #
            right_num = 0
            for yplus in range(win_need):
                y_tmp = y + yplus
                if check(tmp, y_tmp, x) is True:
                    right_num += 1
                else:
                    break
            if right_num >= win_need:
                won(tmp)
            ##
            #
            right_num = 0
            for plus_num in range(win_need):
                x_tmp = x + plus_num
                y_tmp = y + plus_num
                if check(tmp, y_tmp, x_tmp) is True:
                    right_num += 1
                else:
                    break
            if right_num >= win_need:
                won(tmp)
            ##
            right_num = 0
            for plus_num in range(win_need):
                y_tmp = y + plus_num
                x_tmp = x - plus_num
                if check(tmp, y_tmp, x_tmp) is True:
                    right_num += 1
                else:
                    break
            if right_num >= win_need:
                won(tmp)
            #


def won(tmp):
    print_color(player_color[tmp], tmp + "隊贏了")
    print()
    exit()


def check(tmp, y, x):
    global board, board_size_y, board_size_x
    xy = str(x) + "~" + str(y)
    if y > board_size_y or x > board_size_x:
        return False
    if y < 0 or x < 0:
        return False
    if (
        y <= board_size_y
        and x <= board_size_x
        and y > 0
        and x > 0
        and tmp == board[xy]
        and tmp != "空"
    ):
        return True


def tip():
    print_color("bg_cyan", "輸入exit可退出遊戲")
    print()
    print_color("bg_cyan", "輸入save可儲存遊戲")
    print()
    print_color("bg_cyan", "輸入of可打開儲存的遊戲")
    print()


def save():
    global board, board_size_x, board_size_y, turn, player_count, win_need
    ##
    clear()
    full_data_path = os.path.join(os.getcwd(), "data")
    try:
        if (
            os.path.exists(full_data_path) is True
            and os.path.isdir(full_data_path) is True
        ):
            pass
        else:
            os.mkdir(full_data_path)
    except FileNotFoundError:
        os.mkdir(full_data_path)
    print_color("bg_true_teal", "請選擇儲存位子")
    print()
    save_road = select_folder_dir(full_data_path)
    #
    file_road_board = os.path.join(save_road, "board.json")
    file_road_board_size_y = os.path.join(save_road, "board_size_y")
    file_road_board_size_x = os.path.join(save_road, "board_size_x")
    file_road_turn = os.path.join(save_road, "turn")
    file_road_player_count = os.path.join(save_road, "player_count")
    file_road_win_need = os.path.join(save_road, "win_need")
    if (
        os.path.exists(file_road_board) is True
        or os.path.exists(file_road_board_size_y) is True
        or os.path.exists(file_road_board_size_x) is True
        or os.path.exists(file_road_turn) is True
        or os.path.exists(file_road_player_count) is True
        or os.path.exists(file_road_win_need) is True
    ):
        while True:
            tmp = con("sky_blue", "已有檔案是否覆蓋?[y/n]： ")
            if tmp.lower() in ["t", "true", "y", "yes"]:
                break
            elif tmp.lower() in ["f", "false", "n", "no"]:
                print_color("bg_true_teal", "已取消儲存！")
                print()
                con()
                return None
            else:
                print_color("light_red", "輸入錯誤。")
    ##
    print()
    print_color("bg_true_teal", "儲存中...")
    #
    with open(file_road_board, "w", encoding="utf-8") as f:
        json.dump(board, f, indent=4)
    #
    with open(file_road_board_size_y, "w") as f:
        f.write(str(board_size_y))
    #
    with open(file_road_board_size_x, "w") as f:
        f.write(str(board_size_x))
    #
    with open(file_road_turn, "w") as f:
        f.write(turn)
    #
    with open(file_road_player_count, "w") as f:
        f.write(str(player_count))
    #
    with open(file_road_win_need, "w") as f:
        f.write(str(win_need))
    #
    print_color("bg_true_teal", color_text("light_green", "儲存成功!"))
    print()
    sleep(0.5)


def open_file():
    global board, board_size_x, board_size_y, turn, player_count, win_need
    ##
    clear()
    print_color("bg_true_teal", "請選擇先前儲存的位子。")
    print()
    full_data_path = os.path.join(os.getcwd(), "data")
    try:
        if (
            os.path.exists(full_data_path) is True
            and os.path.isdir(full_data_path) is True
        ):
            pass
        else:
            os.mkdir(full_data_path)
            pass
    except FileNotFoundError:
        os.mkdir(full_data_path)
    #
    open_road = select_folder_dir(full_data_path)
    ##
    print()
    print_color("bg_true_teal", "打開中...")
    #
    file_road_board = os.path.join(open_road, "board.json")
    file_road_board_size_y = os.path.join(open_road, "board_size_y")
    file_road_board_size_x = os.path.join(open_road, "board_size_x")
    file_road_turn = os.path.join(open_road, "turn")
    file_road_player_count = os.path.join(open_road, "player_count")
    file_road_win_need = os.path.join(open_road, "win_need")
    # 驗證
    if (
        os.path.exists(file_road_board) is False
        or os.path.exists(file_road_board_size_y) is False
        or os.path.exists(file_road_board_size_x) is False
        or os.path.exists(file_road_turn) is False
        or os.path.exists(file_road_player_count) is False
        or os.path.exists(file_road_win_need) is False
    ):
        print_color("bright_red", "檔案缺失！")
        print()
        con()
        return None
    ########of_ps config 
    foc = 0#    finish open count 
    toc = 6#    total open count 
    ########
    #board 
    of_ps(foc, toc, "開啟檔案")
    with open(file_road_board, "r", encoding="utf-8") as f:
        tmp_board = json.load(f)
    foc += 1
    of_ps(foc, toc, "開啟檔案")
    #board_size_y 
    with open(file_road_board_size_y, "r") as f:
        tmp_board_size_y_str = f.read()
    try:
        tmp_board_size_y = int(tmp_board_size_y_str)
    except ValueError:
        print_color("light_red", "檔案格式錯誤，開啟失敗。")
        print()
        con()
    foc += 1
    of_ps(foc, toc, "開啟檔案")
    #
    with open(file_road_board_size_x, "r") as f:
        tmp_board_size_x_str = f.read()
    try:
        tmp_board_size_x = int(tmp_board_size_x_str)
    except ValueError:
        print_color("light_red", "檔案格式錯誤，開啟失敗。")
        print()
        con()
    foc += 1
    of_ps(foc, toc, "開啟檔案")
    #
    with open(file_road_turn, "r") as f:
        tmp_turn = f.read()
    foc += 1
    of_ps(foc, toc, "開啟檔案")
    #
    with open(file_road_player_count, "r") as f:
        tmp_player_count_str = f.read()
    try:
        tmp_player_count = int(tmp_player_count_str)
    except ValueError:
        print_color("light_red", "檔案格式錯誤，開啟失敗。")
        print()
        con()
    foc += 1
    of_ps(foc, toc, "開啟檔案")
    #
    with open(file_road_win_need, "r") as f:
        tmp_win_need_str = f.read()
    try:
        tmp_win_need = int(tmp_win_need_str)
    except ValueError:
        print_color("light_red", "檔案格式錯誤，開啟失敗。")
        print()
        con()
    foc += 1
    of_ps(foc, toc, "開啟檔案")
    ##更新
    foc = 0
    of_ps(foc, toc, "更新資料")
    #
    board = tmp_board
    foc += 1
    of_ps(foc, toc, "更新資料")
    #
    board_size_y = tmp_board_size_y
    foc += 1
    of_ps(foc, toc, "更新資料")
    #
    board_size_x = tmp_board_size_x
    foc += 1
    of_ps(foc, toc, "更新資料")
    #
    turn = tmp_turn
    foc += 1
    of_ps(foc, toc, "更新資料")
    #
    player_count = tmp_player_count
    foc += 1
    of_ps(foc, toc, "更新資料")
    #
    win_need = tmp_win_need
    foc += 1
    of_ps(foc, toc, "更新資料")
    ##
    print_color("bg_true_teal", "打開成功!")
    print()
    con()

def of_ps(foc: int, toc: int, dt: str):
    """open file print speed"""
    #dt = doing (thing's) type
    print("", end="\r")
    print_color("dim", "正在" + dt)
    print_color("bold", str(foc))
    print_color("dim", "/" + str(toc))


def game():
    global board_size_x, board_size_y, baord, turn, turn_num
    global player_count, all_player, player_color
    global start_time, count_time
    while True:
        ###########
        ##act_y
        while True:
            clear()
            tip()
            print_board()
            #
            start_time = time.time()
            print_color("bg_true_teal", "你的對手花了" + str(count_time) + "秒")
            print()
            act_y_str = con(
                "",
                color_text([player_color[turn]], "現在是")
                + color_text(["bold", player_color[turn]], turn)
                + color_text([player_color[turn]], "隊,你的動作(左邊的數字y)： "),
            )
            if act_y_str == "save":
                save()
                continue
            elif act_y_str == "of":
                open_file()
                continue
            elif act_y_str in ["exit", "退出"]:
                exit()
            try:
                act_y_int = int(act_y_str)
            except ValueError:
                print()
                print_color("light_red", "輸入錯誤：非數字。")
                print()
                sleep(0.75)
                continue
            if act_y_int >= board_size_x or act_y_int < 1:
                print()
                print_color("light_red", "超出棋盤大小")
                print()
                sleep(0.75)
                continue
            break
        #
        while True:
            print_board(act_y_str)
            act_x_str = con(
                "",
                color_text([player_color[turn]], "現在是")
                + color_text(["bold", player_color[turn]], turn)
                + color_text([player_color[turn]], "隊,你的動作(右邊的數字x)："),
            )
            if act_x_str == "save":
                save()
                continue
            elif act_x_str == "of":
                open_file()
                continue
            elif act_x_str == "exit":
                exit()
            try:
                act_x_int = int(act_x_str)
            except ValueError:
                print()
                print_color("light_red", "輸入錯誤：非數字。")
                print()
                sleep(0.75)
                continue
            if act_x_int >= board_size_x or act_x_int < 1:
                print()
                print_color("light_red", "超出棋盤大小")
                print()
                sleep(0.75)
                continue
            break
        #
        xy = act_x_str + "~" + act_y_str
        if board[xy] != "空":
            print()
            print_color("light_red", "這個位子已有棋子")
            print()
            sleep(0.75)
            continue
        board[xy] = turn
        count_time = time.time() - start_time
        #
        if player_count > turn_num:
            turn_num += 1
        else:
            turn_num = 1
        turn = player_num[turn_num]
        check_win()


def init():
    global board_size_x, board_size_y, board
    size_y = board_size_y + 5
    size_x = board_size_x + 5
    board["0~0"] = "空"
    for y in range(1, size_y):
        for x in range(1, size_x):
            xy = str(x) + "~" + str(y)
            board[xy] = "空"


if __name__ == "__main__":
    main()
