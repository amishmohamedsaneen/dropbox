import { useState } from "react";
import TextField from "@mui/material/TextField";
import Button from "@mui/material/Button";
import ListItemText from "@mui/material/ListItemText";
import DownloadIcon from "@mui/icons-material/Download";
import "./App.css";

function App() {
  const [hasUser, setHasUser] = useState(false);
  const [userEmail, setUserEmail] = useState("");
  const [selectedFile, setSelectedFile] = useState([]);

  const saveuploadFiles = async (files) => {
    const url = `http://13.48.70.143:5050/upload/${userEmail}`;
    const formData = new FormData();
    files.forEach((file) => {
      formData.append("file", file);
    });
    try {
      const response = await fetch(url, {
        method: "POST",
        body: formData,
      });
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      const data = await response.json();
    } catch (error) {
      console.error("Error uploading files:", error);
    }
  };

  const handleFileChange = (e) => {
    const files = Array.from(e.target.files);
    const fileNames = files.map((file) => file.name);
    saveuploadFiles(files);
    setSelectedFile((prev) => [...prev, ...fileNames]);
  };

  const handleDownload = async (file) => {
    const url = `http://13.48.70.143:5050/files/${userEmail}/${file}`;
    try {
      const response = await fetch(url, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      });
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      const blob = await response.blob();
      const link = document.createElement("a");
      link.href = window.URL.createObjectURL(blob);
      link.download = file;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    } catch (error) {
      console.error("Error downloading file:", error);
    }
  };

  const handleSearch = async () => {
    const url = `http://13.48.70.143:5050/files/${userEmail}`;
    try {
      const response = await fetch(url, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      });
      const files = await response.json();
      const fileNames = files ? files.map((file) => file.filename) : [];
      setSelectedFile(fileNames);
      setHasUser(true);
    } catch (error) {
      setHasUser(true);
      console.error("Error fetching user data:", error);
    }
  };

  return (
    <div className="App">
      <header className="app-header" onClick={() => setHasUser(false)}>
        <span>Amish File explorer</span>
        {hasUser && <span>Home</span>}
      </header>
      {!hasUser && (
        <div className="search-container">
          <label>Welcome!!</label>
          <div className="search-bar">
            {" "}
            <TextField
              type="text"
              placeholder="Enter registered or new email ID"
              className="search-input"
              size="small"
              onChange={(e) => setUserEmail(e.target.value)}
              variant="outlined"
            />
            <Button variant="contained" onClick={handleSearch}>
              Search
            </Button>
          </div>
        </div>
      )}
      {hasUser && (
        <div className="file-explorer-container">
          Welcome to file explorer!
          <label className="upload-label">
            <input
              type="file"
              accept="application/pdf,image/jpeg,image/png,text/plain,text/csv,application/json"
              style={{ display: "none" }}
              onChange={handleFileChange}
            />

            <Button
              type="button"
              onClick={() =>
                document.querySelector('input[type="file"]').click()
              }
              variant="outlined"
            >
              {" "}
              Upload files
            </Button>
          </label>{" "}
          <span>Previously uploaded files:</span>
          <ul className="file-list">
            {selectedFile && selectedFile.length > 0 ? (
              selectedFile.map((file, index) => (
                <div key={index} className="file-item">
                  <li>{file}</li>
                  <DownloadIcon
                    style={{ marginRight: 4 }}
                    onClick={() => handleDownload(file)}
                  />
                </div>
              ))
            ) : (
              <ListItemText primary="No files uploaded yet." />
            )}
          </ul>
        </div>
      )}
    </div>
  );
}

export default App;
