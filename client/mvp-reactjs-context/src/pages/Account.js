import React, { useContext, useState } from "react";

import { Alert } from "react-bootstrap";
import DepositeComponent from "../components/DepositeComponent";
import DropDownListTopup from "../controls/DropDownListTopup";
import LoginComponent from "../components/LoginComponent";
import RegisterComponent from "../components/RegisterComponent";
import ShopContext from "../context/shop-context";
import { useNavigate } from "react-router-dom";

function AccountPage(props) {
  const navigate = useNavigate();
  const context = useContext(ShopContext);

  const [deposite, setDeposite] = useState(false);
  const [resetDeposite, setResetDeposite] = useState(context.deposite);
  async function useLoginSubmit(context, data) {
    await context.doLogin(data);
    navigate("/");
  }

  async function useRegisterSubmit(context, data) {
    const response = await context.doRegister(data);
    if (response.error !== "1") navigate("/");
  }

  async function useDepositeReset(context) {
    const response = await context.doDepositeReset();
    setDeposite(response);
    resetChildDeposite();
  }

  function resetChildDeposite() {
    setResetDeposite(0);
    context.deposite = 0;
  }

  async function useDepositSubmit(context, data) {
    await context.doDepositeSave(data);
    context.deposite = context.deposite + data.deposite;
  }

  return (
    <>
      {context.token_access ? (
        <div>
          <DropDownListTopup
            resetDeposite={resetDeposite}
            deposite={context.deposite}
            onSubmit={(data) => {
              useDepositSubmit(context, data);
            }}
          />
          {context.user_type === "1" && (
            <div>
              {deposite && (
                <Alert variant="success">
                  the deposit is reset successfully!
                </Alert>
              )}
              <DepositeComponent
                deposite={context.deposite}
                onSubmit={() => {
                  useDepositeReset(context);
                }}
              />
            </div>
          )}
        </div>
      ) : (
        <div className="card-group">
          <LoginComponent
            onSubmit={(data) => {
              useLoginSubmit(context, data);
            }}
          />

          <RegisterComponent
            onSubmit={(data) => {
              useRegisterSubmit(context, data);
            }}
          />
        </div>
      )}
    </>
  );
}

export default AccountPage;
