document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('estimation-form');
    const plafondsPrestationSection = document.getElementById('plafonds-prestation');
    const mursPrestationSection = document.getElementById('murs-prestation'); // Nouvelle section pour les prestations des murs
    const solsPrestationSection =  document.getElementById('sols-prestation');
    const roomSizes = document.getElementById('room-sizes');
    const contactForm = document.getElementById('contact-form');
    const contactInfoForm = document.getElementById('contact-info-form');
    const estimateDetail = document.getElementById('estimateDetail');
    const estimateDetailList = document.getElementById('estimateDetailList');
    const resetButton = document.getElementById('resetButton');
    

    // Coûts unitaires par m² (en euros)
    const costPerSquareMeter = {
        peinture_uniquement: {
            murs: 13.3,
            plafonds: 14.6,
            protection: 4.5
        },
        enduit_partiel: {
            murs: 17.3,
            plafonds: 17.6,
            protection: 4.5
        },
        enduit_general: {
            murs: 23.6,
            plafonds: 25.6,
            protection: 4.5
        },
        enduit_decoratif: {
            murs: 50,
            plafonds: 0,
            protection: 4.5
        },
        sols: {
            pose_parquet: 45,
            pose_pvc: 50,
            vitrification_parquet: 33,
            peinture_sol: 60
        }
    };

    // Coûts fixes par pièce (en euros)
    const fixedCostPerPiece = {
        portes: 72,
        fenetres: 72
    };

   // Valeurs par défaut pour les tailles des pièces (en m²)
const defaultRoomSizes = {
    piece1: 25,
    piece2: 1,
    piece3: 10,
    piece4: 5,
    piece5: 5,
    piece6: 15,
    piece7: 12,
    piece8: 9
};

const defaultHeight = 2.5; // Hauteur par défaut (en mètres)

// Objet pour stocker les tailles saisies par l'utilisateur
const customRoomSizes = {
    piece1: {},
    piece2: {},
    piece3: {},
    piece4: {},
    piece5: {},
    piece6: {},
    piece7: {},
    piece8: {}
};

// Fonction pour créer des champs de taille pour une pièce avec des valeurs personnalisées ou par défaut
function createRoomSizeFields(pieceType, quantity) {
    const container = document.createElement('div');
    container.className = `${pieceType}-sizes piece-sizes`;

    const labelElement = document.querySelector(`label[for="${pieceType}"]`);
    const pieceName = labelElement ? labelElement.textContent : pieceType;

    for (let i = 0; i < quantity; i++) {
        const sizeLabel = document.createElement('label');
        const spanLabel = document.createElement('span');
        spanLabel.className = 'fixedWidth';
        spanLabel.textContent = `Surface ${pieceName.toLowerCase()} ${i + 1}:`;
        sizeLabel.appendChild(spanLabel);

        const inputWrapper = document.createElement('div');
        inputWrapper.className = 'input-wrapper';

        const sizeInput = document.createElement('input');
        sizeInput.type = 'number';
        // Utiliser la valeur saisie si elle existe, sinon la valeur par défaut
        sizeInput.value = customRoomSizes[pieceType][i] || defaultRoomSizes[pieceType];
        sizeInput.min = '1';

        const suffixSpan = document.createElement('span');
        suffixSpan.className = 'suffix';
        suffixSpan.textContent = 'm²';

        inputWrapper.appendChild(sizeInput);
        inputWrapper.appendChild(suffixSpan);

        // Écouter les changements sur le champ de taille pour sauvegarder la valeur
        sizeInput.addEventListener('input', function() {
            customRoomSizes[pieceType][i] = sizeInput.value; // Stocker la taille saisie
        });
        
        sizeLabel.appendChild(inputWrapper);
        container.appendChild(sizeLabel);
    }

    return container;
}

