import "bootstrap/dist/css/bootstrap.min.css";

import {
  Route,
  RouterProvider,
  createBrowserRouter,
  createRoutesFromElements,
} from "react-router-dom";

import AccountPage from "./pages/Account";
import CartPage from "./pages/Cart";
import ErrorPage from "./pages/ErrorPage";
import GlobalState from "./context/GlobalState";
import MasterPage from "./layout/Master";
import ProductsPage from "./pages/Products";
import React from "react";

const router = createBrowserRouter(
  createRoutesFromElements(
    <>
      <Route path="/" exact element={<MasterPage />} errorElement=<ErrorPage />>
        <Route index element={<ProductsPage />} errorElement=<ErrorPage /> />
        <Route path="/cart" element={<CartPage />} errorElement=<ErrorPage /> />
        <Route
          path="/account"
          element={<AccountPage />}
          errorElement=<ErrorPage />
        />
      </Route>
    </>
  )
);
const App = () => (
  <>
    <GlobalState>
      <RouterProvider router={router} />
    </GlobalState>
  </>
);

export default App;
