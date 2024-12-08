"""_summary_
    """

from pydantic import BaseModel


class Order(BaseModel):
    """_summary_

    Args:
        BaseModel (_type_): _description_
    """

    order_id: str
    status: str
    channel: str
