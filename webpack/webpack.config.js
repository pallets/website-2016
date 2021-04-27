const path = require('path')
const MiniCssExtractPlugin = require('mini-css-extract-plugin')

module.exports = {
  mode: 'production',
  entry: './js/app.js',
  output: {
    path: path.dirname(__dirname) + '/assets/static',
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: [
              ['@babel/env', {targets: 'defaults'}]
            ]
          }
        }
      },
      {
        test: /\.scss$/,
        use: [
          MiniCssExtractPlugin.loader,
          'css-loader',
          {
            loader: 'postcss-loader',
            options: {postcssOptions: {plugins: ['postcss-preset-env']}}
          },
          'sass-loader'
        ]
      },
      {
        test: /\.(eot|otf|svg|ttf|woff2?)$/,
        type: 'asset/resource',
        generator: {filename: '[name][ext]'}
      }
    ]
  },
  plugins: [
    new MiniCssExtractPlugin()
  ]
}
