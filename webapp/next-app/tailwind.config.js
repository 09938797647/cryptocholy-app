module.exports = {
  purge: ['./pages/**/*.{js,ts,jsx,tsx}', './components/**/*.{js,ts,jsx,tsx}'],
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {
      colors: {
        'brand': '#007AFF',
        'backgroundColor': '#FFF',
        'borderColor': '#00000012',
        'dark-85': '#262629',
        'transparent-dark-12': '#00000012',
        'transparent-dark-30': '#00000030',
        'transparent-white-12': '#ffffff12',
        'transparent-white-30': '#ffffff30',
      },
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
};