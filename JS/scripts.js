function validarLogin()
{
    const name = document.getElementById("userL");
    const psw = document.getElementById("pswL");
    if( name.value.length < 1 || psw.value.length < 1 )
    {
            window.alert("verifique los datos");
    }
}

function validarRegistro()
              {
                  const name = document.getElementById("name");
                  const last_name = document.getElementById("last_name");
                  const email = document.getElementById("email");
                  const number = document.getElementById("number");
                  const psw = document.getElementById("psw");
                  const psw1 = document.getElementById("psw1");
                  if( name.value.length < 1 || last_name.value.length < 1
                   || email.value.length < 1 || number.value.length < 1
                   || psw.value.length < 1 || psw1.value.length < 1
                   || psw.value == psw1.value)
                  {
                          window.alert("verifique los datos");
                  }
              }

function validarTurno()
{
    const oSoc = document.getElementById('obra_social');
    const fec = document.getElementById('fecha');

    if(oSoc.value.length == 0 || !fec.value)
    {
        window.alert("verifique los datos");
    }
}