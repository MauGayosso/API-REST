function loginUser(idToken){
    let email = document.getElementById('email');
    let password = document.getElementById('password');

    let payload = {
        "username" : email.value,
        "password" : password.value
    }

    var request = new XMLHttpRequest();
    request.open("POST","https://8000-maugayosso-apirest-uapi6cjdvxz.ws-us59.gitpod.io/user/login",true);
    request.setRequestHeader('Accept', 'application/json');
    request.setRequestHeader('Content-Type', 'application/json');

    request.onload = () =>{
        const response = request.responseText;
        const json = JSON.parse(response);
        const status = request.status;

        console.log("Response : " + response);
        console.log("Status   : " + status);

        if (status == 202){
            window.location.replace("getClientes.html");
            sessionStorage.setItem("token", json.user_dat);
            console.log("Response : " + response);
            alert
        }       
        else{
            alert(json.detail);
        }

    };
    request.send(JSON.stringify(payload));
};
