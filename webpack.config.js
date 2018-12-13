const webpack = require('webpack');
const path = require('path');
const ExtractTextPlugin = require("extract-text-webpack-plugin");

module.exports = {

    entry: path.join(__dirname, 'way_to_home/static/src/index.js'),

    output: {
        path: path.join(__dirname, 'way_to_home/static/public'),
        filename: 'bundle.js',
    },

    module: {
        rules: [
              { test: /\.css$/, use: 'css-loader' },
              { test: /\.(js|jsx)$/, use: 'script-loader' },
        ]
    },
};

module.exports = config;
