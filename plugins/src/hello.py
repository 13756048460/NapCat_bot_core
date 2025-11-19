import requests

from api import send_group_msg, send_group_forward_msg
from logs import Logger

async def ra3(msg:dict , websocket):
    if msg.get("message_type") != "group":
        Logger().debug("非群消息")
        return
    if msg.get("raw_message") == "战网数据":
        group_id = msg.get("group_id")
        API_URL = "http://api.ra3battle.cn/api/server/status"
        try:
            getJson = requests.get(API_URL)
            getJson.raise_for_status()  # 添加异常处理
        except requests.RequestException as e:
            msg = f"API请求失败: {e}"
            await send_group_msg(websocket, group_id, msg)
        data = getJson.json()  # 简化变量名
        players = len(data["players"])
        if not data["players"] and not data["games"]:
            msg = f"根据api获取json为\n-------------------\n{data}\n-------------------\n获取players和games内的数据为空\n疑似战网崩溃或战网内暂无玩家\n如崩溃则联系战网管理"
            await send_group_msg(websocket, group_id, msg)
        Total = data["games"]
        total_players = sum(len(game["players"]) for game in Total)
        Idle_player = players - total_players
        count1v1D = data['automatching']['count1v1Details']
        count1v1 = count1v1D.get('ra3', 0)
        count1v1R = count1v1D.get('corona', 0)
        mate_room = str(len(data["automatch"]))
        closed_playing_count = sum(1 for game in Total if game["gamemode"] == 'closedplaying')
        preparing_games = len(Total) - closed_playing_count
        msg = (
            "房间详细数据请发送\"房间数据\"\n"
            "--------------------\n"
            f"当前在线人数：{players}\n"
            f"正在对局玩家：{total_players}\n"
            f"闲置玩家：{Idle_player}\n"
            "--------------------\n"
            f"自动匹配寻找对局的玩家：{count1v1}\n"
            f"日冕自动匹配寻找对局的玩家：{count1v1R}\n"
            "--------------------\n"
            f"正在进行匹配对战的房间总数：{mate_room}\n"
            f"正在进行游戏的房间个数：{closed_playing_count}\n"
            f"正在准备的房间个数：{preparing_games}\n"
            "--------------------"
        )
        await send_group_msg(websocket, group_id, msg)
        
async def room_data(msg:dict , websocket):
    if msg.get("message_type") == "group":
        Logger().debug("非群消息")
    if msg.get("raw_message") == "房间数据":
        group_id = msg.get("group_id")
        url = "https://api.ra3battle.cn/api/server/status"
        req = requests.get(url)
        games = req.json()["games"]
        data = []
        homeSum = 0
        for game in games:
            if game["gamemode"] == "openstaging":
                homeSum += 1
                if not game["players"]:
                    names = "NUll"
                else :
                    names = game["players"][0]["name"]
                homeName = game["hostname"].split()[1]
                modName = game["mod"]
                if modName == "RA3":
                    modName = "原版"
                if modName == "corona":
                    modName = "日冕"
                mapName = game["mapname"].replace("\\", "/").split("/")
                mapName = mapName.pop().split(".")[0]
                data.append(
                    "房间名：" + homeName + "\n" + "地图名：" + mapName + "\n" + "房主名：" + names + "\n" + "MOD名：" + modName + "\n" + "房间内人数：" + str(len(
                        game["players"])) +"\n"+"------------------------------"+"\n")
        out = ''.join(data)
        textT = "正在准备的房间数：" + str(homeSum) + "\n" + "------------------------------" + "\n"
        message = textT + out
        messages = [
            {
                "type": "node",
                "data": {
                    "user_id": "1549184870",
                    "nickname": "qwq",
                    "content": [
                        {
                            "type": "text",
                            "data": {
                                "text": message
                            }
                        }
                    ]
                }
            }
        ]
        await send_group_forward_msg(websocket,group_id,messages,"房间数据","点击查看","房间数据")

# async def at(msg:dict , websocket):
