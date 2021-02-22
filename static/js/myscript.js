// console.log("teste pega valor")
function pegaValor() {
    var total = 0.0;
    if(document.getElementById("agendaservico_form")){
        var valor = document.getElementById("id_valor").value;
        var form = document.getElementsByClassName("field-valor_venda");
        for (let i=0;i < form.length -1 ;i++) {
            var produto = document.getElementById("id_pedido_set-"+i+"-valor_venda").value;
            total = total + parseFloat(produto);
        }
        total = total + parseFloat(valor);
    }
    if(document.getElementById("pagamento_set-group")){
        var le = document.getElementById("pagamento_set-group");
        var href = le.children[0].children[4].children[1].children[1].children[1].children[0].children[0];
        href.addEventListener("click",function(){
            var form = document.getElementById("id_pagamento_set-0-valor");
            form.value = total;
        });
    }
}
window.onload = pegaValor;