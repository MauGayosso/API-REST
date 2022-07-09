function getClientes(){
    
    var query = window.location.search.substring(1); // OBTENER QUERY DE LA URL
    console.log("Query" + query);
    // Conectar con el Backend
    var request = new XMLHttpRequest();
    
    // Sesion de la pagina desde APLICACIONES en Inspeccionar elemento
    //username = sessionStorage.getItem("username");
    //password = sessionStorage.getItem("password");

    var username = "user";
    var password = "user";

    request.open('GET', 'https://8000-maugayosso-apirest-uapi6cjdvxz.ws-us53.gitpod.io/clientes/');
    request.setRequestHeader("Accept", "application/json");
    // + QUERY PARA CONCATENAR DATOS -- SE PUEDE USAR PARA DELETE, UPDATE, GET ONE
    // TRUE PERMITE ASYNC
    // AUTORIZACION
    request.setRequestHeader("Authorization", "Basic " + btoa(username + ":" + password))
    request.setRequestHeader("content-type", "application/json");

    const tabla = document.getElementById("tabla_clientes");

    var tableHead = document.createElement("thead");
    var tableBody = document.createElement("tbody");

    // Crear columnas de la tabla
    tableHead.innerHTML = `
        <tr>
            <th>ID Cliente</th>
            <th>Nombre</th>
            <th>Emal</th>
            <th>Opciones</th>
        </tr>
    `;

    request.onload = () => {
        const response = request.responseText;
        const json = JSON.parse(response);
        //MOSTRAR EN CONSOLA LO QUE RESPONDE
        console.log("Response" + response); 
        console.log("JSON" + json);
         //CICLO PARA GENERAR LOS ELEMENTOS EN BASE A LOS ELEMENTOS QUE SE CONTENGAN EN LA LISTA OBTENIDA
        // document.createElement(" ")  dentro puede asignarse cualquier elemento de HTML para generar
        for (let i = 0; i < json.length; i++){

            var tr = document.createElement("tr");
            var tr_id_cliente = document.createElement("td");
            var tr_nombre = document.createElement("td");
            var tr_email = document.createElement("td");
            var tr_detalles = document.createElement("td");
            var tr_putCliente = document.createElement("td");
            var tr_deleteCliente = document.createElement("td");

            tr_id_cliente.innerHTML = json[i].id_cliente;
            tr_nombre.innerHTML = json[i].nombre;
            tr_email.innerHTML = json[i].email;
            tr_detalles.innerHTML = "<a href=getCliente.html?"+json[i].id_cliente+">Detalles</a>";
            tr_putCliente.innerHTML = "<a href=putCliente.html?"+json[i].id_cliente+">Editar</a>";
            tr_deleteCliente.innerHTML = "<a onclick=deleteCliente("+json[i].id_cliente+")><font color = 'blue'><u>Eliminar</u></a></font>";

            // DAR A CADAR TR(COLUMNAS) DEL HTML LOS VALORES DE CADA FILA
            tr.appendChild(tr_id_cliente);
            tr.appendChild(tr_nombre);
            tr.appendChild(tr_email);
            tr.appendChild(tr_detalles);
            tr.appendChild(tr_putCliente);
            tr.appendChild(tr_deleteCliente);
            // PASAR AL BODY DE LA TABLA LOS DATOS 
            tableBody.appendChild(tr);
        }

        tabla.appendChild(tableHead);
        tabla.appendChild(tableBody);

    };
    request.send();
};

function deleteCliente(id_cliente){

    var request = new XMLHttpRequest();

    console.log('ID Recibido : ' + id_cliente);

    var username = "user";
    var password = "user";

    request.open('DELETE','https://8000-maugayosso-apirest-uapi6cjdvxz.ws-us53.gitpod.io/clientes/' + id_cliente, true);
    request.setRequestHeader("Accept", "application/json");
    request.setRequestHeader("Authorization", "Basic " + btoa(username + ":" + password))
    request.setRequestHeader("content-type", "application/json");
    request.onload = () =>{
        const response = request.responseText;
        const json = JSON.parse(response);
        const status = request.status;

        console.log("Response : " + response);
        console.log("JSON     : " + json);
        console.log("Status   : " + status);

        if (status == 202){
            alert(json.message);
            window.location.reload();
        }


    };
    request.send();
};