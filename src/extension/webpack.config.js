const path = require('path');
const dotenv = require('dotenv');
const { DefinePlugin } = require('webpack');

dotenv.config();

module.exports = {
    mode: 'development',
    entry: {
        bundle: ['./app.js', './EnvConfigParser.js', './CellRender.js',
            './ObjectHelper.js', './TimeTableManager.js', './Modal.js'],
    },
    output: {
        filename: '[name].js',
        path: path.resolve(__dirname, 'dist'),
    },
    plugins: [
        new DefinePlugin({
            'process.env': JSON.stringify(dotenv.config().parsed)
        })
    ]
};