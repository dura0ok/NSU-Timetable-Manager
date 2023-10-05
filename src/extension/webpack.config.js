const path = require('path');

module.exports = {
 mode: 'development',
  entry: {
    bundle: ['./app.js', './cell.js', './modal.js'],
  },
  output: {
    filename: '[name].js',
    path: path.resolve(__dirname, 'dist'),
  },
};
