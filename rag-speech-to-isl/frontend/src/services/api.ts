import { SignGenerateResponse, RetrievedExemplar } from '../types';

export async function fetchLanguages() {
  const res = await fetch('/api/languages');
  return res.json();
}

export async function transcribeAudio(audioBlob: Blob, language = 'auto') {
  const formData = new FormData();
  formData.append('file', audioBlob, 'recording.webm');
  formData.append('language', language);

  const res = await fetch('/api/transcribe', {
    method: 'POST',
    body: formData
  });
  if (!res.ok) throw new Error('Transcription failed');
  return res.json();
}

export async function generateSignSequence(
  text: string,
  language = 'auto',
  useRag = true,
  ragTopK = 3
): Promise<SignGenerateResponse> {
  const res = await fetch('/api/sign/generate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      text,
      language,
      use_rag: useRag,
      rag_top_k: ragTopK
    })
  });
  if (!res.ok) throw new Error('Sign generation pipeline error');
  return res.json();
}

export async function queryRAG(query: string, topK = 3): Promise<RetrievedExemplar[]> {
  const res = await fetch('/api/rag/query', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query, top_k: topK })
  });
  if (!res.ok) throw new Error('RAG query failed');
  const data = await res.json();
  return data.results;
}

export async function runBenchmarkEvaluation(useRag = true) {
  const res = await fetch('/api/evaluate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ use_rag: useRag })
  });
  if (!res.ok) throw new Error('Evaluation benchmark failed');
  return res.json();
}
