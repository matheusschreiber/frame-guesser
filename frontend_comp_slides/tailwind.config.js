/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{html,js,svelte,ts}'],
  theme: {
    fontFamily: {
      sans: [
        'Roboto',
        'system-ui',
        '-apple-system',
      ],
      fredoka: [
        'Fredoka',
        'Roboto'
      ]
    },
    extend: {
      boxShadow: {
        small: ' 0px 1px 27px 0px rgba(0, 0, 0, 0.15)',
        medium: '0px 0px 22px 0px rgba(0, 0, 0, 0.35)',
        heavy: '0px 0px 31px 0px rgba(0, 0, 0, 0.25)'
      },
      backgroundImage: {
        purple: 'linear-gradient(180deg, #351D5B 0%, #2D1652 100%)',
        rankings: 'url(backgrounds/rankings_background.svg)'
      },
      keyframes: {
        colorWarp: {
          '0%, 100%': { color: '#40128B' },
          '50%': { color: '#1F0C3E' },
        }
      },
      animation: {
        colorWarp: 'colorWarp 10s ease-in-out infinite',
      }
    },
    colors: {
      primary: '#40128B',
      secondary: '#432475',
      terciary: '#1F0C3E',
      quaternary: '#432475',
      whitish: '#EFEFEF',
      gray: '#797979',
      lightgray: '#D9D9D9',
      green: '#00EC09',
      yellow: '#EAD83A',
      red: '#EF4343',
      pink: '#DD58D6',
      blue: '#4369EF',
      cyan: '#00DEEC',
    },
  },
  plugins: [],
  corePlugins: {
    // preflight: false,
  }
}

