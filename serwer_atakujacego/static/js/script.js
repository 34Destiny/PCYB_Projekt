function downloadCookies(format) {
    window.location.href = `/download/${format}`;
}

function clearCookies() {
    if (confirm('Czy na pewno chcesz wyczyścić wszystkie przechwycone ciasteczka?')) {
        fetch('/clear', { method: 'POST' })
            .then(() => location.reload());
    }
}

setTimeout(() => location.reload(), 5009);
