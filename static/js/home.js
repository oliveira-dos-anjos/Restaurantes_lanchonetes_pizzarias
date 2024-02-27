document.addEventListener('DOMContentLoaded', function() {
    // Verifica se há um usuário logado
    var userLoggedIn = "{{ user }}" !== "";

    // Se não houver usuário logado, redireciona para a página de login
    document.getElementById('profile-btn').addEventListener('click', function() {
        if (!userLoggedIn) {
            window.location.href = "{{ url_for('login') }}";
        }
    });

    // Se houver usuário logado, exibe o botão "Sair" quando o perfil é clicado
    if (userLoggedIn) {
        document.getElementById('dropdown-content').style.display = 'none'; // Oculta o dropdown inicialmente

        document.getElementById('profile-btn').addEventListener('click', function() {
            document.getElementById('dropdown-content').style.display = 'block';
        });
    }
});