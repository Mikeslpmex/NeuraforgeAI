// CONFIGURACIÓN OFICIAL NEURAFORGE AI
const firebaseConfig = {
  apiKey: "AIzaSyC9FrqJkj7VPQJgniJf8SLkicFBatv2tVE",
  authDomain: "whatsappbotpro-c3680.firebaseapp.com",
  databaseURL: "https://whatsappbotpro-c3680-default-rtdb.firebaseio.com",
  projectId: "whatsappbotpro-c3680",
  storageBucket: "whatsappbotpro-c3680.firebasestorage.app",
  messagingSenderId: "828358151857",
  appId: "1:828358151857:web:24e373b85916e5bfe71c90"
};

// Inicializar Firebase (Versión compatible con navegador/APK)
firebase.initializeApp(firebaseConfig);
const db = firebase.firestore();

// === MONITOREO DEL TESORERO (MIKE AI) ===
function monitorearAdmin(adminId) {
    console.log("🛡️ Nexus Shield: Conectando con la red central...");
    
    db.collection("usuarios").doc(adminId).onSnapshot((doc) => {
        if (doc.exists) {
            const data = doc.data();
            // Actualizar Balance Forgecoin® en el Dashboard
            const balanceEl = document.getElementById("main-balance");
            if(balanceEl) balanceEl.innerHTML = `<i class="fas fa-coins text-warning"></i> ${data.fc_balance || 0} FC`;
            
            // Actualizar Ingresos Live
            const ingresosEl = document.getElementById("ingresos-totales");
            if(ingresosEl) ingresosEl.innerText = `$${data.ingresos_mes || 0}.00 MXN`;
            
            console.log("✅ Datos actualizados desde la Colmena.");
        } else {
            console.log("⚠️ El usuario no existe en la base de datos.");
        }
    });
}

// === FUNCIÓN PARA CREAR BILLETERA A TU HIJA ===
async function crearBilleteraHijaUI() {
    const nombre = document.getElementById("hija-nombre").value;
    const telegramID = document.getElementById("hija-id").value;

    if(!nombre || !telegramID) return alert("Por favor, ingresa Nombre y ID");

    const nuevaBilletera = {
        propietario: nombre,
        telegram_id: telegramID,
        fc_balance: 0,
        nivel: "Sembrador",
        parent_admin: "8362361029", // Vinculada a ti
        fecha_creacion: firebase.firestore.FieldValue.serverTimestamp()
    };

    try {
        await db.collection("usuarios").doc(telegramID).set(nuevaBilletera);
        alert(`🎉 ¡Billetera creada! ${nombre} ya es parte de NeuraforgeAI.`);
    } catch (error) {
        console.error("Error:", error);
        alert("Hubo un error al conectar con Firebase.");
    }
}

// Ejecutar al cargar con tu ID real
monitorearAdmin("8362361029");

