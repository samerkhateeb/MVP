import React, { useEffect, useState } from "react";

import { Button } from "react-bootstrap";
import FileUploadSingle from "../controls/FileUploadSingle";
import InputField from "../controls/InputField";

function ItemEdit(props) {
  const [title, setTitle] = useState("");
  const [cost, setCost] = useState("");
  const [description, setDescription] = useState("");
  const [amount, setAmount] = useState("");
  const [images, setImages] = useState("");

  const updateHandler = (e) => {
    e.preventDefault();

    let data = new FormData();

    data.append("id", props.product.id);
    data.append("title", title);
    data.append("description", description);
    data.append("cost", cost);
    data.append("amount", amount);
    if (images) data.append("image", images, images.name);

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
        <FileUploadSingle title="Image" onChange={setImages} />

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
