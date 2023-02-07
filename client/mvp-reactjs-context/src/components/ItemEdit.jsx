import React, { useEffect, useState } from "react";
import { faCancel, faSave, faTrash } from "@fortawesome/free-solid-svg-icons";

import { Button } from "react-bootstrap";
import FileUploadSingle from "../controls/FileUploadSingle";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
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
    if (images) data.append("images", images, images.name);

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
      <form onSubmit={deleteHandler} className="right">
        <Button type="submit" variant="primary m-2">
          <FontAwesomeIcon icon={faTrash} size="1x" />
        </Button>
      </form>

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

        <Button variant="primary " type="submit">
          <FontAwesomeIcon icon={faSave} size="1x" /> Save
        </Button>
        <Button
          variant="primary m-2"
          onClick={(e) => {
            e.preventDefault();
            props.onCancel(false);
          }}
        >
          <FontAwesomeIcon icon={faCancel} size="1x" /> Cancel
        </Button>
      </form>
    </div>
  );
}

export default ItemEdit;
