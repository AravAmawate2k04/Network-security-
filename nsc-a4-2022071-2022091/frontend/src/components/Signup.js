import { useState } from "react";
import { signup }    from "../api";
import { useNavigate } from "react-router-dom";

export default function Signup() {
  const [form, setForm] = useState({
    name: "", roll_number: "", dob: "",
    pincode: "", email: "", college: "",
    grad_year: "", password: ""
  });
  const [step, setStep] = useState(1);
  const [otp, setOtp]   = useState("");
  const nav = useNavigate();

  const handleSubmit = async e => {
    e.preventDefault();
    try {
      // First step: send all signup fields
      if (step === 1) {
        const res = await signup(form);
        if (res.data.status === "otp_sent") {
          alert("OTP sent to your email");
          setStep(2);
        } else {
          alert(res.data.error || "Signup failed");
        }
      } else {
        // Second step: re-send same data + otp
        const payload = { ...form, otp };
        const res = await signup(payload);
        if (res.data.status === "ok") {
          alert("Signup complete! Please log in.");
          nav("/login");
        } else {
          alert(res.data.error || "Invalid or expired OTP");
        }
      }
    } catch (err) {
      alert(err.message);
    }
  };

  return (
    <div className="card mx-auto" style={{ maxWidth: 500 }}>
      <div className="card-body">
        <h3 className="card-title text-center mb-4">Signup</h3>
        <form onSubmit={handleSubmit}>
          {step === 1 ? (
            <>
              {[
                { label: "Full Name",       key: "name",        type: "text"     },
                { label: "Roll Number",     key: "roll_number", type: "text"     },
                { label: "Date of Birth",   key: "dob",         type: "date"     },
                { label: "Pincode",         key: "pincode",     type: "text"     },
                { label: "Email (Gmail)",   key: "email",       type: "email"    },
                { label: "College Name",    key: "college",     type: "text"     },
                { label: "Graduation Year", key: "grad_year",   type: "number"   },
                { label: "Password",        key: "password",    type: "password" }
              ].map(f => (
                <div className="form-group mb-3" key={f.key}>
                  <label>{f.label}</label>
                  <input
                    type={f.type}
                    className="form-control"
                    value={form[f.key]}
                    onChange={e =>
                      setForm(prev => ({ ...prev, [f.key]: e.target.value }))
                    }
                    required
                  />
                </div>
              ))}
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
                Verify OTP
              </button>
            </>
          )}
        </form>
      </div>
    </div>
  );
}
