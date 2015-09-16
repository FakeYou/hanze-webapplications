var webpack = require('webpack');

module.exports = {
	entry: [
		'webpack/hot/only-dev-server',
		'./js/app.js'
	],
	output: {
		path: __dirname + '/build',
		filename: 'bundle.js'
	},
	module: {
		loaders: [
			{ test: /\.jsx?$/, loaders: ['react-hot', 'babel'], exclude: /node_modules/ },
			{ test: /\.js$/, loader: 'babel-loader', exclude: /node_modules/ },
			{ test: /\.scss$/, loader: 'style!css!sass' },
			{ test: /\.css$/, loader: 'style!css' }
		]
	},
	plugins: [
		new webpack.NoErrorsPlugin()
	]
};