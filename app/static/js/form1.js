document.getElementById("numero").addEventListener("input", function (event) {
    this.value = this.value.replace(/[^0-9]/g, ''); // Supprime tout sauf les chiffres
});
const who = document.querySelectorAll('input[name="who"]');
who_value = false
// Parcourir tous les éléments de la collection
who.forEach(radio => {
    radio.addEventListener('change', (event) => {
        // Récupérer la valeur sélectionnée
        const valeur = event.target.value;
        who_value = valeur;
        // Récupérer les éléments avec la classe "enfant-div"
        const enfantDivs = document.getElementsByClassName("enfant-div");

        // Parcourir tous les éléments de la collection
        for (let div of enfantDivs) {
            if (valeur === 'enfant') {
                div.style.height = "auto"; // Afficher
                div.style.margin = "0 0 35px 0";
            } else {
                div.style.height = "0px"; // Masquer
                div.style.overflow = "hidden";
                div.style.margin = "0";
            }
        }
    });
});

function association_combo() {
    const association_select = document.getElementById('association');
    const association_value = association_select.value;
    
    // Récupérer les éléments de classe "autres-association"
    let autre_association_input = document.getElementsByClassName('autres-association');

    // Vérifier si des éléments existent avant d'appliquer un style
    if (autre_association_input.length > 0) {
        if (association_value === "autres") {
            autre_association_input[0].style.display = 'block';
        } else {
            autre_association_input[0].style.display = 'none';
        }
    }
}

document.getElementById("validate").addEventListener("click", function (event) {
    if (who_value === "enfant") {
        // Récupérer les valeurs des champs
        const nom_enfant = document.getElementById("child-firstname").value;
        const prenom_enfant = document.getElementById("child-lastname").value;
        const date_naissance = document.getElementById("child-birth").value;
        const firstname = document.getElementById("firstname").value;
        const lastname = document.getElementById("lastname").value;
        const birth = document.getElementById("birth").value;
        const numero = document.getElementById("numero").value;
        const association = document.getElementById("association").value;

        // Vérifier si les champs sont remplis
        if (nom_enfant === "" || prenom_enfant === "" || date_naissance === "" || firstname === "" || lastname === "" || birth === "" || numero === "") {
            nom_enfant === "" ? document.getElementById("child-firstname").style.border = "1px solid red" : document.getElementById("child-firstname").style.border = "1px solid #ced4da";
            prenom_enfant === "" ? document.getElementById("child-lastname").style.border = "1px solid red" : document.getElementById("child-lastname").style.border = "1px solid #ced4da";
            date_naissance === "" ? document.getElementById("child-birth").style.border = "1px solid red" : document.getElementById("child-birth").style.border = "1px solid #ced4da";
            firstname === "" ? document.getElementById("firstname").style.border = "1px solid red" : document.getElementById("firstname").style.border = "1px solid #ced4da";
            lastname === "" ? document.getElementById("lastname").style.border = "1px solid red" : document.getElementById("lastname").style.border = "1px solid #ced4da";
            birth === "" ? document.getElementById("birth").style.border = "1px solid red" : document.getElementById("birth").style.border = "1px solid #ced4da";
            numero === "" ? document.getElementById("numero").style.border = "1px solid red" : document.getElementById("numero").style.border = "1px solid #ced4da";
            association == "" ? document.getElementById("association").style.border = "1px solid red" : document.getElementById("association").style.border = "1px solid #ced4da";
            alert("Veuillez remplir tous les champs");
        }else{
            document.getElementById("form1").submit();
        }
    }else{
        // Récupérer les valeurs des champs
        const firstname = document.getElementById("firstname").value;
        const lastname = document.getElementById("lastname").value;
        const birth = document.getElementById("birth").value;
        const numero = document.getElementById("numero").value;
        const association = document.getElementById("association").value;

        // Vérifier si les champs sont remplis
        if (firstname === "" || lastname === "" || birth === "" || numero === "" || association === "") {
            firstname === "" ? document.getElementById("firstname").style.border = "1px solid red" : document.getElementById("firstname").style.border = "1px solid #ced4da";
            lastname === "" ? document.getElementById("lastname").style.border = "1px solid red" : document.getElementById("lastname").style.border = "1px solid #ced4da";
            birth === "" ? document.getElementById("birth").style.border = "1px solid red" : document.getElementById("birth").style.border = "1px solid #ced4da";
            numero === "" ? document.getElementById("numero").style.border = "1px solid red" : document.getElementById("numero").style.border = "1px solid #ced4da";
            association == "" ? document.getElementById("association").style.border = "1px solid red" : document.getElementById("association").style.border = "1px solid #ced4da";
            alert("Veuillez remplir tous les champs");
        }else{
            document.getElementById("form1").submit();
        }
    }
});