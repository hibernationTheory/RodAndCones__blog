/* triggers a task when a change is detected at specified folder */
/* source: https://github.com/gruntjs/grunt-contrib-watch */

module.exports = function(grunt) {
grunt.config('watch', {
	watch_all: {
		files:['<%= src_path %>/**/*'],
		tasks:['build']
	}
});

grunt.loadNpmTasks('grunt-contrib-watch'); // enter the full plugin name here (as it is in package.json)

};



