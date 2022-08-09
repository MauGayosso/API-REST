function postCliente(){
    let name = document.getElementById("name");
    let email = document.getElementById("email");

    let payload = {
        "nombre" : name.value ,
        "email" : email.value
    }

    var request = new XMLHttpRequest();

    token = sessionStorage.getItem("token")

    request.open('POST',"https://8000-maugayosso-apirest-uapi6cjdvxz.ws-us59.gitpod.io/clientes/",true)
    request.setRequestHeader("Accept", "application/json");
    request.setRequestHeader("Authorization", "Bearer " + token)
    request.setRequestHeader("content-type", "application/json");

    request.onload = () =>{
        const response = request.responseText;
        const json = JSON.parse(response);
        const status = request.status;

        console.log("Response : " + response);
        console.log("JSON     : " + json);
        console.log("Status   : " + status);

        if (status == 200){
            window.location.replace("getClientes.html");
        }
        else{
            alert(json.detail);
        }

    };
    request.send(JSON.stringify(payload));
};