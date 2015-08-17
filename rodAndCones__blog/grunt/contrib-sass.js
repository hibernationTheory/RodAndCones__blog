/* converts your sass and scss files into css */
/* source: https://github.com/gruntjs/grunt-contrib-sass */

module.exports = function(grunt) {
grunt.config('sass', {
    dist: {
      files: [{
        expand: true,
        cwd: '<%= src_styles_sass_path %>',
        src: ['**/*.scss'],
        dest: '<%= src_styles_css_path %>',
        ext: '.css'
      }]
    }

});

grunt.loadNpmTasks('grunt-contrib-sass'); // enter the full plugin name here (as it is in package.json)

};



