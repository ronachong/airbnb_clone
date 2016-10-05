// webpack bundles js files into one file for react front-end
// module.exports represents configs for webpack
module.exports = {
    entry: "./js/app.js", // entrypoint for app
    output: {
	// output bundled source code as ./static/bundle.js
	filename: "./static/bundle.js",
	path: __dirname
    },
    module: {
	loaders: [
	    // run babel-loader on all paths matching test regex
	    // (excluding node_modules file) 
	    {
		test: /\.js$/,
		loader: 'babel-loader',
		exclude: /node_modules/,
		query: {
		    presets: ['es2015', 'react']
		}
	]
    }
}
