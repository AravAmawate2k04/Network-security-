import { download } from "../api";

export default function Dashboard() {
  const getFile = async type => {
    const res = await download(type);
    const blob = new Blob([res.data], { type: "application/pdf" });
    const url  = window.URL.createObjectURL(blob);
    const a    = document.createElement("a");
    a.href     = url;
    a.download = `${type}.pdf`;
    a.click();
  };

  return (
    <div className="text-center">
      <h2>Welcome!</h2>
      <button
        className="btn btn-primary m-2"
        onClick={() => getFile("degree")}
      >
        Download Degree Certificate
      </button>
      <button
        className="btn btn-secondary m-2"
        onClick={() => getFile("grade")}
      >
        Download Grade Report
      </button>
    </div>
  );
}
