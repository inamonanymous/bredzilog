function toggle(cellId, checkId) {
    var cell = document.getElementById(cellId);
    
    var checkbox = document.getElementById(checkId);

    if (cell.getAttribute("contentEditable") !== "true") {
        cell.setAttribute("contentEditable", "true");
        cell.focus();
        checkbox.disabled = true; // Disable the checkbox when editing
    } else {
        cell.setAttribute("contentEditable", "false");
        checkbox.disabled = false; // Enable the checkbox after editing
    }

    document.getElementById(checkId).addEventListener("click", function () {
        toggle("editableCell", "editCheckbox");
    });

}