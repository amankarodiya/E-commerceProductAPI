from http.client import NO_CONTENT, NOT_FOUND, NotConnected
from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import schemas, models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
app = FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

result = {
    "status": "success"
}

@app.post('/POST/api/products', status_code=status.HTTP_201_CREATED)
def create(request: schemas.ProductForm, db: Session = Depends(get_db)):
    new_product = models.ProductInfo(name=request.name, category_name=request.category_name, 
                               description=request.description, buy_price=request.buy_price,
                                   sell_price=request.sell_price, quantity=request.quantity)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


@app.delete('/DELETE/api/products/{product_id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(product_id, db:Session = Depends(get_db)):
    product = db.query(models.ProductInfo).filter(models.ProductInfo.id == product_id)
    if not product.first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'status':'failure', 'reason':f'This id {product_id} does not exist.'})

    product.delete(synchronize_session=False)

    db.commit()
    return result

@app.put('/PUT/api/products/{product_id}', status_code=status.HTTP_202_ACCEPTED)
def update(product_id, request: schemas.ProductForm, db: Session = Depends(get_db)):
    product = db.query(models.ProductInfo).filter(models.ProductInfo.id == product_id)
    if not product.first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'status':'failure', 'reason':f'The id {product_id} which you want to update does not exist.'})

    product.update({'name':'updated name'}, {"category_name": "updated category_name"}, {"description": "updated description"}, {"buy_price": "updated buy_price"},
                         {"sell_price": "updated sell_price"}, {"quantity": "updated quantity"})

    db.commit()
    return result

@app.get('/GET/api/products/{product_id}', status_code=200)
def show(product_id, response: Response, db: Session = Depends(get_db)):
    product = db.query(models.ProductInfo).filter(models.ProductInfo.id == product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'status':'failure', 'reason':f'This id {product_id} has no data available.'})
    return product