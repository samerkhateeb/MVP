import React, { useContext } from "react";

import { Button } from "react-bootstrap";
import ShopContext from "../context/shop-context";

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

        <Button
          variant="primary w-100"
          type="button"
          onClick={context.addProductToCart.bind(this, product)}
        >
          Add Item
        </Button>
        {product.seller.username === context.username && context.token_access && (
          <Button
            variant="primary m-2"
            onClick={() => {
              updateHandler(true);
            }}
          >
            Edit Product
          </Button>
        )}
      </div>
    </>
  );
}

export default Item;
