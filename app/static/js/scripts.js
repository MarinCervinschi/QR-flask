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
    // Select all forms in the page
    const forms = document.querySelectorAll('.links-grid');
    let isEditing = false; // Tracks global editing state

    // Loop through each form to attach functionality
    forms.forEach(form => {
        const buttons = form.querySelectorAll('.grid-button'); // All action buttons
        const editButton = form.querySelector('button[data-action="/edit"]'); // Edit button
        const externalInput = form.querySelector('input[name="external"]'); // Input field for editing
        const pencilIcon = editButton.querySelector('i'); // Icon inside edit button
        const idInput = form.querySelector('input[name="id"]');

        buttons.forEach(button => {
            button.addEventListener('click', function (e) {
                e.preventDefault(); // Prevent default form submission

                const action = button.getAttribute('data-action'); // Action type
                form.setAttribute('action', '/private/dashboard' + action); // Update form action dynamically

                if (action === '/delete') {
                    // Handle delete action with confirmation
                    if (confirm('Are you sure you want to remove?')) {
                        idInput.type = "text"
                        form.submit(); // Submit form after confirmation
                    }
                } else if (action === '/edit') {
                    // Handle edit action
                    if (!isEditing) {
                        // Switch to edit mode
                        pencilIcon.classList.remove('bx-pencil');
                        pencilIcon.classList.add('bx-check-square');
                        externalInput.type = 'text'; // Make input editable
                        externalInput.focus(); // Focus on the input field

                        // Set cursor at the end of input text
                        const textLength = externalInput.value.length;
                        externalInput.setSelectionRange(textLength, textLength);

                        editButton.style.backgroundColor = "#8fc0a9";
                        editButton.style.color = "#000";

                        isEditing = true; // Update editing state
                    } else {
                        // Confirm exiting edit mode
                        if (confirm('Are you sure you want to save the changes?')) {
                            idInput.type = 'text'; 
                            form.submit(); // Submit form after confirmation
                        }
                        isEditing = false; // Reset editing state
                    }
                } else if (action === '/qr') {
                    // Handle add action
                    form.submit(); // Submit form
                }
            });
        });
    });

    // Warn user if they try to click outside the form while in edit mode
    document.addEventListener('click', function (e) {
        if (isEditing && !e.target.closest('.links-grid')) {
            alert("You are in edit mode. If you want to save, click the 'check' button!");
        }
    });
});