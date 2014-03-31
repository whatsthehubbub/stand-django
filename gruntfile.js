//Gruntfile
module.exports = function(grunt) {

  //Initializing the configuration object
  grunt.initConfig({
    // Task configuration
    concat: {
      options: {
        separator: ';',
      },
      bootstrap: {
        src: [
          './standbase/static/bower_components/bootstrap/dist/js/bootstrap.min.js'
        ],
        dest: './standbase/static/js/bootstrap.min.js',
      },
      jquery: {
        src: [
          './standbase/static/bower_components/jquery/dist/jquery.min.js',
        ],
        dest: './standbase/static/js/jquery.min.js',
      },
    },
    less: {
      development: {
        options: {
          compress: true,  //minifying the result
        },
        files: {
          //compiling base.less into base.css
          "./standbase/static/css/base.css":"./standbase/static/less/base.less"
        }
      }
    }
  });

  // Plugin loading
  grunt.loadNpmTasks('grunt-contrib-concat');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-contrib-less');
  grunt.loadNpmTasks('grunt-contrib-uglify');

  // Task definition
  grunt.registerTask('default', ['watch']);

};