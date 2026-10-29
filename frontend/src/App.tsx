import React, { useState } from 'react';
import { generateSignSequence } from './services/api';
import { SignGenerateResponse } from './types';

export const App: React.FC = () => {
  const [inputText, setInputText] = useState('नमस्ते, आपका नाम क्या है?');
  const [selectedLang, setSelectedLang] = useState('hi');
  const [useRag, setUseRag] = useState(true);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<SignGenerateResponse | null>(null);

  const handleTranslate = async () => {
    if (!inputText.trim()) return;
    setLoading(true);
    try {
      const data = await generateSignSequence(inputText, selectedLang, useRag);
      setResult(data);
    } catch (e: any) {
      alert(`Pipeline error: ${e.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans">
      <header className="border-b border-slate-800 p-4 flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="w-8 h-8 rounded-lg bg-amber-500 flex items-center justify-center font-bold text-slate-950">
            ISL
          </div>
          <div>
            <h1 className="text-base font-bold">ISL Avatar Studio</h1>
            <p className="text-xs text-slate-400">Speak naturally. Understand through signs.</p>
          </div>
        </div>
      </header>

      <main className="flex-1 p-6 max-w-4xl mx-auto w-full space-y-6">
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4">
          <div className="flex items-center justify-between">
            <label className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Indian Language Input</label>
            <label className="text-xs text-slate-300 flex items-center space-x-2">
              <input
                type="checkbox"
                checked={useRag}
                onChange={e => setUseRag(e.target.checked)}
                className="rounded bg-slate-800 border-slate-700 text-amber-500"
              />
              <span>Enable FAISS RAG</span>
            </label>
          </div>

          <textarea
            value={inputText}
            onChange={e => setInputText(e.target.value)}
            rows={3}
            className="w-full bg-slate-950 border border-slate-700 rounded-lg p-3 text-sm focus:border-amber-500 focus:outline-none"
            placeholder="Type or speak in Hindi, English, Tamil, Telugu..."
          />

          <div className="flex items-center justify-between">
            <select
              value={selectedLang}
              onChange={e => setSelectedLang(e.target.value)}
              className="bg-slate-950 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-slate-200"
            >
              <option value="auto">Auto Detect</option>
              <option value="hi">Hindi (हिन्दी)</option>
              <option value="en">English</option>
              <option value="ta">Tamil (தமிழ்)</option>
              <option value="te">Telugu (తెలుగు)</option>
              <option value="bn">Bengali (বাংলা)</option>
              <option value="mr">Marathi (मराठी)</option>
            </select>

            <button
              onClick={handleTranslate}
              disabled={loading}
              className="px-5 py-2 rounded-lg bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold text-xs uppercase tracking-wider transition"
            >
              {loading ? 'Translating...' : 'Translate & Sign'}
            </button>
          </div>
        </div>

        {result && (
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-3">
            <h2 className="text-xs font-bold text-amber-400 uppercase tracking-wider">ISL Gloss Sequence</h2>
            <div className="flex flex-wrap gap-2">
              {result.gloss_details.map((g, idx) => (
                <span
                  key={idx}
                  className={`px-3 py-1 rounded text-xs font-mono font-bold ${
                    g.is_verified ? 'bg-amber-500/15 text-amber-300 border border-amber-500/30' : 'bg-rose-500/15 text-rose-300'
                  }`}
                >
                  {g.token} ({g.syntax_role})
                </span>
              ))}
            </div>

            <p className="text-xs text-slate-300 mt-2 bg-slate-950/60 p-3 rounded-lg border border-slate-800">
              {result.explanation}
            </p>
          </div>
        )}
      </main>
    </div>
  );
};
export default App;
