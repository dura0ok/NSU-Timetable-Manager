const path = require('path');
const Dotenv = require('dotenv-webpack');

module.exports = {
    mode: 'development',
    entry: {
        bundle: ['./app.js', './EnvConfigParser.js', './render.js', './ObjectHelper.js', './TimeTableManager.js'],
    },
    output: {
        filename: '[name].js',
        path: path.resolve(__dirname, 'dist'),
    },

    plugins: [
        new Dotenv()
    ]
};
