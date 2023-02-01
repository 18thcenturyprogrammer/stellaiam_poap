// i use this config with webpack4

const path = require("path");
const webpack = require("webpack");
const dotenv = require('dotenv');

dotenv.config();

console.log("process.env : ");
console.dir(process.env);




module.exports = (env, argv)=>{
  console.log("argv.mode : ",argv.mode);
  var processEnv;
  if (argv.mode != undefined){
    process.env.NODE_ENV = argv.mode;
    processEnv = process.env
  }else{
    processEnv = process.env;
  }
  console.log("processEnv : ");
  console.dir(processEnv);

  console.log("JSON.stringify(processEnv) : ");
  console.dir(JSON.stringify(processEnv));



  return {
    entry: "./src/index.js",
    output: {
      path: path.resolve(__dirname, "./assets/for_react/js"),
      filename: "[name].js"
    },
    module: {
      rules: [
        {
          test: /\.js$/,
          exclude: /node_modules/,
          use: {
            loader: "babel-loader",
            options:{
              presets: ['@babel/preset-env',"@babel/preset-react"],
              plugins: ['@babel/plugin-proposal-class-properties']
              
            }
          },
        },
        { test: /\.css$/, use: [ 'style-loader', 'css-loader' ] }
      ],
    },
    optimization: {
      minimize: true,
    },
    plugins: [
      new webpack.DefinePlugin({
        "process.env":JSON.stringify(processEnv)
      })
    ],
    
    resolve: {
      fallback: {
        fs: false,
        path: false,
        os: false
      }
    }
  }
};