// Fonction pour mettre à jour les champs de taille des pièces
function updateRoomSizeFields() {
    const piece1Qty = parseInt(document.getElementById('piece1').value) || 0;
    const piece2Qty = parseInt(document.getElementById('piece2').value) || 0;
    const piece3Qty = parseInt(document.getElementById('piece3').value) || 0;
    const piece4Qty = parseInt(document.getElementById('piece4').value) || 0;
    const piece5Qty = parseInt(document.getElementById('piece5').value) || 0;
    const piece6Qty = parseInt(document.getElementById('piece6').value) || 0;
    const piece7Qty = parseInt(document.getElementById('piece7').value) || 0;
    const piece8Qty = parseInt(document.getElementById('piece8').value) || 0;

    roomSizes.innerHTML = '';

    // Vérifiez si des champs sont ajoutés
    let hasFields = false;

    if (piece1Qty > 0) {
        roomSizes.appendChild(createRoomSizeFields('piece1', piece1Qty));
        hasFields = true;
    }
    if (piece2Qty > 0) {
        roomSizes.appendChild(createRoomSizeFields('piece2', piece2Qty));
        hasFields = true;
    }
    if (piece3Qty > 0) {
        roomSizes.appendChild(createRoomSizeFields('piece3', piece3Qty));
        hasFields = true;
    }
    if (piece4Qty > 0) {
        roomSizes.appendChild(createRoomSizeFields('piece4', piece4Qty));
        hasFields = true;
    }
    if (piece5Qty > 0) {
        roomSizes.appendChild(createRoomSizeFields('piece5', piece5Qty));
        hasFields = true;
    }
    if (piece6Qty > 0) {
        roomSizes.appendChild(createRoomSizeFields('piece6', piece6Qty));
        hasFields = true;
    }
    if (piece7Qty > 0) {
        roomSizes.appendChild(createRoomSizeFields('piece7', piece7Qty));
        hasFields = true;
    }
    if (piece8Qty > 0) {
        roomSizes.appendChild(createRoomSizeFields('piece8', piece8Qty));
        hasFields = true;
    }

    // Ajouter le texte d'en-tête si des champs sont ajoutés
    if (hasFields) {
        if (!roomSizes.querySelector('legend')) {
            const legend = document.createElement('legend');
            legend.textContent = 'Si besoin, ajustez la surface au sol des pièces :';
            roomSizes.insertBefore(legend, roomSizes.firstChild);

            // Créer le message explicatif
            const explanation = document.createElement('p');
            explanation.innerHTML = '<i class="fa-solid fa-circle-info"></i>La surface à peindre des murs et plafonds sera calculée automatiquement à partir de la surface au sol.';
            explanation.style.fontSize = '0.88889em'; // Ajuster la taille du texte si nécessaire
            explanation.style.color = '#666'; // Couleur grise pour le texte explicatif
            explanation.style.marginTop = '-16px'; // Couleur grise pour le texte explicatif

        // Ajouter le message explicatif sous le legend
        roomSizes.insertBefore(explanation, roomSizes.firstChild.nextSibling);
        }
        roomSizes.classList.remove('hidden'); // Afficher le fieldset
    } else {
        const legend = roomSizes.querySelector('legend');
        if (legend) {
            roomSizes.removeChild(legend);
        }
        roomSizes.classList.add('hidden'); // Masquer le fieldset
    }
}


    // Fonction pour afficher/masquer la section des prestations des plafonds
    function togglePlafondsPrestationSection() {
        const plafondsChecked = document.querySelector('input[name="elements"][value="plafonds"]').checked;
        plafondsPrestationSection.classList.toggle('hidden', !plafondsChecked);
    }

    // Fonction pour afficher/masquer la section des prestations des murs
    function toggleMursPrestationSection() {
        const mursChecked = document.querySelector('input[name="elements"][value="murs"]').checked;
        mursPrestationSection.classList.toggle('hidden', !mursChecked);
    }

    // Fonction pour afficher/masquer la section des prestations des sols
    function toggleSolsPrestationSection() {
        const solsChecked = document.querySelector('input[name="elements"][value="sols"]').checked;
        solsPrestationSection.classList.toggle('hidden', !solsChecked);
    }

    // Fonction pour configurer les contrôles de quantité
    function setupQuantityControls() {
        document.querySelectorAll('#estimation-form .quantity-controls').forEach(control => {
            const incrementButton = control.querySelector('.increment');
            const decrementButton = control.querySelector('.decrement');
            const input = control.querySelector('input');


            const updateButtonClass = () => {
                let value = parseInt(input.value);
                if (value > 0) {
                    incrementButton.classList.remove('btn--lightsecondary');
                    incrementButton.classList.add('btn--primary');
                    decrementButton.classList.remove('btn--lightsecondary');
                    decrementButton.classList.add('btn--primary');
                } else {
                    incrementButton.classList.remove('btn--primary');
                    incrementButton.classList.add('btn--lightsecondary');
                    decrementButton.classList.remove('btn--primary');
                    decrementButton.classList.add('btn--lightsecondary');
                }
            };

            incrementButton.addEventListener('click', () => {
                let value = parseInt(input.value);
                if (value < 10) {
                    input.value = value + 1;
                    updateRoomSizeFields();
                    updateButtonClass();
                }
            });

            decrementButton.addEventListener('click', () => {
                let value = parseInt(input.value);
                if (value > 0) {
                    input.value = value - 1;
                    updateRoomSizeFields();
                    updateButtonClass();
                    
                }
            });


            input.addEventListener('input', () => {
                updateButtonClass();
                updateRoomSizeFields();
            });

            updateButtonClass();
        });
    }

    setupQuantityControls();

    // Mise à jour des tailles des pièces lors du changement de quantité
    document.querySelectorAll('#estimation-form input[type="number"]').forEach(input => {
        input.addEventListener('input', updateRoomSizeFields);
    });

    // Mise à jour de la visibilité des sections des prestations lors de la sélection des éléments
    document.querySelectorAll('input[name="elements"]').forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            togglePlafondsPrestationSection();
            toggleMursPrestationSection();
            toggleSolsPrestationSection();
        });
    });


    form.addEventListener('submit', function(event) {
        event.preventDefault();
        estimateDetailList.innerHTML = ''; // Clear previous details

        let totalCost = 0;

        const prestationMurs = form.querySelector('input[name="prestation_murs"]:checked')?.value || null;
        const prestationPlafonds = form.querySelector('input[name="prestation_plafonds"]:checked')?.value || null;
        const prestationSols = form.querySelector('input[name="prestation_sols"]:checked')?.value || null; 
        const selectedElements = Array.from(form.querySelectorAll('input[name="elements"]:checked')).map(el => el.value);

        const pieceDetails = {};

        // Initialiser les détails des pièces
        ['piece1', 'piece2', 'piece3', 'piece4', 'piece5', 'piece6', 'piece7', 'piece8'].forEach(pieceType => {
            const quantity = parseInt(document.getElementById(pieceType).value) || 0;
            pieceDetails[pieceType] = {
                quantity,
                surfaceMurs: 0,
                surfacePlafonds: 0,
                surfaceProtection: 0,
                costMurs: 0,
                costPlafonds: 0,
                costSols: 0,
                costProtection: 0,
                fixedCostPortes: 0,
                fixedCostFenetres: 0
            };
        });

        // Calcul des surfaces et des coûts pour chaque pièce
        Array.from(document.querySelectorAll('.piece-sizes input')).forEach(input => {
            const roomSize = parseInt(input.value) || 0;
            const pieceId = input.closest('.piece-sizes').classList[0];
            const pieceType = pieceId.split('-')[0];

            if (pieceDetails[pieceType].quantity > 0) {
                if (selectedElements.includes('murs')) {
                    let largeur, longueur;

                    if (roomSize <= 3) {
                        largeur = 1; // Largeur pour les petites pièces
                    } else if (roomSize <= 20) {
                        largeur = 3; // Largeur pour les pièces moyennes
                    } else {
                        largeur = 5; // Largeur pour les grandes pièces
                    }

                    longueur = roomSize / largeur;
                    const surfaceMurs = 2 * (longueur * defaultHeight) + 2 * (largeur * defaultHeight);
                    pieceDetails[pieceType].surfaceMurs += Math.floor(surfaceMurs);
                    pieceDetails[pieceType].costMurs += Math.floor(surfaceMurs * costPerSquareMeter[prestationMurs]['murs']);
                }

                if (selectedElements.includes('plafonds')) {
                    pieceDetails[pieceType].surfacePlafonds += roomSize;
                    pieceDetails[pieceType].costPlafonds += Math.floor(roomSize * costPerSquareMeter[prestationPlafonds]['plafonds']);
                }

                if (selectedElements.includes('sols') && prestationSols) {
                    const prestationSols = form.querySelector('input[name="prestation_sols"]:checked')?.value || null;
                    pieceDetails[pieceType].surfacePlafonds = roomSize;
                    pieceDetails[pieceType].costSols = Math.floor(roomSize * costPerSquareMeter.sols[prestationSols]);
                }

                pieceDetails[pieceType].surfaceProtection += roomSize;
                pieceDetails[pieceType].costProtection += Math.floor(roomSize * costPerSquareMeter[prestationPlafonds]['protection']);
            }
        });

        // Calcul des coûts fixes pour portes et fenêtres
        const pieceTypes = ['piece1', 'piece2', 'piece3', 'piece4', 'piece5', 'piece6', 'piece7', 'piece8'];
        pieceTypes.forEach(pieceId => {
            const quantity = pieceDetails[pieceId].quantity;
            if (quantity > 0) {
                if (selectedElements.includes('portes')) {
                    pieceDetails[pieceId].fixedCostPortes += fixedCostPerPiece.portes * quantity;
                }
                if (selectedElements.includes('fenetres')) {
                    pieceDetails[pieceId].fixedCostFenetres += fixedCostPerPiece.fenetres * quantity;
                }

                // Calcul du coût total pour chaque pièce
                const pieceTotalCost = pieceDetails[pieceId].costMurs + pieceDetails[pieceId].costPlafonds + (pieceDetails[pieceId].costSols || 0) + pieceDetails[pieceId].fixedCostPortes + pieceDetails[pieceId].fixedCostFenetres + pieceDetails[pieceId].costProtection;
                totalCost += Math.floor(pieceTotalCost);

                // Affichage des détails pour chaque pièce
                if (pieceDetails[pieceId].quantity > 0) {
                    
                    function getPieceName(pieceType) {
                        const labelElement = document.querySelector(`label[for="${pieceType}"]`);
                        return labelElement ? labelElement.textContent : pieceType;
                    }
                    const pieceName = getPieceName(pieceId);
                    const quantity = pieceDetails[pieceId].quantity;
                                        let instancesText = '';
                    if (quantity > 1) {
                        for (let i = 1; i <= quantity; i++) {
                            instancesText += `${pieceName} ${i}`;
                            if (i < quantity) instancesText += ', ';
                        }
                    } else {
                        instancesText = `${pieceName}`;
                    }
                    
                    const pieceIdItem = document.createElement('p');
                    pieceIdItem.innerHTML = `<strong>${instancesText}</strong>`;
                    estimateDetailList.appendChild(pieceIdItem);
                    console.log(`${pieceId.charAt(0).toUpperCase() + pieceId.slice(1)}`);

                    if (selectedElements.includes('plafonds')) {
                     const surfacePlafondsRow = document.createElement('tr');
                        surfacePlafondsRow.innerHTML = `
                            <td>Plafonds</td>
                            <td>${pieceDetails[pieceId].surfacePlafonds} m²</td>
                            <td>${costPerSquareMeter[prestationPlafonds]['plafonds']} €</td>
                            <td>0%</td>
                            <td>${pieceDetails[pieceId].costPlafonds} €</td>
                        `;
                        estimateDetailList.appendChild(surfacePlafondsRow);
                        console.log(`- Total surface des plafonds : ${pieceDetails[pieceId].surfacePlafonds} m² * ${costPerSquareMeter[prestationPlafonds]['plafonds']} €`);

                    }
                    if (selectedElements.includes('murs')) {
                        const surfaceMursRow = document.createElement('tr');
                        surfaceMursRow.innerHTML = `
                            <td>Murs</td>
                            <td>${pieceDetails[pieceId].surfaceMurs} m²</td>
                            <td>${costPerSquareMeter[prestationMurs]['murs']} €</td>
                            <td>0%</td>
                            <td>${pieceDetails[pieceId].costMurs} €</td>
                        `;
                        estimateDetailList.appendChild(surfaceMursRow);
                        console.log(`- Total surface des murs : ${pieceDetails[pieceId].surfaceMurs} m² * ${costPerSquareMeter[prestationMurs]['murs']} €`);
                    }

                    if (selectedElements.includes('sols')) {
                        const selectedSolRadio = document.querySelector('input[name="prestation_sols"]:checked');
                        const tooltipElement = selectedSolRadio.parentElement.querySelector('.tooltiptext');
                        // Obtenir le texte du label en excluant le tooltip
                        let solLabel = selectedSolRadio.parentElement.textContent.trim();
                        if (tooltipElement) {
                            solLabel = solLabel.replace(tooltipElement.textContent.trim(), '').trim();
                        }
                        const surfaceSolsRow = document.createElement('tr');
                        surfaceSolsRow.innerHTML = `
                            <td>Sols : ${solLabel}</td>
                            <td>${pieceDetails[pieceId].surfacePlafonds} m²</td>
                            <td>${costPerSquareMeter.sols[prestationSols]} €</td>
                            <td>0%</td>
                            <td>${pieceDetails[pieceId].costSols} €</td>
                        `;
                        estimateDetailList.appendChild(surfaceSolsRow);
                        console.log(`- Total surface des sols : ${pieceDetails[pieceId].surfacePlafonds} m² * ${costPerSquareMeter.sols[prestationSols]} €`);
                        

                    }

                    if (selectedElements.includes('portes')) {
                        const portesRow = document.createElement('tr');
                        portesRow.innerHTML = `
                            <td>Portes</td>
                            <td>${pieceDetails[pieceId].quantity} unité</td>
                            <td>${fixedCostPerPiece.portes} €</td>
                            <td>0%</td>
                            <td>${pieceDetails[pieceId].fixedCostPortes} €</td>
                        `;
                        estimateDetailList.appendChild(portesRow);
   
                        console.log(`- Nombre de portes : ${pieceDetails[pieceId].quantity} * ${fixedCostPerPiece.portes} €`);
                    }
                    if (selectedElements.includes('fenetres')) {
                        const fenetresRow = document.createElement('tr');
                        fenetresRow.innerHTML = `
                            <td>Fenêtres</td>
                            <td>${pieceDetails[pieceId].quantity} unité</td>
                            <td>${fixedCostPerPiece.fenetres} €</td>
                            <td>0%</td>
                            <td>${pieceDetails[pieceId].fixedCostFenetres} €</td>
                        `;
                        estimateDetailList.appendChild(fenetresRow);
                        console.log(`- Nombre de fenêtres : ${pieceDetails[pieceId].quantity} * ${fixedCostPerPiece.fenetres} €`);
                    }

                    // Détails de protection
                    /*
                    const surfaceProtectionRow = document.createElement('tr');
                    surfaceProtectionRow.innerHTML = `
                        <td colspan="4"><strong>Protection </strong></td>
                        <td>${pieceDetails[pieceId].costProtection} €</td>
                    `;
                    estimateDetailList.appendChild(surfaceProtectionRow);
                    */
                    
                    /* Désactiver le sous-total par piece
                    const pieceTotalRow = document.createElement('tr');
                    pieceTotalRow.innerHTML = `
                        <td colspan="4" style="text-align:right;"><strong>Sous-total </strong></td>
                        <td ><strong>${pieceTotalCost} €</strong></td>`;
                    estimateDetailList.appendChild(pieceTotalRow);
                    console.log(`- Sous-total pièce : ${pieceTotalCost} €`);
                    */
                
                }
            }
        });

        // Total protection à afficher dans le sous-total
        let totalCostProtection = 0;
        Object.keys(pieceDetails).forEach(pieceId => {
            totalCostProtection += pieceDetails[pieceId].costProtection || 0;
        });
        console.log(totalCostProtection)

        //Afficher le detail de total protection
        const totalProtectionRow = document.createElement('tr');
        totalProtectionRow.innerHTML = `
            <td colspan="2">Nettoyage, fournitures courantes et protection</td>
            <td>1 Forfait</td>
            <td>0%</td>
            <td>${totalCostProtection} €</td>`;
        estimateDetailList.appendChild(totalProtectionRow);


        const tvaRow = document.createElement('tr');
        const tvaCell = document.createElement('td');
        tvaCell.colSpan = 5;
        tvaCell.textContent = '*TVA non applicable - article 293 B du CGI';
        tvaCell.style.textAlign = 'right';
        tvaCell.style.fontStyle = 'italic';
        tvaRow.appendChild(tvaCell);
        estimateDetailList.appendChild(tvaRow);

        const TotalRow = document.createElement('tr');
        TotalRow.innerHTML = `
            <td colspan="4"><strong><i class="fa-solid fa-circle-exclamation"></i> Total estimation (À valider par une visite technique) </strong></td>
            <td><strong>${totalCost} €</td></strong>`;
        estimateDetailList.appendChild(TotalRow);
        console.log(`Total : ${totalCost} €`);

        // Arreter l'exécution si aucune checkbox cochée
        if (totalCost === 0) {
            alert("Veuillez ajouter au moins une pièce.");
            return;
        }

        // Arreter l'exécution si aucune checkbox cochée
        if (selectedElements.length === 0) {
            alert("Veuillez sélectionner au moins un élément à peindre.");
            return; 
        }
        

        //totalCostEstimation = totalCost;
        form.style.display = 'none';
        contactForm.style.display = 'block';
        window.scrollTo(0, 0);

        

    });

    



    contactInfoForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const name = document.getElementById('name').value;
        const email = document.getElementById('email').value;
        const location = document.getElementById('location').value;

        // Envoyer vers l'étape 3 qui affiche l'estimation
        contactForm.style.display = 'none';
        estimateDetail.style.display = 'block';
        window.scrollTo(0, 0);

    });

    function resetForm() {
        estimateDetailList.innerHTML = '';
        form.reset();
        contactInfoForm.reset();
        form.style.display = 'block';
        estimateDetail.style.display = 'none';
        let totalCostProtection = 0;
        updateRoomSizeFields();
        togglePlafondsPrestationSection();
        toggleMursPrestationSection();
        toggleSolsPrestationSection();
        window.scrollTo(0, 0);
        document.querySelectorAll('.quantity-controls').forEach(control => {
            const incrementButton = control.querySelector('.increment');
            const decrementButton = control.querySelector('.decrement');
            incrementButton.classList.remove('btn--primary');
            incrementButton.classList.add('btn--lightsecondary');
            decrementButton.classList.remove('btn--primary');
            decrementButton.classList.add('btn--lightsecondary');
        });
        for (const key in customRoomSizes) {
            customRoomSizes[key] = {};
        };
    }

    // Appelle la fonction de réinitialisation
    resetButton.addEventListener('click', resetForm);
    window.onpageshow = function(event) {
        resetForm(); 
    };


    // Appeler la fonction au chargement de la page
    updateRoomSizeFields();
    togglePlafondsPrestationSection();
    toggleMursPrestationSection(); 
    toggleSolsPrestationSection();


