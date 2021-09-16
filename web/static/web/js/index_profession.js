$('#section_codage').hide();
$('#statut').hide();
$('#pub').hide();
$('#position_pub').hide();
$('#position_priv').hide();
$('#nbsal').hide();
$('#bouton_coder').hide();
var hit = null;
var arbreDoc = null;

document.getElementById("arbresvg").onload = function() {
    arbreDoc = document.getElementById("arbresvg").contentDocument;
}

$(document).on('click', function (event) {
    if (!$(event.target).closest('#search_auto').length) {
        cleanAucompletionProfList();
    }
});

$("#libelle").on('input click', function () {
    $('#section_codage').hide();
    suggestProf($(this).val());
    testStrict($(this).val());
});


function changerSexe(valeurSexe) {
    $('#sexe').val(valeurSexe);
    if (valeurSexe == 0) {
        $('#homme').css({ 'color': '#286AC7' });
        $('#femme').css({ 'color': '#B0AEAE' });
    } else {
        $('#homme').css({ 'color': '#B0AEAE' });
        $('#femme').css({ 'color': '#286AC7' });
    }
    if(hit != null){
        var genre = getGenre();
        if(genre == 'masculin'){
            $('#libelle').val(hit['libelle_masculinise']);
        }else{
            if(hit.libelle_feminise == undefined || hit.libelle_feminise == null){
                changerSexe(0);
            }else{
                $('#libelle').val(hit['libelle_feminise']);
            }
        }
    }
}




function testStrict(libelle){
    var genre = getGenre();
    $.post("/api/profession_stricte/", { libelle: libelle, genre: genre}, function (data) {
        updateMessageStrict(data);
    })
}

function getGenre() {
    var genre = 'masculin';
    if ($('#sexe').val() == 1) {
        genre = 'feminin';
    }
    return genre;
}

function suggestProf(value) {
    var genre = getGenre();
    $.post("/api/profession_auto/", { libelle: value, genre: genre}, function (data) {
        showSuggestionsProf(data);
    });
}

function strictProf(value) {
    $.post("/api/profession_id/", { id: value}, function (data) {
        updateListeStrictElement(data);
    });
}

function showSuggestionsProf(data) {
    var div = '';
    data['echos'].forEach(function (suggestion) {
        var texteFormate = '';
        if ($('#sexe').val() == 0) {
            texteFormate = suggestion.libelle_masculinise_formate;
        } else {
            texteFormate = suggestion.libelle_feminise_formate;
        }
        div += ('<li class="list-group-item list-group-item-action pl-4 pt-1 pb-1 pr-4 m-0" onmouseover="this.style.background=\'#8DB0E1\';" onmouseout="this.style.background=\'\';this.style.color=\'\';" onclick="autocompletionProfChoix('+suggestion.id.toString()+')"><small>' + texteFormate + '</small></li>');
    });
    $('#search_auto').html(div);
}

function autocompletionProfChoix(id) {
    cleanAucompletionProfList();
    strictProf(id);
}

function cleanAucompletionProfList() {
    $('#search_auto > li').remove();
}

function updateMessageStrict(data){
    $('#formulaire_index').removeClass('needs-validation');
    $('#formulaire_index').removeClass('was-validated');
    var echos = data['echos'];
    if (data['nb_echos'] == 0) {
        hit = null;
        $('#libelle_validite').removeClass('valid-feedback');
        $('#libelle_validite').addClass('invalid-feedback');
        $('#libelle').removeClass('is-valid');
        $('#libelle').addClass('is-invalid');
        $('#libelle_validite').html('Le libellé saisi est bien dans la liste.');
        if ($('#libelle').val().length == 0) {
            $('#libelle_validite').html('Veuillez saisir un libellé.');
        } else {
            $('#libelle_validite').html('Le libellé saisi n\'est pas dans la liste.');
        }
        $('#statut').hide();
        $('#pub').hide();
        $('#position_pub').hide();
        $('#position_priv').hide();
        $('#nbsal').hide();
        $('#bouton_coder').hide();
    } else {
        if(echos.length > 1){
            hit = null;
            $('#statut').hide();
            $('#pub').hide();
            $('#position_pub').hide();
            $('#position_priv').hide();
            $('#nbsal').hide();
            $('#bouton_coder').hide();
        }else{
            hit = echos[0];
            depilerVariablesAnnexes();
        }
        
        var genre = getGenre();
        if(genre == 'masculin'){
            $('#libelle').val(hit.libelle_masculinise);
        }else{
            $('#libelle').val(hit.libelle_feminise);
        }
        $('#libelle_validite').removeClass('invalid-feedback');
        $('#libelle_validite').addClass('valid-feedback');
        $('#libelle').removeClass('is-invalid');
        $('#libelle').addClass('is-valid');
        $('#libelle_validite').html('Le libellé saisi est bien dans la liste.');
        
    }
}

