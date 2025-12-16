const API = "http://localhost:5000";


function login() {
  const role = roleEl().value;
  const username = userEl().value;
  const password = passEl().value;

  fetch(API + "/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ role, username, password })
  })
  .then(res => res.ok ? res.json() : Promise.reject())
  .then(data => {
    localStorage.setItem("user", JSON.stringify(data.user));
    location.href = role + ".html";
  })
  .catch(() => alert("Login gagal"));
}


function kirimLaporan() {
  const user = JSON.parse(localStorage.getItem("user"));
  fetch(API + "/laporan", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      id_warga: user.id_warga,
      id_kategori: kategoriEl().value,
      deskripsi: deskripsiEl().value
    })
  }).then(() => alert("Laporan terkirim"));
}


function loadAdmin() {
  fetch(API + "/laporan")
    .then(r => r.json())
    .then(data => {
      listEl("adminList").innerHTML = data.map(l => `
        <div class="card">
          <b>${l.warga}</b><br>${l.deskripsi}<br>
          Status: ${l.status}<br>
          ${l.status === "Menunggu Verifikasi"
            ? `<button onclick="update(${l.id_laporan},'Dalam Penanganan')">Verifikasi</button>`
            : ""}
        </div>`).join("");
    });
}


function loadPetugas() {
  fetch(API + "/laporan")
    .then(r => r.json())
    .then(data => {
      listEl("petugasList").innerHTML = data
        .filter(l => l.status === "Dalam Penanganan")
        .map(l => `
          <div class="card">
            ${l.deskripsi}<br>
            <button onclick="update(${l.id_laporan},'Selesai')">Selesai</button>
          </div>`).join("");
    });
}

function update(id, status) {
  fetch(API + `/laporan/${id}/status`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ status })
  }).then(() => location.reload());
}

function logout() {
  localStorage.clear();
  location.href = "index.html";
}


const roleEl = () => document.getElementById("role");
const userEl = () => document.getElementById("username");
const passEl = () => document.getElementById("password");
const kategoriEl = () => document.getElementById("kategori");
const deskripsiEl = () => document.getElementById("deskripsi");
const listEl = id => document.getElementById(id);
