$('#section_codage').hide();
$('#statut').hide();
$('#pub').hide();
$('#position_pub').hide();
$('#position_priv').hide();
$('#nbsal').hide();
$('#bouton_coder').hide();
var hit = null;

$(document).on('click', function (event) {
    if (!$(event.target).closest('#search_auto').length) {
        cleanAucompletionProfList();
    }
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
    $.get("/profession_strict/", { lib: $('#libelle').val() }, function (data) {
        transformerLibelleSexe(data);
    });
}

$("#libelle").on('input click', function () {
    $('#section_codage').hide();
    suggestProf($(this).val());
    strictProf($(this).val());
});

function getGenre() {
    var genre = 'm';
    if ($('#sexe').val() == 1) {
        genre = 'f';
    }
    return genre;
}

function suggestProf(value) {
    var genre = getGenre();
    $.get("/profession/", { lib: value, genre: genre }, function (data) {
        showSuggestionsProf(data);
    });
}

function strictProf(value) {
    var genre = getGenre();
    $.get("/profession_strict/", { lib: value, genre: genre }, function (data) {
        updateListeStrictElement(data);
    });
}

function showSuggestionsProf(data) {
    var div = '';
    data.forEach(function (suggestion) {
        var texteFormate = '';
        if ($('#sexe').val() == 0) {
            texteFormate = suggestion.highlight.libm[0];
        } else {
            texteFormate = suggestion.highlight.libf[0];
        }
        div += ('<li class="list-group-item list-group-item-action pl-4 pt-1 pb-1 pr-4 m-0" onmouseover="this.style.background=\'#8DB0E1\';" onmouseout="this.style.background=\'\';this.style.color=\'\';" onclick="autocompletionProfChoix(this)"><small>' + texteFormate + '</small></li>');
    });
    $('#search_auto').html(div);
}

function autocompletionProfChoix(li) {
    $('#libelle').val(li.textContent);
    cleanAucompletionProfList();
    strictProf($('#libelle').val());
}

function cleanAucompletionProfList() {
    $('#search_auto > li').remove();
}

function updateListeStrictElement(data) {
    $('#formulaire_index').removeClass('needs-validation');
    $('#formulaire_index').removeClass('was-validated');
    var liste_strict_element = null;
    var resultat = data['hits']['hits'];
    if (resultat === undefined) {
        liste_strict_element = null;
    } else if (resultat.length == 0) {
        liste_strict_element = null;
    } else {
        liste_strict_element = resultat[0];
    }
    if (liste_strict_element === null) {
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
        hit = liste_strict_element;
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
        return hit['_source']['ssvaran'];
    } else if (statut == 1) {
        if (nbsal == 0) {
            return hit['_source']['inde_nr'];
        } else if (nbsal == 1) {
            return hit['_source']['inde_0_9'];
        } else if (nbsal == 2) {
            return hit['_source']['inde_10_49'];
        } else {
            return hit['_source']['inde_sup49'];
        }
    } else if (statut == 2) {
        if (pub == 1) {
            if (cpf_pub == 0) {
                return hit['_source']['pub_nr'];
            } else if (cpf_pub == 1) {
                return hit['_source']['pub_catA'];
            } else if (cpf_pub == 2) {
                return hit['_source']['pub_catB'];
            } else {
                return hit['_source']['pub_catC'];
            }
        } else {
            if (cpf_priv == 0) {
                return hit['_source']['priv_nr'];
            } else if (cpf_priv == 1) {
                return hit['_source']['priv_onq'];
            } else if (cpf_priv == 2) {
                return hit['_source']['priv_oq'];
            } else if (cpf_priv == 3) {
                return hit['_source']['priv_emp'];
            } else if (cpf_priv == 4) {
                return hit['_source']['priv_am'];
            } else if (cpf_priv == 5) {
                return hit['_source']['priv_tec'];
            } else {
                return hit['_source']['priv_cad'];
            }
        }
    } else {
        return hit['_source']['aid_fam'];
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
        c = hit['_source'][x];
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
        c = hit['_source'][x];
        console.log(c);
        if (c == 'r') {
            $('#label_node_' + x + ' > tspan').html('REPR');
        } else {
            $('#label_node_' + x + ' > tspan').html(c);
        }
        $('#node_' + x).css('fill', codes_couleurs[c]);
    });
    $('#legende_tree').html('<h6>Légende: </h6>');
    for (const code in codes_couleurs) {
        if (code == 'r') {
            $('#legende_tree').append('<div class="row"><div class="col-auto"><span class="badge badge-light" style="background-color: ' + codes_couleurs[code] + '">REPR</span></div><div class="col"><p>Code d\'envoi en reprise (utilisation des variables contextuelles nécessaire)</p></div></div>');
        } else {
            $.ajax({
                url: '/recuperer_intitule_codepcs/?code=' + code,
                method: 'GET',
                success: function (data) {
                    $('#legende_tree').append('<div class="row"><div class="col-auto"><span class="badge badge-light" style="background-color: ' + codes_couleurs[code] + '">' + code + '</span></div><div class="col"><p>' + data.intitule + '</p></div></div>');
                }

            });
        }
    }
}

