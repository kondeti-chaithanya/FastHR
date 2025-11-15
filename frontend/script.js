const API_BASE = "http://localhost:8000";

/* ---------------------------
   UI: show/hide sections
----------------------------*/
function showSection(sectionId) {
  const sections = document.querySelectorAll(".section");
  sections.forEach(s => (s.style.display = "none"));
  const el = document.getElementById(sectionId);
  if (el) el.style.display = "block";
}

/* ---------------------------
   Helpers
----------------------------*/
function parseDDMMYYYYToYear(ddmm) {
  // Expect dd-mm-yyyy or d-m-yyyy
  if (!ddmm) return null;
  const parts = ddmm.trim().split("-");
  if (parts.length !== 3) return null;
  const year = Number(parts[2]);
  return Number.isFinite(year) ? year : null;
}

/* ---------------------------
   CREATE (Add Employee)
----------------------------*/
async function saveEmployee() {
  const idValue = document.getElementById("empId").value.trim();
  const empId = idValue ? (Number.isFinite(Number(idValue)) ? Number(idValue) : idValue) : null;

  const name = document.getElementById("empName").value.trim();
  const role = document.getElementById("role").value.trim();
  const address = document.getElementById("address").value.trim();
  const tech_stack = document.getElementById("tech").value.trim();
  const experience = Number(document.getElementById("experience").value || 0);
  const joiningText = document.getElementById("joining").value.trim();
  const year_of_joining = parseDDMMYYYYToYear(joiningText);

  // Basic validation
  if (!name) { alert("Employee Name is required"); return; }
  if (!role) { alert("Role is required"); return; }
  if (!tech_stack) { alert("Tech stack is required"); return; }

  // Build payload; include id only if provided
  const payload = {
    ...(empId !== null ? { id: empId } : {}),
    name,
    role,
    address: address || null,
    tech_stack,
    experience,
    year_of_joining,
    resignation_date: null
  };

  console.log("Create payload:", payload);

  // Demo behavior: show success and clear form (replace with fetch() when backend exists)
  alert("Employee saved (frontend demo). Replace with API call when backend is ready.");
  clearAddForm();
}

function clearAddForm() {
  document.getElementById("empId").value = "";
  document.getElementById("empName").value = "";
  document.getElementById("role").value = "";
  document.getElementById("address").value = "";
  document.getElementById("tech").value = "";
  document.getElementById("experience").value = "";
  document.getElementById("joining").value = "";
}

/* ---------------------------
   READ (Load employees)
   -- currently demo data; replace with fetch when backend ready
----------------------------*/
function loadEmployees() {
  const demo = [
    { id: 1, name: "John Doe", role: "Developer", tech_stack: "Python", experience: 4, address: "Hyderabad", year_of_joining: 2020 },
    { id: 2, name: "Sahil", role: "Intern", tech_stack: "FastAPI", experience: 1, address: "Bangalore", year_of_joining: 2023 }
  ];

  renderEmployeeList(demo);
}

function renderEmployeeList(items) {
  const list = document.getElementById("employeeList");
  list.innerHTML = "";
  items.forEach(emp => {
    const li = document.createElement("li");
    li.innerHTML = `
      <strong>${escapeHtml(String(emp.name || "N/A"))}</strong> (${escapeHtml(String(emp.role || "N/A"))})<br>
      ${escapeHtml(String(emp.tech_stack || "N/A"))} — ${escapeHtml(String(emp.experience ?? "N/A"))} years<br>
      Address: ${escapeHtml(String(emp.address || "N/A"))}<br>
      Joined: ${escapeHtml(String(emp.year_of_joining || "N/A"))}<br>
      <small>ID: ${escapeHtml(String(emp.id || "N/A"))}</small>
    `;
    list.appendChild(li);
  });
}

function escapeHtml(str) {
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

/* ---------------------------
   UPDATE (Update Employee)
   Will call backend PATCH when ready; currently demo
----------------------------*/
function updateEmployee() {
  const empId = Number(document.getElementById("updateId").value);
  if (!empId) { alert("Employee ID is required to update"); return; }

  const payload = {
    name: document.getElementById("updateName").value.trim() || null,
    role: document.getElementById("updateRole").value.trim() || null,
    address: document.getElementById("updateAddress").value.trim() || null,
    tech_stack: document.getElementById("updateTech").value.trim() || null,
    experience: (() => {
      const v = document.getElementById("updateExperience").value;
      return v ? Number(v) : null;
    })()
  };

  console.log("Update payload for id", empId, payload);
  alert(`Employee #${empId} updated (frontend demo). Replace with PATCH when backend is ready.`);
  clearUpdateForm();
}

function clearUpdateForm() {
  document.getElementById("updateId").value = "";
  document.getElementById("updateName").value = "";
  document.getElementById("updateRole").value = "";
  document.getElementById("updateAddress").value = "";
  document.getElementById("updateTech").value = "";
  document.getElementById("updateExperience").value = "";
}

/* ---------------------------
   DELETE (Delete Employee)
----------------------------*/
function deleteEmployee() {
  const empId = Number(document.getElementById("deleteId").value);
  if (!empId) { alert("Employee ID is required to delete"); return; }

  console.log("Delete id:", empId);
  alert(`Employee #${empId} deleted (frontend demo). Replace with DELETE when backend is ready.`);
  document.getElementById("deleteId").value = "";
}
