const watch = require("node-watch");
const SVGO = require("svgo");
const fs = require("fs");
const path = require("path");
const less = require("less");
const uglify = require("uglify-js");

const svgo = new SVGO();

function writeFile(directory, fileName, data) {
    fs.writeFile(path.resolve(__dirname, directory, fileName), data, (err) => {
        if (err) throw err;
    })
}

watch('./assets/svg', {filter: /\.svg$/, recursive: true}, (evt, name) => {
    fs.readFile(name, (err, data) => {
        if (err) {
            console.error(err);
            return;
        }
        svgo.optimize(data)
            .then(result => {
                if (result.error) {
                    console.error(result.error)
                }
                else {
                    const basename = path.basename(name).split(".")[0];
                    writeFile("static/img", basename, result.data);
                    console.log("Optimised " + basename);
                }
            })
            .catch((err) => {
                console.error(err.stack);
            })
    });
});

watch(["./assets/less/style.less", "./assets/less/edit.less"], (evt, name) => {
    fs.readFile(name, 'utf8', (err, data) => {
        less.render(data, {
            sourceMap: {sourceMapFileInline: true},
            paths: [path.dirname(name)],
            filename: path.basename(name)
        })
            .then((result) => {
                const basename = path.basename(name).split(".")[0];
                writeFile("static", `${basename}.css`, result.css);
                // writeFile("static", `${basename}.css.map`, result.map);
                console.info(`Compiled ${path.basename(name)}`)
            })
            .catch((err) => {
                console.error(err.stack);
            })
    });
});

// todo shouldn't watch ./static/js in the future, just parse the typescript output
watch(["./assets/js", "./static/js"], {filter: /(?<!\.min)\.js$/, recursive: true}, (evt, name) => {
    if (!fs.existsSync(name)) return;
    fs.readFile(name, "utf8", (err, data) => {
        const basename = path.basename(name);
        const result = uglify.minify(data, {sourceMap: {filename: basename, url: `${basename}.map`}});
        if (result.error) {
            console.error(result.error.stack);
            return;
        }
        writeFile("static/js", `${basename.slice(0, basename.length - 3)}.min.js`, result.code);
        writeFile("static/js", `${basename.slice(0, basename.length - 3)}.map`, result.map);
        console.info(`Minified ${basename}`)
    })
});