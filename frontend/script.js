
const API = "http://127.0.0.1:8000";

function token(){ return localStorage.getItem("token"); }
function authHeaders(){ return {"Content-Type":"application/json","Authorization":"Bearer "+token()}; }

function requireLogin(){
    if(!token()){ window.location.href="index.html"; return false; }
    return true;
}

function logout(){
    localStorage.removeItem("token");
    window.location.href="index.html";
}

function go(page){ window.location.href=page; }

async function api(path, options={}){
    try{
        const response = await fetch(API+path, {
            ...options,
            headers: {...authHeaders(), ...(options.headers||{})}
        });
        const data = await response.json().catch(()=>({message:"Invalid server response"}));
        if(response.status === 401){
            localStorage.removeItem("token");
            window.location.href="index.html";
            return null;
        }
        if(!response.ok) throw new Error(data.detail || data.message || "Request failed");
        return data;
    }catch(error){
        showResult("Error: "+error.message+"\n\nMake sure FastAPI is running on http://127.0.0.1:8000");
        return null;
    }
}

function showResult(data){
    const el=document.getElementById("result");
    if(el) el.textContent=typeof data==="string"?data:JSON.stringify(data,null,2);
}

async function login(){
    const username=document.getElementById("username").value.trim();
    const password=document.getElementById("password").value;
    const msg=document.getElementById("loginMessage");
    if(!username || !password){ msg.textContent="Enter username and password."; return; }
    try{
        const response=await fetch(API+"/login",{
            method:"POST",
            headers:{"Content-Type":"application/json"},
            body:JSON.stringify({username,password})
        });
        const data=await response.json();
        if(data.access_token){
            localStorage.setItem("token",data.access_token);
            window.location.href="dashboard.html";
        }else msg.textContent=data.message || "Invalid username or password";
    }catch(e){ msg.textContent="Cannot connect to FastAPI. Start the backend first."; }
}

async function addCustomer(){
    const data={customer_id:val("customerId"),name:val("customerName"),email:val("customerEmail"),phone:val("customerPhone")};
    if(!data.customer_id||!data.name||!data.email||!data.phone){showResult("Please fill all customer fields.");return}
    const r=await api("/customers",{method:"POST",body:JSON.stringify(data)}); if(r)showResult(r);
}
async function loadCustomers(){
    const r=await api("/customers"); if(r){showResult(r);renderTable(r.customers,["customer_id","name","email","phone"]);}
}
async function loadCustomerOptions(){
    const r=await api("/customers");
    const select=document.getElementById("accountCustomerId");
    if(!select || !r) return;
    select.innerHTML='<option value="">Select Customer</option>';
    (r.customers||[]).forEach(row=>{
        const customerId=Array.isArray(row)?row[0]:row.customer_id;
        const name=Array.isArray(row)?row[1]:row.name;
        if(customerId) select.innerHTML += `<option value="${customerId}">${customerId} - ${name||""}</option>`;
    });
}

async function addAccount(){
    const data={account_id:val("accountId"),customer_id:val("accountCustomerId"),account_type:val("accountType"),balance:num("accountBalance")};
    if(!data.account_id||!data.customer_id||!data.account_type||Number.isNaN(data.balance)||data.balance<0){showResult("Please fill all account fields correctly.");return}
    const r=await api("/accounts",{method:"POST",body:JSON.stringify(data)});
    if(r){showResult(r); document.getElementById("accountId").value=""; document.getElementById("accountBalance").value=""; loadAccounts();}
}
async function deleteAccount(){
    const accountId=val("deleteAccountId");
    if(!accountId){showResult("Enter an Account ID to delete.");return}
    if(!confirm("Delete account "+accountId+"? Its transaction history will also be deleted.")) return;
    const r=await api("/accounts/"+encodeURIComponent(accountId),{method:"DELETE"});
    if(r){showResult(r); document.getElementById("deleteAccountId").value=""; loadAccounts();}
}
async function loadAccounts(){
    const r=await api("/accounts"); if(r){showResult(r);renderTable(r.accounts,["account_id","customer_id","account_type","balance"]);}
}
async function deposit(){
    const data={account_id:val("depositAccount"),amount:num("depositAmount")};
    if(!data.account_id||Number.isNaN(data.amount)||data.amount<=0){showResult("Enter a valid account ID and positive amount.");return}
    const r=await api("/transactions/deposit",{method:"POST",body:JSON.stringify(data)}); if(r)showResult(r);
}
async function withdraw(){
    const data={account_id:val("withdrawAccount"),amount:num("withdrawAmount")};
    if(!data.account_id||Number.isNaN(data.amount)||data.amount<=0){showResult("Enter a valid account ID and positive amount.");return}
    const r=await api("/transactions/withdraw",{method:"POST",body:JSON.stringify(data)}); if(r)showResult(r);
}
async function loadTransactions(){
    const r=await api("/transactions"); if(r){showResult(r);renderTable(r.transactions,["transaction_id","account_id","transaction_type","amount"]);}
}
async function analyzeRisk(){
    const data={customer_id:val("riskCustomer"),account_id:val("riskAccount"),amount:num("riskAmount"),frequency:parseInt(val("riskFrequency"))};
    if(!data.customer_id||!data.account_id||Number.isNaN(data.amount)||Number.isNaN(data.frequency)){showResult("Please fill all risk fields.");return}
    const r=await api("/risk",{method:"POST",body:JSON.stringify(data)}); if(r)showRisk(r);
}
function showRisk(r){
    showResult(r);
    const box=document.getElementById("riskSummary");
    if(box) box.innerHTML=`<div class="stat">${r.risk_score}</div><span class="badge">${r.risk_level}</span><p class="muted" style="margin-top:10px">${(r.risk_indicators||[]).join(", ")||"No risk indicators detected."}</p>`;
}
function val(id){return document.getElementById(id)?.value.trim()||""}
function num(id){return parseFloat(document.getElementById(id)?.value)}
function renderTable(rows,keys){
    const table=document.getElementById("dataTable"); if(!table)return;
    if(!Array.isArray(rows)||!rows.length){table.innerHTML="<p class='muted'>No records found.</p>";return}
    const normalized=rows.map(row=>Array.isArray(row)?Object.fromEntries(keys.map((k,i)=>[k,row[i]])):row);
    table.innerHTML="<table><thead><tr>"+keys.map(k=>`<th>${k}</th>`).join("")+"</tr></thead><tbody>"+
      normalized.map(row=>"<tr>"+keys.map(k=>`<td>${row[k]??""}</td>`).join("")+"</tr>").join("")+"</tbody></table>";
}

async function loadDashboard(){
    if(!requireLogin())return;
    const [c,a,t]=await Promise.all([api("/customers"),api("/accounts"),api("/transactions")]);
    if(c)document.getElementById("customerCount").textContent=c.customers.length;
    if(a)document.getElementById("accountCount").textContent=a.accounts.length;
    if(t)document.getElementById("transactionCount").textContent=t.transactions.length;
}
