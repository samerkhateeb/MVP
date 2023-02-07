import "./Cart.css";

import { Alert, Button } from "react-bootstrap";
import React, { useContext, useState } from "react";
import {
  faBasketShopping,
  faRemove,
  faSubway,
} from "@fortawesome/free-solid-svg-icons";

import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import ShopContext from "../context/shop-context";

function CartPage(props) {
  const { doBuyAllItems, cart, removeProductFromCart, total } = useContext(
    ShopContext
  );
  const [alert, setAlert] = useState({});
  const submitBuyAll = async () => {
    const response = await doBuyAllItems();
    if (response) {
      setAlert({
        type: "danger",
        message:
          "Unable to proceed with payment, you should login and have sufficient fund",
      });
    } else {
      setAlert({
        type: "success",
        message: "The payment is done successfully",
      });
    }
  };
  return (
    <main className="cart">
      {cart.length <= 0 && <p>No Item in the Cart!</p>}
      <ul>
        {cart.map((cartItem) => (
          <li key={cartItem.id}>
            <div>
              <strong>{cartItem.title}</strong> - ${cartItem.cost} (
              {cartItem.quantity})
            </div>
            <div>
              <Button
                variant="primary m-2"
                type="button"
                onClick={removeProductFromCart.bind(this, cartItem.id, 1)}
              >
                <FontAwesomeIcon icon={faRemove} size="1x" />
              </Button>
            </div>
          </li>
        ))}
      </ul>
      {alert && alert.message && (
        <Alert variant={alert.type}>{alert.message}</Alert>
      )}
      {cart.length > 0 && (
        <>
          <div className="total">Total: {total}.00$ </div>
          <Button variant="primary m-2" type="button" onClick={submitBuyAll}>
            <FontAwesomeIcon icon={faBasketShopping} size="1x" /> Buy All
          </Button>
        </>
      )}
    </main>
  );
}

export default CartPage;
