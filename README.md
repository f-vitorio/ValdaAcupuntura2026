# Projeto Valda Acupuntura - Astro Refactoring

Este projeto é uma reconstrução do site original utilizando **Astro 4**, **Tailwind CSS** e otimizações focadas em atingir **100/100 no PageSpeed Insights**.

## Estrutura do Projeto

- `src/pages/index.astro`: Página principal contendo todo o conteúdo e estrutura semântica.
- `src/layouts/Layout.astro`: Layout base com metatags, SEO (JSON-LD) e preloads.
- `src/styles/global.css`: Estilos globais e configuração de fontes.
- `src/assets`: Imagens otimizadas automaticamente pelo Astro.
- `public`: Arquivos estáticos (favicon, etc).

## Otimizações Implementadas

1.  **Imagens**: Uso do componente `<Image />` do Astro para conversão automática para WebP e redimensionamento.
2.  **LCP (Largest Contentful Paint)**: Pré-carregamento explícito da imagem Hero e inlining de CSS crítico.
3.  **CLS (Cumulative Layout Shift)**: Espaços reservados para imagens e fontes carregadas corretamente.
4.  **JS Mínimo**: Zero JavaScript de runtime para interatividade básica (Details/Summary nativo para FAQ). GTM (Google Tag Manager) adiado em 3 segundos.
5.  **Tailwind CSS**: Estilização utility-first com purificação automática de CSS não utilizado (Purge).

## Como Rodar Localmente

1.  Entre na pasta do projeto:
    ```bash
    cd astro_project
    ```
2.  Instale as dependências (se ainda não instaladas):
    ```bash
    npm install
    ```
3.  Inicie o servidor de desenvolvimento:
    ```bash
    npm run dev
    ```
    Acesse http://localhost:4321

## Como Gerar para Produção

Para criar a versão estática otimizada para upload (Hostinger, Vercel, Netlify):

```bash
npm run build
```

Os arquivos finais estarão na pasta `dist/`. Basta pegar o conteúdo desta pasta e fazer upload para o `public_html` da sua hospedagem.

## Notas Pós-Deploy

- **.htaccess**: Certifique-se de copiar o arquivo `.htaccess` otimizado (com regras de cache e compressão) para a raiz do servidor junto com os arquivos da pasta `dist`.
- **Cache**: A configuração de cache de longa duração (1 ano) para assets já está no .htaccess sugerido.
