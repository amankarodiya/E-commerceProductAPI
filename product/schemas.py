from pydantic import BaseModel

class ProductForm(BaseModel):
    name : str
    category_name : str
    description : str
    buy_price : float
    sell_price : float
    quantity : int