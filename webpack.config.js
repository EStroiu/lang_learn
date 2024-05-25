const path = require('path');

module.exports = {
    entry: './src/index.ts',
    module: {
        rules: [
            {
                test: /\.ts$/,
                use: 'ts-loader',
                exclude: /node_modules/
            },
            {
                test: /\.css$/, // Add this rule
                use: ['style-loader', 'css-loader'],
                exclude: /node_modules/
            },
            {
                test: /\.css$/, // Add this rule
                use: ['style-loader', 'css-loader'],
                include: /node_modules/
            }
        ]
    },
    resolve: {
        extensions: ['.ts', '.js']
    },
    output: {
        filename: 'bundle.js',
        path: path.resolve(__dirname, 'static')
    }
};
