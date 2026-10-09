/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./index.html"],
  theme: {
    extend: {
      colors: {
        nile: {
          blue:'#4F6070',
          'blue-dark':'#3A4855',
          'blue-light':'#6B7D8E',
          gold:'#AE9164',
          'gold-light':'#C9A96E',
          'gold-bright':'#E8C88A',
          beige:'#F6F3EE',
          'beige-warm':'#EDE6DA',
          cream:'#FBFAF7',
          ink:'#1a202c',
          muted:'#5A6875'
        }
      },
      fontFamily:{
        script:['"Italianno"','cursive'],
        sans:['"Montserrat"','system-ui','sans-serif'],
        serif:['"Playfair Display"','Georgia','serif']
      },
      boxShadow:{
        soft:'0 4px 24px rgba(79,96,112,.08)',
        medium:'0 8px 40px rgba(79,96,112,.12)',
        gold:'0 8px 32px rgba(174,145,100,.28)',
        'gold-lg':'0 16px 48px rgba(174,145,100,.38)'
      }
    }
  }
}