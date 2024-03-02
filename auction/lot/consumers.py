import json
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Lot, Bid
from channels.db import database_sync_to_async
from django.contrib.humanize.templatetags import humanize
from .tasks import email_on_bid_placed
User = get_user_model()

class BidConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.lot_id = self.scope['url_route']['kwargs']['lot_id']
        self.lot_group_name = f'lot_{self.lot_id}_bids'
        print("--------------------connected")
        print(self.lot_group_name, self.user)

        await self.channel_layer.group_add(
            self.lot_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        print("----------disconnected")
        await self.channel_layer.group_discard(
            self.lot_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        bid_amount = text_data_json['bidAmount']
        print("-----Bid Amount", bid_amount)

        lot = await self.get_lot()

        print("--------", lot)
        await self.save_bid(lot, bid_amount)

        bids = await self.get_latest_bids(lot)
        
        await self.channel_layer.group_send(
            self.lot_group_name,
            {
                'type': 'send_latest_bids',
                'latest_bids': bids
            }
        )

    async def send_latest_bids(self, event):
        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def save_bid(self, lot, bid_amount):
        bidder = self.user
        bid = Bid.objects.create(lot=lot, bidder=bidder, amount=bid_amount)
        bro = email_on_bid_placed.delay(bid.id, self.lot_id)
        print(bro)

        return bid

    @database_sync_to_async
    def get_lot(self):
        print("getting lot", self.lot_id)
        return Lot.objects.get(id=self.lot_id)


    @database_sync_to_async
    def get_latest_bids(self, lot):
        bids = lot.bids.order_by('-amount')
        latest_bids = []
        for bid in bids:
            latest_bids.append({
                'bidder': bid.bidder.get_username_display(),
                'amount': str(humanize.intcomma(bid.amount)),  # Convert to regular string
                'bidded_at': str(humanize.naturaltime(bid.bidded_at))  # Convert to regular string
            })
        print("latest bids------", latest_bids)
        return latest_bids