function updateListeStrictElement(data) {
    var resultat = data['echo'];
    if (resultat === null ||  resultat === undefined) {
        hit = null;
        $('#statut').hide();
        $('#pub').hide();
        $('#position_pub').hide();
        $('#position_priv').hide();
        $('#nbsal').hide();
        $('#bouton_coder').hide();

    } else {
        hit = resultat;
        var genre = getGenre();
        if(genre == 'masculin'){
            $('#libelle').val(hit.libelle_masculinise);
        }else{
            $('#libelle').val(hit.libelle_feminise);
        }
        $('#libelle_validite').removeClass('invalid-feedback');
        $('#libelle_validite').addClass('valid-feedback');
        $('#libelle').removeClass('is-invalid');
        $('#libelle').addClass('is-valid');
        $('#libelle_validite').html('Le libellé saisi est bien dans la liste.');
        depilerVariablesAnnexes();
    }
}


function depilerVariablesAnnexes() {
    if ($('#section_codage').is(':visible')) {
        coder();
    }
    $('#statut').show();
    var statut = $('#statut > select > option:selected').val();
    $('#bouton_coder').show();
    if (statut == 0) {
        $('#pub').hide();
        $('#position_pub').hide();
        $('#position_priv').hide();
        $('#nbsal').hide();
    } else if (statut == 1) {
        $('#pub').hide();
        $('#position_pub').hide();
        $('#position_priv').hide();
        $('#nbsal').show();
    } else if (statut == 2) {
        var pub = $('#pub > select > option:selected').val();
        $('#pub').show();
        $('#nbsal').hide();
        if (pub == 1) {
            $('#position_priv').hide();
            $('#position_pub').show();
        } else {
            $('#position_priv').show();
            $('#position_pub').hide();
        }
    } else {
        $('#pub').hide();
        $('#position_pub').hide();
        $('#position_priv').hide();
        $('#nbsal').hide();
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
    var body_data = '';
    body += '<div id="complement_pcs">';
    body += '<div class="p-3 rounded"  style="background-color: #0F417A;"><div class="row"><div class="col-auto"><h4><span class="badge badge-light">' + code + '</span></h4></div><div class="col"><h4 style="color: white;">' + data.intitule + '</h4></div></div></div>';


    if (data.description) {
        body += '<div class="shadow-none p-3 bg-light rounded">';
        body += '<h5>Description</h5>';
        body += '<small>' + data.description + '</small>';
        if (data.professions_typiques) {
            body += '<h5>Professions les plus typiques</h5>';
            body += '<ul>'
            data.professions_typiques.forEach(function (x) {
                body += '<li><small>' + x + '</small></li>';
            });
            body += '</ul>'
        }
        if (data.professions_exclues) {
            body += '<h5>Professions exclues</h5>';
            body += '<ul>'
            data.professions_exclues.forEach(function (x) {
                body += '<li><small>' + x + '</small></li>';
            });
            body += '</ul>'
            body += '</div>';
        }
        body += '</div>'
    }
    $('#nav-code').html(body);
}

function determinerCouleursFeuilles() {
    var codes_couleurs = {};
    var taille = 0;
    var output_pcs = ['pub_catA', 'pub_catB', 'pub_catC', 'pub_nr', 'priv_onq', 'priv_oq', 'priv_emp', 'priv_am', 'priv_tec', 'priv_cad', 'priv_nr', 'inde_0_9', 'inde_10_49', 'inde_sup49', 'inde_nr', 'aid_fam', 'ssvaran'];
    var couleurs = ['#286AC7', '#FFC300', '#C4E1FF', '#FDF0C9', '#E4003A', '#1CA459', '#F5B8C2', '#8BC8A4', '#954577', '#0C6876', '#CA8CB3', '#97CFD0', '#0C3A5A', '#D98C07', '#AD1638', '#068043', '#633251', '#0C6876'];
    var c = null;
    output_pcs.forEach(function (x) {
        c = hit[x];
        if (!codes_couleurs.hasOwnProperty(c)) {
            codes_couleurs[c] = couleurs[taille];
            taille = taille + 1;
        }
    });
    return codes_couleurs;
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
        arbreDoc.querySelector('#node_' + x).style.fill = codes_couleurs[c];
    });
    
    $('#legende_tree').html('<h6>Légende: </h6>');
    for (const code in codes_couleurs) {
        if (code == 'r') {
            $('#legende_tree').append('<div class="row"><div class="col-auto"><span class="badge badge-light" style="background-color: ' + codes_couleurs[code] + '">REPR</span></div><div class="col"><p>Code d\'envoi en reprise (utilisation des variables contextuelles nécessaire)</p></div></div>');
        } else {
            $.ajax({
                url: '/api/poste_pcs/',
                data: {code_pcs:code},
                method: 'POST',
                success: function (data) {
                    $('#legende_tree').append('<div class="row"><div class="col-auto"><span class="badge badge-light" style="background-color: ' + codes_couleurs[code] + '">' + code + '</span></div><div class="col"><p>' + data.echo.intitule + '</p></div></div>');
                }

            });
        }
    }
}


