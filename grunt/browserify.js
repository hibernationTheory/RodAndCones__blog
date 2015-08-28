/* browserify allows for a module workflow also uses babel to transform content 
which makes it possible to write Ecmascript 6 code */ 

module.exports = function(grunt) {
grunt.config('browserify', {
	options: {
		browserifyOptions: {
        	debug: true,
        	extensions: ['.js', '.json', '.es6'],
        	transform:['babelify']
		}
	},
	dist: {
		files: {
			'<%= dist_js_path %>app_browserify.js': ['<%= dist_js_path %>app.js'],
		},
	},
});

grunt.loadNpmTasks('grunt-browserify');  // enter the full plugin name here (as it is in package.json)

};
    