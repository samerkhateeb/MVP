import "./Cart.css";

import { Alert, Button } from "react-bootstrap";
import React, { useContext, useState } from "react";

import ShopContext from "../context/shop-context";

function CartPage(props) {
  const context = useContext(ShopContext);
  const [error, setError] = useState();
  const submitBuyAll = async () => {
    const response = await context.doBuyAllItems();
    if (response)
      setError(
        "Unable to proceed with payment, you should login and have sufficient fund"
      );
  };
  return (
    <main className="cart">
      {context.cart.length <= 0 && <p>No Item in the Cart!</p>}
      <ul>
        {context.cart.map((cartItem) => (
          <li key={cartItem.id}>
            <div>
              <strong>{cartItem.title}</strong> - ${cartItem.price} (
              {cartItem.quantity})
            </div>
            <div>
              <Button
                variant="primary m-2"
                type="button"
                onClick={context.removeProductFromCart.bind(this, cartItem.id)}
              >
                Remove from Cart
              </Button>
            </div>
          </li>
        ))}
      </ul>
      {error && <Alert variant="danger">{error}</Alert>}
      {context.cart.length > 0 && (
        <Button variant="primary m-2" type="button" onClick={submitBuyAll}>
          Buy All
        </Button>
      )}
    </main>
  );
}

export default CartPage;
