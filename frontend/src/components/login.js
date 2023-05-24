import React, { useState } from "react";
import Header from "./header";
export default function Login() {
  const [username, setusername] = useState("");
  const [password, setpassword] = useState("");
  const handleFormSubmit = (event) => {
    event.preventDefault();
    const formData = {
      username: username,
      password: password,
    };
    fetch("http://localhost:5000/users", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(formData),
    })
      .then((response) => {
        // Handle the response from the server
        if (response.ok) {
          return response.json();
        } else {
          throw new Error("Login failed");
        }
      })
      .then((data) => {
        console.log(data);
      })
      .catch((error) => {
        alert("Login Failed");
        console.log(error);
      });
  };
  return (
    <div className="container">
      <div className="container">
        <Header />
      </div>
      <form className="prompts" onSubmit={handleFormSubmit}>
        <div className="textTitle">Login</div>
        <div className="container">
          <input
            placeholder="CalvinSopocy@gmail.com"
            type="text"
            name="Username"
            value={username}
            onChange={(e) => setusername(e.target.value)}
            className="textbox textbox1"
          ></input>
          <input
            placeholder="********"
            type="password"
            name="Password"
            onChange={(e) => setpassword(e.target.value)}
            className="textbox textbox1"
          ></input>
        </div>
        <div className="container">
          <button className="button">Submit</button>
        </div>
      </form>
    </div>
  );
}
