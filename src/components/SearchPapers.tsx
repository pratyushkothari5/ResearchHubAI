import React, { useState } from "react";
import { searchPapers, importPaper, getWorkspacePapers, deletePaper } from "../api";

interface Props {
  workspaceId: number | null;
  workspaceName: string;
}

const SearchPapers: React.FC<Props> = ({ workspaceId, workspaceName }) => {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<any[]>([]);
  const [imported, setImported] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [tab, setTab] = useState<"search" | "library">("search");

  const handleSearch = async () => {
    if (!query.trim()) return;
    setLoading(true);
    const data = await searchPapers(query);
    setResults(data);
    setLoading(false);
  };

  const loadLibrary = async () => {
    if (!workspaceId) return;
    const data = await getWorkspacePapers(workspaceId);
    setImported(data);
  };

  const handleImport = async (paper: any) => {
    if (!workspaceId) return alert("Select a workspace first!");
    await importPaper(paper, workspaceId);
    alert("Paper imported!");
  };

  const handleDelete = async (id: number) => {
    await deletePaper(id);
    loadLibrary();
  };

  React.useEffect(() => {
    if (tab === "library") loadLibrary();
  }, [tab, workspaceId]);

  return (
    <div className="bg-white rounded-xl shadow p-4">
      <h2 className="text-lg font-bold text-gray-700 mb-3">
        📄 Papers {workspaceName ? `— ${workspaceName}` : ""}
      </h2>
      <div className="flex gap-3 mb-4">
        <button onClick={() => setTab("search")}
          className={`px-4 py-1 rounded-full text-sm font-medium ${tab === "search" ? "bg-blue-600 text-white" : "bg-gray-100"}`}>
          Search
        </button>
        <button onClick={() => setTab("library")}
          className={`px-4 py-1 rounded-full text-sm font-medium ${tab === "library" ? "bg-blue-600 text-white" : "bg-gray-100"}`}>
          My Library
        </button>
      </div>

      {tab === "search" && (
        <>
          <div className="flex gap-2 mb-4">
            <input className="flex-1 border p-2 rounded text-sm" placeholder="Search arXiv papers..."
              value={query} onChange={e => setQuery(e.target.value)}
              onKeyDown={e => e.key === "Enter" && handleSearch()} />
            <button onClick={handleSearch}
              className="bg-blue-600 text-white px-4 rounded text-sm hover:bg-blue-700">
              {loading ? "..." : "Search"}
            </button>
          </div>
          <div className="space-y-3 max-h-96 overflow-y-auto">
            {results.map((p, i) => (
              <div key={i} className="border rounded-lg p-3">
                <p className="font-semibold text-sm text-gray-800">{p.title}</p>
                <p className="text-xs text-gray-500 mb-1">{p.authors} · {p.published_date}</p>
                <p className="text-xs text-gray-600 line-clamp-2">{p.abstract}</p>
                <div className="flex gap-2 mt-2">
                  <button onClick={() => handleImport(p)}
                    className="text-xs bg-green-500 text-white px-3 py-1 rounded hover:bg-green-600">
                    + Import
                  </button>
                  <a href={p.url} target="_blank" rel="noreferrer"
                    className="text-xs text-blue-500 underline py-1">View</a>
                </div>
              </div>
            ))}
          </div>
        </>
      )}

      {tab === "library" && (
        <div className="space-y-3 max-h-96 overflow-y-auto">
          {imported.length === 0 && <p className="text-gray-400 text-sm">No papers imported yet.</p>}
          {imported.map((p) => (
            <div key={p.id} className="border rounded-lg p-3">
              <p className="font-semibold text-sm text-gray-800">{p.title}</p>
              <p className="text-xs text-gray-500 mb-1">{p.authors} · {p.published_date}</p>
              <p className="text-xs text-gray-600 line-clamp-2">{p.abstract}</p>
              <button onClick={() => handleDelete(p.id)}
                className="mt-2 text-xs bg-red-500 text-white px-3 py-1 rounded hover:bg-red-600">
                Delete
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default SearchPapers;