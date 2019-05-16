import os
import pickle
from datetime import datetime

import easytrader


def read_top_cube_json():
    file_path = "record/"
    file_name = datetime.now().strftime("%Y-%m-%d") + ".json"
    if os.path.exists(file_path + file_name):
        with open(file_path + file_name, "rb") as f:
            return pickle.load(f)
    else:
        return None


def write_top_cube_json(top_cubes_json):
    file_path = "record/"
    file_name = datetime.now().strftime("%Y-%m-%d") + ".json"
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    with open(file_path + file_name, "wb") as f:
        pickle.dump(top_cubes_json, f)


user = easytrader.use('xq')
user.prepare("xq.json")
top_cubes = read_top_cube_json()
if top_cubes is None:
    top_cubes = user.get_top_cube_list('YEAR', 1000)
    write_top_cube_json(top_cubes)
now_holding = user.get_position_for_xq()
print("当前持仓：*********************************************")
print(now_holding)
cube_holdings = {}
for (cube_symbol, holding_list) in top_cubes.items():
    for holding_stock in holding_list:
        weight = int(cube_holdings.get(holding_stock["stock_symbol"], 0))
        if weight == 0:
            cube_holdings.setdefault(holding_stock["stock_symbol"], int(holding_stock["weight"]))
        else:
            cube_holdings.setdefault(holding_stock["stock_symbol"], int(holding_stock["weight"]) + weight)
cube_holdings_rank = sorted(cube_holdings.items(), key=lambda stock: stock[1], reverse=True)
print("当前选股排名**********************************************")
print(cube_holdings_rank)



