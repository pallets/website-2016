var webpack = require('webpack');
var path = require('path');
var ExtractTextPlugin = require('extract-text-webpack-plugin');


var options = {
  entry: {
    'app': './js/app.jsx',
    'styles': './scss/main.scss'
  },
  output: {
    path: path.dirname(__dirname) + '/assets/static',
    filename: '[name].js'
  },
  devtool: '#cheap-module-source-map',
  resolve: {
    extensions: ['.jsx', '.js']
  },
  module: {
    loaders: [
      {
        test: /\.jsx?$/,
        exclude: /node_modules/,
        loader: 'babel-loader'
      },
      {
        test: /\.scss$/,
        loader: ExtractTextPlugin.extract({fallback: 'style-loader', use: 'css-loader!sass-loader'})
      },
      {
        test: /\.css$/,
        loader: ExtractTextPlugin.extract({fallback: 'style-loader', use: 'css-loader'})
      },
      {
        test: /\.(woff2?|ttf|eot|svg|png)(\?.*?)?$/,
        loader: 'file-loader'
      }
    ]
  },
  plugins: [
    new webpack.optimize.UglifyJsPlugin(),
    new webpack.ProvidePlugin({
      $: 'jquery',
      jQuery: 'jquery'
    }),
    new ExtractTextPlugin({filename: 'styles.css', allChunks: true})
  ]
};

module.exports = options;
