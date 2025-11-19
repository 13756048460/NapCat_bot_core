
import json
import asyncio
from logs import Logger


async def send_group_msg(websocket, group_id, message):
    """
    发送群消息
    :param websocket:
    :param group_id:
    :param message:
    :return:
    """
    json_msg = {
        "action": "send_group_msg",
        "params": {
            "group_id": group_id,
            "message": [
                {
                    "type": "text",
                    "data": {
                        "text": message
                    }
                }
            ]
        }
    }
    await websocket.send(json.dumps(json_msg))
    Logger().info("发送群消息:%s,群号:%s"%(message,group_id))
    await asyncio.sleep(1)
    Logger().info("发送群消息请求成功")
    
async def send_private_msg(websocket, user_id, message):
    """
    发送私聊消息
    :param websocket:
    :param user_id:
    :param message:
    :return:
    """
    json_msg={
        "action": "send_private_msg",
        "params": {
            "user_id": user_id,
            "message": [
                {
                    "type": "text",
                    "data": {
                        "text": message
                    }
                }
            ]
        }
    }
    await websocket.send(json.dumps(json_msg))
    Logger().info("发送私聊文本:%s,用户:%s"%(message,user_id))
    await asyncio.sleep(1)
    Logger().info("发送私聊文本请求成功")
    
async def send_group_forward_msg(websocket, group_id, message,source,news,prompt):
    """
    发送群转发构造消息
    :param websocket:websocket
    :param group_id:group_id
    :param message:message
    :param source:标题信息
    :param news:下方小标题信息
    :param prompt:主页面信息
    :return:
    """
    json_msg={
        "action": "send_group_forward_msg",
        "params": {
            "group_id": group_id,
            "message": message,
            "news": [
                {
                    "text": news
                }
            ],
            "prompt": prompt,
            "summary": "summary",
            "source": source
        }
    }
    await websocket.send(json.dumps(json_msg))
    Logger().info("构造群转发消息发送成功:%s,群聊:%s"%(message,group_id))
    await asyncio.sleep(1)
    Logger().info("构造群转发消息请求成功")

# async def send_group_poke(websocket, user_id,group_id,target_id):
    # """
    # 发送群戳一戳
    # 不受支持的api
    # :param websocket:websocket
    # :param user_id:user_id
    # :param group_id:group_id 群
    # :param target_id:戳一戳对象
    # :return:
    # """
    # json_msg={
    #     "user_id": user_id,
    #     "group_id": group_id,
    #     "target_id": target_id
    # }
    # await websocket.send(json.dumps(json_msg))
    # Logger().info("群戳一戳发送成功:%s,群聊:%s"%(target_id,group_id))
    # await asyncio.sleep(1)
    # Logger().info("群戳一戳消息请求成功")
async def send_group_msg_at(websocket, group_id, user_id):
    """
    发送群消息at
    :param websocket:
    :param group_id:
    :param user_id:
    :return:
    """
    json_msg={
        "action": "send_private_msg",
        "params": {
            "user_id": group_id,
            "message": [
                {
                    "type": "at",
                    "qq": user_id
                }
            ]
        }
    }
    await websocket.send(json.dumps(json_msg))
    Logger().info("发送群at消息:[qq:%s],群号:%s"%(user_id,group_id))
    await asyncio.sleep(1)
    Logger().info("发送群消息请求成功")