function colorierChemin(statut, pub, cpf_pub, cpf_priv, nbsal) {
    var liste_path = ['path_nr', 'path_inde', 'path_taille_nr', 'path_taille1', 'path_taille2', 'path_taille3', 'path_salarie', 'path_pub', 'path_pub_nr', 'path_catA', 'path_catB', 'path_catC', 'path_priv', 'path_priv_nr', 'path_onq', 'path_oq', 'path_emp','path_am','path_tec','path_cad','path_aide'];
    liste_path.forEach(function(c){
        arbreDoc.getElementById(c).style.stroke = '#B0AEAE';
    })
    if (statut == 0) {
        arbreDoc.querySelector('#path_nr').style.stroke = "#000000";
    } else if (statut == 1) {
        arbreDoc.querySelector("#path_inde").style.stroke = '#000000';
        if (nbsal == 0) {
            arbreDoc.querySelector("#path_taille_nr").style.stroke = '#000000';
        } else if (nbsal == 1) {
            arbreDoc.querySelector("#path_taille1").style.stroke = '#000000';
        } else if (nbsal == 2) {
            arbreDoc.querySelector("#path_taille2").style.stroke = '#000000';
        } else {
            arbreDoc.querySelector("#path_taille3").style.stroke = '#000000';
        }
    } else if (statut == 2) {
        arbreDoc.querySelector("#path_salarie").style.stroke = '#000000';
        if (pub == 1) {
            arbreDoc.querySelector("#path_pub").style.stroke = '#000000';
            if (cpf_pub == 0) {
                arbreDoc.querySelector("#path_pub_nr").style.stroke = '#000000';
            } else if (cpf_pub == 1) {
                arbreDoc.querySelector("#path_catA").style.stroke = '#000000';
            } else if (cpf_pub == 2) {
                arbreDoc.querySelector("#path_catB").style.stroke = '#000000';
            } else {
                arbreDoc.querySelector("#path_catC").style.stroke = '#000000';
            }
        } else {
            arbreDoc.querySelector("#path_priv").style.stroke = '#000000';
            if (cpf_priv == 0) {
                arbreDoc.querySelector("#path_priv_nr").style.stroke = '#000000';
            } else if (cpf_priv == 1) {
                arbreDoc.querySelector("#path_onq").style.stroke = '#000000';
            } else if (cpf_priv == 2) {
                arbreDoc.querySelector("#path_oq").style.stroke = '#000000';
            } else if (cpf_priv == 3) {
                arbreDoc.querySelector("#path_emp").style.stroke = '#000000';
            } else if (cpf_priv == 4) {
                arbreDoc.querySelector("#path_am").style.stroke = '#000000';
            } else if (cpf_priv == 5) {
                arbreDoc.querySelector("#path_tec").style.stroke = '#000000';
            } else {
                arbreDoc.querySelector("#path_cad").style.stroke = '#000000';
            }
        }
    } else {
        arbreDoc.querySelector("#path_aide").style.stroke = '#000000';
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
    var statut = $('#statut > select > option:selected').val();
    var pub = $('#pub > select > option:selected').val();
    var cpf_pub = $('#position_pub > select > option:selected').val();
    var cpf_priv = $('#position_priv > select > option:selected').val();
    var nbsal = $('#nbsal > select > option:selected').val();

    var code = getCode(statut, pub, cpf_pub, cpf_priv, nbsal);

    if (code == 'r') {
        feedCodage('REPR', { intitule: 'Code d\'envoi en reprise (utilisation des variables contextuelles nécessaire)' });
    } else {
        $.post("/api/poste_pcs/", { code_pcs: code.replace(''.replace(/0+$/, "")) }, function (data) {
            feedCodage(code, data['echo']);
        });
    }
    construireArbre(statut, pub, cpf_pub, cpf_priv, nbsal);

}


function transformerLibelleSexe(data) {
    var liste_strict_element = null;
    var resultat = data['echo'];
    if (resultat === undefined) {
        resultat = null;
    } 
    if (!(resultat === null)) {
        var genre = getGenre();
        $('#libelle').val(resultat['lib' + genre.substr(0,1)]);
    }
}
