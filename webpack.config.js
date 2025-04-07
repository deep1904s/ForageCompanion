const path = require("path");

module.exports = {
  mode: "development",
  entry: "./static/index.ts",
  output: {
    filename: "index.js",
    path: path.resolve(__dirname, "static/dist"),
  },
  resolve: {
    extensions: [".ts", ".js"],
  },
  module: {
    rules: [
      {
        test: /\.ts$/,
        use: "ts-loader",
        exclude: /node_modules/,
      },
    ],
  },
  devtool: "source-map",
};
