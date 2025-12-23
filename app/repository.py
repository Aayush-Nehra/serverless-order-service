import boto3
import uuid
from datetime import datetime
from app.schemas import OrderCreate
from decimal import Decimal
import botocore.exceptions

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("Orders")


class OrderRepository:

    def create_order(self, order: OrderCreate):
        order_id = str(uuid.uuid4())
        item = {
            "order_id": order_id,
            "user_id": order.user_id,
            "amount": Decimal(str(order.amount)),
            "status": "CREATED",
            "created_at": datetime.utcnow().isoformat(),
        }
        try:
            table.put_item(Item=item)
        except botocore.exceptions.BotoCoreError as e:
            raise Exception(f"Failed to create order: {e}")
        return item

    def get_order(self, order_id: str):
        try:
            resp = table.get_item(Key={"order_id": order_id})
        except botocore.exceptions.BotoCoreError as e:
            raise Exception(f"Failed to get order: {e}")
        return resp.get("Item")
