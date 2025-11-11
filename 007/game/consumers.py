# game/consumers.py (새로 생성)
import json
from channels.generic.websocket import AsyncWebsocketConsumer


class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "game_room"

        # 그룹에 참가
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

        # 접속 메시지 전송
        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "player_joined", "player_id": self.channel_name},
        )

    async def disconnect(self, close_code):
        # 그룹에서 나가기
        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "player_left", "player_id": self.channel_name},
        )

        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # 클라이언트로부터 메시지 수신
    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get("type")

        if message_type == "player_move":
            # 플레이어 이동 정보를 모든 클라이언트에게 브로드캐스트
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "player_position",
                    "player_id": self.channel_name,
                    "x": data.get("x"),
                    "z": data.get("z"),
                    "color": data.get("color"),
                },
            )
        elif message_type == "item_collected":
            # 아이템 수집 정보를 모든 클라이언트에게 브로드캐스트
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "item_removed",
                    "item_id": data.get("item_id"),
                    "player_id": self.channel_name,
                    "score": data.get("score"),
                },
            )

    # 플레이어 위치 업데이트
    async def player_position(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "type": "player_position",
                    "player_id": event["player_id"],
                    "x": event["x"],
                    "z": event["z"],
                    "color": event["color"],
                }
            )
        )

    # 플레이어 참가
    async def player_joined(self, event):
        await self.send(
            text_data=json.dumps(
                {"type": "player_joined", "player_id": event["player_id"]}
            )
        )

    # 플레이어 나감
    async def player_left(self, event):
        await self.send(
            text_data=json.dumps(
                {"type": "player_left", "player_id": event["player_id"]}
            )
        )

    # 아이템 제거
    async def item_removed(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "type": "item_removed",
                    "item_id": event["item_id"],
                    "player_id": event["player_id"],
                    "score": event["score"],
                }
            )
        )
