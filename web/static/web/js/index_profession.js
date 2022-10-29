document.getElementById('section_codage').classList.add('d-none');
document.getElementById('statut').classList.add('d-none');
document.getElementById('pub').classList.add('d-none');
document.getElementById('position_pub').classList.add('d-none');
document.getElementById('position_priv').classList.add('d-none');
document.getElementById('nbsal').classList.add('d-none');
document.getElementById('bouton_coder').classList.add('d-none');

var hit = null;
var arbreDoc = null;

const couleurCodeArbre = [
    {min: '#ffffff', max: '#ffffff', med: '#ffffff'},
    {min: '#e2c0d5', max: '#6a3155', med: '#b25991'},
    {min: '#bdd3f2', max: '#18427c', med: '#286ac7'},
    {min: '#c0f4d8', max: '#105a31', med: '#1ca459'},
    {min: '#fff0bd', max: '#c49700', med: '#ffc300'},
    {min: '#fbdbc1', max: '#b4550b', med: '#f59042'},
    {min: '#f7c4cd', max: '#af133c', med: '#e4003a'}
] ;

const codeGS = ['0', '1', '2', '3', '4', '5', '6'] ;

const tagsCode= ['pub_catA', 'pub_catB', 'pub_catC', 'pub_nr', 'priv_onq', 'priv_oq', 'priv_emp', 'priv_am', 'priv_tec', 'priv_cad', 'priv_nr', 'inde_0_9', 'inde_10_49', 'inde_sup49', 'inde_nr', 'aid_fam', 'ssvaran'] ;


const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]')  ;
const popoverList = [...popoverTriggerList].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl).show()) ;

var largeTree = false ;
if(window.innerWidth <= 768){
    document.getElementById("arbresvg").setAttribute('data', NG_STATIC_FILES.LONG_TREE);
}else{
    largeTree = true ;
    document.getElementById("arbresvg").setAttribute('data', NG_STATIC_FILES.LARGE_TREE);
}

document.getElementById("arbresvg").onload = function() {
    arbreDoc = document.getElementById("arbresvg").contentDocument;
}

addEventListener('resize', (event) => {
    var change = false ;
    if((window.innerWidth <= 768 ) && largeTree){
        largeTree = false ;
        change = true ;
        document.getElementById("arbresvg").setAttribute('data', NG_STATIC_FILES.LONG_TREE);
    }else if((window.innerWidth > 768 ) && !largeTree){
        largeTree = true ;
        change = true ;
        document.getElementById("arbresvg").setAttribute('data', NG_STATIC_FILES.LARGE_TREE);
    }

    if(change){
        var statut = document.getElementById("statut").querySelector('option:checked').value;
        var pub = document.getElementById("pub").querySelector('option:checked').value;
        var cpf_pub = document.getElementById("position_pub").querySelector('option:checked').value;
        var cpf_priv = document.getElementById("position_priv").querySelector('option:checked').value;
        var nbsal = document.getElementById("nbsal").querySelector('option:checked').value;
        construireArbre(statut, pub, cpf_pub, cpf_priv, nbsal);
    }
});


document.addEventListener('click', function (event) {
    if (!event.target.classList.contains("search-auto-item")) {
        cleanAucompletionProfList();
    }
});

document.getElementById("bouton_coder").addEventListener('click', function () {
    coder();
});

document.getElementById("nav-arbre-tab").addEventListener('click', function () {
    document.getElementById('section_codage').scrollIntoView({behavior: "auto", block: "start"});
});

document.getElementById("nav-code-tab").addEventListener('click', function () {
    document.getElementById('section_codage').scrollIntoView({behavior: "auto", block: "start"});
});

document.getElementById("libelle").addEventListener('input', function () {
    document.getElementById('section_codage').classList.add('d-none');
    suggestProf(this.value);
    testStrict(this.value);
});

document.getElementById("libelle").addEventListener('click', function () {
    document.getElementById('section_codage').classList.add('d-none');
    suggestProf(this.value);
    testStrict(this.value);
});


