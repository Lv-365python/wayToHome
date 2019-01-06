const webpack = require('webpack');
const path = require('path');

module.exports = {
  entry: path.join(__dirname, 'way_to_home/static/src/app.js'),
  output: {
    path: path.join(__dirname, 'way_to_home/static/public'),
    publicPath: '/',
    filename: 'bundle.js'
  },
  watch: true,
  resolve: {
    alias: {
      src: path.join(__dirname, 'way_to_home/static/src')
    },
    extensions: ['*', '.js', '.jsx']
  },
  module: {
    rules: [
      {
        test: /\.jsx?/,
        include: path.join(__dirname, 'way_to_home/static/'),
        use: ['babel-loader']
      },
      {
        test: /\.css$/,
        use: ['style-loader', 'css-loader'],
      }
    ]
  },
  plugins: [
    new webpack.HotModuleReplacementPlugin()
  ],
  devServer: {
    contentBase: './way_to_home/static/public',
    watchContentBase: true,
    compress: true,
    hot: true
  }
};
