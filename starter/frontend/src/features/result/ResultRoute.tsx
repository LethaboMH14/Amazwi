import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { api, userMessage } from "../../api/client";
import type { Result } from "../../api/contracts";
export function ResultRoute(){const {contributionId=""}=useParams();const [result,setResult]=useState<Result>();const [error,setError]=useState("");useEffect(()=>{if(contributionId)api.getResult(contributionId).then(setResult).catch(e=>setError(userMessage(e)));},[contributionId]);return <main className="route" aria-labelledby="result-title"><p className="eyebrow">Voice Value Receipt</p><h1 id="result-title">Your contribution is in the ledger</h1>{result?<><p>{result.outcome}</p><p>{result.reward_minor} {result.currency}</p></>:!error&&<p>Loading your peer decision…</p>}{error&&<p role="alert">{error}</p>}<Link to="/">Back to AMAZWI</Link></main>;}
