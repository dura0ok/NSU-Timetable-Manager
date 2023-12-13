import Toastify from 'toastify-js';

import 'toastify-js/src/toastify.css';

export class ErrorDisplay{
    static display = (message) => {
        Toastify({
            text: message,
            duration: 3000,
            close: true,
            gravity: 'top', // Display the toast at the top of the screen
            position: 'left', // Position the toast on the left side of the screen
            backgroundColor: 'red', // Set the background color of the toast to red
            stopOnFocus: true, // Stop the toast from automatically hiding when it receives focus
        }).showToast();
    };
}