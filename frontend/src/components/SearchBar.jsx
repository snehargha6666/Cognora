import { useState } from "react";

export default function SearchBar({ onSearch, onFileUpload }) {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [fileName, setFileName] = useState(null); // 🔥 NEW

  // 🔹 Normal search
  const handleSubmit = (e) => {
    e.preventDefault();
    if (!query.trim()) return;
    onSearch(query);
  };

  // 🔹 File upload
  const handleFileChange = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setFileName(file.name); // 🔥 store file name

    const formData = new FormData();
    formData.append("file", file);

    try {
      setLoading(true);

      const res = await fetch("http://127.0.0.1:8000/upload", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();

      if (onFileUpload) {
        onFileUpload(data);
      }

    } catch (err) {
      console.error("Upload error:", err);
    } finally {
      setLoading(false);
    }
  };

  // 🔹 Remove file (NEW)
  const handleRemoveFile = () => {
    setFileName(null);
  };

  return (
    <div className="flex flex-col gap-3">
      
      {/* 🔹 Search */}
      <form onSubmit={handleSubmit} className="flex gap-2">
        <input
          className="flex-1 p-3 border rounded-xl"
          placeholder="Ask anything or upload a project..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />

        <button className="px-4 bg-black text-white rounded-xl">
          Search
        </button>
      </form>

      {/* 🔹 Upload Section */}
      <div className="flex items-center gap-2">

        {/* Upload button */}
        {!fileName && (
          <label className="px-4 py-2 bg-gray-200 rounded-xl cursor-pointer hover:bg-gray-300">
            Upload Project
            <input
              type="file"
              className="hidden"
              onChange={handleFileChange}
            />
          </label>
        )}

        {/* File name display */}
        {fileName && (
          <div className="flex items-center gap-2 bg-gray-100 px-3 py-2 rounded-xl">
            <span className="text-sm">{fileName}</span>

            <button
              onClick={handleRemoveFile}
              className="text-red-500 font-bold"
            >
              ✕
            </button>
          </div>
        )}

        {/* Loading */}
        {loading && (
          <span className="text-sm text-gray-500">
            Processing file...
          </span>
        )}
      </div>
    </div>
  );
}