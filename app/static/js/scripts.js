/**
 * Adds event listener to the 'add_button' element to display the 'add_form' element when clicked.
 * @event click
 */
document.getElementById('add_button').addEventListener('click', function () {
    document.getElementById('add_form').style.display = 'flex';
});

/**
 * Adds event listener to the 'close_button' element to hide the 'add_form' element when clicked.
 * @event click
 */
document.getElementById('close_button').addEventListener('click', function () {
    document.getElementById('add_form').style.display = 'none';
});

/**
 * Waits for the DOM content to load, then initializes form actions and button interactions.
 * Includes logic for handling edit mode and submitting forms dynamically.
 */
document.addEventListener("DOMContentLoaded", function () {
    const forms = document.querySelectorAll('.links-grid');
    let isEditing = false;

    forms.forEach(form => {
        const buttons = form.querySelectorAll('.grid-button');
        const editButton = form.querySelector('button[data-action="/edit"]');
        const externalInput = form.querySelector('input[name="external"]');
        const pencilIcon = editButton.querySelector('i');
        const idInput = form.querySelector('input[name="id"]');
        let originalValue = externalInput.value;

        
        function resetEditing() {
            externalInput.value = originalValue;
            externalInput.type = 'button';
            pencilIcon.classList.remove('bx-check-square');
            pencilIcon.classList.add('bx-pencil');
            editButton.style.backgroundColor = '#008000';
            editButton.style.color = '#fff';
            isEditing = false;
        }

        buttons.forEach(button => {
            button.addEventListener('click', function (e) {
                e.preventDefault(); 

                const action = button.getAttribute('data-action');
                form.setAttribute('action', '/private/dashboard' + action);

                if (action === '/delete') {
                    if (confirm('Are you sure you want to remove?')) {
                        idInput.type = "text";
                        form.submit(); 
                    }
                } else if (action === '/edit') {
                    if (!isEditing) {
                        pencilIcon.classList.remove('bx-pencil');
                        pencilIcon.classList.add('bx-check-square');
                        externalInput.type = 'text';
                        externalInput.focus();
                        externalInput.setSelectionRange(externalInput.value.length, externalInput.value.length);
                        editButton.style.backgroundColor = "#8fc0a9";
                        editButton.style.color = "#000";
                        isEditing = true;
                    } else {
                        if (confirm('Are you sure you want to save the changes?')) {
                            idInput.type = 'text';
                            form.submit();
                        } else {
                            resetEditing();
                        }
                        isEditing = false;
                    }
                } else if (action === '/qr') {
                    idInput.type = 'text';
                    form.submit(); 
                }
            });
        });

        externalInput.addEventListener('keydown', function (e) {
            if (isEditing && e.key === "Enter") {
                e.preventDefault(); 
                if (confirm('Do you want to save the changes?')) {
                    idInput.type = 'text';
                    form.submit(); 
                } else {
                    resetEditing(); 
                }
                isEditing = false;
            }
        });
    });

    document.addEventListener('click', function (e) {
        if (isEditing && !e.target.closest('.links-grid')) {
            alert("You are in edit mode. If you want to save, click the 'check' button!");
        }
    });
});
