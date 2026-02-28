<?php
// enviar.php - Script simples de processamento de formulário

// Configurações
$destinatario = "valdaacupuntura@gmail.com"; // Substitua pelo seu e-mail real
$assunto_padrao = "Novo contato via Site - Valda Acupuntura";

// Verifica se o formulário foi submetido
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    
    // Sanitização e Validação dos dados
    $nome = filter_input(INPUT_POST, 'nome', FILTER_SANITIZE_SPECIAL_CHARS);
    $email = filter_input(INPUT_POST, 'email', FILTER_SANITIZE_EMAIL);
    $telefone = filter_input(INPUT_POST, 'telefone', FILTER_SANITIZE_SPECIAL_CHARS);
    $mensagem = filter_input(INPUT_POST, 'mensagem', FILTER_SANITIZE_SPECIAL_CHARS);

    // Validação básica
    if (empty($nome) || empty($email) || empty($telefone)) {
        // Redireciona de volta com erro (opcional) ou mostra mensagem
        die("Por favor, preencha todos os campos obrigatórios.");
    }

    if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        die("E-mail inválido.");
    }

    // Montagem do corpo do e-mail
    $corpo_email = "
    <h2>Novo Agendamento Solicitado</h2>
    <p><strong>Nome:</strong> $nome</p>
    <p><strong>E-mail:</strong> $email</p>
    <p><strong>Telefone:</strong> $telefone</p>
    <p><strong>Mensagem:</strong><br> $mensagem</p>
    <hr>
    <p><em>Enviado através do formulário do site.</em></p>
    ";

    // Cabeçalhos (Headers) para e-mail HTML
    $headers = "MIME-Version: 1.0" . "\r\n";
    $headers .= "Content-type:text/html;charset=UTF-8" . "\r\n";
    $headers .= "From: Site <noreply@valdaacupuntura.com.br>" . "\r\n";
    $headers .= "Reply-To: $email" . "\r\n";

    // Envio do e-mail
    // Nota: A função mail() requer um servidor de e-mail configurado (ex: Sendmail, Postfix)
    $enviado = mail($destinatario, $assunto_padrao, $corpo_email, $headers);

    if ($enviado) {
        // Redireciona para a página de agradecimento
        header("Location: obrigado.html");
        exit;
    } else {
        echo "Ocorreu um erro ao enviar sua mensagem. Tente novamente mais tarde.";
    }

} else {
    // Se acessar o arquivo diretamente, redireciona para a home
    header("Location: index.html");
    exit;
}
?>
