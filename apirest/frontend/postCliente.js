function postCliente(){
    let name = document.getElementById("name");
    let email = document.getElementById("email");

    let payload = {
        "nombre" : name.value ,
        "email" : email.value
    }


    console.log ("Nombre : " + name.value);
    console.log ("Email : " + email.value);

    var request = new XMLHttpRequest();

    var username = "user";
    var password = "user";

    request.open('POST',"https://8000-maugayosso-apirest-uapi6cjdvxz.ws-us53.gitpod.io/clientes/",true)
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



    };
    request.send(JSON.stringify(payload));
};