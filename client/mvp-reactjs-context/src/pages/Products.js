import "./Products.css";

import React, { useContext, useState } from "react";
import {
  faCancel,
  faCirclePlus,
  faSave,
} from "@fortawesome/free-solid-svg-icons";

import { Button } from "react-bootstrap";
import Card from "../components/Card";
import FileUploadSingle from "../controls/FileUploadSingle";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import InputField from "../controls/InputField";
import ShopContext from "../context/shop-context";

// import { connect } from "react-redux";
function ProductsPage(props) {
  const context = useContext(ShopContext);
  const [newPanel, setNewPanel] = useState();
  const [title, setTitle] = useState("");
  const [cost, setCost] = useState("");
  const [description, setDescription] = useState("");
  const [amount, setAmount] = useState("");
  const [images, setImages] = useState();

  const updateHandler = (data) => {
    context.doProductUpdate(data);
  };
  const deleteHandler = async (data) => {
    setNewPanel(false, () => {});
    await context.doProductDelete(data);
  };

  const resetNewPanel = () => {
    setNewPanel(false);
    setTitle("");
    setCost("");
    setDescription("");
    setAmount("");
  };

  const newHandler = (e) => {
    e.preventDefault();

    const data = new FormData();
    data.append("title", title);
    data.append("description", description);
    data.append("cost", cost);
    data.append("amount", amount);
    if (images) data.append("images", images, images.name);
    data.append("category", 3);
    resetNewPanel();

    context.doProductNew(data);
  };
  return (
    <>
      <main className="products">
        {context.token_access && context.user_type === "2" && (
          <div>
            <Button
              as="a"
              variant="primary"
              onClick={() => {
                setNewPanel(true);
              }}
            >
              <FontAwesomeIcon icon={faCirclePlus} size="1x" /> New Product
            </Button>

            {newPanel && (
              <div>
                <form onSubmit={newHandler}>
                  <InputField title="Title" value={title} onChange={setTitle} />
                  <InputField
                    title="Description"
                    value={description}
                    small="Description field should describe your product details like the size  of the product and the status of the product is it new or not"
                    onChange={setDescription}
                  />
                  <InputField title="Cost $$" value={cost} onChange={setCost} />
                  <InputField
                    title="Amount"
                    value={amount}
                    onChange={setAmount}
                  />
                  <FileUploadSingle title="Image" onChange={setImages} />

                  <Button variant="primary m-2" type="submit">
                    <FontAwesomeIcon icon={faSave} size="1x" /> Save
                  </Button>
                  <Button
                    variant="primary m-2"
                    type="button"
                    onClick={(e) => {
                      setNewPanel(false);
                    }}
                  >
                    <FontAwesomeIcon icon={faCancel} size="1x" /> Cancel
                  </Button>
                </form>
              </div>
            )}
          </div>
        )}
        <ul>
          {context.products.map((product) => (
            <Card
              product={product}
              context={context}
              onUpdateSubmit={(data) => {
                updateHandler(data);
              }}
              onDeleteSubmit={(data) => {
                deleteHandler(data);
              }}
            />
          ))}
        </ul>
      </main>
    </>
  );
}

// const mapStateToProps = (state) => {
//   return {
//     products: state.products,
//     cartItemCount: state.cart.reduce((count, curItem) => {
//       return count + curItem.quantity;
//     }, 0),
//   };
// };

// const mapDispatchToProps = (dispatch) => {
//   return {
//     addProductToCart: (product) => dispatch(addProductToCart(product)),
//   };
// };

// // connect the component with the global redux store
// export default connect(
//   mapStateToProps,
//   mapDispatchToProps
// )(ProductsPage);

export default ProductsPage;
