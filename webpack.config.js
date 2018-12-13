const webpack = require('webpack');
const path = require('path');

module.exports = {
  entry: path.join(__dirname, 'way_to_home/static/src/index.js'),
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: ['babel-loader']
      }
    ]
  },
  resolve: {
    extensions: ['*', '.js', '.jsx']
  },
  output: {
    path: path.join(__dirname, 'way_to_home/static/public'),
    publicPath: '/',
    filename: 'bundle.js'
  },
  plugins: [
    new webpack.HotModuleReplacementPlugin()
  ],
  devServer: {
    contentBase: './way_to_home/static/public',
    hot: true
  }
};
