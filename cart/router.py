from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from config.database import get_db
from user.helpers import get_current_user
from payment.router import Initialize_Payment
from products.models import Products
from . import models, schemas
from typing import List


router = APIRouter(prefix="/ap1/v1/cart", tags=["cart"])

cart = {}


@router.post(
    "/add_to_cart",
)
async def add_to_cart(
    item: List[schemas.CartItem],
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # what i did here is collect the product id and quantity as a list,
    # loop through the list,
    # calculate the total price
    # then add a single object to the cart model that return an id to be used in checkout
    for product in item:
        if product.product_id in cart:
            cart[product.product_id] += product.quantity
        else:
            cart[product.product_id] = product.quantity

    total_price = 0
    for product_id, quantity in cart.items():
        single_product = db.query(Products).filter(Products.id == product_id).first()
        price_per_unit = single_product.price
        total_price += price_per_unit * quantity
    save = models.Cart(user=user.id, amount=total_price)
    db.add(save)
    db.commit()
    db.refresh(save)

    cart_items = []
    for pros in item:
        sing_product = db.query(Products).filter(Products.id == pros.product_id).first()
        cart_item_obj = models.CartItems(
            user=user.id,
            name=sing_product.name,
            checkout_id=save.id,
            price=sing_product.price,
            product_id=sing_product.id,
        )
        cart_items.append(cart_item_obj)

    db.add_all(cart_items)
    db.commit()
    cart.clear()
    return {"checkout_id": save.id, "cart": cart, "cart_items": cart_items}


@router.post("/checkout")
async def checkout(
    product_id: str,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # filter through the model and get the checkout object just created
    # this way the checkout object is always stored for the user to see and buy anytime
    checkout_obj = (
        db.query(models.Cart)
        .filter(
            models.Cart.user == user.id,
            models.Cart.id == product_id,
            models.Cart.is_paid == False,
        )
        .order_by(models.Cart.created_at.desc())
        .first()
    )

    total_price = checkout_obj.amount
    pay = await Initialize_Payment(amount=total_price, user=user)

    return {"pay": pay, "cart": cart, "price": total_price}


@router.get("/user/cart-items")
async def get_all_user_cart_items(
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    items = db.query(models.CartItems).filter(models.CartItems.user == user.id).order_by(models.CartItems.created_at.desc()).all()
    return items


@router.get("/user/checkouts")
async def get_all_user_checkouts(
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    items = db.query(models.Cart).filter(models.Cart.user == user.id).order_by(models.Cart.created_at.desc()).all()
    return items