function changerSexe(valeurSexe) {
    document.getElementById('sexe').value = valeurSexe;
    if (valeurSexe == 0) {
        document.getElementById('homme').style.color =  '#286AC7' ;
        document.getElementById('femme').style.color =  '#B0AEAE' ;
    } else {
        document.getElementById('homme').style.color = '#B0AEAE' ;
        document.getElementById('femme').style.color = '#286AC7';
    }
    if(hit != null){
        var genre = getGenre();
        if(genre == 'masculin'){
            document.getElementById('libelle').value = hit['libelle_masculinise'];
        }else{
            if(hit.libelle_feminise == undefined || hit.libelle_feminise == null){
                changerSexe(0);
            }else{
                document.getElementById('libelle').value = hit['libelle_feminise'];
            }
        }
    }
}



function testStrict(libelle){
    var genre = getGenre();
    
    var reqBody = { libelle: libelle, genre: genre} ;
    reqBody = JSON.stringify(reqBody);
    const request = new Request('/api/profession_stricte/', {method: 'POST', body:  reqBody, headers: {'Content-Type': 'application/json'}});
    fetch(request).then(response => {
        if(response.status === 200 ){
           return response.json()  ;
        } else { 
            throw new Error('Erreur pour échanger avec l\'API');
        }
    }).then(data => updateMessageStrict(data)) ;
}

function getGenre() {
    var genre = 'masculin';
    if (document.getElementById('sexe').value == 1) {
        genre = 'feminin';
    }
    return genre;
}

function suggestProf(value) {
    var genre = getGenre();
    
    var reqBody = { libelle: value, genre: genre} ;
    reqBody = JSON.stringify(reqBody);
    const request = new Request('/api/profession_auto/', {method: 'POST', body:  reqBody, headers: {'Content-Type': 'application/json'}});
    fetch(request).then(response => {
        if(response.status === 200 ){
            return response.json() ; 
        } else { 
            throw new Error('Erreur pour échanger avec l\'API');
        }
    }).then(data => showSuggestionsProf(data)) ;
}

function strictProf(value) {
    var reqBody = { id: value};
    reqBody = JSON.stringify(reqBody);
    const request = new Request('/api/profession_id/', {method: 'POST', body:  reqBody, headers: {'Content-Type': 'application/json'}});
    fetch(request).then(
        response => {
        if(response.status === 200 ){
            return response.json() ;
        } else { 
            throw new Error('Erreur pour échanger avec l\'API');
        }
    }).then(data => updateListeStrictElement(data)) ;
}

function showSuggestionsProf(data) {
    var div = '';
    data['echos'].forEach(function (suggestion) {
        var texteFormate = '';
        if (document.getElementById('sexe').value == 0) {
            texteFormate = suggestion.libelle_masculinise_formate;
        } else {
            texteFormate = suggestion.libelle_feminise_formate;
        }
        div += ('<li class="list-group-item list-group-item-action pl-4 pt-1 pb-1 pr-4 m-0 search-auto-item" onmouseover="this.style.background=\'#8DB0E1\';" onmouseout="this.style.background=\'\';this.style.color=\'\';" onclick="autocompletionProfChoix('+suggestion.id.toString()+')"><small>' + texteFormate + '</small></li>');
    });
    document.getElementById('search_auto').innerHTML = div;
}

function autocompletionProfChoix(id) {
    cleanAucompletionProfList();
    strictProf(id);
}

function cleanAucompletionProfList() {
    Array.from(document.querySelectorAll('#search_auto > li')).map(e => e.parentNode.removeChild(e));
}

