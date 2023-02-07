import Card from "react-bootstrap/Card";
import React from "react";

const Wallet = ({ deposit, index = 0 }) => {
  let _depo = 0;

  if (deposit >= 100) _depo = 100;
  else if (deposit >= 50) _depo = 50;
  else if (deposit >= 20) _depo = 20;
  else if (deposit >= 10) _depo = 10;
  else if (deposit >= 5) _depo = 5;
  else _depo = deposit;

  deposit -= _depo;

  return (
    <>
      {_depo > 0 && (
        <>
          <Card
            bg={"light"}
            key={"light"}
            text={"light" === "light" ? "dark" : "white"}
            style={{ width: "11.6rem", height: "10rem", float: "left" }}
            className="m-2"
          >
            <Card.Body>
              <Card.Title> {_depo}€</Card.Title>
              <Card.Text>
                <img
                  alt={_depo}
                  width={100}
                  src={require(`../assets/img/Euro_${
                    _depo < 5 ? 1 : _depo
                  }.jpg`)}
                />
              </Card.Text>
            </Card.Body>
          </Card>

          <Wallet deposit={deposit} index={index + 1} />
        </>
      )}
    </>
  );
};

export default Wallet;
