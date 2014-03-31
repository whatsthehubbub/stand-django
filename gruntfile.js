//Gruntfile
module.exports = function(grunt) {

  //Initializing the configuration object
  grunt.initConfig({
    // Task configuration
    concat: {
      options: {
        separator: ';',
      },
      js_frontend: {
        src: [
          './standbase/static/bower_components/jquery/dist/jquery.js',
          './standbase/static/bower_components/bootstrap/dist/js/bootstrap.js'
        ],
        dest: './standbase/static/js/base.js',
      },
    },
    less: {
      development: {
        options: {
          compress: true,  //minifying the result
        },
        files: {
          //compiling base.less into base.css
          "./standbase/static/css/base.css":"./standbase/static/css/base.less"
        }
      },
    },
    uglify{
      //...
    },
    phpunit{
      //...
    },
    watch{
      //...
    }
  });

  // Plugin loading

  // Task definition

};