function updateMessageStrict(data){
    document.getElementById('formulaire_index').classList.remove('needs-validation');
    document.getElementById('formulaire_index').classList.remove('was-validated');
    var echos = data['echos'];
    if (data['nb_echos'] == 0) {
        hit = null;
        document.getElementById('libelle_validite').classList.remove('valid-feedback');
        document.getElementById('libelle_validite').classList.add('invalid-feedback');
        document.getElementById('libelle').classList.remove('is-valid');
        document.getElementById('libelle').classList.add('is-invalid');
        document.getElementById('libelle_validite').innerHTML = 'Le libellé saisi est bien dans la liste.' ;
        if (document.getElementById('libelle').value.length == 0) {
            document.getElementById('libelle_validite').innerHTML  = 'Veuillez saisir un libellé.';
        } else {
            document.getElementById('libelle_validite').innerHTML = 'Le libellé saisi n\'est pas dans la liste.';
        }
        document.getElementById('statut').classList.add('d-none');
        document.getElementById('pub').classList.add('d-none');
        document.getElementById('position_pub').classList.add('d-none');
        document.getElementById('position_priv').classList.add('d-none');
        document.getElementById('nbsal').classList.add('d-none');
        document.getElementById('bouton_coder').classList.add('d-none');
    } else {
        if(echos.length > 1){
            hit = null;
            document.getElementById('statut').classList.add('d-none');
            document.getElementById('pub').classList.add('d-none');
            document.getElementById('position_pub').classList.add('d-none');
            document.getElementById('position_priv').classList.add('d-none');
            document.getElementById('nbsal').classList.add('d-none');
            document.getElementById('bouton_coder').classList.add('d-none');
        }else{
            hit = echos[0];
            depilerVariablesAnnexes();
        }
        
        var genre = getGenre();
        if(genre == 'masculin'){
            document.getElementById('libelle').value = hit.libelle_masculinise;
        }else{
            document.getElementById('libelle').value =  hit.libelle_feminise;
        }
        document.getElementById('libelle_validite').classList.remove('invalid-feedback');
        document.getElementById('libelle_validite').classList.add('valid-feedback');
        document.getElementById('libelle').classList.remove('is-invalid');
        document.getElementById('libelle').classList.add('is-valid');
        document.getElementById('libelle_validite').innerHTML = 'Le libellé saisi est bien dans la liste.' ;
    }
}

function updateListeStrictElement(data) {
    var resultat = data['echo'];
    if (resultat === null ||  resultat === undefined) {
        hit = null;
        document.getElementById('statut').classList.add('d-none');
        document.getElementById('pub').classList.add('d-none');
        document.getElementById('position_pub').classList.add('d-none');
        document.getElementById('position_priv').classList.add('d-none');
        document.getElementById('nbsal').classList.add('d-none');
        document.getElementById('bouton_coder').classList.add('d-none');
    } else {
        hit = resultat;
        var genre = getGenre();
        if(genre == 'masculin'){
            document.getElementById('libelle').value = hit.libelle_masculinise ;
        }else{
            document.getElementById('libelle').value =  hit.libelle_feminise ;
        }
        document.getElementById('libelle_validite').classList.remove('invalid-feedback');
        document.getElementById('libelle_validite').classList.add('valid-feedback');
        document.getElementById('libelle').classList.remove('is-invalid');
        document.getElementById('libelle').classList.add('is-valid');
        document.getElementById('libelle_validite').innerHTML = 'Le libellé saisi est bien dans la liste.' ;
        depilerVariablesAnnexes();
    }
}


