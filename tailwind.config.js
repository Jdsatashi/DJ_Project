/** @type {import('tailwindcss').Config} */
const {green, emerald} = require("tailwindcss/colors");

module.exports = {
  content: [
      './src/templates/**/*.html',
      './src/post/templates/**/*.html',
      "./node_modules/flowbite/**/*.js"
  ],
  theme: {
    extend: {
            screens: {
                'sm-max': {'max': '767px'},
                'md-max': {'max': '1023px'},
                'lg-max': {'max': '1279px'},
                'xl-max': {'max': '1535px'},
            },
            colors: {
                green: green,
                emerald: emerald,
            }
        },
  },
  plugins: [
      require("flowbite/plugin")
  ],
}
