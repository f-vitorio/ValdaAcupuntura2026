# Tracking — Valda Acupuntura

Documentação técnica de mensuração digital do site.

## Arquitetura

- Framework: **Astro 4 (SSG/static)** + React + Tailwind
- Camada de medição: **Google Tag (gtag.js)** via **Partytown** (web worker, off main thread)
- GA4 Measurement ID: `G-FJW7NC2BW9`
- Conversão no Google Ads: **importação manual** pelo usuário (sem tag AW- no site)

Não utiliza Google Tag Manager. Toda a medição é feita via gtag.js direto.

## Carga do Google Tag

Arquivo: `src/layouts/Layout.astro` (head, linhas ~264-272)

```html
<script type="text/partytown" src="https://www.googletagmanager.com/gtag/js?id=G-FJW7NC2BW9"></script>
<script type="text/partytown">
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-FJW7NC2BW9');
</script>
```

### Forward do Partytown (obrigatório)

`astro.config.mjs` — integração `@astrojs/partytown`:

```js
config: { forward: ["dataLayer.push", "gtag"] }
```

- `dataLayer.push` e `gtag` são expostos no **main thread** como proxies para o worker.
- Sem `"gtag"` no forward, `typeof window.gtag === 'function'` é `false` no main thread e **nenhum evento dispara**. Este é o fix que destravou as microconversões.

## Eventos implementados

Snippet global em `src/layouts/Layout.astro` (final do body), que roda em **todas** as páginas via event delegation.

| Evento | Gatilho | Parâmetros |
|---|---|---|
| `whatsapp_click` | clique em `a[href*="wa.me"]` | `page_path`, `cta_position` |
| `whatsapp_float_click` | clique no botão flutuante (`class*="fixed"`) | `page_path` |
| `phone_click` | clique em `a[href^="tel:"]` | `page_path`, `cta_position` |
| `generate_lead` | clique em WhatsApp de agendamento (href com `utm_campaign=whatsapp_agendamento`) | `lead_type`, `service`, `method`, `page_path`, `cta_position` |

Exemplo de evento enviado:

```js
gtag('event', 'generate_lead', {
  lead_type: 'whatsapp',
  service: 'acupuntura',
  method: 'whatsapp',
  page_path: '/tratamentos/acupuntura-ansiedade/'
});
```

### Lógica do `generate_lead`

Todos os CTAs de agendamento do site usam `utm_campaign=whatsapp_agendamento` no `href`. O snippet dispara `generate_lead` apenas nesses cliques, diferenciando agendamento (conversão) de cliques informativos. O botão flutuante não gera `generate_lead` (não carrega esse utm).

## Conversão primária (GA4 key event)

Para importar manualmente no Google Ads:

1. No GA4 (`G-FJW7NC2BW9`): **Admin → Events → `generate_lead` → Mark as key event**.
2. No Google Ads: **Goals → New conversion action → Import → Google Analytics 4 → `generate_lead`** → marque como *Primary*.
3. Não há tag `AW-` no site; a conversão é atribuída via importação do GA4.

## Microconversões (parâmetros de contexto)

`whatsapp_click`, `whatsapp_float_click` e `phone_click` são sinais de engajamento (não conversão primária). Use-os como eventos secundários no GA4.

## UTMs

Os links `wa.me` já carregam `utm_source`, `utm_medium` e `utm_campaign`. Eles são passados ao GA4 como `source/medium/campaign` no tráfego. O snippet repassa `page_path` e `cta_position` aos eventos, mas não persiste os UTMs no dataLayer (todos os links de agendamento usam o mesmo `utm_campaign=whatsapp_agendamento`).

## Página de agradecimento

`public/obrigado.html` é uma página estática independente do Layout, com o gtag.js carregado diretamente (async, main thread). Não dispara `generate_lead` (não há formulário ativo no site). Manter somente se um formulário voltar a existir.

## Validação

Como não há GTM, a validação é feita no **GA4 DebugView**:

1. Abra `https://valdaacupuntura.com.br/` com a extensão **Google Analytics Debugger** ativada.
2. Vá a **GA4 → Reports → DebugView** (`G-FJW7NC2BW9`).
3. Clique em um CTA de WhatsApp e confira `whatsapp_click` e `generate_lead`.
4. Clique no botão flutuante e confira `whatsapp_float_click`.
5. Clique em um telefone e confira `phone_click`.

Requisito: como o gtag roda em worker do Partytown, o clique deve ocorrer **após** o carregamento do worker (normalmente pronto no `DOMContentLoaded`).

## Observações / não implementado

- **Consent Mode**: não configurado (site não usa banner de cookies). Revisar se a operação exige consentimento.
- **Enhanced Conversions**: não aplicável ao fluxo de lead por WhatsApp (sem coleta de e-mail no envio).
- **Measurement Protocol / conversões offline**: não configurado; a importação manual do GA4 cobre o lead de WhatsApp.
- **page_view**: único por página (gtag config no head; sem carregamento duplicado). Não há SPA.

## Histórico

- 2026-09-05 — Fix do forward do Partytown (`gtag` no main thread); tracking global centralizado no Layout; remoção de tracking duplicado em `precos.astro`; eventos `whatsapp_click`, `whatsapp_float_click`, `phone_click`, `generate_lead`.