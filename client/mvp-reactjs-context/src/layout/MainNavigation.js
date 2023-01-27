import "./MainNavigation.css";

import React, { useContext } from "react";

import LogoutComponent from "../components/LogoutComponent";
import { NavLink } from "react-router-dom";
import shopContext from "../context/shop-context";

// import { createStyles, makeStyles, Theme } from "@material-ui/core/styles";

function mainNavigation(props) {
  const context = useContext(shopContext);
  async function useLogoutSubmit() {
    context.doLogout();
  }

  return (
    <header className="main-navigation">
      <nav>
        <ul>
          <li>
            <NavLink to="/account">Account</NavLink>
          </li>
          <li>
            <NavLink to="/">Products</NavLink>
          </li>
          <li>
            <NavLink to="/cart">Cart ({props.cartItemNumber})</NavLink>
          </li>

          {context.token_access && context.deposite && (
            <li>
              <NavLink to="/account">Credit ${context.deposite}</NavLink>
            </li>
          )}
          {context.token_access && (
            <li>
              <LogoutComponent
                onSubmit={() => {
                  useLogoutSubmit();
                }}
              />
            </li>
          )}
        </ul>
      </nav>
    </header>
  );
}

export default mainNavigation;
