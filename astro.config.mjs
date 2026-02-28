import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';
import partytown from '@astrojs/partytown';
import react from '@astrojs/react';

// https://astro.build/config
export default defineConfig({
    site: "https://valdaacupuntura.com.br",
    integrations: [
        tailwind(),
        react(), // Adicionado para suportar componentes e ícones
        partytown({
            config: {
                forward: ["dataLayer.push"],
            },
        }),
    ],
    build: {
        inlineStylesheets: "auto",
    },
    compressHTML: true,
});