function depilerVariablesAnnexes() {
    if (document.getElementById('section_codage').classList.contains('visible')) {
        coder();
    }
    document.getElementById('statut').classList.remove('d-none');
    var statut = document.getElementById("statut").querySelector('option:checked').value;
    document.getElementById('bouton_coder').classList.remove('d-none');
    if (statut == 0) {
        document.getElementById('pub').classList.add('d-none');
        document.getElementById('position_pub').classList.add('d-none');
        document.getElementById('position_priv').classList.add('d-none');
        document.getElementById('nbsal').classList.add('d-none');
    } else if (statut == 1) {
        document.getElementById('pub').classList.add('d-none');
        document.getElementById('position_pub').classList.add('d-none');
        document.getElementById('position_priv').classList.add('d-none');
        document.getElementById('nbsal').classList.remove('d-none');
    } else if (statut == 2) {
        var pub = document.getElementById("pub").querySelector('option:checked').value;
        document.getElementById('pub').classList.remove('d-none');
        document.getElementById('nbsal').classList.add('d-none');
        if (pub == 1) {
            document.getElementById('position_priv').classList.add('d-none');
            document.getElementById('position_pub').classList.remove('d-none');
            
        } else {
            document.getElementById('position_pub').classList.add('d-none');
            document.getElementById('position_priv').classList.remove('d-none');
            
        }
    } else {
        document.getElementById('pub').classList.add('d-none');
        document.getElementById('position_pub').classList.add('d-none');
        document.getElementById('position_priv').classList.add('d-none');
        document.getElementById('nbsal').classList.add('d-none');
    }
}

function getCode(statut, pub, cpf_pub, cpf_priv, nbsal) {
    if (statut == 0) {
        return hit['ssvaran'];
    } else if (statut == 1) {
        if (nbsal == 0) {
            return hit['inde_nr'];
        } else if (nbsal == 1) {
            return hit['inde_0_9'];
        } else if (nbsal == 2) {
            return hit['inde_10_49'];
        } else {
            return hit['inde_sup49'];
        }
    } else if (statut == 2) {
        if (pub == 1) {
            if (cpf_pub == 0) {
                return hit['pub_nr'];
            } else if (cpf_pub == 1) {
                return hit['pub_catA'];
            } else if (cpf_pub == 2) {
                return hit['pub_catB'];
            } else {
                return hit['pub_catC'];
            }
        } else {
            if (cpf_priv == 0) {
                return hit['priv_nr'];
            } else if (cpf_priv == 1) {
                return hit['priv_onq'];
            } else if (cpf_priv == 2) {
                return hit['priv_oq'];
            } else if (cpf_priv == 3) {
                return hit['priv_emp'];
            } else if (cpf_priv == 4) {
                return hit['priv_am'];
            } else if (cpf_priv == 5) {
                return hit['priv_tec'];
            } else {
                return hit['priv_cad'];
            }
        }
    } else {
        return hit['aid_fam'];
    }
}

function feedCodage(code, data) {
    var body = '';
    body += '<div id="complement_pcs">';
    body += '<div class="pt-3 px-2 pb-2 rounded"  style="background-color: #0F417A;"><div class="row"><div class="col-auto"><h4><span class="badge bg-light" style="color: black ;">' + code + '</span></h4></div><div class="col"><h4 style="color: white;">' + data.intitule + '</h4></div></div></div>';


    if (data.description) {
        body += '<div class="shadow-none p-3 bg-light rounded">';
        body += '<h5>Description</h5>';
        body += '<small>' + data.description + '</small>';
        if (data.professions_typiques) {
            body += '<h5>Libellés les plus fréquents</h5>';
            body += '<ul>'
            data.professions_typiques.forEach(function (x) {
                body += '<li><small>' + x + '</small></li>';
            });
            body += '</ul>'
        }
        if (data.autres_professions) {
            body += '<h5>Autres exemples de libellés</h5>';
            body += '<ul>'
            data.autres_professions.forEach(function (x) {
                body += '<li><small>' + x + '</small></li>';
            });
            body += '</ul>'
            body += '</div>';
        }
        body += '</div>'
    }
    document.getElementById('nav-code').innerHTML = body ;
}

function getCorrectTextColor(hexcolor){
    hexcolor = hexcolor.replace("#", "");
    var r = parseInt(hexcolor.substr(0,2),16);
    var g = parseInt(hexcolor.substr(2,2),16);
    var b = parseInt(hexcolor.substr(4,2),16);
    var yiq = ((r*299)+(g*587)+(b*114))/1000;
    return (yiq >= 128) ? 'black' : 'white';
}

function getUniqueCodeLibelle(hit){
    var uniqueCodes = new Set();
    tagsCode.forEach(function (x) {
        uniqueCodes.add(hit[x]) ; 
    });
    return uniqueCodes;

}


