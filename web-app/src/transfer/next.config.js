/* eslint-disable */
const withCSS = require('@zeit/next-css')
const withFonts = require('next-fonts')

// fix: prevents error when .css files are required by node
if (typeof require !== 'undefined') {
  require.extensions['.css'] = (file) => {}
}

module.exports = withFonts(
  withCSS()
)
