const path = require('path');
const webpack = require('webpack');
const UglifyJsPlugin = require('uglifyjs-webpack-plugin');

module.exports = {
    entry: {
        table: './assets/ts/table.ts',
        edit: './assets/ts/edit.ts'
    },
    devtool: 'source-map',
    module: {
        rules: [
            {
                test: /\.tsx?$/,
                use: 'ts-loader',
                exclude: /node_modules/
            }
        ]
    },
    plugins: [
        new UglifyJsPlugin({sourceMap: true}),
        new webpack.optimize.CommonsChunkPlugin({name: 'common', async: false})
    ],
    resolve: {
        extensions: ['.ts', '.js']
    },
    output: {
        filename: '[name].bundle.js',
        path: path.resolve(__dirname, 'static', 'js')
    }
};