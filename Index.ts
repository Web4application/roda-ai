import esbuild from "rollup-plugin-esbuild";
import { nodeResolve } from "@rollup/plugin-node-resolve";
import commonjs from "@rollup/plugin-commonjs";
import postcss from "rollup-plugin-postcss";
import url from "@rollup/plugin-url";

const input = "./src/index.ts";
const plugins = [
nodeResolve({ preferBuiltins: false, browser: true }),
commonjs(),
esbuild({
include: /\.[jt]sx?$/, // Include .ts, .tsx, .js, .jsx files
minify: process.env.NODE_ENV === 'production',
target: 'es2017', // Specify ECMAScript target version
}),
postcss({
extract: true, // Extract CSS to a separate file
minimize: process.env.NODE_ENV === 'production', // Minify CSS in production
}),
url({
include: ["**/*.svg", "**/*.png", "**/*.jpg", "**/*.gif"], // Handle image assets
limit: 8192, // Inline files smaller than 8KB
emitFiles: true, // Emit files as separate assets
}),
];

export default {
input,
output: {
file: "dist/bundle.js",
format: "cjs", // CommonJS format
sourcemap: true, // Generate source maps
},
plugins,
};
