const $ = id => document.getElementById(id);
let lastAnswer = "0", history = JSON.parse(localStorage.getItem("cw-history") || "[]");
const prefs = JSON.parse(localStorage.getItem("cw-prefs") || "{}");
$("angle-mode").value = prefs.angle || "DEG"; $("precision").value = String(prefs.precision || 10);
document.documentElement.dataset.theme = prefs.theme || "dark";
function insertAtCursor(text){const el=$("expression");const start=el.selectionStart,end=el.selectionEnd;el.setRangeText(text,start,end,"end");el.focus();}
async function api(path,data){const r=await fetch(path,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(data)});const j=await r.json();if(!r.ok||!j.ok)throw new Error(j.error||"Request failed.");return j;}
function showError(err){$("status").textContent="ERROR";$("result").textContent=err.message||String(err);}
async function calculate(){let expr=$("expression").value.replace(/\bAns\b/g,lastAnswer);if(!expr.trim())return;try{const j=await api("/api/calculate",{expression:expr,angle_mode:$("angle-mode").value,precision:Number($("precision").value)});lastAnswer=j.result.exact;$("result").textContent=j.result.approx;$("status").textContent=j.result.is_exact?"EXACT":"APPROXIMATE";addHistory(expr,j.result.approx);}catch(e){showError(e)}}
function addHistory(expr,result){history.unshift({expr,result});history=history.slice(0,50);localStorage.setItem("cw-history",JSON.stringify(history));renderHistory();}
function renderHistory(){$("history-list").innerHTML="";if(!history.length){$("history-list").innerHTML='<p class="micro">No calculations yet.</p>';return;}history.forEach(item=>{const b=document.createElement("button");b.className="history-item";b.innerHTML=`<small></small><strong></strong>`;b.querySelector("small").textContent=item.expr;b.querySelector("strong").textContent="= "+item.result;b.onclick=()=>{$("expression").value=item.expr;$("expression").focus();};$("history-list").appendChild(b);});}
$("keypad").addEventListener("click",e=>{const b=e.target.closest("button");if(!b)return;if(b.dataset.action==="clear"){$("expression").value="";$("result").textContent="0";$("status").textContent="READY";return;}if(b.dataset.action==="backspace"){const el=$("expression"),s=el.selectionStart,en=el.selectionEnd;if(s!==en)el.setRangeText("",s,en,"end");else if(s>0)el.setRangeText("",s-1,s,"end");el.focus();return;}if(b.dataset.action==="calculate"){calculate();return;}if(b.dataset.insert)insertAtCursor(b.dataset.insert);});
$("expression").addEventListener("keydown",e=>{if(e.key==="Enter"&&!e.shiftKey){e.preventDefault();calculate();}if(e.key==="Escape"){$("expression").value="";}});
$("angle-mode").onchange=savePrefs;$("precision").onchange=savePrefs;
function savePrefs(){localStorage.setItem("cw-prefs",JSON.stringify({angle:$("angle-mode").value,precision:$("precision").value,theme:document.documentElement.dataset.theme}));}
$("theme-toggle").onclick=()=>{document.documentElement.dataset.theme=document.documentElement.dataset.theme==="dark"?"light":"dark";savePrefs();};
$("history-toggle").onclick=()=>{$("history-panel").classList.toggle("hidden");renderHistory();};
$("clear-history").onclick=()=>{history=[];localStorage.setItem("cw-history","[]");renderHistory();};
$("copy-expression").onclick=()=>navigator.clipboard?.writeText($("expression").value);
$("copy-result").onclick=()=>navigator.clipboard?.writeText($("result").textContent);
$("use-result").onclick=()=>insertAtCursor("Ans");
document.querySelectorAll(".tab").forEach(tab=>tab.onclick=()=>{document.querySelectorAll(".tab").forEach(t=>t.classList.toggle("active",t===tab));document.querySelectorAll(".tool-panel").forEach(p=>p.classList.toggle("hidden",p.id!==tab.dataset.panel));});
function matrixText(id){return $(id).value.trim().split(";").map(r=>r.split(",").map(v=>{const n=Number(v.trim());if(!v.trim()||!Number.isFinite(n))throw new Error("Matrix entries must be numeric.");return n;}));}
$("convert-btn").onclick=async()=>{try{const j=await api("/api/convert",{value:Number($("conv-value").value),from_unit:$("conv-from").value.trim(),to_unit:$("conv-to").value.trim()});$("conv-output").textContent=String(j.value);}catch(e){$("conv-output").textContent=e.message;}};
$("equation-btn").onclick=async()=>{try{const j=await api("/api/equation",{equation:$("equation-input").value,variable:"x"});$("equation-output").textContent=j.solutions.join(", ");}catch(e){$("equation-output").textContent=e.message;}};
$("matrix-btn").onclick=async()=>{try{const op=$("matrix-op").value,a=matrixText("matrix-a"),b=["add","subtract","multiply"].includes(op)?matrixText("matrix-b"):null;const j=await api("/api/matrix",{operation:op,a,b});$("matrix-output").textContent=JSON.stringify(j.result);}catch(e){$("matrix-output").textContent=e.message;}};
$("stats-btn").onclick=async()=>{try{const values=$("stats-values").value.split(",").map(s=>{if(!s.trim())throw new Error("Use comma-separated numbers.");return Number(s.trim())});const j=await api("/api/statistics",{values});$("stats-output").textContent=Object.entries(j.result).map(([k,v])=>`${k}: ${Number(v).toPrecision(8)}`).join("\n");}catch(e){$("stats-output").textContent=e.message;}};
$("base-btn").onclick=async()=>{try{const j=await api("/api/base",{value:$("base-value").value,from_base:Number($("base-from").value),to_base:Number($("base-to").value)});$("base-output").textContent=j.result;}catch(e){$("base-output").textContent=e.message;}};
renderHistory();
