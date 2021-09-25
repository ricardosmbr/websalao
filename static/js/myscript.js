// console.log("teste pega valor")
function pegaValor() {
    var total = 0.0;
    function valor(total) {
        if(document.getElementById("agendaservico_form")){
            var valor = document.getElementById("id_valor").value;
            total = total + parseFloat(valor);
            var form = document.getElementsByClassName("field-valor_venda");
            for (let i=0;i < form.length -1 ;i++) {             
                var produto = document.getElementById("id_pedido_set-"+i+"-valor_venda").value;
                total = total + parseFloat(produto);
            }
            return total;
        }
    }

    if(document.getElementById("pagamento_set-group")){

        var le = document.getElementById("pagamento_set-group");
        var href = le.children[0].children[4].children[1].children[1].children[1].children[0].children[0];
        href.addEventListener("click",function(){
            total = total + valor(total);
            var form = document.getElementById("id_pagamento_set-0-valor");
            form.value = total;
        });
    }
}
window.onload = pegaValor;