function determinerCouleursFeuilles() {
    var uniqueCode = Array.from(getUniqueCodeLibelle(hit));
    const nbCodeParGS = [...new Set(uniqueCode.map(x => x.substring(0,1)))] ;
    return  Object.fromEntries(nbCodeParGS.map(gs => {
        if(gs == 'r'){
            return [{code: 'r', couleur: '#ffffff'}]
        }else{
                var codesGS = uniqueCode.filter(c => c.substring(0,1) == gs) ;
                codesGS.sort() ;
                
                if(codesGS.length == 1){
                    return [{code: codesGS[0]+"", couleur:couleurCodeArbre[parseInt(gs)].med}] ;
                }else if(codesGS.length == 2){
                    return [{code: codesGS[0]+"", couleur: couleurCodeArbre[parseInt(gs)].min}, 
                        {code: codesGS[1]+"", couleur: couleurCodeArbre[parseInt(gs)].med}];
                }else{
                    var colorsChroma =  chroma.scale(
                        [couleurCodeArbre[parseInt(gs)].min,couleurCodeArbre[parseInt(gs)].max]
                    ).mode('lch').colors(codesGS.length) ;
                    return colorsChroma.map((e,i) => {return {code: codesGS[i], couleur: e}})
                }
        }
    }).flat(1).reduce(
        (accumulateur, valeurCourante) => accumulateur.set(
            valeurCourante.code, {background:valeurCourante.couleur, text:getCorrectTextColor(valeurCourante.couleur)}
        ), new Map() 
    ));

}



function colorierFeuille() {
    var codes_couleurs = determinerCouleursFeuilles();

    var output_pcs = ['pub_catA', 'pub_catB', 'pub_catC', 'pub_nr', 'priv_onq', 'priv_oq', 'priv_emp', 'priv_am', 'priv_tec', 'priv_cad', 'priv_nr', 'inde_0_9', 'inde_10_49', 'inde_sup49', 'inde_nr', 'aid_fam', 'ssvaran'];
    var c = null;
    output_pcs.forEach(function (x) {
        c = hit[x];
        if (c == 'r') {
            arbreDoc.querySelector('#label_node_' + x).innerHTML = 'REPR';
        } else {
            arbreDoc.querySelector('#label_node_' + x).innerHTML = c;
        }
        arbreDoc.querySelector('#node_' + x).style.fill = codes_couleurs[c].background;
        arbreDoc.querySelector('#label_node_' + x).style.fill = codes_couleurs[c].text;
    });
    
    document.getElementById('legende_tree').innerHTML =  '<h6>Légende: </h6>';
    
    codes_tries = Object.keys(codes_couleurs) ;
    codes_tries.sort() ;
    codes_tries.forEach( code => {
        if (code == 'r') {
            document.getElementById('legende_tree').innerHTML += '<div class="row"><div class="col-auto"><span class="badge badge-light" style="background-color: ' + codes_couleurs[code].background + '; color: '+codes_couleurs[code].text +'">REPR</span></div><div class="col"><p>Code d\'envoi en reprise (utilisation des variables contextuelles nécessaire)</p></div></div>' ;
        } else {
            var cp = code + "";
            document.getElementById('legende_tree').innerHTML +=  '<div class="row"><div class="col-auto"><span class="badge badge-light" style="background-color: ' + codes_couleurs[code].background + '; color: '+codes_couleurs[code].text +'">' + code + '</span></div><div id="legende_item_'+code+'" class="col"><p> </p></div></div>' ;
            var reqBody = {code_pcs:cp.replace(/0+$/, "")} ;
            reqBody = JSON.stringify(reqBody);
            const request = new Request('/api/poste_pcs/', {method: 'POST', body:  reqBody, headers: {'Content-Type': 'application/json'}});
            fetch(request).then(response => {
                if(response.status === 200 ){
                    return response.json() ;
                } else { 
                    throw new Error('Erreur pour échanger avec l\'API');
                }
            }).then(data => document.getElementById('legende_item_'+code).innerHTML =  '<p>' + data.echo.intitule + '</p>') ;
        }
    });
}