/* Code pour générer calendly */
/*
document.getElementById('openCalendlyModal').onclick = function() {
    var calendlyUrl = 'https://calendly.com/justindolle-peinture/discussion-par-telephone-de-votre-projet';

    // Récupérer les valeurs du formulaire de contact
    var userName = document.querySelector('input[name="name"]').value;
    var userEmail = document.querySelector('input[name="email"]').value;

    // Nettoyer le conteneur avant d'ajouter un nouveau widget
    var calendlyContainer = document.getElementById('calendly-container');
    calendlyContainer.innerHTML = ''; // Retire l'iframe existante

    // Pré-remplir les informations dans Calendly
    Calendly.initInlineWidget({
        url: calendlyUrl,
        parentElement: calendlyContainer,
        prefill: {
            name: userName,
            email: userEmail
        },
        utm: {}
    });
    
    // Ouvrir la modal
    document.getElementById('calendlyModal').style.display = "block";
}
    

document.querySelector('.close').onclick = function() {
    // Fermer la modal
    document.getElementById('calendlyModal').style.display = "none";
    
    // Nettoyer le conteneur pour éviter les iframes multiples
    document.getElementById('calendly-container').innerHTML = '';
}

window.onclick = function(event) {
    if (event.target == document.getElementById('calendlyModal')) {
        // Fermer la modal
        document.getElementById('calendlyModal').style.display = "none";
        
        // Nettoyer le conteneur pour éviter les iframes multiples
        document.getElementById('calendly-container').innerHTML = '';
    }
}
*/

