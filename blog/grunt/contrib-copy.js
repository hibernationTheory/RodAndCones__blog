/* copies files in a given dir to a target dir */

module.exports = function(grunt) {
grunt.config('copy', {
	main: {
	files: [
		// makes all src relative to cwd 
		{expand: true, cwd: '<%= src_path %>', src: ['**'], dest: '<%= dist_path %>'},
		],
	},
});

grunt.loadNpmTasks('grunt-contrib-copy');  // enter the full plugin name here (as it is in package.json)

};