function colorierLineSVG(ids, svg, hex){
    ids.forEach((id) => {
        el = svg.getElementById(id) ;
        if(!(el === null)){
            el.style.stroke = hex;
        }
    })
}

function colorierChemin(statut, pub, cpf_pub, cpf_priv, nbsal) {
    var liste_path = ['path_nr', 'path_inde', 'path_taille_nr', 'path_taille1', 'path_taille2',
    'path_taille3', 'path_salarie', 'path_pub', 'path_pub_nr', 'path_catA', 'path_catB',
    'path_catC', 'path_priv', 'path_priv_nr', 'path_onq', 'path_oq', 'path_emp','path_am',
    'path_tec','path_cad','path_aide',
    'path_statut_1','path_statut_2','path_statut_3','path_statut_4',
    'path_salarie_1', 'path_salarie_2',
    'path_pub_1', 'path_pub_2', 'path_pub_3', 'path_pub_4',
    'path_priv_1', 'path_priv_2', 'path_priv_3', 'path_priv_4','path_priv_5','path_priv_6', 'path_priv_7',
    'path_priv_1', 'path_priv_2', 'path_priv_3', 'path_priv_4','path_priv_5','path_priv_6', 'path_priv_7',
    'path_inde_1', 'path_inde_2', 'path_inde_3', 'path_inde_4'
    ];
    colorierLineSVG(liste_path, arbreDoc,'#B0AEAE');


    if (statut == 0) {
        colorierLineSVG(['path_nr', 'path_statut_1', 'path_statut_2', 'path_statut_3', 'path_statut_4'], arbreDoc,'#000000');
    } else if (statut == 1) {
        colorierLineSVG(['path_inde', 'path_statut_1', 'path_statut_2'], arbreDoc,'#000000');
        if (nbsal == 0) {
            colorierLineSVG(['path_taille_nr', 'path_inde_1', 'path_inde_2', 'path_inde_3', 'path_inde_4'], arbreDoc,'#000000');
        } else if (nbsal == 1) {
            colorierLineSVG(['path_taille1', 'path_inde_1'], arbreDoc,'#000000');
        } else if (nbsal == 2) {
            colorierLineSVG(['path_taille2', 'path_inde_1', 'path_inde_2'], arbreDoc,'#000000');
        } else {
            colorierLineSVG(['path_taille3', 'path_inde_1', 'path_inde_2', 'path_inde_3'], arbreDoc,'#000000');
        }
    } else if (statut == 2) {
        colorierLineSVG(['path_salarie', 'path_statut_1'], arbreDoc,'#000000');
        if (pub == 1) {
            colorierLineSVG(['path_pub', 'path_salarie_1'], arbreDoc,'#000000');
            if (cpf_pub == 0) {
                colorierLineSVG(['path_pub_nr', 'path_pub_1', 'path_pub_2', 'path_pub_3', 'path_pub_4'], arbreDoc,'#000000');
            } else if (cpf_pub == 1) {
                colorierLineSVG(['path_catA', 'path_pub_1'], arbreDoc,'#000000');
            } else if (cpf_pub == 2) {
                colorierLineSVG(['path_catB', 'path_pub_1', 'path_pub_2'], arbreDoc,'#000000');
            } else {
                colorierLineSVG(['path_catC', 'path_pub_1', 'path_pub_2', 'path_pub_3'], arbreDoc,'#000000');
            }
        } else {
            colorierLineSVG(['path_priv', 'path_salarie_1', 'path_salarie_2'], arbreDoc,'#000000');
            if (cpf_priv == 0) {
                colorierLineSVG(['path_priv_nr', 'path_priv_1', 'path_priv_2', 'path_priv_3', 'path_priv_4', 'path_priv_5', 'path_priv_6', 'path_priv_7'], arbreDoc,'#000000');
            } else if (cpf_priv == 1) {
                colorierLineSVG(['path_onq', 'path_priv_1'], arbreDoc,'#000000');
            } else if (cpf_priv == 2) {
                colorierLineSVG(['path_oq', 'path_priv_1', 'path_priv_2'], arbreDoc,'#000000');
            } else if (cpf_priv == 3) {
                colorierLineSVG(['path_emp', 'path_priv_1', 'path_priv_2', 'path_priv_3'], arbreDoc,'#000000');
            } else if (cpf_priv == 4) {
                colorierLineSVG(['path_am', 'path_priv_1', 'path_priv_2', 'path_priv_3', 'path_priv_4'], arbreDoc,'#000000');
            } else if (cpf_priv == 5) {
                colorierLineSVG(['path_tec', 'path_priv_1', 'path_priv_2', 'path_priv_3', 'path_priv_4', 'path_priv_5'], arbreDoc,'#000000');
            } else {
                colorierLineSVG(['path_cad', 'path_priv_1', 'path_priv_2', 'path_priv_3', 'path_priv_4', 'path_priv_5', 'path_priv_6'], arbreDoc,'#000000');
            }
        }
    } else {
        colorierLineSVG(['path_aide', 'path_statut_1', 'path_statut_2', 'path_statut_3'], arbreDoc,'#000000');
    }
}


