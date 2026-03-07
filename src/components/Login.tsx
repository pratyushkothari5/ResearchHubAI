import React, { useState } from "react";
import { register, login } from "../api";

interface Props {
  onLogin: (token: string) => void;
}

const Login: React.FC<Props> = ({ onLogin }) => {
  const [isRegister, setIsRegister] = useState(false);
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async () => {
    setError("");
    try {
      if (isRegister) {
        await register(username, email, password);
        setIsRegister(false);
        alert("Registered! Please login.");
      } else {
        const data = await login(username, password);
        localStorage.setItem("token", data.access_token);
        onLogin(data.access_token);
      }
    } catch (e: any) {
      setError(e.response?.data?.detail || "Something went wrong");
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-blue-50">
      <div className="bg-white p-8 rounded-xl shadow-md w-96">
        <h1 className="text-2xl font-bold text-blue-700 mb-2">🔬 ResearchHub AI</h1>
        <p className="text-gray-500 mb-6">{isRegister ? "Create an account" : "Sign in to continue"}</p>
        {error && <p className="text-red-500 text-sm mb-3">{error}</p>}
        <input className="w-full border p-2 rounded mb-3" placeholder="Username"
          value={username} onChange={e => setUsername(e.target.value)} />
        {isRegister && (
          <input className="w-full border p-2 rounded mb-3" placeholder="Email"
            value={email} onChange={e => setEmail(e.target.value)} />
        )}
        <input className="w-full border p-2 rounded mb-4" placeholder="Password"
          type="password" value={password} onChange={e => setPassword(e.target.value)} />
        <button onClick={handleSubmit}
          className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 font-semibold">
          {isRegister ? "Register" : "Login"}
        </button>
        <p className="text-center mt-4 text-sm text-gray-500">
          {isRegister ? "Already have an account? " : "Don't have an account? "}
          <button className="text-blue-600 font-medium" onClick={() => setIsRegister(!isRegister)}>
            {isRegister ? "Login" : "Register"}
          </button>
        </p>
      </div>
    </div>
  );
};

export default Login;s