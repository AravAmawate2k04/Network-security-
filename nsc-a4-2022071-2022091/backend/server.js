
const express       = require("express");
const bodyParser    = require("body-parser");
const { PythonShell } = require("python-shell");
const path          = require("path");
const cors          = require("cors");
const cookieParser  = require("cookie-parser");
const fs = require("fs");
const app = express();
const corsOptions = {
    origin: "http://localhost:3000",
    credentials: true,
    methods: ["GET","POST","OPTIONS"],
    allowedHeaders: ["Content-Type"]
  };
  
  app.use(cors(corsOptions));
  app.options("*", cors(corsOptions));
  
  app.use(bodyParser.json());
  app.use(cookieParser());

// ─── callPython helper ───────────────────────────────────────────────
function callPython(payload) {
  return new Promise((resolve, reject) => {
    const pyshell = new PythonShell("api.py", {
      mode: "json",
      pythonOptions: ["-u"],
      scriptPath: path.join(__dirname, "../utils")
    });
    pyshell.send(payload);
    pyshell.on("message", msg => resolve(msg));
    pyshell.on("stderr", err => console.error("PY ERR:", err));
    pyshell.end(err => {
      if (err) reject(err);
    });
  });
}

// ─── Validation helpers ──────────────────────────────────────────────
function requireFields(body, fields) {
  for (const f of fields) {
    if (!body[f]) throw new Error(`Missing field: ${f}`);
  }
}

// ─── Signup ────────────────────────────────────────────────
app.post("/api/signup", async (req, res) => {
    console.log("↪︎ Signup payload:", req.body);
    try {
      requireFields(req.body, [
        "name","roll_number","dob","pincode",
        "email","college","grad_year","password"
      ]);

    const pyRes = await callPython({
      action: "signup",
      ...req.body
    });

    if (pyRes.error) return res.status(400).json(pyRes);
    res.json(pyRes);

  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});

// ─── Login ─────────────────────────────────────────────────
app.post("/api/login", async (req, res) => {
    console.log("↪︎ Login payload:", req.body);
    try {
      requireFields(req.body, ["roll_number", "password"]);
  
      const pyRes = await callPython({
        action: "login",
        ...req.body
      });
      console.log("↪︎ login_cli returned:", pyRes);
  
      if (pyRes.error) {
        return res.status(400).json(pyRes);
      }
  
      if (pyRes.status === "otp_sent") {
        return res.json(pyRes);
      }
  
      res.cookie("roll", pyRes.user.roll_number, { httpOnly: true });
      return res.json(pyRes);
  
    } catch (err) {
      return res.status(400).json({ error: err.message });
    }
  });
app.get("/api/download/:type", async (req, res) => {
    try {
      const roll = req.cookies.roll;
      if (!roll) return res.status(401).json({ error: "Not logged in" });
  
      console.log("↪︎ Download request:", { roll, type: req.params.type });
  
      const pyRes = await callPython({
        action: "generate",
        roll_number: roll
      });
      console.log("↪︎ generate returned:", pyRes);
  
      if (pyRes.error) {
        return res.status(400).json(pyRes);
      }
  
      // Decide which file to send
      const key = req.params.type === "degree" ? "degree_path" : "grade_path";
      const relPath = pyRes[key];
      const filePath = path.isAbsolute(relPath) ? relPath : path.join(__dirname, "..", relPath);
      console.log("↪︎ Attempting to send file:", filePath);
  
      // Check that the file exist
      if (!fs.existsSync(filePath)) {
        console.error("✖ File not found:", filePath);
        return res.status(404).json({ error: "File not found" });
      }
  
      return res.download(filePath);
  
    } catch (err) {
      console.error("‼ Download error:", err);
      return res.status(500).json({ error: err.message });
    }
  });
app.listen(4000, () => {
  console.log("Backend running on http://localhost:4000");
});
