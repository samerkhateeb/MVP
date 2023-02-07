import React, { useContext } from "react";
import {
  faCartShopping,
  faEdit,
  faPlus,
} from "@fortawesome/free-solid-svg-icons";

import { Button } from "react-bootstrap";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import ShopContext from "../context/shop-context";

// <-- import styles to be used

// <-- import styles to be used

function Item(props) {
  const product = props.product;
  const context = useContext(ShopContext);

  function updateHandler(val) {
    props.onUpdate(val);
  }

  return (
    <>
      <div className="left">
        <img alt={product.title} src={product.image} />
        <div>
          <strong className="title">{product.title}</strong>
          <div className="description">{product.description}</div>
          <div className="description">Amount: {product.amount}</div>
          <div className="description">Seller: {product.seller.name}</div>
        </div>
      </div>
      <div>
        <div className="price">{product.cost}$</div>
        {product.seller.username === context.username && context.token_access && (
          <>
            <Button
              variant="primary m-1"
              onClick={() => {
                updateHandler(true);
              }}
            >
              <FontAwesomeIcon icon={faEdit} size="1x" />
            </Button>
          </>
        )}
        {/* <FontAwesomeIcon icon={faEnvelope} /> */}

        <Button
          variant="primary w-70"
          type="button"
          onClick={context.addProductToCart.bind(this, product)}
        >
          <FontAwesomeIcon icon={faCartShopping} size="1x" />
          <FontAwesomeIcon icon={faPlus} size="1x" />
        </Button>
      </div>
    </>
  );
}

export default Item;
