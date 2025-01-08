document.addEventListener("DOMContentLoaded", function () {
    const bidInput = document.querySelector(".bid-input");

    bidInput.addEventListener("input", function () {
        let value = this.value.replace(/\D/g, ''); // Remove all non-numeric characters

        // Always start with two zeros before the decimal
        if (value.length < 3) {
            value = '00.' + value.padStart(2, '0');
        } else {
            // Split the string into the integer part and the decimal part
            const integerPart = value.slice(0, value.length - 2);
            const decimalPart = value.slice(value.length - 2);

            // Combine the integer and decimal parts
            value = integerPart + '.' + decimalPart;
        }

        // Limit the length to something reasonable
        if (value.length > 8) {
            value = value.slice(0, 8);
        }

        // Set the value back to the input field
        this.value = value;
    });
});
