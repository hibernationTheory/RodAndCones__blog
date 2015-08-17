/* removes target files and/or folders */
/* source: https://github.com/gruntjs/grunt-contrib-sass */

module.exports = function(grunt) {
grunt.config('clean', {
	options:{
		"no-write":false
	},
	"clean":['<%= dist_path %>']
});

grunt.loadNpmTasks('grunt-contrib-clean'); // enter the full plugin name here (as it is in package.json)

};



