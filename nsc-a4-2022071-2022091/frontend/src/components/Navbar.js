import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <nav className="navbar navbar-expand-lg navbar-light bg-light">
      <Link className="navbar-brand" to="/">CertApp</Link>
      <div className="collapse navbar-collapse">
        <ul className="navbar-nav">
          <li className="nav-item">
            <Link className="nav-link" to="/">Signup</Link>
          </li>
          <li className="nav-item">
            <Link className="nav-link" to="/login">Login</Link>
          </li>
        </ul>
      </div>
    </nav>
  );
}
