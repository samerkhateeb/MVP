import React, { useContext, useState } from "react";

import { Alert } from "react-bootstrap";
import Button from "react-bootstrap/Button";
import Card from "react-bootstrap/Card";
import DepositeComponent from "../components/DepositeComponent";
import DropDownListTopup from "../controls/DropDownListTopup";
import LoginComponent from "../components/LoginComponent";
import RegisterComponent from "../components/RegisterComponent";
import ShopContext from "../context/shop-context";
import Wallet from "../components/Wallet";
import { useNavigate } from "react-router-dom";

function AccountPage(props) {
  const navigate = useNavigate();
  const context = useContext(ShopContext);
  const [error, setError] = useState({ error: "", message: "" });
  const [messageRegister, setMessageRegister] = useState();
  let {
    deposite,
    doRegister,
    doLogin,
    doDepositeReset,
    doDepositeSave,
    token_access,
    user_type,
  } = useContext(ShopContext);

  const [depositeS, setDeposite] = useState({});
  const [resetDeposite, setResetDeposite] = useState(deposite);

  async function useLoginSubmit(context, data) {
    const response = await doLogin(data);
    if (response === "error") {
      setError({
        error: "1",
        message: "Error in login, please check your credentials",
      });
    } else {
      setError({
        error: "",
        message: "",
      });
      navigate("/");
    }
  }

  async function useRegisterSubmit(context, data) {
    const response = await doRegister(data);
    if (response.error === "1") {
      setMessageRegister(null);
      setMessageRegister(
        "there's an error in the registration, make sure you put unique information, try again !!"
      );
    } else navigate("/");
  }

  async function useDepositeReset() {
    await doDepositeReset();
    setDeposite({
      message:
        "Your process is done Successfully!! You Can Topup Again from the Topup Section, Thanks For Using Our Services",
    });
    changeChildDeposite(0);
  }

  function changeChildDeposite(value) {
    setResetDeposite(value);
    deposite = value;
  }

  async function useDepositSubmit(data) {
    deposite = await doDepositeSave(data);

    changeChildDeposite(deposite);
  }

  return (
    <>
      {depositeS.message && (
        <Alert variant="success">{depositeS.message}</Alert>
      )}
      {error.error && <Alert variant="danger">{error.message}</Alert>}

      {token_access ? (
        <div>
          <Card className="text-center">
            <Card.Header>Topup</Card.Header>
            <Card.Body>
              <Card.Title>Your Credit is {deposite} € Topup Now !!</Card.Title>
              <Card.Text>
                With support of our team, we offer you to Topup your account for
                Free, and you can buy a goods for free from our machine !
              </Card.Text>
              <DropDownListTopup
                resetDeposite={resetDeposite}
                deposite={deposite}
                onSubmit={(data) => {
                  useDepositSubmit(data);
                }}
              />
            </Card.Body>
            <Card.Footer className="text-muted">2 days ago</Card.Footer>
          </Card>
          {user_type === "1" && ( // Buyers
            <>
              {deposite > 0 && ( // Wallet
                <Card className="text-center mt-2">
                  <Card.Header>Wallet</Card.Header>
                  <Card.Body>
                    <Card.Title>Your Change, Withdraw ? </Card.Title>
                    <Card.Text>
                      you can withdraw your change anytime, you will take the
                      money based based on the coins shows down below, Withdraw?
                    </Card.Text>
                    <DepositeComponent
                      deposite={deposite}
                      text="Withdraw Money"
                      onSubmit={() => {
                        useDepositeReset();
                      }}
                    />
                    <div>
                      <Wallet deposit={deposite} />
                    </div>
                  </Card.Body>
                  <Card.Footer className="text-muted">
                    Withdraw Money
                  </Card.Footer>
                </Card>
              )}

              <Card className="bg-dark text-white p-5 text-center mt-2">
                <Card.Title>Reset Your Deposite</Card.Title>
                <Card.Text>
                  Would you like to reset your deposite? warning !! this Process
                  cannot be undone !
                </Card.Text>
                <DepositeComponent
                  deposite={deposite}
                  onSubmit={() => {
                    useDepositeReset();
                  }}
                />

                <Card.Text>Last updated 3 mins ago</Card.Text>
              </Card>
            </>
          )}
        </div>
      ) : (
        // Sellers
        <div className="card-group">
          <LoginComponent
            onSubmit={(data) => {
              useLoginSubmit(context, data);
            }}
          />

          <RegisterComponent
            message={messageRegister}
            onSubmit={(data) => {
              useRegisterSubmit(context, data);
            }}
            onReset={() => {
              setMessageRegister(null);
            }}
          />
        </div>
      )}
    </>
  );
}

export default AccountPage;
