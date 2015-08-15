/* copies files in a given dir to a target dir */
/* source: https://github.com/yoniholmes/grunt-text-replace */

module.exports = function(grunt) {
grunt.config('replace', {
	main: {
		src: ['<%= dist_path %>/*.html'],
		overwrite: true,
		replacements: [{
			from:"Testing Replacement",
			to: "Replacement Succeeded! (text-replace seems to work ;) )"
		}]
	}
});

grunt.loadNpmTasks('grunt-text-replace'); // enter the full plugin name here (as it is in package.json)

};



