const path = require('path');

module.exports = {

    mode: 'development',

    entry: './way_to_home/static/index.js',

    output: {
        path: path.resolve(__dirname, 'dist'),
        filename: 'bundle.js',
    },

    watch: true,

    watchOptions: {
        aggregateTime: 100
    },

    module: {
        rules: [
              { test: /\.css$/, use: 'css-loader' },
              { test: /\.ts$/, use: 'ts-loader' }
        ]
    },

    devtool: "source-map",

    externals: {
        react: 'react'
    },

    devServer: {
        proxy: {
            '/api': 'http://localhost:8000'
        },
    }
};