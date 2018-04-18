const fs = require("fs-extra");
const path = require("path");
const csso = require("csso");
const SVGO = require("svgo");
const less = require("less");
const uglify = require("uglify-js");
const svgo = new SVGO();

function buildImages() {
    fs.ensureDirSync("static/img");

    // PNG images
    fs.copy("assets/images", "static/img/", (err) => {if (err) console.log(err);});

    // SVG
    fs.readdir("./assets/svg", (err, files) => {
        files.forEach((file) => {
            const data = fs.readFileSync(`assets/svg/${file}`);
            svgo.optimize(data)
                .then(result => {
                    if (result.error) { console.error(result.error); }
                    else {
                        fs.outputFile(`static/img/${file}`, result.data);
                        console.log(`Optimised ${file}`)
                    }
                })
                .catch((err) => console.error(err.stack));
        })
    });
}

function minifyCss(data, filename) {
    return csso.minify(data, {filename: filename, comments: false})
}

function buildCss() {
    fs.readdirSync("assets/less").forEach((file) => {
        const data = fs.readFileSync(`assets/less/${file}`, "utf8");
        less.render(data, {
            paths: ["assets/less/"],
            filename: file // need to pass full path to ensure it works with @import
        })
            .then((result) => {
                fs.outputFile(`static/css/${path.parse(file).name}.css`, minifyCss(result.css).css);
                console.info(`Compiled ${file}`)
            })
            .catch((err) => {
                console.error(err.stack);
            });
    });

    fs.readdirSync("./assets/css").forEach((file) => {
        const data = fs.readFileSync(`./assets/css/${file}`, "utf8");
        fs.outputFile(`static/css/${file}`, minifyCss(data).css);
        console.info(`Minified ${file}`)
    });
}

function buildJs() {
    fs.readdirSync("assets/js").forEach((file) => {
        if (file.indexOf(".map") !== -1) return;
        const data = fs.readFileSync(`assets/js/${file}`, "utf8");
        const files = {};
        files[file] = data;
        const result = uglify.minify(files);
        if (result.error) {
            console.error(result.error.stack);
            return;
        }
        fs.outputFile(`static/js/${path.parse(file).name}.min.js`, result.code);
        console.info(`Minified ${file}`)
    });
}

function copyFonts() {
    fs.ensureDirSync("static/fonts");
    fs.copy("assets/fonts", "static/fonts/", (err) => {if (err) console.log(err);});
    console.log("Copied fonts")
}

function copyIcons() {
    fs.ensureDirSync("static/icons");
    fs.copy("assets/icons", "static/icons/", (err) => {if (err) console.log(err);});
    console.log("Copied icons")
}

buildCss();
buildImages();
buildJs();
copyFonts();
copyIcons();