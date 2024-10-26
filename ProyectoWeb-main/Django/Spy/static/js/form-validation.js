function validateForm() {
    var email = document.getElementById('floatingCorreo').value;
    var telefono = document.getElementById('floatingTelefono').value;
    var password = document.getElementById('floatingPassword').value;
    var confirmPassword = document.getElementById('floatingConfirmPassword').value;

    var emailRegex = /\S+@\S+\.\S+/;
    var telefonoRegex = /^\d{9}$/; // Modificado para aceptar 9 dígitos
    var passwordMinLength = 9; // Longitud mínima de la contraseña

    if (!emailRegex.test(email)) {
        document.getElementById('floatingCorreo').classList.add('is-invalid');
        return false;
    }

    if (!telefonoRegex.test(telefono)) {
        document.getElementById('floatingTelefono').classList.add('is-invalid');
        return false;
    }

    if (password.length < passwordMinLength) {
        document.getElementById('floatingPassword').classList.add('is-invalid');
        return false;
    }

    if (password !== confirmPassword) {
        document.getElementById('floatingConfirmPassword').classList.add('is-invalid');
        document.getElementById('confirmPasswordErrorMessage').innerText = "Las contraseñas no coinciden.";
        return false;
    }

    return true;
}
