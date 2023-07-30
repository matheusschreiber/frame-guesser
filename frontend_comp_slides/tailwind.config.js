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
        medium: '0px 0px 22px 0px rgba(0, 0, 0, 0.35)',
        heavy: '0px 0px 31px 0px rgba(0, 0, 0, 0.25)'
      },
      backgroundImage: {
        purple: 'linear-gradient(180deg, #351D5B 0%, #2D1652 100%)',
      }
    },
    colors: {
      primary: '#40128B',
      secondary: '#9336B4',
      terciary: '#1F0C3E',
      quaternary: '#432475',
      whitish: '#EFEFEF',
      gray: '#797979',
      green: '#00EC09',
      yellow: '#EAD83A',
      red: '#EF4343',
      blue: '#4369EF',
      cyan: '#00DEEC',
    },
  },
  plugins: [],
  corePlugins: {
    // preflight: false,
  }
}

