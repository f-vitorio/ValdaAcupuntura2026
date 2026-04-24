import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';
import partytown from '@astrojs/partytown';
import react from '@astrojs/react';
import sitemap from '@astrojs/sitemap';

// https://astro.build/config
export default defineConfig({
    site: "https://valdaacupuntura.com.br/",
    trailingSlash: 'always',
    output: 'static',
    integrations: [
        tailwind(),
        react(), // Adicionado para suportar componentes e ícones
        partytown({
            config: {
                forward: ["dataLayer.push"],
            },
        }),
        sitemap({
            changefreq: 'weekly',
            priority: 0.8,
            serialize(item) {
                if (item.url === 'https://valdaacupuntura.com.br/') {
                    item.changefreq = 'daily';
                    item.priority = 1.0;
                } else if (item.url.includes('/precos/')) {
                    item.priority = 0.9;
                } else {
                    item.priority = 0.7;
                    item.changefreq = 'weekly';
                }
                return item;
            },
            lastmod: new Date(),
        }),
    ],
    build: {
        inlineStylesheets: "auto",
    },
    compressHTML: true,
});