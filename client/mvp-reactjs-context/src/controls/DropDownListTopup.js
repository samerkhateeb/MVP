import "./dropdownList.css";

import { Alert, Button } from "react-bootstrap";
import React, { useContext, useEffect, useState } from "react";

import ShopContext from "../context/shop-context";

class DropDownListTopup extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      open: false,
      deposite: props.deposite,
      error: false,
    };
  }

  static contextType = ShopContext;

  componentDidMount() {}

  handleOpen = () => {
    const open = !this.state.open;
    this.setState({ open: open });
  };

  componentWillReceiveProps(props) {
    this.setState({ deposite: props.resetDeposite });
  }

  submitHandler = (_deposit) => {
    const context = this.context;

    this.setState({ open: false });
    if (context.user_type === "2") this.setState({ error: true });
    else {
      const vdeposite = this.state.deposite + _deposit;
      this.setState({ deposite: vdeposite });

      const data = {
        deposite: _deposit,
      };
      this.props.onSubmit(data);
    }
  };

  render() {
    return (
      <>
        {this.state.error && (
          <Alert variant="danger">
            Buyers only can Topup their account, please ask the admin to make
            your account as a Buyer
          </Alert>
        )}
        <Dropdown
          open={this.state.open}
          trigger={
            <Button
              variant="primary m-2"
              type="button"
              onClick={this.handleOpen}
            >
              Topup Credit?
            </Button>
          }
          menu={[
            <button onClick={this.submitHandler.bind(this, 5)}>Topup 5</button>,
            <button onClick={this.submitHandler.bind(this, 10)}>
              Topup 10
            </button>,
            <button onClick={this.submitHandler.bind(this, 20)}>
              Topup 20
            </button>,
            <button onClick={this.submitHandler.bind(this, 50)}>
              Topup 50
            </button>,
            <button onClick={this.submitHandler.bind(this, 100)}>
              Topup 100
            </button>,
          ]}
        />
      </>
    );
  }
}

const Dropdown = ({ open, trigger, menu }) => {
  return (
    <div className="dropdown">
      {trigger}
      {open ? (
        <ul className="menu">
          {menu.map((menuItem, index) => (
            <li key={index} className="menu-item">
              {menuItem}
            </li>
          ))}
        </ul>
      ) : null}
    </div>
  );
};

export default DropDownListTopup;
