import boto3
import uuid
from datetime import datetime
from app.schemas import OrderCreate
from decimal import Decimal

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
            "created_at": datetime.utcnow().isoformat()
        }

        table.put_item(Item=item)
        return item

    def get_order(self, order_id: str):
        resp = table.get_item(Key={"order_id": order_id})
        return resp.get("Item")
