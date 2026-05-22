from django.http import HttpResponse


def home(request):
    return HttpResponse(
        """
        <!doctype html>
        <html lang="pt-BR">
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>VerificaEstagio</title>
            <style>
                body {
                    margin: 0;
                    font-family: Arial, sans-serif;
                    background: #f5f7fb;
                    color: #1f2937;
                }
                main {
                    max-width: 900px;
                    margin: 48px auto;
                    padding: 0 24px;
                }
                h1 {
                    margin-bottom: 8px;
                    font-size: 32px;
                }
                p {
                    margin-top: 0;
                    color: #4b5563;
                }
                .links {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
                    gap: 12px;
                    margin-top: 24px;
                }
                a {
                    display: block;
                    padding: 16px;
                    border: 1px solid #d1d5db;
                    border-radius: 8px;
                    background: #ffffff;
                    color: #111827;
                    text-decoration: none;
                    font-weight: 700;
                }
                a span {
                    display: block;
                    margin-top: 6px;
                    color: #6b7280;
                    font-size: 14px;
                    font-weight: 400;
                }
                a:hover {
                    border-color: #2563eb;
                }
            </style>
        </head>
        <body>
            <main>
                <h1>VerificaEstagio</h1>
                <p>Links rapidos para testar a API local.</p>
                <section class="links">
                    <a href="/api/docs/">Swagger UI<span>Testar endpoints pelo navegador</span></a>
                    <a href="/api/redoc/">ReDoc<span>Documentacao alternativa da API</span></a>
                    <a href="/api/schema/">OpenAPI Schema<span>Schema JSON/YAML gerado pelo DRF</span></a>
                    <a href="/api/">API Root<span>Lista de recursos REST</span></a>
                    <a href="/admin/">Django Admin<span>Painel administrativo</span></a>
                    <a href="/api/auth/register/">Cadastro<span>Endpoint de registro de usuario</span></a>
                    <a href="/api/auth/login/">Login<span>Endpoint de autenticacao</span></a>
                    <a href="/api/contratos/">Contratos<span>CRUD de contratos</span></a>
                    <a href="/api/estagios/">Estagios<span>CRUD de estagios</span></a>
                    <a href="/api/analises/">Analises<span>Resultados de validacao</span></a>
                </section>
            </main>
        </body>
        </html>
        """
    )
