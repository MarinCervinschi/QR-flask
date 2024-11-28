
/**
 * Adds event listener to the 'add_button' element to display the 'add_form' element when clicked.
 * @event click
 * @function
 */

document.getElementById('add_button').addEventListener('click', function() {
    document.getElementById('add_form').style.display = 'flex';
});

/**
 * Adds event listener to the 'close_button' element to hide the 'add_form' element when clicked.
 * @event click
 * @function
 */

document.getElementById('close_button').addEventListener('click', function() {
    document.getElementById('add_form').style.display = 'none';
});