import React, { Component } from "react";
import {
  buyAllItems,
  depositeReset,
  depositeSave,
  login,
  productDelete,
  productNew,
  productUpdate,
  productsLoad,
  register,
} from "./apis";

import ShopContext from "./shop-context";

class GlobalState extends Component {
  constructor() {
    super();
    this.doLogin = this.doLogin.bind(this);
    this.doRegister = this.doRegister.bind(this);
    this.doLogout = this.doLogout.bind(this);
    this.doDepositeReset = this.doDepositeReset.bind(this);
    this.doBuyAllItems = this.doBuyAllItems.bind(this);
    this.doProductUpdate = this.doProductUpdate.bind(this);
    this.doProductDelete = this.doProductDelete.bind(this);
    this.doProductNew = this.doProductNew.bind(this);

    this.state = {
      products: [],
      cart: [],
      loading: true,
      token_access: "",
      token_refresh: "",
      token_csrf: "",
      first_name: "",
      last_name: "",
      username: "",
      user_type: "",
      email: "",
      image: "",
      bio: "",
      deposite: "",
    };
  }

  componentDidMount() {
    try {
      const response = this.loadProducts();
      if (!response.ok) {
        throw Error(response.statusText);
      }
    } catch (error) {
      console.log(error);
    }
  }

  loadProducts = async () => {
    try {
      const res = await productsLoad();
      this.setState({ products: res, loading: false });
      return res;
    } catch (error) {
      console.log(error);
      return "";
    }
  };

  async doProductNew(data) {
    try {
      const Bearer = this.state.token_access;
      const response = await productNew(Bearer, data);
      this.setState({
        cart: [],
      });
      await this.loadProducts();

      return response;
    } catch (error) {
      console.log(error);
      return "";
    }
  }

  async doProductUpdate(data) {
    try {
      const Bearer = this.state.token_access;
      const response = await productUpdate(Bearer, data);
      this.setState({
        cart: [],
      });
      await this.loadProducts();

      return response;
    } catch (error) {
      return "";
    }
  }

  async doProductDelete(data) {
    try {
      const Bearer = this.state.token_access;
      const response = await productDelete(Bearer, data);

      this.setState({
        cart: [],
      });
      await this.loadProducts();

      return response;
    } catch (error) {
      console.log(error);
      return "";
    }
  }

  componentDidUpdate(prevProps, prevState) {
    if (this.state.value !== prevState.value) {
      localStorage.setItem("parentValueKey", this.state.value);
    }
  }

  async doDepositeReset() {
    try {
      const Bearer = this.state.token_access;
      const response = await depositeReset(Bearer);
      return response;
    } catch (error) {
      return "";
    }
  }

  async doDepositeSave(data) {
    try {
      const Bearer = this.token_access;
      const response = await depositeSave(Bearer, data);
      return response;
    } catch (error) {
      console.log(error);
      return false;
    }
  }

  async doLogin(data) {
    try {
      const response = await login(data);

      this.setState({
        token_access: response.token.access,
        token_refresh: response.token.refresh,
        token_csrf: response.token.csrf,
        first_name: response.userprofile.first_name,
        last_name: response.userprofile.last_name,
        username: response.userprofile.username,
        user_type: response.userprofile.user_type,
        email: response.userprofile.email,
        image: response.userprofile.image,
        bio: response.userprofile.bio,
        deposite: response.userprofile.deposite,
      });

      if (response.error !== "0") {
        throw Error(response.statusText);
      } else {
        this.loadProducts();
        return response;
      }
    } catch (error) {
      console.log(error);
    }
  }

  async doLogout() {
    try {
      this.setState({
        token_access: null,
        token_refresh: null,
        token_csrf: null,
        first_name: null,
        last_name: null,
        username: null,
        useer_type: null,
        email: null,
        bio: null,
        image: null,
      });

      return this.state;
    } catch (error) {
      console.log(error);
    }
  }

  async doRegister(data) {
    try {
      const response = await register(data);

      this.setState({
        token_access: response.token.access,
        token_refresh: response.token.refresh,
        token_csrf: response.token.csrf,
        first_name: response.userprofile.first_name,
        last_name: response.userprofile.last_name,
        username: response.userprofile.username,
        user_type: response.userprofile.user_type,
        email: response.userprofile.email,
        image: response.userprofile.image,
        bio: response.userprofile.bio,
        deposite: response.userprofile.deposite,
      });

      if (response.error !== "0") {
        return response;
      } else {
        this.loadProducts();
        return response;
      }
    } catch (error) {
      console.log(error);
      return error;
    }
  }

  addProductToCart = (product) => {
    let updatedCart = [...this.state.cart];
    let updatedItemIndex = updatedCart.findIndex(
      (item) => item.id === product.id
    );

    if (updatedItemIndex < 0) {
      // if the item is not exist, push it.
      updatedCart.push({ ...product, quantity: 1 });
    } else {
      const updatedItem = { ...updatedCart[updatedItemIndex] };
      if (updatedItem.quantity + 1 <= product.amount) {
        // if the item exist, just updatet he quentity
        updatedItem.quantity++;
        updatedCart[updatedItemIndex] = updatedItem;
      }
    }
    this.setState({ cart: updatedCart });
  };

  removeProductFromCart = (productId) => {
    let updatedCart = [...this.state.cart];
    let updatedItemIndex = updatedCart.findIndex(
      (item) => item.id === productId
    );

    const updatedItem = { ...updatedCart[updatedItemIndex] };
    updatedItem.quantity--;
    if (updatedItem.quantity <= 0) {
      updatedCart.splice(updatedItemIndex, 1);
    } else {
      updatedCart[updatedItemIndex] = updatedItem;
    }

    this.setState({ cart: updatedCart });
    // setTimeout(() => {}, 700);
  };

  doBuyAllItems = async () => {
    const Bearer = this.state.token_access;

    this.state.cart.map(async (cart, index) => {
      try {
        const response = await buyAllItems(Bearer, cart);

        if (index === 0) {
          if (response) {
            this.setState({
              cart: [],
              products: [],
            });
            this.loadProducts();
            return true;
          }
        }
      } catch (error) {
        return "";
      }
    });
  };

  render() {
    if (this.state.loading) {
      return <section>Loading ......</section>;
    } else {
      return (
        <ShopContext.Provider
          value={{
            // this is the context which we declared in the products page, all the context values comes from here
            products: this.state.products,
            cart: this.state.cart,
            addProductToCart: this.addProductToCart,
            removeProductFromCart: this.removeProductFromCart,
            doLogin: this.doLogin,
            doRegister: this.doRegister,
            doLogout: this.doLogout,
            doDepositeReset: this.doDepositeReset,
            doDepositeSave: this.doDepositeSave,
            doBuyAllItems: this.doBuyAllItems,
            doProductUpdate: this.doProductUpdate,
            doProductDelete: this.doProductDelete,
            doProductNew: this.doProductNew,
            loading: this.state.loading,
            token_access: this.state.token_access,
            token_refresh: this.state.token_refresh,
            token_csrf: this.state.token_csrf,
            first_name: this.state.first_name,
            last_name: this.state.last_name,
            username: this.state.username,
            user_type: this.state.user_type,
            email: this.state.email,
            image: this.state.image,
            bio: this.state.bio,
            deposite: this.state.deposite,
          }}
        >
          {this.props.children}
        </ShopContext.Provider>
      );
    }
  }
}

export default GlobalState;
