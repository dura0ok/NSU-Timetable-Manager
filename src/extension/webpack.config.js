const path = require('path');
const dotenv = require('dotenv');
const {DefinePlugin} = require('webpack');

dotenv.config();

module.exports = {
    mode: 'production',
    entry: {
        bundle: ['./app.js'],
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