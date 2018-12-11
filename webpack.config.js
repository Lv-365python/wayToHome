const path = require('path');

module.exports = {

    entry: path.join(__dirname, 'way_to_home/static/src/app.js'),

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
