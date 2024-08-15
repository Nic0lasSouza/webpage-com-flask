//MONITORA AS MUDANÇAS NO INPUT DO TIPO "FILE"  DENTRO DE UM FORMULARIO A FUNÇÃO É ATIVADA
$('form input[type="file"]').change(event => {
    //ARMAZENA OS ARQUIVOS SELECIONADOS EM UMA VARIAVEL CHAMADA 'ARQUIVOS'
    let arquivos =event.target.files;
    //VERIFICA SE O ARRAY DE ARQUIVOS NÃO ESTÁ VAZIO
    if(arquivos.length == 0){
        console.log('sem imagem pra mostrar')
    } else{
        //VERIFICA SE ARQUIVO É DO TIPO 'JPEG'
        if(arquivos[0].type == 'image/jpeg'){
            //REMOVE QUALQUER IMAGEM EXISTENTE NA PAGINA
            $('img').remove();
            //CRIA UM NOVO ELEMENTO IMG COM CLASSE
            let imagem = $('<img class="img-fluid">');
            //DEFINE A SRC DA IMAGEM COMO O URL TEMPORARIO
            imagem.attr('src', window.URL.createObjectURL(arquivos[0]));
            //INSERE IMAGEM CRIADA DENTRO DE UM ELEMENTO FIGURE NA PAGINA
            $('figure').prepend(imagem);
        }
        else if(arquivos[0].type == 'image/png'){
            //REMOVE QUALQUER IMAGEM EXISTENTE NA PAGINA
            $('img').remove();
            //CRIA UM NOVO ELEMENTO IMG COM CLASSE
            let imagem = $('<img class="img-fluid">');
            //DEFINE A SRC DA IMAGEM COMO O URL TEMPORARIO
            imagem.attr('src', window.URL.createObjectURL(arquivos[0]));
            //INSERE IMAGEM CRIADA DENTRO DE UM ELEMENTO FIGURE NA PAGINA
            $('figure').prepend(imagem);
        } 
        else{
            //ARQUIVO FORA DO FORMATO
            alert('Formato não suportado')
        }
    }
})