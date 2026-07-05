import React, {
  createContext,
  useEffect,
  useState,
} from "react";

import {
  getMe,
  loginUser,
  registerUser,
} from "../services/api";

export const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => {
    const stored = localStorage.getItem("techmart_user");

    return stored
      ? JSON.parse(stored)
      : null;
  });

  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem("techmart_token");

    if (!token) {
      setLoading(false);
      return;
    }

    getMe()
      .then((res) => {
        setUser(res.data);

        localStorage.setItem(
          "techmart_user",
          JSON.stringify(res.data)
        );
      })
      .catch(() => {
        localStorage.removeItem("techmart_token");
        localStorage.removeItem("techmart_user");
        setUser(null);
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  const login = async (email, password) => {
    const res = await loginUser({
      email,
      password,
    });

    localStorage.setItem(
      "techmart_token",
      res.data.access_token
    );

    localStorage.setItem(
      "techmart_user",
      JSON.stringify(res.data.user)
    );

    setUser(res.data.user);

    return res.data.user;
  };

  const register = async (
    name,
    email,
    password
  ) => {
    const res = await registerUser({
      name,
      email,
      password,
    });

    localStorage.setItem(
      "techmart_token",
      res.data.access_token
    );

    localStorage.setItem(
      "techmart_user",
      JSON.stringify(res.data.user)
    );

    setUser(res.data.user);

    return res.data.user;
  };

  const logout = () => {
    localStorage.removeItem("techmart_token");
    localStorage.removeItem("techmart_user");

    setUser(null);
  };

  const updateUserLocal = (updated) => {
    setUser(updated);

    localStorage.setItem(
      "techmart_user",
      JSON.stringify(updated)
    );
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        loading,
        login,
        register,
        logout,
        updateUserLocal,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}