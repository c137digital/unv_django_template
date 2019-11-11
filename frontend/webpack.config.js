const path = require('path');

const MiniCssExtractPlugin = require('mini-css-extract-plugin');

const DIST_DIR = path.resolve(
  __dirname, '../src/app/components/site/static/site/'
);

const config = {
  entry: {
    app: __dirname + '/js/app.js',
    libs: __dirname + '/js/libs.js'
  },
  mode: 'development',
  performance: {
    maxEntrypointSize: 512000,
    maxAssetSize: 512000
  },
  output: {
      filename: '[name].js',
      path: DIST_DIR
  },
  plugins: [
    new MiniCssExtractPlugin({
      filename:  '[name].css',
      path: DIST_DIR
    }),
  ],
  module: {
    rules: [
      // {
      //   test: /\.js$/,
      //   exclude: /node_modules/,
      //   loader: 'babel-loader',
      // },
      {
        test: /\.scss$/,
        use: [
          {
            loader: MiniCssExtractPlugin.loader,
            options: { publicPath: '../'},
          },
          'css-loader',
          'sass-loader',
          // 'postcss-loader',
        ],
      },
      {
        test: /\.(gif|png|jpe?g|svg)$/i,
        use: [
          {
            loader: 'url-loader',
            options: {
              fallback: 'file-loader',
              limit: 25000,
              name: '[name].[ext]',
              outputPath: 'img',
              publicPath: '/static/site/img/',
            }
          },
          {
            loader: 'image-webpack-loader',
            options: {
              mozjpeg: {
                mozjpeg: {
                  progressive: true,
                  quality: 65,
                },
                pngquant: {
                  quality: '65-90',
                  speed: 4,
                },
                gifsicle: {
                  interlaced: false,
                },
                webp: {
                  quality: 75,
                },
              },
            },
          }
        ],
      }
    ]
  }
};

module.exports = config;
