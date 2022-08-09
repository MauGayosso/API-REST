function putCliente(){

    var request = new XMLHttpRequest();
    token = sessionStorage.getItem('token')

    let id_cliente = window.location.search.substring(1);

    let name = document.getElementById("name");
    let email = document.getElementById("email");

    console.log('ID Recibido : ' + id_cliente);
    console.log('Name Recibido : ' + name.value);
    console.log('Email Recibido : ' + email.value);

    let payload = {
        "id_cliente" : id_cliente, //No usa .value
        "nombre" : name.value ,
        "email" : email.value
    }

    var username = "user";
    var password = "user";

    request.open('PUT','https://8000-maugayosso-apirest-uapi6cjdvxz.ws-us59.gitpod.io/clientes/' + id_cliente.value, true);
    request.setRequestHeader("Accept", "application/json");
    request.setRequestHeader("Authorization", "Bearer " + token);
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
            window.location.replace('getClientes.html');
        }
        else{
            alert(json.detail);
        }


    };
    request.send(JSON.stringify(payload));
};