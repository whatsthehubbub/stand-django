//Gruntfile
module.exports = function(grunt) {

  //Initializing the configuration object
  grunt.initConfig({
  	pkg: grunt.file.readJSON('package.json'),

    // Concat JavaScript
    concat: {
      options: {
        separator: ';',
      },
      dist: {
        src: ['./standbase/static/bower_components/jquery/dist/jquery.js', './standbase/static/bower_components/bootstrap/dist/js/*.js'],
        dest: './standbase/static/js/<%= pkg.name %>.js'
      }
    },

    // Uglify JavaScript
    uglify: {
      options: {
        banner: '/*! <%= pkg.name %> <%= grunt.template.today("dd-mm-yyyy") %> */\n'
      },
      dist: {
        files: {
          './standbase/static/js/<%= pkg.name %>.min.js': ['<%= concat.dist.dest %>']
        }
      }
    },

    jshint: {
      // define the files to lint
      files: ['./standbase/static/js/*.js'],
      // configure JSHint
      options: {
        globals: {
          jQuery: true,
        }
      }
    },

    // Translate LESS
    less: {
      development: {
        options: {
          yuicompress: true
        },
        files: {
          "./standbase/static/css/base.css":"./standbase/static/less/base.less"
        }
      }
    },

    watch: {
      src: {
        files: ['<%= jshint.files %>'],
        tasks: ['concat', 'uglify']
      },
      less: {
        files: './standbase/static/less/*.less',
        tasks: ['less'],
        options: {
          livereload: 8000,
      	},
      },
    },

  });

  // Plugin loading
  grunt.loadNpmTasks('grunt-contrib-concat');
  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-contrib-jshint');
  grunt.loadNpmTasks('grunt-contrib-less');
  grunt.loadNpmTasks('grunt-contrib-watch');

  // Task definition
  grunt.registerTask('default', ['watch']);

};