function construireArbre(statut, pub, cpf_pub, cpf_priv, nbsal) {
    if (arbreDoc == null){
        document.getElementById("arbresvg").addEventListener("load",function() {
            arbreDoc = document.getElementById("arbresvg").contentDocument;
                colorierFeuille();
                colorierChemin(statut, pub, cpf_pub, cpf_priv, nbsal);
        }, false);
    }else{
        colorierFeuille();
        colorierChemin(statut, pub, cpf_pub, cpf_priv, nbsal);
    }
}

function coder() {
    document.getElementById('section_codage').classList.remove('d-none');


    var statut = document.getElementById("statut").querySelector('option:checked').value;
    var pub = document.getElementById("pub").querySelector('option:checked').value;
    var cpf_pub = document.getElementById("position_pub").querySelector('option:checked').value;
    var cpf_priv = document.getElementById("position_priv").querySelector('option:checked').value;
    var nbsal = document.getElementById("nbsal").querySelector('option:checked').value;

    var code = getCode(statut, pub, cpf_pub, cpf_priv, nbsal);

    if (code == 'r') {
        feedCodage('REPR', { intitule: 'Code d\'envoi en reprise (utilisation des variables contextuelles nécessaire)' });
    } else {
        var reqBody = { code_pcs: code.replace(/0+$/, "") } ;
        reqBody = JSON.stringify(reqBody);
        const request = new Request('/api/poste_pcs/', {method: 'POST', body:  reqBody, headers: {'Content-Type': 'application/json'}});
        fetch(request).then(response => {
            if(response.status === 200 ){
                return response.json() ;
            } else { 
                throw new Error('Erreur pour échanger avec l\'API');
            }
        }).then(data => {
            feedCodage(code, data['echo']);
            document.getElementById('section_codage').scrollIntoView({behavior: "smooth", block: "start"});
    
        }) ;
    }
    construireArbre(statut, pub, cpf_pub, cpf_priv, nbsal);
}


function transformerLibelleSexe(data) {
    var resultat = data['echo'];
    if (resultat === undefined) {
        resultat = null;
    } 
    if (!(resultat === null)) {
        var genre = getGenre();
        document.getElementById('libelle').value = resultat['lib' + genre.substring(0,1)];
    }
}




var triggerTabList = [].slice.call(document.querySelectorAll('#nav-tab a'))
triggerTabList.forEach(function (triggerEl) {
  var tabTrigger = new bootstrap.Tab(triggerEl)

  triggerEl.addEventListener('click', function (event) {
    event.preventDefault()
    tabTrigger.show()
  })
})

