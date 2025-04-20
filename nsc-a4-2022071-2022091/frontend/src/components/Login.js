import { useState } from "react";
import { login }     from "../api";
import { useNavigate } from "react-router-dom";

export default function Login() {
  const [form, setForm] = useState({ roll_number: "", password: "" });
  const [step, setStep] = useState(1);
  const [otp, setOtp]   = useState("");
  const nav = useNavigate();

  const handleSubmit = async e => {
    e.preventDefault();
    try {
      if (step === 1) {
        // Step 1: send credentials
        const res = await login(form);
        if (res.data.status === "otp_sent") {
          alert("OTP sent to your email");
          setStep(2);
        } else {
          alert(res.data.error || "Login failed");
        }
      } else {
        // Step 2: send credentials + otp
        const payload = { ...form, otp };
        const res = await login(payload);
        if (res.data.status === "ok") {
          nav("/dash");
        } else {
          alert(res.data.error || "Invalid or expired OTP");
        }
      }
    } catch (err) {
        const msg = err.response?.data?.error || err.message;
        alert(msg);
    }
  };

  return (
    <div className="card mx-auto" style={{ maxWidth: 400 }}>
      <div className="card-body">
        <h3 className="card-title text-center mb-4">Login</h3>
        <form onSubmit={handleSubmit}>
          {step === 1 ? (
            <>
              <div className="form-group mb-3">
                <label>Roll Number</label>
                <input
                  type="text"
                  className="form-control"
                  value={form.roll_number}
                  onChange={e =>
                    setForm(prev => ({ ...prev, roll_number: e.target.value }))
                  }
                  required
                />
              </div>
              <div className="form-group mb-3">
                <label>Password</label>
                <input
                  type="password"
                  className="form-control"
                  value={form.password}
                  onChange={e =>
                    setForm(prev => ({ ...prev, password: e.target.value }))
                  }
                  required
                />
              </div>
              <button className="btn btn-primary w-100" type="submit">
                Send OTP
              </button>
            </>
          ) : (
            <>
              <div className="form-group mb-3">
                <label>Enter OTP</label>
                <input
                  type="text"
                  className="form-control"
                  value={otp}
                  onChange={e => setOtp(e.target.value)}
                  required
                />
              </div>
              <button className="btn btn-success w-100" type="submit">
                Verify OTP & Login
              </button>
            </>
          )}
        </form>
      </div>
    </div>
  );
}
