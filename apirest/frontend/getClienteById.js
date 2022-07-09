function getClienteById(){
    var query = window.location.search.substring(1);
    console.log("Id cliente : " + query);

    var request = new XMLHttpRequest();

    var username = "user";
    var password = "user";

    request.open('GET','https://8000-maugayosso-apirest-uapi6cjdvxz.ws-us53.gitpod.io/clientes/' +query, true);
    request.setRequestHeader("Accept", "application/json");
    request.setRequestHeader("Authorization", "Basic " + btoa(username + ":" + password))
    request.setRequestHeader("content-type", "application/json");

    request.onload = () => {
        const response = request.responseText;
        const json = JSON.parse(response);

        console.log("Response : " + response);
        console.log("JSON : " + json);

        if (request.status == 202){
            
            document.getElementById("name").value = json.nombre;
            document.getElementById("email").value = json.email;
        }
        else if (request.status == 401){
            alert(json.detail);
        }
    };
    request.send();
};