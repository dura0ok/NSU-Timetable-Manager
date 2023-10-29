const path = require('path');

module.exports = {
    mode: 'development',
    entry: {
        bundle: ['./app.js', './cell.js', './modal.js', './helper.js', './dataLoader.js', './render.js'],
    },
    output: {
        filename: '[name].js',
        path: path.resolve(__dirname, 'dist'),
    },
};
