# FastAPI and Javascript DOM - Cheat Sheet :)


## Filename: main.py

CORS (Cross-Origin Resource Sharing): CORS or "Cross-Origin Resource Sharing" refers to the situations when a frontend running in a browser has JavaScript code that communicates with a backend, and the backend is in a different "origin" than the frontend.

```python
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
# CONEXION PARA LOS PUERTOS DEL BACKEND Y FRONTEND UVICORN Y python3 -m http.server 7050 EXAMPLE
origins = [
    "http://localhost:8080",
    "http://127.0.0.1:3000",
]

app.add_middleware( 
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Filename: get_productos.html

```html
<!DOCTYPE html>
<html lang="es">
    <header>
        <title>DOM javascript</title>
    </header>
    <body>
        <h1>DOM javascript</h1>
        <script type="text/javascript" src="get_productos.js"></script>
        <table id="tabla_productos">

        </table>

        <script async>
            document.body.onload = getProductos(0);
        </script>
    </body>
</html>
```



## Filename: get_productos.js

```javascript 

function getProductos(offset) {
    var request = new XMLHttpRequest();
    //Accede a la session de la pagina
    username= sessionStorage.getItem("username");
    password= sessionStorage.getItem("password");
   
    request.open('GET', 'http://127.0.0.1:8000/productos/?offset='+offset+'&limit=10', true);
    request.setRequestHeader("Accept", "application/json");
    request.setRequestHeader("Authorization", "Basic " + btoa(username + ":" + password))
    request.setRequestHeader("Content-Type", "application/json");

    const  tabla   = document.getElementById("tabla_productos");

    var tblBody = document.createElement("tbody");
    var tblHead = document.createElement("thead");

    tblHead.innerHTML = `
        <tr>
            <th>Opciones</th>
            <th>Actualizar</th>
            <th>Borrar</th>
            <th>Sku</th>
            <th>Producto</th>
            <th>Precio</th>
        </tr>`;

    request.onload = () => {
        // Almacena la respuesta en una variable, si es 202 es que se obtuvo correctamente
        const response = request.responseText;
        const json = JSON.parse(response);
        console.log("Response " + response);
        console.log("Json " +  json);
        if (request.status === 401 || request.status === 403) {
            alert(json.detail);
            window.location.replace("http://localhost:8080/validate/");
        }
        else if (request.status == 202){
            console.log(request);
            const response = request.responseText;
            const json = JSON.parse(response);
            console.log(json);
            for (let i = 0; i < json.length; i++) {
                var tr = document.createElement('tr');
                var get_producto = document.createElement('td');
                var sku = document.createElement('td');
                var producto = document.createElement('td');
                var precio = document.createElement('td');

                get_producto.innerHTML = "<a href='\\producto\\get\\"+json[i].sku+"'>Ver</a>";
                sku.innerHTML = json[i].sku;
                producto.innerHTML = json[i].producto;
                precio.innerHTML = json[i].precio;

                tr.appendChild(get_producto);
                tr.appendChild(sku);
                tr.appendChild(producto);
                tr.appendChild(precio);
                
                tblBody.appendChild(tr);
            }
            tabla.appendChild(tblHead);
            tabla.appendChild(tblBody);
        }
    };
    request.send();
};
```