import React, { useEffect, useState } from "react";

import { Button } from "react-bootstrap";
import InputField from "../controls/InputField";

function ItemEdit(props) {
  const [title, setTitle] = useState("");
  const [cost, setCost] = useState("");
  const [description, setDescription] = useState("");
  const [amount, setAmount] = useState("");

  const updateHandler = (e) => {
    e.preventDefault();

    const product_data = {
      id: props.product.id,
      title: title,
      description: description,
      cost: cost,
      amount: amount,
    };

    const data = product_data;
    props.onUpdate(data);
  };

  function deleteHandler(e) {
    e.preventDefault();
    const product_data = {
      id: props.product.id,
    };
    const data = product_data;
    props.onDelete(data);
  }

  useEffect(() => {
    setTitle(props.product.title);
    setDescription(props.product.description);
    setCost(props.product.cost);
    setAmount(props.product.amount);
  }, []);

  return (
    <div>
      <form onSubmit={updateHandler}>
        <InputField title="Title" value={title} onChange={setTitle} />
        <InputField
          title="Description"
          value={description}
          small="Description field should describe your product details like the size  of the product and the status of the product is it new or not"
          onChange={setDescription}
        />
        <InputField title="Cost $$" value={cost} onChange={setCost} />
        <InputField title="Amount" value={amount} onChange={setAmount} />
        <Button variant="primary m-2" type="submit">
          Save
        </Button>
        <Button
          variant="primary m-2"
          onClick={(e) => {
            e.preventDefault();
            props.onCancel(false);
          }}
        >
          Cancel
        </Button>
      </form>
      <form onSubmit={deleteHandler}>
        <Button type="submit" variant="primary m-2">
          Delete
        </Button>
      </form>
    </div>
  );
}

export default ItemEdit;
