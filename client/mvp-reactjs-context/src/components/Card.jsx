import React, { useEffect, useRef, useState } from "react";

import Item from "./Item";
import ItemEdit from "./ItemEdit";

function Card(props) {
  const [showEdit, setShowEdit] = useState(false);
  const product = props.product;

  function updateHandler(data) {
    setShowEdit(false);
    props.onUpdateSubmit(data);
  }

  function deleteHandler(data) {
    props.onDeleteSubmit(data);
  }

  return (
    <li key={product.id}>
      {!showEdit ? (
        <>
          <Item
            product={product}
            onUpdate={(val) => {
              setShowEdit(val);
            }}
          />
        </>
      ) : (
        <ItemEdit
          product={product}
          onUpdate={updateHandler}
          onDelete={deleteHandler}
          onCancel={(val) => {
            setShowEdit(val);
          }}
        />
      )}
    </li>
  );
}

export default Card;
