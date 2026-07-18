import { sveltekit } from "@sveltejs/kit/vite";
import tailwindcss from "@tailwindcss/vite";
import { defineConfig } from "vite";

export default defineConfig({
	// @ts-expect-error - fmt and lint are custom properties for vp tool
	fmt: {
		ignorePatterns: [],
		printWidth: 120,
		sortImports: {
			customGroups: [
				{
					groupName: "svelte",
					elementNamePattern: ["svelte", "svelte/*"],
				},
				{
					groupName: "app",
					elementNamePattern: ["$app", "$app/*"],
				},
				{
					groupName: "lib",
					elementNamePattern: ["$lib", "$lib/*"],
				},
			],
			groups: ["svelte", "app", ["value-builtin", "value-external"], "lib", "unknown"],
			newlinesBetween: false,
		},
		sortPackageJson: true,
		sortTailwindcss: {
			stylesheet: "./src/app.css",
		},
		svelte: {
			indentScriptAndStyle: false,
		},
		useTabs: true,
	},
	plugins: [tailwindcss(), sveltekit()],
	worker: {
		format: "es",
	},
	lint: {
		categories: {
			correctness: "error",
			pedantic: "warn",
			perf: "error",
			style: "warn",
			suspicious: "error",
		},
		globals: {
			$derived: "readonly",
			$effect: "readonly",
			$props: "readonly",
			$state: "readonly",
		},
		options: {
			typeAware: true,
			typeCheck: true,
		},
		plugins: ["unicorn", "typescript", "oxc"],
		rules: {
			curly: "error",
			"eslint/no-await-in-loop": "off",
			"id-length": "off",
			"max-statements": "off",
			"no-console": ["error", { allow: ["error"] }],
			"no-inline-comments": "off",
			"no-magic-numbers": "off",
			"no-null": "off",
			"no-ternary": "off",
			"no-unsafe-assignment": "off",
			"prefer-named-capture-group": "off",
			"prefer-readonly-parameter-types": "off",
			"sort-imports": "off",
			"strict-boolean-expressions": "off",
			"filename-case": "off",
			"sort-keys": "off",
			"max-params": "off",
		},
	},
});
