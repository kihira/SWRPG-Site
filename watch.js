const watch = require("node-watch");
const SVGO = require("svgo");
const fs = require("fs");
const path = require("path");
const less = require("less");

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