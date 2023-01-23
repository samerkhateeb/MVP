import "./Layouts.css";

import MainNavigation from "./MainNavigation";
import React from "react";
import ShopContext from "../context/shop-context";

function Layouts(props) {
  return (
    <ShopContext.Consumer>
      {(context) => (
        <React.Fragment>
          <div>
            <MainNavigation
              cartItemNumber={context.cart.reduce((count, curItem) => {
                return count + curItem.quantity;
              }, 0)}
            />

            <main>{props.children}</main>
          </div>
        </React.Fragment>
      )}
    </ShopContext.Consumer>
  );
}

export default Layouts;
