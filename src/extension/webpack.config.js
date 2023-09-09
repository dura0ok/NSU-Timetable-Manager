const path = require('path');

module.exports = {
  entry: {
    bundle: ['./app.js', './cell.js'],
  },
  output: {
    filename: '[name].js',
    path: path.resolve(__dirname, 'dist'),
  },
};
