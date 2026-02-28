/** @type {import('tailwindcss').Config} */
export default {
    content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
    theme: {
        extend: {
            colors: {
                primary: '#2F5C48',
                secondary: '#25D366',
                accent: '#16a34a',
                text: '#374151',
                'bg-light': '#f9fafb',
                'verde-botanico': '#2F5C48',
                'verde-claro': '#E8F5E9',
                'verde-destaque': '#4CAF50',
                'branco-neve': '#FFFFFF',
                'cinza-chumbo': '#374151',
                'cinza-claro': '#F3F4F6',
                'cor-texto': '#4B5563',
            },
            fontFamily: {
                serif: ['"Playfair Display"', 'serif'],
                sans: ['"Inter"', 'sans-serif'],
            },
            animation: {
                'fade-in': 'fadeIn 0.5s ease-out forwards',
                'pulse-slow': 'pulse 3s infinite',
            },
            keyframes: {
                fadeIn: {
                    '0%': { opacity: '0', transform: 'translateY(10px)' },
                    '100%': { opacity: '1', transform: 'translateY(0)' },
                }
            }
        },
    },
    plugins: [],
}
