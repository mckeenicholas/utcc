import { sveltekit } from "@sveltejs/kit/vite";
import tailwindcss from "@tailwindcss/vite";
import { defineConfig } from "vite";

export default defineConfig({
	fmt: {
		ignorePatterns: [],
		printWidth: 120,
		svelte: {
			indentScriptAndStyle: false,
		},
		sortImports: {
			groups: [
				"type-import",
				["value-builtin", "value-external"],
				"type-internal",
				"value-internal",
				["type-parent", "type-sibling", "type-index"],
				["value-parent", "value-sibling", "value-index"],
				"unknown",
			],
			newlinesBetween: false,
		},
		sortPackageJson: true,
		sortTailwindcss: {
			stylesheet: "./src/app.css",
		},
		useTabs: true,
	},
	plugins: [tailwindcss(), sveltekit()],
	worker: {
		format: "es",
	},
	lint: {
		options: {
			typeAware: true,
			typeCheck: true,
		},
		plugins: ["unicorn", "typescript", "oxc"],
		categories: {
			correctness: "error",
			perf: "error",
			suspicious: "error",
		},
		rules: {
			"eslint/no-await-in-loop": "off",
			"no-console": ["error", { allow: ["error"] }],
			curly: "error",
		},
		globals: {
			$state: "readonly",
			$props: "readonly",
			$derived: "readonly",
			$effect: "readonly",
		},
	},
});
