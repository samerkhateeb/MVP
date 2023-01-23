import axios from "axios";
let serverUrl = "http://127.0.0.1:8000";

export async function productsLoad() {
  const headers = {
    "Content-Type": "application/json",
  };
  const response = await axios
    .get(`${serverUrl}/api/products/`, null, {
      headers,
    })
    .then((res) => {
      return res.data;
    })
    .then((json) => {
      return json.context;
    })
    .catch((err) => {
      throw {
        message: `Failed....${err}`,
        status: 500,
      };
    });
  return response;
}

export async function productNew(Bearer, data) {
  const headers = {
    "Content-Type": "application/json",
    Authorization: `Bearer ${Bearer}`,
  };
  const response = axios
    .post(`${serverUrl}/api/products/new/`, JSON.stringify(data), {
      headers,
    })
    .then((res) => {
      return res;
    })
    .catch((err) => {
      throw {
        message: `Failed....${err}`,
        status: 500,
      };
    });

  return response;
}

export async function productUpdate(Bearer, data) {
  const headers = {
    "Content-Type": "application/json",
    Authorization: `Bearer ${Bearer}`,
  };
  const response = axios
    .put(`${serverUrl}/api/products/manage/${data.id}`, JSON.stringify(data), {
      headers,
    })
    .then((res) => {
      return res;
    })
    .catch((err) => {
      throw {
        message: `Failed....${err}`,
        status: 500,
      };
    });

  return response;
}

export async function productDelete(Bearer, data) {
  const headers = {
    "Content-Type": "application/json",
    Authorization: `Bearer ${Bearer}`,
  };
  const response = axios
    .delete(`${serverUrl}/api/products/manage/${data.id}`, {
      headers,
    })
    .then((res) => {
      return res;
    })
    .catch((err) => {
      throw {
        message: `Failed....${err}`,
        status: 500,
      };
    });

  return response;
}

export async function depositeReset(Bearer) {
  const headers = {
    "Content-Type": "application/json",
    Authorization: `Bearer ${Bearer}`,
  };

  const response = axios
    .put(`${serverUrl}/api/auth_user/reset/`, {
      headers,
    })
    .then((res) => {
      return res;
    })
    .catch((err) => {
      throw {
        message: `Failed....${err}`,
        status: 500,
      };
    });

  return response;
}

export async function depositeSave(Bearer, data) {
  const headers = {
    "Content-Type": "application/json",
    Authorization: `Bearer ${Bearer}`,
  };

  const response = axios
    .put(`${serverUrl}/api/auth_user/deposite/`, JSON.stringify(data), {
      headers,
    })
    .then((res) => {
      return res;
    })
    .catch((err) => {
      throw {
        message: `Failed....${err}`,
        status: 500,
      };
    });

  return response;
}

export async function login(data) {
  const headers = {
    method: "POST",
    body: JSON.stringify(data),
    headers: {
      "Content-Type": "application/json",
    },
  };
  const response = await fetch(`${serverUrl}/api/auth_user/login/`, headers)
    .then((res) => res.json())
    .then((json) => {
      if (json.error != "0") {
        throw Error(json);
      } else {
        return json.context;
      }
    });

  return response;
}

export async function register(data) {
  const headers = {
    method: "POST",
    body: JSON.stringify(data),
    headers: {
      "Content-Type": "application/json",
    },
  };
  const response = await fetch(`${serverUrl}/api/auth_user/register/`, headers)
    .then((res) => res.json())
    .then((json) => {
      if (json.error != "0") {
        throw Error(json);
      } else {
        return json.context;
      }
    });

  return response;
}

export async function buyAllItems(Bearer, cart) {
  const headers = {
    "Content-Type": "application/json",
    Authorization: `Bearer ${Bearer}`,
  };

  const response = await axios
    .put(`${serverUrl}/api/products/buy/${cart.id}/${cart.quantity}/`, null, {
      headers,
    })
    .then((res) => {
      return res;
    })

    .catch((err) => {
      let error = "";
      if ((err.response.data.error = null))
        error = err.response.data.code + err.response.data.detail;
      else error = err.response.data.error;
      throw Error(error);
    });
  return response;
}