/* Fonction envoi de données à google sheet */

    contactInfoForm.addEventListener('submit', function(event) {
    event.preventDefault(); // Empêche le rechargement de la page

    const formData = new FormData(this);
    const innerEstimateDetails = estimateDetailList.innerText; // Récupérer le contenu de la div estimateDetailList
    formData.append('details', innerEstimateDetails); // Ajouter le contenu de estimateDetailList à formData
    

    const url = 'https://script.google.com/macros/s/AKfycbzBEM8uMZN5gCwrv5QI0AmSCXX1y0wXMMVVcQxpdcL1oDqvNiFCnSWe-zVxVPN4T2F-/exec'; // Remplacez par l'URL de votre script Apps Script

    fetch(url, {
        method: 'POST',
        body: formData,
    })
    .then(response => {
        if (response.ok) {
            console.log('Estimation envoyée avec succès.');
            //alert('Estimation envoyée avec succès.');
        } else {
            console.log('Erreur lors de l\'envoi de l\'estimation.');
            //alert('Erreur lors de l\'envoi de l\'estimation.');
        }
    })
    .catch(error => {
        console.error('Erreur de réseau :', error);
        //alert('Erreur de réseau. Veuillez réessayer.');
    });
});



/* Générer un pdf*/
document.getElementById('generatePDF').addEventListener('click', function () {
    // Sélectionne la div contenant les détails de l'estimation
    var element = document.getElementById('estimateDetail');

    // Insérer la date du jour dans le PDF
    var today = new Date();
    today.setMonth(today.getMonth() + 1);
    var formattedDate = today.toLocaleDateString('fr-FR', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
    document.getElementById('currentDate').innerText = formattedDate;

    // Rendre les éléments cachés visibles pour le PDF
    document.querySelectorAll('.hidden-in-web').forEach(function(el) {
        el.style.display = 'block';
    });

    // Utilise html2pdf pour générer le PDF
    html2pdf(element, {
      margin: 10,
      filename: 'estimation.pdf',
      html2canvas: {
        scale: 2,
        ignoreElements: function (element) {
          // Ignorer les éléments avec la classe "no-print"
          return element.classList.contains('no-print');
        }
      },
      jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' }
    }).then(function() {
        // Masquer à nouveau les éléments après la génération du PDF
        document.querySelectorAll('.hidden-in-web').forEach(function(el) {
            el.style.display = 'none';
        });
    });
});


  /* Autre tracking */

  document.querySelector('#estimation-form > button').addEventListener('click', function() {
    gtag('event', 'estimation_gotostep2', {
        'event_category': 'estimate form',
        'event_label': 'go to step 2',
        'value': 1
    });
    console.log ('go to step 2 trigger')
});

document.querySelector('#contact-info-form > button').addEventListener('click', function() {
    gtag('event', 'estimation_gotostep3', {
        'event_category': 'estimate form',
        'event_label': 'go to step 3',
        'value': 1
    });
    console.log ('go to step 3 trigger')
});

document.getElementById('generatePDF').addEventListener('click', function() {
    gtag('event', 'estimation_generatepdf', {
        'event_category': 'estimate form',
        'event_label': 'generate pdf',
        'value': 1
    });
    console.log ('generate pdf trigger')
});





});