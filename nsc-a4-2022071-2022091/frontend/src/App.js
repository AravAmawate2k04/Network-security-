import { BrowserRouter, Routes, Route } from "react-router-dom";
import Navbar      from "./components/Navbar";
import Signup      from "./components/Signup";
import Login       from "./components/Login";
import Dashboard   from "./components/Dashboard";

function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <div className="container mt-5">
        <Routes>
          <Route path="/"      element={<Signup />} />
          <Route path="/login" element={<Login />}  />
          <Route path="/dash"  element={<Dashboard />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;