function colorierChemin(statut, pub, cpf_pub, cpf_priv, nbsal) {
    $("path[id^=path_]").css('stroke', '#B0AEAE');
    $("#path_root").css('stroke', '#000000');
    if (statut == 0) {
        $("#path_nr").css('stroke', '#000000');
    } else if (statut == 1) {
        $("#path_inde").css('stroke', '#000000');
        if (nbsal == 0) {
            $("#path_taille_nr").css('stroke', '#000000');
        } else if (nbsal == 1) {
            $("#path_taille1").css('stroke', '#000000');
        } else if (nbsal == 2) {
            $("#path_taille2").css('stroke', '#000000');
        } else {
            $("#path_taille3").css('stroke', '#000000');
        }
    } else if (statut == 2) {
        $("#path_salarie").css('stroke', '#000000');
        if (pub == 1) {
            $("#path_pub").css('stroke', '#000000');
            if (cpf_pub == 0) {
                $("#path_pub_nr").css('stroke', '#000000');
            } else if (cpf_pub == 1) {
                $("#path_catA").css('stroke', '#000000');
            } else if (cpf_pub == 2) {
                $("#path_catB").css('stroke', '#000000');
            } else {
                $("#path_catC").css('stroke', '#000000');
            }
        } else {
            $("#path_priv").css('stroke', '#000000');
            if (cpf_priv == 0) {
                $("#path_priv_nr").css('stroke', '#000000');
            } else if (cpf_priv == 1) {
                $("#path_onq").css('stroke', '#000000');
            } else if (cpf_priv == 2) {
                $("#path_oq").css('stroke', '#000000');
            } else if (cpf_priv == 3) {
                $("#path_emp").css('stroke', '#000000');
            } else if (cpf_priv == 4) {
                $("#path_am").css('stroke', '#000000');
            } else if (cpf_priv == 5) {
                $("#path_tec").css('stroke', '#000000');
            } else {
                $("#path_cad").css('stroke', '#000000');
            }
        }
    } else {
        $("#path_aide").css('stroke', '#000000');
    }
}


function construireArbre(statut, pub, cpf_pub, cpf_priv, nbsal) {
    colorierFeuille();
    colorierChemin(statut, pub, cpf_pub, cpf_priv, nbsal);
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
        $.get("/recuperer_intitule_codepcs/", { code: code }, function (data) {
            feedCodage(code, data);
        });

    }
    construireArbre(statut, pub, cpf_pub, cpf_priv, nbsal);

}


function transformerLibelleSexe(data) {
    var liste_strict_element = null;
    var resultat = data['hits']['hits'];
    if (resultat === undefined) {
        liste_strict_element = null;
    } else if (resultat.length == 0) {
        liste_strict_element = null;
    } else {
        liste_strict_element = resultat[0];
    }
    if (!(liste_strict_element === null)) {
        var genre = getGenre();
        $('#libelle').val(liste_strict_element['_source']['lib' + genre]);
    }
}