// Lógica para conectar el Dashboard con Firebase
const db = firebase.firestore();

function cargarDatosTesoreria(userId) {
    db.collection("usuarios").doc(userId).onSnapshot((doc) => {
        if (doc.exists) {
            const data = doc.data();
            // Actualiza el balance en el Dashboard
            document.querySelector(".fc-balance").innerHTML = `<i class="fas fa-coins"></i> ${data.fc_balance} FC`;
            // Actualiza los ingresos del mes
            document.getElementById("ingresos-totales").innerText = `$${data.ingresos_mes}.00 MXN`;
        }
    });
}
x
