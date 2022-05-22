"use strict";

/**
 * Increment a date-picker value by months
 * @param {string} input_id - the input element id for the date-picker
 * @param {number} months - number of months to add
 */
function incr_date_by_months(input_id, months) {
    let element = document.getElementById(input_id);

    if (!element.value) {
        element.value = (new Date()).toISOString().split("T")[0];
    }

    let new_date = new Date(element.value);
    new_date.setUTCMonth(new_date.getUTCMonth() + months);
    element.value = new_date.toISOString().split("T")[0];
}
