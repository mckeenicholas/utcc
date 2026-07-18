import type { Config } from "tailwindcss";
import typography from "@tailwindcss/typography";

export default {
	content: ["./src/**/*.{html,js,svelte,ts}"],

	plugins: [typography],

	theme: {
		extend: {},
	},
} satisfies Config;
