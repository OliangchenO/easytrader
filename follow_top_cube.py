import random
from datetime import datetime
import json
import redis
import os
import easytrader.sendmail

import time

import easytrader

redis_export_time = 86400
r = redis.Redis(host='localhost', port=6379, db=0)
date_str = datetime.now().strftime("%Y-%m-%d")
# 获取当前文件路径
current_path = os.path.abspath(__file__)
# 获取当前文件的父目录
father_path = os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".")
user = easytrader.use('xq')
user.prepare(os.path.join(father_path, "xq.json"))


def get_cookie():
    redis_cookies = json.loads(r.get("xue_qiu_cookies"))
    return redis_cookies[random.randint(0, len(redis_cookies)-1)]


def reset_cookies():
    redis_cookies = [
        "xq_a_token=f08a32e242338bcc98ff69c2c46f06491e601791; xq_r_token=8ff15c48ad46599ebf51ba3b4ff8b268768a04bc",
        "xq_a_token=8e8257f583bfb613c5a23f9e5b6cd4f63ff23c5b; xq_r_token=22152bf1cd9f4bc6e8e14461bf1cac33678eedb8",
        "xq_a_token=f4254e7026648a2ca246e63187877ef3890bae41; xq_r_token=b984c956d81916bbd6be0aa47bfce231978731ab"]
    r.set("xue_qiu_cookies", json.dumps(redis_cookies))


def del_cookies(cookie):
    redis_cookies = json.loads(r.get("xue_qiu_cookies"))
    redis_cookies.remove(cookie)
    r.set("xue_qiu_cookies", json.dumps(redis_cookies))


def cookies_size():
    redis_cookies = json.loads(r.get("xue_qiu_cookies"))
    return len(redis_cookies)


def sort_by_value(dict_to_sort, reverse):
    sorted_list = sorted(dict_to_sort.items(), key=lambda d: d[1], reverse=reverse)
    sorted_dict = {}
    for o in sorted_list:
        sorted_dict[o[0]] = o[1]
    return sorted_dict


def get_top_cube_list(num):
    top_cubes_key = "top_cube_symbol_list_" + date_str
    top_cube_symbol_list = None
    if r.get(top_cubes_key) is not None:
        top_cube_symbol_list = json.loads(r.get(top_cubes_key))
    if top_cube_symbol_list is None or len(top_cube_symbol_list) < num:
        top_cube_symbol_list = user.get_top_cube_list('YEAR', num)
        r.set(top_cubes_key, json.dumps(top_cube_symbol_list), redis_export_time)
    print(top_cube_symbol_list)
    return top_cube_symbol_list


def get_top_cubes_holding(symbol):
    cube_holding_list_key = symbol + "_" + date_str
    holding_list = None
    if r.get(cube_holding_list_key) is not None:
        holding_list = json.loads(r.get(cube_holding_list_key))
    if holding_list is None:
        try:
            cookies = get_cookie()
            holding_list = user.get_position_for_xq(cube_symbol, cookies)
            r.set(cube_holding_list_key, json.dumps(holding_list), redis_export_time)
        except Exception as e:
            print(e)
            del_cookies(cookies)
            if cookies_size() == 0:
                time.sleep(1200)
                reset_cookies()
            cookies = get_cookie()
            holding_list = user.get_position_for_xq(cube_symbol, cookies)
            r.set(cube_holding_list_key, json.dumps(holding_list), redis_export_time)
    print(holding_list)
    return holding_list


reset_cookies()
cube_list = get_top_cube_list(100)
cubes_holding = {}
for cube_symbol in cube_list:
    cubes_holding[cube_symbol] = get_top_cubes_holding(cube_symbol)
print(cubes_holding)
cubes_holding_pre = {}
for (cube_symbol, holdings) in cubes_holding.items():
    for holding_stock in holdings:
        if holding_stock["stock_symbol"] is not None and holding_stock["stock_symbol"] in cubes_holding_pre:
            weight = float(cubes_holding_pre.get(holding_stock["stock_symbol"]))
            cubes_holding_pre[holding_stock["stock_symbol"]] = float(holding_stock["weight"]) + weight
        else:
            cubes_holding_pre[holding_stock["stock_symbol"]] = float(holding_stock["weight"])
# cube_holdings_rank = sorted(cubes_holding_pre.items(), key=lambda stock: stock[1], reverse=True)
cube_holdings_rank = sorted(cubes_holding_pre.items(), key=lambda stock: stock[1], reverse=True)
print("当前选股排名**********************************************")
print(cube_holdings_rank)
cube_holdings_5 = cube_holdings_rank[0:5]
print("前五名持仓**************************************")
print(cube_holdings_5)
print("当前持仓：*********************************************")
now_holding = user.get_position_for_xq()
print(now_holding)
should_buy_list = []
for buy_stock in cube_holdings_5:
    should_buy_list.append(buy_stock[0])
adjust_info = "调仓成功！ "
for now_holding_stock in now_holding:
    stock_symbol = now_holding_stock["stock_symbol"]
    if stock_symbol not in should_buy_list:
        # 当前持仓不在备选组合中卖出
        user.adjust_weight(stock_symbol, 0)
        adjust_info.join("卖出，股票：" + stock_symbol)
    else:
        should_buy_list.remove(stock_symbol)
balance = user.get_balance_for_follow()
error_code = balance["error_code"]
if error_code is None:
    cash = balance["cash"]
    if len(should_buy_list) > 0:
        weight = cash/len(should_buy_list)
        for buy_stock in should_buy_list:
            user.adjust_weight(buy_stock, weight)
            adjust_info.join("买入，股票：" + buy_stock + "买入比例：" + str(weight))
mail = easytrader.sendmail.MailUtils()
mail.send_email("593705862@qq.com", "调仓成功", adjust_info)


