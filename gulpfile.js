const {src, dest, parallel, watch} = require('gulp');
const csso = require("gulp-csso");
const svgo = require("gulp-svgo");
const less = require("gulp-less");
const uglify = require('gulp-uglify');
const ts = require("gulp-typescript");

const tsProject = ts.createProject('tsconfig.json');

function tsCompile() {
    return src("assets/ts/**/*.ts")
        .pipe(tsProject())
        .pipe(uglify())
        .pipe(dest("static/js"));
}

function jsMinify() {
    return src("assets/js/**/*.js")
        .pipe(uglify())
        .pipe(dest("static/js"));
}

function fontsCopy() {
    return src("assets/fonts/*")
        .pipe(dest("static/fonts"));
}

function iconsCopy() {
    return src("assets/icons/**")
        .pipe(dest("static/icons"));
}

function imagesCopy() {
    return src("assets/images/**")
        .pipe(dest("static/img"));
}

function svgOptimise() {
    return src("assets/svg/**")
        .pipe(svgo())
        .pipe(dest("static/img"));
}

function lessCompile() {
    return src("assets/less/**")
        .pipe(less())
        .pipe(csso())
        .pipe(dest("static/css"));
}

function cssOptimise() {
    return src("assets/css/**")
        .pipe(csso())
        .pipe(dest("static/css"));
}

exports.build = parallel(
    fontsCopy,
    iconsCopy,
    imagesCopy,
    svgOptimise,
    lessCompile,
    cssOptimise,
    jsMinify,
    tsCompile,
)

exports.watch = () =>
{
    watch("assets/css/*", cssOptimise);
    watch("assets/ts/*", tsCompile);
    watch("assets/svg/*", svgOptimise);
    watch("assets/less/*", lessCompile);
    watch("assets/images/*", imagesCopy);
}

exports.default = exports.build;