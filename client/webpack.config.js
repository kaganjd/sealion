const path = require("path");

module.exports = {
  entry: "./src/index.js",
  output: {
    filename: "main.js",
    path: path.resolve(__dirname, "dist"),
    library: "Sniffer",
    libraryTarget: "umd"
  },
  devServer: {
    contentBase: "./dist"
  },
  mode: "development",
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        loader: "babel-loader",
        options: {
          presets: ["@babel/preset-env"],
          plugins: [
            [
              "@babel/plugin-transform-runtime",
              {
                corejs: false,
                helpers: true,
                regenerator: true,
                useESModules: false
              }
            ]
          ],
          sourceType: "unambiguous"
        }
      }
    ]
  }
};
